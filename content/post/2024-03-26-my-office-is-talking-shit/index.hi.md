---
date: 2024-03-26 09:00:00-05:00
description: मैंने सेंसर और एक LLM का उपयोग करके अपने ऑफिस को बोलने लायक बनाया। हमने
  इससे हास्यास्पद LLM-जनित टिप्पणियाँ तैयार कीं—और एक इंटरैक्टिव, गाली-गलौज व व्यक्तित्व
  से भरपूर ऑफिस स्पेस बनाया।
draft: false
generateSocialImage: true
slug: our-office-avatar-pt-1-the-office-is-talking-shit-again
tags:
- office-automation
- sensors
- llm
- home-assistant
- technology
title: 'हमारा ऑफिस अवतार भाग 1: दफ़्तर फिर से बकवास कर रहा है'
translationKey: 'Our Office Avatar pt 1: The office is talking shit again'
---

**tl;dr:** _मैंने ढेर सारे सेंसर और एक LLM की जुगलबंदी से अपने ऑफिस को ऐसा बड़बोला बनाकर खड़ा कर दिया है कि वहाँ जो भी चल रहा हो, वो खुद-बख़ुद हमें सुना देता है। पोस्ट लंबी ज़रूर है, पर समझने में आसान। असल ज़िंदगी में मैं LLMs का कैसे इस्तेमाल कर रहा हूँ, यह इसका धांसू नमूना है।_

