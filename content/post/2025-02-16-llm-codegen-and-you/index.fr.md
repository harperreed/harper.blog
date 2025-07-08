---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: Un aperçu détaillé de mon flux de travail actuel pour utiliser les LLM
  afin de développer des logiciels, de la phase de remue-méninges jusqu’à la planification
  et l’exécution.
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
title: Mon flux de travail de génération de code LLM en ce moment
translationKey: My LLM codegen workflow atm
---

_TL;DR — On peaufine d’abord la spécification au moyen de séances de brainstorming, on élabore ensuite un plan, puis on exécute grâce à la génération de code par LLM. Boucles distinctes. Et, au bout du compte, la magie. ✩₊˚.⋆☾⋆⁺₊✧_

J’ai enchaîné les petits projets à base de LLM : c’est fun et utile, mais les pièges peuvent faire perdre un temps fou. Il y a quelque temps, un ami m’a demandé comment j’utilisais les LLM pour coder. Je me suis dit : « Ouh là ! Tu as combien de temps ? » — d’où ce billet.

(p.s. : si vous détestez l’IA, filez directement à la fin)

Je discute souvent avec des amis dev ; chacun bidouille un peu différemment, mais on suit globalement la même approche.

Voici donc ma démarche. Elle s’appuie sur mon expérience, des échanges avec des amis (merci [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki) et [Erik](https://thinks.lol/)), ainsi que sur pas mal de bonnes pratiques glanées dans les recoins (parfois douteux) du Net : [ici](https://news.ycombinator.com/) et [là](https://twitter.com).

Ça marche très bien **MAINTENANT** ; dans deux semaines, ce sera peut-être cassé… ou deux fois plus efficace. ¯\\\_(ツ)\_/¯

## Allons-y

{{< image src="llm-coding-robot.webp" alt="Robot Juggalo" caption="Je me méfie toujours un peu de ces images générées par IA. Dites bonjour à mon ange robot juggalo codeur !" >}}

Il existe mille façons de développer, mais je me retrouve généralement dans l’un de ces deux cas :

- Code neuf (greenfield)  
- Code existant moderne (legacy modern/brownfield)

Voici mon mode opératoire pour chacun.

## Greenfield

Pour un projet neuf, la démarche qui suit fonctionne bien : planification et documentation béton, puis exécution en petites étapes.

{{< image src="greenfield.jpg" alt="Champ vert" caption="Techniquement, il y a un champ vert à droite. Leica Q, 14/05/2016" >}}

### Étape 1 : affiner l’idée

Utilisez un LLM conversationnel pour clarifier l’idée (j’emploie ChatGPT 4o / o3) :

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

À la fin du brainstorming (vous le sentirez) :

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

Vous obtenez ainsi une spécification carrée, prête pour la phase suivante. Je la sauvegarde en `spec.md` dans le dépôt.

> On peut faire plein de choses avec cette spécification. Ici on fait de la génération de code, mais je l’ai déjà utilisée pour demander à un modèle de raisonnement de percer des trous dans l’idée (toujours plus !), rédiger un white paper ou carrément un business model. Vous pouvez même lancer une recherche approfondie et recevoir un doc de 10 k mots en retour.

### Étape 2 : planification

Passez la spécification à un modèle de raisonnement (« o1* », « o3* », « r1 »).

(Prompt – TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(Prompt – non-TDD)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

Le modèle doit produire un plan de prompts exécutable avec Aider, Cursor, etc. Je l’enregistre en `prompt_plan.md` dans le dépôt.

Je lui fais ensuite générer un `todo.md` :

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

Enregistrez-le dans le dépôt.  
L’outil de génération pourra cocher les cases de `todo.md` en avançant : parfait pour garder l’état d’une session à l’autre.

#### Yay. Plan !

Vous avez maintenant un plan solide et une documentation de référence qui vous permettront de garder le cap.  
Le tout prend **environ 15 minutes**. Dingue.

### Étape 3 : exécution

Il existe un tas d’options pour l’exécution. Le succès dépend surtout de la qualité de l’étape 2.

J’ai testé ce flux de travail avec [GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude Engineer](https://github.com/Doriandarko/claude-engineer), [sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [claude.ai](https://claude.ai), etc. Ça tourne avec tout ce que j’ai essayé — et sûrement avec n’importe quel outil de génération de code.

Perso, je préfère **Claude en mode natif** et Aider.

### Claude

Je fais du pair-programming sur [claude.ai](https://claude.ai) : je soumets les prompts l’un après l’autre. Les allers-retours sont parfois pénibles, mais ça fonctionne.

Je suis responsable du boilerplate et de la config au départ : ça évite que Claude parte par défaut sur du React et ça fixe la stack de mon choix.

Quand ça bloque, j’utilise [repomix](https://github.com/yamadashy/repomix) pour filer toute la base de code à Claude et déboguer.

Flux :

- initialiser le dépôt (boilerplate, `uv init`, `cargo init`, etc.)  
- coller le prompt dans Claude  
- copier-coller le code dans l’IDE  
- exécuter le code, lancer les tests, etc.  
- …  
- si ça passe : prompt suivant  
- sinon : repomix + Claude pour déboguer  
- on recommence ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) est fun et un peu étrange. Il s’emboîte nickel avec la sortie de l’étape 2 : on avance très vite avec presque rien.

Même flux, mais en collant les prompts dans Aider, qui « fait le taf » pendant qu’on joue à [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/).

> Au passage : Aider publie d’excellents benchmarks des nouveaux modèles dans ses [LLM leaderboards](https://aider.chat/docs/leaderboards/) — super pour jauger les dernières bêtes.

Les tests ? Encore plus simple : Aider lance la suite et corrige.

Flux :

- init du dépôt (boilerplate, `uv init`, `cargo init`, etc.)  
- lancer Aider  
- coller le prompt  
- regarder Aider danser ♪┏(・o･)┛♪  
- Aider lance les tests, ou vous exécutez pour vérifier  
- si ça passe : prompt suivant  
- sinon : Q/R avec Aider  
- on recommence ✩₊˚.⋆☾⋆⁺₊✧

### Résultats

J’ai bâti une tonne de trucs avec ce flux : scripts, apps Expo, CLI Rust, etc. Ça marche quel que soit le langage et le contexte.

Si vous repoussez un projet, petit ou gros, testez-le : vous serez bluffé·e par la vitesse d’avancement.

Ma todo « hacks » est vide parce que j’ai tout fait. Je pense à un nouveau truc, je le sors en regardant un film. Pour la première fois depuis des années, je joue avec de nouveaux langages et outils : ça élargit ma perspective de dev.

## Legacy modern (Brownfield) : itérer, petit à petit

Parfois, pas de terrain vierge : il faut améliorer une base de code existante.

{{< image src="brownfield.jpg" alt="un champ brun" caption="Ce n’est pas un champ vert. Photo prise par mon grand-père – quelque part en Ouganda dans les années 60" >}}

La méthode est proche, mais moins centrée sur un grand plan ; on planifie tâche par tâche.

### Choper le contexte

Chacun a son outil, mais il faut extraire la base de code et l’injecter efficacement dans le LLM.

J’utilise [repomix](https://github.com/yamadashy/repomix) avec des tâches définies dans `~/.config/mise/config.toml`.

Liste :

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

Je génère un `output.txt` avec le contexte. Si je **crame trop de jetons** et que le bundle est trop volumineux, j’ajuste pour ignorer ce qui n’est pas utile.

> Avantage de `mise` : on peut redéfinir ces tâches dans le `.mise.toml` du projet. Tant que ça sort un `output.txt`, mes commandes LLM tournent. Top quand les bases de code divergent.

Une fois `output.txt` prêt, je passe ça à [LLM](https://github.com/simonw/LLM) pour diverses transformations, puis je sauvegarde en Markdown.

```shell
cat output.txt | LLM -t readme-gen > README.md
# ou
cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md
```

> Ce n’est pas très compliqué : la commande `LLM` fait le gros du travail (gestion des modèles, des clés et des templates de prompt).

Besoin d’un examen express **et d’une correction** de la couverture de tests ? Voilà :

#### Claude

- se placer dans le dossier  
- `mise run LLM:generate_missing_tests`  
- ouvrir `missing-tests.md`  
- copier le bundle : `mise run LLM:copy_buffer_bundle`  
- coller le tout dans Claude avec la première *issue*  
- copier le code généré dans l’IDE  
- …  
- lancer les tests  
- on recommence ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- se placer dans le dossier  
- lancer Aider (sur une branche dédiée)  
- `mise run LLM:generate_missing_tests`  
- ouvrir `missing-tests.md`  
- coller la première *issue* dans Aider  
- regarder Aider danser ♪┏(・o･)┛♪  
- …  
- exécuter les tests  
- on recommence ✩₊˚.⋆☾⋆⁺₊✧

Méthode efficace pour améliorer progressivement une grosse base de code ; j’ai pu prendre des tâches de toute taille avec ça.

### Magie des prompts

Ces mini-hacks permettent de repérer très vite les points à renforcer dans un projet. C’est extrêmement rapide et efficace.

Quelques-uns de mes prompts :

#### Revue de code

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

Ces prompts sont un peu *old and busted* (« prompts de boomer », quoi). Ils méritent un refacto. Si vous avez des idées, faites signe !

## Le ski ᨒ↟ 𖠰ᨒ↟ 𖠰

Quand j’explique ce processus, je dis toujours qu’il faut **suivre de près tout ce qui se passe, sinon on se retrouve vite “over one’s skis”** — autrement dit, on va trop vite et on perd le contrôle.

La phase **planification** (cf. Greenfield) aide à rester droit : au moins, vous avez un doc de référence sur lequel revenir. Je crois aussi que les tests sont indispensables — surtout en freestyle avec Aider — pour garder un code propre et rigoureux.

Malgré ça, je me retrouve encore souvent *over my skis*. Parfois, une pause ou une courte marche suffit. C’est du problem-solving classique… mais en accéléré.

> On demande parfois au LLM d’ajouter des trucs improbables dans un code pas si improbable. Exemple : créer un fichier de *lore*, des interfaces bancales (*glitchy interfaces*), puis les référencer dans l’UI. Tout ça pour simplement gérer tes fonctions cloud, ta todo-list, ou n’importe quoi d’autre. Tout est possible.

## Je me sens seul (｡•́︿•̀｡)

Mon principal reproche : tout ça se joue surtout en solo — des interfaces « single player ».

J’ai codé seul, en binôme, en équipe ; c’est toujours mieux à plusieurs. Ces flux ne sont pas simples à partager : bots qui se marchent dessus, merges horribles, contexte compliqué.

Je rêve d’une solution pour que coder avec un LLM devienne un jeu multi, pas une expé de hacker solitaire. Il y a un boulevard : **AU BOULOT !**

## ⴵ Temps ⴵ

Toute cette génération de code a décuplé ce qu’une seule personne peut produire. Effet secondaire : pas mal de temps mort en attendant que le LLM brûle ses jetons.

{{< image src="apple-print-shop-printing.png" alt="Impression" caption="Je m’en souviens comme si c’était hier" >}}

J’ai donc adapté ma façon de bosser pour occuper ces moments :

- je lance le brainstorming d’un autre projet  
- j’écoute des vinyles  
- je joue à [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/)  
- je papote avec des amis (humains ou robots)

C’est génial de hacker comme ça. Hack ! Hack ! Hack ! Je n’ai jamais été aussi productif.

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

Pas mal d’amis me disent : « fuck les LLM, c’est naze. » Je **ne partage pas** cette opinion, mais je pense qu’il est sain de rester sceptique. Les raisons de haïr l’IA ne manquent pas. Ma crainte principale : la consommation d’énergie et l’impact sur le climat. Mais… *the code must flow*. *Sigh*.

Si vous voulez creuser sans devenir un·e dev cyborg, lisez le bouquin d’Ethan Mollick : [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/).

Ça expose bien les bénéfices sans le ton techno-libertarien. J’ai eu plein de discussions nuancées avec des amis qui l’ont lu. Recommandé.

Sceptique mais un peu curieux·se ? Pinguez-moi : je peux vous montrer comment on se sert des LLM, et on pourra peut-être construire quelque chose ensemble.

_thanks to [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com), and [Erik](https://thinks.lol/) for taking a look at this post and suggesting edits. I appreciate it._