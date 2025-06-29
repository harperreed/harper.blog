---
date: 2024-03-26 09:00:00-05:00
description: Usé sensores y un LLM para hacer que mi oficina hablara. Con esto generamos
  comentarios humorísticos creados por un LLM, creando un espacio de oficina interactivo,
  lleno de palabrotas y personalidad.
draft: false
generateSocialImage: true
slug: our-office-avatar-pt-1-the-office-is-talking-shit-again
tags:
- office-automation
- sensors
- llm
- home-assistant
- technology
title: 'Nuestro Avatar de la Oficina pt 1: La oficina vuelve a hablar mierda'
translationKey: 'Our Office Avatar pt 1: The office is talking shit again'
---

**tl;dr:** _Uso un montón de sensores y un LLM para que mi oficina nos cuente qué está pasando. Es una entrada larga, pero bastante sencilla. En general es una buena demostración de cómo estoy utilizando los LLM en mi vida real._

En 2019 mi amigo Ivan y yo empezamos a trabajar en este [estudio alucinante](https://company.lol) aquí en Chicago. Básicamente nos la pasamos vagueando y construyendo cosas divertidas.

{{< image src="/images/posts/office.webp" caption="Nuestro alucinante estudio">}}

Al principio, una de las cosas a las que más tiempo dediqué fue a añadir sensores y automatización a la oficina. Mi objetivo era poder conocer en todo momento el entorno y el estado de la oficina.

Usamos [Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant) para reunir todos los sensores en una sola plataforma. Creé unas automatizaciones bastante aburridas que anunciaban distintos estados.

Las notificaciones eran muy simples:

- Anunciar cuándo llega alguien  
- Anunciar cuándo la temperatura está demasiado alta o demasiado baja  
- Anunciar cuándo el nivel de CO₂ es demasiado alto  
- Emitir un sonido cuando la puerta se abre o se cierra (el «ding» típico de las tiendas de conveniencia)

Mandábamos las notificaciones a Slack y a un viejo altavoz Google Home con el micrófono desactivado. El altavoz funcionaba y sonaba bastante decente. Lo colocamos a unos 3,7 m de altura, justo en el centro del espacio, de modo que parecía que el sonido venía de todas partes. Si buscas un «altavoz para avisos», estos son bastante fiables.

Aquí tienes un ejemplo de las notificaciones:

{{< image src="/images/posts/office-slack.png" caption="Aburridas y nada inteligentes">}}

Como puedes ver, son útiles, pero bastante aburridas.

Las notificaciones resultaban muy útiles cuando estábamos en la oficina, y aún más cuando no estábamos. Al inicio de la pandemia de COVID-19, cuando nadie sabía nada, era reconfortante poder vigilar el estado de la oficina a distancia.

Cuando estábamos allí, los anuncios y otras notificaciones ambientales hacían que el espacio pareciera sacado del futuro, como si la oficina supiera lo que pasaba y tuviera personalidad.

No teníamos ni idea de lo que se nos venía encima…

## La singularidad JSON ya está aquí

Ahora todos sabemos que esta revolución de los modelos de lenguaje grande (LLM) lo está poniendo todo patas arriba y, probablemente, convertirá gran parte del trabajo intelectual en algo raro, salvaje, divertido y complicado durante los próximos años.

Cuando salió GPT-3 en 2020, enseguida empecé a crear software rarísimo para usarlo. Pensé mucho en cómo aprovechar esta tecnología en mi día a día. Construí un montón de *bots*, la mayoría con un tono muy personal en sus mensajes.

Mi truco «emergente» favorito es tomar datos estructurados en JSON y convertirlos en **prosa** mediante el LLM. Cuando digo prosa, no me refiero a poemas; hablo de palabras y frases.

{{< image src="/images/posts/api-llm-lol.png" caption="Mi nueva gráfica favorita">}}

Concretamente, tomo un JSON:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

Luego añado un *prompt* divertido:

> What should I wear. Be concise, have some personality. Think of this as a tweet telling people what to wear

Lo paso a `GPT-4-turbo` y obtengo esto:

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

Bastante sencillo. Lo realmente genial es que no hace falta predefinir el objeto JSON; el LLM es **muy** flexible. Por ejemplo, añadamos al azar otra entidad al JSON:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

Y el LLM responderá sin cambiar el *prompt*:

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

Esto es, efectivamente, magia ;)

Ahora, conéctalo todo con una aplicación sencilla en Python o Node.js y ¡BAM!, tienes un *bot* que te dirá cada mañana qué ponerte a partir de datos meteorológicos estructurados sin que tengas que andarte con cuidado.

Lo más gracioso es que, al construir este tipo de app, si hay un error, el LLM interpretará el error con el mismo *prompt*:

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

Uso este patrón constantemente. Principalmente creo *bots* pequeñitos que se quedan por ahí contándome cosas:

