---
date: 2024-03-11 11:04:11-05:00
description: AI를 사용해 의미 있는 메시지를 자동으로 생성함으로써 내 Git 커밋 프로세스를 혁신했다. 이 구성은 llm CLI와 Git
  훅을 멋지게 통합해 내 시간을 절약해 준다. 이제 씨발 로봇들이 내 커밋을 문서화하는 동안 난 딴짓이나 할 수 있다
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
title: LLM을 이용해 마법처럼 자동으로 의미 있는 Git 커밋 메시지 생성하기
translationKey: Use an llm to automagically generate meaningful git commit messages
---

_TL;DR: pre-commit-msg Git 훅을 설정해 `llm` CLI를 호출하면, 최근 코드 변경 사항을 요약한 커밋 메시지를 자동으로 만들 수 있다._

프로젝트를 뚝딱거리며 노는 건 정말 재미있지만, 의미 있는 커밋을 남기는 데는 영 소질이 없다.

예를 들면:  
{{< image src="/images/posts/commits.png" caption="끔찍한 내 커밋 메시지" >}}

Trash commit messages. I am lazy!

## 걱정 마, LLM이 왔으니까

친구 [Kanno](https://twitter.com/ryankanno?lang=en)가 `git diff`로부터 커밋 메시지를 만들어 주는 간단한 Git 별칭을 보내 줬다. 꽤 탄탄했다.

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

하지만 shell-GPT 대신 Simon의 [LLM CLI](https://llm.datasette.io/en/stable/)를 쓰고 싶었다. LLM은 지원 모델이 훨씬 다양하고, 로컬 모델이나 MLX도 사용할 수 있기 때문이다.

또한 프롬프트를 외부에 두면 `.gitconfig`를 반복해서 건드릴 일도 없다.

그래서 `~/.config/prompts/git-commit-message.txt`에 프롬프트를 저장했다. 내용은 다음과 같다.

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

그리고 별칭을 이렇게 바꿨다.

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

원하던 기능은 갖췄지만, 여전히 자동화가 더 필요했다.

[Claude](https://claude.ai)에게 메시지를 확인하고 마음에 들지 않으면 커밋을 중단하도록 해 달라고 부탁했다.

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

거의 다 됐지만 조금 조악해서 Claude에게 다시 부탁했고, 결과는 다음과 같았다.

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

괜찮았지만 아직도 임시 방편 느낌이 강했다.

## Git 훅

그러다 “아, Git 훅이 있지!” 하고 떠올랐다.

Claude에게 다시 요청하자 `prepare-commit-msg` 이벤트에서 작동하는 간단한 훅 스크립트를 만들어 줬다.

커밋 메시지를 직접 입력하면 훅이 건너뛰고, 메시지를 생략하면 LLM이 호출된다.

```bash
#!/bin/sh

# Exit if the `SKIP_LLM_GITHOOK` environment variable is set
if [ -n "$SKIP_LLM_GITHOOK" ]; then
  exit 0
fi

# ANSI color codes for styling the output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Skip for merge commits
[ -n "$2" ] && exit 0

# Check if `llm` is installed
if ! command -v llm >/dev/null 2>&1; then
  echo "${RED}Error: 'llm' command is not installed. Please install it and try again.${NC}"
  exit 1
fi

# Start spinner
spin_animation &
spin_pid=$!

# Generate commit message
if ! commit_msg=$(git diff --cached | llm -s "$(cat ~/.config/prompts/commit-system-prompt.txt)" 2>&1); then
  kill $spin_pid
  wait $spin_pid 2>/dev/null
  tput cnorm
  printf "\\n"
  printf "${RED}Error: 'llm' command failed to generate the commit message:\\n${commit_msg}${NC}\\n\\nManually set the commit message"
  exit 1
fi

# Stop spinner
kill $spin_pid
wait $spin_pid 2>/dev/null
tput cnorm
echo

# Show generated message
echo "${BLUE}=== Generated Commit Message ===${NC}"
echo "${GREEN}$commit_msg${NC}"
echo "${BLUE}=================================${NC}"
echo

# Write message to file
echo "$commit_msg" > "$1"
```

잘 동작하고, 스피너도 있고, 오류도 잡는다!

![](/images/posts/llm-commit-hook.gif)

이제 메시지 없이 `git commit`을 실행하면 훅이 스테이징된 diff를 LLM CLI로 보내고, 지정한 시스템 프롬프트에 따라 깔끔한 커밋 메시지를 만들어 준다.

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

Yay. 훨씬 낫다! [훅](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg)과 [프롬프트](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt)는 공개돼 있다.

환경 변수 `SKIP_LLM_GITHOOK`을 설정하면 훅을 비활성화할 수 있다.

## 설치 방법

### 1. `llm` 설치

[llm.datasette.io](https://llm.datasette.io/en/stable/)의 안내를 참고하자. 필자는 `pipx`를 사용했다.

```bash
pipx install llm
```

설치 후 API 키와 기본 모델을 지정한다.

```bash
llm keys set openai
llm models default gpt-4-turbo
```

### 2. 프롬프트 디렉터리 생성

```bash
mkdir -p ~/.config/prompts
```

### 3. 시스템 프롬프트 추가

훅은 `~/.config/prompts/commit-system-prompt.txt`를 읽는다. 앞서 제시한 내용을 그대로 저장하자.

### 4. 전역 Git 훅 디렉터리 만들기

```bash
mkdir -p ~/.git_hooks
```

### 5. `prepare-commit-msg` 파일 생성

```bash
touch ~/.git_hooks/prepare-commit-msg
```

### 6. 에디터로 열어 위 훅 스크립트를 붙여넣기

### 7. 실행 권한 부여

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Git에 전역 훅 디렉터리 설정

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. 코드를 작성하고, 변경 사항을 스테이징한 뒤 `git commit` 실행

메시지를 생략하면 LLM이 자동으로 메시지를 생성한다. 건너뛰고 싶을 때는 평소처럼 직접 메시지를 입력하면 된다.

```bash
git commit -m "fixed issue #420"
```

## 작동 원리

`core.hooksPath`를 설정하면, 모든 저장소에서 `git commit` 시 전역 `prepare-commit-msg` 훅이 실행된다. 훅은 스테이징된 diff를 `llm`에 보내고, 시스템 프롬프트를 적용해 커밋 메시지를 생성한 뒤 파일에 기록한다.

`llm` 명령과 프롬프트 파일이 올바르게 준비돼 있어야 정상 작동한다.

## 그냥 재미로 만든 해킹—AI는 헛소리도 한다

만들면서 무척 즐거웠다. 가끔은 “Fixed issue #54” 같은 상상력 넘치는 문구를 덧붙이기도 한다. 늘 그렇듯 결과는 상황에 따라 달라질 수 있다.

도움이 됐다면 메일 한 통 부탁한다!  
[harper@modest.com](mailto:harper@modest.com)