---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description:
    Panduan terperinci tentang alur kerja saya saat ini untuk menggunakan
    LLM guna membangun perangkat lunak, mulai dari brainstorming hingga perencanaan
    dan eksekusi
draft: false
generateSocialImage: true
slug: my-llm-codegen-workflow-atm
tags:
    - LLM
    - coding
    - ai
    - workflow
    - software-development
    - productivity
title: "Alur kerja codegen LLM saya saat ini"
translationKey: My LLM codegen workflow atm
---

_TL;DR: Brainstorm spesifikasi, rencanakan rencana, lalu eksekusi dengan codegen LLM. Loop terpisah. Setelah itu, sulap. ✩₊˚.⋆☾⋆⁺₊✧_

Saya sudah membangun banyak produk kecil dengan LLM. Seru dan bermanfaat, tetapi ada jebakan yang bisa menyita waktu. Beberapa waktu lalu seorang teman bertanya bagaimana saya memakai LLM untuk menulis perangkat lunak. Saya sempat berpikir, “oh boy, berapa lama waktu yang kamu punya!” Maka lahirlah tulisan ini.

(p.s. jika kamu pembenci AI—gulir saja ke bagian akhir)

Saya berbincang dengan banyak teman dev tentang hal ini, dan kami semua punya pendekatan serupa dengan berbagai penyesuaian.

Berikut alur kerja saya. Alur ini lahir dari pengalaman pribadi, obrolan dengan teman-teman (terima kasih [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki), dan [Erik](https://thinks.lol/)), serta berbagai best practice dari sudut-sudut buruk internet [bad](https://news.ycombinator.com/) [places](https://twitter.com).

Metode ini berjalan mulus **SAAT INI**—dua minggu lagi bisa saja tidak berfungsi sama sekali, atau malah dua kali lebih ampuh. `¯\_(ツ)_/¯`

## Ayo mulai

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="Aku selalu merasa gambar hasil AI itu mencurigakan. Sapa, dong, malaikat robot juggalo yang sedang ngoding!" >}}

Ada banyak cara mengembangkan perangkat lunak, tetapi kasus saya biasanya salah satu dari dua:

- Kode greenfield (mulai dari nol)
- Kode legacy (tapi masih “modern”)

Saya akan menunjukkan proses saya untuk kedua jalur tersebut.

## Greenfield

Proses berikut bekerja sangat baik untuk pengembangan greenfield. Ia memberi landasan perencanaan dan dokumentasi yang kokoh, serta memungkinkan eksekusi mudah dalam langkah-langkah kecil.

{{< image src="greenfield.jpg" alt="Green field" caption="Secara teknis memang ada ladang hijau di sebelah kanan. Leica Q, 14/5/2016" >}}

### Langkah 1: Mempertajam ide

Gunakan LLM percakapan untuk mempertajam ide (saya biasa pakai ChatGPT 4o / o3):

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

Saat sesi brainstorming selesai (biasanya akan berakhir dengan sendirinya):

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

Prompt tersebut akan menghasilkan spesifikasi yang cukup solid dan lugas—bisa langsung dipakai di langkah perencanaan. Saya suka menyimpannya sebagai `spec.md` di repo.

> Spesifikasi ini bisa dipakai untuk banyak hal. Di sini kita akan menggunakannya untuk codegen, tetapi saya juga sering memintanya kepada model penalaran agar mencari celah dalam ide (must go deeper!), menyusun white paper, atau membuat model bisnis. Masukkan saja ke riset mendalam dan kamu bisa mendapat dokumen pendukung 10 000 kata.

### Langkah 2: Perencanaan

Ambil spesifikasi tersebut dan kirim ke model penalaran yang mumpuni (`o1*`, `o3*`, `r1`):

