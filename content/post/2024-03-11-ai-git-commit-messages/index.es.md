---
date: 2024-03-11 11:04:11-05:00
description: He transformado mi proceso de commits en Git usando una IA para generar
  automáticamente mensajes significativos. Esta configuración implica una ingeniosa
  integración de la CLI de LLM y los hooks de Git, lo que me ahorra tiempo. Ahora
  puedo largarme mientras los robots documentan mis commits
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
title: 'Utiliza un LLM para generar automágicamente mensajes de commit significativos
  en Git

  description: He transformado mi proceso de commits en Git usando una IA para generar
  automáticamente mensajes significativos. Esta configuración implica una ingeniosa
  integración de la CLI de LLM y los hooks de Git, lo que me ahorra tiempo. Ahora
  puedo largarme mientras los robots documentan mis commits'
translationKey: Use an llm to automagically generate meaningful git commit messages
---

_TL;DR: Puedes configurar un hook de git `pre-commit-msg` para que la CLI `llm` genere un resumen de tus cambios recientes y lo use como mensaje de commit._

Me encanta cacharrear con proyectos, pero soy pésimo escribiendo commits que tengan sentido.

{{< image src="/images/posts/commits.png" caption="Mis horribles mensajes de commit" >}}

Mensajes de commit basura. ¡Soy un perezoso!

## Nunca temas, los LLM están aquí

Mi colega [Kanno](https://twitter.com/ryankanno?lang=en) me pasó un fragmento de código que permitía crear un alias de git sencillo para generar un mensaje de commit a partir del `git diff`. Era bastante sólido.

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

Pero yo quería usar la CLI de Simon, [`llm`](https://llm.datasette.io/en/stable/), en lugar de Shell GPT. `llm` admite muchos más modelos y puede usar modelos locales, MLX, etc.

También quería que el *prompt* estuviera guardado externamente para poder iterar sin tener que volver a toquetear el `.gitconfig` una y otra vez.

Así que coloqué mi *prompt* en `~/.config/prompts/git-commit-message.txt`. Este es el *prompt*:

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

Y este es el alias `gpt` actualizado:

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

Con esto obtenía exactamente lo que quería. Sin embargo, sigo siendo perezoso y quería un poco más de magia.

Le pedí a [Claude](https://claude.ai) que lo hiciera más interactivo y que me permitiera abortar el commit si el mensaje no me convencía.

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

Estuvimos muy cerca de que funcionara. Volví a preguntarle a Claude y llegamos a esto:

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

Quedé satisfecho, pero seguía siendo demasiado enrevesado y parcheado.

## Git Hooked

¡Entonces lo recordé! ¡Git hooks! ¿Por qué tengo eso en la cabeza? Quién sabe.

Le pedí a Claude otra vez y preparó un script sencillo que actúa como hook (gancho) y se dispara con el evento `prepare-commit-msg`.

Esto es genial porque, si quieres añadir tu propio mensaje de commit, puedes saltarte el hook. Pero si eres perezoso, dejas el mensaje en blanco y llamará al LLM.

El hook de commit es súper simple:

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

(ChatGPT añadió la documentación)

¡Funciona! ¡Tiene un *spinner*! ¡Captura errores! ¡Y además se ve bonito!

![](/images/posts/llm-commit-hook.gif)

Ahora, cada vez que hago un commit sin mensaje, el hook se ejecuta y envía el `diff` de los cambios a la CLI `llm` con el *prompt* del sistema previamente definido. ¡El resultado queda genial!

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

¡Mucho mejor! Puedes ver [mi hook](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg) y [mi prompt](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt) en mis dotfiles.

Incluso puedes desactivarlo definiendo la variable de entorno `SKIP_LLM_GITHOOK`.

## Cómo configurarlo

### 1. Instala `llm`

Visita [llm.datasette.io](https://llm.datasette.io/en/stable/) para ver las instrucciones. Yo lo instalé con `pipx`:

```bash
pipx install llm
```

Recuerda definir tu clave y el modelo por defecto.

Configura tu clave de OpenAI:

```bash
llm keys set openai
```

Elige el modelo predeterminado:

```bash
llm models default gpt-4-turbo
```

(La CLI `llm` es increíble. Admite un montón de modelos —incluidos locales— y distintos contextos. Vale la pena explorarlo, sin duda).

### 2. Crea un directorio para tus *prompts*

```bash
mkdir -p ~/.config/prompts
```

### 3. Añade tu *prompt* de sistema

El hook buscará en `~/.config/prompts/commit-system-prompt.txt`. Crea el archivo con este contenido:

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

Este *prompt* me funciona de lujo, pero si se te ocurren mejoras, ¡avísame! Lo considero la versión v0.

### 4. Crea un directorio para tus hooks globales de Git

Por ejemplo:

```bash
mkdir -p ~/.git_hooks
```

### 5. Crea `prepare-commit-msg`

```bash
touch ~/.git_hooks/prepare-commit-msg
```

### 6. Abre `prepare-commit-msg` en tu editor favorito (vi or death) y pega el mismo contenido mostrado antes:

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

Puedes ver [el mío en mis dotfiles](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg).

### 7. Haz ejecutable `prepare-commit-msg`

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Configura Git para usar tu directorio global de hooks

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. Programa, construye cosas y luego haz commit de algo

## Explicación de cómo funciona

Ese último comando establece la opción de configuración `core.hooksPath` para que apunte a `~/.git_hooks`.

Ahora, cada vez que ejecutes `git commit` en cualquiera de tus repositorios, Git lanzará el hook global `prepare-commit-msg`. El hook generará el mensaje en base a los cambios ya preparados (*staged*) usando `llm` y el *prompt* en `~/.config/prompts/commit-system-prompt.txt`.

Con un hook global tienes la funcionalidad en todos tus repos sin configurarla uno por uno.

Asegúrate de tener la CLI `llm` y el archivo `~/.config/prompts/commit-system-prompt.txt` correctamente configurados.

Prepara tus cambios con `git add` o `git add -p`, y luego ejecuta `git commit`. El hook generará el mensaje automáticamente, listo para que lo revises antes de confirmar.

Si quieres omitir la generación del mensaje con LLM, simplemente añade tu propio mensaje:  

```bash
git commit -m "fixed issue #420"
```

Con eso parece que se omite el hook de pre-commit.

## Esto es solo un hack. La IA puede alucinar.

Me divertí montando esto y es desternillante.

En ocasiones alucina cosas muy graciosas; de momento no ha inventado cambios, pero hace cosas raras como añadir “Fixed issue #54” al final.

Como todo en la vida, tu kilometraje puede variar (YMMV).

Si te resulta útil, mándame un correo y cuéntame. Mi email es [harper@modest.com](mailto:harper@modest.com).