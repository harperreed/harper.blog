---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description:
    Un recorrido detallado sobre el uso del asistente de IA Claude Code para
    el desarrollo de software, que incluye consejos de flujo de trabajo, prácticas de
    pruebas y ejemplos prácticos de proyectos reales. Cubre estrategias de codificación
    defensiva, TDD e implementación en equipo.
draft: false
generateSocialImage: true
tags:
    - ai
    - coding
    - claude
    - development
    - automation
    - testing
    - tdd
    - programming
title: Código Básico de Claude
slug: basic-claude-code
translationKey: Basic Claude Code
---

Me encanta esto del _agentic coding_ (programación agéntica). Es muy atractivo en muchos sentidos.

Desde que escribí [aquella entrada original del blog](/2025/02/16/my-llm-codegen-workflow-atm/) han pasado un montón de cosas en el mundo de Claude:

- Claude Code
- MCP
- etc

He recibido cientos (wat) de correos de gente contándome sus flujos de trabajo y cómo han usado el mío para sacar provecho. He impartido charlas en varias conferencias y dado algunas clases sobre _codegen_. También he descubierto que los ordenadores se empeñan en corregir “codegen” a “codeine”. ¡Quién lo diría!

{{< image src="codegen.png"  >}}

El otro día hablaba con una [amiga](https://www.elidedbranches.com/) sobre cómo **estamos totalmente jodidos** y **la IA nos va a quitar el curro** (ya hablaré de eso en otra entrada). Ella me dijo: «Deberías escribir un post sobre Claude Code».

Aquí vamos.

Claude Code salió ocho días después de que publicara mi entrada original sobre el flujo de trabajo y, como predije, dejó gran parte de ella obsoleta. Desde entonces migré de Aider a Claude Code y no he vuelto a mirar atrás. Sigo apreciando Aider —tiene su momento— pero Claude Code me resulta bastante más útil ahora mismo.

Claude Code es potentísimo y carísimo.

Mi flujo de trabajo sigue siendo casi el mismo de antes:

- Charlo con `gpt-4o` para afinar la idea.
- Uso el mejor modelo de razonamiento que encuentre para generar la _spec_. Hoy es `o1-pro` o `o3` (¿es `o1-pro` mejor que `o3` o solo me lo parece porque tarda más?).
- Con ese modelo genero los _prompts_. Usar un LLM para crear _prompts_ es un truco precioso. También hace que los boomers se enfaden.
- Guardo `spec.md` y `prompt_plan.md` en la raíz del proyecto.
- Después le paso a claude lo siguiente:

```prompt
1. Open **@prompt_plan.md** and identify any prompts not marked as completed.
2. For each incomplete prompt:
    - Double-check if it's truly unfinished (if uncertain, ask for clarification).
    - If you confirm it's already done, skip it.
    - Otherwise, implement it as described.
    - Make sure the tests pass, and the program builds/runs
    - Commit the changes to your repository with a clear commit message.
    - Update **@prompt_plan.md** to mark this prompt as completed.
3. After you finish each prompt, pause and wait for user review or feedback.
4. Repeat with the next unfinished prompt as directed by the user.
```

La magia de este _prompt_ es que revisa el `prompt_plan.md`, busca lo que aún no está marcado como completado y aborda la siguiente tarea pendiente. Hace _commit_ con `git`, actualiza el plan con lo que ya está listo y, al terminar, se planta para pedirte que continúes. 🤌

Entonces me relajo y me limito a escribir `yes` mientras claude trabaja. Pide _feedback_ y la magia sucede.  
Y muchos más clics de Cookie Clicker.

Esto funciona de lujo. Hay un par de superpoderes que puedes incorporar a tu proceso y que ayudan muchísimo.

## Programación defensiva

### Pruebas

Las pruebas y el desarrollo guiado por pruebas (_TDD_) son imprescindibles. Te recomiendo comprometerte de verdad con una práctica sólida de TDD.

Yo odiaba el TDD. Se me daba fatal y sentía que estaba perdiendo el tiempo. Estaba equivocado, lol. Lo reconozco: durante las últimas décadas metimos un montón de pruebas en nuestras empresas y proyectos. La mayoría se añadieron DESPUÉS de terminar el núcleo. Esto está bien para humanos.

ESTO ES MALO PARA LOS ROBOTS.

A los robots les encanta el TDD. En serio, lo devoran.

Con TDD tu colega robot escribe la prueba y el _mock_; en el siguiente _prompt_ conviertes el _mock_ en código real. Y al robot le chifla. Es el antídoto más efectivo que he encontrado contra las alucinaciones y la deriva de alcance de los LLM. Les ayuda muchísimo a mantenerse enfocados.

### Linting

Soy fan del _linting_. Es una gozada. Ruff es maravilloso, Biome está genial y Clippy es divertido (y el nombre es top).

Por alguna razón los robots disfrutan ejecutando un buen _linter_.

Tenerlo configurado para que se ejecute todo el rato mantiene muchos _bugs_ a raya y deja el código más mantenible y legible. Ya lo sabes.

Añade un _formatter_ decente y todo queda precioso.

### Hooks de pre-commit

La auténtica magia está en meter todas estas tareas en un _hook_ de pre-commit. Recomiendo el paquete de Python `pre-commit`. Puedes instalarlo con `uv tools install pre-commit`, crear un archivo `.pre-commit-config.yaml` chulo y ¡bam! Cada vez que intentes hacer _commit_ correrá pruebas, comprobación de tipos, _linting_, etc., para asegurarse de que tu código sea A+++ y volvería a aprobar cada vez.

Esto es un truco buenísimo para trabajar con Claude Code. El robot QUIERE hacer _commit_ sí o sí. Así que cuando le pides que escriba código y luego haga _commit_ (como arriba), hará cambios salvajes, hará _commit_, inevitablemente lo fastidiará todo y luego tendrá que arreglarlo.

Y es fantástico porque no atasca tus GitHub Actions con montones de _linting_, formato y comprobaciones de tipos que fallan porque el robot estaba de malas.

> Algo curioso de claude es que NO PUEDE, ni a tiros, aprender a usar `uv` correctamente. Si te descuidas hará `pip install` a lo loco. Y si le ordenas usar `uv`, se limitará a hacer `uv pip install`. Igual la AGI no llega en junio… qué pena.

### CLAUDE.md y comandos

Son dos añadidos muy simples que permiten sacar muchísimo más partido.

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse en el estudio, Sigma fp, 15 de noviembre de 2023" >}}

Le tomé prestado un [CLAUDE.md](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md) a mi colega [Jesse Vincent](https://fsck.com/), que se pegó [un currazo brutal para dejarlo ultra robusto](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md). Está de lujo. Incluye, por ejemplo:

- una versión ligera de la _big daddy rule_
- instrucciones sobre cómo hacer TDD
- pautas de estilo sobre mi forma de programar

> [@clint](https://instagram.com/clintecker) configuró su CLAUDE.md para que lo llame MR BEEF y ahora toda nuestra documentación suelta perlas de MR BEEF: «If you're stuck, stop and ask for help—MR BEEF may know best.» Mientras escribía esto, decidí que mi CLAUDE.md me llame “Harp Dog”. Es una _feature_, no un _bug_.

Los comandos también son muy prácticos. Puedes ver algunos de los míos en mis dotfiles [aquí](https://github.com/harperreed/dotfiles/tree/master/.claude/commands).

{{< image src="commands.png"  >}}

Antes los usaba mucho más, pero siguen siendo una forma estupenda de sacar partido a _prompts_ recurrentes. Además, puedes pasar argumentos. Por ejemplo, en mi comando para _issues_ de GitHub le pasas el número de _issue_ que quieres que claude mire: `/user:gh-issue #45`

claude ejecutará entonces el _prompt_ definido en el archivo `gh-issue.md`.

También puedes colocar estos comandos en el directorio del proyecto y crear un `CLAUDE.md` personalizado ahí. Yo lo hago para tener comandos específicos de Hugo, Rust, Go o JavaScript según el proyecto.

## "Continue"

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

A veces me siento como ese pájaro con la cabeza oscilante que Homer puso a pulsar la tecla “y”: solo escribo “continue” o pulso la flecha arriba y pego el mismo _prompt_.

La mayoría de los planes tienen entre 8 y 12 pasos. Suelo terminar un desarrollo _greenfield_ (desde cero) en 30–45 min sin importar la complejidad aparente o el lenguaje.

Se lo contaba a mi amigo Bob y no me creía. Le dije: «Nómbrame algo que construir y un lenguaje: ¡veamos!»

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 17 de noviembre de 2024" >}}

Él soltó: «Vale. Un intérprete de BASIC en C».

No era lo ideal. No sé C, tampoco sé realmente escribir un intérprete y, francamente, me da igual. Pero qué rayos.

Seguí los pasos de arriba y Claude Code lo bordó. Tenemos [un intérprete de BASIC que funciona](https://github.com/harperreed/basic). La primera versión estuvo lista en una hora. Luego la pulí un par más y quedó bastante decente. ¿La habría lanzado en 1982? Probablemente no. Puedes ver el [prompt_plan.md aquí](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md).

## El equipo

Todo nuestro equipo usa ahora Claude Code. Seguimos más o menos el proceso anterior, con bastantes retoques personales.

Estamos logrando una cobertura de pruebas muchísimo mayor que nunca. Tenemos mejor código y parece ser tan eficaz como el código horrible que escribíamos antes. Es divertido pasear la vista y ver Claude Code corriendo en Ghostty, en la terminal de VS Code, en la terminal de Zed y trasteando con _notebooks_ de Python.

{{< image src="dril.jpg" >}}

Alguien con un montón de tokens, por favor, ayúdame a presupuestar esto. Mi familia se muere.

## Gracias

A todas las personas que siguen enviándome correos: es divertidísimo y un placer conocer vuestros flujos de trabajo y proyectos. Lo agradezco un montón. ¡Seguid enviándolos!
