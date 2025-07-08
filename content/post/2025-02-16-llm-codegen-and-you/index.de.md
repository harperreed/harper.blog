---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: Eine detaillierte Schritt-für-Schritt-Anleitung meines aktuellen Workflows
  für den Einsatz von LLMs zur Softwareentwicklung, vom Brainstorming über die Planung
  bis zur Umsetzung.
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
title: Mein derzeitiger LLM-Codegen-Workflow
translationKey: My LLM codegen workflow atm
---

_tl;dr: Erst eine Spezifikation brainstormen, dann einen Plan schmieden und anschließend in klar abgegrenzten Iterationen mit LLM-Codegen umsetzen. Danach passiert Magie. ✩₊˚.⋆☾⋆⁺₊✧_

Ich habe in letzter Zeit wahnsinnig viele kleine Produkte mithilfe von LLMs gebaut. Das macht Spaß und ist nützlich. Allerdings gibt es Fallstricke, die enorm viel Zeit fressen können. Vor einer Weile fragte mich ein Freund, wie ich LLMs zum Programmieren nutze. Ich dachte: „Oh boy, wie viel Zeit hast du?!“ – und so entstand dieser Beitrag.

(P.S. Wenn du zu den KI-Skeptiker*innen gehörst – einfach bis ganz nach unten scrollen.)

Ich spreche mit vielen Entwickler­freund*innen darüber, und wir alle verfolgen einen ähnlichen Ansatz, nur mit kleinen Feinschliffen hier und da.

