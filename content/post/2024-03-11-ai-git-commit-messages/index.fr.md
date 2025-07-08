---
date: 2024-03-11 11:04:11-05:00
description: J'ai transformé mon processus de commit git en utilisant une IA pour
  générer automatiquement des messages pertinents. Cette configuration implique une
  intégration astucieuse du CLI llm et des hooks git, ce qui me fait gagner du temps.
  Maintenant, je peux foutre le camp pendant que les robots documentent mes commits
draft: false
generateSocialImage: true
slug: use-an-llm-to-automagically-generate-meaningful-git-commit-messages
tags:
- git
- llm
- commit-messages
- programming
- automation
- source-code-management
title: Utiliser un llm pour générer automatiquement des messages de commit git significatifs
translationKey: Use an llm to automagically generate meaningful git commit messages
---

_TL;DR : Vous pouvez configurer un hook git `pre-commit-msg` pour appeler la CLI `llm` et obtenir un résumé de vos dernières modifications de code comme message de commit._

J’adore bidouiller sur des projets, mais je suis vraiment mauvais pour rédiger des commits qui tiennent la route.

{{< image src="/images/posts/commits.png" caption="Mes messages de commit catastrophiques" >}}

Des messages de commit pourris. Je suis paresseux !

## Pas de panique, les LLM sont là

