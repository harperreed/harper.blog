---
date: 2024-03-26 09:00:00-05:00
description: J'ai utilisé des capteurs et un LLM pour faire parler mon bureau. Nous
  nous en sommes servis pour générer un commentaire humoristique produit par un LLM,
  créant ainsi un espace de bureau interactif, imprégné de grossièretés et de personnalité.
draft: false
generateSocialImage: true
slug: our-office-avatar-pt-1-the-office-is-talking-shit-again
tags:
- office-automation
- sensors
- llm
- home-assistant
- technology
title: 'Notre avatar de bureau partie 1 : Le bureau recommence à dire des conneries'
translationKey: 'Our Office Avatar pt 1: The office is talking shit again'
---

**tl;dr :** _J’utilise tout un tas de capteurs, plus un LLM, pour que mon bureau nous raconte ce qui s’y passe. Ce billet est long, mais il devrait rester assez clair. C’est globalement une bonne démonstration de la façon dont j’utilise les LLM dans la vraie vie._

En 2019, mon pote Ivan et moi avons commencé à bosser dans ce [bureau incroyable](https://company.lol) à Chicago. La plupart du temps, on glande pas mal tout en bricolant plein de trucs marrants.

{{< image src="/images/posts/office.webp" caption="Notre bureau incroyable">}}

Très vite, je me suis consacré à ajouter des capteurs et des automatismes au bureau. Mon objectif : connaître l’état de l’environnement et compagnie du bureau à tout moment.

Nous avons utilisé [Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant) pour centraliser tous les capteurs sur une seule plateforme. J’ai bricolé quelques automatismes assez basiques qui annonçaient divers états.

Les notifications étaient assez simples :

- Annoncer quand quelqu’un arrive  
- Annoncer quand la température est trop chaude ou trop froide  
- Annoncer quand le taux de CO₂ est trop élevé  
- Jouer un son quand la porte s’ouvre ou se ferme (le petit « ding » des supérettes)

On envoyait les notifications vers un canal Slack et vers une vieille enceinte Google Home (micro coupé). L’enceinte fonctionne bien et offre un son correct. On l’a placée à environ 3,7 m de hauteur, bien au centre de l’espace ; on a l’impression que le son vient de partout. Si vous cherchez une enceinte de notification, c’est plutôt solide.

Exemple de notifications :

{{< image src="/images/posts/office-slack.png" caption="Ennuyeux et pas très malin">}}

C’est efficace, mais super ennuyeux.

Les notifications étaient très utiles quand nous étions au bureau, et encore plus quand personne n’était présent. Au début du Covid, quand personne ne comprenait rien, c’était rassurant de pouvoir surveiller l’état du bureau à distance.

Sur place, les annonces et autres notifications ambiantes donnaient au bureau un petit côté futuriste, comme s’il savait ce qui se passait et qu’il avait un peu de personnalité.

On ne se doutait pas de ce qui nous attendait…

## La singularité JSON est arrivée

On sait tous que la révolution des LLM fait tout exploser et qu’elle va probablement rendre le travail intellectuel étrange, déjanté, fun et compliqué dans les prochaines années.

Quand GPT-3 est sorti en 2020, je me suis aussitôt mis à développer des logiciels bizarres pour l’utiliser. J’ai beaucoup réfléchi à la façon d’intégrer cette techno dans mon quotidien. J’ai construit plein de « bots », la plupart avec un ton très personnel.

Mon truc émergent préféré consiste à prendre des données structurées en **JSON** et à les convertir en prose via le LLM. Par prose, je ne parle pas de poèmes : juste de phrases normales.

{{< image src="/images/posts/api-llm-lol.png" caption="Mon nouveau graphe préféré">}}

Concrètement, je prends du JSON :

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

Puis j’ajoute un prompt sympa :

> What should i wear. Be concise, have some personality. Think of this as a tweet telling people what to wear

Je l’envoie à `GPT-4-turbo` et j’obtiens :

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

C’est plutôt simple. Le mieux, c’est qu’il n’y a même pas besoin de prédéfinir l’objet JSON. Le LLM est **très** flexible. Par exemple, ajoutons au hasard une autre donnée :

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

Le LLM répond sans changer le prompt :

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

C’est quasiment de la magie, sérieux 😉.

On relie tout ça avec un petit script Python ou Node.js, et voilà : on a un bot qui te dit quoi porter chaque matin à partir de données météo structurées, sans prise de tête.

Hilarant : si l’appli plante, le LLM interprète l’erreur avec le même prompt :

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

J’utilise ce schéma en permanence. Je construis surtout des petits bots qui traînent et me racontent des trucs :

- Analyse de mes performances de sommeil  
- Bot météo  
- [Compte Twitter Chicago Alerts](https://twitter.com/chicagoalerts)  
- Décisions de capteurs pour mes écrans e-ink ambiants  

(_Pas d’inquiétude, je documenterai tout ça plus tard._)

## Retour au bureau

Début 2023, ma boîte partait en vrille et je passais beaucoup de temps à bidouiller des projets pour me vider la tête. J’étais aussi plus souvent au bureau avec l’équipe. Les limites de la première version d’automatismes basés sur l’état (celle de 2019) ont commencé à se voir.

Armé de ce nouveau paradigme et d’un surplus soudain de temps, j’ai décidé de refaire les notifications du bureau.

D’abord, j’ai prototypé le système en récupérant les données des capteurs et en les envoyant manuellement à ChatGPT pour voir comment il réagirait. C’était assez simple, et évidemment très dépendant du prompt.

Voici le premier prompt qu’on a utilisé :

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

Je passais l’état par défaut pour que le LLM sache ce qu’est la situation normale, puis l’état actuel, et, en joker, l’état précédent.

Par exemple pour une porte :

- default_state : `{ "front_door": "closed" }`  
- current_state : `{ "front_door": "open" }`  
- last_state : `{ "front_door": "open" }`

Le LLM pouvait répondre :

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

Il constate qu’il n’y a pas de changement et indique l’état. Si on ferme la porte, il dit :

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

C’était très convaincant. Un peu agaçant, mais convaincant !

Il était temps d’envoyer tout un tas de signaux au LLM pour voir ce qui se passe.

## Regroupements de capteurs

Le principal problème de cette approche, c’est qu’on ne veut pas une annonce à chaque changement de capteur. Pour faire mieux que l’approche de 2019 basée sur l’état, il fallait regrouper les capteurs.

J’ai donc codé une petite application Flask qui collecte les données **JSON** des capteurs via **MQTT** puis, selon plusieurs paramètres (temps, vitesse de variation et nombre), regroupe un ensemble d’états dans un seul paquet.

Les objets ressemblent à :

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

Ce qui se traduit en :

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

Puis c’est envoyé à OpenAI pour transformer ce JSON en prose :

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

Tout ça passe par notre ami à tous : **MQTT**.

J’ai ensuite un automatisme Home Assistant qui envoie les changements de capteurs pour être collectés puis transformés.

Automatisme pour changements rapides :

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

Automatisme pour changements lents :

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

Comme on le voit, les deux automatismes ne se déclenchent que si le bureau est marqué « occupé ». Chaque réponse coûte de l’argent : pas envie qu’il parle qualité de l’air quand personne n’est là !

J’en ai deux parce que certains états évoluent lentement (qualité de l’air, présence dans l’espace), d’autres très vite (présence individuelle, portes, climatisation (AC), etc.).

Ces automatismes sont très simples : ils guettent un changement d’état puis publient la charge utile sur le topic **MQTT**.

Comme c’est du Home Assistant, je peux ajouter n’importe quel capteur Home Assistant, et l’agent en parlera aussitôt.

Le prompt est séparé, ce qui me permet d’en modifier le ton sans redémarrer toute la pile logicielle (stack). Très pratique pour régler le niveau de sarcasme du bureau.

## ET LES YEUX, ALORS !

Une fois tout cela en place, j’ai voulu que le bureau voie. En l’écrivant, je me dis que c’était peut-être une mauvaise idée. Mais c’est hilarant.

J’ai pondu un bout de code vraiment simple : il se déclenche via un détecteur de mouvement, prend une capture d’une caméra de sécurité, l’envoie à une machine tournant sous **LLAVA** puis récupère un JSON décrivant la scène.

```python
(Missing code here)
```

Ça marche étonnamment bien. J’envoie ensuite simplement ce JSON dans le collecteur, comme s’il s’agissait d’un capteur supplémentaire.

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

Ce qui donne :

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe

L’agent voit ! Ça ajoute un autre niveau :

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

Puis rapidement :

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

Encore un exemple où il commente la tenue :

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## Tous ensemble maintenant

Une fois tout branché, on a eu des moments magiques, comme lorsque j’ai quitté le bureau l’autre jour :

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

Et voilà à quoi ressemble désormais notre serveur Discord :

{{< image src="/images/posts/office-discord.png" caption="Le Discord est en pleine ébullition">}}

On ajuste constamment le prompt et les capteurs pour que ce soit pile entre agaçant et drôle. C’est une ligne très mince.

Comme le système attend un paquet JSON, il est très facile d’étendre l’agent pour réagir à d’autres capteurs.

**La prochaine étape : l’ouïe**

## Le code ! Vous pouvez le faire tourner

Tout le code est open source. Il n’est pas super élégant et n’a pas été majoritairement écrit par un LLM. Mais il fonctionne bien.

Le code qui s’occupe de récupérer les capteurs et de faire parler le LLM est ici : [harperreed/houseagent](https://github.com/harperreed/houseagent)

Le code pour les yeux est là : [harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

Je pense que ce n’est pas très compliqué à câbler, mais ce n’est pas plug-and-play non plus. Ce code tourne sans gros ajustements depuis 6 à 8 mois : c’est constamment hilarant, ça fait toujours sourire les occupants et dire « wtf » aux visiteurs. Si vous tentez le coup, faites-moi signe. Et si vous galérez, envoyez-moi un [email](mailto:harper@modest.com) : je pourrai peut-être aider !

Ma prédiction : bientôt, tout ça sera faisable directement dans Home Assistant.

**La partie 2 arrivera plus tard. Je vous raconterai comment on a utilisé un rig de VTuber pour donner un corps à l’agent.**