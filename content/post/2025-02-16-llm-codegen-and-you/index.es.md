---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description:
    Un recorrido detallado por mi flujo de trabajo actual para usar LLMs
    para crear software, desde la lluvia de ideas hasta la planificación y la ejecución.
draft: false
generateSocialImage: true
slug: my-llm-codegen-workflow-atm
tags:
    - LLM
    - coding
    - ai
    - workflow
    - software-development
    - productivity
title: "Mi flujo de trabajo de generación de código con LLM en este momento"
translationKey: My LLM codegen workflow atm
---

_tl;dr: Primero genera una **especificación (spec)** con una lluvia de ideas; luego **planea un plan** y, por último, ejecuta con generación de código mediante LLMs. **Bucles discretos**. Después, magia. ✩₊˚.⋆☾⋆⁺₊✧_

He estado creando un montón de pequeños productos con LLMs. Ha sido divertido y útil. Sin embargo, hay obstáculos que pueden hacerte perder muchísimo tiempo. Hace un tiempo un amigo me preguntó cómo estaba usando los LLMs para escribir software. Pensé: «¡Madre mía! ¿Cuánto tiempo tienes?» y así nació este post.

(P. D.: si odias la IA, ve hasta el final).

Hablo con muchos amigos _dev_ sobre esto y todos tenemos un enfoque parecido, con matices en una u otra dirección.

