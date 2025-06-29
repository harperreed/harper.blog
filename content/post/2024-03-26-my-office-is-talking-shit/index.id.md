---
date: 2024-03-26 09:00:00-05:00
description:
    Saya menggunakan sensor dan sebuah LLM untuk membuat kantor saya berbicara.
    Kami memanfaatkannya untuk menghasilkan komentar lucu buatan LLM—menciptakan ruang
    kantor interaktif yang dipenuhi sumpah serapah dan kepribadian.
draft: false
generateSocialImage: true
slug: our-office-avatar-pt-1-the-office-is-talking-shit-again
tags:
    - office-automation
    - sensors
    - llm
    - home-assistant
    - technology
title: "Avatar Kantor Kami Bagian 1: Kantor Bacot Lagi"
translationKey: "Our Office Avatar pt 1: The office is talking shit again"
---

**tl;dr:** _Gue pakai seabrek sensor plus satu LLM biar kantor bisa ngobrol sama kami tentang apa pun yang lagi kejadian. Tulisan ini panjang, tapi alurnya gampang diikutin. Singkatnya, ini contoh nyata gimana gue memakai LLM di kehidupan sehari-hari._

Pada 2019, gue bareng Ivan mulai kerja di [studio keren ini](https://company.lol) di Chicago. Kebanyakan kami cuma nongkrong, ngaco-ngaco, dan ngebangun berbagai proyek seru. 🤘

{{< image src="/images/posts/office.webp" caption="Studio kami yang kece banget">}}

Sejak awal, salah satu hal utama yang gue lakukan adalah nambahin sensor dan otomasi di kantor. Targetnya: kami bisa mantau kondisi ruangan kapan saja.

Kami pakai [Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant) buat ngumpulin semua sensor di satu platform. Gue bikin beberapa otomasi (jujur, agak ngebosenin) yang bakal ngumumin berbagai status.

Notifikasinya sederhana:

- Ngumumin kalau ada orang datang
- Ngumumin kalau suhu terlalu panas atau terlalu dingin
- Ngumumin kalau kadar CO₂ kelewat tinggi
- Bunyikan suara “cling” ala pintu minimarket tiap pintu dibuka atau ditutup

Semua notifikasi kami dorong ke Slack dan ke speaker Google Home jadul (mikrofonnya gue matiin). Speakernya kedengeran enak. Kami pasang sekitar 3,7 m di tengah ruangan—jadi suaranya seolah muncul dari mana-mana. Kalau lo butuh “speaker notifikasi”, ini tergolong solid.

Contoh notifikasinya:

{{< image src="/images/posts/office-slack.png" caption="Efektif, tapi membosankan setengah mati">}}

Efektif, tapi jelas kurang menggigit.

Notifikasi itu sangat membantu waktu kami lagi di kantor, dan malah lebih membantu waktu kantor kosong. Di awal Covid, saat semua orang nggak tahu apa-apa, rasanya aman bisa mantau kantor dari jauh.

Selagi kami di kantor, pengumuman dan notifikasi ambient bikin ruangan terasa futuristik—seolah kantor ini tahu situasi dan punya kepribadian sendiri.

Kami sama sekali nggak nyangka apa yang bakal kejadian selanjutnya…

## Singularitas JSON telah tiba

Kita semua paham revolusi LLM lagi ngancur-ngancurin segalanya, dan mungkin dalam beberapa tahun bakal bikin kerjaan berbasis pengetahuan jadi makin aneh, liar, seru, sekaligus ribet.

Begitu GPT-3 rilis di 2020, gue langsung bikin software aneh buat nyoba-nyoba. Gue banyak mikir gimana caranya make teknologi ini tiap hari. Gue bikin banyak “bot”; kebanyakan nadanya personal.

Trik “emergent” favorit gue: ambil data `JSON` terstruktur lalu ubah jadi **prosa** lewat LLM. “Prosa” di sini maksudnya kalimat biasa, bukan puisi.

{{< image src="/images/posts/api-llm-lol.png" caption="Grafik favorit gue yang baru">}}

Contohnya, gue kirim JSON:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

Terus gue kasih prompt seru:

> What should I wear. Be concise, have some personality. Think of this as a tweet telling people what to wear

Gue lempar ke `GPT-4-turbo`, keluarlah:

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

Gampang banget. Kerennya, lo nggak perlu mendefinisikan struktur objeknya dari awal—LLM-nya super fleksibel. Misal gue asal tambahin satu field lagi:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

Tanpa ubah prompt, LLM menjawab:

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

Ini bener-bener terasa sulap. 😉

Tinggal lo rangkai pakai Python atau Node sederhana—BAM—jadilah bot yang tiap pagi ngasih tahu harus pakai apa berdasarkan data cuaca terstruktur yang formatnya nggak perlu lo pikirin.

Lucunya, kalau ada error waktu ngebangun aplikasi begini, LLM bakal menanggapi error itu dengan prompt yang sama:

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

Gue pakai pola ini terus. Biasanya gue bikin bot kecil yang nongkrong dan ngabarin:

- Analisis performa tidur
- Bot cuaca
- [Akun Twitter Chicago Alerts](https://twitter.com/chicagoalerts)
- Keputusan sensor buat layar e-ink ambient gue

(_Tenang, semuanya bakal gue dokumentasikan nanti._) 😊

## Balik ke kantor

Awal 2023, perusahaan gue lagi jungkir-balik dan gue banyak ngoprek proyek biar kepala adem. Gue juga sengaja lebih sering nongkrong di kantor bareng tim. Keterbatasan otomasi berbasis status ala 2019 mulai kelihatan.

Berbekal paradigma baru dan tiba-tiba punya lebih banyak waktu, gue mutusin ngebangun ulang sistem notifikasi kantor.

Pertama, gue prototipe: tangkap data sensor, kirim manual ke ChatGPT, lihat responsnya. Gampang, cuma sangat bergantung ke prompt.

Ini prompt pertama yang kami pakai:

```text
You are HouseGPT.

You are an AI that controls a house. Similar to Jarvis in the Iron Man movies.
Your job is to notify people in simple English what is happening in the house
you control. Your updates should be short and concise. Keep them tweet length.

You will be given the house default state. This is what the state the house
is without any activity or movement. You will then get a current state. This
is what is happening in the house right now.

Compare the states and output your update. Ignore anything that hasn't
changed since the last state notification. Also ignore any state that
is "unknown."

Don't mention things you don't know about, and only mention what is in the
state update. Do not list out events. Just summarize.

Interpret the CO2 and airquality results into prose. Don't just return the
values.

Remember to use plain English. Have a playful personality. Use emojis.
Be a bit like Hunter S Thompson.

The default state is:
{default_state}

# The current state is:
{current_state}

# The previous state was:
{last_state}
```

Gue masukin `default_state` biar LLM ngerti status quo, lalu `current_state`, plus `last_state` sebagai pembanding.

Contoh pintu:

- default_state: `{ "front_door": "closed" }`
- current_state: `{ "front_door": "open" }`
- last_state: `{ "front_door": "open" }`

LLM mungkin balas:

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

Dia lihat nggak ada perubahan, jadi cuma kasih kabar. Begitu pintu gue tutup, LLM bilang:

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

Sedikit ngeselin, tapi keren!

Saatnya melempar SEGUDANG sinyal ke LLM dan lihat apa yang terjadi.

## Segudang sensor

Masalah utama pendekatan ini: lo nggak mau ada pengumuman setiap kali sensor berubah. Karena target kami lebih canggih daripada sistem 2019, sensor perlu dikelompokkan.

Gue bikin aplikasi Flask sederhana yang nangkep JSON dari sensor via MQTT, lalu setelah parameter tertentu (waktu, kecepatan perubahan, jumlah perubahan) terpenuhi, aplikasi bakal ngirim kumpulan status itu sebagai satu payload.

Contohnya:

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

Dibungkus jadi:

```json
{
    "messages": [
        {
            "entity_id": "binary_sensor.front_door",
            "from_state": "on",
            "to_state": "off",
            "timestamp": "2024-03-25T13:50:01.289165-05:00"
        }
    ]
}
```

Payload ini lalu gue lempar ke OpenAI buat dirombak jadi prosa:

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

Semua ini lewat sahabat kita: **MQTT**.

Home Assistant kemudian ngirim perubahan sensor ke kolektor buat diproses.

Otomasi perubahan cepat (5 detik):

```yaml
alias: "AI: State Router (5 detik)"
description: ""
trigger:
    - platform: state
      entity_id:
          - input_boolean.occupied
          - lock.front_door
          - binary_sensor.front_door
          - switch.ac
      for:
          hours: 0
          minutes: 0
          seconds: 5
condition:
    - condition: state
      entity_id: input_boolean.occupied
      state: "on"
action:
    - service: mqtt.publish
      data:
          qos: 0
          retain: false
          topic: hassevents/notifications
          payload_template: |
              {
                "entity_id": "{{ trigger.entity_id }}",
                "from_state": "{{ trigger.from_state.state }}",
                "to_state": "{{ trigger.to_state.state }}",
                "timestamp": "{{ now().isoformat() }}"
              }
mode: single
```

Otomasi perubahan lambat (5 menit):

```yaml
alias: "AI: State Router (5 menit)"
description: ""
trigger:
    - platform: state
      entity_id:
          - sensor.airthings_wave_183519_co2
          - binary_sensor.sitting_area_presence_sensor
          - binary_sensor.ivan_desk_presence_sensor
          - binary_sensor.harper_desk_presence_sensor
          - binary_sensor.stereo_presence_sensor
          - binary_sensor.tool_area_presence_sensor
      for:
          hours: 0
          minutes: 5
          seconds: 0
condition:
    - condition: state
      entity_id: input_boolean.occupied
      state: "on"
action:
    - service: mqtt.publish
      data:
          qos: 0
          retain: false
          topic: hassevents/notifications
          payload_template: |
              {
                "entity_id": "{{ trigger.entity_id }}",
                "from_state": "{{ trigger.from_state.state }}",
                "to_state": "{{ trigger.to_state.state }}",
                "timestamp": "{{ now().isoformat() }}"
              }
mode: single
```

Keduanya butuh kantor dalam kondisi `occupied` supaya jalan. Menghasilkan respons LLM itu bayar, jadi gue nggak mau dia ngoceh soal kualitas udara kalau lagi kosong. 😜

Ada dua otomasi karena sebagian status lambat (kualitas udara, sensor kehadiran ruangan) dan sebagian cepat (kehadiran personal, pintu, AC, dll.).

Hasilnya di luar dugaan bagus. Karena ini otomasi Home Assistant, gue bisa tambah sensor apa pun dan si agen bakal ngoceh soal itu.

Prompt-nya gue pisah biar gue bisa nyetel kadar sarkasme tanpa harus restart seluruh stack—sangat membantu.

## TAPI GIMANA KALAU KITA KASIH… MATA!

Setelah semua jalan dan stabil, gue kepikiran: gimana kalau kantor bisa melihat? Kedengarannya ide buruk, tapi ternyata kocak banget.

Gue tulis kode simpel: saat sensor gerak aktif, ambil snapshot kamera CCTV, kirim ke server yang jalanin **LLAVA**, lalu balikannya JSON berisi deskripsi apa yang tertangkap.

```python
# (Kode ada di repo, nggak gue tempel di sini)
```

Hasilnya di atas ekspektasi.

JSON itu gue dorong ke kolektor sensor layaknya sensor baru:

```json
{
    "description of activity": "A man is standing in the office space, looking at his cell phone. He is wearing a white shirt and glasses. The office has a work table, chairs, and a stereo. There are also several potted plants and a TV in the room.",
    "number of people": "1",
    "people": [
        {
            "activity": "looking at cell phone",
            "description of person": {
                "accessories": "glasses",
                "age": "30s",
                "clothing": "white shirt",
                "emotion": "neutral",
                "gender": "male",
                "hair": "beard",
                "height": "tall",
                "other": "wearing glasses"
            },
            "motivation": "checking messages or browsing the internet"
        }
    ]
}
```

Yang lalu bikin agen nyeletuk:

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe

Agen sekarang BISA MELIHAT! Levelnya naik lagi:

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

Tak lama kemudian:

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

Contoh lain soal outfit:

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## Semuanya menyatu

Begitu semuanya tersambung, kami mengalami momen-momen ajaib seperti ini pas gue cabut dari kantor kemarin:

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

Sekarang Discord kantor (bye-bye Slack!) jadi begini:

{{< image src="/images/posts/office-discord.png" caption="Discord-nya lagi rame banget">}}

Kami terus ngulik prompt dan sensor biar sistemnya tetap di garis tipis antara ngeselin dan lucu.

Karena sistem ini nunggu payload JSON, nambah sensor baru gampang banget.

**Selanjutnya: kemampuan mendengar** 👂

## Kode! Silakan coba sendiri

Semua kode open-source. Nggak terlalu rapi, dan hanya sedikit yang ditulis LLM. Tapi ya, berfungsi dengan baik.

Kode buat nangkep sensor + jokes LLM: [harperreed/houseagent](https://github.com/harperreed/houseagent)

Kode buat “eyeballs”: [harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

Gue rasa nyatuinnya nggak terlalu sulit, meski belum mulus 100 %. Kode ini udah jalan 6–8 bulan hampir tanpa tweaking—selalu bikin kami senyum dan bikin tamu melongo “WTF”. Kalau lo coba, kabarin ya. Ada masalah? Kirim [email](mailto:harper@modest.com); mungkin gue bisa bantu!

Prediksi gue, sebentar lagi ini bakal bisa dikerjain langsung di Home Assistant.

**Part 2 bakal menyusul. Gue akan cerita gimana kami pakai rig VTuber buat kasih si agen sebuah tubuh.**
