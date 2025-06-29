---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description:
    Panduan mendetail tentang penggunaan asisten AI Claude Code untuk pengembangan
    perangkat lunak, termasuk kiat alur kerja, praktik pengujian, dan contoh praktis
    dari proyek nyata. Mencakup strategi pengkodean defensif, TDD, dan penerapan di
    tim.
draft: false
generateSocialImage: true
slug: basic-claude-code
tags:
    - ai
    - coding
    - claude
    - development
    - automation
    - testing
    - tdd
    - programming
title: Code Claude Dasar
translationKey: Basic Claude Code
---

Gue benar-benar suka sama konsep agentic coding — gila, keren banget di banyak hal.

Sejak gue nulis [tulisan blog yang asli](/2025/02/16/my-llm-codegen-workflow-atm/), banyak hal terjadi di jagat Claude:

- Claude Code
- MCP
- dll

Gue udah nerima ratusan (wat!) email dari orang-orang yang cerita soal workflow mereka dan gimana mereka pakai workflow gue buat jadi selangkah lebih maju. Gue juga udah ngomong di beberapa konferensi dan ngajar beberapa kelas soal codegen. Ternyata komputer kepingin banget mengoreksi “codegen” jadi “codeine” — siapa sangka!

{{< image src="codegen.png"  >}}

