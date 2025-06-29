---
date: 2024-04-12 09:00:00-05:00
description: Saya membangun mesin pencari meme ajaib menggunakan siglip/CLIP dan penyandian
  vektor gambar. Ini adalah cara yang menyenangkan untuk mempelajari teknologi yang
  kuat ini. Saya membagikan kodenya agar Anda bisa membuatnya sendiri dan menemukan
  permata terlupakan di perpustakaan foto Anda. Mari kita lepaskan kekuatan AI pada
  gambar-gambar kita!
draft: false
generateSocialImage: true
slug: i-accidentally-built-a-meme-search-engine
tags:
- meme-search-engine
- vector-embeddings
- applied-ai
- siglip
- image-search
title: Saya tanpa sengaja membuat mesin pencari meme
translationKey: I accidentally built a meme search engine
---

## Atau: cara belajar soal CLIP/SigLIP dan pengkodean gambar menjadi vektor

_tl;dr_: Gue bikin mesin pencari meme pakai SigLIP/CLIP dan pengkodean gambar menjadi vektor. Seru banget—gue belajar banyak.

Gue sudah lama ngerjain berbagai alat AI terapan. Salah satu komponen yang selalu terasa paling ajaib adalah _embedding_ vektor. [Word2Vec](https://en.wikipedia.org/wiki/Word2vec) dan kawan-kawan benar-benar bikin otak gue meledak—kayak sulap.

Di Hacker News gue lihat [aplikasi sederhana](https://news.ycombinator.com/item?id=39392582) yang [gokil banget](https://mood-amber.vercel.app/). Ada orang yang merayapi segudang gambar Tumblr, pakai [SigLIP](https://arxiv.org/abs/2303.15343) buat dapetin _embedding_-nya, lalu bikin app “klik gambar, keluar gambar serupa”. Kelihatan magis. Gue nggak punya ide gimana caranya, tapi rasanya terjangkau.

Jadi gue pakai momen motivasi dadakan ini buat cari tahu “sebenernya gimana sih semua ini jalan”.

## Apaan Sih?

Kalau lo belum pernah ketemu _embedding_ vektor, CLIP/SigLIP, basis data vektor, dan semacamnya—tenang aja.

Sebelum lihat hack di HN, gue juga nggak kepikiran soal _embedding_ vektor, _embedding_ multimodal, atau basis data vektor. Gue pernah main-main pakai FAISS (pustaka vektor simpel buatan Facebook) dan Pinecone ($$) buat beberapa hack, tapi nggak mendalaminya. Cuma bikin jalan, “oke, tes lulus”, selesai.

Gue sendiri nyaris nggak paham apa itu vektor. LOL. Sebelum bikin ini, gue nggak ngerti gimana mau pakai vektor selain buat RAG (Retrieval-Augmented Generation) atau proses LLM lainnya.

Gue belajar dengan cara ngebangun. Hasilnya makin menarik _dan_ terasa magis.

### Istilah WTF

Beberapa temen baca tulisan ini sebelum gue rilis dan nanya, “wtf itu X?” Berikut daftar singkat istilah yang dulu baru buat gue:

- **Embedding Vektor** — Mengubah teks atau gambar menjadi representasi numerik agar lo bisa menemukan gambar serupa dan menelusuri koleksi dengan efektif.  
- **Basis Data Vektor** — Tempat menyimpan dan mencari item yang sudah dienkode, memudahkan pencarian item serupa.  
- **Word2Vec** — Teknik terobosan yang mengubah kata menjadi vektor numerik, sehingga kita bisa mencari kata sejenis dan memetakan relasi antar-kata.  
- **CLIP** — Model OpenAI yang mengekode gambar dan teks ke vektor numerik.  
- **OpenCLIP** — Implementasi sumber terbuka model CLIP, jadi siapa pun bisa pakai tanpa izin khusus.  
- **FAISS** — Pustaka efisien untuk mengelola dan mencari koleksi besar vektor, bikin pencarian gambar super cepat.  
- **ChromaDB** — Basis data yang menyimpan dan mengambil vektor gambar/teks (sering disebut singkat “Chroma”), lalu mengembalikan hasil serupa secepat kilat.

## Sederhanain saja, Harper.

Ini hack yang cukup sederhana. Gue cuma fuck around, jadi nggak terlalu mikirin skalabilitas—yang penting gampang direplikasi biar lo bisa coba sendiri.

Target pertama: semuanya berjalan lokal di laptop. Kita punya GPU Mac yang canggih—biar panas sekalian.

Langkah awal: bikin crawler sederhana yang merayapi satu folder gambar. Gue pakai Apple Photos, jadi nggak punya folder foto bebas. Tapi gue punya bucket meme raksasa dari grup chat meme rahasia (jangan bilang-bilang). Gue ekspor chat-nya, pindahin gambar ke satu folder, dan BAM—dataset uji siap.

### Crawler-nya

Gue bikin crawler terburuk sejagat. Jujur: Claude yang nulis, gue yang nyuruh.

Agak ribet, tapi alurnya gini:

1. Ambil daftar file di folder target.  
2. Simpan daftar itu ke file `msgpack`.  
3. Baca `msgpack`, iterasi setiap gambar, lalu simpan ke database `sqlite` sambil mencatat metadata:  
   - nilai hash  
   - ukuran file  
   - path  
4. Iterasi basis data `sqlite`, mengekode tiap gambar dengan CLIP untuk dapat _embedding_ vektor.  
5. Simpan vektor itu balik ke `sqlite`.  
6. Iterasi lagi, masukkan vektor + path gambar ke ChromaDB.  
7. Selesai.

Ini sebenernya kerja dua kali. Bisa aja langsung: gambar → _embedding_ → ChromaDB. Gue pilih ChromaDB karena gampang, gratis, tanpa infra.

Gue bikin ribet karena:  

- Setelah dataset meme, gue merayapi 140 ribu gambar dan butuh sistem tahan crash.  
- Harus bisa _resume_ kalau listrik mati, dsb.  
- Gue cinta _loop_.  

Meski kompleks, semuanya berjalan sangat baik. Gue udah merayapi 200 ribu+ gambar tanpa masalah.

### Sistem _embedding_

Mengekode gambar itu menyenangkan.

Awalnya gue pakai SigLIP dan bikin [web service sederhana](https://github.com/harperreed/imbedding) buat upload gambar & dapet vektor. Ini jalan di salah satu GPU box studio dan kinerjanya lumayan. Nggak super cepat, tapi tetap jauh lebih kencang ketimbang nyoba [OpenCLIP](https://github.com/mlfoundations/open_clip) lokal.

Tapi gue tetap pengen lokal. Gue keingat repo [ml-explore](https://github.com/ml-explore/) dari Apple. Ternyata mereka punya [implementasi CLIP](https://github.com/ml-explore/mlx-examples/tree/main/clip) yang ngebut gila-gilaan. Pakai model gede pun masih lebih kencang dari 4090—wildstyle.

Gue cuma perlu bikin gampang dipakai di skrip.

### MLX_CLIP

Gue dan Claude ngehack skrip contoh Apple jadi kelas Python kecil yang bisa lo pakai lokal di mesin mana pun. Dia bakal mengunduh model kalau belum ada, mengonversinya, lalu langsung dipakai.

Cek di sini: https://github.com/harperreed/mlx_clip

Gue cukup bangga sama hasilnya. Kayak yang orang udah tau, Apple Silicon cepat banget.

Cara pakainya simpel:

```python
import mlx_clip

# Inisialisasi model.
clip = mlx_clip.mlx_clip("openai/clip-vit-base-patch32")

# Enkode gambar dan dapatkan embedding.
image_embeddings = clip.image_encoder("assets/cat.jpeg")
print(image_embeddings)

# Enkode deskripsi teks dan dapatkan embedding.
text_embeddings = clip.text_encoder("a photo of a cat")
print(text_embeddings)
```

Gue pengen ini juga jalan pakai SigLIP, karena model itu menurut gue jauh lebih bagus dari CLIP. Tapi ini cuma POC, bukan produk yang bakal gue rawat. Kalau ada yang tau cara bikin SigLIP jalan—[hmu](mailto:harper@modest.com). Gue males nyiptain ulang OpenCLIP—secara teori sudah jalan bagus di Apple Silicon.

### Lanjut apa?

Begitu semua vektor gambar dijejalkan ke basis data vektor, waktunya bikin antarmuka. Gue pakai fungsi kueri bawaan ChromaDB buat nampilin gambar serupa.

Ambil vektor gambar acuan → ajukan kueri ke ChromaDB → ChromaDB mengirimkan daftar ID gambar serupa dengan urutan tingkat kemiripan menurun.

Lalu gue bungkus semua jadi app Tailwind + Flask.  
Gila, ini keren.

Nggak kebayang 2015 perlu berapa kerja buat bikin ginian. Gue habis paling 10 jam dan berasa remeh.

Hasilnya bener-bener sulap.

### Pencarian konsep meme

Inget, dataset awal gue meme: 12 000 meme buat disisir.

Mulai dengan ini:

{{< image src="images/posts/vector-memes-bowie.png" caption="So true" >}}

Enkode → kirim vektornya ke ChromaDB → dapet gambar serupa.

Hasilnya:  
{{< image src="images/posts/vector-memes-bowie-results.png" >}}

Contoh lain:  
{{< image src="images/posts/vector-memes-star-trek.png" >}}

Hasilnya:  
{{< image src="images/posts/vector-memes-star-trek-results.png" >}}

Seru banget buat klik-klik.

### Namespace?

Keajaiban sebenernya bukan “klik gambar, dapet gambar mirip” aja. Itu keren, tapi belum “gila banget”.

Yang bikin mind-blown adalah pakai model sama buat mengekode teks pencarian ke vektor, terus nyari gambar yang mirip sama teks itu.

Entah kenapa otak gue korslet tiap liat ini. Pencarian semantik gambar berbasis gambar udah keren, tapi antarmuka multimodal ini kayak trik sulap.

Contoh:

Cari **money** → dapet embedding → ChromaDB:  
{{< image src="images/posts/vector-memes-money.png" >}}

Cari **AI**  
{{< image src="images/posts/vector-memes-ai.png" >}}

Cari **red** (membingungkan banget! Warna kah? Gaya hidup? Rusia?)  
{{< image src="images/posts/vector-memes-red.png" >}}

Dan seterusnya. Sampai bosan. Ajaib. Lo bisa nemuin harta karun yang kelupaan. Misalnya butuh meme soal nulis blog:  
{{< image src="images/posts/vector-memes-writing-meme.jpg" >}}

(Gue sadar diri, tapi bodo amat—LOL)

### Gimana kalau di perpustakaan foto?

Berjalan sangat baik.

Gue rekomendasiin lo coba ke library foto sendiri. Gue unduh Google Photos Takeout, ekstrak ke disk eksternal, terus jalankan beberapa skrip biar rapi (orang yang desain Takeout doyan duplikat data). Abis itu gue arahkan skrip ke folder itu, bukan folder meme, dan langsung jalan.

Ada sekitar 140 ribu foto; prosesnya kira-kira 6 jam. Not bad. Hasilnya edan.

#### Beberapa contoh seru:

Jelas mirip (gue juga punya masalah duplikat di Google Photos):  
{{< image src="images/posts/vector-memes-harper.png" >}}

Kami pernah punya banyak pudel. Nih sebagian:  
{{< image src="images/posts/vector-memes-poodles.png" >}}

Bisa cari landmark. Gue nggak sadar pernah moto Fuji-san dari pesawat!  
{{< image src="images/posts/vector-memes-fuji-results.png" >}}

Terus nemuin gambar Fuji serupa.  
{{< image src="images/posts/vector-memes-fuji-similar.png" >}}

Cari tempat gampang banget.  
{{< image src="images/posts/vector-memes-chicago.png" >}}

Atau emosi. Ternyata muka gue sering kaget.  
{{< image src="images/posts/vector-memes-surprised.png" >}}

Hal niche kayak low rider (ini di Shibuya!)  
{{< image src="images/posts/vector-memes-low-riders.png" >}}

Bahkan hal yang susah dicari manual, misalnya bokeh.  
{{< image src="images/posts/vector-memes-bokeh.png" >}}

Asik, karena gue bisa klik-klik dan nemu foto keren yang lupa. Misalnya foto Baratunde ini dari 2017:

{{< image src="images/posts/vector-memes-baratunde.png" >}}

### Ini bakal ada di mana-mana

Gue yakin teknologi ini bakal segera nyelip di semua app foto. Mungkin Google Photos udah punya, tapi udah terlalu “di-Google-in” sampai orang nggak ngeh.

Terlalu bagus buat nggak dipakai. Kalau gue punya produk besar yang main gambar, gue langsung bikin pipeline buat mengekode gambar dan lihat fitur aneh apa kebuka.

## lo bisa pakai ini dengan harga nol rupiah

Source-nya di sini: [harperreed/photo-similarity-search](https://github.com/harperreed/photo-similarity-search).

Silakan dicek.

Cukup gampang jalaninnya, walau agak hacky. LOL.

Gue saranin pakai Conda atau sejenis biar environment bersih. Antarmuka: Tailwind. Web server: Flask. Kode: Python. Host lo: Harper Reed.

## Tantangan gue buat lo!

Tolong bikinin dong app Mac sederhana buat mengatalogkan library foto gue. Gue nggak mau upload ke mana-mana. Tinggal tunjuk folder, “crawl”. Bayangin fitur tambahannya:

- Llava/Moondream auto-caption  
- Kata kunci / tag  
- Kemiripan vektor  
- dll

Harus jalan lokal. Native. Simpel, efektif. Mungkin sambung ke Lightroom, Capture One, atau Apple Photos.

Gue pengen ini. Bikin, gih. Mari kita temuin foto keren lewat sihir AI.

## Ekstra Kredit: Recovery JPEG Preview Lightroom

Teman hacking gue, Ivan, nongol pas gue ngebangun ini. Dia langsung lihat magisnya dan pengen pakai.

Katalog fotonya ada di hard-disk eksternal—tapi file preview Lightroom ada lokal. Dia nulis skrip cepet buat mengekstrak thumbnail + metadata dari file preview dan nyimpennya ke disk eksternal.

Kami jalankan crawler vektor gambar dan BAM—dia bisa lihat gambar serupa. Berjalan mulus.

#### Pulihin foto Lightroom lo—minimal thumbnail-nya.

Skrip simpel Ivan buat tarik gambar dari file preview itu keren. Kalau lo kehilangan library foto asli (hard-disk korup, dsb.) tapi masih punya file `.lrprev`, skrip ini bisa nyelametin versi low-res-nya.

Skrip berguna buat disimpen.

Cek di sini: [LR Preview JPEG Extractor](https://github.com/ibips/lrprev-extract).

## Thanks udah baca.

Seperti biasa, [hmu](mailto:harper@modest.com) dan ayo nongkrong. Gue lagi banyak mikirin AI, e-commerce, foto, hi-fi, hacking, dan hal-hal seru lain.

Kalau lo di Chicago, kabarin aja.