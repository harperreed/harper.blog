---
date: 2025-04-10
description:
    Una exploración de cómo la IA está acelerando los métodos de desarrollo
    tradicionales hacia ciclos de cascada rápidos de 15 minutos, transformando los flujos
    de trabajo de ingeniería de software y la dinámica de los equipos.
draft: false
generateSocialImage: true
generated: true
slug: waterfall-in-15-minutes-or-your-money-back
tags:
    - llm
    - large-language-models
    - code-generation
    - ai
    - artificial-intelligence
    - coding
    - programming
    - workflow
    - software-development
    - development-practices
    - productivity
    - automation
title: "Cascada en 15 minutos o le devolvemos su dinero"
translationKey: Waterfall in 15 Minutes or Your Money Back
---

Hace poco tuve una conversación con un amigo que empezó como una simple puesta al día y acabó en una profunda exploración sobre la programación asistida por IA y lo que está haciendo a nuestros flujos de trabajo, a nuestros equipos y a nuestro sentido del «oficio». Hablamos de todo: desde la reescritura de codebases antiguas hasta cómo la cobertura de pruebas automatizadas cambia la naturaleza misma de la programación.

Tomé la transcripción de granola, la metí en o1-pro y le pedí que convirtiera todo en esta entrada de blog. Quedó bastante bien. Representa lo que pienso.

Se la envié a algunos amigos, y todos querían reenviarla a más gente. Eso significa que tengo que publicarla. ¡Allá vamos!

> esto es un buen recordatorio de que, si recibes un correo y la redacción es perfecta y sin afectación, probablemente lo haya escrito una IA. LOL.

---

## _Waterfall_ en 15 minutos o te devolvemos el dinero

### La nueva normalidad: «¿Por qué debería importar la calidad del código?»

Durante años hemos hablado del código como artesanía: cómo entramos en ese preciado estado de flujo (_flow_), esculpimos un fragmento de lógica y salimos victoriosos, con correcciones artesanales de errores en la mano. Pero se está colando un nuevo paradigma en el que las herramientas de generación de código —piensa en los grandes modelos de lenguaje (LLM)— pueden despachar funcionalidades en cuestión de minutos.

A algunos les desconcierta esta velocidad y cómo trastoca los antiguos estándares de «código limpio». De repente, escribir baterías de pruebas robustas —o incluso practicar desarrollo guiado por pruebas— consiste más en dejar que los bots se verifiquen a sí mismos que en recorrer metódicamente cada línea de código.

¿Se desplomará la calidad del código? Posiblemente. Por otro lado, también vemos un impulso hacia la programación hiperdefensiva: análisis estático, verificación formal y cobertura de pruebas por todas partes, de modo que, si un agente basado en IA rompe algo, lo detectemos de inmediato. Nunca habíamos necesitado tanto los _pipelines_ de CI/CD y las revisiones rigurosas como ahora.

---

### _Waterfall_ en 15 minutos

{{< image src="waterfall.webp" alt="Cascada" caption="En Islandia abundan las cascadas. Leica Q, 30/9/2016" >}}

Antes hablábamos de _Waterfall_ frente a _Agile_ como si fueran polos morales opuestos y _Agile_ fuera el único camino correcto. Pero, paradójicamente, la generación de código nos empuja hacia microciclos de _Waterfall_: definimos con cuidado una especificación (porque la IA necesita claridad), pulsamos «Go» (el botón de ejecutar), esperamos a que se genere el código y lo revisamos. Puede que siga pareciendo iterativo, pero en la práctica hacemos un bloque de planificación, luego uno de ejecución y después uno de revisión. «_Waterfall_ en 15 minutos».

¿La verdadera magia? Puedes poner en marcha varios «agentes» simultáneamente. Mientras una IA construye una funcionalidad, otra se ocupa de tu documentación y una tercera mastica tu cobertura de pruebas. No es exactamente la vieja idea de un _Waterfall_ lineal único: esto es concurrencia desbocada, una auténtica «concurrencia con esteroides».

---

### El próximo giro en la cultura del equipo

Si diriges un equipo de ingeniería, probablemente oigas desde arriba: «¿Y la IA para hacernos más productivos?». Pero quizá también notes que tu equipo tiene distintos niveles de entusiasmo por estas herramientas. Algunos están a tope —crean funcionalidades enteras solo con _prompts_— mientras que otros protegen su identidad de artesanos.

Creo que esto funciona:

1. **Realiza pilotos pequeños**

    Elige un proyecto interno, o quizá una herramienta auxiliar que no suponga un gran riesgo en producción, y deja que un par de ingenieros curiosos se suelten con la IA: que rompan cosas, experimenten y comprueben qué pasa cuando confían demasiado en el modelo y luego incorporen buenas prácticas para reconducirlo todo.