- Análisis del rendimiento del sueño  
- *Bot* del tiempo  
- [Cuenta de Twitter Chicago Alerts](https://twitter.com/chicagoalerts)  
- Decisiones de sensores para mis pantallas de tinta electrónica  

(_No temas, documentaré todo esto más adelante._)

## De vuelta a la oficina

A principios de 2023 mi empresa empezó a entrar en barrena y yo me puse a trastear en proyectos para despejar la mente. También pasé más tiempo, de forma deliberada, en la oficina con el equipo. Las limitaciones de las automatizaciones basadas en estados de 2019 empezaron a notarse.

Con este nuevo paradigma y un repentino excedente de tiempo, decidí rehacer las notificaciones de la oficina.

Primero, prototipé el sistema capturando los datos de los sensores y enviándolos manualmente a ChatGPT para ver cómo reaccionaba. Era bastante directo y, obviamente, muy dependiente del *prompt*.

Este fue el primer *prompt* que usamos

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
is 'unknown.'

Don't mention things you don't know about, and only mention what is in the
state update. Do not list out events. Just summarize.

Interpret the co2 and airquality results into prose. Don't just return the
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

Le pasaba el estado por defecto para que el LLM supiera cuál era la situación normal, luego el estado actual y, como comodín, el último estado.

Por ejemplo, si se trata de una puerta:

- default_state: `{ "front_door": "closed" }`  
- current_state: `{ "front_door": "open" }`  
- last_state: `{ "front_door": "open" }`

El LLM puede responder:

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

Vio que no había cambio y nos informó. Si cerramos la puerta, el LLM dice:

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

Era muy convincente. Un poco molesto, ¡pero convincente!

Ahora tocaba enviarle un MONTÓN de señales al LLM y ver qué pasaba.

## Montones de sensores

El principal problema con este enfoque es que no quieres un anuncio cada vez que cambia un sensor. Como nuestro objetivo era algo mejor que la versión basada en estados de 2019, necesitábamos agrupar los sensores.

Decidí crear una aplicación muy sencilla en Flask que recogía datos JSON de sensores vía MQTT y, tras cumplir ciertos parámetros (tiempo, velocidad de cambio y cantidad), enviaba un montón de estados JSON en una sola carga útil.

Los objetos tienen este aspecto:

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

Que se traduce en:

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

De ahí se pasa a OpenAI para convertir este JSON en prosa:

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

Todo esto sucede gracias a mi amigo y, por qué no, el tuyo: **MQTT**.

Luego tengo Home Assistant enviando los cambios de sensor por la red para ser recopilados y transformados.

### Automatización de cambios rápidos

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

### Automatización de cambios lentos

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

Como ves, ambas requieren que la oficina esté «ocupada» para que la automatización se active. Como cuesta dinero generar respuestas, no quiero que se hable de la calidad del aire cuando no estamos ;)

Tengo dos automatizaciones porque algunos estados cambian lentamente (calidad del aire, presencia en el espacio físico) y otros son rápidos (presencia personal, puertas, aire acondicionado, etc.).

Las automatizaciones son bastante simples: buscan un cambio de estado y luego envían ese cambio al tema de MQTT.

Esto funciona sorprendentemente bien. Al ser una automatización de Home Assistant, puedo añadir cualquier sensor a la lista y el agente hablará sobre él.

Además, tengo el *prompt* separado para poder iterar sin reiniciar toda la *stack*. Esto es muy útil cuando ajustas el nivel de sarcasmo de tu oficina.

## ¡PERO QUÉ TAL SI LE PONEMOS OJOS!

Una vez que todo esto estaba montado y funcionando, decidí que quería que la oficina viera. Mientras escribo esto, parece quizá una mala idea. Sin embargo, es graciosísimo.

Escribí un script muy sencillo que se activa con un sensor de movimiento, toma una instantánea de una cámara de seguridad, la envía a una máquina con LLAVA y devuelve un JSON de lo que había en la cámara en ese momento.

```python
(Missing code here)
```

Funciona sorprendentemente bien.

Luego simplemente envío este JSON al recolector de sensores y hago que actúe como otro sensor.

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

Lo que resulta en:

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe

¡El agente puede ver! Esto añadió otra dimensión:

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

Seguido rápidamente por:

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

Otro ejemplo en el que habló de ropa:

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## Todos juntos ahora

Una vez conectado todo, vivimos momentos mágicos como este cuando me fui de la oficina el otro día:

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

Y ahora nuestro Discord de la oficina (¿adiós Slack?) luce así:

{{< image src="/images/posts/office-discord.png" caption="El Discord está que arde">}}

Estamos ajustando constantemente el *prompt* y los sensores para que se sitúe entre molesto y gracioso. Es una línea finísima (tan fina como una oblea).

Como el sistema espera una carga JSON, es muy fácil ampliar el agente para reaccionar a otros sensores.

**Lo próximo: ¡hacer que oiga!**

## ¡Código! Puedes ejecutarlo tú mismo

Todo el código es *open source*. No es bonito y la mayor parte **no** la escribió un LLM, pero funciona de maravilla.

El código que se encarga de capturar sensores y soltar las gracias con el LLM está aquí: [harperreed/houseagent](https://github.com/harperreed/houseagent)

El código para los ojos está aquí: [harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

Imagino que no es súper difícil de conectar, pero tampoco es plug-and-play. Este código lleva funcionando desde hace 6-8 meses sin muchos retoques. Es constantemente hilarante y siempre arranca una sonrisa a los ocupantes y un «wtf» a nuestros visitantes. Si te animas, cuéntame. Además, si tienes problemas, mándame un [email](mailto:harper@modest.com) y quizá pueda ayudarte.

Mi predicción es que pronto se podrá hacer todo esto directamente en Home Assistant.

**La Parte 2 saldrá más adelante. Les contaré cómo usamos un _rig_ de vtuber para darle un cuerpo al agente**