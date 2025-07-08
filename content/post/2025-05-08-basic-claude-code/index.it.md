---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description: Una guida dettagliata all'utilizzo dell'assistente AI Claude Code per
  lo sviluppo software, inclusi suggerimenti sul flusso di lavoro, pratiche di testing
  ed esempi pratici tratti da progetti reali. Copre strategie di codifica difensiva,
  TDD e implementazione del lavoro di squadra.
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
title: Claude Code di base
translationKey: Basic Claude Code
---

Mi piace un sacco l’*agentic coding* (la programmazione “agentica”): è davvero coinvolgente sotto molti aspetti.

Da quando ho scritto [quel post originale sul blog](/2025/02/16/my-llm-codegen-workflow-atm/) è successo di tutto nel mondo di Claude:

- Claude Code
- MCP
- ecc.

Ho ricevuto centinaia di email (sì, *wat*) da persone che raccontavano i loro *workflow* e di come abbiano usato il mio per guadagnare terreno. Ho parlato a qualche conferenza e tenuto un paio di corsi sul *codegen*. Ho scoperto che i computer vogliono davvero correggere “codegen” in “codeine”: chi l’avrebbe mai detto!

{{< image src="codegen.png"  >}}

L’altro giorno chiacchieravo con un’[amica](https://www.elidedbranches.com/) di come siamo **TUTTI COMPLETAMENTE FOTTUTI** e di come **l’IA ci ruberà il lavoro** (ne parlerò in un post futuro) e lei mi fa: «Dovresti scrivere un post su Claude Code».

Eccoci qui.

Claude Code è stato rilasciato otto giorni dopo il mio post sul *workflow* e, come avevo previsto, ha reso irrilevante buona parte di ciò che avevo scritto. Da allora sono passato da Aider a Claude Code e non mi sono più voltato indietro. Aider mi piace ancora e ha comunque la sua nicchia, ma in questo momento Claude Code è un filo più utile.

Claude Code è potentissimo, e costa un botto.

Il mio *workflow* è praticamente lo stesso di prima.

- Chatto con `gpt-4o` per affinare l’idea.
- Uso il miglior modello di ragionamento che trovo per generare la *spec*. In questi giorni è o1-pro o o3 (o1-pro è davvero migliore di o3 o mi sembra tale solo perché impiega più tempo?).
- Uso lo stesso modello per generare i *prompt*. Far scrivere i *prompt* a un LLM è un hack geniale che fa imbestialire i boomer.
- Salvo `spec.md` e `prompt_plan.md` nella directory principale del progetto.
- Poi digito in Claude Code quanto segue:

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

- La magia di questo *prompt* è che controlla **@prompt_plan.md**, cerca ciò che non è segnato come completato, quindi affronta il task successivo ancora aperto. Esegue il *commit* in Git, aggiorna il *prompt_plan* con ciò che ha terminato e poi si ferma chiedendoti se vuoi continuare. 🤌
- Io mi metto comodo e rispondo semplicemente «yes» mentre il processo va avanti. Ogni tanto chiede feedback e succede la magia.
- E via di click compulsivi, modello Cookie Clicker.

Funziona alla grande. Ci sono un paio di superpoteri da inserire nel processo che fanno davvero la differenza.

## Programmazione difensiva!

### Testing

Il *testing* e il *test-driven development* sono imprescindibili. Ti consiglio caldamente di coltivare una solida pratica di TDD.

Ero un *hater* del TDD: non ero bravo e mi sembrava di perdere tempo. Mi sbagliavo, lol. Lo riconosco. Negli ultimi decenni abbiamo aggiunto un sacco di test a progetti e aziende, ma per lo più DOPO il lavoro centrale. Per gli umani va bene.

QUESTO È PESSIMO PER I ROBOT.

I ROBOT ADORANO IL TDD. Sul serio: se lo divorano.

Con il TDD fai creare al tuo amico robot il test e il *mock*. Poi, nel *prompt* successivo, trasformi il *mock* in qualcosa di reale. L’assistente impazzisce di gioia. È la contromisura più efficace che abbia trovato contro le allucinazioni e la *scope drift* degli LLM. Li aiuta davvero a restare sul pezzo.

### Linting

Sono un grande fan del *linting*. Ruff è una meraviglia. Biome è fico. Clippy è divertente, e ha un gran nome.

Per qualche motivo i ROBOT adorano un buon *linter*.

Integrare la pratica di far girare continuamente il *linter* tiene lontani un sacco di bug e rende il codice più manutenibile e leggibile. Lo sai già.

Aggiungi un buon *formatter* ed è tutto bellissimo.

### Pre-commit hook

La vera magia è aggiungere queste attività a un *pre-commit hook*. Consiglio il pacchetto Python `pre-commit`. Con `uv tools install pre-commit` lo installi al volo, poi crei per bene un `.pre-commit-config.yaml` e bam: ogni volta che provi a fare *commit* esegue test, *type checking*, *linting* ecc. per assicurarsi che il tuo codice sia A+++ e pronto a girare di nuovo.

Ed è un hack fantastico per lavorare con Claude Code. IL ROBOT VUOLE DAVVERO fare *commit*. Quindi, quando gli dici di scrivere codice e poi committare (come ho fatto sopra), farà cambiamenti selvaggi, committerà il codice, inevitabilmente incasinerà tutto e poi dovrà sistemarlo.

È comodo perché non intasa le GitHub Actions con una valanga di *linting*, formattazione e *type checking* falliti solo perché l’IA era di cattivo umore.

> Una cosa buffa di Claude è che NON RIESCE proprio a capire come usare `uv` correttamente. Se non stai attento farà `pip install` a casaccio dappertutto. E se gli ordini di usare `uv`, lui eseguirà un misterioso `uv pip install`. Forse l’AGI non arriverà a giugno. Che tristezza.

### CLAUDE.md e comandi

Sono due aggiunte semplicissime che spremono un sacco di valore.

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

Ho rubato un [CLAUDE.md](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md) al mio amico [Jesse Vincent](https://fsck.com/) che ha fatto [un sacco di lavoro per renderlo super robusto](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md). È davvero figo. Dentro ci trovi, tra le altre cose:

- una versione light della “big daddy rule”;
- istruzioni su come fare TDD;
- indicazioni di stile su come mi piace scrivere codice.

> [@clint](https://instagram.com/clintecker) ha configurato il suo CLAUDE.md per farsi chiamare MR BEEF e adesso in tutta la nostra documentazione compaiono perle come «Se sei bloccato, fermati e chiedi aiuto—MR BEEF potrebbe saperla lunga». Mentre scrivevo questo, ho deciso di far sì che mi chiami “Harp Dog”. È una feature, non un bug.

Anche i comandi sono comodissimi. Puoi vederne alcuni nei miei dotfiles [qui](https://github.com/harperreed/dotfiles/tree/master/.claude/commands).

{{< image src="commands.png"  >}}

Una volta li usavo molto di più, ma restano un ottimo modo per riutilizzare *prompt* ricorrenti. Puoi anche passare argomenti: nel mio comando per le issue di GitHub, per esempio, passi il numero dell’issue che vuoi far analizzare a Claude: `/user:gh-issue #45`

A quel punto Claude eseguirà lo script *prompt* definito in `gh-issue.md`.

Puoi inoltre mettere questi comandi nella cartella di un progetto e creare un CLAUDE.md personalizzato per quel progetto. Lo faccio per avere comandi specifici quando lavoro con Hugo, Rust, Go o JavaScript.

## «Continue»

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

A volte mi sento come quell’uccellino che Homer usa per premere «y»: scrivo solo «continue» oppure premo la freccia su e incollo lo stesso *prompt*.

Di solito i piani sono di 8–12 passaggi. Nella maggior parte dei casi riesco a completare uno sviluppo da zero in 30–45 minuti, a prescindere da complessità apparente o linguaggio.

Ne parlavo con il mio amico Bob e non mi credeva. Gli ho chiesto: «Dimmi una cosa da costruire e il linguaggio con cui farla, e vediamo!»

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

Lui: «Ok. Un interprete BASIC in C.»

Non era il massimo: non conosco C, non ho mai scritto un interprete e, onestamente, non ne avevo troppa voglia. Ma pazienza.

Ho seguito i passaggi sopra e Claude Code ha fatto un ottimo lavoro. Ora abbiamo [un interprete BASIC funzionante](https://github.com/harperreed/basic). La prima versione è uscita in un’ora. Ci ho smanettato ancora un paio d’ore ed è piuttosto buono. Lo avremmo potuto distribuire nel 1982? Probabilmente no. Puoi vedere il [prompt_plan qui](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md).

## Il team

Tutto il nostro team usa attualmente Claude Code. Seguiamo più o meno il processo sopra, ognuno con le proprie personalizzazioni.

Stiamo raggiungendo una *test coverage* molto più alta di quanto abbiamo mai fatto. Il codice è migliore e sembra efficace quanto l’orribile codice che scrivevamo in passato. È divertente dare un’occhiata in giro e vedere Claude Code che gira in Ghostty, nel terminale di VS Code, in quello di Zed, mentre smanetta con notebook Python.

{{< image src="dril.jpg" >}}

Qualcuno con un mucchio di token, per favore, mi aiuti a gestire il budget. La mia famiglia sta morendo.

## Grazie

A tutte le persone che continuano a scrivermi: è davvero bello e divertente sentire dei vostri *workflow* e progetti. Lo apprezzo tantissimo. Continuate a mandarli!