2. **Haz que la gente rote**

    Tener un proyecto paralelo «codificado con IA» permite que los miembros del equipo roten: que pasen una o dos semanas en este nuevo entorno, aprendan unos de otros y luego traigan esas lecciones al código principal.

3. **Ponte serio con la documentación**

    Los «agentes» de IA exigen especificaciones clarísimas. Generar código es barato, pero guiar a un LLM en la dirección correcta cuesta planificación cuidadosa. Si quieres que todo tu equipo se beneficie, coloca las mejores especificaciones y documentos de arquitectura que hayas escrito en un repositorio compartido. Te lo agradecerás cuando la gente rote dentro o fuera de ese proyecto.

---

### Quizá el estado de flujo esté sobrevalorado

Una conclusión sorprendente: muchos nos metimos a programar porque amamos el estado de flujo —esa sensación pura de estar «en la zona»—. Pero la programación con IA no siempre fomenta la misma inmersión. Puedes pasar una hora afinando _prompts_, dejar que la IA genere cosas en segundo plano y asomarte de vez en cuando para aprobar o corregir.

A algunos esto les desconcierta; a otros —sobre todo quienes tienen hijos o mil tareas— les libera. Cuando puedes cambiar de contexto (revisar la salida de la IA, volver a la vida real y luego regresar a un fragmento ya funcional), descubres una nueva forma de ser productivo que no depende de largas franjas de silencio.

---

### ¿Hemos llegado al «peak programmer»?

Se comenta que, una vez la IA pueda generar código, habremos alcanzado el _peak programmer_: pronto no necesitaremos tantos ingenieros. Puede que sea parcialmente cierto si hablamos de trabajo directo sobre funcionalidades sencillas o de conectar una API. Pero también surgen nuevas complejidades: seguridad, cumplimiento normativo, cobertura de pruebas y arquitectura.

¿La diferencia real? Prosperarán los ingenieros estratégicos: quienes sepan orquestar varias herramientas de IA, vigilar la calidad del código y diseñar sistemas que escalen. Los que triunfen serán parte product manager, parte arquitecto, parte QA y parte desarrollador. Moldearán los _prompts_, definirán las pruebas, mantendrán la calidad y atenderán todos los casos límite que un LLM no prevé.

---

### Consejos desde la trinchera

Algunas cosas que he aprendido por las malas:

1. **Empieza manualmente y luego enciende la IA**

    Para las apps de iOS, inicializa el proyecto en Xcode primero; así los archivos autogenerados no confundirán a la IA. Después deja que la IA complete el resto.

2. **Los _prompts_ cortos y claros a veces superan instrucciones largas**

    Curiosamente, decirle a un LLM «make code better» puede funcionar tan bien como un _prompt_ superelaborado. Experimenta: algunos modelos responden mejor con menos restricciones.

3. **Usa un flujo de trabajo con _checkpoints_**

    Haz commits con frecuencia, incluso si es «Commit -m "It passed the tests, I guess!"». La IA puede romper todo tan rápido como lo arregla. Los commits frecuentes te dan puntos de control fáciles de revertir.

4. **Evita que la IA sobrepruebe lo básico**

    A la IA le encanta probarlo todo, incluso si un `for` sigue iterando. Mantente alerta, elimina las pruebas inútiles y mantén tu _pipeline_ ligero.

5. **Documenta absolutamente todo**

    Deja que la IA genere extensas _Implementation Guides_. Esas guías no solo te ayudan a ti; también ayudan a la propia IA en pasadas posteriores.

---

### Reflexiones finales

{{< image src="waterfall-road.webp" alt="Camino al futuro" caption="Camino al futuro. Colorado es plano. Leica Q, 14/5/2016" >}}

Nuestro sector está cambiando más rápido que nunca. Algunas de nuestras viejas suposiciones —como la centralidad del estado de flujo o los grandes festejos por funcionalidades meticulosamente hechas a mano— están a punto de parecer pintorescas. Pero eso no significa que perdamos creatividad. Ahora se trata de orquestación estratégica: saber qué construir, cómo describirlo y cómo impedir que se convierta en un _dumpster fire_ (un desastre monumental).

Al final, quizá descubramos que lo que hace que tu producto triunfe no es la fuerza bruta al escribir código, sino diseñar una experiencia que enamore a las personas. Porque, si podemos clonar diez versiones de Instagram en un fin de semana, el desempate no será lo elegante que esté el código, sino cuál conecta con la gente —y eso es un problema de diseño y producto, no puramente de ingeniería—.

Bienvenido al nuevo _Waterfall_: ciclos de 15 minutos con la IA como ingeniera júnior inagotable y tu _pipeline_ de código a hipervelocidad. Es raro, maravilloso y, a veces, aterrador. Y lo más probable es que todos tengamos que aprender este baile tarde o temprano.

---

_Qué mundo tan loco el nuestro. Creo que todo va a seguir poniéndose aún más raro. ¡Manos a la obra!_
