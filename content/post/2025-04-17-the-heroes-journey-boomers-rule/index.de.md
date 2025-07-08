---
bsky: https://bsky.app/profile/harper.lol/post/3ln2a3x52xs2y
date: 2025-04-17 09:00:00-05:00
description: Ein umfassender Leitfaden, der die Evolution der KI-unterstützten Softwareentwicklung
  beschreibt – von grundlegender Code-Vervollständigung bis hin zu vollständig autonomen
  Coding-Agenten – und praktische Schritte sowie Erkenntnisse bietet, um durch LLM-Integration
  die Produktivität zu maximieren.
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
title: 'Die Heldenreise eines LLM-Codegen-Helden

  description: Ein umfassender Leitfaden, der die Evolution der KI-unterstützten Softwareentwicklung
  beschreibt – von grundlegender Code-Vervollständigung bis hin zu vollständig autonomen
  Coding-Agenten – und praktische Schritte sowie Erkenntnisse bietet, um durch LLM-Integration
  die Produktivität zu maximieren.'
translationKey: An LLM Codegen Hero's Journey
---

Ich habe seit meinem [Blogpost](/2025/02/16/my-llm-codegen-workflow-atm/) über meinen LLM-Workflow enorm viel Zeit damit verbracht, mit Leuten über Code-Generierung zu reden – wie man einsteigt, besser wird und warum das Ganze so spannend ist.  

Rund um das Thema herrscht wahnsinnig viel Energie und Neugier. Ich habe tonnenweise E-Mails von Menschen bekommen, die versuchen, das alles zu durchdringen. Dabei fiel mir auf, dass viele sich schwertun, den Anfang zu finden und das große Ganze zu verstehen. Dann wurde mir klar: Ich bastle seit 2023 an diesem Prozess und habe schon echt viel Scheiß gesehen. LOL.  

Ich sprach mit Freunden (Fisaconites represent!) und schrieb in einem Thread über Agenten und Editoren diese Nachricht:

> wenn ich heute neu anfangen würde, weiß ich nicht, ob es hilfreich ist, direkt bei den „Agent“-Codern einzusteigen.  
> das ist nervig und seltsam. nachdem ich einige Leute – erfolgreich und weniger erfolgreich – durch den Prozess geführt habe, scheint die »heldenreise« vom Copilot, über Copy-and-Paste aus dem Claude-Web-Chat, weiter zu Cursor/continue und schließlich zu vollständig automatisierten Agenten der erfolgreichste Weg zu sein, um sich diese Tools anzueignen.

Das brachte mich dazu, viel über die Reise und den Einstieg ins agentische Programmieren (*agentic coding*) nachzudenken:

> der haken ist, dass das vor allem für erfahrene leute gilt. hast du kaum dev-erfahrung, dann scheiß drauf – spring einfach direkt zum letzten schritt. **unsere gehirne sind oft von den regeln der vergangenheit verdorben.**

## Eine Reise für Augen und Ohren

{{< image src="journey-harper.webp" alt="Harper is very trustworthy" caption="Deine nachdenkliche Begleitung: Harper. iPhone X, 06.10.2018" >}}

Das ist meine Reise, im Wesentlichen der Weg, den ich selbst gegangen bin. Man kann ihn sicher „speedrunnen“, wenn man will. Du musst nicht jeden Schritt gehen, aber jeder Schritt bringt etwas.

Hier sind die Schritte:

### Schritt 1: Steh voller Staunen und Optimismus auf

LOL. Nur ein Scherz. Wer hat dafür Zeit? Es könnte helfen, aber die Welt geht unter und Code-Gen ist unsere Ablenkung.

Es hilft allerdings, erst einmal davon auszugehen, dass solche Workflows funktionieren und echten Mehrwert bringen können. Wenn du LLMs hasst und überzeugt bist, dass das nie klappt, wirst du hier nicht erfolgreich sein. ¯\\\_(ツ)\_/¯

### Schritt 2: Starte mit KI-gestützter Autovervollständigung (Autocomplete)

