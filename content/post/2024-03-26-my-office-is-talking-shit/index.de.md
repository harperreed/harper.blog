---
date: 2024-03-26 09:00:00-05:00
description: Ich habe Sensoren und ein LLM genutzt, um mein Büro zum Sprechen zu bringen.
  Damit haben wir humorvolle, vom LLM erzeugte Kommentare erstellt – und so einen
  interaktiven Büroraum mit Flüchen und Persönlichkeit geschaffen.
draft: false
generateSocialImage: true
slug: our-office-avatar-pt-1-the-office-is-talking-shit-again
tags:
- office-automation
- sensors
- llm
- home-assistant
- technology
title: 'Unser Büro-Avatar Teil 1: Das Büro labert mal wieder Scheiße'
translationKey: 'Our Office Avatar pt 1: The office is talking shit again'
---

**tl;dr:** _Ich nutze einen Haufen Sensoren und ein LLM, damit unser Büro uns erzählt, was gerade los ist. Der Beitrag ist lang, aber ziemlich geradlinig. Insgesamt ist das ein gutes Beispiel dafür, wie ich LLMs in meinem Alltag einsetze._

In 2019 fingen mein Kumpel Ivan und ich an, in diesem [fantastischen Studio](https://company.lol) hier in Chicago zu arbeiten. Meistens vertrödeln wir die Zeit und bauen jede Menge abgefahrenen Kram.

{{< image src="/images/posts/office.webp" caption="Unser fantastisches Studio">}}

Schon früh steckte ich viel Zeit hinein, Sensoren und Automatisierung im Büro einzurichten. Mein Ziel war, jederzeit Einblick in die Umgebungsbedingungen des Büros zu haben.

Wir nutzten [Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant), um alle Sensoren auf einer Plattform zu bündeln. Ich baute ein paar ziemlich langweilige Automatisierungen, die verschiedene Zustände ansagten.

Die Benachrichtigungen waren recht simpel:

- Ansage, wenn jemand ankommt  
- Ansage, wenn es zu heiß oder zu kalt ist  
- Ansage, wenn der CO₂-Wert zu hoch ist  
- Ladenklingelgeräusch, wenn die Tür geöffnet oder geschlossen wird  

Wir schickten die Benachrichtigungen in Slack und über einen alten Google-Home-Lautsprecher mit deaktiviertem Mikrofon. Der Speaker klingt ziemlich gut und hängt rund 12 ft (ca. 3,7 m) über dem Boden mitten im Raum – so scheint die Stimme von überall zu kommen. Wenn du einen „Notification Speaker“ suchst: Die Dinger sind ziemlich solide.

Hier ein Beispiel für die Notifications:

{{< image src="/images/posts/office-slack.png" caption="Langweilig und nicht sehr smart">}}

Wie man sieht: effektiv, aber ziemlich langweilig.

Die Ansagen waren super hilfreich, wenn wir im Büro waren, und noch hilfreicher, wenn wir weg waren. Gerade zu Beginn von Covid, als niemand irgendetwas wusste, war es angenehm, den Zustand des Büros aus der Ferne überwachen zu können.

Im Büro verliehen die Ansagen und anderen Ambient-Benachrichtigungen dem Raum einen futuristischen Touch – als hätte das Büro eine eigene Persönlichkeit.

Wir hatten keine Ahnung, was als Nächstes kommen würde …

## Die JSON-Singularität ist da.

Wir wissen inzwischen alle, dass die LLM-Revolution gerade alles gewaltig auf den Kopf stellt und die Wissensarbeit in den nächsten Jahren verrückt, wild, spaßig und kompliziert machen wird.

Als GPT-3 im Jahr 2020 erschien, fing ich sofort an, schräge Software damit zu bauen. Ich dachte viel darüber nach, wie ich diese Technologie im Alltag nutzen kann. Ich bastelte jede Menge Bots – die meisten mit sehr persönlichem Tonfall.

Mein liebstes „emergentes“ Kunststück ist, strukturierte `JSON`-Daten per LLM in **Prosa** zu verwandeln. Mit Prosa meine ich keine Gedichte, sondern ganz normale Sätze.

{{< image src="/images/posts/api-llm-lol.png" caption="Mein neues Lieblingsdiagramm">}}

Konkret nehme ich JSON:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

Dann packe ich einen spaßigen Prompt dazu:

> What should i wear. Be concise, have some personality. Think of this as a tweet telling people what to wear

Schicke es an `GPT-4-turbo` und bekomme:

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

Ziemlich simpel. Großartig ist, dass man das JSON nicht vorher definieren muss. Das LLM ist **sehr** flexibel. Fügen wir zum Beispiel einfach noch ein Feld hinzu:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

Und das LLM antwortet – ohne Prompt-Änderung:

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

Das ist praktisch Magie. ;)

Jetzt noch eine simple Python- oder Node-App drumherum und – BAM – hast du einen Bot, der dir jeden Morgen sagt, was du anziehen sollst, basierend auf strukturierten Wetterdaten, um die du dich nicht kümmern musst.

Zum Brüllen: Wenn beim Bau so einer App ein Fehler auftaucht, interpretiert das LLM die Fehlermeldung mit demselben Prompt:

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

Dieses Muster nutze ich ständig. Meistens baue ich kleine Bots, die rumhängen und mir Dinge erzählen:

