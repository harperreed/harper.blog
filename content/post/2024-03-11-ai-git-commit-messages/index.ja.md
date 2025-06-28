---
date: 2024-03-11 11:04:11-05:00
description: AIを利用して意味のあるメッセージを自動生成することで、Gitコミットのプロセスを一新しました。この仕組みはllm CLIとGitフックを巧みに統合したもので、時間を節約できます。これで私はサボっている間にロボットがコミットを書いてくれます
draft: false
generateSocialImage: true
tags:
    - git
    - llm
    - commit-messages
    - programming
    - automation
title: LLMを使って意味のあるGitコミットメッセージを自動生成する
translationKey: Use an llm to automagically generate meaningful git commit messages
slug: use-an-llm-to-automagically-generate-meaningful-git-commit-messages
---

_TL;DR: pre-commit-msg Git フックに `llm` CLI を組み込めば、最近のコード変更を要約したコミットメッセージが自動で生成される。_

プロジェクトをいじるのは大好きなのに、意味のあるコミットメッセージを書くのはめちゃくちゃ苦手。自分でも驚くほど怠け者だ。

たとえばこれ:  
{{< image src="/images/posts/commits.png" caption="My terrible commit messages" >}}

コミットメッセージが完全にダメ。

## Never fear, LLMs are here.

友人の [Kanno](https://twitter.com/ryankanno?lang=en) が、`git diff` からコミットメッセージを生成してくれるシンプルな Git エイリアスを送ってくれた。かなりしっかり動く。

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the \'why\' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

けれど自分は shell-gpt ではなく、Simon の [LLM CLI](https://llm.datasette.io/en/stable/) を使いたかった。LLM は対応モデルが豊富で、ローカルモデルや MLX も利用できる。

さらに `.gitconfig` を何度もいじるのは面倒なので、プロンプトは外部ファイルに分けたい。

そこで `~/.config/prompts/git-commit-message.txt` にプロンプトを保存した。内容はこうだ:

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

エイリアスを次のように更新した:

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

これでやりたいことはほとんど実現したが、まだ手間が残る。

そこで [Claude](https://claude.ai) に頼んで、メッセージが気に入らなければコミットを中断できるインタラクティブ版を作ってもらった。

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

あと一歩というところだったので、さらに詰めてこうなった:

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

満足できたけれど、まだゴチャゴチャしている。

## Git Hooked

そこで思い出したのが Git フックだ。

Claude に再度頼んで、`prepare-commit-msg` イベントで動くシンプルなフックを書いてもらった。

メッセージを自分で入力すればフックはスキップされるし、メッセージを省けば LLM が呼ばれる。

フックの内容は以下のとおり:

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
  spinner=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
  while true; do
    for i in "${spinner[@]}"; do
      tput civis
      tput el1
      printf "\\r${YELLOW}%s${NC} Generating LLM commit message..." "$i"
      sleep 0.1
      tput cub 32
    done
  done
}

# Skip on merge commits
if [ -n "$2" ]; then
  exit 0
fi

# Check if the `llm` command is installed
if ! command -v llm &> /dev/null; then
  echo "${RED}Error: 'llm' command is not installed. Please install it and try again.${NC}"
  exit 1
fi

# Start the spinner
spin_animation &
spin_pid=$!

# Generate the commit message
if ! commit_msg=$(git diff --cached | llm -s "$(cat ~/.config/prompts/commit-system-prompt.txt)" 2>&1); then
  kill $spin_pid
  wait $spin_pid 2>/dev/null
  tput cnorm
  printf "\\n"
  printf "${RED}Error: 'llm' command failed to generate the commit message:\\n${commit_msg}${NC}\\n\\nManually set the commit message"
  exit 1
fi

kill $spin_pid
wait $spin_pid 2>/dev/null
tput cnorm
echo

echo "${BLUE}=== Generated Commit Message ===${NC}"
echo "${GREEN}$commit_msg${NC}"
echo "${BLUE}=================================${NC}"
echo

echo "$commit_msg" > "$1"
```

(ChatGPT added the documentation)

ちゃんと動くし、スピナーもエラーハンドリングもあって見た目もいい。

![](/images/posts/llm-commit-hook.gif)

これでメッセージなしで `git commit` するとフックが発火し、ステージした変更を `llm` CLI とシステムプロンプトに送り、コミットメッセージを生成してくれる。出力はこんな感じ:

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

最高だ。自分の [フック](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg) と [プロンプト](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt) は dotfiles に置いてあるので参考にどうぞ。`SKIP_LLM_GITHOOK` 環境変数をセットすれば無効化できる。

## How to set this up!

### 1. Install `llm`.

手順は [llm.datasette.io](https://llm.datasette.io/en/stable/) を参照。自分は `pipx` でインストールした。

```bash
pipx install llm
```

OpenAI のキーとデフォルトモデルを設定:

```bash
llm keys set openai
llm models default gpt-4-turbo
```

(LLM CLI はローカルモデルを含む多数のモデルをサポートしており、試す価値あり)

### 2. Create a new directory for your prompts:

```bash
mkdir -p ~/.config/prompts
```

### 3. Add your system prompt:

フックは `~/.config/prompts/commit-system-prompt.txt` を読み込む。次の内容を保存しよう。

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

これは暫定版 (v0)。改善案があればぜひ教えてほしい。

### 4. Create a new directory for your global Git hooks.

```bash
mkdir -p ~/.git_hooks
```

### 5. Touch the `prepare-commit-msg`

`~/.git_hooks` に拡張子なしで `prepare-commit-msg` ファイルを作成する。

### 6. Open the `prepare-commit-msg` file in a text editor (vi or death) and add the same content as before:

(訳注: “vi or death” は「vi を使うか死ぬかだぜ」というジョーク)

先ほどのシェルスクリプトをそのまま貼り付けて保存。

### 7. Make the `prepare-commit-msg` file executable

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Configure Git to use your global hooks directory

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. Code, build things and then commit something

## Explanation on how it works

`core.hooksPath` を `~/.git_hooks` に設定したことで、どのリポジトリでも `git commit` を実行するとグローバル `prepare-commit-msg` フックが走る。フックはステージした変更を `llm` と `~/.config/prompts/commit-system-prompt.txt` に渡し、生成されたメッセージをコミットメッセージファイルに書き込む。

LLM の生成をスキップしたい場合は、メッセージを付けてコミットすればいい:

```bash
git commit -m "fixed issue #420"
```

## This is just a hack. AI will hallucinate.

作るのはとても楽しかったし笑える。でもときどき「Fixed issue #54」みたいな謎行を付け足すことがある。今のところ変更内容を捏造した例はないけれど、結果は人それぞれだ。

役に立ったらぜひメールしてほしい → [harper@modest.com](mailto:harper@modest.com)
