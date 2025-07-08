---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: Una guida dettagliata del mio flusso di lavoro attuale per utilizzare
  gli LLM nella realizzazione di software, dal brainstorming alla pianificazione e
  all'esecuzione.
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
title: 'Il mio flusso di lavoro di generazione di codice con LLM al momento

  description: Una guida dettagliata del mio flusso di lavoro attuale per utilizzare
  gli LLM nella realizzazione di software, dal brainstorming alla pianificazione e
  all''esecuzione.'
translationKey: My LLM codegen workflow atm
---

_tl;dr – Fai brainstorming sulla specifica, poi prepara il piano, quindi esegui con la generazione di codice via LLM. Cicli discreti. Poi magia. ✩₊˚.⋆☾⋆⁺₊✧_

Da qualche tempo realizzo un sacco di piccoli prodotti con gli LLM: è divertente e utile. Però ci sono tranelli che possono farti sprecare un mare di tempo. Un po’ di tempo fa un amico mi ha chiesto come stessi usando gli LLM per scrivere software. Ho pensato: «Oh boy, quanto tempo hai?!» — ed ecco questo post.

(p.s. se detesti l’IA — scorri pure fino in fondo)

Parlo spesso con parecchi amici sviluppatori: abbiamo tutti un approccio simile, con qualche variazione qua e là.

Ecco il mio flusso di lavoro. Si basa sul mio lavoro, sulle chiacchiere con amici (grazie [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki) ed [Erik](https://thinks.lol/)) e su un mucchio di best practice raccolte in quei terribili [angoli](https://news.ycombinator.com/) [dell’Internet](https://twitter.com).

Funziona bene **ORA**: fra due settimane forse non funzionerà più o andrà il doppio meglio. ¯\\\_(ツ)\_/¯

## Andiamo

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="Trovo sempre sospette queste immagini generate dall’IA. Saluta il mio juggalo coding robot!" >}}

Di solito mi trovo in una di due situazioni:

- Greenfield (codice del tutto nuovo)  
- Codice legacy ma comunque recente

Ti mostrerò il mio flusso di lavoro per entrambi i casi.

## Greenfield

Per lo sviluppo greenfield il processo seguente funziona bene: offre una pianificazione e una documentazione robuste e ti permette di procedere facilmente a piccoli passi.

{{< image src="greenfield.jpg" alt="Green field" caption="Tecnicamente, un campo verde è sulla destra. Leica Q, 14 maggio 2016" >}}

### Fase 1: affinare l’idea

Perfeziona l’idea con un LLM in modalità conversazionale (io uso ChatGPT 4o/4o3):

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

Alla fine del brainstorming (arriverà a una conclusione naturale):

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

Otterrai una specifica solida e chiara da passare alla fase di pianificazione. Io la salvo come `spec.md` nel repo.

> Puoi usare questa specifica per un sacco di cose. Qui la useremo per la generazione di codice, ma l’ho già sfruttata per rafforzare idee chiedendo a un modello di ragionamento di trovare falle (must go deeper!), per creare un white paper o un business model. Se la infili in una “ricerca profonda”, può tornarti un documento di supporto da 10 000 parole.

### Fase 2: pianificazione

Prendi la `spec` e passala a un modello di puro ragionamento (`o1*`, `o3*`, `r1`).

