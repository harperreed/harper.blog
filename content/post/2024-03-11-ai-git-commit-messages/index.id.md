---
date: 2024-03-11 11:04:11-05:00
description: Saya telah mengubah proses commit git saya dengan menggunakan AI untuk
  secara otomatis menghasilkan pesan yang bermakna. Pengaturan ini melibatkan integrasi
  ciamik antara CLI llm dan git hooks, menghemat waktu saya. Sekarang saya bisa cabut
  sementara robot mendokumentasikan commit saya
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
title: Gunakan LLM untuk secara otomatis menghasilkan pesan commit git yang bermakna
translationKey: Use an llm to automagically generate meaningful git commit messages
---

_TL;DR: Lo bisa bikin Git hook `prepare-commit-msg` yang manggil CLI `llm` buat merangkum perubahan kode terbaru sebagai pesan commit._

Gue seneng banget ngoprek proyek, tapi sering kali pesan commit gue kacau-balau.

Contohnya:  
{{< image src="/images/posts/commits.png" caption="Pesan commit gue yang amburadul" >}}

Pesan commit gue sampah. Gue pemalas!

## Jangan panik, LLMs datang menyelamatkan!

Awalnya, temen gue [Kanno](https://twitter.com/ryankanno?lang=en) ngirimin snippet supaya gue punya alias Git simpel yang bisa bikin pesan commit dari `git diff`. Lumayan tangguh.

```bash
# generate comment
gpt = "!f() { git diff $1 | sgpt 'Write concise, informative commit messages: Start with a summary in imperative mood, explain the 'why' behind changes, keep the summary under 50 characters, use bullet points for multiple changes, and reference related issues or tickets. What you write will be passed to git commit -m \"[message]\"'; }; f"
```

Tapi gue pengin pakai [LLM CLI](https://llm.datasette.io/en/stable/) buatan Simon, bukan `shell-gpt`. LLM punya dukungan model jauh lebih banyak—termasuk model lokal, MLX, dan lain-lain.

Selain itu, gue mau prompt-nya disimpen di luar repo biar gampang diutak-atik tanpa harus ngacak-ngacak `.gitconfig` melulu—ribet banget, cuy.

Prompt-nya gue taro di `~/.config/prompts/git-commit-message.txt`. Isinya:

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

Ini alias `gpt` yang udah gue perbarui:

```bash
gpt = "!f() { git diff $1 | llm -s \"$(cat ~/.config/prompts/commit-system-prompt.txt)\" }; f"
```

Persis kayak yang gue mau. Tapi dasar gue malesan, gue masih pengin nambah sedikit sihir lagi.

Gue minta bantuan [Claude](https://claude.ai) supaya lebih interaktif dan bikin gue bisa batalin commit kalau pesannya jelek banget.

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

Ini sudah nyaris banget, sumpah. Setelah ngobrol lagi sama Claude, jadinya begini:

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

Gue sebenarnya sudah puas, tapi semua ini masih terasa terlalu merepotkan dan tambal-sulam.

## Terpancing Git Hook

Terus gue keinget—Git hooks! LOL. Kenapa masih nyangkut di otak? Entahlah!

Gue minta Claude bikin skrip sederhana yang jadi hook untuk event `prepare-commit-msg`.

Keren banget, soalnya kalo mau nulis pesan sendiri tinggal tulis; kalau lagi mager, kosongin aja dan hook bakal manggil LLM.

Hook-nya simpel banget:

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
      printf "\\r${YELLOW}%s${NC} Generating LLM commit message..." "$i"
      sleep 0.1
      tput cub 32
    done
  done
}

# Check if the commit is a merge commit based on the presence of a second argument
if [ -n "$2" ]; then
  exit 0
fi

# Check if the `llm` command is installed
if ! command -v llm &> /dev/null; then
  echo "${RED}Error: 'llm' command is not installed. Please install it and try again.${NC}"
  exit 1
fi

# Start the spinning animation in the background
spin_animation &
spin_pid=$!

# Generate the commit message using `git diff` piped into `llm` command
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

(ChatGPT nambahin dokumentasi)

Skripnya jalan, ada spinner, nangkep error, dan tampilannya kece!

![](/images/posts/llm-commit-hook.gif)

Sekarang tiap kali gue commit tanpa pesan, hook ini jalan, ngirim `diff` ke CLI `llm` dengan system prompt tadi, dan hasilnya kece parah:

```text
🤖💬 AI-powered git commit messages FTW! 🚀🎉
- Updated content/post/2024-03-11-ai-git-commit-messages.md
- Added links to my actual git hook and prompt in dotfiles repo 🔗
- Removed unnecessary code block formatting for the output example 🗑️
- AI is making us lazy devs, but who cares when commit messages are this awesome! 😂👌
```

Jauh lebih baik! Lo bisa cek [hook gue](https://github.com/harperreed/dotfiles/blob/master/.git_hooks/prepare-commit-msg) dan [prompt gue](https://github.com/harperreed/dotfiles/blob/master/.config/prompts/commit-system-prompt.txt) di repo dotfiles.

Mau nonaktifin? Setel aja variabel lingkungan `SKIP_LLM_GITHOOK`.

## Cara Mengaturnya

### 1. Instal `llm`

Kunjungin [llm.datasette.io](https://llm.datasette.io/en/stable/) buat instruksi lengkap. Gue pakai `pipx`:

```bash
pipx install llm
```

Jangan lupa setel API key dan model default.

Atur OpenAI key:

```bash
llm keys set openai
```

Atur model default:

```bash
llm models default gpt-4-turbo
```

(Perintah `llm` keren banget—dukung banyak model, termasuk lokal, plus berbagai konteks. Wajib dicoba!)

### 2. Bikin direktori buat prompt

```bash
mkdir -p ~/.config/prompts
```

### 3. Tambahin system prompt

Hook bakal nyari `~/.config/prompts/commit-system-prompt.txt`. Bikin file itu dengan isi berikut:

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

Prompt ini ampuh buat gue—kalau lo punya saran, kasih tau ya. Anggep aja ini versi 0.

### 4. Bikin direktori buat Git hooks global

```bash
mkdir -p ~/.git_hooks
```

### 5. Sentuh file `prepare-commit-msg`

Bikin file tanpa ekstensi bernama `prepare-commit-msg` di `~/.git_hooks`.

### 6. Buka file itu di editor favorit lo (vi or death, kata penulis) dan tempel skrip hook tadi.

### 7. Jadikan executable

```bash
chmod +x ~/.git_hooks/prepare-commit-msg
```

### 8. Konfigurasi Git biar pakai direktori hooks global

```bash
git config --global core.hooksPath ~/.git_hooks
```

### 9. Ngodinglah, bangun sesuatu, terus commit deh

## Penjelasan Cara Kerja

Perintah tadi ngeset `core.hooksPath` ke `~/.git_hooks`. Jadi setiap lo `git commit` di repo mana pun, Git bakal ngejalanin global `prepare-commit-msg`. Hook ini bakal bikin pesan commit berdasarkan perubahan yang sudah di-stage lewat `llm` dan system prompt di `~/.config/prompts/commit-system-prompt.txt`.

Dengan hook global, fitur ini langsung aktif di semua repo tanpa perlu setup satu-satu.

Pastikan perintah `llm` dan file prompt tadi sudah ada supaya hook-nya lancar.

Kalau mau skip LLM, cukup kasih pesan manual:

```bash
git commit -m "fixed issue #420"
```

Ini bakal ngelewatin hook.

## Ini Cuma Hack—AI Bisa Halusinasi

Gue seneng banget ngerjain ini, hasilnya kadang kocak.

Gue pernah liat dia nambahin hal aneh kayak “Fixed issue #54” di akhir pesan. Jadi, kayak hidup, hasilnya bisa beda-beda.

Kalau ini ngebantu, email gue di [harper@modest.com](mailto:harper@modest.com).