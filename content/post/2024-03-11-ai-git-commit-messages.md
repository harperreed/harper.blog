---
title: Use an llm to automagically generate meaningful git commit messages
date: 2024-03-11T11:04:11-05:00
description: "I've transformed my git commit process by using an AI to automatically generate meaningful messages. This setup involves a nifty integration of the llm CLI and git hooks, saving me time. Now I can fuck off while the robots document my commits"
draft: false
---

*TL;DR: You can set a pre-commit-msg git hook to call the `llm` cli and get a summary of your recent code changes as your commit message.*


I love hacking on projects, but often I am super bad at making commits that make sense.

For instance:
![](/images/posts/commits.png)

Trash commit messages. I am lazy!


## Never fear, LLMs are here.

Originally my buddy [Kanno](https://twitter.com/ryankanno?lang=en) sent me a snippet that would allow you to have a simple git alias that would generate a commit message from the git diff. It was pretty robust.

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

However, I wanted to use Simon’s [LLM cli](https://llm.datasette.io/en/stable/) instead of shell gpt. LLM has way more model support, and can use local models, MLX, etc.

I also wanted the prompt to be stored externally so I could iterate on it without having to fuck with the `.gitconfig` over and over again.

I went ahead and put my prompt in `~/.config/prompts/git-commit-message.txt`. Here is the prompt:

```text
Write concise, informative commit messages:
- Remember to mention the files that were changed, and what was changed
- Start with a summary in imperative mood
- Explain the 'why' behind changes
- Keep the summary under 50 characters
- Use bullet points for multiple changes
- Reference related issues or tickets
- If there are no changes, or the input is blank - then return a blank string

Think carefully before you write your commit message.

What you write will be passed to git commit -m "[message]"
```

And here is the updated gpt alias:

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

This did everything I wanted it to do. However, I am lazy, so I wanted to add a bit more magic.

I asked [claude](https://claude.ai) to make it more interactive and allow me to abort the commit message if it sucked.

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

This was so so close. I asked claude again, and we got to this:

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

I was satisfied, but this was still too much work, and too kludgy.

## Git Hooked

Then I remembered! Git hooks! Lol. Why would I have that in my brain - who knows!

I asked claude again, and they whipped up a simple script that would act as a hook that triggers with the `prepare-commit-msg` event.

This is awesome, cuz if you want to add a git message, you can skip the hook. But if you are lazy, you exclude the message and it will call the LLM.

The commit hook is super simple:

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

(ChatGPT added the documentation)

It works! And has a spinner! And catches errors! And is pretty!

![](/images/posts/llm-commit-hook.gif)

Now, whenever I commit without a message, the commit hook executes and sends the diff of the changes to the llm cli with the system prompt previously defined. The output is really nice!

```text
Feat: Add prepare-commit-msg git hook
- Automatically generate informative commit messages using git diff and LLM
- Skip message generation for merge commits
- Write the generated message to the commit message file
```

Yay. Much better! You can see [mine in my dotfiles](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg).

You can even disable it by setting the `SKIP_LLM_GITHOOK` environment variable.

## How to set this up!

### 1. Install `llm`.

Visit [llm.datasette.io](https://llm.datasette.io/en/stable/) for instructions. I used `pipx` to install it:

```bash
pipx install llm
```

Remember to set your key and default model.

Set your Openai key:
```bash
llm keys set openai
```

Set which model is default:
```bash
llm models default gpt-4-turbo
```

(The `llm` cli is awesome. It supports lots of different models (including local models), and contexts. Worth digging in for sure)

### 2. Create a new directory for your prompts:

```bash
mkdir -p ~/.config/prompts
```

### 3. Add your system prompt:

The hook will look in `~/.config/prompts/commit-system-prompt.txt` for the system prompt. You can create a file with the following content:

```text
Write concise, informative commit messages:
- Remember to mention the files that were changed, and what was changed
- Start with a summary in imperative mood
- Explain the 'why' behind changes
- Keep the summary under 50 characters
- Use bullet points for multiple changes
- Reference related issues or tickets
- If there are no changes, or the input is blank - then return a blank string

Think carefully before you write your commit message.

What you write will be passed to git commit -m "[message]"
```

This prompt worked great for me - but let me know if you have changes. I consider this prompt v0.

### 4. Create a new directory for your global Git hooks.

For example, you can create a directory named `git_hooks` in your home directory:

```bash
mkdir -p ~/.git_hooks
```

### 5. Touch the `prepare-commit-msg`

Create a new file named `prepare-commit-msg` (without any extension) in the `~/.git_hooks` directory.

### 6. Open the `prepare-commit-msg` file in a text editor (vi or death) and add the same content as before:

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

You can see [mine in my dotfiles](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg).


### 7. Make the `prepare-commit-msg` file executable

Run the following command in your terminal:

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Configure Git to use your global hooks directory

Run the following command to set your global hooks directory

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. Code, build things and then commit something


## Explanation on how it works
This command sets the `core.hooksPath` configuration option to your global hooks directory (`~/.git_hooks`).

Now, whenever you run `git commit` in any of your repositories, Git will execute the global `prepare-commit-msg` hook located in `~/.git_hooks/prepare-commit-msg`. The hook will generate the commit message based on the staged changes using the `llm` command and the system prompt from `~/.config/prompts/commit-system-prompt.txt`.

By setting up a global `prepare-commit-msg` hook, you can have the commit message generation functionality available in all your repositories without the need to set it up individually for each repository.

Remember to have the `llm` command and the `~/.config/prompts/commit-system-prompt.txt` file set up correctly for the global hook to work as expected.

With this global hook in place, you can simply stage your changes normally using `git add` or `git add -p`, and then run `git commit`.

The global `prepare-commit-msg` hook will automatically generate the commit message for you, ready for review and editing before finalizing the commit.

If you want to skip the LLM commit message generation, just commit with a message: `git commit -m “fixed issue #420”`. This seems to bypass the pre commit hook.

## This is just a hack. AI will hallucinate.

I had fun building this, and it is hilarious.

I have had it hallucinate hilarious things. Never making up changes (thus far), but doing weird shit like adding “Fixed issue #54” at the end.

Like everything in life, YMMV.

If this is helpful, send me an email and let me know! My email is [harper@modest.com](mailto:harper@modest.com).