(Questo è il prompt TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(Questo è il prompt non TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

Otterrai un piano di prompt eseguibile con Aider, Cursor, ecc. Io lo salvo come `prompt_plan.md` nel repo.

Poi gli chiedo di generare un `todo.md` da spuntare:

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

Salvalo come `todo.md` nel repo.

Il tuo strumento di generazione del codice dovrebbe spuntare il `todo.md` mentre lavora: è utile per mantenere lo stato fra le sessioni.

#### Grandioso, abbiamo un piano!

Ora hai un piano robusto e la documentazione che ti aiuteranno a costruire il progetto.

Tutto il processo richiede forse **15 minuti**. È piuttosto folle, a dirla tutta.

### Fase 3: esecuzione

Le opzioni di esecuzione sono tante; il successo dipende da quanto bene è andata la fase 2.

Ho usato questo flusso di lavoro con [GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude Engineer](https://github.com/Doriandarko/claude-engineer), [Sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [Claude.ai](https://claude.ai) e altri. Finora ha funzionato con tutti gli strumenti di code-gen che ho provato e immagino che funzioni bene con qualunque tool del genere.

Io però preferisco Claude “puro” e Aider.

### Claude

In pratica faccio pair programming con [Claude.ai](https://claude.ai) e inserisco ogni prompt in modo iterativo. Funziona bene; il continuo back-and-forth può essere noioso, ma di solito rende.

Mi occupo del boilerplate iniziale e di configurare gli strumenti: avere già un fondamento solido con linguaggio, stile e tooling scelti aiuta molto, visto che Claude tende a generare soprattutto codice React.

Quando le cose si bloccano uso un tool come [Repomix](https://github.com/yamadashy/repomix) per iterare (ne parlo più avanti).

Il flusso di lavoro è il seguente:

- preparo il repo (boilerplate, `uv init`, `cargo init`, ecc.)  
- incollo il prompt in Claude  
- copio il codice da Claude.ai nell’IDE  
- avvio il codice, faccio girare i test  
- …  
- se funziona, passo al prompt successivo  
- se non funziona, uso Repomix per passare l’intera codebase a Claude e fare debug  
- ripeti da capo ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) è divertente e un po’ particolare. Si integra bene con l’output della fase 2: con pochissimo sforzo puoi andare molto avanti.

Il flusso è pressoché lo stesso, ma invece di incollare in Claude incolli i prompt in Aider.

Aider «fa e basta» e nel frattempo ti fai una partita a [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/).

> Piccola parentesi: Aider pubblica ottimi benchmark dei nuovi modelli di code-gen nei suoi [LLM leaderboards](https://aider.chat/docs/leaderboards/); è una grande risorsa per valutarne l’efficacia.

Il testing con Aider è quasi automatico: può eseguire la test-suite e fare debug per te.

Il flusso di lavoro è il seguente:

- preparo il repo (boilerplate, `uv init`, `cargo init`, ecc.)  
- avvio Aider  
- incollo il prompt in Aider  
- guardo Aider all’opera ♪┏(・o･)┛♪  
- Aider esegue i test, oppure avvio l’app per verificare  
- se funziona, passo al prompt successivo  
- se non funziona, dialogo con Aider per sistemare  
- ripeti da capo ✩₊˚.⋆☾⋆⁺₊✧

### Risultati

Con questo flusso di lavoro ho costruito di tutto: script, app Expo, CLI in Rust, ecc. Ha funzionato con diversi linguaggi e contesti e lo adoro.

Se hai un progetto (piccolo o grande) che stai rimandando, prova: rimarrai sorpreso da quanto lontano puoi arrivare in poco tempo.

La mia to-do list di hack è vuota perché ho costruito tutto. Continuo a pensare nuove cose e le completo mentre guardo un film. Per la prima volta da anni sto sperimentando nuovi linguaggi e strumenti, ampliando la mia prospettiva di programmatore.

## Non-greenfield: iterare in modo incrementale

A volte non hai un greenfield: devi iterare o fare lavoro incrementale su una codebase esistente.

{{< image src="brownfield.jpg" alt="Campo bruno" caption="Questo non è un campo verde. Foto a caso dalla macchina fotografica di mio nonno — Uganda, anni ’60" >}}

Per questo uso un metodo leggermente diverso: simile a quello sopra, ma meno «basato sulla pianificazione». Qui la pianificazione è per singolo task, non per l’intero progetto.

### Recuperare contesto

Chi sviluppa con gli LLM usa strumenti diversi, ma serve qualcosa che prenda il tuo codice e lo infili efficacemente nel modello.

Io uso [Repomix](https://github.com/yamadashy/repomix). Ho una raccolta di task definita nel mio `~/.config/mise/config.toml` globale che mi permette di fare varie cose con la codebase ([regole mise](https://mise.jdx.dev/)).

Ecco la lista di task LLM:

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

Genero un `output.txt` con il contesto della codebase. Se il file è troppo grande e consumo troppi token, modifico il comando di generazione per ignorare parti non rilevanti.

> Una cosa splendida di `mise` è che i task possono essere ridefiniti nel `.mise.toml` della directory di lavoro. Posso usare un altro tool per impacchettare il codice e, finché produce `output.txt`, i miei task LLM funzionano. È utile quando le codebase sono molto diverse. Spesso sovrascrivo lo step `repomix` con pattern di ignore più ampi o un tool più efficace.

Una volta generato `output.txt`, lo passo al comando [LLM](https://github.com/simonw/LLM) per varie trasformazioni e salvo l’output in un file markdown.

In pratica il task mise esegue `cat output.txt | LLM -t readme-gen > README.md` o `cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md`. Niente di complesso: il comando `LLM` fa il grosso (supportando diversi modelli, gestendo le chiavi e usando template di prompt).

Per esempio, se mi serve una rapida revisione della copertura dei test faccio così.

#### Claude

- entro nella directory del codice  
- eseguo `mise run LLM:generate_missing_tests`  
- apro `missing-tests.md`  
- copio il contesto completo con `mise run LLM:copy_buffer_bundle`  
- incollo tutto in Claude insieme alla prima issue sui test mancanti  
- copio il codice generato da Claude nell’IDE  
- …  
- lancio i test  
- ripeti da capo ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- entro nella directory del codice  
- avvio Aider (assicurati di essere su un nuovo branch)  
- eseguo `mise run LLM:generate_missing_tests`  
- apro `missing-tests.md`  
- incollo la prima issue in Aider  
- guardo Aider all’opera ♪┏(・o･)┛♪  
- …  
- lancio i test  
- ripeti da capo ✩₊˚.⋆☾⋆⁺₊✧

È un ottimo modo per migliorare incrementalmente una codebase e funziona bene anche per task di qualsiasi dimensione.

### Magia dei prompt

Questi hack veloci funzionano alla grande per rendere un progetto più robusto, in modo rapido ed efficace.

Ecco alcuni prompt che uso su codebase esistenti:

#### Code review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply  before writing the code review. Review every part, and don't hallucinate.
```

#### Generazione di issue GitHub

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Test mancanti

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues  will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

Questi prompt sono un po’ old and busted («prompt da boomer», se vogliamo): avrebbero bisogno di refactoring. Se hai idee per migliorarli, fammi sapere.

## Sci ᨒ↟ 𖠰ᨒ↟ 𖠰

Quando descrivo questo processo dico spesso: «devi tenere traccia di ciò che succede in modo aggressivo, perché puoi facilmente ritrovarti troppo avanti».

Per qualche motivo dico «over my skis» parlando di LLM. Non so perché. Mi risuona parecchio. Forse perché è come sciare su polvere perfetta, poi all’improvviso pensi «CHE DIAVOLO STA SUCCEDENDO!» e ti ritrovi perso, precipitando da un dirupo.

Una fase di pianificazione (come nel processo greenfield) aiuta a tenere tutto sotto controllo. Almeno hai un documento su cui ricontrollare. Credo anche che i test siano utili — soprattutto se fai coding stile wild con Aider: aiutano a mantenere tutto solido e pulito.

Comunque mi ritrovo ancora over my skis abbastanza spesso. A volte bastano una breve pausa o una passeggiata. In fondo è un normale problem-solving, ma accelerato a velocità folle.

> Capita spesso di chiedere all’LLM di inserire cose assurde in un codice che di suo non sarebbe così folle. Per esempio gli abbiamo chiesto di creare un file di lore e poi di citarlo nell’interfaccia utente di un tool CLI Python. All’improvviso compaiono lore, interfacce glitchate ecc. Tutto per gestire le tue cloud function, la tua to-do list o chissà che altro. Il cielo è il limite.

## Sono così solo (｡•́︿•̀｡)

La mia principale lamentela su questi flussi di lavoro è che sono per lo più un’esperienza in solitaria: le interfacce sono tutte in modalità giocatore singolo.

Ho passato anni a programmare da solo, in pair e in team. È sempre meglio con altre persone. Questi flussi non sono facili da usare in squadra: i bot collidono, i merge sono orribili, il contesto è complicato.

Vorrei davvero che qualcuno risolvesse questo problema e rendesse la programmazione con un LLM un gioco multiplayer, non un’esperienza da hacker solitario. C’è un’enorme opportunità per farlo diventare fantastico.

GET TO WORK!

## ⴵ Tempo ⴵ

Tutta questa code-gen ha aumentato di molto la quantità di codice che riesco a produrre da solo. C’è però un effetto collaterale strano: ho un sacco di «tempo morto» mentre l’LLM macina token.

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="Me lo ricordo come fosse ieri" >}}

Ho quindi cambiato modo di lavorare e ora sfrutto quell’attesa per:

- avviare il brainstorming di un altro progetto  
- ascoltare vinili  
- giocare a Cookie Clicker  
- chiacchierare con amici e robot  

È fantastico poter hackerare in questo modo. Hack, hack, hack. Non ricordo un altro momento in cui sia stato così produttivo con il codice.

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

Molti amici mi dicono: «fanculo gli LLM, fanno schifo in tutto». Non mi infastidisce questo punto di vista: non lo condivido, ma credo sia importante essere scettici. Ci sono parecchi motivi per odiare l’IA. La mia paura principale è il consumo energetico e l’impatto ambientale. Ma… the code must flow. Sigh.

Se sei curioso ma non vuoi diventare un programmatore cyborg, ti suggerisco di leggere il libro di Ethan Mollick sugli LLM e sul loro utilizzo: [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/).

Spiega i benefici senza essere un tomo da bro anarco-capitalista tech. L’ho trovato molto utile e ho fatto tante conversazioni interessanti con amici che l’hanno letto. Consigliatissimo.

Se sei scettico ma un po’ curioso, scrivimi: parliamo di tutta questa follia e magari costruiamo qualcosa insieme.

_grazie a [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com) ed [Erik](https://thinks.lol/) per aver letto questo post e suggerito modifiche. Vi apprezzo._