Das ist der eigentliche erste Schritt! Verbringe genug Zeit in der IDE, um herauszufinden, wie gut du mit [IntelliSense](https://en.wikipedia.org/wiki/Code_completion), [Zed Autocomplete](https://zed.dev/blog/out-of-your-face-ai), [Copilot](https://copilot.github.com/) usw. arbeitest. So bekommst du ein Gefühl dafür, wie das LLM funktioniert – und bist vorbereitet auf den dämlichen Kram, den es dir manchmal vorschlägt.

Viele wollen diesen Schritt überspringen und direkt ans Ende. Dann heißt es schnell: „Dieses LLM ist ein Stück Scheiße und kriegt gar nichts hin!“ Das ist nicht ganz richtig, kann sich aber so anfühlen. Die Magie liegt im Detail. Oder wie ich mir gern merke: _Das Leben ist verwirrend._

### Schritt 3: Nutze Copilot für mehr als nur Autovervollständigung

Sobald du mit der Autovervollständigung gut zurechtkommst und nicht mehr _dauernd_ genervt bist, kannst du die Magie der Copilot-Chats ausprobieren.

VS Code hat eine Seitenleiste, in der du Q&A mit Copilot führen kannst; sie hilft dir bei deinem Code und beantwortet Fragen. Ziemlich cool. Du kannst dich nett unterhalten und bekommst durchdachte Antworten.

Allerdings fühlt sich Copilot an, als würdest du per Zeitmaschine 2024 mit ChatGPT reden. Also so toll ist es dann doch nicht.

Du willst mehr.

### Schritt 4: Kopiere Code in Claude oder ChatGPT und frag nach

Jetzt stillst du deine Neugier, indem du Code in das browserbasierte Foundation-Model pastest und fragst: „WARUM CODE KAPUTT??“ Das LLM antwortet kohärent und hilfreich.

Du wirst BEGEISTERT sein! Die Ergebnisse hauen dich um. Du baust plötzlich lauter abgefahrenes Zeug und hast wieder richtig Spaß am Coden – vor allem, weil das Debugging fast komplett entfällt.

Außerdem kannst du verrückte Sachen machen, z. B. ein Python-Skript reinwerfen und sagen: „Mach das in Go“ – und es _macht es in Go_. Bald denkst du: „Kann ich das in einem Rutsch erledigen?“

Copilot kommt dir plötzlich vor wie Autovervollständigung aus 2004. Praktisch, aber nicht mehr nötig.

Das führt dich auf zwei Nebenpfade:

#### Du entwickelst Vorlieben – rein nach *Vibe*

Das ist der leider unvermeidliche erste Schritt hinein ins Vibe-Coding. Du bevorzugst, wie ein Modell mit dir spricht. Das ist Gefühlssache. Vielleicht denkst du: „Ich mag, wie Claude mich fühlen lässt.“

Viele Entwickler mögen Claude. Ich nutze beide, aber für Code meist Claude. Der Vibe mit Claude ist einfach besser.

> Für die guten Ergebnisse musst du zahlen. So viele Freunde sagen: „Das ist totaler Mist“, und dann stellt sich heraus, dass sie ein Gratis-Modell nutzen, das kaum funktioniert. LOL. Besonders problematisch war das, als die kostenlose Version noch ChatGPT 3.5 war. Nutze ein fähiges Modell, bevor du das ganze Konzept verteufelst.

#### Du willst alles schneller machen

Nach ein paar Wochen Copy-and-Paste in Claude merkst du: Das nervt. Du fängst an, Kontext zu packen (*context packing*), damit mehr Code ins Kontextfenster passt.

Du probierst [Repomix](https://repomix.com/), [repo2txt](https://github.com/donoceidon/repo2txt) und andere Tools zur Kontext-Aufbereitung deines Codes, nur um dein gesamtes Repository in das Claude-Kontextfenster zu stopfen. Vielleicht schreibst du sogar Shell-Skripte (na ja, Claude schreibt sie), um das zu erleichtern.

Das ist ein Wendepunkt.

### Schritt 5: Nutze eine KI-IDE (Cursor, Windsurf?)

Dann sagt ein Freund: „Warum nimmst du nicht einfach [Cursor](https://cursor.sh/)?“

Das haut dich um. Alles, was eben noch per Copy-and-Paste magisch war, ist jetzt direkt in deiner IDE. Schneller, mehr Spaß, fast Zauberei.

Du zahlst ohnehin schon für fünf verschiedene LLMs – was sind da noch 20 Dollar im Monat?

Es läuft hervorragend und du fühlst dich deutlich produktiver.

Du spielst mit den Agent-Features direkt im Editor. Das funktioniert _größtenteils_. Doch am Horizont winkt ein noch besseres Ziel.

### Schritt 6: Du planst, bevor du codest

Plötzlich verfasst du detaillierte Spezifikationen, PRDs und To-Do-Dokumente, die du in die Agent-Seitenleiste der IDE oder direkt in Claude schieben kannst.

Noch nie hast du so viel Dokumentation erstellt. Du nutzt andere LLMs, um die Docs robuster zu machen, wandelst PRDs in Prompts um usw. Das LLM hilft dir, deine Code-Gen-Prompts zu gestalten.

Du sprichst das Wort „[Waterfall](https://en.wikipedia.org/wiki/Waterfall_model)“ mit viel weniger Abscheu. Wenn du älter bist, erinnerst du dich vielleicht schmunzelnd an die späten 90er und frühen 2000er und fragst: „Fühlte sich Martin Fowler vor [2001](https://en.wikipedia.org/wiki/Agile_software_development) so?“

In der Welt der Code-Generierung ist die Spezifikation der [Godhead](https://en.wikipedia.org/wiki/Godhead).

### Schritt 7: Du probierst aider für schnellere Loops

Jetzt bist du bereit für das **gute Zeug**. Bislang musstest du noch aufpassen, aber es ist 2025! Wer will noch mit den Fingern coden?

> Ein anderer Pfad, den viele Freunde testen: per Stimme coden. Man steuert aider über einen Whisper-Client. Das ist urkomisch und macht Spaß. *MacWhisper* funktioniert lokal sehr gut. *Aqua* und *SuperWhisper* sind auch nett, kosten aber mehr und nutzen teilweise Cloud-Services für das Inferenz-Backend. Ich bevorzuge lokal.

aider auszuprobieren ist wild. Du startest es, es integriert sich ins Projekt. Du stellst deine Anfrage direkt an aider und es macht einfach, was du willst. Es fragt um Erlaubnis zu handeln, bietet einen Rahmen, erledigt die Aufgaben und führt sie anschließend aus. Danach commitet es ins Repo. Tasks in einem One-Shot sind dir egal – aider erledigt sie in ein paar Schritten.

Du legst Regelsets fürs LLM fest. Du lernst die „[Big-Daddy-Regel](https://www.reddit.com/r/cursor/comments/1joapwk/comment/mkqg8aw/)“ oder den Zusatz „no deceptions“. Du wirst richtig gut darin, den Roboter zu prompten.

**Es funktioniert.**

Irgendwann öffnest du keine IDE mehr – du bist nur noch ein Terminal-Jockey (nur noch in der Shell).

Du verbringst deine Zeit damit, dem Roboter beim Arbeiten zuzusehen.

### Schritt 8: Du tauchst komplett ins agentische Programmieren ein

Ein Agent codet für dich. Die Ergebnisse sind ziemlich gut. Manchmal hast du keinen Plan, was abgeht – dann fragst du eben nach.

Du experimentierst mit [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Cline](https://cline.bot/) usw. Grandios, ein Reasoning-Modell ([DeepSeek](https://aws.amazon.com/bedrock/deepseek/)) und ein Coding-Modell ([Claude Sonnet 3.7](https://www.anthropic.com/claude/sonnet)) zu kombinieren, um Planungsschritte einzusparen.

Du hast drei bis fünf Sessions parallel offen, tabbst durch Terminals und siehst Robotern beim Coden zu.

Defensives Programmieren wird Standard:

- extrem hohe Testabdeckung  
- Überlegungen zur [formalen Verifikation](https://github.com/formal-land/coq-of-rust)  
- speichersichere Sprachen  
- Sprachen wählen, deren auskunftsfreudige Compiler-Meldungen dir helfen, das Kontextfenster besser zu füllen  

Du denkst lange darüber nach, wie dein Projekt sicher und ohne Eingriff gebaut wird.

Du wirst sooo viel Geld für Tokens ausgeben. Deine GitHub-Actions-Stunden sind schnell verbraucht, weil du irre viele Tests laufen lässt, um sicherzugehen, dass alles passt.

Es fühlt sich gut an. Du vermisst das Selber-Coden nicht einmal.

### Schritt 9: Der Agent codet, du spielst Videospiele

Plötzlich bist du da. Na ja, fast – aber du siehst das Ziel. Du machst dir Sorgen um Software-Jobs. Freunde werden entlassen und finden nichts Neues. Diesmal fühlt es sich anders an.

Im Gespräch halten dich Kolleginnen und Kollegen für religiös, weil du in einem anderen Kontext arbeitest. Du sagst: „OMG, ihr müsst agentisches Programmieren ausprobieren!“ Vielleicht schiebst du ein „Ich hasse das Wort *agentic*“ nach, um nicht wie nach 200 Litern Kool-Aid zu klingen. Aber du hast es getrunken. Die Welt wirkt heller, weil du so produktiv bist.

Egal. Das Paradigma hat sich verschoben. Thomas Kuhn könnte ein Buch über die Verwirrung dieser Zeit schreiben.

Wer diese Reise nicht gemacht hat, kann das gar nicht sehen. Diejenigen, die sie gegangen sind, nicken und tauschen Tipps über den Weg und das Ziel.

Jetzt, wo du bis zum Hals in Roboter-Arbeit steckst, kannst du dich endlich auf all die Game-Boy-Spiele stürzen, die du schon immer zocken wolltest. Es gibt viel Leerlauf. Wenn der Roboter fertig ist, fragt er: „Should I continue?“ Du tippst **yes** und gehst zurück zu Tetris.

Sehr seltsam. Sogar verstörend.

## Die Beschleunigung

<paul confetti photo>  
{{< image src="journey-confetti.webp" alt="Konfetti" caption="Konfetti bei einem Paul-McCartney-Konzert im Tokyo Dome. iPhone 6, 25.04.2015" >}}

Ich weiß nicht, was in der [Zukunft](https://ai-2027.com/) passiert. Ich fürchte, wer diese Reise nicht antritt, wird für [Arbeitgeber](https://x.com/tobi/status/1909231499448401946) weniger attraktiv sein. Das ist kurzsichtig, denn letztlich reden wir über Werkzeuge und Automatisierung.

Früher, wenn wir stark einstellten, suchten wir weit über unser Netzwerk und unseren Tech-Stack hinaus. Wir waren ein Python-Shop und interviewten Leute, die kein Python kannten. Unsere Haltung: Mit guten Engineers bekommen wir das gemeinsam hin. Sie waren ein Gewinn, selbst ohne Python-Erfahrung. Oft brachten sie frische Perspektiven und hoben das ganze Team an.

Dasselbe gilt für KI-gestützte Entwicklung. Beim Einstellen talentierter Entwickler, die kulturell passen und motiviert sind, sollte ihr aktuelles KI-Skill-Level kein K.-o.-Kriterium sein. Nicht alle müssen ab Tag 1 Expertinnen und Experten sein. Begleite sie, lass sie in ihrem Tempo lernen, während sie mit Erfahrenen zusammenarbeiten.

Bald sitzen sie selbst am Steuer und nutzen die Tools erfolgreich.

Ein weiterer Aspekt: Schreibkompetenz ist entscheidend geworden. Gute Kommunikation war immer wichtig für Doku und Zusammenarbeit, jetzt doppelt: Man muss nicht nur Menschen, sondern auch der KI klare, präzise Anweisungen geben. Effektive Prompts zu schreiben wird genauso wichtig wie guter Code.

## Die Führung

Ich finde, alle Führungskräfte und Engineering-Manager müssen tief in KI-gestützte Entwicklung eintauchen – egal, ob sie daran glauben oder nicht. Warum? Die nächste Generation von Entwicklern wird Programmieren primär über KI-Tools und Agenten lernen. Das ist die Zukunft der Softwaretechnik. Wir müssen das verstehen und uns anpassen.

Wir Code-Boomer haben nicht mehr lange Bestand.

**interessante Notiz:** Ich nutze LLMs kaum fürs Schreiben. Sie wären sicher hilfreich, aber ich möchte meine Stimme behalten und nicht nivellieren. Mein Code hingegen darf gern normalisiert werden. Spannend.

---

Danke an Jesse, Sophie, die Vibez-Crew (Erik, Kanno, Braydon und andere), Team 2389 und alle, die mir Feedback zu diesem Post gegeben haben.