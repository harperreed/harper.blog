---
date: 2024-03-11 11:04:11-05:00
description: मैंने एआई की मदद से अपनी गिट कमिट प्रक्रिया को बदल दिया है, जो स्वचालित
  रूप से अर्थपूर्ण संदेश बना देता है। यह सेटअप llm CLI और गिट हुक्स के बढ़िया एकीकरण
  पर आधारित है, जिससे मेरा समय बचता है। अब रोबॉट मेरे कमिट का दस्तावेज़ तैयार कर रहे
  हैं और मैं आराम से दफ़ा हो सकता हूँ।
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
title: अर्थपूर्ण गिट कमिट संदेश अपने-आप तैयार करने के लिए एलएलएम का उपयोग करें
translationKey: Use an llm to automagically generate meaningful git commit messages
---

_TL;DR: आप ‘pre-commit-msg’ गिट हुक सेट करके `llm` CLI (कमांड-लाइन इंटरफ़ेस) से अपने हालिया कोड-बदलावों का संक्षिप्त सार सीधे कमिट संदेश के रूप में बनवा सकते हैं।_

मुझे अलग-अलग प्रोजेक्ट्स पर हैक करना बेहद पसंद है, लेकिन समझदार कमिट संदेश लिखना मेरी सबसे कमज़ोर आदत है।  
उदाहरण के लिये:  
{{< image src="/images/posts/commits.png" caption="My terrible commit messages" >}}

बेकार कमिट संदेश। मैं तो आलसी हूँ!

## घबराइए मत, LLM आ गये हैं