Baru-baru ini gue ngobrol sama seorang [teman](https://www.elidedbranches.com/) soal betapa **kita semua bakal kelar** dan **AI bakal ngambil kerjaan kita** (lebih lanjut di postingan terpisah), dan dia bilang, “lo harus nulis postingan soal Claude Code.”

Here we go.

Claude Code rilis delapan hari setelah gue nulis blog workflow pertama, dan — sesuai prediksi — banyak bagian tulisan gue langsung jadi nggak relevan. Sejak itu gue pindah dari Aider ke Claude Code dan nggak pernah nengok lagi. Aider masih gue suka — ada gunanya sendiri — tapi buat sekarang Claude Code lebih membantu.

Claude Code memang kuat, dan jauh — bahkan sangat — lebih mahal.

Workflow gue, secara garis besar, masih sama kayak dulu.

- Gue ngobrol sama `gpt-4o` buat mempertajam ide.
- Gue pakai model penalaran (reasoning model) terbaik yang ada buat bikin spesifikasi — sekarang `o1-pro` atau `o3` (apakah `o1-pro` lebih baik dari `o3`, atau gue cuma ngerasa begitu karena prosesnya lebih lama?).
- Model penalaran itu gue suruh bikin prompt. Nyuruh LLM bikin prompt itu hack yang indah — plus bikin para boomers kesal.
- Gue simpan `spec.md` dan `prompt_plan.md` di root proyek.
- Lalu gue ketik di Claude Code perintah berikut:

```prompt
1. Open **@prompt_plan.md** and identify any prompts not marked as completed.
2. For each incomplete prompt:
    - Double-check if it's truly unfinished (if uncertain, ask for clarification).
    - If you confirm it's already done, skip it.
    - Otherwise, implement it as described.
    - Make sure the tests pass, and the program builds/runs
    - Commit the changes to your repository with a clear commit message.
    - Update **@prompt_plan.md** to mark this prompt as completed.
3. After you finish each prompt, pause and wait for user review or feedback.
4. Repeat with the next unfinished prompt as directed by the user.
```

- Kerennya prompt ini: dia memeriksa `prompt_plan.md`, mencari item yang belum ditandai selesai, lalu mengeksekusi tugas berikutnya. Setelah beres, dia `commit` ke Git, memperbarui `prompt_plan.md`, lalu nanya mau lanjut apa nggak. 🤌
- Gue tinggal selonjoran sambil menjawab `yes` waktu Claude beraksi. Dia bakal muncul lagi minta feedback, dan abrakadabra.
- Sisanya tinggal klik-klik ala Cookie Clicker.

Trik ini jalan mulus banget. Ada beberapa “superpower” yang bisa lo selipkan biar makin nendang.

## Defensive coding!

### Testing

Pengujian dan Test-Driven Development (TDD) itu wajib. Gue sangat menyarankan lo benar-benar membangun praktik TDD yang kokoh.

Gue dulu benci TDD — gue jelek ngejalaninnya dan merasa buang waktu. Gue ternyata salah. LOL. Selama beberapa dekade kami memang nambahin tes ke perusahaan dan proyek, tapi kebanyakan setelah kerjaan inti kelar. Itu masih oke buat manusia.

INI JELEK BUAT ROBOT.

Robot CINTA TDD. Serius — mereka benar-benar melahapnya.

Dengan TDD, lo suruh “teman robot” bikin test dan mock-nya. Prompt berikutnya, lo bikin mock itu jadi implementasi nyata. Robot langsung senang. Ini penangkal paling ampuh buat halusinasi dan scope drift LLM yang pernah gue temui. Benar-benar bantu robot tetap fokus.

### Linting

Gue fans berat linting. `Ruff` mantap, `Biome` keren, `Clippy` lucu (dan namanya kece).

Entah kenapa ROBOT doyan banget jalanin linter yang oke.

Kebiasaan menjalankan linter terus-menerus menyingkirkan banyak bug, bikin kode lebih terawat, dan gampang dibaca. Lo sudah tahu lah.

Tambahkan formatter yang baik, semuanya jadi rapi.

### Pre-commit hooks

Sihir sesungguhnya adalah naro tugas-tugas di atas ke pre-commit hook. Gue rekomendasi paket Python `pre-commit`. Cukup `uv tools install pre-commit`, bikin file `.pre-commit-config.yaml` yang ciamik, dan bam — tiap kali lo `commit`, dia bakal jalanin tes, type checking, linting, dan sebagainya biar kode lo A+++ dan siap jalan lagi.

Hack ini ampuh banget bareng Claude Code. Robot BENEEEER-benar pengen `commit`. Begitu lo suruh dia nulis kode lalu `commit` (kayak di atas), dia bakal bikin perubahan liar, `commit`, terus ngacauin semuanya dan harus benerin sendiri.

Ini menguntungkan karena nggak mengotori GitHub Actions lo dengan linting, formatting, dan type checking yang gagal cuma karena robot lagi “mood”.

> Hal lucu soal Claude: dia sama sekali nggak paham cara pakai `uv` dengan benar. Kalau nggak diawasin, dia bakal `pip install` sana-sini. Dan kalau lo instruksikan pakai `uv`, dia cuma bakal ngetik `uv pip install`. Mungkin AGI nggak jadi rilis Juni. So sad.

### `CLAUDE.md` dan commands

Dua tambahan simpel yang bisa ngeluarin banyak potensi.

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

Gue nyomot [`CLAUDE.md`](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md) dari temen gue [Jesse Vincent](https://fsck.com/) yang udah [bikin filenya super tangguh](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md). Isinya antara lain:

- versi ringan dari “big daddy rule”;
- instruksi cara TDD;
- gaya koding yang gue suka.

> [@clint](https://instagram.com/clintecker) ngatur `CLAUDE.md`-nya supaya manggil dia MR BEEF, dan sekarang dokumentasi kami terselip kalimat: “If you're stuck, stop and ask for help—MR BEEF may know best.” Sambil ngetik ini, gue mutusin `CLAUDE.md` gue bakal manggil gue “Harp Dog.” Itu fitur, bukan bug.

Fitur commands juga keren. Lihat beberapa contohnya di dotfiles gue [di sini](https://github.com/harperreed/dotfiles/tree/master/.claude/commands).

{{< image src="commands.png"  >}}

Dulu gue lebih sering pakai commands, tapi ini cara jitu buat memanfaatkan prompt yang sering dipakai. Lo juga bisa ngirim argumen. Misalnya di command GitHub issue, lo masukin nomor issue: `/user:gh-issue #45`

Claude bakal jalanin skrip “prompt” yang didefinisiin di `gh-issue.md`.

Lo juga bisa naro commands ini di direktori proyek dan bikin `CLAUDE.md` khusus proyek. Gue lakuin ini buat perintah khusus Hugo, Rust, Go, atau JavaScript per proyek.

## "Continue"

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

Kadang gue merasa kayak burung yang dipakai Homer buat nepuk tombol “y”. Gue cuma ngetik “continue” atau tekan panah atas buat nampilin prompt yang sama.

Biasanya rencananya 8–12 langkah. Gue bisa nyelesaiin pengembangan greenfield (proyek baru dari nol) dalam 30–45 menit, terlepas dari kompleksitas atau bahasanya.

Gue ngobrol sama temen gue Bob dan dia nggak percaya. Gue bilang, “sebutkan apa yang mau dibangun, pakai bahasa apa — ayo kita lihat!”

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

Dia jawab, “oke. Sebuah interpreter BASIC dalam C.”

Ini sebenernya kurang ideal — gue nggak bisa C, juga nggak paham cara nulis interpreter. Tapi ya sudahlah.

Gue ikuti langkah-langkah di atas dan Claude Code bekerja dengan baik. Sekarang kami punya [interpreter BASIC yang jalan](https://github.com/harperreed/basic). Versi pertama kelar dalam sejam. Gue utak-atik lagi beberapa jam dan hasilnya lumayan. Dirilis tahun 1982? Mungkin nggak. Lo bisa lihat [prompt plan-nya di sini](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md).

## Tim

Seluruh tim kami lagi pakai Claude Code. Kami semua kurang lebih ngikutin proses di atas dengan banyak penyesuaian pribadi.

Cakupan pengujian kami jauh lebih tinggi dari sebelumnya. Kode kami lebih baik, dan tampaknya sama efektifnya dibanding kode horor yang dulu kami tulis. Seru banget ngeliat orang kerja sambil lihat Claude Code jalan di Ghostty, terminal VS Code, terminal Zed, sampai main di notebook Python.

{{< image src="dril.jpg" >}}

Ada yang punya token seabrek? Tolong bantuin gue bikin anggaran. Keluarga gue sekarat.

## thanks

Buat semua yang terus email gue: seru banget denger cerita workflow dan proyek kalian. Gue benar-benar menghargainya. Keep ’em coming!
