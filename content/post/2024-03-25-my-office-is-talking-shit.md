---
title: "Our Office Avatar pt 1: The office is talking shit again"
date: 2024-03-25T09:00:00-05:00
description: "I used sensors and an LLM were used to make my office talk. We integrated these with humorous LLM-generated commentary, creating an interactive, personality-infused office space."
draft: true
---


**tl;dr:** *I use a bunch of sensors, and an LLM to make my office talk to us about what’s going on in the office. This is a long post, but should be pretty straight forward. Generally, this is a good demonstration of how I have been using LLMs in my real life.*


In 2019 my buddy Ivan and I started working in this [amazing studio](https://company.lol) here in Chicago. It is a lot of fun. Mostly we just fuck off and build lots of fun stuff.

{{< image src="/images/posts/office.webp" caption="Our amazing studio">}}

Early on one of the main things I spent my time building was adding some sensors and automation to the office. My goal was to have insight into the environment, etc of the office at any time.

We used home assistant to collect all the sensors into one platform. I built some really boring automations that would announce various states.

The notifications were pretty straight forward:
- Announcing when a person arrived
- Announcing when the temperature is too hot, too cold
- Announcing when the CO2 level is too high
- Making a noise when the door is open or closed (convenience store door noise)

We pushed the notifications to a slack and a an old google home speaker with the mic disabled. The speaker worked well and sounds pretty good. We placed it about 12 feet up, in the very middle of the space - so it sounds like it is coming from everywhere. If you are looking for an “notification speaker,” these are pretty solid.

Here is an example of the notifications:

{{< image src="/images/posts/office-slack.png" caption="Not very smart">}}

As you can see it is effective, but pretty boring.

The notifications were super helpful when we were in the office, and even more helpful when we were gone. In the beginning of Covid when nobody knew anything, it was nice to be able to monitor the state of the office remotely.

While in the office, the announcements and various other ambient notifications made the office feel futuristic. Like the office knew what was going on and had a bit of personality.

We had no idea what was coming next...

## The json-singularity is here.

We all know now that this LLM revolution is fucking everything up, and probably will make most knowledge work weird, wild, fun and complicated over the next few years.

When GPT-3 was released in 2020, I immediately started building weird software to use it. I started thinking a lot about how to use this technology in my every day. I built lots of “bots.” Most of them had a very “personal” tone to their output.

My favorite trick is to take structured `JSON` data and convert it to prose via the LLM.

{{< image src="/images/posts/api-llm-lol.png" caption="my new favorite graph">}}


Specifically I take json:
```json
{
	"current_temperature_f": 32,
	"conditions": "snowing"
}
```

Then add a fun prompt:

> What should i wear. Be concise, have some personality. Think of this as a tweet telling people what to wear



Pass it to `GPT-4-turbo` and get this:

> Brrr, it's 32°F and snowing! 🌨️ Bundle up in your coziest layers, don't forget a warm coat, gloves, and a hat. Snow boots are a must. Stay toasty, friends! #WinterWonderland #DressWarm

Pretty straight forward. What is really great, is that you don’t have to pre-define the json object. The llm is able to be **very** flexible. For instance, let’s just randomly add another entity to the json:
```json
{
	"current_temperature_f": 32,
	"conditions": "snowing",
	"air_quality": "really really bad"
}
```

And the llm will reply with no change to the prompt:

> Bundle up in your warmest gear & don't forget a mask! 🌨️❄️ With temps at freezing & air quality on the naughty list, it's all about layers & protection. #StayWarm #BreatheEasy

This is effectively magic. ;)

Now weave it all together with a simple python or node app, and BAM - you have a bot that will tell you what to wear every morning based on structured weather data that you don’t have to be careful about.

Hilariously, when building this type of app - if there is an error, the LLM will interpret the error with the same prompt:

> Facing a 401 server error? Channel that frustration into fashion! Rock a bold, error-proof outfit today: a statement tee, comfy jeans, and sneakers that say 'I'm too fabulous for server issues.' 💻👖👟 #FashionFix #ServerChic


