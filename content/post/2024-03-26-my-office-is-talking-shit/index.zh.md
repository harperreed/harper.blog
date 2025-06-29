---
date: 2024-03-26 09:00:00-05:00
description: 我用传感器和大型语言模型让办公室开口说话。我们借此生成幽默的 LLM 评论，打造出一个互动的、充满脏话与个性的办公室空间。
draft: false
generateSocialImage: true
slug: our-office-avatar-pt-1-the-office-is-talking-shit-again
tags:
- office-automation
- sensors
- llm
- home-assistant
- technology
title: 我们的办公室化身 第1部分：办公室又在胡扯了
translationKey: 'Our Office Avatar pt 1: The office is talking shit again'
---

**tl;dr：** _我用一堆传感器加上一个大型语言模型（LLM），让办公室随时开口播报最新动态。文章虽然不短，但思路却很清晰。这正是我把 LLM 融入现实生活的一个示范。_

2019 年，我和好友 Ivan 入驻芝加哥这间 [超棒的工作室](https://company.lol)。我们大部分时间都在里面瞎玩，造各种有趣的小东西。

{{< image src="/images/posts/office.webp" caption="我们的超棒工作室">}}

一开始，我花了不少时间给办公室装上传感器并做自动化，目标是随时掌握办公室的环境等各项数据。

我们用 [Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant) 把所有传感器集中到同一平台，我又写了几条简单的自动化来播报各种状态。

通知内容很直白：

- 有人到来时播报  
- 温度过高或过低时播报  
- CO₂ 浓度过高时播报  
- 门开关时播放便利店“叮咚”声  

我们把通知同时推送到 Slack 和一台关闭了麦克风的旧 Google Home 扬声器。那只扬声器音质不错，挂在离地约 12 英尺、房间正中央的位置——听起来像是四面八方都在说话。如果你在物色“通知专用扬声器”，这种型号很靠谱。

示例通知如下：

{{< image src="/images/posts/office-slack.png" caption="有效，但无聊且不够智能">}}

如你所见，虽然实用，却有些单调。

这些播报在我们身处办公室时很方便；在我们离开时就更显其用。尤其是新冠初期大家一头雾水时，能远程监控办公室状态让人安心。

而在办公室时，各种提示与播报又让空间充满未来感——仿佛它知道一切，还带着点个性。

我们当时完全没想到接下来会发生什么……

## JSON 奇点来了

如今大家都知道，LLM 革命正把许多事情搅得天翻地覆，也很可能让未来几年的知识工作变得怪诞、疯狂、好玩又复杂。

2020 年 GPT-3 发布后，我立刻开始折腾各种奇怪的软件，也一直在思考如何把这项技术融入日常。我造了不少 “机器人”（bot），它们输出的语气都颇具个人风格。

我最喜欢的“涌现”技巧，是把结构化的 `JSON` 数据交给 LLM，再让它转换成**自然语言**。这里的自然语言不是诗，而是通俗的文字与句子。

{{< image src="/images/posts/api-llm-lol.png" caption="我最近最爱的那张图">}}

举例来说，把这段 JSON：

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

配上一条有趣的提示词（prompt）：

> What should i wear. Be concise, have some personality. Think of this as a tweet telling people what to wear

送进 `GPT-4-turbo`，就会得到：

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

非常直接。更棒的是，你根本不用预先固定 JSON 的字段，LLM 具有极高的弹性。比如随手再加一个字段：

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

同样的提示词，它依旧能正常回复：

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

简直像魔法。😉

再写几行 Python 或 Node 把流程串起来——每天早上自动告诉你该穿什么的机器人就搞定了，而且不必担心数据格式。

更搞笑的是，如果程序报错，LLM 也会用同一提示词把错误信息解释成段子：

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

我天天用这套路，做了一堆在旁边碎碎念的小机器人：

- 睡眠质量分析  
- 天气机器人  
- [Chicago Alerts Twitter 账号](https://twitter.com/chicagoalerts)  
- 为电子墨水环境显示屏挑选要展示的传感器数据  

（别担心，之后都会补文档。）

## 回到办公室

2023 年初，公司陷入螺旋式下滑，我开始疯狂 hack 各种项目来分散注意力，也更有意识地在办公室陪团队一起工作。2019 年那套基于状态的自动化开始显得捉襟见肘。

有了全新的思路，又突然多了时间，我决定把办公室的通知系统彻底重做一次。

我先做了个原型：捕获传感器数据，手动丢给 ChatGPT，看看它会怎么回应。过程很简单，但显然高度依赖提示词。

以下是我们用的第一版提示词：

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

我会把默认状态传进去，让 LLM 知道常态；然后传入当前状态，并附上上一次状态作对照。

比如门的情况：

- default_state: `{ "front_door": "closed" }`  
- current_state: `{ "front_door": "open" }`  
- last_state: `{ "front_door": "open" }`

LLM 可能回复：

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

它看到状态没变，就轻描淡写地提一句。如果把门关上，它则说：

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

虽然有点吵，但确实有趣！

接着，我把更多信号一起塞给 LLM，看它能玩出什么花样。

## 传感器分组（Sensor Bunches）

最大的问题在于：不能每个传感器一有变化就播报。既然目标是做得比 2019 年的纯状态方案更好，就得把多颗传感器的变化“打包”成一条消息。

我写了个很简单的 Flask 应用，通过 MQTT 收集各传感器发来的 JSON 数据；当满足时间、速度和数量等条件后，把多条状态组装成一个 payload。

单条数据长这样：

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

组装后变成：

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

随后交给 OpenAI，把 JSON 变成人话：

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

这一切都依赖我的老朋友：MQTT。

Home Assistant 的自动化会把传感器变化经由 MQTT 发送出去，由收集器接收并转换。

快速变化自动化：

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

慢速变化自动化：

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

两条自动化都要求办公室处于“occupied”状态才触发——毕竟生成文字要花钱，空房子就别谈空气质量了 😉

之所以拆成两条，是因为有的状态变化慢（空气质量、空间存在），有的变化快（人员在场、门、空调等）。

逻辑很简单：一旦状态改变，就把变化推到 MQTT。

这套方案效果出奇地顺畅。由于基于 Home Assistant 的自动化，我想让智能体关注哪个传感器，随时添加即可。

提示词也被独立出来，这样调整办公室的吐槽风格时，无需重启整套系统，非常方便。

## 还要给它装上“眼睛”！

系统都跑通后，我忽然想让办公室“看得到”。写下这些字时，我也觉得这想法也许不太妙，但它实在太好玩。

我写了一段很简单的代码：当运动传感器被触发时，从监控摄像头抓一帧，传给一台运行 LLAVA 的机器，再返回识别到的 JSON。

```python
(缺少的代码在此)
```

效果出奇地好。

然后我把这段 JSON 也丢进传感器收集器，让它像另一颗传感器一样工作。

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

于是它会吐槽：

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe

智能体现在“有眼睛”了！炫酷度再上一层：

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

随后又来一条：

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

再来一条关于穿搭的吐槽：

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## All together now

当所有东西接在一起后，前几天我离开办公室时就收到了这样一条魔性播报：

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

现在我们的办公室 Discord 长这样：

{{< image src="/images/posts/office-discord.png" caption="Discord 聊天炸开了锅">}}

我们不断调整提示词和传感器，努力把系统保持在“有趣”和“吵闹”之间那条细如刀锋的分界线上。

由于系统期望的就是 JSON，所以想让智能体支持新的传感器非常容易。

**下一步——让它学会“听”！**

## 代码！你也可以自己跑

所有代码都是开源的。写得不算优雅，也并非全部由 LLM 生成，但运行得很稳。

负责抓取传感器数据并让 LLM 说段子的代码：  
[harperreed/houseagent](https://github.com/harperreed/houseagent)

给智能体装“眼睛”的代码：  
[harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

理论上并不难搭，但也谈不上“一键部署”。这套东西已经连续跑了 6–8 个月，几乎没怎么动过，经常把我们逗得哈哈大笑，也让来访的朋友发出“WTF”感叹。如果你动手试了，务必告诉我；有问题就 [发邮件](mailto:harper@modest.com)，也许我能帮上忙！

我猜，用不了多久 Home Assistant 就能直接搞定这一切。

**Part 2 稍后上线——到时再告诉大家我们如何用一套 VTuber 装备给智能体安上“身体”**