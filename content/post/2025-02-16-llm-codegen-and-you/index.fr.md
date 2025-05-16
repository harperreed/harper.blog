---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: Une présentation détaillée de mon workflow actuel pour utiliser les LLMs
  afin de créer des logiciels, du brainstorming à la planification et à l'exécution.
draft: false
generateSocialImage: true
tags:
- LLM
- coding
- ai
- workflow
- software-development
- productivity
title: Mon workflow de génération de code LLM en ce moment
translationKey: My LLM codegen workflow atm
---

_tl ; dr : fais un brainstorming de la spécification, puis élabore un plan de plan, puis exécute avec de la génération de code par LLM. Boucles bien distinctes. Ensuite, la magie. ✩₊˚.⋆☾⋆⁺₊✧_

Je développe depuis quelque temps une foule de petits produits grâce aux LLM. C’est fun — et utile. Mais il y a aussi des pièges qui font perdre un temps fou. Un jour, un ami m’a demandé comment j’utilisais les LLM pour écrire du logiciel. J’ai pensé : « Oh boy, t’as combien d’heures devant toi ? » — d’où ce billet.

(p.s. si tu détestes l’IA, file direct à la fin)

J’en parle souvent avec des potes dev et on suit tous à peu près la même approche, chacun y ajoutant ses petits réglages.

Voici donc mon flux de travail. Il repose sur mon expérience personnelle, sur des échanges avec des amis (merci [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki) et [Erik](https://thinks.lol/)), ainsi que sur de bonnes pratiques glanées dans les recoins (parfois douteux) du Net : [bad](https://news.ycombinator.com/) [places](https://twitter.com).

Ça marche super bien **MAINTENANT** ; dans deux semaines ce sera peut-être cassé… ou deux fois plus performant. ¯\\\_(ツ)_/¯

## Allons-y

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="Je trouve toujours ces images générées par IA un peu louches. Voici mon ange-robot codeur façon juggalo !" >}}

Il existe mille manières de développer, mais je me retrouve généralement dans l’un de ces deux cas :

- nouveau projet (greenfield) ;
- code « legacy moderne » (un projet assez récent mais déjà hérité).

Je vais te montrer mon processus pour les deux pistes.

## Greenfield

Pour un projet greenfield, ce processus fonctionne bien : planification solide, docs propres et avancée par petits pas.

{{< image src="greenfield.jpg" alt="Green field" caption="Techniquement, il y a bien un champ vert à droite. Leica Q, 14/05/2016" >}}

### Étape 1 : affiner l’idée

Utilise un LLM conversationnel pour peaufiner l’idée (j’emploie ChatGPT 4o / o3).

Conserve les prompts suivants en anglais (les modèles les préfèrent ainsi).

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

Quand le brainstorming arrive à sa conclusion naturelle :

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

Tu obtiens une spécification bien nette que je sauvegarde d’habitude sous `spec.md`.

> On peut tirer beaucoup de choses de cette spec. Ici, on vise le codegen, mais je l’utilise aussi pour demander à un modèle de raisonnement de dénicher les failles (toujours plus profond !), pour rédiger un white paper ou imaginer un business model. Tu peux même lancer une recherche poussée et récupérer un document de 10 000 mots en retour.

### Étape 2 : planification

Envoie la spec à un modèle orienté raisonnement (`o1*`, `o3*`, `r1`).

#### Prompt TDD

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

#### Prompt non-TDD

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

Le modèle te fournit alors un plan de prompts à exécuter (je le sauvegarde en `prompt_plan.md`).

Demande-lui ensuite une todo-list :

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

Ton outil de génération de code pourra cocher `todo.md` au fil de la session : parfait pour garder le contexte.

#### Youpi, un plan !

Tu as désormais un plan solide et une doc prête à piloter ton projet.

Ces deux premières étapes prennent quoi… **15 minutes** ? C’est dingue.

### Étape 3 : exécution

Il existe une foule d’outils ; leur succès dépend surtout de la qualité de l’étape 2.

