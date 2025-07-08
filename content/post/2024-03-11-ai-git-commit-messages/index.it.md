---
date: 2024-03-11 11:04:11-05:00
description: Ho trasformato il mio processo di commit su Git usando un'IA per generare
  automaticamente messaggi significativi. Questa configurazione prevede una pratica
  integrazione tra la CLI di LLM e gli hook di Git, facendomi risparmiare tempo. Ora
  posso cazzeggiare mentre i robot documentano i miei commit
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
title: Usa un LLM per generare in modo automagico messaggi di commit Git significativi
translationKey: Use an llm to automagically generate meaningful git commit messages
---

_TL;DR: Puoi configurare un hook di Git pre-commit-msg che richiama la CLI `llm` e usa un riassunto delle tue ultime modifiche di codice come messaggio di commit._

Adoro smanettare sui progetti, ma spesso faccio commit che non hanno alcun senso.

Per esempio:  
{{< image src="/images/posts/commits.png" caption="My terrible commit messages" >}}

Messaggi di commit da cestinare. Sono uno sfaticato!

## Niente paura, arrivano gli LLM.

All’inizio il mio amico [Kanno](https://twitter.com/ryankanno?lang=en) mi ha mandato uno snippet che ti permette di creare un semplice alias di Git in grado di generare il messaggio di commit a partire dal `git diff`. Era piuttosto robusto.

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

Volevo però usare la [CLI `llm`](https://llm.datasette.io/en/stable/) di Simon al posto di Shell-GPT. `llm` supporta molti più modelli, anche locali, MLX, ecc.

Inoltre volevo che il prompt fosse salvato esternamente, così da poterlo modificare senza dover, ogni volta, incasinare il `.gitconfig`.

Ho quindi salvato il mio prompt in `~/.config/prompts/git-commit-message.txt`. Ecco il prompt:

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

Ed ecco l’alias `gpt` aggiornato:

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

Fa esattamente quello che voglio. Ma, essendo pigro, volevo un pizzico di magia in più.

Ho chiesto a [Claude](https://claude.ai) di renderlo interattivo e di permettermi di annullare il commit se il messaggio faceva schifo.

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

Eravamo quasi a posto. Ho chiesto di nuovo a Claude e siamo arrivati a questo:

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

Ero soddisfatto, ma era ancora troppo sbatti e un po’ raffazzonato.

## «Git-Hooked»: completamente agganciato

Poi mi sono ricordato degli hook di Git! LOL. Perché mai li ho ancora in testa? Boh!

Ho chiesto di nuovo a Claude e ha sfornato un semplice script che funge da hook di Git attivato dall’evento `prepare-commit-msg`.

È fantastico, perché se vuoi aggiungere tu il messaggio basta fornirlo e l’hook non parte; se invece sei uno sfaticato, lasci il messaggio vuoto e ci pensa l’LLM.

L’hook di Git è davvero minimale:

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

(ChatGPT ha aggiunto la documentazione)

Funziona! Ha perfino uno spinner! Cattura gli errori! Ed è pure carino!

![](/images/posts/llm-commit-hook.gif)

Ora, ogni volta che fai un commit senza messaggio, l’hook parte, manda il diff alla CLI `llm` con il prompt di sistema e il risultato è bellissimo!

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

Yay. Molto meglio! Puoi dare un’occhiata [al mio hook](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg) e [al mio prompt](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt) nel mio repo di dotfiles.

Puoi persino disabilitarlo impostando la variabile d’ambiente `SKIP_LLM_GITHOOK`.

## Come impostare il tutto!

### 1. Installa `llm`

Visita [llm.datasette.io](https://llm.datasette.io/en/stable/) per le istruzioni. Io l’ho installata con `pipx`:

```bash
pipx install llm
```

Ricorda di impostare la tua chiave e il modello di default.

Imposta la tua chiave OpenAI:

```bash
llm keys set openai
```

Scegli il modello di default:

```bash
llm models default gpt-4-turbo
```

(La CLI `llm` è fantastica. Supporta un sacco di modelli diversi, anche locali, e vari contesti. Vale davvero la pena approfondirla!)

### 2. Crea una cartella per i tuoi prompt

```bash
mkdir -p ~/.config/prompts
```

### 3. Aggiungi il tuo system prompt

L’hook cercherà il prompt in `~/.config/prompts/commit-system-prompt.txt`. Crea il file con il seguente contenuto:

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

Per me funziona alla grande, ma fammi sapere se hai suggerimenti. Considero questo prompt la versione 0.

### 4. Crea una directory per gli hook di Git globali

Ad esempio puoi creare una cartella `git_hooks` nella tua home:

```bash
mkdir -p ~/.git_hooks
```

### 5. Crea il file `prepare-commit-msg`

Crea un nuovo file chiamato `prepare-commit-msg` (senza estensione) dentro `~/.git_hooks`.

### 6. Aprilo con un editor (vi o morte 😜) e incolla il contenuto visto sopra:

```bash
#!/bin/sh
...
```

Puoi vedere [il mio nei dotfiles](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg).

### 7. Rendi eseguibile `prepare-commit-msg`

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Di’ a Git di usare la cartella degli hook globali

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. Scrivi codice, costruisci cose e poi fai il commit

## Spiegazione di come funziona

Il comando precedente imposta l’opzione `core.hooksPath` sulla directory degli hook globali (`~/.git_hooks`).

D’ora in poi, ogni volta che esegui `git commit` in qualunque repository, Git lancerà l’hook globale `prepare-commit-msg` presente in `~/.git_hooks/prepare-commit-msg`. L’hook genererà il messaggio di commit in base alle modifiche in staging usando la CLI `llm` e il prompt di sistema in `~/.config/prompts/commit-system-prompt.txt`.

Grazie all’hook globale hai la generazione automatica dei messaggi in tutti i tuoi repository senza doverla configurare singolarmente.

Assicurati che la CLI `llm` e il file `~/.config/prompts/commit-system-prompt.txt` siano configurati correttamente perché l’hook funzioni a dovere.

Con questo hook globale puoi semplicemente mettere in staging le modifiche con `git add` o `git add -p`, quindi eseguire `git commit`.

Il `prepare-commit-msg` genererà automaticamente il messaggio, pronto per la tua revisione o per eventuali ritocchi prima del commit definitivo.

Se vuoi saltare la generazione tramite LLM, esegui il commit con un messaggio esplicito, ad esempio:  
`git commit -m "fixed issue #420"`. In questo modo verrà bypassato il pre-commit hook.

## È solo un hack. L’IA può allucinare.

Mi sono divertito un sacco a costruirlo ed è esilarante.

Mi è capitato che allucinasse cose divertenti. Finora non si è inventata modifiche, ma a volte aggiunge cose strane come “Fixed issue #54” alla fine.

Come sempre, la tua esperienza può variare (YMMV).

Se ti è utile, mandami una mail! La mia è [harper@modest.com](mailto:harper@modest.com).