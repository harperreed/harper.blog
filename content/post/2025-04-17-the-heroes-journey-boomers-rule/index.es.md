---
bsky: https://bsky.app/profile/harper.lol/post/3ln2a3x52xs2y
date: 2025-04-17 09:00:00-05:00
description:
    Una guía completa que detalla la evolución del desarrollo de software
    asistido por IA, desde el autocompletado básico de código hasta los agentes de codificación
    totalmente autónomos, con pasos prácticos e ideas para maximizar la productividad
    mediante la integración de LLM.
draft: false
generateSocialImage: true
slug: an-llm-codegen-heros-journey
tags:
    - llm
    - coding
    - artificial-intelligence
    - development-workflow
    - software-engineering
    - developer-productivity
    - boomers
title: "El viaje del héroe del codegen con LLM"
translationKey: An LLM Codegen Hero's Journey
---

Desde que publiqué aquella [entrada del blog](/2025/02/16/my-llm-codegen-workflow-atm/) sobre mi flujo de trabajo con _LLM_, he pasado muchísimo tiempo hablando con gente acerca de la generación de código: cómo empezar, cómo mejorar y por qué resulta tan atractiva.

La energía y el interés que ha despertado el tema son increíbles. He recibido montones de correos de personas que intentan descifrar todo esto. Empecé a notar que muchos se preguntan por dónde iniciar y cómo encajar todas las piezas. Entonces caí en la cuenta de que llevo trasteando con este proceso desde 2023 y he visto de todo. Jajaja.

Hablando de ello con unos amigos (¡que se manifieste la gente de Fisaconites!) envié este mensaje en un hilo sobre agentes asistidos por IA y editores:

> Si estuviera empezando, no sé si sería útil saltar directamente a los agentes que programan. Es engorroso y extraño. Tras guiar a varias personas en esto (con éxito y sin él), veo que la «ruta del héroe» —empezar con Copilot, pasar al copiar y pegar en Claude Web, luego a Cursor/Continue y, por último, a los agentes totalmente automatizados— suele ser la forma más exitosa de adoptarlo todo.

Esto me hizo pensar mucho en el viaje y en cómo iniciarse en la programación con agentes (_agentic coding_):

> El aviso es que esto va, sobre todo, para gente con experiencia. Si casi no tienes experiencia como _dev_, entonces a la mierda: salta directo al final. **Nuestros cerebros suelen estar arruinados por las reglas del pasado.**

## Un viaje para la vista y el oído

{{< image src="journey-harper.webp" alt="Harper inspira confianza" caption="Tu guía reflexiva: Harper. iPhone X, 10 jun 2018" >}}

Este es mi recorrido. Es, en gran medida, el camino que yo seguí. Creo que podrías recorrerlo a toda velocidad si te lo propones. No necesitas cumplir cada paso al pie de la letra, pero pienso que cada uno suma.

Aquí van los pasos:

### Paso 1: Levántate de la cama con asombro y optimismo

Jaja. Es broma. ¿A quién le da la vida para eso? Tal vez ayude, pero el mundo se desmorona y lo único que tenemos para distraernos es el _codegen_.

Conviene asumir que estos flujos de trabajo pueden funcionar y aportar valor. Si odias los _LLM_ y crees que no sirven, aquí no tendrás éxito. ¯\\\_(ツ)\_/¯

### Paso 2: Empieza con autocompletado asistido por IA

