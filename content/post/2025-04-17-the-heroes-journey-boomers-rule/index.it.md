---
bsky: https://bsky.app/profile/harper.lol/post/3ln2a3x52xs2y
date: 2025-04-17 09:00:00-05:00
description: Una guida completa che illustra l'evoluzione dello sviluppo software
  assistito dall'IA, dal semplice completamento del codice fino ad agenti di programmazione
  completamente autonomi, con passaggi pratici e spunti per massimizzare la produttività
  attraverso l'integrazione degli LLM.
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
title: Il viaggio dell'eroe del codegen con LLM
translationKey: An LLM Codegen Hero's Journey
---

Ho passato un sacco di tempo, da quando ho pubblicato il mio [post sul blog](/2025/02/16/my-llm-codegen-workflow-atm/) sul mio workflow basato su LLM, a chiacchierare con persone che si occupano di codegen: come iniziare, come migliorare e perché diamine sia così interessante.  

Si è creata un’enorme ondata di energia e curiosità sull’argomento. Mi sono arrivate valanghe di e-mail da chi cerca di capirci qualcosa. Ho notato che molti fanno fatica a capire da dove partire e come far combaciare tutti i pezzi. Poi mi sono ricordato che ci smanetto dal 2023 e ne ho viste di tutti i colori. Lol.  

Ne parlavo con alcuni amici (Fisaconites, fatevi valere!) e ho inviato questo messaggio in risposta a un thread sugli editor e sugli agenti assistiti dall’IA:

> se dovessi ricominciare da zero, non so se serva davvero buttarsi subito in quegli “agent-coder”. È roba strana e frustrante. Avendo accompagnato un po’ di persone in questo viaggio (con successo e, a volte, senza successo) trovo che la «hero’s journey» – partire da Copilot, passare al copia-e-incolla da Claude Web, poi a Cursor/Continue e infine agli agent completamente automatizzati – funzioni alla grande per adottare ‘sta roba.

Questo mi ha fatto riflettere parecchio sul viaggio e su come cominciare con la programmazione basata su agenti («agentic coding»):

> Premessa: vale soprattutto per chi ha già esperienza. Se non ne hai, fanculo – salta direttamente alla fine. **Il nostro cervello è spesso rovinato dalle regole del passato.**

## Un viaggio fra suoni e visioni

{{< image src="journey-harper.webp" alt="Harper è assolutamente affidabile" caption="La tua guida premurosa: Harper. iPhone X, 6 ottobre 2018" >}}

Questo è il mio percorso. È più o meno la strada che ho fatto io. Volendo potresti farne uno speedrun. Non serve seguire ogni tappa, ma ognuna aggiunge qualcosa.

Ecco i passaggi:

### Passo 1: Alzati dal letto con meraviglia e ottimismo

Lol. Scherzo. Chi ha il tempo? Potrebbe aiutare, ma il mondo va a rotoli e tutto quello che abbiamo per distrarci è il codegen.  

Comunque, conviene almeno pensare che questi workflow possano funzionare e darti valore. Se odi gli LLM e credi che non servano a niente, non combinerai molto qui. ¯\_(ツ)_/¯

### Passo 2: Inizia con l’autocompletamento assistito dall’IA

