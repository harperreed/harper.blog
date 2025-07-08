---
date: 2024-04-12 09:00:00-05:00
description: Ich habe mit siglip/CLIP und der Vektorkodierung von Bildern eine magische
  Meme-Suchmaschine gebaut. Es war eine unterhaltsame Möglichkeit, diese leistungsstarke
  Technologie kennenzulernen. Ich teile den Code, damit du deine eigene bauen und
  vergessene Schätze in deiner Fotobibliothek entdecken kannst. Lass uns die Kraft
  der KI auf unsere Bilder loslassen!
draft: false
generateSocialImage: true
slug: i-accidentally-built-a-meme-search-engine
tags:
- meme-search-engine
- vector-embeddings
- applied-ai
- siglip
- image-search
title: Ich habe versehentlich eine Meme-Suchmaschine gebaut
translationKey: I accidentally built a meme search engine
---

## Oder: wie man CLIP/SigLIP kennenlernt und Bilder per Vektoren kodiert

_tl;dr_: Ich habe eine Meme-Suchmaschine mit SigLIP/CLIP und Vektor-Einbettungen gebaut. Es war mega spaßig und ich habe eine Menge gelernt.

Seit einiger Zeit baue ich praktische KI-Tools. Der Teil, der mir dabei immer am magischsten vorkam, waren Vektor-Einbettungen. [Word2Vec](https://en.wikipedia.org/wiki/Word2vec) und ähnliche Techniken haben mir regelrecht den Kopf verdreht – pure Zauberei.

Auf [Hacker News](https://news.ycombinator.com/item?id=39392582) stieß ich auf eine [super einfache App](https://mood-amber.vercel.app/), die mich schwer beeindruckt hat. Jemand hatte einen Haufen Tumblr-Bilder gecrawlt, sie mit [SigLIP](https://arxiv.org/abs/2303.15343) eingebettet und daraus eine simple „Klick aufs Bild, zeig mir ähnliche Bilder“-App gebaut. Es fühlte sich nach Magie an. Ich hatte keinen Plan, wie man so etwas umsetzt – aber es wirkte machbar.

Also nutzte ich den plötzlichen Motivationsschub, um herauszufinden, _wie das alles eigentlich funktioniert_.

## *wut*

Falls dir Vektor-Einbettungen, multimodale Einbettungen, CLIP/SigLIP, Vektordatenbanken und Ähnliches noch nie begegnet sind – keine Sorge.

Vor diesem Hack hatte ich darüber kaum nachgedacht. Ich hatte zwar mit FAISS (Facebooks einfache Vektor-Datenbank) und Pinecone ($$) herumgebastelt, aber nie wirklich tief gegraben. Ich brachte es kurz zum Laufen und dachte: „Yep. Tests bestanden.“

Ich habe immer noch kaum eine Ahnung, was Vektoren eigentlich sind, lol. Bevor ich damit anfing, verstand ich nicht, wofür ich sie außerhalb von RAG oder anderen LLM-Workflows nutzen sollte.

Ich lerne am besten, indem ich baue – und je magischer das Ergebnis wirkt, desto schneller lerne ich.

### WTF-Begriffe

Ein paar Freunde haben das vorab gelesen und gefragt: „WTF ist X?“ Hier eine kurze Liste von Begriffen, die damals auch für mich neu waren:

- **Vektor-Einbettungen** – wandeln Text oder Bilder in Zahlenvektoren um, sodass du ähnliche Objekte finden und deine Bibliothek effektiv durchsuchen kannst.  
- **Vektordatenbank** – speichert diese Vektoren und ermöglicht schnelles Suchen nach ähnlichen Elementen.  
- **Word2Vec** – bahnbrechende Technik, die Wörter in numerische Vektoren übersetzt; damit kann man z. B. ähnliche Wörter finden oder Beziehungen erkunden.  
- **CLIP** – OpenAIs Modell, das Bilder und Text in numerische Vektoren kodiert.  
- **OpenCLIP** – Open-Source-Implementierung von CLIP, die jeder ohne besondere Zugriffs- oder Lizenzanforderungen nutzen und erweitern kann.  
- **FAISS** – effiziente Bibliothek zum Verwalten und Durchsuchen großer Vektorbestände.  
- **ChromaDB** – Datenbank, die Bild- und Textvektoren speichert und blitzschnell ähnliche Ergebnisse liefert.  

## Mach’s einfach, Harper.

Das hier ist ein ziemlich geradliniges Hackerprojekt. Ich fummel nur rum, also war mir Skalierbarkeit egal. Mir ging es darum, dass **du** das ohne viel Aufwand nachbauen kannst.

Eines meiner Ziele war, alles lokal auf meinem Laptop laufen zu lassen. Wir haben diese schicken Mac-GPUs – lassen wir sie mal richtig heiß laufen.

Der erste Schritt war ein simpler Crawler, der ein Verzeichnis voller Bilder durchsucht. Ich nutze Apple Photos, hatte also keinen Ordner mit all meinen Fotos. Dafür aber einen riesigen Ordner voller Memes aus meinem streng geheimen Meme-Chat (nicht weitersagen!). Chat exportiert, Bilder in einen Ordner geschoben – BÄM – fertiger Testdatensatz.

### Der Crawler

Ich habe den schlechtesten Crawler der Welt gebaut. Genau genommen hat Claude ihn nach meinen Anweisungen gebaut.

Hier die Schritte im Überblick:

1. Er holt die Dateiliste des Zielverzeichnisses.  
2. Er speichert diese Liste in einer msgpack-Datei.  
3. Er liest die msgpack-Datei wieder ein, iteriert über jedes Bild und legt es in einer SQLite-DB ab – inklusive  
   - Hashwert  
   - Dateigröße  
   - Speicherort  
4. Dann iteriert er über die SQLite-DB und lässt CLIP für jedes Bild die Vektor-Einbettungen berechnen.  
5. Die Vektoren werden wieder in die SQLite-DB geschrieben.  
6. Anschließend läuft er noch einmal über die DB und schiebt Vektoren plus Bildpfad in Chroma, eine Vektordatenbank.  
7. Fertig.

Das ist eine Menge unnötige Arbeit – man könnte beim Durchlauf direkt einbetten und alles nach Chroma schreiben (ich habe Chroma gewählt, weil es simpel, kostenlos und ohne zusätzliche Infrastruktur ist).

Warum also der Umweg?

- Nach den Memes habe ich 140 000 Bilder gecrawlt und wollte, dass das Ding Abstürze wegsteckt.  
- Falls Strom ausfällt oder sonst etwas passiert, soll es genau dort weitermachen.  
- Ich mag Loops.  

Trotz der Extrakomplexität lief alles glatt. Ich habe über 200 000 Bilder verarbeitet – ohne Mucken.

### Ein Einbettungssystem

Das Kodieren der Bilder hat richtig Spaß gemacht.

Ich begann mit SigLIP und baute einen [einfachen Web-Service](https://github.com/harperreed/imbedding), bei dem man ein Bild hochlädt und die Vektoren zurückbekommt. Das lief auf einer unserer GPU-Maschinen und war nicht superschnell, aber immer noch deutlich schneller, als OpenCLIP lokal auszuführen.

Trotzdem wollte ich alles lokal haben. Ich erinnerte mich ans [ml-explore](https://github.com/ml-explore/)-Repo von Apple. Und BÄM – dort gab es eine [CLIP-Implementierung](https://github.com/ml-explore/mlx-examples/tree/main/clip), die schnell as fuck ist – wildstyle! Selbst das größere Modell lief schneller als eine 4090.

Ich musste das nur skripttauglich machen.

### MLX_CLIP

Claude und ich haben das Apple-Beispiel in eine kleine Python-Klasse gegossen, die du lokal auf jedem deiner Rechner nutzen kannst (besonders schnell auf Apple Silicon). Fehlen die Modelle, werden sie heruntergeladen, konvertiert und direkt verwendet.

Zu finden unter: https://github.com/harperreed/mlx_clip

Ich bin ziemlich stolz darauf – Apple Silicon ist wirklich schnell as fuck.

Benutzung:

```python
import mlx_clip

# Modell initialisieren
clip = mlx_clip.mlx_clip("openai/clip-vit-base-patch32")

# Bild einbetten
image_embeddings = clip.image_encoder("assets/cat.jpeg")
print(image_embeddings)

# Text einbetten
text_embeddings = clip.text_encoder("a photo of a cat")
print(text_embeddings)
```

Ich würde das gern auch mit SigLIP zum Laufen bringen – das Modell schlägt CLIP deutlich. Aber hier geht’s nur um einen Proof of Concept. Wer einen Tipp hat, wie SigLIP auf Apple Silicon fliegt: [hmu](mailto:harper@modest.com). OpenCLIP sollte theoretisch bereits gut laufen und ist ebenfalls stark.

### Und jetzt?

Nachdem alle Bildvektoren in der Vektordatenbank lagen, konnte ich das Interface bauen. Ich nutzte die eingebaute Query-Funktion von ChromaDB, um ähnliche Bilder anzuzeigen.

Bild auswählen, Vektoren holen, Chroma fragen. Chroma spuckt eine Liste von Bild-IDs aus, sortiert nach abnehmender Ähnlichkeit.

Ich habe das Ganze in eine Tailwind/Flask-App gepackt.  
Ich kann mir gar nicht ausmalen, wie viel Arbeit wir 2015 dafür hätten aufbringen müssen. Ich habe vielleicht zehn Stunden daran gesessen – trivial.

Das Ergebnis ist einfach magisch.

### Meme-Konzeptsuche

Zur Erinnerung: Mein erster Datensatz bestand aus Memes – 12 000 Stück.

Starte mit diesem Bild:

{{< image src="images/posts/vector-memes-bowie.png" caption="So true" >}}

Einbetten, an Chroma schicken, ähnliche Bilder holen:

{{< image src="images/posts/vector-memes-bowie-results.png" >}}

Noch ein Beispiel:

{{< image src="images/posts/vector-memes-star-trek.png" >}}

liefert:

{{< image src="images/posts/vector-memes-star-trek-results.png" >}}

Es macht richtig Laune, sich da durchzuklicken.

### Namespaces?

Nur auf ein Bild zu klicken, um ähnliche zu finden, ist cool, aber noch nicht „holy shit“.

Was mich völlig umgehauen hat: denselben Encoder auf Suchtext anzuwenden und damit passende Bilder zu finden.

Warum auch immer – das verdreht mir den Kopf. Bild-zu-Bild-Suche ist schon nett, aber eine echte multimodale Schnittstelle fühlt sich wie ein Zaubertrick an.

Beispiele:

Suche nach **money** – Vektoren holen, Chroma fragen:  
{{< image src="images/posts/vector-memes-money.png" >}}

Suche nach **AI**  
{{< image src="images/posts/vector-memes-ai.png" >}}

Suche nach **red** (Farbe? Lebensstil? Russland?)  
{{< image src="images/posts/vector-memes-red.png" >}}

Und so weiter, endlos. Magisch. Man findet ständig vergessene Schätze. Brauche ich ein Meme übers Blogschreiben?  
{{< image src="images/posts/vector-memes-writing-meme.jpg" >}}

(ich bin mir dessen bewusst, aber es ist mir egal, lol)

### Wie schlägt sich das bei einer Fotobibliothek?

Großartig.

Ich kann nur empfehlen, das auf deine Fotobibliothek loszulassen. Ich habe mir mein Google-Photos-Takeout gezogen, auf eine externe Platte entpackt (wer immer das designt hat, scheint geradezu begeistert von Dubletten zu sein) und das Skript auf dieses Verzeichnis losgelassen.

Bei etwa 140 000 Fotos dauerte das rund sechs Stunden. Nicht übel – und die Ergebnisse sind beeindruckend.

#### Ein paar Beispiele:

Offensichtlich ähnliche Aufnahmen (Dubletten, wohin man schaut)  
{{< image src="images/posts/vector-memes-harper.png" >}}

Wir hatten viele Pudel. Hier ein paar:  
{{< image src="images/posts/vector-memes-poodles.png" >}}

Landmarks: Ich wusste nicht, dass ich den Fuji-san aus dem Flugzeug geknipst hatte!  
{{< image src="images/posts/vector-memes-fuji-results.png" >}}

Ähnliche Fuji-Bilder:  
{{< image src="images/posts/vector-memes-fuji-similar.png" >}}

Orte finden ist easy:  
{{< image src="images/posts/vector-memes-chicago.png" >}}

Oder Emotionen. Offenbar schaue ich oft überrascht:  
{{< image src="images/posts/vector-memes-surprised.png" >}}

Auch Nischiges wie Lowrider-Cars (diese sind aus Shibuya!):  
{{< image src="images/posts/vector-memes-low-riders.png" >}}

Und Motive, die schwer zu taggen sind, z. B. Bokeh:  
{{< image src="images/posts/vector-memes-bokeh.png" >}}

Fantastisch, denn so stoße ich auf längst vergessene Aufnahmen – etwa dieses großartige Foto von Baratunde aus 2017:

{{< image src="images/posts/vector-memes-baratunde.png" >}}

### Das wird überall auftauchen

Ich wette, dass diese Technik bald in jeder Foto-App steckt. Google Photos macht das vermutlich längst, aber so versteckt, dass es niemand bemerkt.

Dafür ist das Feature einfach zu gut. Hätte ich ein Produkt mit vielen Bildern, würde ich sofort eine Pipeline aufsetzen, um Einbettungen zu erzeugen – mal sehen, welche spannenden Funktionen das ermöglicht.

## DU KANNST DAS ALLES KOSTENLOS NUTZEN

Source: [harperreed/photo-similarity-search](https://github.com/harperreed/photo-similarity-search)

Schau es dir an.

Der Einstieg ist unkompliziert, wenn auch ein bisschen hacky, lol.

Ich würde conda oder Ähnliches nutzen, um die Umgebung sauber zu halten. Interface: Tailwind. Web: Flask. Code: Python.  
Euer Gastgeber: Harper Reed.

## Meine Challenge für dich!

Bau mir bitte eine App, mit der ich meine Fotobibliothek sauber katalogisieren kann – ohne alles irgendwo hochladen zu müssen. Eine schlanke Mac-App, der ich meinen Foto-Ordner zeige und „crawl das“ sage. Ich stelle mir jede Menge cooler Features vor:

- Llava/Moondream-Autobeschriftung  
- Schlüsselwörter / Tags  
- Vektor-Ähnlichkeit  
- usw.  

Das Ganze muss lokal laufen, nativ sein, simpel und effektiv. Vielleicht mit Lightroom, Capture One oder Apple Photos verzahnt.

Ich will das. Bau es. Lass uns mithilfe von KI all die großartigen Fotos wiederentdecken, die wir geschossen haben.

## Extra Credit: Lightroom-Preview-JPEG-Recovery

Mein Hacker-Kumpel Ivan war dabei, als ich das gebaut habe. Er erkannte sofort, wie viel man mit seiner Fotobibliothek entdecken kann. Seine eigentlichen Fotos liegen auf einer externen Platte, aber die Lightroom-Preview-Datei hatte er lokal. Er schrieb fix ein Skript, das Thumbnails und Metadaten aus der Preview zieht und extern speichert.

Dann lief der Image-Vector-Crawler – BÄM, ähnliche Bilder usw. Perfekt.

#### Lightroom-Fotos retten – zumindest die Thumbnails

Ivans Skript zum Extrahieren der Bilder aus der Preview ist superpraktisch. Wenn deine eigentliche Bibliothek futsch ist (kaputte HDD oder was auch immer) und du nur noch die *.lrprev*-Datei hast, kannst du damit wenigstens die Low-Res-Versionen retten.

Ein Skript, das man sich merken sollte.

Hier gibt’s das Teil: [LR Preview JPEG Extractor](https://github.com/ibips/lrprev-extract)

## Danke fürs Lesen.

Wie immer: [hmu](mailto:harper@modest.com) – lass uns abhängen. Ich denke viel über AI, E-Commerce, Fotos, Hi-Fi, Hacking und anderen Kram nach.

Wenn du in Chicago bist, komm vorbei!