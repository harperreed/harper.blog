---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description: Ein ausführlicher Leitfaden zur Verwendung des KI-Assistenten Claude
  Code für die Softwareentwicklung, einschließlich Workflow-Tipps, Testpraktiken und
  praktischer Beispiele aus realen Projekten. Behandelt defensive Programmierstrategien,
  TDD und die Implementierung im Team.
draft: false
generateSocialImage: true
slug: basic-claude-code
tags:
- ai
- coding
- claude
- development
- automation
- testing
- tdd
- programming
title: 'Grundlegender Claude Code

  description: Ein ausführlicher Leitfaden zur Verwendung des KI-Assistenten Claude
  Code für die Softwareentwicklung, einschließlich Workflow-Tipps, Testpraktiken und
  praktischer Beispiele aus realen Projekten. Behandelt defensive Programmierstrategien,
  TDD und die Implementierung im Team.'
translationKey: Basic Claude Code
---

Ich steh’ total auf dieses „Agentic Coding“, also agentenhaftes Programmieren. Es ist auf so vielen Ebenen unglaublich faszinierend.

Seit ich [diesen ursprünglichen Blogpost](/2025/02/16/my-llm-codegen-workflow-atm/) geschrieben habe, ist in Claude-Land einiges passiert:

- Claude Code  
- MCP  
- usw.

Ich habe Hunderte (wat) E-Mails von Leuten bekommen, die mir ihre Workflows schildern und erzählen, wie sie mit meinem Ansatz vorankommen. Ich habe auf ein paar Konferenzen gesprochen und einige Kurse über Codegen gegeben. Dabei habe ich gelernt, dass Computer „codegen“ unbedingt zu „codeine“ korrigieren wollen – wer hätte das gedacht!

{{< image src="codegen.png"  >}}