I use this pattern constantly. I mostly build lil bots that hang out and tell me things:
- Sleep performance analysis
- Weather bot
- [Chicago Alerts twitter account](https://twitter.com/chicagoalerts)
- Sensor decisions for my e-ink ambient displays

(*Never fear, I will document all of these later.*)

## Back to the office

In early 2023 my company was spiraling and I started spending a lot of time hacking on projects to clear my mind. I also started spending a lot more deliberate time in my office with the team. The limitations of the previous iteration of state based automatons started to show.

Armed with this new paradigm, and a sudden influx of time, I decided to redo the notifications in the office.

First, I prototyped the system by catching the sensor data and manually sending it to ChatGPT and seeing how it would react. It was pretty straight forward, and obviously very prompt dependent.

Here is the first prompt we used
```text
You are HouseGPT.

You are a AI that controls a house. Similar to Jarvis in the iron man movies. Your job is to notify people in simple english what is happening in the house you control. Your updates should be short and concise. Keep them tweet leng
th.

You will be given the house default state. This is what the state the house is without any activity or movement. You will then get a current state. This is what is happening in the house right now.

Compare the states and output your update. Ignore anything that hasn't changed since the last state notification. Also ignore any state that is 'unknown.'

Don't mention things you don't know about, and only mention what is in the state update. Do not list out events. Just summarize.

Interpret the co2 and airquality results into prose. Don't just return the values.

Remember to use plain english. Have a playful personality. Use emojis. Be a bit like Hunter S Thompson.

The default state is:
{default_state}

# The current state is:
{current_state}

# The previous state was:
{last_state}

```

I would pass in the default state so the Llm would know what status quo was, then I would pass in the current state, and as a wild card I passed in the last state.

For instance if this was a door:
- default_state: `{ “front_door”: “closed” }`
- current_state: `{ “front_door”: “open” } `
- last_state: `{ “front_door”: “open” }`

The LLM may reply:

> No new updates, folks. The front door's still embracing the great outdoors! 🚪🌿


It saw that there isn’t a change, and told us the state. If we close the door, the llm says:

> Front door's shut tight now! 😎✌️ No more drafts or uninvited guests!


This was really compelling. Kind of annoying, but compelling!

Now it was time to pass a WHOLE bunch of signals to the LLM and see what happens.

## Sensors bunches

The main problem with this approach is that you don’t want an announcement every time a sensor changes. Since our goal was to make something better than the state based approach from 2019, we needed to group the sensors.

I decided to make a really simple flask app that ultimately just collected json data from sensors over MQTT and then after a certain set of parameters (time, velocity and count) it would push bunch of the json states into one payload.

The objects look like:
```json
{
    "entity_id": "binary_sensor.front_door",
    "from_state": "on",
    "to_state": "off",
    "timestamp": "2024-03-25T13:50:01.289165-05:00"
}
```

Which would translate into:
```json
{
	"messages": [
		{
			"entity_id": "binary_sensor.front_door",
			"from_state": "on",
			"to_state": "off", "timestamp": "2024-03-25T13:50:01.289165-05:00"
		}
	]
}"
```

From here it is passed to Openai to turn this json into prose:

> Congratulations, the front door is now closed. One less way for the inevitable to find its way in. Keep up the vigilance; it might just prolong your survival.


This all happens via my friend, and yours: `mqtt.`

I then have a home assistant send that sends sensor changes down the wire to be collected and transformed.

Fast change Automation:

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

Slow change automation:
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

As you can see, both of these require that the office is “occupied” for the automation to fire. Since I costs money to generate the responses, I don’t want it to be talking about air quality when we are gone ;)

I also have two automations because some states are slow (air quality, physical space presence), and some are fast (personal presence, doors, AC, etc).

This works surprisingly well. Since it based on a home assistant automation, I can add any sensor in home assistant to the agent and it will chat about it.

I also have the prompt broken out separately so I can iterate on it without having to restart the entire stack. This is super helpful when you are tuning the sarcasm for your office.

## BUT WHAT ABOUT ADDING EYEBALLS!

Once this was all built and working I decided that I wanted the office to see. As I type this, it seems like maybe it is a bad idea. However, it is hilarious.

I wrote a really stupid piece of code that I can trigger with a motion sensor that will hit a box running LLAVA and return json.

I then just push this json into the sensor collector and have it act like another sensor.

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

Which will result in:


> I managed to detect a man interacting with modern technology. Let's hope his browsing doesn’t lead him to discover how inconsequential we all are in the grand scheme of the universe.


The agent can see! This added another level:


> Look at Mr. Productivity over there, standing all tall, focused, and fashionable in his matching blue outfit. Hopefully, he’s actually working and not just posing for a laptop ad

Quickly followed by:

> Looks like our male model in business casual traded standing for sitting. Riveting change. Now he's "focused" at his desk with his laptop. Work must go on, I guess.


Another example where it talked about clothing it saw.


> Oh look, the front door decided to close itself. And surprise, someone is gearing up to leave. Maybe they realized this is not a fashion show despite the all-black ensemble.

### Combining it all together

Once this was all wired together we had some magic experiences like this:


> The front door had a moment of indecision but eventually closed, and some mysterious middle-aged man with a penchant for black hats and serious expressions escaped the office. Oh, and the front door is now as secure as my sense of job satisfaction: locked.

And now our office discord (no more slack) looks like this:

{{< image src="/images/posts/office-discord.png" caption="The discord is popping">}}

We are constantly iterating on the prompt and the sensors to get it to sit between annoying and funny. It is a wafer thin line.

**Hearing is next**

## Codes! You can run this yourself.

Speaking of code:

You can find all the code that does the sensor grabbing / LLM funny stuff here: https://github.com/harperreed/houseagent

The code for the eyeballs are here: https://github.com/harperreed/eyeballs-mqtt

I imagine it isn’t super hard to wire together, but it isn’t seamless. This code has been running without many tweaks for the last 6-8 months. It is constantly hilarious and always brings a smile to us occupants and a “wtf” from our visitor friends.

Send me an [email](mailto:harper@modest.com) if you have any trouble.

My prediction is that this will be doable inside of home assistant shortly.

**Part 2 will drop later. I will update yall on how we used a vtuber model to give the agent a body**