(Ini prompt TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(Ini prompt non-TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

Model akan menghasilkan rencana prompt yang bisa dieksekusi dengan aider, cursor, dan sebagainya. Biasanya saya simpan sebagai `prompt_plan.md` di repo.

Lalu saya minta dibuatkan `todo.md` yang bisa dicentang:

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

Simpan saja sebagai `todo.md`.

Alat codegen-mu sebaiknya bisa mencentang `todo.md` saat berjalan—bagus untuk menjaga konteks antarsesi.

#### Hore, rencana!

Sekarang kamu punya rencana dan dokumentasi yang kokoh untuk mengeksekusi proyekmu.

Seluruh proses ini kira-kira memakan waktu **15 menit** saja. Cukup cepat—liar banget, jujur.

### Langkah 3: Eksekusi

Ada banyak opsi untuk eksekusi. Keberhasilan sangat bergantung pada seberapa baik langkah 2 dikerjakan.

Saya sudah memakai alur ini dengan [GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [aider](https://aider.chat/), [cursor](https://www.cursor.com/), [claude engineer](https://github.com/Doriandarko/claude-engineer), [sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [Claude.ai](https://claude.ai), dan sebagainya. Semuanya berjalan cukup mulus.

Namun, saya pribadi paling suka **Claude mentah (raw)** dan Aider.

### Claude

Saya pada dasarnya melakukan _pair programming_ bersama [Claude.ai](https://claude.ai) dan memasukkan setiap prompt satu per satu. Cara ini cukup efektif, meski bolak-balik-nya memang melelahkan.

Saya bertanggung jawab atas kode boilerplate awal dan memastikan tooling terpasang benar. Claude cenderung langsung memuntahkan kode React; jadi memiliki fondasi yang kuat—bahasa, gaya, tooling—sangat membantu.

Saat buntu, saya memakai [repomix](https://github.com/yamadashy/repomix) untuk iterasi (detail nanti).

Alurnya:

- siapkan repo (boilerplate, `uv init`, `cargo init`, dan sebagainya)
- masukkan prompt ke Claude
- salin kode dari Claude.ai ke IDE
- jalankan kode & tes
- …
- jika berhasil, lanjut ke prompt berikutnya
- jika gagal, pakai repomix untuk mengirim codebase ke Claude agar di-debug
- ulang lagi ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) menyenangkan dan unik. Ia pas sekali dengan output langkah 2. Saya bisa melaju jauh dengan usaha minim.

Alurnya mirip, tetapi prompt ditempel ke Aider.

Aider akan “langsung kerjakan” dan saya tinggal main [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/).

> Selingan: Aider melakukan benchmarking model-model codegen baru di [LLM leaderboards](https://aider.chat/docs/leaderboards/). Sumber bagus untuk melihat seefektif apa model terbaru.

Testing dengan Aider lebih santai karena ia akan menjalankan test suite dan men-debug secara otomatis.

Alurnya:

- siapkan repo (boilerplate, `uv init`, `cargo init`, dan sebagainya)
- jalankan Aider
- tempel prompt ke Aider
- tonton Aider menari ♪┏(・o･)┛♪
- Aider menjalankan tes, atau kamu jalankan aplikasi untuk verifikasi
- jika berhasil, lanjut prompt berikutnya
- jika tidak, tanya-jawab dengan Aider sampai beres
- ulang lagi ✩₊˚.⋆☾⋆⁺₊✧

### Hasil

Dengan workflow ini saya telah membangun banyak hal: skrip, aplikasi Expo, tool CLI Rust, dan lain-lain. Berhasil lintas bahasa dan konteks, dan saya menikmatinya.

Jika kamu punya proyek—kecil ataupun besar—yang terus kamu tunda, coba deh. Kamu akan kaget seberapa jauh kemajuan dalam waktu singkat.

Daftar todo hack saya kosong karena semuanya sudah saya bangun. Saya terus memikirkan hal baru dan menyelesaikannya sambil menonton film atau apa pun. Untuk pertama kalinya dalam bertahun-tahun, saya mencicipi bahasa dan alat baru dan memperluas perspektif pemrograman saya.

## Non-greenfield: iterasi, selangkah demi selangkah

Kadang kita tidak berada di greenfield, tetapi perlu menambah fitur atau iterasi pada codebase yang sudah ada.

{{< image src="brownfield.jpg" alt="a brown field" caption="Ini jelas bukan green field. Foto acak dari kamera kakek saya—entah di Uganda tahun 60-an" >}}

Untuk ini, metodenya agak berbeda. Mirip dengan di atas, tetapi perencanaan dilakukan per tugas, bukan untuk seluruh proyek.

### Mendapatkan konteks

Setiap orang yang terjun di AI dev biasanya punya alat berbeda, tetapi intinya kamu perlu sesuatu yang mengambil source code dan menjejalkannya ke LLM secara efisien.

Saat ini saya memakai [repomix](https://github.com/yamadashy/repomix). Di `~/.config/mise/config.toml` global, saya punya koleksi task yang memungkinkan berbagai operasi pada codebase saya ([mise rules](https://mise.jdx.dev/)).

Daftar task LLM:

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

Task tersebut menghasilkan `output.txt` berisi konteks codebase. Jika jumlah token membengkak dan file terlalu besar, saya ubah perintah generate agar mengabaikan bagian yang tidak relevan.

> Salah satu hal menarik dari `mise` adalah task bisa didefinisikan ulang di `.mise.toml` proyek. Selama tetap menghasilkan `output.txt`, semua task LLM saya masih berfungsi. Ini membantu, karena tiap codebase berbeda-beda. Saya sering menimpa langkah `repomix` untuk pola ignore yang lebih luas, atau memakai alat lain yang lebih efektif.

Setelah `output.txt` jadi, saya pipakan ke perintah [LLM](https://github.com/simonw/LLM) untuk berbagai transformasi lalu simpan sebagai file markdown.

Intinya task mise menjalankan `cat output.txt | LLM -t readme-gen > README.md` atau `cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md`. Tidak rumit; perintah `LLM` yang menanggung pekerjaan berat (mendukung berbagai model, menyimpan key, memakai template prompt).

Contoh, kalau butuh review cepat dan menambah coverage tes, langkah saya:

#### Claude

- masuk ke direktori project
- jalankan `mise run LLM:generate_missing_tests`
- buka `missing-tests.md` yang dihasilkan
- salin konteks penuh: `mise run LLM:copy_buffer_bundle`
- tempel itu di Claude bersama isu “missing test” pertama
- salin kode dari Claude ke IDE
- …
- jalankan tes
- ulang lagi ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- masuk ke direktori project
- jalankan Aider (selalu di branch baru untuk kerja Aider)
- jalankan `mise run LLM:generate_missing_tests`
- buka `missing-tests.md`
- tempel isu “missing test” pertama ke Aider
- tonton Aider menari ♪┏(・o･)┛♪
- …
- jalankan tes
- ulang lagi ✩₊˚.⋆☾⋆⁺₊✧

Cara ini cukup ampuh untuk memperbaiki codebase secara bertahap. Tugas kecil maupun besar bisa ditangani.

### Sihir prompt

Hack cepat ini efektif untuk menggali area yang bisa membuat proyek lebih tangguh. Berikut beberapa prompt yang saya gunakan pada codebase yang sudah ada:

#### Code review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply  before writing the code review. Review every part, and don't hallucinate.
```

#### Pembuatan GitHub Issue

(saya masih perlu mengotomatiskan posting issue!)

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Tes yang hilang

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues  will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

Prompt-prompt ini sudah agak _old and busted_ (“boomer prompts”, kalau boleh). Perlu disegarkan. Jika ada ide, beri tahu saya.

## Berseluncur ᨒ↟ 𖠰ᨒ↟ 𖠰

Saat menjelaskan proses ini saya sering bilang, “kamu harus agresif memantau apa yang terjadi karena mudah sekali kebablasan.”

Entah kenapa saya sering mengatakan “over my skis” saat berbicara soal LLM. Rasanya seperti meluncur di salju bubuk yang mulus, lalu tiba-tiba “WHAT THE FUCK IS GOING ON!”, tersesat total dan jatuh dari tebing.

Menurut saya, menambahkan **langkah perencanaan** (seperti pada proses Greenfield di atas) membantu menjaga keadaan tetap terkendali. Setidaknya ada dokumen untuk cek silang. Pengujian juga penting—terutama jika kamu ngoding liar dengan Aider—agar semuanya tetap rapi.

Meski begitu, saya masih sering **over my skis**. Kadang jeda sebentar atau berjalan singkat sudah cukup. Intinya tetap proses pemecahan masalah biasa, hanya dalam kecepatan yang gila.

> Kami sering meminta LLM memasukkan hal konyol ke kode yang sebenarnya tidak begitu konyol. Misalnya, kami memintanya membuat file _lore_ lalu merujuk _lore_ tersebut di antarmuka pengguna—padahal ini hanya tool CLI Python. Tiba-tiba ada lore, antarmuka glitchy, dan lain-lain. Semua itu hanya untuk mengelola cloud function-mu, daftar todo-mu, atau apa pun.

## Saya kesepian (｡•́︿•̀｡)

Keluhan utama saya tentang alur ini: pada dasarnya solo—antarmukanya semuanya _single-player mode_.

Saya pernah bertahun-tahun ngoding sendiri, berpasangan, dan dalam tim. Selalu lebih seru dengan orang lain. Alur ini tidak mudah dipakai ramai-ramai—bot bertabrakan, merge horor, konteks rumit.

Saya benar-benar ingin ada yang memecahkan masalah ini dan membuat ngoding dengan LLM menjadi permainan multipemain, bukan pengalaman hacker solo. Peluangnya besar sekali.

**AYO KERJA!**

## ⴵ Waktu ⴵ

Codegen ini mempercepat jumlah kode yang saya hasilkan sendirian. Tetapi ada efek samping: banyak _downtime_ menunggu LLM selesai menggunakan token.

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="Saya masih ingat ini seperti kemarin" >}}

Sekarang saya mengisi waktu tunggu dengan:

- Memulai proses brainstorming proyek lain
- Mendengarkan piringan hitam
- Main [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/)
- Mengobrol dengan teman dan robot

Senang sekali bisa ngoding seperti ini. Ngoding tanpa henti—hack hack hack.

Saya tak ingat pernah seproduktif ini dalam menulis kode.

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

Banyak teman berkata, “fuck LLMs. Mereka payah di segala hal.” Saya tidak masalah dengan sudut pandang itu; penting untuk bersikap skeptis. Ada segudang alasan membenci AI. Kekhawatiran utama saya soal konsumsi daya dan dampak lingkungan. Tapi… kode harus tetap mengalir, kan? _sigh_.

Jika kamu terbuka belajar tetapi tidak ingin menjadi “programmer cyborg”, saran saya: jangan ubah opinimu dulu, tetapi baca buku Ethan Mollick tentang LLM dan cara memanfaatkannya: [**Co-Intelligence: Living and Working with AI.**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/)

Buku itu menjelaskan manfaat tanpa gaya bro tekno anarko-kapitalis. Sangat membantu, dan saya sudah punya banyak obrolan seru dengan teman-teman yang membacanya. Highly recommended.

Jika kamu skeptis tetapi penasaran, hubungi saya—mari ngobrol tentang kegilaan ini. Saya bisa menunjukkan bagaimana kami memakai LLM, mungkin kita bisa membangun sesuatu bersama.

_thanks to [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com), and [Erik](https://thinks.lol/) for taking a look at this post and suggesting edits. I appreciate it._