Questo è il vero step one! Devi passare abbastanza tempo nell’IDE per capire come ti trovi con [IntelliSense](https://en.wikipedia.org/wiki/Code_completion), [l’autocomplete di Zed](https://zed.dev/blog/out-of-your-face-ai), [Copilot](https://copilot.github.com/), ecc. Ti dà un’idea di come ragiona l’LLM e ti prepara alle cazzate che a volte proporrà.  

La gente vuole saltare questo step e andare dritta alla fine. Poi esclama: «Questo LLM è una merda, non fa niente di giusto!». Non è proprio così, ma può anche essere vero. La magia sta nelle sfumature. O, come mi piace dire: _la vita è confusa_.

### Passo 3: Usa Copilot per qualcosa di più dell’autocomplete

Quando hai un buon ritmo con l’autocomplete e non sei incazzato _sempre_, puoi passare alla magia di chiacchierare con Copilot.  

VS Code ha un pannello domande-e-risposte dove puoi dialogare con Copilot e farti aiutare sul codice. È parecchio figo.  

Però usare Copilot è un po’ come parlare con ChatGPT nel 2024 via macchina del tempo: non è **così** fantastico.  

Vorrai di più.

### Passo 4: Copia-incolla il codice in Claude o ChatGPT

Cominci a toglierti la curiosità incollando codice in un modello fondazionale nel browser e chiedendo: «WHY CODE BROKE??», e l’LLM risponde in modo coerente e utile.  

Rimarrai SBALORDITO! I risultati ti faranno impazzire. Tornerai a costruire roba strana e divertente, soprattutto perché salti quasi tutto il debugging.  

Puoi fare cose folli tipo incollare uno script Python e dire: «Trasformalo in Go» e lui lo _trasforma in Go_. Penserai: «Chissà se riesco a farlo in un colpo solo».  

Copilot comincerà a sembrarti un autocompletamento da 2004: utile, ma non indispensabile.

Questo ti porterà su un paio di percorsi secondari:

#### Inizierai a preferire un modello per “vibes”

Questo è il primo, e purtroppo inevitabile, passo verso il «vibe-coding» (programmazione a vibrazioni, se vogliamo). Inizierai a preferire come un modello ti parla. Sono sensazioni, un po’ strane. Ti sorprenderai a pensare: «Mi piace come Claude mi fa sentire».  

Molti sviluppatori amano Claude. Io uso entrambi, ma per il codice quasi sempre Claude: la vibe è semplicemente migliore.

> Devi pagarli per avere il buono. Un sacco di amici dicono «Fa schifo» e poi scopri che usano un modello gratuito che funziona a stento. Lol. Era peggio quando la versione free era ChatGPT 3.5, ma in ogni caso assicurati di usare un modello all’altezza prima di cestinare tutto il concetto.

#### Inizierai a chiederti come accelerare tutto

Dopo qualche settimana di copia-incolla in Claude capirai che è snervante. Comincerai a cimentarti nell’impacchettamento del contesto, cercando di far entrare più codice possibile nella finestra di contesto (context window).  

Sperimenterai con [repomix](https://repomix.com/), [repo2txt](https://github.com/donoceidon/repo2txt) e altri tool, magari facendoti scrivere da Claude degli script di shell per rendere tutto più semplice.  

Questo è un punto di svolta.

### Passo 5: Usa un IDE con IA integrata (Cursor, Windsurf?)

Poi un amico dirà: «Perché non usi semplicemente [Cursor](https://cursor.sh/)?»  

Ti salterà in aria il cervello. Tutta la magia del copia-incolla adesso è dentro l’IDE: più veloce, divertente, quasi magica.  

A questo punto stai già pagando tipo cinque LLM diversi: che saranno mai altri 20 dollari al mese?  

Funziona alla grande e ti senti MOLTO più produttivo.  

Inizierai a smanettare con le funzionalità basate su agenti integrate negli editor: funzionano _quasi_ del tutto. Ma all’orizzonte intravedi qualcosa di ancora migliore.

### Passo 6: Cominci a pianificare prima di scrivere codice

All’improvviso ti ritrovi a produrre specifiche, PRD e to-do super dettagliati da dare in pasto all’agente dell’IDE o a Claude Web.  

Non hai mai scritto così tanta documentazione. Usi altri LLM per renderla ancora più robusta. Trasponi documenti da un contesto (PRD) a un altro («Puoi farne dei prompt?»). Usi l’LLM per progettare i prompt di codegen.  

Pronunci la parola “[waterfall](https://en.wikipedia.org/wiki/Waterfall_model)” con molto meno disprezzo. Se sei un po’ attempato, ricorderai con affetto la fine degli anni ’90 e ti chiederai: «È così che si sentiva Martin Fowler prima del [2001](https://en.wikipedia.org/wiki/Agile_software_development)?»  

Nel mondo del codegen la specifica è la divinità assoluta.

### Passo 7: Prova aider per cicli più rapidi

Ora sei pronto per **la roba buona**. Finora il codegen richiedeva la tua supervisione, ma è il 2025! Chi vuole ancora digitare con le dita?

> Un’altra strada che molti amici stanno provando è programmare a voce, parlando ad aider tramite un client Whisper. È esilarante e divertente. MacWhisper è ottimo in locale; Aqua e superWhisper sono validi ma costano di più e spesso usano il cloud per l’inferenza. Io preferisco il locale.

Provare aider è folle. Lo avvii, si installa nel progetto, gli scrivi la richiesta e lui fa quello che hai chiesto: chiede il permesso di agire, ti fornisce un mini-framework per portare avanti il task e poi esegue. Completa il compito e fa i commit sul repo. Non ti preoccupi più di risolvere tutto in un colpo solo: lasci che aider lo faccia in più step.  

Cominci a creare set di regole per l’LLM. Scopri la “[Big Daddy rule](https://www.reddit.com/r/cursor/comments/1joapwk/comment/mkqg8aw/)” o l’aggiunta “no deceptions” ai prompt. Diventi davvero bravo a istruire il robot.  

**Funziona.**  

Alla fine non apri più un IDE: sei rimasto solo un fantino del terminale.  

Passi il tempo a guardare il robot che fa il tuo lavoro.

### Passo 8: Ti butti completamente nella programmazione basata su agenti («agentic coding»)

Ora usi un agente che scrive codice per te. I risultati sono ottimi. A volte non capisci che diamine stia succedendo, poi ti ricordi che puoi semplicemente chiederglielo.  

Smanetti con [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Cline](https://cline.bot/) e altro. Sei felice di combinare un modello di ragionamento ([DeepSeek](https://aws.amazon.com/bedrock/deepseek/)) e uno di coding ([Claude Sonnet 3.7](https://www.anthropic.com/claude/sonnet)) per togliere di mezzo intere fasi di pianificazione.  

Fai cose folli tipo tenere aperte 3-5 sessioni in parallelo, tabbando fra terminali e guardando i robot che scrivono.  

Inizi a programmare in modalità “difensiva”:

- copertura di test super rigorosa  
- pensi alla [formal verification](https://github.com/formal-land/coq-of-rust)  
- scegli linguaggi che garantiscono la sicurezza della memoria  
- valuti i linguaggi in base alla verbosità del compilatore per ottimizzare la finestra di contesto  

Penserai a lungo e seriamente su come garantire che ciò che costruisci venga realizzato in sicurezza, senza interventi.  

Spenderai **UN SACCO** di soldi in token. Brucerai tutte le ore gratuite di GitHub Actions mandando in esecuzione test assurdi per assicurarti che il codice sia solido.  

È bello. Non ti manca scrivere codice a mano.

### Passo 9: L’agente programma e tu giochi ai videogiochi

All’improvviso ci sei. Sei (quasi) arrivato, ma capisci dove stiamo andando. Cominci a preoccuparti per i lavori nel software: amici licenziati che non trovano nuovi impieghi. Stavolta l’aria è diversa.  

Quando parli con i colleghi, ti vedono come un fanatico religioso perché lavori in un contesto diverso. Dici: «Omg, devi provare la programmazione basata su agenti!» Magari aggiungi «odio la parola _agentic_» per dimostrare che non hai bevuto 200 litri di Kool-Aid. Ma li hai bevuti. Il mondo sembra più luminoso perché sei così produttivo.  

Non importa. Il paradigma è cambiato. Kuhn potrebbe scriverci un libro sulla confusione di quest’epoca.  

Chi non ha fatto il viaggio non lo vede; chi l’ha fatto scambia consigli sul percorso e discute della meta.  

Ora che lasci lavorare i robot, puoi finalmente dedicarti a tutti quei giochi per Game Boy che volevi finire. C’è un sacco di downtime. Quando il robot finisce un task e chiede «Devo continuare?», tu digiti **yes** e torni a Tetris.  

Molto strano. Inquietante, persino.

## L’accelerazione

<paul confetti photo>
{{< image src="journey-confetti.webp" alt="Coriandoli" caption="Coriandoli a un concerto di Paul McCartney al Tokyo Dome. iPhone 6, 25/4/2015" >}}

Non so cosa succederà nel [futuro](https://ai-2027.com/). Temo che chi non stia facendo questo viaggio non risulterà interessante per i [datori di lavoro](https://x.com/tobi/status/1909231499448401946). È una visione un po’ miope, perché alla fine stiamo parlando di tooling e automazione.  

Quando in passato aumentavamo l’organico, spesso cercavamo oltre la nostra rete e oltre il nostro stack. Eravamo una realtà Python e intervistavamo persone che non l’avevano mai usato. Pensavamo che, con un ottimo ingegnere, avremmo potuto aiutarlo a sentirsi a proprio agio con Python. Ha funzionato: assumevamo persone incredibili che portavano prospettive nuove e alzavano il livello di tutto il team.  

Gli stessi principi valgono per lo sviluppo assistito dall’IA. Quando assumi sviluppatori talentuosi che si integrano con la cultura del team e mostrano entusiasmo, il loro livello di esperienza con gli strumenti IA non dovrebbe essere decisivo. Non devono essere esperti dal giorno uno: guidali nell’apprendimento, al loro ritmo, accanto a membri più esperti.  

Alla fine saranno loro a guidare e useranno questi strumenti con successo.  

Un’altra cosa che mi frulla in testa: le skill di scrittura sono diventate critiche. Abbiamo sempre apprezzato chi comunica bene per documentazione e collaborazione, ma ora è doppiamente importante. Devi comunicare con gli umani _e_ scrivere istruzioni chiare per l’IA. Saper scrivere prompt efficaci sta diventando importante quanto scrivere buon codice.

## La leadership

Penso che tutte le leader e i leader, così come i manager d’ingegneria, debbano buttarsi a capofitto nello sviluppo assistito dall’IA, che ci credano o no. Ecco perché: la prossima generazione di sviluppatori imparerà a programmare principalmente con tool e agent IA. Questo è ciò che sta diventando l’ingegneria del software. Dobbiamo capirlo e adattarci.  

Noi boomer del codice non abbiamo vita lunga, ormai.

**nota interessante:** non uso davvero gli LLM per aiutarmi a scrivere testi. Immagino funzionino bene, ma voglio che la mia voce si senta e non venga normalizzata. Il mio codice, invece, va benissimo se è normalizzato. Interessante.

---

Grazie a Jesse, Sophie, alla crew Vibez (Erik, Kanno, Braydon e altri), al team 2389 e a tutti quelli che mi hanno dato feedback su questo post.