¡Este es el auténtico paso uno! Necesitas pasar suficiente tiempo en el IDE para saber qué tal trabajas con [IntelliSense](https://en.wikipedia.org/wiki/Code_completion), [Zed Autocomplete](https://zed.dev/blog/out-of-your-face-ai), [Copilot](https://copilot.github.com/), etc. Te da una idea de cómo funciona el _LLM_ y te prepara para las sugerencias estúpidas que, a menudo, soltará.

Mucha gente quiere saltarse este paso e ir directa al final. Luego sueltan: «¡Este LLM es una basura y no hace nada bien!». No es del todo cierto (aunque a veces lo parezca). La magia está en los matices. O, como me gusta recordar: _la vida es un lío_.

### Paso 3: Usa Copilot como algo más que autocompletado

Cuando ya tengas un buen flujo con el autocompletado y no estés enfadado _todo_ el tiempo, puedes pasar a la magia de hablar con Copilot.

VS Code tiene un panel de chat donde puedes intercambiar preguntas y respuestas con Copilot y este te ayuda con tu código. Es bastante chulo. Puedes mantener una buena conversación y te responde con criterio, ayudándote a resolver lo que le pidas.

Sin embargo, usar Copilot es como subirse a una máquina del tiempo para hablar con ChatGPT en 2024: no es para tanto.

Querrás más.

### Paso 4: Copia y pega código en Claude o ChatGPT

Empiezas a saciar tu curiosidad pegando código en el modelo fundacional basado en navegador y preguntando: «¿POR QUÉ SE ROMPIÓ EL CÓDIGO?». El _LLM_ responde de forma coherente y útil.

¡Alucinarás! Los resultados te volarán la cabeza. Volverás a crear cosas muy raras y a divertirte con el código, sobre todo porque elimina casi todo el proceso de depuración.

También puedes hacer locuras como pegar un script de Python y decirle al LLM: «Convierte esto a Go»… y simplemente _lo convierte a Go_. Empezarás a pensar: «¿Y si lo puedo hacer de una sola vez?».

Copilot empezará a parecer autocompletado de 2004: útil, pero no imprescindible.

Esto te conducirá por dos subrutas:

#### Empezarás a preferir un modelo por la vibra

Este es el desafortunado primer paso hacia lo que yo llamo _vibe coding_ (programar guiado por la vibra). Simplemente por la vibra que transmite, empezarás a preferir cómo te habla uno de los grandes modelos. Te sorprenderás pensando: «Me gusta cómo me hace sentir Claude».

Muchos desarrolladores prefieren Claude. Yo uso ambos, pero casi siempre Claude para temas de código. La vibra con Claude es sencillamente mejor.

> Tienes que pagar si quieres lo bueno. Muchos amigos dicen: «Esto es una basura» y luego descubres que usan la versión gratuita, que apenas funciona. Lol. Esto era más evidente cuando la opción gratis era ChatGPT 3.5, pero asegúrate de usar un modelo capaz antes de descartar la idea por completo.

#### Empezarás a pensar en cómo acelerar todo

Tras unas semanas copiando y pegando código en Claude, te darás cuenta de que es molesto. Empezarás a trabajar en el empaquetado de contexto e intentar meter más código en la ventana de contexto del LLM.

Probarás herramientas como [RepoMix](https://repomix.com/), [repo2txt](https://github.com/donoceidon/repo2txt) y otras para meter toda tu base de código en la ventana de contexto de Claude. Incluso empezarás a escribir —bueno, Claude los escribirá— scripts de _shell_ que faciliten el proceso.

Este es un punto de inflexión.

### Paso 5: Usa un IDE con IA integrada (Cursor, ¿Windsurf?)

Entonces, un amigo dirá: «¿Por qué no usas [Cursor](https://cursor.sh/)?».

Te dejará alucinado. Toda la magia que acabas de experimentar copiando y pegando ahora vive dentro de tu IDE. Es más rápido, más divertido y roza la magia.

A estas alturas ya pagas como por cinco _LLM_ distintos: ¿qué son 20 $ más al mes?

Funciona de maravilla y te sientes muchísimo más productivo.

Empezarás a jugar con las funciones de programación con agentes que vienen en los editores. Funcionan _más o menos_ bien, pero ves un destino en el horizonte que quizá sea mejor.

### Paso 6: Empiezas a planificar antes de codificar

De pronto te descubres creando especificaciones, _PRD_ y documentos de tareas súper exhaustivos que puedes pasar al agente del IDE o a Claude Web.

Nunca habías _escrito_ tanta documentación. Empiezas a usar otros LLM para redactar documentación aún más robusta. Transpones documentación de un contexto (_PRD_) a otro («Convierte esto en _prompts_»). Empiezas a usar el LLM para diseñar tus propios _prompts_ de generación de código.

Empiezas a pronunciar la palabra «_waterfall_» con mucho menos desdén. Si eres veterano, quizá recuerdes con cariño los 90 y primeros 2000 y te preguntes: «¿Así se sentía Martin Fowler antes de [2001](https://en.wikipedia.org/wiki/Agile_software_development)?».

En el mundo del _codegen_, la _spec_ es la [divinidad](https://en.wikipedia.org/wiki/Godhead).

### Paso 7: Empiezas a jugar con aider para ciclos más rápidos

Ahora sí estás listo para meterte en **LO BUENO**. Hasta aquí, el _codegen_ requería tu atención constante. Pero ¡es 2025! ¿Quién quiere programar con los dedos?

> Otra ruta que muchos amigos exploran es programar con la voz: darle instrucciones a aider mediante un cliente Whisper. Es divertidísimo. Para usarlo en local, MacWhisper va genial. Aqua y SuperWhisper también están bien, pero son más caros y quizá usen la nube para la inferencia. Yo prefiero local.

Probar aider es una experiencia salvaje. Lo inicias, se instancia dentro de tu proyecto y se integra en él. Escribes tu petición directamente en aider y simplemente hace lo que le pides. Pide permiso para actuar, te propone un plan y luego actúa. Completa la tarea y hace _commits_ en tu repositorio. Ya no te obsesionas con hacerlo de un solo tiro: dejas que aider lo haga en unos cuantos pasos.

Empiezas a crear conjuntos de reglas para que el LLM las siga. Aprendes la regla «[Big Daddy](https://www.reddit.com/r/cursor/comments/1joapwk/comment/mkqg8aw/)» o la cláusula «no deceptions» en tus _prompts_. Te vuelves muy bueno dándole instrucciones al robot.

**Funciona.**

Al final ni siquiera abres un IDE: ahora eres un _jinete de la terminal_.

Pasas el tiempo viendo al robot hacer tu trabajo.

### Paso 8: Te entregas por completo a la programación con agentes

Ahora usas un agente que programa por ti. Los resultados son bastante buenos. Hay momentos en los que no tienes ni idea de qué está pasando, pero recuerdas que puedes preguntarle.

Empiezas a experimentar con [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Cline](https://cline.bot/), etc. Te encanta poder usar un modelo de razonamiento ([DeepSeek](https://aws.amazon.com/bedrock/deepseek/)) junto a un modelo de código ([Claude Sonnet 3.7](https://www.anthropic.com/claude/sonnet)) para quitar pasos de planificación.

Haces locuras como ejecutar de tres a cinco sesiones concurrentes. Solo vas cambiando de pestaña en la terminal mientras los robots programan.

Empiezas a programar a la defensiva:

- cobertura de tests muy exhaustiva
- pensar en [verificación formal](https://github.com/formal-land/coq-of-rust)
- usar lenguajes con seguridad de memoria
- elegir lenguajes según la verbosidad del compilador para meter todo en la ventana de contexto

Piensas largo y tendido en cómo lograr que lo que construyes se genere, de forma segura y sin intervención.

Gastas **MUCHO** dinero en _tokens_. También agotas tus horas de GitHub Actions ejecutando todas las pruebas salvajes que necesitas para garantizar que el código se construya con seguridad.

Se siente bien. No te enfada no escribir código.

### Paso 9: Dejas que el agente programe y tú juegas videojuegos

De repente has llegado. Bueno, más o menos, pero ves adónde vamos. Empiezas a preocuparte por los puestos de software. Despiden a tus amigos y no encuentran trabajo. Esta vez se siente distinto.

Cuando hablas con tus colegas, te ven como a un fanático religioso porque trabajas en un contexto distinto al suyo. Les dices: «¡Tienes que probar la programación con agentes!». Quizá añadas: «Odio la palabra _agentic_» solo para demostrar que no te has bebido 200 galones de Kool-Aid. Pero sí lo has hecho. El mundo parece más brillante porque eres muy productivo con tu código.

Da igual. El paradigma ha cambiado. Kuhn podría escribir un libro sobre la confusión de estos tiempos.

Nadie lo ve porque no hizo el viaje para llegar aquí. Pero quienes sí lo hicieron comparten consejos sobre el recorrido y debaten el destino.

Ahora que estás hasta las rodillas dejando que los robots trabajen, por fin puedes centrarte en todos esos juegos de Game Boy que querías jugar. Hay mucho tiempo muerto. Y cuando el robot termina una tarea, pregunta: «¿Sigo?» y tú escribes «sí» antes de volver a tu partida de Tetris.

Muy extraño. Inquietante, incluso.

## La aceleración

<paul confetti photo>
{{< image src="journey-confetti.webp" alt="Confeti" caption="Confeti en un concierto de Paul McCartney en el Tokyo Dome. iPhone 6, 25 abr 2015" >}}

No sé qué pasará en el [futuro](https://ai-2027.com/). Me preocupa que quienes no recorran este camino dejen de resultar atractivos para los [empleadores](https://x.com/tobi/status/1909231499448401946). Es algo miope, porque en último término hablamos de herramientas y automatización.

Cuando antes aumentábamos la contratación, solíamos ampliar la búsqueda más allá de nuestra red y de nuestra pila tecnológica. Éramos una empresa Python y entrevistábamos a personas que no conocían Python ni lo habían usado nunca. Pensábamos que, con un buen ingeniero, podríamos trabajar juntos para que se sintiera cómodo con Python. Aportaría valor aunque no dominara nuestro _stack_. Nos funcionó bien: contratamos a gente impresionante que jamás había usado nuestra pila, y muchas veces aportaron una perspectiva tan distinta que elevó a todo el equipo.

Los mismos principios se aplican al desarrollo asistido por IA. Al contratar desarrolladores con talento que encajen en la cultura del equipo y muestren entusiasmo, su experiencia con herramientas de IA no debería ser decisiva. No todos tienen que ser expertos en IA desde el primer día. Acompáñalos en el proceso mientras trabajan junto a compañeros más experimentados.

Con el tiempo terminarán tomando el volante y usarán estas herramientas con éxito.

Otro aspecto en el que no dejo de pensar: las habilidades de escritura se han vuelto cruciales. Siempre valoramos a buenos comunicadores en los equipos técnicos para la documentación y la colaboración, pero ahora es el doble de importante. No solo debes comunicarte con humanos; también tienes que redactar instrucciones claras y precisas para la IA. Saber crear _prompts_ efectivos se está volviendo tan vital como escribir buen código.

## El liderazgo

Creo que todos los líderes y _engineering managers_ deben sumergirse en el desarrollo asistido por IA, sean creyentes o no. ¿Por qué? Porque la próxima generación de desarrolladores que contratarás habrá aprendido a programar principalmente con herramientas y agentes de IA. A eso se dirige la ingeniería de software. Necesitamos entenderlo y adaptarnos.

Nosotros, los «code boomers», no duraremos mucho en este mundo.

**Nota curiosa:** no suelo usar LLM para ayudarme a escribir. Imagino que serían buenos en ello, pero quiero que se oiga mi voz y no que se normalice. En cambio, mi código _sí_ necesita normalizarse. Interesante.

---

Gracias a Jesse, Sophie, la crew de Vibez (Erik, Kanno, Braydon y demás), al equipo 2389 y a todas las personas que me dieron _feedback_ sobre esta entrada.
