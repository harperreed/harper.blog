---
date: 2025-04-10
description: Eine Untersuchung, wie KI traditionelle Entwicklungsmethoden zu schnellen,
  15-minütigen Wasserfallzyklen beschleunigt und dabei Arbeitsabläufe in der Softwareentwicklung
  sowie Teamdynamiken verändert.
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
title: 'Wasserfall in 15 Minuten oder Geld zurück

  description: Eine Untersuchung, wie KI traditionelle Entwicklungsmethoden zu schnellen,
  15-minütigen Wasserfallzyklen beschleunigt und dabei Arbeitsabläufe in der Softwareentwicklung
  sowie Teamdynamiken verändert.'
translationKey: Waterfall in 15 Minutes or Your Money Back
---

Ich hatte neulich ein Gespräch mit einem Freund, das als lockerer Austausch begann und sich rasch zu einer tiefen Diskussion über KI-unterstütztes Programmieren entwickelte – darüber, wie das unsere Workflows, Teams und unser Gefühl für „Craft“ verändert. Wir streiften alles – vom Neuschreiben alter Codebasen bis hin zu der Frage, wie automatisierte Testabdeckung die Art des Programmierens verändert.

Ich hab das Granola-Transkript einfach in o1-pro gekippt und die KI gebeten, daraus diesen Blogpost zu bauen. Gar nicht schlecht – trifft meine Ansichten ziemlich gut.

Ich habe den Entwurf ein paar Freunden geschickt, und alle wollten ihn sofort weiterleiten. Heißt: Ich muss wohl veröffentlichen. Also los!

> this is a good reminder that if you get an email from someone and the writing is perfect and has no affectation - an AI probably wrote it. lol.  
> *Zur Erinnerung: Wenn du eine E-Mail bekommst, die sprachlich perfekt und völlig ohne Eigenheiten ist – dann hat sie wahrscheinlich eine KI geschrieben. lol.*

---

## Waterfall in 15 Minuten – oder Geld zurück

### The New Normal: „Warum ist Codequalität überhaupt wichtig?“

Jahrelang haben wir über Code als Handwerk gesprochen – darüber, wie wir in diesen kostbaren Flow-Zustand kommen, ein Stück Logik meißeln und mit handgemachten Bugfixes siegreich wieder auftauchen. Doch ein neues Paradigma schleicht sich ein: Code-Generatoren – sprich, große Sprachmodelle (Large Language Models, LLMs) – können Features inzwischen in wenigen Minuten raushauen.

Einige sind von diesem Tempo verunsichert, weil es die traditionellen Clean-Code-Standards auf den Kopf stellt. Plötzlich geht es bei robusten Test-Suites oder sogar testgetriebener Entwicklung eher darum, die KI-Agenten ihren eigenen Output verifizieren zu lassen, statt jede Zeile methodisch zu prüfen.

Wird die Codequalität abstürzen? Vielleicht. Gleichzeitig beobachten wir einen Trend zu extrem defensivem Programmieren – statische Analysen, Formale Verifikation und Testabdeckung überall –, damit wir Fehler eines KI-Agenten blitzschnell entdecken. Erstklassige CI/CD-Pipelines und strenge Prüfungen waren noch nie so nötig wie heute.

---

### Waterfall in 15 Minuten

{{< image src="waterfall.webp" alt="Waterfall" caption="Island hat viele Wasserfälle. Leica Q, 30.09.2016" >}}

Früher stellten wir „Waterfall vs. Agile“ als moralische Gegensätze dar, wobei Agile der einzig wahre Weg sein sollte. Ironischerweise drängt uns die Code-Generierung jetzt in Micro-Waterfall-Zyklen: Wir definieren sorgfältig eine Spezifikation (weil die KI Klarheit braucht), klicken auf „Go“, warten auf den generierten Code und prüfen ihn. Das fühlt sich zwar iterativ an, de facto läuft es aber so: erst ein Block Planung, dann ein Block Umsetzung, dann ein Block Review – Waterfall in 15 Minuten.

Der eigentliche Zauber? Du kannst mehrere KI-Agenten gleichzeitig starten. Während ein Agent ein Feature baut, erstellt ein zweiter die Doku und ein dritter kümmert sich um die Testabdeckung. Das ist nicht das alte lineare Waterfall-Modell – das ist Parallelität hoch 10.

---

### Die bevorstehende Veränderung der Teamkultur

Wenn du ein Engineering-Team leitest, hörst du von oben sicher: „Wie können wir KI nutzen, um produktiver zu werden?“ Gleichzeitig merkst du, dass dein Team unterschiedlich begeistert ist. Einige sind voll dabei – bauen komplette Features ausschließlich per promptbasiertem Programmieren –, andere verteidigen ihr Selbstverständnis als Handwerker.

Was meiner Erfahrung nach funktioniert:

1. **Kleine Pilotprojekte starten**  
   Such dir ein internes Tool oder ein Nebenprojekt ohne großes Produktionsrisiko und lass ein paar neugierige Entwickler:innen dort mit KI experimentieren. Lass sie ruhig Dinge kaputtmachen, schauen, was passiert, wenn man dem Modell zu viel Vertrauen schenkt und beobachten, wie sich Best Practices herausbilden.