J’ai testé ce workflow avec [GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude-Engineer](https://github.com/Doriandarko/claude-engineer), [Sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [Claude.ai](https://claude.ai)… Ils s’en sortent tous.

Moi, je préfère Claude en mode brut (sans surcouche) et Aider.

### Claude

Je fais du pair-programming sur [Claude.ai](https://claude.ai) : je colle chaque prompt tour à tour. Les allers-retours peuvent être pénibles, mais ça fonctionne.

Je gère le boilerplate et le setup tooling ; ainsi, Claude n’impose pas d’office du React et je garde la main sur la stack.

Quand ça coince, j’utilise [Repomix](https://github.com/yamadashy/repomix) (un empaqueteur de dépôt) pour envoyer tout le code à Claude et déboguer.

Workflow :

- initialise le dépôt (boilerplate, `uv init`, `cargo init`, etc.) ;
- colle le prompt dans Claude ;
- copie le code généré dans ton IDE ;
- lance l’appli, exécute les tests ;
- …  
- si ça roule : prompt suivant ;  
- sinon : repomix + Claude pour déboguer ;
- on rince, on répète ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) est fun et un peu étrange ; il s’imbrique bien avec la sortie de l’étape 2 et permet d’aller très loin sans effort.

Même logique : on colle les prompts dans Aider.

Aider « fait le taf » et je joue à [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/).

> Au passage, Aider publie d’excellents benchmarks de modèles de codegen dans ses [LLM leaderboards](https://aider.chat/docs/leaderboards/). Idéal pour jauger les nouveaux modèles.

Grâce aux tests, Aider peut être encore plus mains libres : il exécute la suite et débogue tout seul.

Workflow :

- initialise le dépôt ;
- lance Aider ;
- colle le prompt ;
- regarde Aider danser ♪┏(・o･)┛♪ ;
- Aider lance les tests ou tu lances l’appli pour vérifier ;
- si OK : prompt suivant ;
- sinon : questions/réponses avec Aider pour corriger ;
- on rince, on répète ✩₊˚.⋆☾⋆⁺₊✧

### Résultats

J’ai réalisé une quantité folle de trucs : scripts, applis Expo, CLI Rust, etc. Tout langages confondus. Ultra efficace.

Ma todo hack est vide parce que j’ai tout fini. Je continue d’avoir de nouvelles idées que j’enchaîne pendant un film. Pour la première fois depuis des années, je découvre de nouveaux langages et outils ; ça élargit vraiment mon horizon.

## Non-greenfield : itérations incrémentales

Parfois, on n’est pas en terrain vierge : il faut itérer sur une base de code existante.

{{< image src="brownfield.jpg" alt="a brown field" caption="Ce n’est pas un champ vert. Photo prise par mon grand-père — Ouganda, années 60" >}}

Dans ce cas, méthode un peu différente : moins de plan global, plus de planification tâche par tâche.

### Obtenir le contexte

Chacun a sa technique pour empaqueter le code et l’injecter dans le LLM. J’utilise actuellement [Repomix](https://github.com/yamadashy/repomix) via des tâches définies dans `~/.config/mise/config.toml` (voir les [règles Mise](https://mise.jdx.dev/)).

Voici la liste des tâches LLM :

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

Je génère un `output.txt` contenant tout le contexte. Si ça déborde en tokens, j’exclus les parties inutiles.

> Atout de `mise` : on peut redéfinir ou surcharger ces tâches dans le `.mise.toml` du projet. Tant que ça produit un `output.txt`, mes tâches LLM tournent. Pratique quand les bases de code sont très différentes. Je surcharge souvent l’étape Repomix pour élargir les motifs d’exclusion ou utiliser un empaqueteur plus adapté.

Une fois `output.txt` prêt, je le passe à la commande [LLM](https://github.com/simonw/LLM) pour diverses transformations et je sauvegarde la sortie en markdown.

En pratique :

```
cat output.txt | LLM -t readme-gen > README.md
```

ou :

```
cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md
```

`LLM` gère modèles, clés et templates.

Exemple : améliorer rapidement la couverture de tests.

#### Claude

- place-toi dans le dossier du code ;  
- `mise run LLM:generate_missing_tests` ;  
- ouvre `missing-tests.md` ;  
- copie le bundle : `mise run LLM:copy_buffer_bundle` ;  
- colle-le dans Claude avec la première « issue » ;  
- copie le code généré dans ton IDE ;  
- exécute les tests ;  
- on rince, on répète ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- place-toi dans le dossier ;  
- lance Aider (sur une nouvelle branche) ;  
- `mise run LLM:generate_missing_tests` ;  
- ouvre `missing-tests.md` ;  
- colle la première « issue » dans Aider ;  
- regarde Aider danser ♪┏(・o･)┛♪ ;  
- exécute les tests ;  
- on rince, on répète ✩₊˚.⋆☾⋆⁺₊✧

Super efficace pour améliorer progressivement une grosse base de code.

### Magie des prompts

Ces petites astuces sont redoutables pour rendre un projet plus robuste. Vite fait, bien fait.

Voici quelques prompts que j’utilise sur du code établi (à conserver en anglais) :

#### Code review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply before writing the code review. Review every part, and don't hallucinate.
```

#### Génération d’issues GitHub

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Tests manquants

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

Ces prompts datent un peu (« prompts de boomer »). Si tu as des idées pour les améliorer, fais signe !

## Skiing ᨒ↟ 𖠰ᨒ↟ 𖠰

Quand j’explique ce procédé, je dis : « Il faut suivre de près ce qui se passe, sinon tu te retrouves vite **over your skis**. »

Je parle souvent d’être ***over my skis*** avec les LLM : tu skies dans de la poudre parfaite et, soudain, « WHAT THE FUCK IS GOING ON ? » — tu pars en vrille et tu chutes.

La **phase de planification** (cf. greenfield) aide à garder le contrôle : tu as au moins un doc de référence. Les tests aussi, surtout avec Aider en mode freestyle : ça garde le code propre et serré.

Malgré ça, je me retrouve encore souvent ***over my skis***. Parfois, une pause ou une petite marche suffit. Au fond, c’est le même processus de résolution de problèmes, mais à vitesse supersonique.

> On demande parfois au LLM d’ajouter des trucs totalement absurdes dans un code qui ne l’est pas tant que ça. Exemple : créer un fichier de lore puis le référencer dans l’interface d’un outil CLI Python. D’un coup, il y a du lore, des interfaces glitchy, etc. Tout ça pour gérer tes fonctions cloud, ta todo list ou n’importe quoi. Le ciel est la limite.

## Je suis si seul (｡•́︿•̀｡)

Mon principal reproche : tout ça reste principalement **solo** — le mode « single player ».

J’ai codé des années seul, en pair, en équipe ; à plusieurs, c’est toujours mieux. Là, les bots se percutent, les merges deviennent atroces, le contexte est complexe.

Je veux vraiment qu’on transforme le dev avec LLM en expérience multijoueur, pas juste un trip de hacker solitaire. Il y a un boulevard à ouvrir.

AU BOULOT !

## ⴵ Temps ⴵ

La génération de code a multiplié la quantité de code qu’une seule personne peut produire. Effet secondaire étrange : beaucoup de « temps mort » pendant que le LLM brûle ses tokens.

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="Je m’en souviens comme si c’était hier" >}}

J’ai donc adapté ma façon de bosser pour combler ces attentes :

- je lance le brainstorming d’un autre projet ;
- j’écoute des vinyles ;
- je joue à [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/) ;
- je discute avec des amis et des robots.

C’est génial de hacker comme ça. Hack ! Hack ! Hack ! Je ne me souviens pas avoir été aussi productif.

## Haterade ╭∩╮( •̀_•́ )╭∩╮

Pas mal de potes me disent : « Les LLM, c’est naze. » Je respecte ce point de vue, même si je ne le partage pas. Il y a plein de raisons de se méfier de l’IA. Ma plus grande crainte : la conso électrique et l’impact environnemental. Mais… le code doit couler. *soupir*

Si tu es curieux sans vouloir devenir un « cyborg programmer », lis le livre d’Ethan Mollick : [**Co-Intelligence : Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/).

Bonne intro, sans le ton bro techno-libertarien. J’ai eu plein de discussions nuancées avec des amis après l’avoir lu. Recommandé.

Si tu es sceptique mais un peu curieux, contacte-moi et on parlera de toute cette folie. On pourra peut-être construire un truc ensemble.

_merci à [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com) et [Erik](https://thinks.lol/) d’avoir relu ce billet et proposé des modifs. Je vous suis reconnaissant._