---
date: 2024-03-26 09:00:00-05:00
description: センサーとLLMを使ってオフィスに喋らせた。面白く、下品さと個性を盛り込んだLLM生成コメントでインタラクティブなオフィス空間を作り出した。
draft: false
generateSocialImage: true
tags:
- office-automation
- sensors
- llm
- home-assistant
- technology
title: '私たちのオフィスアバター パート1：またオフィスがクソ喋ってる

  description: センサーとLLMを使ってオフィスに喋らせた。面白く、下品さと個性を盛り込んだLLM生成コメントでインタラクティブなオフィス空間を作り出した。'
translationKey: 'Our Office Avatar pt 1: The office is talking shit again'
---

**tl;dr:** _山ほどあるセンサー＋LLMで、オフィスがいま何が起きてるかをしゃべりまくる仕組みを作った。ポストは長いけど内容はわかりやすいしシンプル。リアルライフで LLM をどう使ってるかの良いデモだぜ。_

2019 年、友人の Ivan とオレはシカゴの [クソ最高なスタジオ](https://company.lol) で仕事を始めた。基本ダラダラ遊びつつ、面白いモノを作りまくってる。

{{< image src="/images/posts/office.webp" caption="クソ最高なスタジオ">}}

最初にやったのは、オフィスにセンサーと自動化をぶち込むこと。狙いは、いつでもオフィスの環境や状態をのぞき見できるようにすることだった。

オレらは [Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant) に全部のセンサーをまとめて、超つまんねぇオートメーションを書いて状態をアナウンスさせた。

通知内容はこんな感じ:

- 人が来たらアナウンス  
- 暑すぎ／寒すぎをアナウンス  
- CO₂ がヤバいとアナウンス  
- ドアの開閉でコンビニの「チーン」音

通知は Slack と、マイクを切った古い Google Home スピーカーに飛ばしてた。スピーカーは音が良くて天井 3.7 m くらいのど真ん中に置いたから、声が空間全体から降ってくる感じ。通知用スピーカーとしてはかなりイケてる。

通知の例:

{{< image src="/images/posts/office-slack.png" caption="役立つけど賢くはなく、そして退屈">}}

見てのとおり効くけど、クッソ退屈。

オフィスにいるときも、離れてるときも通知は助かった。COVID 初期で何もわからなかった頃、リモートでオフィスの様子を見守れるのは心強かった。

オフィスにいると、アナウンスや環境音っぽい通知で未来感が出て「オフィスに人格あるじゃん」って気分になる。

このあと何が来るかなんて、まるで想像してなかった――

## JSON シンギュラリティがやって来た

ご存じのとおり、LLM 革命は世の中をマジでぶっ壊しにかかってて、これから数年、知的労働はワイルド＆カオス＆エキサイティングになるはず。

2020 年に GPT-3 が出た瞬間、オレは速攻でヘンテコソフトを書きまくり、「これを日常でどう使うか」を考え倒した。その結果“ボット”を量産して、ほとんどが超パーソナルなトーンでしゃべる。

お気に入りの“創発”ワザは、構造化された `JSON` を LLM に食わせて **文章** に変換させること。詩じゃなくて、普通の文ね。

{{< image src="/images/posts/api-llm-lol.png" caption="最近のお気に入りグラフ">}}

たとえばこの JSON:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

にプロンプトを添える:

> What should i wear. Be concise, have some personality. Think of this as a tweet telling people what to wear

`GPT-4-turbo` の返事:

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

シンプルだし、JSON をガチガチに定義しなくても OK。LLM の柔軟さはチート級だ。試しに項目を足してみよう:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

同じプロンプトで――

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

まじ魔法。

あとは Python か Node でちゃちゃっとラップすれば、毎朝「今日何着りゃいい?」を教えてくれるボットのできあがり。

笑えるのは、エラーが出ても LLM が同じノリでエラーをツイート風にしゃべること。

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

このパターンは常用してて、たとえば――

- 睡眠パフォーマンス解析  
- 天気ボット  
- [Chicago Alerts Twitter アカウント](https://twitter.com/chicagoalerts)  
- E-ink アンビエントディスプレイ用のセンサー選別  

(_これらはそのうち詳しく書くわ。_)

## オフィスの話に戻ろうぜ

2023 年初頭、会社がスパイラル状態になり、気分転換にプロジェクトをハックしまくってた。オフィスにいる時間も増えたおかげで、2019 年版の状態ベース自動化が限界なのが見えてきた。

新しいパラダイムと余った時間を手に、通知システムを全部作り直すことに。

まずセンサーデータをキャッチして、手動で ChatGPT に投げて反応を見るプロトタイプを作った。結果は当然プロンプト次第。

最初のプロンプトはこれ:

```text
You are HouseGPT.

You are a AI that controls a house. Similar to Jarvis in the iron man movies.
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

`default_state` がデフォ、`current_state` が現在、`last_state` が直前の状態。

たとえばドアの場合:

- default_state: `{ "front_door": "closed" }`  
- current_state: `{ "front_door": "open" }`  
- last_state: `{ "front_door": "open" }`

LLM の返事:

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

変化なし、と判断。ドアを閉めると――

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

面白いけど、ちょいウザい。でもクセになる！

次はもっと大量のシグナルを一気に LLM にぶち込んでみた。

## センサーをまとめてブチ込む

問題は、センサーが変わるたびにアナウンスされたら騒がしすぎること。2019 年版よりマシにするために、センサーの変化を束ねる仕組みが必要だ。

そこで超シンプルな Flask アプリを作成。MQTT 経由でセンサーの JSON を受け取り、時間・変化量・件数などの条件がそろったらまとめて 1 つのペイロードにして送る。

オブジェクト例:

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

束ねると:

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

これを OpenAI に投げると――

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

ここでも相棒は `mqtt`。

Home Assistant のオートメーションがセンサー変化を拾って MQTT に流すので、新しい Home Assistant センサーを追加すれば即しゃべり出す。

### 高速変化オートメーション (5 秒)

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

### 低速変化オートメーション (5 分)

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

どちらもオフィスが `occupied` のときだけ発火。応答生成は課金だから、留守中に空気質を実況されてもムダ金だしね。

プロンプトは別ファイルに分けてあるので、スタックを再起動せずにトーン――とくに“皮肉度”――をチューニングできる。これがマジ便利。

## んで、“目” を付けたらどうよ？

仕組みが安定したところで、「オフィスに視覚持たせたら爆笑じゃね？」と思い立った。こう書くと若干ヤバい気もするけど、実際おもろい。

モーションセンサーをトリガーに防犯カメラのスナップショットを撮り、LLAVA を走らせて JSON で返す――そんなクソ単純なコードを書いた。

```python
# (コードは割愛)
```

意外とちゃんと動く。

返ってきた JSON をそのまま追加センサーとして MQTT に流し込む。

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

すると――

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe

エージェントが“見える”ようになった！  
さらに――

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

続いて――

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

服装イジりも――

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## ぜんぶ合体するとこうなる

この前オフィスを出たときの実況がコレ:

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

そして今やオフィス Discord（もう Slack じゃないってこと?!）はこんな感じ:

{{< image src="/images/posts/office-discord.png" caption="Discord がバチバチに盛り上がり中">}}

「ウザい」と「笑える」のクレープ並みに薄いラインを狙って、プロンプトとセンサーを日々チューニングしてる。

システムは JSON ペイロードを待ってるだけだから、センサーを増やすのも超ラク。

**次は“聴覚”を付ける予定だぜ**

## コード公開 — 自分でも動かせるぞ

コードは全部 OSS。見た目はキレイじゃないし、ほぼ LLM も書いてないけど、ちゃんと動く。

- センサー取得＆LLM 変換: [harperreed/houseagent](https://github.com/harperreed/houseagent)  
- “目玉” カメラ側コード: [harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

配線はそこまで難しくないと思うけど、かといって完全シームレスでもない。とはいえ 6〜8 か月ほぼノーメンテで動いてて、居住メンバーには笑顔を、来客には「WTF?」を提供中。試したらぜひ教えてくれ。ハマったら [メール](mailto:harper@modest.com) くれたら、たぶん助ける！

そのうち全部 Home Assistant だけで完結するようになると予想。

**Part 2 は後日！ VTuber リグでエージェントに“身体”を与えた話をお楽しみに！**