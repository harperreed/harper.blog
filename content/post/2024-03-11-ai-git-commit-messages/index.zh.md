---
date: 2024-03-11 11:04:11-05:00
description: 通过使用 AI 自动生成有意义的提交信息，我彻底改变了我的 Git 提交流程。该方案巧妙地将 llm CLI 与 Git 钩子结合，为我节省了时间。现在机器人替我记录提交，我可以随便浪了
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
title: 使用 LLM 自动生成有意义的 Git 提交信息
translationKey: Use an llm to automagically generate meaningful git commit messages
---

_TL;DR：你可以設定一個 **pre-commit-msg** Git hook，呼叫 `llm` CLI，將最近程式碼變動的摘要直接當成 commit message。_

我超愛隨手 hack 各種專案，但 commit message 常常寫得一團糟。

例如：  
{{< image src="/images/posts/commits.png" caption="My terrible commit messages" >}}

垃圾般的 commit message，只因為我實在太懶。

## 別怕，LLM 來了

我的朋友 [Kanno](https://twitter.com/ryankanno?lang=en) 之前丟給我一段腳本，做成 Git alias，把 `git diff` 餵進 `sgpt` 產生 commit message，挺好用：

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

不過我想改用 Simon 的 [LLM CLI](https://llm.datasette.io/en/stable/)。LLM 支援更多模型，還能跑本地模型、MLX 等等。

我也想把 prompt 獨立存檔，免得老是改 `.gitconfig`。於是我把 prompt 放在 `~/.config/prompts/git-commit-message.txt`，內容如下：

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

接著把 alias 改成：

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

這樣雖然能用了，但我還嫌不夠順手，想再加點魔法。

我請 [Claude](https://claude.ai) 幫我弄成互動式腳本，如果產出的訊息不滿意，可以直接中止提交：

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

這已經非常接近了。我又請 Claude 幫忙，最後我們弄成這樣：

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

好用是好用，但還是太像拼補丁，不夠優雅。

## Git Hook 上場

忽然想起 Git hook！為什麼腦子裡會突然冒出這東西——誰知道！

我再請 Claude 幫忙，它寫了一支 `prepare-commit-msg` hook 腳本。這很方便：如果你手動加 `-m` 會跳過 hook；懶得打訊息，就讓 LLM 代勞。

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

（ChatGPT 自動產生的註解）

它能跑、帶轉圈動畫、還能抓錯誤，顏值也不錯！

![](/images/posts/llm-commit-hook.gif)

現在只要在沒有訊息的情況下執行 `git commit`，hook 就會把 diff 丟給 `llm`，用先前的 prompt 生成漂亮的 commit message：

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

太好了！你可以在這裡看到我的 [hook](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg) 和 [prompt](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt)。

想停用？設定環境變數 `SKIP_LLM_GITHOOK` 就行。

## 如何設定！

### 1. 安裝 `llm`

到 [llm.datasette.io](https://llm.datasette.io/en/stable/) 查看說明。我用 `pipx`：

```bash
pipx install llm
```

設定 OpenAI 金鑰：

```bash
llm keys set openai
```

設定預設模型：

```bash
llm models default gpt-4-turbo
```

`llm` CLI 很強，支援雲端與本地模型，還能切換不同上下文，值得深入研究。

### 2. 建立 prompt 資料夾

```bash
mkdir -p ~/.config/prompts
```

### 3. 新增 system prompt

在 `~/.config/prompts/commit-system-prompt.txt` 中放入以下內容：

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

### 4. 建立全域 Git hooks 目錄

```bash
mkdir -p ~/.git_hooks
```

### 5. 建立 `prepare-commit-msg`

```bash
touch ~/.git_hooks/prepare-commit-msg
```

### 6. 用 vi（vi or death!*）開啟檔案，貼上前述腳本  
\*玩笑說法，意思是「不用 vi 就不寫」。

### 7. 讓它可執行

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. 告訴 Git 使用你的 hooks 目錄

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. 盡情寫程式，然後 `git add`、`git commit`

## 原理

上述指令把 `core.hooksPath` 設為 `~/.git_hooks`。  
之後任何 repo 執行 `git commit`，Git 都會跑全域的 `prepare-commit-msg` hook；它把已 staged 的 diff 丟進 `llm`，用你的 prompt 生成 commit message，直接寫回提交說明檔案。

透過設定全域 `prepare-commit-msg` hook，你可以在所有專案裡自動享受這套 commit message 產生器，無需逐個 repo 重複設定。

記得先裝好 `llm`，並確定 `~/.config/prompts/commit-system-prompt.txt` 存在，否則 hook 會報錯。

有了這個全域 hook，平常只要正常 `git add` 或 `git add -p` 把檔案放進暫存區，再 `git commit` 就行。hook 會自動幫你寫好訊息，提交前還能讓你檢閱、編輯，滿意再存檔。

如果想跳過 LLM，只要：

```bash
git commit -m "fixed issue #420"
```

手動帶 `-m` 似乎就能略過 `prepare-commit-msg` hook。

## 這只是個小 hack，AI 會瞎掰

我做這東西純粹好玩，也很有喜感。

它偶爾會亂加東西。目前沒編造變更，但會在最後添句「Fixed issue #54」之類。

就像人生一樣：YMMV（Your Mileage May Vary，實際效果因人而異）。

如果這工具對你有幫助，寫信讓我知道！harper@modest.com