Hier ist mein Ablauf. Er basiert auf meiner eigenen Arbeit, Gesprächen mit Freund*innen (Danke [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki) und [Erik](https://thinks.lol/)) sowie auf zahlreichen Best Practices aus den berüchtigten Ecken des Internets – den [bad](https://news.ycombinator.com/) [places](https://twitter.com).

Das funktioniert **JETZT** hervorragend – in zwei Wochen vielleicht gar nicht mehr oder doppelt so gut. ¯\\\_(ツ)\_/¯

## Los geht’s

{{< image src="llm-coding-robot.webp" alt="Juggalo-Roboter" caption="Ich finde diese AI-Bilder immer ein bisschen suspekt. Sagt Hallo zu meinem Juggalo-Coding-Roboter-Engel!" >}}

Bei der Entwicklung gibt es für mich im Wesentlichen zwei Szenarien:

- Greenfield-Code  
- modernisierten Legacy-Code

Ich zeige dir meinen Prozess für beide Wege.

## Greenfield

Für Greenfield-Entwicklung hat sich Folgendes bewährt: ein robuster Planungs- und Dokumentationsansatz, der die Umsetzung in kleinen Schritten erleichtert.

{{< image src="greenfield.jpg" alt="Grünes Feld" caption="Rein technisch gesehen liegt rechts ein grünes Feld. Leica Q, 14.05.2016" >}}

### Schritt 1: Idee schärfen

Nutze ein Konversations-LLM, um die Idee auszuarbeiten (ich verwende ChatGPT 4o/o3):

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

Am Ende des Brainstormings (das Gespräch kommt meist von selbst zu einem Abschluss):

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

Das Ergebnis ist eine solide, klar strukturierte Spezifikation, die du direkt als `spec.md` im Repo speichern kannst.

> Diese Spezifikation kannst du vielfältig nutzen. Wir setzen sie hier fürs Codegen ein, ich habe sie aber auch schon verwendet, um mithilfe eines logikorientierten Modells Schwachstellen aufzudecken (immer tiefer bohren!), ein Whitepaper zu verfassen oder ein Geschäftsmodell abzuleiten. Stecke sie in ein Recherche-LLM und du erhältst ein 10 000 Wörter starkes Begleitdokument.

### Schritt 2: Planung

Nimm die Spezifikation und füttere damit ein ordentliches logikorientiertes Modell (`o1*`, `o3*`, `r1`):

_(TDD-Prompt)_

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

_(Non-TDD-Prompt)_

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

Das Modell liefert einen Prompt-Fahrplan, den du mit Aider, Cursor & Co. abarbeiten kannst. Ich speichere ihn als `prompt_plan.md` im Repo.

Danach lasse ich mir eine `todo.md` erzeugen:

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

Speichere sie als `todo.md` im Repo. Dein Codegen-Tool kann die Punkte während der Arbeit abhaken – das hilft, den Überblick zu behalten.

#### Yay. Plan!

Jetzt hast du einen soliden Plan plus Doku, um dein Projekt umzusetzen. Das Ganze dauert vielleicht **15 Minuten** – ziemlich verrückt, ehrlich gesagt.

### Schritt 3: Umsetzung

Es gibt unzählige Optionen; wie gut es läuft, hängt stark von Schritt 2 ab.

Ich habe den Workflow mit [GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude Engineer](https://github.com/Doriandarko/claude-engineer), [sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [claude.ai](https://claude.ai) usw. genutzt. Klappt überall ganz gut.

Meine Favoriten sind **reiner** Claude und Aider:

### Claude

Im Prinzip pair-programmiere ich mit [claude.ai](https://claude.ai) und reiche die Prompts nacheinander ein. Das Hin und Her nervt manchmal, funktioniert aber.

Ich kümmere mich ums Grundgerüst (Boilerplate, Tooling usw.), damit Claude nicht reflexhaft React-Code ausspuckt.

Wenn etwas hängt, nehme ich [repomix](https://github.com/yamadashy/repomix) zur Hilfe (mehr dazu später).

Workflow:

- Repo aufsetzen (`uv init`, `cargo init`, …)  
- Prompt bei Claude einwerfen  
- Code von claude.ai kopieren und in der IDE speichern  
- Code ausführen, Tests laufen lassen  
- …  
- läuft alles → nächster Prompt  
- läuft es nicht → repomix nutzen, um den Code an Claude zu schicken und zu debuggen  
- und immer so weiter ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) ist spaßig und etwas eigen. Passt super zu den Ergebnissen aus Schritt 2 – mit wenig Aufwand kommst du sehr weit.

Tests sind mit Aider besonders angenehm, weil du dich nahezu ohne manuelles Eingreifen zurücklehnen kannst: Aider führt die Test-Suite aus und debuggt selbst.

Workflow:

- Repo aufsetzen  
- Aider starten  
- Prompt einfügen  
- Aider beim Tanzen zusehen ♪┏(・o･)┛♪  
- Aider führt Tests aus oder du startest die App  
- bei Erfolg → nächster Prompt  
- bei Fehlern → Q&A mit Aider, bis es passt  
- und immer so weiter ✩₊˚.⋆☾⋆⁺₊✧

> Nebenbei: Aider betreibt hervorragendes Benchmarking neuer Modelle für Codegen in seinen [LLM-Leaderboards](https://aider.chat/docs/leaderboards/). Eine super Ressource, um zu sehen, wie effektiv neue Modelle sind.

### Ergebnisse

Ich habe mit diesem Workflow unzählige Dinge gebaut: Skripte, Expo-Apps, Rust-CLI-Tools und mehr – über verschiedenste Sprachen und Kontexte hinweg.

Wenn du ein kleines oder großes Projekt aufschiebst, probier’s aus – du wirst staunen, wie schnell du vorankommst.

Meine Hack-To-Do-Liste ist leer, weil ich alles umgesetzt habe. Mir fallen ständig neue Ideen ein, die ich dann mal eben nebenbei – etwa beim Filmschauen – umsetze. Zum ersten Mal seit Jahren befasse ich mich wieder mit neuen Sprachen und Tools. Das erweitert meinen Programmier-Horizont enorm.

## Non-Greenfield: Inkrementell iterieren

Manchmal ist kein Greenfield möglich, sondern man muss auf einer bestehenden Codebasis weiterarbeiten.

{{< image src="brownfield.jpg" alt="Brownfield-Gelände" caption="Das ist kein Greenfield. Ein Foto aus der Kamera meines Großvaters – irgendwo in Uganda in den 60ern" >}}

Hier nutze ich eine leicht andere Methode: Planung pro Aufgabe, nicht fürs ganze Projekt.

### Kontext holen

Alle, die tief in AI-Dev stecken, haben ihr eigenes Tool dafür – du brauchst etwas, das deinen Quellcode zügig ins LLM einspeist.

Ich verwende aktuell [repomix](https://github.com/yamadashy/repomix) über eine Task-Sammlung in `~/.config/mise/config.toml`.

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

Ich erzeuge eine `output.txt`, die den Code-Kontext enthält. Wenn sie zu groß wird, passe ich die Ignore-Pattern an.

> Ein großer Vorteil von `mise` ist, dass Tasks im `.mise.toml` des Arbeitsverzeichnisses überschrieben werden können. Ich kann ein anderes Tool nutzen, um den Code zu packen – solange es eine `output.txt` erzeugt, funktionieren meine LLM-Tasks. Das ist praktisch, wenn Codebasen sehr unterschiedlich sind.

Danach füttere ich `output.txt` an den [LLM](https://github.com/simonw/LLM)-Befehl, um verschiedene Transformationen zu erzeugen und als Markdown abzulegen.

Im Kern läuft z. B. `cat output.txt | LLM -t readme-gen > README.md` oder  
`cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md`. Nicht kompliziert – der `LLM`-Befehl übernimmt die eigentliche Arbeit (Modelle, Keys, Prompt-Templates).

Beispiel-Workflow für fehlende Tests:

#### Claude

- Ins Projektverzeichnis wechseln  
- `mise run LLM:generate_missing_tests` ausführen  
- die erzeugte Datei `missing-tests.md` ansehen  
- kompletten Code-Kontext kopieren: `mise run LLM:copy_buffer_bundle`  
- Kontext + ersten Punkt „fehlende Tests“ in Claude einfügen  
- generierten Code in der IDE übernehmen  
- Tests ausführen  
- und immer so weiter ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- Ins Projektverzeichnis wechseln (immer auf einem neuen Branch für Aider-Arbeit)  
- Aider starten  
- `mise run LLM:generate_missing_tests` ausführen  
- `missing-tests.md` ansehen  
- ersten Punkt „fehlende Tests“ in Aider einfügen  
- Aider beim Tanzen zusehen ♪┏(・o･)┛♪  
- Tests ausführen  
- und immer so weiter ✩₊˚.⋆☾⋆⁺₊✧

So lässt sich eine große Codebasis Stück für Stück verbessern.

### Prompt-Magie

Diese schnellen Hacks helfen, Projekte robuster zu machen. Hier ein paar meiner Prompts:

#### Code-Review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply before writing the code review. Review every part, and don't hallucinate.
```

#### GitHub-Issues

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Fehlende Tests

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

Diese Prompts sind schon etwas „old and busted“ (Boomer-Prompts). Wenn du Ideen hast, wie man sie aufpolieren kann – sag gern Bescheid.

## Skifahren ᨒ↟ 𖠰ᨒ↟ 𖠰

Wenn ich den Prozess erkläre, sage ich oft: „Man muss aggressiv den Überblick behalten, sonst gerät man schnell *over my skis* – sprich: man übernimmt sich.“

Warum auch immer: Ich sage ständig *over my skis*, wenn es um LLMs geht. Vielleicht, weil alles butterweich läuft und man plötzlich denkt: „WTF geht hier ab?!“ – und schon stürzt man die Klippe runter.

Ein **Planungsschritt** (siehe Greenfield) hilft enorm. Tests sind ebenfalls Gold wert – besonders beim wilden Aider-Coding.

Trotzdem gerate ich oft *over my skis*. Eine kurze Pause oder ein Spaziergang wirken Wunder.

> Wir bitten das LLM häufig, völlig absurde Dinge in unseren eigentlich nüchternen Code einzubauen. Zum Beispiel haben wir es gebeten, eine Lore-Datei anzulegen und sie dann in der Benutzeroberfläche zu referenzieren – für ein Python-CLI-Tool. Plötzlich gibt es Lore, glitchige Interfaces usw. Nur um deine Cloud-Functions oder deine To-Do-Liste zu verwalten. The sky is the limit.

## Ich bin so einsam (｡•́︿•̀｡)

Mein größter Kritikpunkt: Das Ganze ist meist Single-Player-Modus.

Ich habe allein, im Pair und im Team gearbeitet – mit Leuten ist es immer besser. Diese Workflows sind im Team schwer: Bots kollidieren, Merges sind hässlich, Kontext ist kompliziert.

Ich wünsche mir dringend, dass jemand das in ein echtes Multiplayer-Game verwandelt. Riesige Chance – legt los!

## ⴵ Zeit ⴵ

All dieses Codegen hat meine Output-Menge extrem gesteigert. Nebenwirkung: viel „Downtime“, während das LLM Tokens verbrennt.

{{< image src="apple-print-shop-printing.png" alt="Druckvorgang" caption="Ich erinnere mich daran, als wäre es gestern gewesen" >}}

Ich nutze die Wartezeit inzwischen so:

- Ich starte den Brainstorming-Prozess für ein anderes Projekt  
- Ich höre Schallplatten  
- Ich spiele [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/)  
- Ich quatsche mit Freund*innen und Robotern

So produktiv war ich beim Coden noch nie.

## Haterade ╭∩╮( •̀_•́ )╭∩╮

Viele Freund*innen sagen: „Fuck LLMs. Die können doch nix.“ Skepsis ist okay. Gründe zum Ablehnen gibt es genug. Meine größte Sorge: Stromverbrauch und Umweltbelastung. Aber … der Code muss fließen. Right? *seufz*

Mein Rat lautet nicht, deine Meinung zu ändern, sondern lediglich Ethan Mollicks Buch [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/) zu lesen.

Es zeigt die Vorteile ohne Tech-Bro-Geschwafel. Hat schon viele gute, nuancierte Gespräche ausgelöst – sehr empfehlenswert.

Bist du skeptisch, aber doch interessiert? Melde dich gern, vielleicht bauen wir zusammen was.

_Danke an [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com) und [Erik](https://thinks.lol/) fürs Gegenlesen dieses Beitrags und die Vorschläge. Ich weiß das zu schätzen._