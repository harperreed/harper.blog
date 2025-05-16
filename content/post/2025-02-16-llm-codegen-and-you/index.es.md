---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: Un recorrido detallado de mi flujo de trabajo actual para usar LLMs en
  la construcción de software, desde la lluvia de ideas hasta la planificación y la
  ejecución.
draft: false
generateSocialImage: true
tags:
- LLM
- coding
- ai
- workflow
- software-development
- productivity
title: Mi flujo de trabajo de generación de código con LLM en este momento
translationKey: My LLM codegen workflow atm
---

_tl;dr: Tormenta de ideas para la especificación (*spec*), luego planificar el plan (sí, planificar el plan), después ejecutar con generación de código (*codegen*) mediante los LLM. Bucles discretos. Y luego… magia. ✩₊˚.⋆☾⋆⁺₊✧_

He estado construyendo **muchísimos** productos pequeños con los LLM. Ha sido divertido y útil, pero hay trampas que pueden hacerte perder muchísimo tiempo. Hace un tiempo, un amigo me preguntó cómo estaba usando los LLM para escribir software. Pensé: «¡Madre mía! ¿Cuánto tiempo tienes?» y así nació esta entrada.

(P. D.: si odias la IA, salta al final).

Hablo con muchos amigos desarrolladores sobre esto y todos seguimos un enfoque parecido, con matices aquí y allá.

Aquí va mi *workflow* (flujo de trabajo). Se basa en mi experiencia, en charlas con amigos (gracias [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki) y [Erik](https://thinks.lol/)), y en un puñado de buenas prácticas compartidas en los más infames y terribles rincones de Internet ([uno](https://news.ycombinator.com/) y [otro](https://twitter.com)).

Esto funciona bien **AHORA**; puede que en dos semanas deje de servir… o que funcione el doble de bien. ¯\\\_(ツ)\_/¯

## Vamos allá

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="Siempre desconfío de estas imágenes generadas por IA. ¡Saluda a mi ángel-robot *juggalo* programador!" >}}

Hay muchos caminos para desarrollar, pero mis proyectos suelen caer en uno de estos dos escenarios:

- Código nuevo desde cero (*greenfield*)
- Base de código heredada pero moderna (*non-greenfield*)

Te mostraré mi proceso para ambos.

## Greenfield

El siguiente proceso me funciona de maravilla cuando parto de cero. Aporta una planificación y documentación sólidas y permite avanzar fácilmente en pasos pequeños.

{{< image src="greenfield.jpg" alt="Campo verde" caption="Técnicamente, hay un campo verde a la derecha. Leica Q, 14/5/2016" >}}

### Paso 1: Afinar la idea

Usa un LLM conversacional para pulir la idea (yo utilizo ChatGPT-4o / o3):

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

Al final de la lluvia de ideas (llegará a una conclusión natural):

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

Obtendrás una especificación bastante sólida que podrás pasar al paso de planificación. Suelo guardarla como `spec.md` en el repositorio.

> Esa especificación sirve para muchas cosas. Aquí la usamos para generación de código (*codegen*), pero también la he empleado para pedirle a un modelo de razonamiento que busque puntos débiles (¡hay que ir más profundo!), para generar un *white paper* o un modelo de negocio. Incluso puedes lanzarla a una investigación exhaustiva y recibir a cambio un documento de apoyo de 10 000 palabras.

### Paso 2: Planificación

Pasa la *spec* a un modelo de razonamiento (`o1*`, `o3*`, `r1`):