Au départ, mon pote [Kanno](https://twitter.com/ryankanno?lang=en) m’a envoyé un petit bout de config : un alias git qui génère un message de commit à partir du `git diff`. C’était vraiment robuste.

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

Mais je voulais utiliser la [CLI `llm`](https://llm.datasette.io/en/stable/) de Simon à la place de shell gpt : beaucoup plus de modèles, y compris locaux via MLX, etc.

Je tenais aussi à stocker le prompt ailleurs pour pouvoir l’affiner sans avoir à toucher sans cesse à mon `.gitconfig`.

J’ai donc placé mon prompt dans `~/.config/prompts/git-commit-message.txt`. Voici le prompt :

```text
Write short commit messages:
- The first line should be a short summary of the changes
- Remember to mention the files that were changed, and what was changed
- Explain the 'why' behind changes
- Use bullet points for multiple changes
- Tone: Use a LOT of emojis, be funny, and expressive. Feel free to be profane, but don't be offensive
- If there are no changes, or the input is blank - then return a blank string

Think carefully before you write your commit message.

The output format should be:

Summary of changes
- changes
- changes

What you write will be passed directly to git commit -m "[message]"
```

Et voici l’alias `gpt` mis à jour :

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

C’était exactement ce qu’il me fallait. Mais comme je suis paresseux, j’en voulais encore plus.

J’ai demandé à [Claude](https://claude.ai) de rendre le tout interactif et de me laisser annuler le commit si le message généré était nul.

```bash
llm = "!f() { \
    if git diff --quiet $1; then \
        echo \"No changes to commit. Aborting.\"; \
    else \
        commit_msg=$(git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\"); \
        echo \"Commit message:\n$commit_msg\"; \
        read -p \"Do you want to commit with this message? [y/N] \" confirm; \
        if [[ $confirm =~ ^[Yy]$ ]]; then \
            git commit -m \"$commit_msg\"; \
        else \
            echo \"Commit aborted.\"; \
        fi; \
    fi; \
}; f"
```

On y était presque, mais c’était encore un peu bancal.

J’ai relancé Claude et on est arrivés à ceci :

```bash
llm-staged = "!f() { \
    git add -p; \
    if ! git diff --cached --quiet; then \
        commit_msg=$(git diff --cached | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\"); \
        echo \"Commit message:\n$commit_msg\"; \
        read -p \"Do you want to commit with this message? [y/N] \" confirm; \
        if [[ $confirm =~ ^[Yy]$ ]]; then \
            git commit -m \"$commit_msg\"; \
        else \
            git reset HEAD .; \
            echo \"Commit aborted.\"; \
        fi; \
    else \
        echo \"No changes staged for commit. Aborting.\"; \
    fi; \
}; f"
```

J’étais satisfait, mais c’était encore trop de boulot, et ça restait trop rafistolé.

## Git Hooked

Et là, les hooks git me sont revenus en tête — allez savoir !

Je redemande donc à Claude, et il me pond un petit script qui sert de hook déclenché par l’événement `prepare-commit-msg`.

C’est top : si vous ajoutez déjà un message, le hook est ignoré ; si vous êtes paresseux, laissez le champ vide et le LLM s’en charge.

Le hook est ultra simple :

```bash
#!/bin/sh

# Exit if the `SKIP_LLM_GITHOOK` environment variable is set
if [ ! -z "$SKIP_LLM_GITHOOK" ]; then
  exit 0
fi

# ANSI color codes for styling the output
RED='\033[0;31m'    # Sets text to red
GREEN='\033[0;32m'  # Sets text to green
YELLOW='\033[0;33m' # Sets text to yellow
BLUE='\033[0;34m'   # Sets text to blue
NC='\033[0m'        # Resets the text color to default, no color


# Function to display a spinning animation during the LLM processing
spin_animation() {
  # Array of spinner characters for the animation
  spinner=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
  # Infinite loop to keep the animation running
  while true; do
    for i in "${spinner[@]}"; do
      tput civis  # Hide the cursor to enhance the animation appearance
      tput el1    # Clear the line from the cursor to the beginning to display the spinner
      printf "\\r${YELLOW}%s${NC} Generating LLM commit message..." "$i"  # Print the spinner and message
      sleep 0.1   # Delay to control the speed of the animation
      tput cub 32 # Move the cursor back 32 columns to reset the spinner position
    done
  done
}

# Check if the commit is a merge commit based on the presence of a second argument
if [ -n "$2" ]; then
  exit 0  # Exit script if it's a merge commit, no custom message needed
fi

# Check if the `llm` command is installed
if ! command -v llm &> /dev/null; then
  echo "${RED}Error: 'llm' command is not installed. Please install it and try again.${NC}"
  exit 1
fi

# Start the spinning animation in the background
spin_animation &
spin_pid=$!  # Capture the process ID of the spinning animation

# Generate the commit message using `git diff` piped into `llm` command
# The LLM command takes a system prompt from a file as input
if ! commit_msg=$(git diff --cached | llm -s "$(cat ~/.config/prompts/commit-system-prompt.txt)" 2>&1); then
  # Stop the spinning animation by killing its process
  kill $spin_pid
  wait $spin_pid 2>/dev/null  # Wait for the process to terminate and suppress error messages

  # Finalizing output
  tput cnorm  # Show the cursor again
  printf "\\n"  # Move the cursor to the next line

  printf "${RED}Error: 'llm' command failed to generate the commit message:\\n${commit_msg}${NC}\\n\\nManually set the commit message"
  exit 1
fi

# Stop the spinning animation by killing its process
kill $spin_pid
wait $spin_pid 2>/dev/null  # Wait for the process to terminate and suppress error messages

# Finalizing output
tput cnorm  # Show the cursor again
echo  # Move the cursor to the next line

# Display the generated commit message with color-coded headings
echo "${BLUE}=== Generated Commit Message ===${NC}"
echo "${GREEN}$commit_msg${NC}"
echo "${BLUE}=================================${NC}"
echo

# Write the generated commit message to the specified file (usually the commit message file in .git)
echo "$commit_msg" > "$1"
```

(ChatGPT a ajouté la documentation.)

Ça marche ! Il y a un spinner ! Ça gère les erreurs ! Et c’est plutôt joli !

![](/images/posts/llm-commit-hook.gif)

Désormais, chaque fois que je commit sans message, le hook exécute la CLI `llm`, lui envoie le diff des changements ainsi que le system-prompt défini plus haut, et le résultat est impeccable !

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

Yay ! Tellement mieux ! Vous pouvez voir [mon hook](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg) et [mon prompt](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt) dans mes dotfiles.

Vous pouvez même le désactiver en définissant la variable d’environnement `SKIP_LLM_GITHOOK`.

## Comment mettre ça en place !

### 1. Installer `llm`

Rendez-vous sur [llm.datasette.io](https://llm.datasette.io/en/stable/) pour les instructions. De mon côté, j’ai utilisé `pipx` :

```bash
pipx install llm
```

Pensez ensuite à définir votre clé et le modèle par défaut.

Définir la clé OpenAI :

```bash
llm keys set openai
```

Choisir le modèle par défaut :

```bash
llm models default gpt-4-turbo
```

(La CLI `llm` est géniale : elle gère plein de modèles, y compris locaux, et différents contextes. Ça vaut clairement le détour.)

### 2. Créer un répertoire pour vos prompts

```bash
mkdir -p ~/.config/prompts
```

### 3. Ajouter votre _system prompt_

Le hook cherchera `~/.config/prompts/commit-system-prompt.txt`. Créez ce fichier avec le contenu suivant :

```text
Write short commit messages:
- The first line should be a short summary of the changes
- Remember to mention the files that were changed, and what was changed
- Explain the 'why' behind changes
- Use bullet points for multiple changes
- Tone: Use a LOT of emojis, be funny, and expressive. Feel free to be profane, but don't be offensive
- If there are no changes, or the input is blank - then return a blank string

Think carefully before you write your commit message.

The output format should be:

Summary of changes
- changes
- changes

What you write will be passed directly to git commit -m "[message]"
```

Ce prompt me convient parfaitement (version v0). Si vous l’améliorez, dites-le-moi !

### 4. Créer un répertoire pour vos hooks git globaux

```bash
mkdir -p ~/.git_hooks
```

### 5. Créer `prepare-commit-msg`

Dans `~/.git_hooks`, créez un fichier nommé `prepare-commit-msg` (sans extension).

### 6. Ouvrir `prepare-commit-msg` dans un éditeur (vi ou la mort) et coller le contenu du hook

```bash
#!/bin/sh
...
```

(Mon fichier complet est [ici](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg).)

### 7. Rendre le hook exécutable

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Dire à git d’utiliser ce répertoire de hooks

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. Codez, construisez des trucs, puis faites un commit

## Comment ça marche

La commande ci-dessus définit `core.hooksPath` sur `~/.git_hooks`.

À chaque `git commit`, git exécute donc `~/.git_hooks/prepare-commit-msg`. Le hook génère le message à partir du diff indexé via `llm` et le prompt stocké dans `~/.config/prompts/commit-system-prompt.txt`.

Grâce à ce hook global, la génération automatique du message est disponible dans tous vos dépôts sans configuration supplémentaire.

Assurez-vous simplement que la commande `llm` est installée et que le fichier de prompt est au bon endroit.

Vous pouvez continuer à indexer vos changements normalement avec `git add` ou `git add -p`, puis lancer `git commit`. Le hook global se charge de générer le message, prêt à être relu ou édité avant validation.

Si vous voulez contourner la génération LLM, commitez simplement avec un message explicite :

```bash
git commit -m "fixed issue #420"
```

Cela bypassera le hook _prepare-commit-msg_.

## C’est juste un hack. L’IA peut halluciner.

Je me suis bien amusé à construire ça, c’est franchement hilarant.

Il lui arrive d’halluciner des trucs marrants : pour l’instant pas de faux changements, mais parfois des bizarreries comme « Fixed issue #54 » à la fin.

Comme toujours, YMMV (votre expérience peut varier).

Si cela vous aide, envoyez-moi un mail ! [harper@modest.com](mailto:harper@modest.com).