- Analyse meiner Schlafleistung  
- Wetter-Bot  
- [Chicago Alerts Twitter-Account](https://twitter.com/chicagoalerts)  
- Trifft Entscheidungen darüber, welche Sensordaten meine E-Ink-Ambient-Displays anzeigen  

(_Keine Sorge, das dokumentiere ich später alles._)

## Zurück ins Büro

Anfang 2023 geriet meine Firma ins Trudeln, und ich verbrachte viel Zeit mit Bastelprojekten, um den Kopf freizubekommen. Außerdem war ich wieder häufiger und bewusster mit dem Team im Büro. Die Grenzen der bisherigen zustandsbasierten Automatisierungen von 2019 wurden deutlich.

Bewaffnet mit diesem neuen Paradigma und plötzlich viel Zeit beschloss ich, die Büro-Benachrichtigungen neu aufzusetzen.

Zuerst baute ich einen Prototypen: Ich fing die Sensordaten ab, schickte sie manuell an ChatGPT und schaute, was passierte. Das war recht simpel, aber natürlich stark Prompt-abhängig.

Hier ist der erste Prompt, den wir nutzten

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

Ich übergab also den Grundstatus, den aktuellen Status und – als Joker – den vorherigen Status.

Beispiel für eine Tür:

- default_state: `{ "front_door": "closed" }`  
- current_state: `{ "front_door": "open" }`  
- last_state: `{ "front_door": "open" }`

Das LLM könnte antworten:

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

Es erkennt, dass sich nichts geändert hat, und meldet den Zustand. Schließen wir die Tür, sagt das LLM:

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

Ziemlich überzeugend. Etwas nervig, aber überzeugend!

Nun wollte ich eine GANZE Menge Signale ans LLM schicken und schauen, was passiert.

## Sensor-Bunches

Das Hauptproblem: Man will nicht bei jeder Sensoränderung eine Ansage bekommen. Wir wollten ja etwas Besseres als den alten zustandsbasierten Ansatz von 2019, also mussten wir die Sensoren bündeln.

Ich schrieb eine simple Flask-App, die JSON-Daten der Sensoren via MQTT einsammelte und – anhand bestimmter Parameter (Zeit, Ereignisfrequenz und Anzahl) – mehrere Status in einer Nutzlast zusammenfasste.

Die Objekte sahen so aus:

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

Das wurde zu:

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

Das schickte ich an OpenAI, um die JSON-Nutzlast in Prosa umzuwandeln:

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

Das läuft alles über meinen Freund – und deinen: **MQTT**.

Ich ließ dann Home Assistant die Statusänderungen über die Leitung schicken, wo sie gesammelt und umgewandelt wurden.

Schnell-Änderungs-Automation:

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

Langsame-Änderungs-Automation:

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

Beide feuern nur, wenn das Büro als „occupied“ markiert ist. Da es Geld kostet, die Antworten zu generieren, soll es nicht über die Luftqualität reden, wenn niemand da ist. ;)

Ich habe zwei Automationen, weil manche Status langsam (Luftqualität, Raumpräsenz) und manche schnell sind (Personenpräsenz, Türen, Klima usw.).

Das funktioniert erstaunlich gut. Da es Home-Assistant-Automationen sind, kannst du jeden Sensor hinzufügen, und der Agent plaudert darüber.

Ich habe den Prompt separat ausgelagert, sodass ich ihn anpassen kann, ohne den gesamten Stack neu zu starten – super praktisch, wenn du den Sarkasmus-Level fürs Büro feinjustierst.

## ABER WAS IST MIT AUGEN ?!

Als das alles lief, wollte ich, dass das Büro auch sehen kann. Während ich das schreibe, wirkt das vielleicht wie eine schlechte Idee. Aber es ist urkomisch.

Ich schrieb ein herrlich dummes Stück Code, das bei einer Bewegung ein Snapshot der Überwachungskamera macht, ihn an eine Box mit LLAVA schickt und dann JSON zurückbekommt, was auf dem Bild zu sehen ist.

```python
(Missing code here)
```

Das funktioniert überraschend gut.

Dann schiebe ich dieses JSON einfach in den Sensor-Collector und behandele es wie einen weiteren Sensor.

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

Ergebnis:

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe

Der Agent kann sehen! Das bringt eine neue Ebene:

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

Kurz darauf:

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

Noch ein Beispiel, bei dem es um Kleidung ging:

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## Alles zusammen

Wenn das alles verkabelt ist, entstehen magische Momente wie neulich beim Verlassen des Büros:

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

Und so sieht unser Office-Discord (kein Slack mehr?!) jetzt aus:

{{< image src="/images/posts/office-discord.png" caption="Unser Discord geht ab">}}

Wir feilen ständig am Prompt und an den Sensoren, um die Balance zwischen nervig und witzig zu treffen. Es ist ein hauchdünner Grat.

Da das System eine JSON-Nutzlast erwartet, lässt sich der Agent sehr leicht erweitern, um auf andere Sensoren zu reagieren.

**Als Nächstes bekommt der Agent Ohren**

## Code! Probier’s selbst aus.

Der gesamte Code ist Open Source. Er ist nicht hübsch und wurde größtenteils **nicht** von einem LLM geschrieben. Aber er funktioniert.

Den Code fürs Sensor-Grabbing / LLM-Geplapper gibt’s hier: [harperreed/houseagent](https://github.com/harperreed/houseagent)

Den Code für die Augen hier: [harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

Ich glaube, das Ganze ist nicht superschwer zu verkabeln, aber auch nicht völlig nahtlos. Der Code läuft seit 6–8 Monaten fast ohne Anpassungen. Er ist konstant witzig und sorgt bei uns Bewohnern für ein Grinsen und bei Besucher*innen für ein „wtf“. Falls du es ausprobierst – sag Bescheid. Wenn du Probleme hast, schick mir eine [E-Mail](mailto:harper@modest.com), vielleicht kann ich helfen!

Meine Prognose: Bald geht das alles direkt in Home Assistant.

**Teil 2 kommt später. Dann erzähle ich, wie wir dem Agenten mit einem VTuber-Rig einen Körper gegeben haben.**