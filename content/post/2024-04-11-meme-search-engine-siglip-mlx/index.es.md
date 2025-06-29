---
date: 2024-04-12 09:00:00-05:00
description:
    Construí un buscador de memes mágico usando siglip/CLIP y codificación
    vectorial de imágenes. Fue una forma divertida de aprender sobre esta poderosa tecnología.
    Comparto el código para que puedas crear el tuyo y descubrir joyas olvidadas en
    tu biblioteca de fotos. ¡Desatemos el poder de la IA en nuestras imágenes!
draft: false
generateSocialImage: true
slug: i-accidentally-built-a-meme-search-engine
tags:
    - meme-search-engine
    - vector-embeddings
    - applied-ai
    - siglip
    - image-search
title: "Accidentalmente construí un buscador de memes"
translationKey: I accidentally built a meme search engine
---

# O bien: cómo aprender sobre siglip/CLIP y la codificación vectorial de imágenes

_tl;dr_: Construí un buscador de memes con siglip/CLIP y codificación vectorial de imágenes. Fue muy divertido y aprendí un montón.

Llevo un tiempo creando un montón de herramientas de IA aplicada. Uno de los componentes que siempre me ha parecido más mágico son los _embeddings_ vectoriales. [Word2Vec](https://en.wikipedia.org/wiki/Word2vec) y similares me volaron la cabeza. Es como magia.

Vi una [app sencilla en Hacker News](https://news.ycombinator.com/item?id=39392582) que era [súper impresionante](https://mood-amber.vercel.app/). Alguien rastreó muchas imágenes de Tumblr, usó [siglip](https://arxiv.org/abs/2303.15343) para obtener los _embeddings_ y luego montó una app de «haz clic en una imagen y ve otras similares». Parecía magia. No tenía idea de cómo lograrlo, pero se veía alcanzable.

Decidí aprovechar la motivación para aprender cómo funciona todo esto.

## wut

Si nunca te has topado con _embeddings_ vectoriales, siglip/CLIP, bases de datos vectoriales y compañía, no te preocupes.

Antes de ver aquel hack en HN apenas pensaba en _embeddings_ vectoriales, _embeddings_ multimodales o almacenes vectoriales. Había usado FAISS (la base vectorial sencilla de Facebook) y Pinecone ($$) en algunos experimentos, pero sin profundizar: los hacía funcionar y luego pensaba «listo, las pruebas pasan».

Sigo sin tener clarísimo qué demonios son los vectores, jajaja. Antes de meterme a construir esto, de verdad no veía cómo usarlos fuera de RAG (Retrieval-Augmented Generation) u otro proceso con LLM.

Aprendo construyendo. Ayuda cuando los resultados son intrigantes y, en este caso, prácticamente mágicos.

### Glosario WTF

Unos amigos leyeron esto antes de publicarlo y varios dijeron «¿WTF es X?». Aquí va una lista breve de términos que eran casi nuevos para mí:

- **Embeddings vectoriales**: convierten tu texto —o, mejor dicho, _text of images_— en representaciones numéricas que permiten encontrar fotos similares y buscar tu biblioteca con eficacia.
- **Base de datos vectorial**: sistema para almacenar y buscar elementos codificados, lo que posibilita hallar ítems parecidos.
- **Word2Vec**: técnica pionera que convierte palabras en vectores numéricos y permite encontrar términos afines y explorar sus relaciones.
- **CLIP**: modelo de OpenAI que codifica imágenes y texto en vectores numéricos.
- **OpenCLIP**: implementación de código abierto del modelo CLIP, que cualquiera puede usar y ampliar sin permisos especiales.
- **FAISS**: biblioteca eficiente para gestionar y buscar en grandes colecciones de vectores de imágenes; facilita encontrar la imagen que buscas.
- **ChromaDB**: base de datos que guarda y recupera vectores de imagen y texto, devolviendo rápidamente los resultados más similares.

## Manténlo simple, Harper

Este proyecto es bastante directo. Solo estoy trasteando, así que no me preocupaba escalarlo. Sí quería que fuera replicable: algo que **tú** pudieras ejecutar sin mucho esfuerzo.

Una de mis metas era que todo se ejecutara localmente en mi portátil. Tenemos estas GPU muy potentes en los Mac: ¡vamos a calentarlas!

El primer paso fue crear un rastreador sencillo que recorriera un directorio de imágenes. Uso Apple Photos, así que no tenía una carpeta llena de fotos sueltas. Eso sí, tenía una enorme carpeta de memes de mi preciado y muy secreto chat de memes (no se lo digas a nadie). Exporté el chat, moví las imágenes a un directorio y ¡BAM!, ya tenía mi conjunto de pruebas.

### El rastreador

Creé el peor rastreador del mundo. Bueno, seamos honestos: Claude lo creó con mis indicaciones.

Es un poco enrevesado, pero estos son los pasos:

1. Obtiene la lista de archivos del directorio objetivo.
2. Guarda la lista en un archivo `msgpack`.
3. A partir del archivo `msgpack`, recorre cada imagen y la almacena en una base de datos SQLite, extrayendo algunos metadatos:
    - hash
    - tamaño de archivo
    - ubicación
4. Recorre esa base SQLite y usa CLIP para obtener el vector de cada imagen.
5. Guarda esos vectores de nuevo en la base SQLite.
6. Recorre la base SQLite e inserta los vectores y la ruta de la imagen en ChromaDB.
7. Fin.

Sí, es mucho trabajo redundante: podría recorrer las imágenes, sacar los _embeddings_ y meterlos directamente en ChromaDB (la elegí porque es sencilla, gratuita y sin infraestructura adicional).

Lo hice así porque:

- Después de los memes, rastreé 140 000 imágenes y quería que fuera resistente a fallos.
- Necesitaba poder reanudar la construcción de las bases si se cortaba la luz o se colgaba el sistema.
- Me encantan los bucles.

Pese a la complejidad extra, funcionó sin problemas. He rastreado más de 200 000 imágenes sin un solo tropiezo.

### Un sistema de embeddings

Codificar las imágenes fue muy divertido.

Empecé con siglip y creé un [servicio web sencillo](https://github.com/harperreed/imbedding) donde subíamos la imagen y obteníamos los vectores. Corría en una de nuestras máquinas con GPU y funcionaba bien. No era rápido, pero sí más veloz que ejecutar OpenCLIP localmente.

Aun así quería ejecutarlo en mi máquina. Recordé que el repositorio [ml-explore](https://github.com/ml-explore/) de Apple tenía ejemplos interesantes. ¡Y BAM!, tenían una [implementación de CLIP](https://github.com/ml-explore/mlx-examples/tree/main/clip) rapidísima. Incluso con el modelo grande era más veloz que la 4090. Una locura.

Solo tenía que facilitar su uso dentro de mi script.

### MLX_CLIP

Claude y yo adaptamos el script de ejemplo de Apple y lo convertimos en una pequeña clase de Python que puedes usar localmente. Descarga los modelos si no existen, los convierte y los usa al vuelo.

Puedes verlo aquí: https://github.com/harperreed/mlx_clip

Estoy bastante satisfecho con el resultado. El silicio de Apple es rapidísimo.

Resultó muy sencillo de usar:

```python
import mlx_clip

# Inicializa el modelo con el nombre elegido.
clip = mlx_clip.mlx_clip("openai/clip-vit-base-patch32")

# Codifica la imagen y obtén los embeddings.
image_embeddings = clip.image_encoder("assets/cat.jpeg")
print(image_embeddings)

# Codifica el texto y obtén los embeddings.
text_embeddings = clip.text_encoder("a photo of a cat")
print(text_embeddings)
```

Me encantaría que esto funcionara con siglip, porque prefiero ese modelo (es mucho mejor que CLIP). Sin embargo, esto es una prueba de concepto, no un producto que quiera mantener. Si alguien sabe cómo hacerlo con siglip, [avísame](mailto:harper@modest.com). No quiero reinventar OpenCLIP, que en teoría corre bien en Apple Silicon y es muy bueno.

### ¿Y ahora qué?

Con todos los vectores cargados en el almacén vectorial, era momento de la interfaz. Usé la función de consulta integrada de ChromaDB para mostrar imágenes similares.

Obtienes los vectores de la imagen de partida, los consultas en ChromaDB y ChromaDB devuelve una lista de ID de imágenes similares en orden descendente de similitud.

Luego envolví todo en una app con Tailwind CSS y Flask.  
Fue increíble.

Ni imaginar el trabajo que habría supuesto en 2015. Invertí quizá diez horas y fue trivial.

Los resultados parecen magia.

### Búsqueda de conceptos en memes

Recuerda: usé memes como conjunto inicial. Tenía 12 000 memes para buscar.

Empieza con esto:

{{< image src="images/posts/vector-memes-bowie.png" caption="So true" >}}

Lo codificas, envías el vector a ChromaDB y listo.

Las imágenes que devuelve son así:  
{{< image src="images/posts/vector-memes-bowie-results.png" >}}

Otro ejemplo:  
{{< image src="images/posts/vector-memes-star-trek.png" >}}

Devuelve cosas como:  
{{< image src="images/posts/vector-memes-star-trek-results.png" >}}

Es muy divertido hacer clic y explorar.

### ¿Namespaces?

La verdadera magia no está en hacer clic en una imagen y obtener otra similar. Eso está bien, pero no fue mi momento de «¡guau!».

Lo que me voló la cabeza fue usar el mismo modelo para codificar texto de búsqueda en vectores y encontrar imágenes que coinciden con ese texto.

Por alguna razón, esto me deja boquiabierto. Una cosa es una búsqueda semántica de imagen a imagen. Pero tener una interfaz multimodal agradable lo convierte en un truco de magia.

Ejemplos:

Buscar **money**. Obtengo el _embedding_ de _money_ y lo envío a ChromaDB. Los resultados:  
{{< image src="images/posts/vector-memes-money.png" >}}

Buscar **AI**  
{{< image src="images/posts/vector-memes-ai.png" >}}

Buscar **red** (¿color, estilo de vida, Rusia?)  
{{< image src="images/posts/vector-memes-red.png" >}}

Y así hasta el infinito. Es mágico. Encuentras joyas olvidadas. «Necesito un meme sobre escribir un blog post»:  
{{< image src="images/posts/vector-memes-writing-meme.jpg" >}}

(Soy consciente; simplemente no me importa, jajaja).

### ¿Cómo funciona con una fototeca?

Funciona de maravilla.

Te recomiendo encarecidamente ejecutar esto sobre tu biblioteca de fotos. Para empezar, descargué mi archivo de Google Photos Takeout, lo descomprimí en un disco externo y ejecuté unos scripts para hacerlo usable (quien diseñó el Takeout está obsesionado con los duplicados). Luego apunté el script a ese directorio en vez de a la carpeta de memes y lo dejé correr.

Tenía unas 140 000 fotos y tardó unas seis horas. Nada mal. Los resultados son increíbles.

#### Algunos ejemplos divertidos

Obviamente se parecen (también tengo problema de duplicados en Google Photos):  
{{< image src="images/posts/vector-memes-harper.png" >}}

Hemos tenido muchos caniches. Aquí algunos:  
{{< image src="images/posts/vector-memes-poodles.png" >}}

Puedes buscar monumentos. ¡No sabía que había fotografiado el Fuji-san desde un avión!  
{{< image src="images/posts/vector-memes-fuji-results.png" >}}

Luego encontrar imágenes parecidas del monte Fuji.  
{{< image src="images/posts/vector-memes-fuji-similar.png" >}}

Buscar lugares es muy sencillo.  
{{< image src="images/posts/vector-memes-chicago.png" >}}

O emociones. Al parecer me sorprendo mucho, así que tengo un montón de fotos «sorprendidas».  
{{< image src="images/posts/vector-memes-surprised.png" >}}

También cosas de nicho como _lowriders_ (¡estas son de Shibuya!):  
{{< image src="images/posts/vector-memes-low-riders.png" >}}

Y sirve para encontrar cosas difíciles de etiquetar, como el _bokeh_.  
{{< image src="images/posts/vector-memes-bokeh.png" >}}

Es maravilloso, porque puedo hacer clic y encontrar fotos geniales que había olvidado. Como esta gran foto de Baratunde que tomé en 2017:

{{< image src="images/posts/vector-memes-baratunde.png" >}}

### Esto estará en todas partes

Imagino que veremos esta tecnología integrada en todas las apps de fotos dentro de poco. Google Photos probablemente ya lo hace, pero lo han “googleado” tanto que nadie lo nota.

Es demasiado buena como para no incorporarla. Si tuviera un producto a gran escala que use imágenes, montaría ya mismo una tubería para codificarlas y ver qué funciones interesantes se desbloquean.

## PUEDES USAR ESTO POR EL MÓDICO PRECIO DE GRATIS

El código está aquí: [harperreed/photo-similarity-search](https://github.com/harperreed/photo-similarity-search).

Échale un vistazo.

Es bastante directo ponerlo en marcha, aunque un poco improvisado.

Usa conda o algo similar para mantener todo limpio. La interfaz está en Tailwind CSS, la web en Flask, el código en Python. Tu anfitrión: Harper Reed.

## ¡Mi reto para ti!

Construye una app que me permita catalogar mi fototeca de forma cómoda. No quiero subirla a ningún sitio: quiero una app nativa para Mac que apunte a mi biblioteca de fotos y diga «rastrea esto». Se le podrían añadir cosas geniales:

- Autocaptioning con Llava/Moondream
- Palabras clave / etiquetas
- Similitud vectorial
- etc.

Debe ejecutarse localmente, ser una app nativa, sencilla y eficaz. Quizá integrarse con Lightroom, Capture One o Apple Photos.

Lo quiero. ¡Constrúyelo! Descubramos todas las fotos increíbles que hemos tomado gracias a la magia de la IA.

## Crédito extra: recuperación de JPEG de previsualización de Lightroom

Mi colega hacker Ivan estaba por aquí mientras montaba esto. En cuanto vio la magia de usarlo sobre una fototeca, quiso probarlo.

Su catálogo está en un disco externo, pero tenía el archivo de previsualización de Lightroom en local. Escribió un script rápido para extraer las miniaturas y metadatos del archivo y guardarlos en un disco externo.

Luego lanzamos el rastreador de vectores y ¡BAM!, pudo ver imágenes similares y demás. Funcionó perfecto.

#### Recupera tus fotos de Lightroom… o al menos las miniaturas

El sencillo script de Ivan para extraer imágenes del archivo `.lrprev` es genial. Si alguna vez pierdes tu biblioteca (disco dañado, lo que sea) y aún tienes el archivo de previsualización, este script puede ayudarte a rescatar al menos la versión en baja resolución.

Un script muy útil para tener a mano.

Puedes verlo aquí: [LR Preview JPEG Extractor](https://github.com/ibips/lrprev-extract).

## Gracias por leer

Como siempre, [avísame](mailto:harper@modest.com) y salgamos a charlar. Estoy pensando mucho en IA, comercio electrónico, fotos, hi-fi, _hacking_ y otras cosas.

Si estás por Chicago, pasa a saludar.
