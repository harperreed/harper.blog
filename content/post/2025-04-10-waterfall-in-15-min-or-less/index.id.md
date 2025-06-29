---
date: 2025-04-10
description: Sebuah penjelajahan tentang bagaimana AI mempercepat metode pengembangan
  tradisional menjadi siklus waterfall cepat selama 15 menit, sehingga mengubah alur
  kerja rekayasa perangkat lunak dan dinamika tim.
draft: false
generateSocialImage: true
generated: true
slug: waterfall-in-15-minutes-or-your-money-back
tags:
- llm
- large-language-models
- code-generation
- ai
- artificial-intelligence
- coding
- programming
- workflow
- software-development
- development-practices
- productivity
- automation
title: 'Waterfall dalam 15 Menit atau Uang Anda Kembali'
translationKey: Waterfall in 15 Minutes or Your Money Back
---

Baru-baru ini aku mengobrol santai dengan seorang teman. Obrolan ringan itu tiba-tiba melebar menjadi diskusi mendalam tentang pemrograman berbantuan AI—dampaknya pada alur kerja, tim, dan rasa craftsmanship kami. Topiknya meliputi semuanya, dari menulis ulang codebase lama sampai bagaimana cakupan pengujian otomatis mengubah hakikat pemrograman.

Aku mengambil transkripnya dari granola, memasukkannya ke o1-pro, lalu memintanya menulis postingan blog ini. Hasilnya? Tidak buruk—cukup merepresentasikan pandanganku.

Kukirim ke beberapa teman, dan mereka ingin meneruskan ke lebih banyak teman lagi. Artinya, mau tak mau aku harus memublikasikannya. Baiklah, ini dia!

> Ini pengingat bagus: kalau kamu menerima email dengan tulisan sempurna tanpa gaya personal, kemungkinan besar AI yang menulisnya. lol.

---

## Waterfall dalam 15 Menit atau Uangmu Kembali

### Kenormalan Baru: “Kenapa Kualitas Kode Masih Penting?”

Selama bertahun-tahun kita bicara tentang kode sebagai karya—bagaimana kita masuk ke flow state yang berharga, memahat sepotong logika, dan keluar sebagai pemenang dengan perbaikan bug berkelas. Kini muncul paradigma baru: alat pembangkit kode berbasis LLM mampu memompa fitur dalam hitungan menit.

Sebagian orang kelabakan oleh kecepatan ini dan bagaimana ia mengguncang standar lama “clean code”. Mendadak, menulis rangkaian tes yang andal—bahkan TDD—lebih tentang membiarkan bot memverifikasi dirinya sendiri daripada menelusuri tiap baris kode secara metodis.

Apakah kualitas kode bakal merosot? Mungkin. Di sisi lain, kita juga melihat dorongan ke penulisan kode hiper-defensif—analisis statis, metode verifikasi formal, dan cakupan pengujian di mana-mana—supaya kalau sebuah agen AI berulah, kita langsung mengetahuinya. Belum pernah sebelumnya kita membutuhkan pipeline CI/CD kelas satu dan pemeriksaan yang ketat serta penuh rigor setinggi sekarang.

---

### Waterfall dalam 15 Menit

{{< image src="waterfall.webp" alt="Waterfall" caption="Iceland has a lot of waterfalls. Leica Q, 9/30/2016" >}}

Dulu kita membahas “Waterfall vs. Agile” seolah keduanya kutub moral, dengan Agile sebagai satu-satunya jalan benar. Ironisnya, pembangkit kode justru mendorong kita ke siklus mikro-Waterfall: kita menulis spesifikasi sejelas mungkin (karena AI butuh kejelasan), menekan “go”, menunggu kode dihasilkan, lalu meninjaunya. Rasanya tetap iteratif, tetapi dalam praktiknya kita melakukan satu blok perencanaan, satu blok eksekusi, lalu satu blok peninjauan—“Waterfall dalam 15 menit”.

Keajaibannya? Kamu bisa menyalakan banyak “agen” sekaligus. Satu AI membangun fitur, yang lain membereskan dokumentasi, sementara yang ketiga memproses cakupan tes. Ini jelas bukan Waterfall linear lama—ini konkurensi yang disuntik steroid.

---

### Pergeseran Budaya Tim yang Akan Datang

Kalau kamu memimpin tim engineering, mungkin atasan bertanya, “Bisa nggak kita pakai AI supaya lebih produktif?” Sementara itu, antusiasme di tim beragam. Ada yang all-in—membangun fitur baru lewat prompt saja—ada juga yang protektif terhadap identitas craftsmanship-nya.

Menurutku, yang manjur itu:

1. **Lakukan proyek percontohan kecil**

   Pilih proyek internal atau alat sampingan berisiko rendah, lalu biarkan beberapa engineer yang penasaran bereksperimen dengan coding AI. Biarkan mereka merusak sesuatu, lihat apa yang terjadi kalau terlalu percaya model, lalu perhatikan bagaimana mereka menarik rem memakai best practice.

