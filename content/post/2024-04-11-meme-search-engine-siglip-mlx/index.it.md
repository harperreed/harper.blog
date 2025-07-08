---
date: 2024-04-12 09:00:00-05:00
description: Ho creato un motore di ricerca di meme magico utilizzando siglip/CLIP
  e la codifica vettoriale delle immagini. È stato un modo divertente per conoscere
  questa potente tecnologia. Condivido il codice così potrai costruirne uno tuo e
  scoprire gemme dimenticate nella tua libreria fotografica. Liberiamo la potenza
  dell'IA sulle nostre immagini!
draft: false
generateSocialImage: true
slug: i-accidentally-built-a-meme-search-engine
tags:
- meme-search-engine
- vector-embeddings
- applied-ai
- siglip
- image-search
title: Ho creato per sbaglio un motore di ricerca di meme
translationKey: I accidentally built a meme search engine
---

## Ovvero: come imparare tutto su CLIP/SigLIP e sulla codifica vettoriale delle immagini

_tl;dr_: ho costruito un motore di ricerca per meme usando SigLIP/CLIP e la codifica vettoriale delle immagini. È stato divertente e ho imparato un sacco di cose.

Da un po’ realizzo strumenti di IA applicata. Uno degli elementi che mi è sempre sembrato più «magico» è l’ embedding vettoriale. [Word2Vec](https://en.wikipedia.org/wiki/Word2vec) e simili mi hanno letteralmente fatto esplodere il cervello: pura magia.

Su Hacker News ho visto [una piccola app](https://news.ycombinator.com/item?id=39392582) davvero [strepitosa](https://mood-amber.vercel.app/). Qualcuno ha crawlerizzato un mucchio di immagini da Tumblr, ha usato [SigLIP](https://arxiv.org/abs/2303.15343) per ottenere gli embedding vettoriali e poi ha messo online una semplice app: «clicca l’immagine e vedi quelle simili». Sembrava magia. Non avevo idea di come farlo, ma pareva a portata di mano.

Ho deciso di sfruttare questa improvvisa motivazione per capire davvero «come funziona tutto questo».

## wut

Se non ti sei mai imbattuto in embedding vettoriali, CLIP/SigLIP, database vettoriali e simili, non temere.

Prima di quell’hack su HN non avevo riflettuto granché su embedding multimodali o database vettoriali. Avevo usato FAISS (il semplice datastore vettoriale di Facebook) e Pinecone ($$) per qualche hack, ma senza approfondire: era solo «ok, i test passano».

Tuttora so a malapena cosa siano davvero i vettori, lol. Prima di mettermi su questo progettino non capivo bene come usarli al di fuori di RAG o di qualche altro processo LLM.

Io imparo costruendo. Se poi i risultati sono intriganti—e in questo caso pure un po’ magici—meglio ancora.

### Termini WTF

Alcuni amici hanno letto la bozza prima della pubblicazione e mi hanno chiesto: «WTF è X?». Ecco quindi un mini glossario di termini che erano nuovi anche per me:

- **Embedding vettoriali** – trasformano testo o immagini in rappresentazioni numeriche (vettori) che ti permettono di trovare facilmente elementi simili nella tua libreria.  
- **Database vettoriale** – sistema che memorizza e permette di cercare rapidamente gli elementi codificati, consentendoti di trovare quelli più simili.  
- **Word2Vec** – tecnica rivoluzionaria che converte le parole in vettori, permettendo di trovare termini affini ed esplorare le loro relazioni.  
- **CLIP** – modello di OpenAI che codifica immagini e testo in vettori numerici.  
- **OpenCLIP** – implementazione open-source di CLIP, utilizzabile e modificabile da chiunque senza bisogno di permessi speciali o accessi particolari.  
- **FAISS** – libreria ottimizzata per gestire e cercare grandi collezioni di vettori di immagini, rendendo rapidissimo trovare ciò che cerchi.  
- **ChromaDB** – database che memorizza e recupera i vettori di immagini e testo, restituendo al volo i risultati più simili.

## Tienila semplice, Harper.

Questo è un hack piuttosto lineare. Sto solo cazzeggiando, quindi non mi interessava farlo scalare davvero. Volevo però che fosse replicabile: qualcosa che **tu** potessi far girare senza troppa fatica.

Uno degli obiettivi era far girare tutto in locale sul mio portatile. Nei Mac abbiamo GPU di tutto rispetto: facciamole scaldare.

Il primo passo è stato creare un crawler semplice che scandisse una directory di immagini. Uso Apple Photos, quindi non avevo una cartella piena di foto. Però avevo un enorme mucchio di meme provenienti dalla mia preziosa e segretissima chat di meme (non dirlo a nessuno). Ho esportato la chat, spostato le immagini in una cartella e BAM: ecco il mio set di test.

### Il crawler

Ho creato il peggior crawler del mondo. Beh, a essere onesti: è Claude che l’ha scritto seguendo le mie istruzioni.

È un po’ contorto, ma ecco i passaggi:

1. Ottiene la lista dei file della directory target.  
2. Salva la lista in un file msgpack.  
3. Legge il msgpack, scorre ogni immagine e la inserisce in un database SQLite con qualche metadato:  
   - hash  
   - dimensione del file  
   - posizione/percorso  
4. Scorre il database SQLite e usa CLIP per ottenere l’embedding vettoriale di ogni immagine.  
5. Salva quegli embedding di nuovo nel database SQLite.  
6. Scorre il database SQLite e inserisce vettori e percorso dell’immagine in ChromaDB.  
7. Fine.  

Un sacco di lavoro superfluo: potresti semplicemente iterare sulle immagini, prendere gli embedding e caricarli su ChromaDB (l’ho scelta perché è facile, gratis e non richiede infrastruttura).

L’ho fatta così perché:

- Dopo i meme ho indicizzato 140 000 immagini e volevo fosse resiliente ai crash.  
- Doveva poter riprendere in caso di crash, blackout, ecc.  
- Adoro i cicli.

Nonostante la complessità extra, ha funzionato alla grande: più di 200 000 immagini senza un singhiozzo.

### Un sistema di embedding

Codificare le immagini è stato divertente.

Sono partito da SigLIP e ho creato un [semplice web service](https://github.com/harperreed/imbedding) dove carichi l’immagine e ottieni i vettori. Girava su una GPU in studio e andava bene. Non velocissimo, ma comunque molto più veloce che eseguire [OpenCLIP](https://github.com/mlfoundations/open_clip) in locale.

Ma volevo comunque eseguirlo sul portatile. Mi sono ricordato del repository [ml-explore](https://github.com/ml-explore/) di Apple, che contiene alcuni esempi utili. E *bam*: ho trovato un’[implementazione di CLIP](https://github.com/ml-explore/mlx-examples/tree/main/clip) velocissima—più veloce perfino di una 4090. Da fuori di testa (*wildstyle*).

Dovevo solo integrarla comodamente nel mio script.

### MLX_CLIP

Io e Claude abbiamo «convinto» lo script d’esempio di Apple a diventare una piccola classe Python che puoi usare in locale su qualsiasi macchina. Scarica i modelli se non ci sono, li converte e li usa al volo nel tuo script.

La trovi qui: https://github.com/harperreed/mlx_clip

Sono piuttosto soddisfatto del risultato. Lo sappiamo: Apple Silicon va come un razzo.

Usarla è facilissimo (commenti in inglese per chi copia/incolla):

```python
import mlx_clip

# Initialize the mlx_clip model with the given model name.
clip = mlx_clip.mlx_clip("openai/clip-vit-base-patch32")

# Encode the image from the specified file path and obtain the image embeddings.
image_embeddings = clip.image_encoder("assets/cat.jpeg")
print(image_embeddings)

# Encode the text description and obtain the text embeddings.
text_embeddings = clip.text_encoder("a photo of a cat")
print(text_embeddings)
```

Mi piacerebbe farlo andare con SigLIP, che preferisco (è molto meglio di CLIP). Però questo è più un POC che un prodotto da mantenere. Se qualcuno ha dritte su come far girare SigLIP—[fate un fischio](mailto:harper@modest.com). Non voglio reinventare OpenCLIP, che in teoria dovrebbe andare bene su Apple Silicon ed è già ottimo.

### E adesso?

Ora che tutti i vettori delle immagini sono nel database vettoriale possiamo passare all’interfaccia. Ho usato la funzione di query integrata di ChromaDB per mostrare immagini simili.

Ottieni i vettori dell’immagine di partenza, li passi a ChromaDB, che restituisce una lista di ID immagine ordinati per similarità decrescente.

Poi ho impacchettato tutto in un’app Tailwind/Flask. Una figata.

Nel 2015 ci avremmo messo una vita per costruire una cosa del genere. Io ci ho speso forse 10 ore totali ed è stato banale.

Il risultato è roba da dire «porca miseria, che magia!».

### Ricerca concettuale di meme

Ricorda: ho usato i meme come set iniziale, circa 12 000.

Parti da questa:

{{< image src="images/posts/vector-memes-bowie.png" caption="So true" >}}

La codifichi, la passi a ChromaDB e…

Ecco le immagini simili:  
{{< image src="images/posts/vector-memes-bowie-results.png" >}}

Altro esempio:  
{{< image src="images/posts/vector-memes-star-trek.png" >}}

Risultati:  
{{< image src="images/posts/vector-memes-star-trek-results.png" >}}

È divertentissimo cliccare in giro.

### Namespaces?

La vera magia non è cliccare un’immagine per trovarne una simile—figo, ma non «holy shit».

Quello che mi ha sconvolto è usare lo stesso modello per codificare il testo di ricerca in vettori e trovare immagini simili a quel testo.

Per qualche ragione mi manda in tilt. Una cosa è cercare immagini semanticamente simili a un’altra immagine; avere un’interfaccia multimodale così elegante è un vero trucco di prestigio.

Esempi:

Cercando **money**. Prendo l’embedding di «money» e lo passo a ChromaDB. Risultati:  
{{< image src="images/posts/vector-memes-money.png" >}}

Cercando **AI**  
{{< image src="images/posts/vector-memes-ai.png" >}}

Cercando **red** (è un colore? uno stile di vita? la Russia?)  
{{< image src="images/posts/vector-memes-red.png" >}}

E avanti così, all’infinito. Magia pura. Ritrovi chicche dimenticate. Oh, mi serve un meme sulla scrittura di un post:  
{{< image src="images/posts/vector-memes-writing-meme.jpg" >}}

(Sì, sono auto-ironico, ma chissenefrega – lol)

### Come va con una libreria di foto?

Alla grande.

Consiglio caldamente di provarlo sulla tua raccolta. Per iniziare ho scaricato il mio archivio Takeout da Google Photos. L’ho estratto su un disco esterno, ho lanciato qualche script per ripulirlo (chi ha progettato il Takeout di Google adora i duplicati). Poi ho puntato lo script a quella directory invece che alla cartella dei meme e via, a tutta velocità.

Avevo circa 140 000 foto e ci ha messo 6 ore. Non male. I risultati sono incredibili.

#### Alcuni esempi divertenti:

Ovviamente queste sono simili (e ho un problema di duplicati su Google Photos)  
{{< image src="images/posts/vector-memes-harper.png" >}}

Abbiamo avuto molti barboncini. Eccone alcuni:  
{{< image src="images/posts/vector-memes-poodles.png" >}}

Puoi cercare luoghi. Non sapevo di aver fotografato il Fuji-san da un aereo!  
{{< image src="images/posts/vector-memes-fuji-results.png" >}}

E poi trovare immagini simili del Monte Fuji.  
{{< image src="images/posts/vector-memes-fuji-similar.png" >}}

Facile cercare città.  
{{< image src="images/posts/vector-memes-chicago.png" >}}

O emozioni. A quanto pare sono spesso sorpreso.  
{{< image src="images/posts/vector-memes-surprised.png" >}}

Anche chicche di nicchia come i low-rider (questi sono di Shibuya!)  
{{< image src="images/posts/vector-memes-low-riders.png" >}}

E puoi cercare cose difficili da filtrare, tipo il bokeh.  
{{< image src="images/posts/vector-memes-bokeh.png" >}}

Meraviglioso: puoi cliccare e ritrovare foto splendide dimenticate. Come questo scatto di Baratunde del 2017:

{{< image src="images/posts/vector-memes-baratunde.png" >}}

### Questo sarà ovunque

Scommetto che questa tecnologia finirà presto in tutte le app fotografiche. Probabilmente Google Photos lo fa già, ma l’hanno «googlizzata» talmente tanto che nessuno se ne accorge.

È troppo utile per non integrarla in qualunque app di immagini. Se gestissi un prodotto che usa foto, metterei subito su una pipeline per codificarle e scoprire funzionalità inedite.

## PUOI AVERLO AL FANTASTICO PREZZO DI… GRATIS

Il codice è qui: [harperreed/photo-similarity-search](https://github.com/harperreed/photo-similarity-search).

Dacci un’occhiata.

Avviarlo è abbastanza semplice, anche se un po’ raffazzonato, lol.

Usa conda o simili per tenere pulito l’ambiente. L’interfaccia è in Tailwind, il web è Flask, il codice è Python.  
Il vostro anfitrione di turno è Harper Reed.

## La mia sfida per te!

Costruisci un’app che possa catalogare la mia libreria di foto in modo elegante. Non voglio caricarle altrove. Voglio una semplice app Mac che punti alla mia libreria e dica «scansiona». Immagino si possano aggiungere tante chicche:

- didascalie automatiche con Llava/Moondream  
- parole chiave / tag  
- similarità vettoriale  
- ecc.

Deve girare in locale, essere nativa, semplice ed efficace. Magari integrarsi con Lightroom, Capture One o Apple Photos.

La voglio. Costruiscila. Scopriamo tutte le foto stupende che abbiamo grazie alla magia dell’IA.

## Extra Credit: recupero JPEG dalle miniature di Lightroom

Il mio compagno di hack Ivan era con me durante il progetto. Ha subito colto la magia di esplorare la propria libreria così. Voleva provarlo all’istante.

Il suo catalogo foto sta su un hard disk esterno, ma aveva il file di anteprima di Lightroom in locale. Ha scritto uno script veloce per estrarre miniature e metadati dal file di anteprima e salvarli su un disco esterno.

Abbiamo lanciato il crawler vettoriale e BAM: anche lui poteva vedere immagini simili, e via dicendo. Perfetto.

#### Recupera le tue foto di Lightroom. O almeno le miniature.

Lo script di Ivan per estrarre immagini dal file `.lrpreview` è fantastico. Se hai perso la libreria originale (hard disk corrotto, ecc.) e ti resta il `.lrpreview`, questo script ti permette di salvare almeno la versione a bassa risoluzione.

Uno script utilissimo da tenere.

Lo trovi qui: [LR Preview JPEG Extractor](https://github.com/ibips/lrprev-extract).

## Grazie per aver letto fin qui.

Come sempre, [scrivimi](mailto:harper@modest.com) e facciamo due chiacchiere. Sto pensando un sacco a IA, e-commerce, foto, hi-fi, hacking e altre stronzate.

Se sei a Chicago, passa a trovarmi.