---
description: Kolofon untuk harper.blog
hideReply: true
menu:
    footer:
        name: Colophon
        weight: 3
nofeed: true
slug: colophon
title: Kolofon
translationKey: colophon
type: special
url: colophon
weight: 6
---

Situs web [harper.blog](https://harper.blog) adalah blog pribadi Harper Reed. Situs ini dibangun menggunakan teknologi web modern dan berbagai teknik _static site generation_ (pembuatan situs statis).

## Teknologi yang Digunakan

- **Static Site Generator (generator situs statis)**: [Hugo](https://gohugo.io/)
- **Hosting**: [Netlify](https://www.netlify.com/)
- **Kontrol Versi**: Git (repositori berada di GitHub)

## Desain dan Tata Letak

- Situs ini menggunakan tema khusus berbasis [Bear Cub](https://github.com/clente/hugo-bearcub) ᕦʕ •ᴥ•ʔᕤ
- ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•!
- Tipografi: situs ini menggunakan font sistem bawaan demi performa optimal dan tampilan alami
- Desain responsif memastikan situs dapat digunakan di berbagai perangkat dan ukuran layar

## Manajemen Konten

- Konten ditulis dalam _Markdown_

## Build dan Deployment

- **Continuous Deployment (CD)** dikonfigurasi melalui Netlify
- Setiap kali ada perubahan yang _di-push_ ke cabang utama (_main_), situs secara otomatis dibangun dan _di-deploy_
- Perintah serta pengaturan _build_ khusus didefinisikan di `netlify.toml`

## Optimasi Kinerja

- Gambar dioptimalkan dan disajikan dalam format WebP bila memungkinkan
- Berkas CSS diperkecil (_minified_) untuk _build_ produksi
- Alur aset (_asset pipeline_) bawaan Hugo digunakan untuk optimasi sumber daya

## Fitur Tambahan

- _RSS feed_ tersedia untuk sindikasi konten
- Tag meta media sosial diterapkan agar konten lebih mudah dibagikan di platform seperti Twitter dan Facebook
- _Shortcode_ khusus digunakan untuk memperkaya format konten (misalnya integrasi Kit.co)

## Alat Pengembangan

- Sebuah `Makefile` digunakan untuk mempermudah tugas pengembangan umum
- Proyek ini menggunakan _Go modules_ untuk manajemen dependensi

## Aksesibilitas dan Standar

- Situs ini dirancang agar mudah diakses serta mematuhi standar web modern
- HTML semantik digunakan di seluruh situs

## Analitik

- Situs ini menggunakan [tinylytics](https://tinylytics.app/) untuk memantau berbagai _bits_ dan _hits_. Anda dapat melihat hasilnya [di sini](https://tinylytics.app/public/cw1YY9KSGSE4XkEeXej7).

- Situs ini telah menerima {{< ta_hits >}} _hits_ dari negara-negara berikut: {{< ta_countries >}}.

## Penulis dan Pemelihara

Situs ini dipelihara oleh Harper Reed. Untuk pertanyaan, silakan hubungi [harper@modest.com](mailto:harper@modest.com).

Terakhir diperbarui: September 2024

## Log Perubahan

Berikut log _commit_ Git untuk iterasi ini:

{{% readfile file="gitlog.md" markdown="true" %}}

---

Dibangun dengan ❤️ menggunakan Hugo dan _di-deploy_ dengan Netlify.