Neulich plauderte ich mit einer [Freundin](https://www.elidedbranches.com/) darüber, dass wir **alle total gefickt sind** und **die KI uns die Jobs klauen wird** (mehr dazu in einem späteren Post). Sie meinte nur: „Schreib doch mal was zu Claude Code.“

Also los.

Claude Code erschien acht Tage nach meinem ursprünglichen Workflow-Post und machte, wie von mir prophezeit, einen Großteil davon hinfällig. Seitdem bin ich von Aider zu Claude Code gewechselt und habe seitdem nicht mehr zurückgeblickt. Aider mag ich immer noch – es hat sein eigenes Einsatzgebiet –, aber gerade ist Claude Code einfach nützlicher.

Claude Code ist sackstark – und verdammt viel teurer.

Mein Workflow sieht im Grunde immer noch so aus:

- Ich chatte mit `gpt-4o`, um die Idee zu schärfen.  
- Dann lasse ich das beste Reasoning-Modell, das ich finde, die Spezifikation erzeugen – aktuell `o1-pro` oder `o3` (ist `o1-pro` wirklich besser als `o3`, oder fühlt es sich nur so an, weil es länger rechnet?).  
- Anschließend lasse ich dasselbe Modell die Prompts schreiben. Ein LLM Prompts generieren zu lassen, ist ein genialer Hack – und macht Boomers wütend.  
- `spec.md` und `prompt_plan.md` landen im Projekt-Root.  
- Danach tippe ich in Claude Code:

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

- Das Geniale: Claude liest den Prompt-Plan, sucht alles, was noch offen ist, erledigt die nächste Aufgabe, committet in Git, aktualisiert den Plan und fragt dann, ob es weitergehen soll. 🤌  
- Dann chille ich einfach, tippe bei Claude `yes` – und lasse es machen. Zwischendurch fragt es nach Feedback und es passiert Magie.  
- Viel Zeit für Cookie Clicker.

Das läuft richtig gut. Ein paar eingebettete Superkräfte heben den Prozess auf ein neues Level.

## Defensive Coding

### Testing

Test-Driven Development (TDD) ist Pflicht. Bau dir unbedingt eine solide TDD-Praxis auf.

Früher war ich überzeugter TDD-Hater. Ich konnte es nicht und fand es Zeitverschwendung – komplett falsch, lol. In den letzten Jahrzehnten haben wir zwar massig Tests in unsere Projekte gepackt, aber oft erst nach der eigentlichen Arbeit. Für Menschen okay.

Für *Roboter* ist das SCHLECHT.

Die Roboter LIEBEN TDD. Wirklich. Sie saugen das auf.

Erst lässt du den Roboter die Tests und Mocks bauen, im nächsten Prompt ersetzt du den Mock durch echte Implementierung – und der Roboter flippt vor Freude aus. Das ist das effektivste Gegenmittel gegen Halluzinationen und LLM-Scope-Drift, das ich kenne. Es hält den Roboter sauber auf Kurs.

### Linting

Ich bin ein riesiger Linting-Fan. Ruff ist super, Biome cool, Clippy macht Spaß (und der Name erst).

Aus irgendeinem Grund stehen *Roboter* total auf einen guten Linter.

Wenn ständig ein Linter läuft, bleiben Bugs fern und der Code ist wartbarer. Du weißt das eh.

Pack noch einen guten Formatter dazu und alles glänzt.

### Pre-Commit-Hook

Der eigentliche Zauber entsteht, wenn du all das in einen Pre-Commit-Hook steckst. Ich empfehle das Python-Paket `pre-commit`. Einmal `uv tools install pre-commit`, eine `.pre-commit-config.yaml` basteln und bam – bei jedem Commit laufen Tests, Typprüfungen, Linting usw., damit der Code Note A+++ bekommt und sofort wieder lauffähig ist.

Das ist ein grandioser Hack mit Claude Code. Der Roboter WILL committen. Sag ihm also, er soll Code schreiben und committen (siehe oben): Er ändert wild, committet, zerschießt alles – und muss es gleich wieder reparieren.

So verstopfen fehlgeschlagene Lint- oder Format-Runs nicht deine GitHub Actions, nur weil der Roboter Laune hatte.

> Eine witzige Sache an Claude: Es checkt `uv` einfach nicht. Wenn du nicht aufpasst, macht es überall `pip install`. Bittest du es ausdrücklich, `uv` zu verwenden, schreibt es „uv pip install“. Vielleicht kommt die AGI doch nicht im Juni. So sad.

### CLAUDE.md und Commands

Beide Kleinigkeiten holen enorm viel raus.

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

Ich habe mir eine [CLAUDE.md](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md) von meinem Freund [Jesse Vincent](https://fsck.com/) geklaut, der [sie sehr ausgebaut hat](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md). Darin stecken u. a.:

- eine Light-Version der *big daddy rule*  
- Anweisungen zu TDD  
- stilistische Leitlinien, wie ich gern codiere

> [@clint](https://instagram.com/clintecker) hat seine CLAUDE.md so konfiguriert, dass sie ihn „MR BEEF“ nennt, und jetzt steht in aller Doku: „If you're stuck, stop and ask for help—MR BEEF may know best.“ Während ich das tippe, habe ich beschlossen, meine Datei so umzubauen, dass sie mich „Harp Dog“ nennt. Feature, kein Bug.

Auch die Commands sind superpraktisch. Einige findest du in meinen Dotfiles [hier](https://github.com/harperreed/dotfiles/tree/master/.claude/commands).

{{< image src="commands.png"  >}}

Früher nutzte ich die Commands viel häufiger, aber sie sind perfekt für wiederkehrende Prompts. Man kann sogar Argumente weitergeben. Zum Beispiel bei meinem GitHub-Issues-Command: `/user:gh-issue #45`

Claude führt dann das Skript aus, das in `gh-issue.md` definiert ist.

Du kannst diese Commands auch ins Projektverzeichnis packen und dort eine eigene `CLAUDE.md` ablegen. So habe ich pro Projekt spezifische Befehle für Hugo, Rust, Go oder JavaScript.

## „Continue“

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

Manchmal fühle ich mich wie der Vogel aus der Simpsons-Folge, der ständig „y“ tippt. Ich schreibe einfach „continue“ oder drücke ↑ und feuere denselben Prompt ab.

Die Pläne umfassen meist 8–12 Schritte. Ein *Greenfield-Projekt* ist damit in 30–45 Minuten durch – egal wie komplex oder in welcher Sprache.

Ich habe das mit meinem Freund Bob ausprobiert, und er glaubte es nicht. Also fragte ich: „Nenn was zu bauen und eine Sprache – los!“

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

Er so: „Okay. Einen BASIC-Interpreter in C.“

Nicht ideal – ich kann kein C, hab keine Ahnung, wie man einen Interpreter schreibt, und Lust darauf auch nicht. Fuck it.

Ich folgte den oben beschriebenen Schritten – und Claude Code lieferte. Wir haben jetzt [einen funktionierenden BASIC-Interpreter](https://github.com/harperreed/basic). Die erste Version lief nach einer Stunde. Ich habe noch ein paar Stunden gefeilt und er ist ziemlich gut. Würde ich ihn 1982 shippen? Wahrscheinlich nicht. Den [Prompt-Plan findest du hier](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md).

## Das Team

Unser ganzes Team nutzt aktuell Claude Code. Wir folgen grob dem obigen Prozess, jeder mit eigenen Tweaks.

Unsere Testabdeckung ist höher als je zuvor. Der Code ist besser und wirkt genauso effektiv wie der gruselige Kram von früher. Es ist lustig, Leuten zuzusehen, wie Claude Code in Ghostty, im VS-Code-Terminal, im Zed-Terminal oder in Jupyter-Notebooks läuft.

{{< image src="dril.jpg" >}}

Jemand mit vielen Tokens – bitte hilf mir, das zu budgetieren. Meine Familie stirbt hier!

## Danke

Danke an alle, die mir dauerhaft Mails schicken. Es ist super, von euren Workflows und Projekten zu hören. Ich weiß das echt zu schätzen. Immer her damit!