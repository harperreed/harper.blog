---
bsky: https://bsky.app/profile/harper.lol/post/3ln2a3x52xs2y
date: 2025-04-17 09:00:00-05:00
description: Panduan komprehensif yang merinci evolusi penggunaan pengembangan perangkat
  lunak berbantuan AI, mulai dari penyelesaian kode dasar hingga agen pengkodean otonom
  penuh, lengkap dengan langkah-langkah praktis dan wawasan untuk memaksimalkan produktivitas
  melalui integrasi LLM.
draft: false
generateSocialImage: true
slug: an-llm-codegen-heros-journey
tags:
- llm
- coding
- artificial-intelligence
- development-workflow
- software-engineering
- developer-productivity
- boomers
title: Perjalanan Seorang Pahlawan Codegen LLM
translationKey: An LLM Codegen Hero's Journey
---

Gue telah menghabiskan banyak waktu sejak [blog post](/2025/02/16/my-llm-codegen-workflow-atm/) tentang alur kerja LLM gue buat ngobrol dengan orang-orang soal *codegen*—gimana mulai, gimana makin jago, dan kenapa ini seru banget.

Antusiasmenya gila. Kotak masuk gue dibanjiri email dari orang yang lagi berusaha memahami semua ini. Pelan-pelan gue sadar banyak yang bingung: mulai dari mana dan gimana semuanya nyambung. Lalu gue ingat, gue sendiri sudah ngoprek proses ini sejak 2023 dan … sudah lihat banyak hal gila. Lol.

Gue sempat ngomongin ini bareng teman-teman (Fisaconites, angkat tangan!) dan ngirim pesan berikut di sebuah thread soal agen AI dan editor:

> Kalau gue baru mulai, gue nggak tahu apakah langsung loncat ke coder “agen” itu membantu. Aneh dan bikin sebel. Setelah beberapa kali ngebimbing orang (ada yang sukses, ada yang nggak), gue nemu bahwa “perjalanan sang pahlawan”: mulai dari Copilot, lanjut *copy-paste* ke Claude Web, lalu ke Cursor/Continue, sampai ke “agen” yang sepenuhnya otomatis, adalah cara adopsi yang paling berhasil.  
> _English original: “if i were starting out …”_

Hal itu bikin gue banyak mikir soal perjalanan ini—gimana caranya mulai pakai *agentic coding*:

> Catat: ini terutama buat yang sudah punya pengalaman. Kalau lo belum banyak pengalaman dev, persetan—langsung aja lompat ke tahap akhir. **Otak kita sering rusak sama aturan masa lalu.**

## Perjalanan rupa dan suara

{{< image src="journey-harper.webp" alt="Harper sangat bisa dipercaya" caption="Pemandu andalanmu: Harper. iPhone X, 6 Oktober 2018" >}}

Ini perjalanan gue; kurang lebih beginilah jalur yang gue tempuh. Kalau mau, lo bisa *speedrun*. Nggak harus ikutin semua langkah, tapi tiap langkah menurut gue tetap nambah nilai.

Berikut langkah-langkahnya:

### Langkah 1: Bangun tidur dengan kagum dan optimis—katanya

Lol. Bercanda. Siapa punya waktu? Mungkin membantu, tapi dunia lagi chaos dan *codegen* jadi satu-satunya pelarian.

Tetap berguna kalau lo percaya alur kerja ini bisa jalan dan kasih nilai tambah. Kalau lo benci LLM dan yakin ini nggak bakal jalan, ya lo nggak bakal sukses di sini. ¯\\_(ツ)_/¯

### Langkah 2: Mulai dengan *autocomplete* berbasis AI