(Este es el *prompt* con TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(Este es el *prompt* sin TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

El modelo devolverá un plan de *prompts* que podrás ejecutar con Aider, Cursor, etc. Yo lo guardo como `prompt_plan.md` en el repositorio.

Después le pido una lista de comprobación:

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

Guárdalo como `todo.md`. Tu herramienta de generación de código debería ir marcando esta lista para mantener el estado entre sesiones.

#### ¡Plan listo!

Con esto tienes un plan robusto y documentación clara para construir tu proyecto.

Todo el proceso lleva, como mucho, **15 minutos**. Una locura, la verdad.

### Paso 3: Ejecución

Hay muchísimas opciones; el éxito depende de lo bien que salió el Paso 2.

He usado este flujo con [GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude Engineer](https://github.com/Doriandarko/claude-engineer), [Sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [Claude.ai](https://claude.ai)… Funciona bien con todas las que he probado y, seguramente, con cualquier otra herramienta de generación de código (*codegen*).

Aun así, prefiero **Claude puro** y Aider.

### Claude

Básicamente hago *pair programming* con [Claude.ai](https://claude.ai) pegando cada instrucción de forma iterativa. Funciona bastante bien: el ida y vuelta puede ser pesado, pero cumple.

Yo me encargo del código base inicial y de que las herramientas estén configuradas. Esto da cierta libertad y guía al principio. Claude tiende a escupir código React a la mínima; contar con una base sólida en el lenguaje y estilo de tu elección ayuda mucho.

Cuando las cosas se atascan, uso [Repomix](https://github.com/yamadashy/repomix) para iterar.

Flujo de trabajo:

- preparo el repositorio (`uv init`, `cargo init`, etc.);
- pego la instrucción en Claude;
- copio el código al IDE;
- ejecuto el código y la suite de pruebas;
- si funciona, paso a la siguiente instrucción;
- si no, paso la base de código a Claude con Repomix para depurar;
- y a repetir ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) es divertido y algo peculiar. Encaja muy bien con la salida del Paso 2: avanzo muchísimo con muy poco esfuerzo.

El flujo es casi idéntico, pero pegando las instrucciones en Aider.

Aider «simplemente lo hace» y yo me pongo a jugar a [*Cookie Clicker*](https://orteil.dashnet.org/cookieclicker/).

> Aider publica un *benchmark* excelente de modelos nuevos en su [LLM Leaderboard](https://aider.chat/docs/leaderboards/). Es un recurso brutal para ver qué tan efectivos son los modelos.

Las pruebas son aún más automáticas con Aider, porque ejecuta la suite y depura por ti.

Flujo de trabajo:

- preparo el repositorio (`uv init`, `cargo init`, etc.);
- inicio Aider (procura estar siempre en una rama nueva);
- pego la instrucción;
- veo a Aider bailar ♪┏(・o･)┛♪;
- Aider ejecuta pruebas o corro la app para verificar;
- si funciona, siguiente instrucción;
- si no, sesión de preguntas y respuestas con Aider hasta arreglarlo;
- y a repetir ✩₊˚.⋆☾⋆⁺₊✧

### Resultados

He construido scripts, apps de Expo, herramientas CLI en Rust, etc., usando este método. Funciona en distintos lenguajes y contextos. La verdad, me encanta.

Si tienes un proyecto —grande o pequeño— aparcado, prueba esto: te sorprenderá lo lejos que avanzas en poco tiempo.

Mi lista de *hacks* pendientes está vacía porque ya construí todo. Pienso ideas nuevas y las tacho mientras veo una peli. Por primera vez en años estoy jugando con lenguajes y herramientas nuevas, y eso amplía mi perspectiva como programador.

## No-greenfield: iteración incremental (sobre código existente)

A veces no partes de cero y toca mejorar o añadir funcionalidades a una base de código existente.

{{< image src="brownfield.jpg" alt="a brown field" caption="Esto NO es un *greenfield*. Foto aleatoria de la cámara de mi abuelo — Uganda, años 60." >}}

Para esto uso un método parecido, pero menos de “planificación global”: planifico por tarea, no por proyecto.

### Obtener contexto

Quienes estamos hasta las rodillas en desarrollo con IA solemos tener cada uno nuestra herramienta favorita para empaquetar el código y pasarlo eficazmente a los LLM.

Yo utilizo [Repomix](https://github.com/yamadashy/repomix) y un conjunto de tareas en `~/.config/mise/config.toml` (ver [reglas de mise](https://mise.jdx.dev/)):

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

Genero un `output.txt` con el contexto de la base de código. Si se pasa de tokens, ajusto el comando para ignorar partes irrelevantes.

> Algo estupendo de `mise` es que las tareas pueden redefinirse en el `.mise.toml` del proyecto. Puedo usar otra herramienta para empaquetar el código y, mientras genere un `output.txt`, mis tareas LLM siguen funcionando. Suelo sobreescribir el paso de Repomix para incluir patrones de *ignore* más amplios o usar una herramienta más eficaz según el caso.

Luego paso `output.txt` al comando [LLM](https://github.com/simonw/LLM) y guardo la salida como Markdown.

En el fondo, la tarea ejecuta algo como:

```bash
cat output.txt | LLM -t readme-gen > README.md
# o
cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md
```

Por ejemplo, para mejorar la cobertura de pruebas:

#### Claude

- voy al directorio del código;
- `mise run LLM:generate_missing_tests`;
- reviso `missing-tests.md`;
- copio el contexto con `mise run LLM:copy_buffer_bundle`;
- pego eso en Claude junto con el primer “issue” de pruebas faltantes;
- copio el código generado al IDE;
- ejecuto pruebas;
- y a repetir ✩₊˚.⋆☾⋆⁺₊✧  

#### Aider

- voy al directorio del código;
- abro Aider (siempre en una rama nueva);
- `mise run LLM:generate_missing_tests`;
- reviso `missing-tests.md`;
- pego el primer “issue” en Aider;
- veo a Aider bailar ♪┏(・o･)┛♪;
- ejecuto pruebas;
- y a repetir ✩₊˚.⋆☾⋆⁺₊✧  

Esta metodología es muy útil para mejorar gradualmente cualquier base de código, sin importar el tamaño de la tarea.

### Magia de *prompts*

Estos pequeños *hacks* van de maravilla para hurgar en el proyecto y hacerlo más robusto.

#### Revisión de código

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply  before writing the code review. Review every part, and don't hallucinate.
```

#### Generación de issues de GitHub

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Tests faltantes

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues  will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

Estos *prompts de boomer* necesitan un repaso. Si tienes ideas para mejorarlos, avísame.

## Esquí ᨒ↟ 𖠰ᨒ↟ 𖠰

Cuando explico este proceso digo: «Hay que llevar el control de forma agresiva porque es muy fácil adelantarte a ti mismo.»

Por alguna razón digo mucho *over my skis* (pasado de vueltas) cuando hablo de los LLM. Quizá porque es como esquiar en polvo perfecto y, de pronto, «¡¿QUÉ CARAJO ESTÁ PASANDO?!», te pierdes y caes por un precipicio.

Usar un **paso de planificación** (como en el proceso *greenfield*) ayuda: al menos tienes un documento para comprobar. También creo que las pruebas son clave —sobre todo si codificas “a lo loco” con Aider—: mantienen todo ajustado.

Aun así, a menudo sigo sintiéndome *over my skis*. Un descanso rápido o un paseo corto suele ayudar. Al fin y al cabo es el proceso normal de resolver problemas, solo que a velocidad de vértigo.

> A veces pedimos a los LLM que incluyan cosas ridículas en nuestro código no tan ridículo. Por ejemplo, le pedimos que creara un archivo de *lore* y luego lo referenciara en la interfaz de usuario de una herramienta CLI de Python. De repente tienes *lore*, interfaces glitchy… Todo ello, paradójicamente, solo para gestionar tus funciones en la nube, tu lista de tareas o lo que sea. El cielo es el límite.

## Estoy tan solo (｡•́︿•̀｡)

Mi mayor queja es que estos flujos son, básicamente, _single-player_. He pasado años programando solo, en pareja y en equipo. Siempre es mejor con gente. Estos flujos no son fáciles de usar en grupo: los bots chocan, las fusiones son horribles, el contexto se complica.

Quiero que alguien convierta la programación con LLM en un juego multijugador. ¡Hay una oportunidad enorme! **GET TO WORK!**

## ⴵ Tiempo ⴵ

Toda esta generación de código ha disparado la cantidad de trabajo que puedo producir. Pero hay un efecto raro: mucho tiempo muerto mientras el LLM quema tokens.

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="Lo recuerdo como si fuera ayer" >}}

Para aprovechar la espera:

- inicio la lluvia de ideas de otro proyecto;
- pongo vinilos;
- juego a *Cookie Clicker*;
- charlo con amigos… y con robots.

Hack, hack, hack. No recuerdo otra época en la que fuera tan productivo.

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

Muchos colegas dicen: «Los LLM apestan; fallan en todo». No comparto esa opinión, pero el escepticismo es sano. Hay razones de sobra para odiar la IA. Mi miedo principal es el consumo energético y el impacto ambiental. Pero… el código debe fluir. *Suspiro.* ¯\\\_(ツ)\_/¯

Si quieres saber más sin convertirte en cíborg programador, te recomiendo el libro de Ethan Mollick: [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/). Explica los beneficios sin rollo *tech-bro* y me ha permitido charlas muy matizadas con amigos. Muy recomendado.

Si eres escéptico pero curioso, escríbeme: te enseño cómo usamos los LLM y quizá construyamos algo juntos.

_Gracias a [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com) y [Erik](https://thinks.lol/) por revisar esta entrada y sugerir cambios. ¡Lo aprecio!_