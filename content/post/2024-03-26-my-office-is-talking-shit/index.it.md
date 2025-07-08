---
date: 2024-03-26 09:00:00-05:00
description: Ho usato sensori e un LLM per far parlare il mio ufficio. Con questo
  abbiamo generato un commento umoristico prodotto dall'LLM, creando uno spazio di
  lavoro interattivo, intriso di parolacce e personalità.
draft: false
generateSocialImage: true
slug: our-office-avatar-pt-1-the-office-is-talking-shit-again
tags:
- office-automation
- sensors
- llm
- home-assistant
- technology
title: 'Il nostro Avatar d''Ufficio pt 1: l''ufficio torna a sparare cazzate'
translationKey: 'Our Office Avatar pt 1: The office is talking shit again'
---

**tl;dr:** _Uso un mucchio di sensori e un LLM per far sì che il mio ufficio ci parli di ciò che succede al suo interno. È un post lungo ma piuttosto facile da seguire. In generale, è un ottimo esempio di come utilizzo gli LLM nella vita di tutti i giorni._

Nel 2019 io e il mio amico Ivan abbiamo iniziato a lavorare in questo [studio pazzesco](https://company.lol) qui a Chicago. Passiamo il tempo cazzeggiando e costruendo un sacco di roba divertente.

{{< image src="/images/posts/office.webp" caption="Il nostro fantastico studio">}}

Fin dall’inizio ho dedicato parecchio tempo ad aggiungere sensori e automazioni all’ufficio. L’obiettivo era poter conoscere in ogni momento l’ambiente e, in generale, lo stato dell’ufficio.

Abbiamo usato [Home Assistant](https://en.wikipedia.org/wiki/Home_Assistant) per raggruppare tutti i sensori in un’unica piattaforma. Ho creato automazioni piuttosto noiose che annunciavano vari stati.

Le notifiche erano piuttosto semplici:

- Annuncio dell’arrivo di una persona  
- Avviso quando la temperatura è troppo alta o troppo bassa  
- Avviso quando il livello di CO₂ è troppo alto  
- Suono quando la porta si apre o si chiude (il classico «ding» da negozio)

Le notifiche finivano su un workspace Slack e su un vecchio Google Home con il microfono disattivato. L’altoparlante, montato a circa tre metri e mezzo di altezza al centro dello spazio, ha una resa sonora niente male e fa sembrare la voce provenire da ogni direzione. Se cercate un «notification speaker», questi dispositivi sono un’ottima scelta.

Ecco un esempio delle notifiche:

{{< image src="/images/posts/office-slack.png" caption="Noiose e per niente intelligenti">}}

Come vedete, sono efficaci ma parecchio monotone.

Le notifiche erano utilissime quando eravamo in ufficio e ancora di più quando eravamo via. All’inizio del Covid, quando nessuno sapeva nulla, era comodissimo poter monitorare lo stato dell’ufficio da remoto.

Mentre eravamo presenti, gli annunci e le altre notifiche ambientali facevano sembrare lo spazio futuristico, come se sapesse cosa stava succedendo e avesse un po’ di personalità.

Non sapevamo cosa ci aspettava…

## La singolarità del JSON è arrivata

Ormai sappiamo tutti che questa rivoluzione degli LLM sta mandando tutto a puttane e probabilmente renderà il lavoro intellettuale strano, folle, divertente e complicato nei prossimi anni.

Quando GPT-3 uscì nel 2020, cominciai subito a creare software bizzarro che lo sfruttasse. Pensavo di continuo a come usare questa tecnologia nella vita di tutti i giorni e misi insieme un sacco di bot, quasi tutti con un tono molto personale.

Il mio trucco «emergente» preferito è prendere dati strutturati in `JSON` e convertirli in **prosa** tramite l’LLM. Per prosa non intendo poesie, ma parole e frasi.

{{< image src="/images/posts/api-llm-lol.png" caption="Il mio nuovo grafico preferito">}}

Per esempio, prendo questo JSON:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing"
}
```

Poi aggiungo un prompt divertente:

> What should I wear? Be concise, have some personality. Think of this as a tweet telling people what to wear

Lo passo a `GPT-4-turbo` e ottengo:

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

Niente di complicato.

La cosa fantastica è che non serve definire in anticipo l’oggetto JSON: l’LLM è estremamente flessibile. Per esempio, aggiungiamo a caso un’altra voce:

```json
{
    "current_temperature_f": 32,
    "conditions": "snowing",
    "air_quality": "really really bad"
}
```

E l’LLM risponde senza cambiare prompt:

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

È praticamente magia. ;)

Ora unite il tutto con una semplice app in Python o Node e… BAM: avete un bot che, ogni mattina, vi dice come vestirvi in base a dati meteo strutturati senza doverci pensare troppo.

Esilarante: se c’è un errore, l’LLM lo interpreta con lo stesso prompt:

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic

Uso questo schema in continuazione. Di solito costruisco piccoli bot che se ne stanno lì a raccontarci cose:

- Analisi delle prestazioni del sonno  
- Bot del meteo  
- [Account Twitter Chicago Alerts](https://twitter.com/chicagoalerts)  
- Decisioni basate sui sensori per i miei display e-ink ambientali  

(_Documenterò tutto più avanti._)

## Ritorno all’ufficio

A inizio 2023 la mia azienda era in caduta libera e ho iniziato a dedicarmi a progetti di hacking per schiarirmi la mente. Passavo anche molto più tempo in ufficio con il team, così vennero a galla i limiti della vecchia soluzione basata sugli stati del 2019.

Armato di questo nuovo paradigma e con un improvviso surplus di tempo, decisi di rifare le notifiche in ufficio.

Per prima cosa ho prototipato il sistema intercettando i dati dei sensori e inviandoli manualmente a ChatGPT per vedere come reagiva. Era tutto piuttosto semplice ed era, ovviamente, molto dipendente dal prompt.

Ecco il primo prompt che abbiamo usato:

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

Interpret the CO2 and air quality results into prose. Don't just return the
values.

Remember to use plain English. Have a playful personality. Use emojis.
Be a bit like Hunter S. Thompson.

The default state is:
{default_state}

# The current state is:
{current_state}

# The previous state was:
{last_state}
```

Gli passavo lo stato di partenza, poi lo stato attuale e, come carta jolly, lo stato precedente.

Per esempio, se si tratta di una porta:

- default_state: `{ "front_door": "closed" }`  
- current_state: `{ "front_door": "open" }`  
- last_state: `{ "front_door": "open" }`

L’LLM potrebbe rispondere:

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿

Vede che non c’è cambiamento e ce lo comunica. Se chiudiamo la porta, l’LLM dice:

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!

È davvero coinvolgente. Un po’ fastidioso, ma coinvolgente!

Ora era il momento di inviare un sacco di segnali all’LLM e vedere che succedeva.

## Sensori ammucchiati

Il problema principale di questo approccio è che non volete un annuncio ogni volta che cambia un sensore. Poiché l’obiettivo era superare il sistema basato sugli stati del 2019, bisognava raggruppare gli eventi.

Ho quindi creato una semplicissima app Flask che raccoglieva dati JSON dai sensori via MQTT e, dopo un certo insieme di parametri (tempo, frequenza e numero di eventi), raggruppava gli stati in un unico payload.

Gli oggetti sono fatti così:

```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

che si trasforma in:

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

Da qui viene passato a OpenAI per trasformare il JSON in prosa:

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.

Tutto viaggia attraverso il nostro (e vostro) amico: `mqtt`.

In Home Assistant ho due automazioni che inviano i cambi di stato sul topic da raccogliere e trasformare.

Automazione per i cambi veloci:

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

Automazione per i cambi lenti:

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

Come vedete, entrambe richiedono che l’ufficio sia «occupato» perché scattino. Generare risposte costa, quindi non voglio che parli di qualità dell’aria quando non c’è nessuno. ;)

Funziona sorprendentemente bene. Essendo un’automazione di Home Assistant, posso aggiungere qualsiasi sensore e l’agente ne parlerà.

Tengo anche il prompt separato, così posso modificarlo senza riavviare l’intero stack: utilissimo per calibrare il sarcasmo dell’ufficio.

## MA SE AGGIUNGESSIMO GLI OCCHI!

Quando tutto funzionava, ho deciso che volevo che l’ufficio potesse vedere. Mentre lo scrivo mi rendo conto che forse non è l’idea migliore, però è esilarante.

Ho scritto un pezzo di codice stupidissimo che, al trigger di un sensore di movimento, cattura un’istantanea dalla videocamera di sicurezza, la manda a una macchina con LLAVA e restituisce un JSON con ciò che c’era nell’inquadratura.

```python
(Missing code here)
```

Funziona sorprendentemente bene.

Poi infilo quel JSON nel collettore, facendolo comportare come un sensore qualsiasi:

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

Che produce:

> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe.

Ora l’agente ci vede! Questo ha aggiunto un ulteriore livello:

> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad.

Subito seguito da:

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.

Ancora un esempio, stavolta sui vestiti:

> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

## Tutto insieme, adesso

Quando tutto era collegato, abbiamo vissuto momenti magici, tipo quando sono uscito dall’ufficio l’altro giorno:

> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

E ora il nostro Discord (niente più Slack?!) è così:

{{< image src="/images/posts/office-discord.png" caption="Il nostro Discord scoppia di notifiche">}}

Stiamo costantemente ritoccando i prompt e i sensori per restare su una linea sottile come un wafer tra il fastidioso e l’esilarante.

Poiché il sistema si aspetta un payload JSON, è facilissimo estendere l’agente per reagire ad altri sensori.

**Il prossimo passo è l’udito**

## Codice! Potete provarci anche voi.

Tutto il codice è open source. Non è un capolavoro estetico e non è stato scritto per lo più da un LLM, ma funziona.

Il codice che si occupa della raccolta dei sensori e delle battute via LLM è qui: [harperreed/houseagent](https://github.com/harperreed/houseagent)

Il codice per gli «occhi» è qui: [harperreed/eyeballs-mqtt](https://github.com/harperreed/eyeballs-mqtt)

Non dovrebbe essere troppo difficile da mettere in piedi, ma non è plug-and-play. Questo codice gira senza particolari ritocchi da 6–8 mesi: è costantemente esilarante e strappa sempre un sorriso a noi occupanti e un «wtf» agli amici in visita. Se ci provate, fatecelo sapere. E se avete problemi, mandate un’[email](mailto:harper@modest.com) e magari possiamo aiutare!

La mia previsione è che presto sarà possibile fare tutto direttamente dentro Home Assistant.

**La parte 2 arriverà più avanti. Vi aggiorneremo su come abbiamo dato un corpo all’agente usando un rig da VTuber.**