2019 में मेरे जिगरी यार Ivan और मैंने शिकागो के इस [कमाल के स्टूडियो](https://company.lol) में काम शुरू किया। ज़्यादातर वक़्त हम बस हरामख़ोरी करते रहे और मज़ेदार चीज़ें ठोकते रहे।

{{< image src="/images/posts/office.webp" caption="हमारा खतरनाक स्टूडियो">}}

शुरू-शुरू में मैंने ढेर सारा समय ऑफिस में सेंसर और ऑटोमेशन फिट करने में झोंक दिया। मक़सद यह था कि कभी भी ऑफिस के माहौल वग़ैरह की पूरी ख़बर रहती रहे।

सारे सेंसर एक जगह लाने के लिए हमने होम असिस्टेंट (Home Assistant) इस्तेमाल किया। फिर मैंने कुछ बोरिंग-सी ऑटोमेशन लिखीं, जो अलग-अलग हालात में नोटिफ़िकेशन फेंकती थीं।

नोटिफ़िकेशन कुछ यूँ थे:

- किसी के पहुँचते ही ऐलान  
- तापमान बहुत गरम या बहुत ठंडा होते ही चेतावनी  
- CO₂ ज़्यादा होते ही अलर्ट  
- दरवाज़ा खुलते-बंद होते ही कन्वीनियंस-स्टोर वाला “डिंग-डॉन्ग”  

हम ये नोटिफ़िकेशन Slack और एक पुराने Google Home स्पीकर (माइक बंद) पर ठेलते थे। स्पीकर की आवाज़ बढ़िया है। उसे हमने क़रीब 12 फ़ुट ऊपर, कमरे के बिलकुल बीच में टाँग दिया—आवाज़ चारों ओर से आती लगती है। अगर आप “नोटिफ़िकेशन स्पीकर” ढूँढ रहे हों, तो ये धमाल है।

उदाहरण देखें:

{{< image src="/images/posts/office-slack.png" caption="काम का, पर बोरिंग">}}

असरदार भले हो, पर मज़ा कम है।

ऑफिस में रहते हुए ये घोषणाएँ बड़े काम की रहीं, और बाहर रहते हुए तो सोने पे सुहागा। कोविड की शुरुआत में, जब किसी को कुछ पत्ता नहीं था, दूर बैठे-बैठे ऑफिस की हालत देख लेना बड़ा सुकून देता था।

अंदर मौजूद रहते वक़्त ये ऐलान और बाकी एम्बिएंट सिग्नल माहौल को ऐसा बना देते थे मानो ऑफिस खुद ज़िंदा हो—अपनी ही पर्सनैलिटी के साथ।

हमें कतई भनक नहीं थी कि आगे क्या तूफ़ान आने वाला था…

## JSON-सिंगुलैरिटी आ चुकी है

अब हम सब जानते हैं कि LLM वाली क्रांति दुनिया भर की चीज़ें तहस-नहस कर रही है, और आने वाले सालों में ज़्यादातर नॉलेज-वर्क को अजीब, जंगली, मज़ेदार और पेचीदा बना देगी।

2020 में GPT-3 आया तो मैंने झटपट अतरंगी सॉफ़्टवेयर बनाना शुरू कर दिया। मैंने ढेर सारे “बॉट” बनाए—ज़्यादातर का टोन बड़ा पर्सनल और बेहिचक था।

मेरा सबसे पसंदीदा “इमर्जेंट” जुगाड़ यह है कि स्ट्रक्चर्ड `JSON` डेटा को LLM से **गद्य** में बदलवाएँ—सीधे-सपाट शब्दों और वाक्यों में।

{{< image src="/images/posts/api-llm-lol.png" caption="मेरा नया फ़ेवरेट ग्राफ़">}}

मिसाल के तौर पर ऐसा JSON लें:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

और उस पर ये मस्त प्रॉम्प्ट ठोकें:

> What should i wear. Be concise, have some personality. Think of this as a tweet telling people what to wear

इसे `GPT-4-turbo` को भेजो और धड़ाम! —

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

ख़ास बात ये कि JSON ऑब्जेक्ट आपको पहले से बाँधकर नहीं देना पड़ता; LLM बहोत लचीला है। चलो मनमाने ढंग से एक फ़ील्ड और जोड़ दो:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

प्रॉम्प्ट वही, और जवाब:

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

सीधा काला जादू है, दोस्तو! 😉

अब एक छोटी-सी Python या Node स्क्रिप्ट बुनो और हो गया—एक बॉट जो हर सुबह स्ट्रक्चर्ड मौसम-डाटा देखकर बताएगा कि क्या पहनना है, वो भी बिना डेटा-फ़ॉर्मैट की झंझट के।

और अगर कहीं एरर आ जाए, तो LLM उसी प्रॉम्प्ट के साथ उसे भी फ़ैशन टिप में बदल देता है:

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

मैं ये पैटर्न लगातार अपनाता हूँ। ज़्यादातर मैं छोटे-मोटे बॉट बनाता हूँ जो मुझे तमाम चीज़ें बताते रहें:

- स्लीप-परफ़ॉर्मेंस एनालिसिस  
- मौसम बॉट  
- [Chicago Alerts ट्विटर अकाउंट](https://twitter.com/chicagoalerts)  
- मेरी E-Ink एम्बिएंट डिस्प्ले के लिए सेंसर-आधारित फ़ैसले  

(_डरो मत, सब कुछ बाद में विस्तार से लिखूँगा._)

## वापस ऑफिस में

2023 की शुरुआत में मेरी कंपनी गोता लगा रही थी, तो दिमाग़ साफ़ करने के लिए मैंने प्रोजेक्ट्स पर जमकर हाथ साफ़ किया। टीम के साथ ऑफिस में वक़्त भी बढ़ा। 2019 वाले स्टेट-बेस्ड सिस्टम की सीमाएँ अब चुभने लगीं।

नई समझ और अचानक मिले फ़ालतू वक़्त के साथ, मैंने ऑफिस की नोटिफ़िकेशन मशीनरी को दोबारा खड़ा करने का तय कर लिया।

सबसे पहले सेंसर-डेटा पकड़ कर उसे मैन्युअली ChatGPT में डाला और देखा क्या निकलता है। सीधा-सादा था, सारा खेल प्रॉम्प्ट का था।

पहला प्रॉम्प्ट ये था:

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

`default_state` भेजा जाता ताकि LLM को पता चले कि नार्मल क्या है, फिर `current_state`, और फिर `last_state`।

मान लो मामला दरवाज़े का है:

- default_state: `{ "front_door": "closed" }`  
- current_state: `{ "front_door": "open" }`  
- last_state: `{ "front_door": "open" }`

LLM बोलेगा:

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

जब कोई बदलाव नहीं, तो बस यही। दरवाज़ा बंद कर दो, तो:

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

बेहद असरदार—थोड़ा चिड़चिड़ा, पर मज़ेदार!

अब बारी थी ढेर सारे सिग्नल एक साथ LLM के मुंह में ठूँसने की।

## सेंसर-बंडल

सबसे बड़ा झंझट ये था कि हर बार किसी सेंसर का स्टेट बदले तो घंटा-घड़ियाल सुनाना भयंकर बोर करता। 2019 वाले स्टेट-बेस्ड जुगाड़ से बेहतर चीज़ बनाने के लिए हमें सेंसर-डेटा को गुच्छों में बाँधना पड़ा।

मैंने एक सिंपल Flask ऐप लिखा, जो MQTT के ज़रिये सेंसर-डेटा समेटता है और जब कुछ शर्तें पूरी होती हैं—समय, बदलाव कितनी तेज़ी से हो रहे हैं (velocity), और इवेंट की गिनती—तब कई स्टेट्स को एक ही पेलोड में गठरी करके भेज देता है।

ऑब्जेक्ट कुछ ऐसा दिखता है:

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

और पेलोड बनता है:

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

इसके बाद इसे OpenAI को भेजते हैं, जो इस JSON को गद्य में बदल देता है:

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

ये सब हमारे पुराने यार MQTT के ज़रिये होता है।

होम असिस्टेंट से सेंसर-बदलाव पकड़कर MQTT पाइप में भेजने के लिए मैंने ये ऑटोमेशन लिखी:

तेज़ बदलाव वाली ऑटोमेशन:

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

धीमे बदलाव वाली ऑटोमेशन:

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

दोनों तभी फायर होंगी जब ऑफिस “occupied” है—आख़िर हर जनरेशन में पैसे लगते हैं; ख़ाली दफ़्तर में एयर-क्वॉलिटी की बकवास कौन सुने! 😉

ये सेट-अप उम्मीद से ज़्यादा बढ़िया चलता है। होम असिस्टेंट में कोई भी नया सेंसर जोड़ दो, एजेंट तुरन्त उस पर बकैती करने लगता है।

मैंने प्रॉम्प्ट अलग फ़ाइल में रखा है ताकि पूरे स्टैक को री-स्टार्ट किए बग़ैर इसकी बदतमीज़ी को ट्यून कर सकूँ।

## अब आँखें भी जोड़ें!

सब कुछ सेट होकर चलने लगा तो सोचा—ऑफिस “देख” भी क्यों न पाए? सुनने में पागलपन लगता है, पर नतीजा जानलेवा मज़ेदार है।

एक छोटी-सी स्क्रिप्ट लिखी; मोशन सेंसर ट्रिगर होते ही सिक्योरिटी कैमरे से स्नैपशॉट लेती है, LLAVA चल रहे डिब्बे पर भेजती है, और वहाँ से उस पल का JSON लौटाती है।

```python
(Missing code here)
```

उम्मीद से बढ़कर काम करता है।

अब इस JSON को भी सेंसर-कलेक्टर में धकेल दिया, ताकि यह भी एक और सेंसर समझा जाए।

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

जिस पर एजेंट दहाड़ा:

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe

अब एजेंट देख भी सकता है! फिर दूसरा तंज:

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

और थोड़ी देर बाद:

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

कपड़ों पर भी छींटाकशी:

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## सब कुछ एक साथ

सारी वायरिंग पूरी होने के बाद, पिछले हफ़्ते मैं ऑफिस से निकला तो ये ऐलान गूँजा:

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

और अब हमारा ऑफिस Discord (बाय-बाय Slack!) कुछ यूँ दिखता है:

{{< image src="/images/posts/office-discord.png" caption="Discord पे हंगामा है, भैया">}}

हम प्रॉम्प्ट और सेंसर लगातार ट्यून करते रहते हैं ताकि यह चिड़चिड़े और फनी के बीच उस पतली रेखा पर संतुलित रहे।

क्योंकि सिस्टम को बस JSON पेलोड चाहिए, नए सेंसर जोड़ना बच्चों का खेल है।

**अगला कदम—सुनना (Hearing is next)**

## कोड! तुम भी चला सकते हो

सारा कोड ओपन-सोर्स है। दिखने में खूबसूरत नहीं, कुछ हिस्सा खुद LLM ने हग्गा-पिट्ठू लिखा है, पर चलता धमाकेदार।

सेंसर पकड़ने और LLM-वाले मज़ाक के लिए कोड: [harperreed/houseagent](https://github.com/harperreed/houseagent)

“आँखों” वाले कोड के लिए: [harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

इसे सेट-अप करना बहुत मुश्किल नहीं, मगर पूरी तरह प्लग-एंड-प्ले भी नहीं है। यह कोड पिछले 6-8 महीनों से बिना खास ताम-झाम के चल रहा है—हमें लगातार हँसाता है और मेहमानों को “WTF!” बुलवाता है। अगर तुम इसे आज़माओ तो ज़रूर बताना। दिक्कत हो तो [ई-मेल](mailto:harper@modest.com) मारो, शायद कुछ जुगाड़ बता दूँ!

मेरा अंदाज़ा है कि जल्दी ही यह सब सीधे Home Assistant के अंदर ही हो पाएगा।

**Part 2 जल्द आएगा—बताएँगे कि VTuber रिग से एजेंट को जिस्म कैसे दिया**