2. **Leute rotieren lassen**  
   Ein dediziertes, promptgesteuertes Nebenprojekt ermöglicht es, Teammitglieder für ein bis zwei Wochen komplett in dieses neue Umfeld eintauchen zu lassen, dort voneinander zu lernen und die Erkenntnisse anschließend in die Haupt-Codebasis zurückzubringen.

3. **Dokumentation ernst nehmen**  
   KI-Agenten brauchen extrem klare Spezifikationen. Code-Generierung ist billig, doch ein LLM richtig zu steuern kostet sorgfältige Planung. Pack also die besten Spezifikationen und Architektur-Docs, die du je geschrieben hast, in ein gemeinsames Repository. Du wirst dir danken, wenn Leute auf das Projekt wechseln oder es wieder verlassen.

---

### Warum der Flow-Zustand vielleicht überschätzt wird

Eine überraschende Erkenntnis: Viele von uns sind wegen dieses Flow-Zustands zum Programmieren gekommen – dem tiefen Eintauchen in die „Zone“. KI-gestütztes Programmieren liefert den nicht immer. Du verbringst vielleicht eine Stunde damit, Prompts aufzusetzen, lässt die KI im Hintergrund arbeiten und schaust gelegentlich vorbei, um abzunicken oder nachzusteuern.

Für manche ist das irritierend. Andere – besonders jene mit Kindern oder zig parallelen Aufgaben – finden es befreiend. Wenn du den Kontext wechseln kannst, kurz die Ergebnisse der KI prüfst, ins echte Leben springst und dann zu funktionierendem Code zurückkehrst, merkst du: Produktivität geht auch ohne stundenlange Konzentrationsblöcke.

---

### Bedeutet das „Peak Programmer“?

Es heißt, sobald KI Code generieren kann, hätten wir den Punkt „Peak Programmer“ erreicht – bald bräuchten wir weniger Entwickler:innen. Für einfache Features oder API-Anbindungen mag das teilweise stimmen. Gleichzeitig entstehen neue Komplexitäten: Security, Compliance, Testabdeckung, Architektur.

Der Unterschied? Strategische Entwickler:innen werden aufblühen – diejenigen, die mehrere KI-Tools orchestrieren, die Codequalität im Blick behalten und Systeme entwerfen, die skalieren. Sie sind Teil Product-Manager, Teil Architekt, Teil QA und Teil Developer. Sie formulieren die Prompts, definieren die Tests, halten die Qualität hoch und kümmern sich um all die Randfälle, die ein LLM übersieht.

---

### Profi-Tipps von der Front

Ein paar Dinge, die ich schmerzhaft gelernt habe:

1. **Erst manuell starten, dann die KI einschalten**  
   Bei iOS-Apps das Projekt zuerst in Xcode initialisieren, damit die automatisch erzeugten Dateien die KI nicht verwirren. Danach darf die KI den Rest ausfüllen.

2. **Kurze, klare Prompts schlagen manchmal lange Anweisungen**  
   Merkwürdigerweise reicht „make code better“ bei manchen LLMs fast so gut wie ein seitenlanger Prompt. Probier’s aus – manche Modelle reagieren besser auf weniger Vorgaben.

3. **Checkpoint-Workflow verwenden**  
   Häufig committen, selbst wenn es nur  
   `git commit -m "It passed the tests, I guess!"`  
   ist. KI kann alles so schnell zerlegen, wie sie es repariert. Viele Commits bedeuten einfache Rollbacks.

4. **Die KI daran hindern, Grundlegendes überzutesten**  
   KI testet gern alles, sogar ob eine `for`-Schleife noch schleift. Bleib wachsam, entferne sinnlose Tests und halte die Pipeline schlank.

5. **Wirklich alles dokumentieren**  
   Lass die KI ausführliche „Implementation Guides“ erstellen. Diese Guides helfen nicht nur dir, sondern auch der KI selbst bei späteren Durchläufen.

---

### Schlussgedanken

{{< image src="waterfall-road.webp" alt="Road to the future" caption="Straße in die Zukunft. Colorado ist flach. Leica Q, 14.05.2016" >}}

Unsere Branche verändert sich schneller als je zuvor. Manche liebgewonnene Annahmen – etwa die Wichtigkeit des Flow-Zustands oder große Feiern rund um sorgfältig handgeschriebene Features – werden bald nostalgisch wirken. Unsere Kreativität verlieren wir nicht; sie verlagert sich auf strategische Orchestrierung: zu wissen, was gebaut werden muss, wie man es beschreibt und wie man verhindert, dass alles in ein ausgewachsenes Chaos kippt.

Am Ende zeigt sich vielleicht: Dein Produkt gewinnt nicht, weil du massenhaft Code schreibst, sondern weil du ein Erlebnis gestaltest, das Menschen lieben. Wenn wir an einem Wochenende zehn Instagram-Klone hochziehen können, entscheidet nicht der eleganteste Code, sondern was bei den Leuten ankommt – eine Frage von Design und Produkt, nicht nur von Engineering.

Willkommen also im neuen Waterfall – erledigt in 15-Minuten-Zyklen, mit einer unermüdlichen Junior-Entwicklerin oder einem unermüdlichen Junior-Entwickler an deiner Seite und einer Code-Pipeline im Hyperdrive. Es ist schräg, wunderbar und gelegentlich beängstigend. Und wir werden alle lernen müssen, diesen Tanz zu tanzen.

---

*Was für eine verrückte Welt. Ich glaube, es wird weiter seltsam bleiben. Also: Packen wir’s an.*