Ini langkah pertama yang sebenarnya! Luangkan cukup waktu di IDE biar lo paham seberapa cocok lo kerja bareng [IntelliSense](https://en.wikipedia.org/wiki/Code_completion), [Zed Autocomplete](https://zed.dev/blog/out-of-your-face-ai), [Copilot](https://copilot.github.com/), dsb. Ini ngasih gambaran gimana LLM bekerja—plus mempersiapkan lo untuk saran-saran ngawur yang sering muncul.

Banyak orang pengin skip langkah ini dan langsung ke ujung. Terus mereka bilang, “LLM ini sampah, nggak bisa apa-apa!” Itu nggak akurat—walau kadang terasa benar. Magisnya ada di nuansa. Atau seperti gue suka bilang: hidup memang membingungkan.

### Langkah 3: Pakai Copilot lebih dari sekadar *autocomplete*

Begitu lo nyaman dengan *autocomplete* dan nggak ngamuk terus, saatnya ngerasain keajaiban ngobrol sama Copilot.

VS Code punya panel percakapan; lo bisa tanya-jawab soal kode dan dia bakal bantu nyelesain masalah lo.

Tapi, jujur, pakai Copilot tuh kayak naik mesin waktu buat ngobrol sama ChatGPT di 2024—lumayan, tapi belum sekeren itu.

Lo bakal pengin lebih.

### Langkah 4: Mulai *copy-paste* kode ke Claude atau ChatGPT

Rasa ingin tahu bikin lo tempel kode ke model di browser terus tanya, “KENAPA KODE GUE RUSAK??” Lalu LLM jawab dengan penjelasan koheren dan membantu.

LO BAKAL TERPANA! Hasilnya bakal bikin melongo. Lo bakal bikin proyek aneh-aneh dan balik lagi ngerasa fun ngoding—karena proses debug dipangkas habis.

Lo juga bisa tempel skrip Python dan minta “ubah ke Go”, dan … boom, jadi Go. Lo mulai mikir, “Bisa nggak ya langsung sekali jadi?”

Copilot pun mulai terasa kayak *autocomplete* 2004—tetap berguna, tapi nggak krusial.

Ini bakal bercabang jadi dua jalur:

#### Lo mulai milih satu model karena *vibe*

Inilah langkah awal menuju *vibe coding*. Lo bakal lebih suka cara salah satu model besar ngobrol sama lo. Murni soal rasa. Lo mungkin bilang, “Claude bikin gue merasa nyaman.”

Banyak dev memang suka Claude. Gue pakai dua-duanya, tapi lebih sering Claude buat kode. *Vibenya* pas.

> Lo harus bayar biar dapet yang bagus. Banyak teman ngomel, “Ini sampah,” padahal pakai versi gratis yang nyaris nggak jalan. Lol. Dulu ini kerasa banget waktu ChatGPT gratis masih 3.5; intinya, pastiin dulu lo pakai model mumpuni sebelum lo buang premisnya.

#### Lo mulai mikir cara mempercepat proses

Beberapa minggu *copy-paste* ke Claude bikin lo sadar ini ribet. Lo mulai eksperimen *context packing*—gimana masukin lebih banyak kode ke jendela konteks LLM.

Lo main-main dengan [repomix](https://repomix.com/), [repo2txt](https://github.com/donoceidon/repo2txt), dan alat sejenis, demi menjejalkan seluruh codebase ke jendela konteks Claude. Bisa jadi lo bahkan bikin skrip shell (atau tepatnya, Claude yang nulis) biar prosesnya gampang.

Ini titik balik.

### Langkah 5: Pakai IDE ber-AI (Cursor, Windsurf?)

Lalu seorang teman bilang, “Kenapa nggak pakai [Cursor](https://cursor.sh/) aja?”

Otak lo langsung meledak. Semua keajaiban *copy-paste* sekarang nempel di IDE. Lebih cepat, lebih seru, nyaris sihir.

Pada titik ini lo udah langganan lima LLM—tambah 20 dolar sebulan juga santai.

Kinerjanya mantap, dan produktivitas lo melonjak.

Lo mulai mainin fitur *agentic coding* bawaan editor. Fitur ini *hampir* selalu jalan. Tapi lo bisa melihat tujuan di cakrawala yang terasa lebih baik.

### Langkah 6: Lo mulai merencanakan sebelum ngoding

Tiba-tiba lo bikin spesifikasi, PRD, dan daftar to-do yang super lengkap buat lo umpan ke agen di IDE atau ke Claude Web.

Belum pernah lo nulis dokumentasi sebanyak ini. Lo pakai LLM lain buat bikin dokumen makin tebal. Lo mindahin dokumen dari satu konteks (PRD) ke konteks lain (“Bisa bikin ini jadi *prompt*?”). Lo pakai LLM buat merancang *prompt* *codegen*.

Kata “[waterfall](https://en.wikipedia.org/wiki/Waterfall_model)” sekarang lo ucapkan dengan jauh lebih sedikit sinisme. Kalau lo senior, mungkin lo nostalgia akhir 90-an dan awal 2000-an sambil mikir, “Apa Martin Fowler ngerasa gini sebelum [2001](https://en.wikipedia.org/wiki/Agile_software_development)?”

Di dunia *codegen*: spesifikasi adalah dewa utamanya.

### Langkah 7: Lo mulai main-main dengan aider biar loop makin cepat

Pada titik ini lo siap masuk **inti keseruan**. Sebelumnya *codegen* butuh lo terlibat dan mantengin. Tapi ini 2025! Siapa masih mau mengetik dengan tangan?

> Ada jalur lain yang banyak teman coba: ngoding pakai suara. Mulai ngasih instruksi ke **aider** lewat klien Whisper. Kocak dan seru. **MacWhisper** bagus dipakai lokal. **Aqua** dan **SuperWhisper** juga oke tapi lebih mahal—biasanya mereka pakai layanan cloud buat inferensi. Gue pribadi pilih yang lokal.

Nyoba aider itu pengalaman liar. Lo jalankan, dia inisialisasi diri di proyek. Lo ketik permintaan langsung ke aider dan dia benar-benar mengeksekusi apa yang lo minta. Dia minta izin, ngasih kerangka, lalu bertindak. Begitu tugas kelar, dia *commit* ke repo. Lo nggak lagi terobsesi *one-shot*; biarin aja aider nyelesain dalam beberapa langkah.

Lo mulai bikin aturan buat LLM. Lo kenal “[Big Daddy](https://www.reddit.com/r/cursor/comments/1joapwk/comment/mkqg8aw/)” rule, atau nambah klausa “no deceptions” di *prompt*. Lo makin piawai menulis *prompt* buat robot.

**Dan ini berhasil.**

Lama-lama lo nggak buka IDE sama sekali—cuma jadi “joki terminal”.

Waktu lo habis nonton robot ngerjain kerjaan lo.

### Langkah 8: Lo bersandar penuh pada *agentic coding*

Sekarang agen yang nulis kode buat lo. Hasilnya cukup top. Kadang lo bengong, terus ingat: tinggal tanya balik.

Lo eksperimen pakai [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Cline](https://cline.bot/), dll. Lo senang karena bisa gabungin model penalaran ([deepseek](https://aws.amazon.com/bedrock/deepseek/)) dan model coding ([Claude Sonnet 3.7](https://www.anthropic.com/claude/sonnet)) buat memangkas langkah perencanaan.

Lo ngelakuin hal gila kayak jalanin 3-5 sesi terminal paralel. Tinggal pindah tab sambil nonton robot ngoding.

Lo mulai nulis kode secara defensif:

- cakupan pengujian super ketat  
- mulai mikir [formal verification](https://github.com/formal-land/coq-of-rust)  
- pakai bahasa pemrograman yang aman terhadap memori  
- milih bahasa berdasarkan verbositas keluaran kompilernya supaya mudah mengepak jendela konteks  

Lo mikir keras gimana caranya bikin apa pun yang lo bangun selesai dengan aman tanpa intervensi.

Lo bakar **BANYAK** duit buat token. Jam GitHub Action lo habis jalanin tumpukan tes buat mastiin kodenya aman.

Rasanya enak. Lo nggak kesel walau nggak ngetik kode.

### Langkah 9: Biarkan agen ngoding, lo main video game

Tahu-tahu lo sampai di tujuan. Yah, semacam—tapi lo paham arahnya. Lo mulai cemas soal kerjaan software. Teman-teman di-PHK dan susah cari kerja baru. Rasanya beda kali ini.

Pas lo ngobrol sama rekan, mereka ngeliat lo kayak fanatik karena konteks kerja lo beda. Lo bilang, “OMG lo mesti coba *agentic coding*!” Mungkin lo tambahin, “Gue juga benci kata *agentic* kok,” biar kelihatan belum minum 200 galon kool-aid. Padahal … iya juga. Dunia terasa lebih cerah karena lo super produktif.

Nggak masalah. Paradigmanya udah geser. Kuhn mungkin bisa nulis buku soal kekacauan masa ini.

Banyak orang nggak bisa lihat karena mereka belum menempuh perjalanan ini. Tapi yang sudah, saling berbagi tips dan debat soal tujuan akhir.

Sekarang, ketika robot kerja, lo bisa fokus namatin game-game Game Boy yang tertunda. Waktu senggang melimpah. Begitu robot tanya “Lanjut?”, lo ketik **yes** dan balik ke Tetris.

Aneh banget. Sedikit mengusik malah.

## Akselerasi

<paul confetti photo>
{{< image src="journey-confetti.webp" alt="Confetti" caption="Konfeti di konser Paul McCartney, Tokyo Dome. iPhone 6, 25 April 2015" >}}

Gue nggak tahu apa yang bakal terjadi di [masa depan](https://ai-2027.com/). Gue khawatir orang yang nggak menempuh perjalanan ini bakal kurang menarik di mata [pemberi kerja](https://x.com/tobi/status/1909231499448401946). Itu agak picik, karena ujung-ujungnya kita ngomongin tooling dan automasi.

Dulu, pas kami agresif merekrut, kami sering nyari kandidat jauh di luar jaringan dan stack kami. Kami Python-shop tapi nginterviu orang yang belum pernah pakai Python. Prinsipnya: kalau engineer-nya hebat, kami bisa bantu mereka nyaman dengan Python dan mereka tetap nambah nilai. Strategi ini manjur—kami merekrut orang keren yang bawa perspektif segar dan ngangkat tim.

Prinsip yang sama berlaku di pengembangan berbantuan AI. Waktu merekrut developer berbakat yang cocok budaya tim dan antusias, pengalaman mereka dengan alat AI seharusnya bukan faktor penentu. Nggak semua orang harus jadi pakar AI sejak hari pertama. Dampingi mereka sesuai ritme, sambil kerja bareng anggota tim yang lebih berpengalaman.

Lama-lama, merekalah yang bakal pegang kemudi dan sukses pakai alat-alat ini.

Satu hal lain yang terus gue pikirin: kemampuan menulis sekarang krusial. Dulu kami udah menghargai komunikator kuat buat dokumentasi dan kolaborasi; sekarang pentingnya dobel. Lo nggak cuma harus ngomong ke manusia, tapi juga nulis instruksi jelas dan presisi buat AI. Mampu merancang *prompt* efektif jadi sama vitalnya dengan nulis kode bagus.

## Kepemimpinan

Gue rasa semua leader dan engineering manager perlu nyebur ke pengembangan berbantuan AI—percaya atau nggak. Alasannya simpel: generasi developer berikutnya bakal belajar ngoding terutama lewat alat AI dan agen. Begitulah masa depan rekayasa perangkat lunak. Kita mesti paham dan beradaptasi.

Kita para *code boomer* mungkin nggak lama lagi bertahan.

**Catatan menarik:** gue hampir nggak pernah pakai LLM buat nulis teks. Kayaknya bakal bagus, tapi gue pengin suara gue sendiri terdengar, nggak dinormalisasi. Sedangkan kode gue justru perlu dinormalisasi. Menarik, ya.

---

Terima kasih buat Jesse, Sophie, kru Vibez (Erik, Kanno, Braydon, dan lain-lain), tim 2389, dan semua yang udah kasih masukan buat tulisan ini.