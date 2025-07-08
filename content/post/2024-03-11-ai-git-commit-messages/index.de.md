---
date: 2024-03-11 11:04:11-05:00
description: Ich habe meinen Git-Commit-Prozess revolutioniert, indem ich eine KI
  einsetze, die automatisch aussagekräftige Nachrichten erstellt. Dieses Setup kombiniert
  clever die llm-CLI mit Git-Hooks und spart mir Zeit. Jetzt kann ich mich verpissen,
  während die Roboter meine Commits dokumentieren
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
title: 'Verwende ein LLM, um automatisch aussagekräftige Git-Commit-Nachrichten zu
  erzeugen

  description: Ich habe meinen Git-Commit-Prozess revolutioniert, indem ich eine KI
  einsetze, die automatisch aussagekräftige Nachrichten erstellt. Dieses Setup kombiniert
  clever die llm-CLI mit Git-Hooks und spart mir Zeit. Jetzt kann ich mich verpissen,
  während die Roboter meine Commits dokumentieren'
translationKey: Use an llm to automagically generate meaningful git commit messages
---

_TL;DR: Du kannst einen Git-Hook (`prepare-commit-msg`) einrichten, der die `llm`-CLI aufruft und dir aus deinen letzten Code-Änderungen automatisch eine Commit-Nachricht zusammenstöpselt._

Ich schraube gern an Projekten herum, bin aber echt mies darin, sinnvolle Commits zu schreiben.

{{< image src="/images/posts/commits.png" caption="Meine miesen Commit-Nachrichten" >}}

Miese Commit-Nachrichten. Ich bin faul!

## Keine Panik, jetzt kommen die LLMs!

Ursprünglich hat mir mein Kumpel [Kanno](https://twitter.com/ryankanno?lang=en) einen Schnipsel geschickt, mit dem man per Git-Alias aus dem `git diff` eine Commit-Nachricht generieren konnte – ziemlich robust.

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

Ich wollte allerdings Simons [llm-CLI](https://llm.datasette.io/en/stable/) statt Shell-GPT verwenden. Die llm-CLI unterstützt deutlich mehr Modelle – inklusive lokaler Modelle, MLX usw.

Außerdem wollte ich das System-Prompt extern ablegen, damit ich daran feilen kann, ohne ständig wieder an der `.gitconfig` herumscheißen zu müssen.

Also habe ich mein Prompt unter `~/.config/prompts/git-commit-message.txt` gespeichert. Hier das Prompt:

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

Und hier der aktualisierte GPT-Alias:

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

Der Alias tat genau das, was ich wollte. Aber ich bin faul, also wollte ich noch etwas Magie obendrauf.

Ich bat [Claude](https://claude.ai), das Ganze interaktiver zu machen, damit ich den Commit abbrechen kann, falls die Nachricht Schrott ist.

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

Das war schon verdammt nah dran. Ich fragte Claude noch einmal und wir landeten hier:

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

Damit war ich zufrieden, aber es fühlte sich immer noch zu umständlich und bastelig an.

## Git Hooked

Da fiel es mir wieder ein: Git-Hooks! Lol. Warum mein Hirn sich das gemerkt hat – keine Ahnung!

Ich fragte Claude erneut, und Claude bastelte ein einfaches Skript, das beim `prepare-commit-msg`-Event ausgelöst wird.

Das ist großartig: Wenn du selbst eine Commit-Nachricht angibst, wird der Hook umgangen. Bist du faul, lässt du die Nachricht weg und das LLM springt ein.

Der Git-Hook ist super simpel:

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

(ChatGPT hat die Dokumentation ergänzt)

Und es läuft: mit schicker Spinner-Animation, sauberer Fehlerbehandlung – und das Ganze sieht auch noch gut aus!

![](/images/posts/llm-commit-hook.gif)

Immer wenn ich jetzt ohne Nachricht commit­te, greift der Hook, schickt den Diff ans llm-CLI mit dem zuvor definierten System-Prompt – und die Ausgabe ist richtig nice!

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

Yay. Viel besser! Du findest [meinen Hook](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg) und [mein Prompt](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt) in meinen Dotfiles.

Du kannst den Hook sogar deaktivieren, indem du die Umgebungsvariable `SKIP_LLM_GITHOOK` setzt.

## So richtest du das ein!

### 1. `llm` installieren

Besuche [llm.datasette.io](https://llm.datasette.io/en/stable/) für die Anleitung. Ich habe es mit `pipx` installiert:

```bash
pipx install llm
```

Denk daran, deinen API-Key und das Standardmodell zu setzen.

OpenAI-Key hinterlegen:

```bash
llm keys set openai
```

Standardmodell festlegen:

```bash
llm models default gpt-4-turbo
```

(Die llm-CLI ist großartig: Sie unterstützt viele verschiedene Modelle, auch lokale, und unterschiedliche Kontexte. Lohnt sich auf jeden Fall.)

### 2. Verzeichnis für deine Prompts anlegen

```bash
mkdir -p ~/.config/prompts
```

### 3. System-Prompt hinzufügen

Der Hook sucht in `~/.config/prompts/commit-system-prompt.txt` nach dem System-Prompt. Lege dort eine Datei mit folgendem Inhalt an:

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

Dieses Prompt funktioniert bei mir super – gib Bescheid, falls du Verbesserungen hast. Das hier ist Version 0.

### 4. Globales Git-Hook-Verzeichnis anlegen

```bash
mkdir -p ~/.git_hooks
```

### 5. Datei `prepare-commit-msg` anlegen

```bash
touch ~/.git_hooks/prepare-commit-msg
```

### 6. `prepare-commit-msg` im Editor öffnen (vi oder stirb 😈) und den Hook-Code hineinkopieren

*(siehe oben)*

### 7. Hook ausführbar machen

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Git sagen, wo die Hooks liegen

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. Coden, Dinge bauen, committen

## Wie das Ganze funktioniert

Der oben gezeigte Befehl setzt `core.hooksPath` auf dein globales Git-Hook-Verzeichnis (`~/.git_hooks`).

Immer wenn du jetzt `git commit` in irgendeinem Repo ausführst, wird der globale `prepare-commit-msg`-Hook ausgeführt. Er generiert anhand der gestagten Änderungen eine Commit-Nachricht über die llm-CLI und das System-Prompt aus `~/.config/prompts/commit-system-prompt.txt`.

Durch den globalen Hook hast du diese Funktion in allen Repos, ohne sie jeweils neu einrichten zu müssen. Achte nur darauf, dass die llm-CLI und die Prompt-Datei vorhanden sind.

Workflow: Änderungen wie gewohnt stagen (`git add` oder `git add -p`) und `git commit` ausführen – der Hook erstellt die Nachricht, die du vor dem finalen Commit noch anpassen kannst.

Willst du die LLM-Magie überspringen, committe einfach mit eigener Nachricht:

```bash
git commit -m "fixed issue #420"
```

Das umgeht den Hook.

## Das ist nur ein Hack – KI halluziniert.

Der Bau hat Spaß gemacht, und das Ergebnis ist herrlich witzig.

Ich habe schon urkomische Halluzinationen erlebt. Bislang keine erfundenen Änderungen, aber so Sachen wie „Fixed issue #54“ am Ende.

Wie immer gilt: Your Mileage May Vary (YMMV).

Falls dir das hilft, schreib mir gern eine Mail: [harper@modest.com](mailto:harper@modest.com).