2. **Rotasikan anggota tim**

   Memiliki proyek sampingan khusus “AI-coded” memungkinkanmu menggilir anggota—biarkan mereka satu-dua minggu hidup di lingkungan baru ini, saling belajar, lalu bawa pulang pelajarannya ke codebase utama.

3. **Serius soal dokumentasi**

   Agen-agen AI memerlukan spesifikasi yang sangat jelas. Pembangkit kode itu murah, tetapi mengarahkan LLM butuh perencanaan cermat. Taruh spesifikasi dan dokumen arsitektur terbaikmu di repositori bersama. Kamu akan berterima kasih pada dirimu sendiri ketika orang masuk atau keluar proyek.

---

### Flow State Mungkin Terlalu Diagung-agungkan

Satu hal mengejutkan: banyak dari kita masuk dunia coding karena jatuh cinta pada flow state. Namun coding AI tidak selalu memunculkan keterhanyutan yang sama. Kamu bisa sejam menyusun prompt, membiarkan AI bekerja di latar belakang, lalu sesekali mampir untuk menyetujui atau mengarahkan.

Bagi sebagian orang, itu bikin kagok. Bagi yang punya anak atau harus juggling sejuta urusan, justru melegakan. Ketika kamu bisa berpindah konteks—cek keluaran AI, kembali ke kehidupan nyata, lalu balik lagi ke potongan kode yang sudah jadi—kamu sadar ada cara baru untuk produktif tanpa memerlukan blok waktu sunyi yang panjang.

---

### Apakah Ini “Peak Programmer”?

Ada gosip bahwa setelah AI bisa menghasilkan kode, kita sampai di “peak programmer”—konon nanti jumlah engineer bakal turun. Mungkin benar untuk pekerjaan fitur sederhana atau menyambung API. Tapi muncul juga kompleksitas baru seputar keamanan, kepatuhan, cakupan tes, dan arsitektur.

Perbedaannya? Engineer strategis akan bersinar—mereka yang bisa mengorkestrasi banyak alat AI, mengawasi kualitas kode, dan merancang sistem yang skalabel. Mereka separuh PM, separuh arsitek, separuh QA, separuh developer. Mereka menyusun prompt, mendefinisikan tes, menjaga kualitas, dan menangani semua edge case yang tak diprediksi LLM.

---

### Tips dari Garis Depan

Beberapa pelajaran yang kupetik sendiri:

1. **Mulai manual, baru nyalakan AI**

   Untuk aplikasi iOS, inisialisasi proyek di Xcode dulu agar berkas otomatisnya tidak membingungkan AI. Setelah itu, biarkan AI menyelesaikan sisanya.

2. **Prompt singkat dan jelas kadang lebih tokcer**

   Aneh tapi nyata, meminta LLM “make code better” kadang seefektif prompt super-rinci. Bereksperimenlah—beberapa model lebih responsif kalau tidak terlalu dibatasi.

3. **Gunakan alur checkpoint**

   Commit sering, bahkan jika hanya `commit -m "It passed the tests, I guess!"`. AI bisa merusak secepat ia memperbaiki. Commit sering = titik rollback gampang.

4. **Cegah AI menguji hal-hal dasar secara berlebihan**

   AI gemar mengetes segalanya, termasuk apakah `for` loop masih berputar. Tetap waspada, buang tes yang tak penting, dan jaga pipeline tetap ramping.

5. **Dokumentasikan absolut semuanya**

   Biarkan AI menghasilkan “Implementation Guide” besar. Panduan ini membantu kamu—dan membantu AI sendiri pada iterasi berikutnya.

---

### Penutup

{{< image src="waterfall-road.webp" alt="Road to the future" caption="Road to the future. Colorado is flat. Leica Q, 5/14/2016" >}}

Industri kita bergerak lebih cepat daripada sebelumnya. Banyak asumsi lama—seperti sentralnya flow state atau pesta besar atas fitur yang dikode manual dengan teliti—akan segera tampak menggemaskan. Namun kreativitas tidak hilang; ia berubah menjadi orkestrasi strategis: tahu apa yang harus dibangun, bagaimana mendeskripsikannya, dan bagaimana mencegahnya menjadi dumpster fire—berantakan total.

Pada akhirnya, yang membuat produkmu menang bukan brute-forcing kode, melainkan merancang pengalaman yang dicintai pengguna. Karena kalau kita bisa memutar 10 versi Instagram dalam satu akhir pekan, penentunya bukan seberapa elegan kodenya, melainkan mana yang paling nyambung ke hati—dan itu urusan desain serta produk, bukan semata-mata engineering.

Jadi, selamat datang di Waterfall baru—tuntas dalam siklus 15 menit, dengan AI sebagai junior engineer tak terbatas dan pipeline kode di hyperdrive. Aneh, menakjubkan, dan kadang menyeramkan. Dan sepertinya kita semua harus belajar tarian baru ini, cepat atau lambat.

---

_Aneh betul dunia ini. Sepertinya semuanya akan terus makin aneh. Mari kita selami_