Este es mi flujo de trabajo. Se basa en mi propio trabajo, en conversaciones con amigos (gracias [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki) y [Erik](https://thinks.lol/)) y en muchas buenas prácticas compartidas en esos infames rincones de Internet, por ejemplo HN o Twitter.

Esto funciona muy bien **AHORA**; quizá dentro de dos semanas no funcione… o funcione el doble de bien. ¯\\\_(ツ)\_/¯

## Vamos allá

{{< image src="llm-coding-robot.webp" alt="Robot juggalo" caption="Siempre desconfío un poco de estas imágenes generadas por IA. ¡Saluda a mi ángel robot juggalo programador!" >}}

Hay muchos caminos para desarrollar, pero en mi caso suelo enfrentarme a uno de dos escenarios:

- Código _greenfield_ (proyecto empezado desde cero)
- Código heredado _moderno_

Te mostraré mi proceso para ambos casos.

## _Greenfield_

El siguiente proceso me funciona bien para proyectos _greenfield_. Proporciona una planificación y documentación sólidas y permite avanzar fácilmente en pequeños pasos.

{{< image src="greenfield.jpg" alt="Campo verde" caption="Técnicamente, hay un campo verde a la derecha. Leica Q, 14/05/2016" >}}

### Paso 1: Afinar la idea

Utiliza un LLM conversacional para concretar la idea (yo uso ChatGPT 4o / o3):

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

Al final de la sesión de _brainstorming_ (llegará a una conclusión natural):

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

Esto genera una _spec_ bastante sólida y directa que puedes pasar a la fase de planificación. Me gusta guardarla como `spec.md` en el repositorio.

> Puedes emplear esta especificación para varias cosas. Aquí la usaremos para _codegen_, pero también la he usado para reforzar ideas pidiéndole a un modelo de razonamiento que les busque puntos débiles (¡profundiza más!), para generar un _white paper_ o un modelo de negocio. Incluso puedes enviarla a un modelo de investigación profunda y obtener a cambio un documento de 10 000 palabras de soporte.

### Paso 2: Planificación

Toma la _spec_ y pásala a un modelo de razonamiento (`o1*`, `o3*`, `r1`):

(Éste es el _prompt_ TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break them into smaller steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(Éste es el _prompt_ sin TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break them into smaller steps. Review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

Debería generar un **plan de _prompts_** (`prompt_plan.md`) que puedas ejecutar con Aider, Cursor, etc.

Luego pido un `todo.md` para usarlo como lista de verificación:

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

Guárdalo como `todo.md` en el repositorio.

Tu herramienta de generación de código debería poder ir marcando el `todo.md` mientras avanza. Así se mantiene el estado entre sesiones.

#### ¡Yay, plan!

Ahora tienes un plan robusto y documentación que te ayudarán a ejecutar y construir tu proyecto.

Todo este proceso lleva quizá **15 minutos**. Bastante rápido, la verdad. ¡Una locura, sinceramente!

### Paso 3: Ejecución

Las opciones para ejecutar son muchísimas. El éxito depende en gran medida de lo bien que haya salido el paso 2.

He usado este proceso con [GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude Engineer](https://github.com/Doriandarko/claude-engineer), [sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [Claude.ai](https://claude.ai), etc. En todos los casos ha funcionado bastante bien, y supongo que irá igual con cualquier herramienta de generación de código.

Yo, sin embargo, prefiero **Claude en bruto** y Aider:

### Claude

Básicamente programo en pareja con [Claude.ai](https://claude.ai) y voy pegando cada _prompt_ de forma iterativa. Funciona bastante bien; el ida y vuelta puede ser un poco tedioso, pero se lleva.

Me ocupo del _boilerplate_ inicial y de que las herramientas estén configuradas. Eso da libertad y guía al principio. Claude tiende a escupir código React, y contar con una base sólida en el lenguaje, estilo y _tooling_ de tu elección ayuda mucho.

Cuando algo se atasca, uso [repomix](https://github.com/yamadashy/repomix) para iterar (hablo de ello más adelante).

El proceso es así:

- crear el repo (boilerplate, `uv init`, `cargo init`, etc);
- pegar el _prompt_ en Claude;
- copiar el código de Claude.ai al IDE;
- ejecutar el código y las pruebas;
- …;
- si funciona, pasar al siguiente _prompt_;
- si no funciona, usar repomix para pasar la base de código a Claude y depurar;
- repetir el ciclo ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) es divertido y un poco peculiar. Encaja bien con la salida del paso 2: puedo avanzar muchísimo con muy poco esfuerzo.

El flujo es esencialmente el mismo, pero en vez de pegar en Claude, pego las instrucciones en Aider.

Aider entonces «simplemente lo hace» y yo juego a _Cookie Clicker_.

> Nota: Aider hace una excelente evaluación comparativa de los nuevos modelos de generación de código en su [LLM leaderboard](https://aider.chat/docs/leaderboards/). Es un recurso buenísimo para ver la eficacia de los modelos.

Probar es cómodo con Aider: puede ser aún más automático; Aider ejecuta la _suite_ de tests y depura por ti.

El proceso es así:

- crear el repo (boilerplate, `uv init`, `cargo init`, etc);
- iniciar Aider;
- pegar la instrucción en Aider;
- ver a Aider hacer su magia ♪┏(・o･)┛♪;
- Aider ejecuta las pruebas o puedes lanzar la app para verificar;
- si funciona, siguiente instrucción;
- si no, preguntas y respuestas con Aider para arreglar;
- repetir el ciclo ✩₊˚.⋆☾⋆⁺₊✧

### Resultados

He construido un montón de cosas con este proceso: scripts, apps en Expo, herramientas CLI en Rust, etc. Ha funcionado con distintos lenguajes y contextos. Me encanta.

Si tienes un proyecto —grande o pequeño— que estás posponiendo, te recomiendo probar este método. Te sorprenderá lo lejos que puedes llegar en poco tiempo.

Mi lista de hacks pendientes está vacía porque ya lo hice todo. Cada vez que se me ocurre algo nuevo lo construyo mientras veo una peli o lo que sea. Por primera vez en años estoy dedicando tiempo a nuevos lenguajes y herramientas, lo que amplía mi perspectiva como programador.

## _Brownfield_: iteración incremental

A veces no tienes un proyecto _greenfield_ y necesitas iterar o hacer trabajo incremental sobre una base de código ya existente.

{{< image src="brownfield.jpg" alt="Un campo marrón" caption="Esto no es un campo verde. Foto aleatoria de la cámara de mi abuelo, en algún lugar de Uganda en los 60" >}}

Para esto uso un método ligeramente distinto. Es parecido al anterior, pero algo menos “basado en planificación”: la planificación se hace por tarea, no para todo el proyecto.

### Obtener contexto

Cada persona metida en desarrollo con IA tiene su herramienta para esto, pero necesitas algo que capture tu código fuente y lo empaquete eficientemente para el LLM.

Actualmente uso [repomix](https://github.com/yamadashy/repomix). Tengo una colección de tareas definida en mi `~/.config/mise/config.toml` global que me permite hacer varias cosas con la base de código ([reglas de mise](https://mise.jdx.dev/)).

Lista de tareas LLM:

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

Genero un `output.txt` con el contexto del código. Si me paso de tokens y es demasiado grande, modifico el comando para ignorar las partes que no sean relevantes para la tarea.

> Algo muy útil de `mise` es que las tareas pueden redefinirse y sobrecargarse en el `.mise.toml` del directorio de trabajo. Puedo usar otra herramienta para empaquetar el código y, mientras genere un `output.txt`, mis tareas LLM seguirán funcionando. Esto ayuda cuando las bases de código son muy distintas. A menudo sobrescribo el paso de `repomix` para ampliar patrones de _ignore_ o uso otra herramienta más eficaz.

Una vez generado `output.txt`, lo paso al comando [LLM](https://github.com/simonw/LLM) para hacer varias transformaciones y guardarlas como archivo Markdown.

En esencia, la tarea de mise ejecuta algo como: `cat output.txt | LLM -t readme-gen > README.md` o `cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md`. No tiene mayor complicación; el comando `LLM` hace el trabajo pesado.

Por ejemplo, si necesito una revisión rápida y mejorar la cobertura de tests, haría lo siguiente:

#### Claude

- ir al directorio del código;
- ejecutar `mise run LLM:generate_missing_tests`;
- revisar el Markdown generado (`missing-tests.md`);
- copiar el contexto completo con `mise run LLM:copy_buffer_bundle`;
- pegar eso en Claude junto con el primer _issue_ de tests faltantes;
- copiar el código generado por Claude al IDE;
- …;
- ejecutar las pruebas;
- repetir el ciclo ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- ir al directorio del código;
- iniciar Aider (siempre en una rama nueva);
- ejecutar `mise run LLM:generate_missing_tests`;
- revisar el Markdown (`missing-tests.md`);
- pegar el primer _issue_ de tests faltantes en Aider;
- ver a Aider hacer su magia ♪┏(・o･)┛♪;
- …;
- ejecutar las pruebas;
- repetir el ciclo ✩₊˚.⋆☾⋆⁺₊✧

Es una forma bastante buena de mejorar una base de código de manera incremental. Me ha resultado útil para tareas de cualquier tamaño.

### Magia de _prompts_

Estos hacks rápidos funcionan muy bien para profundizar en los puntos donde un proyecto puede hacerse más robusto. Son rápidos y efectivos.

Algunos de mis _prompts_ para bases de código establecidas (se dejan en inglés porque así se usan con el modelo):

#### Revisión de código

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply before writing the code review. Review every part, and don't hallucinate.
```

#### Generación de _issues_ de GitHub

(¡Tengo que automatizar la publicación real de los _issues_!)

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to execute on, so they should be in a format that is compatible with GitHub issues
```

#### Tests faltantes

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to execute on, so they should be in a format that is compatible with GitHub issues
```

Estos _prompts_ están algo _old and busted_ («_prompts_ boomer», si se quiere). Necesitan refactorización. Si tienes ideas para mejorarlos, avísame.

## Esquí ᨒ↟ 𖠰ᨒ↟ 𖠰

Cuando describo este proceso suelo decir: «tienes que llevar un control agresivo de lo que está pasando porque puedes adelantarte fácilmente».

Por alguna razón, cuando hablo de LLMs digo mucho _over my skis_ (ir demasiado rápido). No sé por qué, pero me resuena: es como deslizarte por nieve polvo perfecta y, de repente, pensar «¡¿QUÉ DEMONIOS PASA?!», perderte y caer por un precipicio.

Creo que usar un **paso de planificación** (como en el proceso _greenfield_) ayuda a mantener las cosas bajo control: al menos tendrás un documento para comprobar. También creo que las pruebas son útiles, sobre todo si vas a lo loco con Aider; ayudan a mantener todo ordenado y ajustado.

Aun así, sigo encontrándome **over my skis** con frecuencia. A veces un descanso corto o una caminata ayudan. En ese sentido es un proceso de resolución de problemas normal, pero acelerado a velocidad de vértigo.

> A menudo pedimos al LLM que incluya cosas ridículas en nuestro código no tan ridículo. Por ejemplo, le pedimos que creara un archivo de _lore_ y luego lo referenciara en la interfaz de usuario (para herramientas CLI en Python). De pronto aparece _lore_, interfaces glitchy, etc. Todo para gestionar funciones en la nube, tu lista de tareas o lo que sea. El cielo es el límite.

## Estoy tan solooo (｡•́︿•̀｡)

Mi principal queja sobre estos procesos es que, en gran medida, son de **modo de un solo jugador**.

He pasado años programando solo, años programando en pareja y años en equipo. Siempre es mejor con gente. Estos flujos no son fáciles de usar en equipo: los bots chocan, las fusiones son horribles y el contexto se complica.

Quiero que alguien resuelva esto y convierta la programación con un LLM en un juego multijugador, no en la experiencia del hacker solitario. Hay muchísimo por mejorar.

¡A TRABAJAR!

## ⴵ Tiempo ⴵ

Todo este _codegen_ ha acelerado la cantidad de código que puedo generar yo solo. Sin embargo, hay un efecto curioso: tengo mucho “tiempo muerto” esperando a que el LLM termine de quemar tokens.

{{< image src="apple-print-shop-printing.png" alt="Imprimiendo" caption="Lo recuerdo como si fuera ayer" >}}

He cambiado mi forma de trabajar e incorporado algunas prácticas para aprovechar ese tiempo de espera:

- comienzo el _brainstorming_ de otro proyecto;
- escucho discos;
- juego a _Cookie Clicker_;
- converso con amigos y robots.

Es genial poder hackear así. Hack, hack, hack. No recuerdo otra época en la que fuera tan productivo programando.

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

Muchos amigos me dicen: «Los LLMs apestan, son malos en todo». No me molesta ese punto de vista. Yo no lo comparto, pero creo que es importante ser escéptico. Hay un montón de razones para odiar la IA. Mi mayor temor es el consumo energético y el impacto medioambiental. Pero… el código debe fluir. ¿Verdad? _Suspiro_.

Si quieres saber más, pero no te apetece convertirte en un «programador cíborg», mi recomendación no es que cambies de opinión, sino que leas el libro de Ethan Mollick sobre LLMs y su uso: [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/).

Explica muy bien los beneficios sin ser un panfleto tecno-anarcocapitalista. Me resultó útil y he tenido conversaciones buenas y matizadas con amigos que lo leyeron. Muy recomendado.

Si eres escéptico pero tienes algo de curiosidad, escríbeme y hablamos de esta locura. Puedo mostrarte cómo usamos LLMs y quizá construir algo juntos.

_Gracias a [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com) y [Erik](https://thinks.lol/) por revisar este post y sugerir cambios. ¡Lo aprecio!_
