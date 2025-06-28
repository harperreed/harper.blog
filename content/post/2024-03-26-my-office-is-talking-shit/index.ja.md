---
date: 2024-03-26 09:00:00-05:00
description: センサーとLLMを組み合わせてオフィスをしゃべらせた。この仕組みでユーモアたっぷりのLLM生成コメントを生み出し、罵詈雑言と個性がしみ込んだインタラクティブなオフィス空間を作り上げた。
draft: false
generateSocialImage: true
tags:
    - office-automation
    - sensors
    - llm
    - home-assistant
    - technology
title: "Our Office Avatar pt 1: The office is talking shit again"
translationKey: "Our Office Avatar pt 1: The office is talking shit again"
slug: our-office-avatar-pt-1-the-office-is-talking-shit-again
---

**tl;dr:** _いろんなセンサーと LLM をゴッソリ突っ込んで、オフィスが俺たち——そう、あんたも含めた **us**——に「いま何が起きてるか」しゃべり倒すようにしたぜ。記事は長いけど内容はシンプル。リアルライフで LLM をどうブッ込んでるかの実例だ。_

2019 年、相棒 Ivan とオレらはシカゴの [amazing studio](https://company.lol) で仕事を始めた。基本オレら、ダラダラとクソ面白いモノを量産して遊んでるだけ。

{{< image src="/images/posts/office.webp" caption="俺たちのクソ最高なスタジオ">}}

まず着手したのは、オフィスにセンサーと自動化を入れて環境をいつでも把握できるようにすること。

[Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant) に全部のセンサーを集約し、退屈きわまりない自動化をいくつか書いた。

通知内容はホントにベタ:

- 人が来たらアナウンス
- 室温がクソ暑い／クソ寒いときにアナウンス
- CO₂ 濃度がヤバいときにアナウンス
- ドアが開閉したらコンビニみたいにチリン♪と鳴らす

通知は Slack と、マイクを殺した古い Google Home スピーカーへ。音はそこそこいいし、部屋のド真ん中 12 フィート上に吊ってるから四方八方から聞こえる。通知専用スピーカー探してるなら悪くないぜ。

通知の例はこんな感じ：

{{< image src="/images/posts/office-slack.png" caption="頭はカラッポで正直退屈">}}

見てのとおり役には立つがクソつまらん。

オフィスにいるときはもちろん、離れているときにも超便利だった。Covid 初期で誰も何もわからなかった頃、リモートでオフィスの状態を監視できたのはマジで助かった。

室内にいるあいだはアナウンスと環境音のおかげで「オフィスに人格がある」みたいな近未来感があった。

でも、次に来るカオスは想像もしなかった……。

## JSON シンギュラリティがやって来た

いまや LLM 革命があらゆるものをぶっ壊しつつあって、これから数年は知識労働がワイルドで複雑になるのは確実だ。

2020 年に GPT-3 が出た瞬間、オレは即座に変なソフトを量産し始めた。日常でどうイジるか考えながら “bot” を山ほど作り、たいていは超 “個人的” な語り口になった。

一番イカれた発見は、構造化された `JSON` データを LLM で **文章**に変換させること。詩じゃなく、普通の文章な。

{{< image src="/images/posts/api-llm-lol.png" caption="オレのお気に入りニューグラフ">}}

たとえばこんな JSON を用意して──

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

軽いプロンプトを添える：

> What should i wear. Be concise, have some personality. Think of this as a tweet telling people what to wear

これを `GPT-4-turbo` に投げると、

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

と返ってくる。しかも JSON の項目をカッチリ決めなくても平気。LLM がクソ柔軟に噛み砕いてくれる。ためしにフィールドを一つ増やしても、

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

同じプロンプトで――

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

これ、マジで魔法。

あとは Python か Node でチョロっと書けば、天気データを元に毎朝「今日の服装」を教えてくれる bot の完成。JSON が多少変形してもノープロブレム。

笑えるのが、エラーが帰ってきても LLM が同じテンションでイジってくること。

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

このパターンをオレは常用してて、周りに小さな bot をいくつも放し飼いにしている：

- 睡眠パフォーマンス解析
- 天気 bot
- [Chicago Alerts Twitter アカウント](https://twitter.com/chicagoalerts)
- E-Ink アンビエントディスプレイの表示決定

(_これらはあとでちゃんと書くぜ。_)

## Back to the office

2023 年初頭、会社がガタガタで気晴らしにプロジェクトをハックしまくり、オフィスにも意識的に入り浸るようになった。2019 年に作った状態ベース自動化の限界が露呈し始めた。

新しいパラダイムとヒマを手に入れたオレは、通知システムを作り直すことに。

まずはセンサーデータを手動で ChatGPT に投げて挙動を確認。プロンプト依存だけど流れは単純。

一発目のプロンプトはこれ：

```text
You are HouseGPT.

You are an AI that controls a house. Similar to Jarvis in the iron man movies.
Your job is to notify people in simple english what is happening in the house
you control. Your updates should be short and concise. Keep them tweet length.

You will be given the house default state. This is what the state the house
is without any activity or movement. You will then get a current state. This
is what is happening in the house right now.

Compare the states and output your update. Ignore anything that hasn't
changed since the last state notification. Also ignore any state that
is 'unknown.'

Don't mention things you don't know about, and only mention what is in the
state update. Do not list out events. Just summarize.

Interpret the co2 and airquality results into prose. Don't just return the
values.

Remember to use plain english. Have a playful personality. Use emojis.
Be a bit like Hunter S Thompson.

The default state is:
{default_state}

# The current state is:
{current_state}

# The previous state was:
{last_state}
```

`default_state` が平常時、`current_state` が現在。おまけ（ワイルドカード）的に `last_state` も投げてる。

ドアならこんな感じ：

- default_state: `{ "front_door": "closed" }`
- current_state: `{ "front_door": "open" }`
- last_state: `{ "front_door": "open" }`

LLM の返答はこうだ：

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

変化ナシならこのとおり。ドアを閉めると、

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

ちょっとウザいけど面白い。

じゃあセンサーを山ほど投げたらどうなる？

## Sensors bunches

センサーが変わるたびにアナウンスしたらウザすぎる。2019 年版を超えるにはセンサーを束ねる必要があった。

そこでシンプルな Flask アプリを書いて、MQTT 経由で飛んでくる JSON を集め、一定の条件（時間・変化の速度・件数）でまとめて 1 ペイロードに。

単体はこんな JSON：

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

束ねると：

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

これを OpenAI に渡すと、

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

すべては我らが—もちろんあんたの—相棒 **MQTT** 経由で行われる。

Home Assistant のオートメーションがセンサー変化を MQTT に送り、Flask アプリが受け取って文章化。

### Fast change automation (5 seconds)

```yaml
alias: "AI: State Router (5 seconds)"
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

### Slow change automation (5 minutes)

```yaml
alias: "AI: State Router (5 minutes)"
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

どちらも `input_boolean.occupied` (在室中) がオンのときだけ実行。金かけて生成するんだから、誰もいないときに空気質を語られても意味ねぇ。

オートメーションは状態変化を検知して MQTT に流すだけ。Home Assistant のセンサーなら何でも追加可能。

プロンプトは別ファイルにしてあるので、スタックを再起動せずに毒舌レベルをチューニングできる。これが超便利。

## BUT WHAT ABOUT ADDING EYEBALLS!

システムが動き始めた頃、「オフィスに“目”を付けたらどうよ？」と思った。書きながらヤバい気もするが、面白さが勝つ。

モーションセンサーをトリガーに防犯カメラのスナップを撮り、LLAVA で解析して JSON を返す雑なコードを書いた。

```python
(Missing code here)
```

意外としっかり動く。

あとはその JSON を他のセンサーと同じように MQTT にブチ込むだけ。

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

すると LLM はこう吐く。

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe

エージェントが“見える”ようになった！

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

さらに、

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

服装にも容赦なし。

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## All together now

最近オレがオフィスを出たときはこんな感じだった。

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

そしてオフィス Discord はこんなノリ：

{{< image src="/images/posts/office-discord.png" caption="Discord がカオスってる">}}

ウザすぎず笑える、その差はウエハース一枚分ってくらい紙一重のラインを目指し、プロンプトとセンサーを日々チューニング中。

システムは JSON ペイロードさえ来れば何でも扱えるから、センサー拡張も楽勝。

**次は“聴覚”を追加予定だ。**

## Codes! You can run this yourself.

コードは全部オープンソース。見た目は雑だし、LLM に丸投げしたわけでもないけど、動くんだから問題なし。

センサー取得＋LLM 連携本体:  
[harperreed/houseagent](https://github.com/harperreed/houseagent)

“Eyeballs” 用コード:  
[harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

配線はそんなに難しくないが、完全自動でもない。このコードはここ 6〜8 か月ほぼノータッチで走り続け、オレらには常に爆笑を、来客には「何コレ？」を提供し続けてる。試したら知らせてくれ。ハマったら [メール](mailto:harper@modest.com) くれれば、気が向いたら助けるぜ！

そのうち Home Assistant だけで完結できるようになると踏んでる。

**Part 2 は後日投下。VTuber のリグでエージェントに肉体を与えた話をお楽しみに！**