पहले मेरे दोस्त [Kanno](https://twitter.com/ryankanno?lang=en) ने एक स्निपेट भेजा था, जिससे एक साधारण गिट ऐलियस `git diff` से कमिट संदेश बना देता था। यह ख़ासा मज़बूत था।

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

लेकिन मैं shell-GPT की जगह Simon का [LLM CLI](https://llm.datasette.io/en/stable/) इस्तेमाल करना चाहता था। LLM में मॉडल का बेहतर और व्यापक समर्थन है—लोकल मॉडल, MLX वगैरह तक।

साथ ही, मैं चाहता था कि प्रॉम्प्ट अलग फ़ाइल में रहे ताकि बार-बार `.gitconfig` से छेड़छाड़ न करनी पड़े।

मैंने अपना प्रॉम्प्ट `~/.config/prompts/git-commit-message.txt` में रखा। (ध्यान दें: आगे के उदाहरणों में मैं इसी फ़ाइल को `commit-system-prompt.txt` नाम से बुला रहा हूँ।) यह रहा वह प्रॉम्प्ट:

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

और यह रहा बदला हुआ gpt ऐलियस:

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

यह मेरी ज़रूरत पूरी कर देता था, पर मैं आलसी हूँ, तो थोड़ी और जादूगरी चाहता था।

मैंने [claude](https://claude.ai) से इसे इंटरैक्टिव बनाने को कहा, ताकि अगर कमिट संदेश पसंद न आये तो कमिट रद्द कर सकूँ:

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

यह लगभग सही बैठ गया था। फिर claude से दोबारा पूछा और नतीजा यह निकला:

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

मैंने सोचा काम बन गया, लेकिन अब भी काफ़ी मैनुअल काम बचा था और सब कुछ थोड़ा जुगाड़ू-सा लग रहा था।

## Git Hooked — लॉल!

उस वक़्त मुझे याद आया—गिट हुक!  

मैंने फिर claude से पूछा और उसने `prepare-commit-msg` इवेंट पर चलने वाला एक छोटा-सा स्क्रिप्ट बना दिया।

बढ़िया बात यह है कि अगर आप कमिट संदेश पहले से दे देंगे तो हुक नहीं चलेगा; और अगर अलसाया मन बिना संदेश के कमिट करेगा तो LLM अपना काम कर देगा।

कमिट हुक बेहद सीधा है:

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

# Abort for merge commits
if [ -n "$2" ]; then
  exit 0
fi

# Ensure llm is installed
if ! command -v llm &> /dev/null; then
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
  printf "\\n${RED}Error: 'llm' command failed to generate the commit message:\\n${commit_msg}${NC}\\n\\nManually set the commit message"
  exit 1
fi

# Stop spinner
kill $spin_pid
wait $spin_pid 2>/dev/null
tput cnorm
echo

# Show the message
echo "${BLUE}=== Generated Commit Message ===${NC}"
echo "${GREEN}$commit_msg${NC}"
echo "${BLUE}=================================${NC}"
echo

# Write to the commit-message file
echo "$commit_msg" > "$1"
```

(ChatGPT added the documentation.)

यह चलता है, इसमें स्पिनर है, एरर पकड़ता है और दिखने में भी अच्छा लगता है!

![](/images/posts/llm-commit-hook.gif)

अब जैसे ही मैं बिना संदेश के `git commit` चलाता हूँ, हुक सक्रिय होकर स्टेज किये गये बदलावों का डिफ़ `llm` CLI के पास भेज देता है और पहले से तय सिस्टम प्रॉम्प्ट के आधार पर कमिट संदेश बना देता है। आउटपुट कुछ ऐसा दिखता है:

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

काफ़ी बेहतर! आप [मेरा हुक](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg) और [मेरा प्रॉम्प्ट](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt) मेरी डॉटफ़ाइलों में देख सकते हैं।

इसे `SKIP_LLM_GITHOOK` एनवायरनमेंट वैरिएबल सेट करके अस्थायी तौर पर बंद भी किया जा सकता है।

## सेट-अप कैसे करें!

### 1. `llm` इंस्टॉल करें

निर्देशों के लिये [llm.datasette.io](https://llm.datasette.io/en/stable/) देखें। मैंने `pipx` से इंस्टॉल किया:

```bash
pipx install llm
```

अपनी OpenAI कुंजी और डिफ़ॉल्ट मॉडल सेट करें:

```bash
llm keys set openai
llm models default gpt-4-turbo
```

`llm` CLI बेहतरीन है—कई अलग-अलग मॉडल (लोकल मॉडल भी) और कॉन्टेक्स्ट सपोर्ट करता है; एक बार ज़रूर आज़माएँ।

### 2. प्रॉम्प्ट के लिये नयी डायरेक्टरी बनाएं

```bash
mkdir -p ~/.config/prompts
```

### 3. सिस्टम प्रॉम्प्ट जोड़ें

हुक `~/.config/prompts/commit-system-prompt.txt` फ़ाइल ढूँढ़ेगा। उसमें यह सामग्री रखें:

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

यह प्रॉम्प्ट मेरे लिये बढ़िया चल रहा है—सुझाव हों तो बताइए; फिलहाल इसे v0 मानें।

### 4. ग्लोबल गिट हुक के लिये डायरेक्ट्री बनाएं

```bash
mkdir -p ~/.git_hooks
```

### 5. `prepare-commit-msg` फ़ाइल बनाएं

`~/.git_hooks` में बिना एक्सटेंशन वाली फ़ाइल `prepare-commit-msg` बनाएं।

### 6. फ़ाइल को किसी एडिटर (उदा. “vi या मौत”) में खोलें और ऊपर वाला स्क्रिप्ट चिपकाएं।

### 7. फ़ाइल को executable बनाएं

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Git को अपना ग्लोबल हुक पाथ बताएं

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. कोड लिखें, कुछ बनाएं और फिर कमिट करें 🚀

## काम कैसे करता है — छोटा रीकैप

ऊपर वाला कमांड `core.hooksPath` को `~/.git_hooks` पर सेट कर देता है। अब किसी भी रिपॉज़िटरी में `git commit` चलाने पर Git यही ग्लोबल `prepare-commit-msg` हुक चलाएगा। हुक स्टेज किये गये बदलावों का डिफ़ लेकर `llm` को देता है, जो आपके सिस्टम प्रॉम्प्ट के आधार पर कमिट संदेश बना देता है। आप चाहें तो संदेश देख कर एडिट भी कर सकते हैं।

इस ग्लोबल हुक से हर रिपॉज़िटरी में अलग-अलग सेट-अप करने की ज़रूरत नहीं रहती—बस इतना ध्यान रहे कि `llm` कमांड और `~/.config/prompts/commit-system-prompt.txt` फ़ाइल मौजूद हों।

अगर LLM-जनित संदेश नहीं चाहिए, तो सीधे कमिट करें:  
`git commit -m "fixed issue #420"` — यह हुक बाइपास हो जाएगा।

## यह तो बस एक हैक है — AI हॉलुसिनेट भी कर सकता है

इसे बनाते समय बड़ा मज़ा आया और यह काफ़ी फ़नी है।  

मैंने कभी-कभी इसे अजीब बातें हॉलुसिनेट करते देखा है—अब तक बदलाव तो ठीक बताता है, पर कभी “Fixed issue #54” सरीखा कुछ जोड़ देता है।

ज़िंदगी की तरह, **YMMV** 😉

अगर यह मददगार लगे तो मुझे ई-मेल करें: [harper@modest.com](mailto:harper@modest.com)।