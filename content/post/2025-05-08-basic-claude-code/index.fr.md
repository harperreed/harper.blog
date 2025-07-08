---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description: Un guide détaillé sur l’utilisation de l’assistant IA Claude Code pour
  le développement logiciel, incluant des conseils de flux de travail, des pratiques
  de test et des exemples pratiques tirés de projets réels. Couvre les stratégies
  de programmation défensive, le TDD et la mise en œuvre au sein d’une équipe.
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
title: Code Claude de base
translationKey: Basic Claude Code
---

J’adore vraiment cette « agentic coding ». C’est incroyablement fascinant à bien des égards.

Depuis que j’ai rédigé [ce billet de blog original](/2025/02/16/my-llm-codegen-workflow-atm/), beaucoup de choses se sont passées dans le monde de Claude :

- Claude Code  
- MCP  
- etc.

J’ai reçu des centaines (*« wat »*) d’e-mails de personnes m’expliquant leur workflow et comment elles se sont appuyées sur le mien pour prendre de l’avance. J’ai présenté le sujet lors de quelques conférences et donné plusieurs cours sur le codegen. J’ai aussi découvert que les ordinateurs veulent absolument corriger « codegen » en « codeine » — qui l’eût cru !

{{< image src="codegen.png"  >}}

Je discutais l’autre jour avec une [amie](https://www.elidedbranches.com/) de la façon dont **nous sommes TOUS totalement FOUTUS** et dont **l’IA va nous piquer nos boulots** (j’y reviendrai dans un prochain post). Elle m’a lancé : « Tu devrais écrire un article sur Claude Code. »

C’est parti.

Claude Code est sorti huit jours après mon billet sur le workflow et, comme je l’avais prédit, une bonne partie de ce billet est devenue caduque. J’ai depuis migré d’Aider vers Claude Code sans jamais revenir en arrière. J’aime toujours Aider, qui a son utilité propre, mais Claude Code est un peu plus pratique en ce moment.

Claude Code est puissant… et sacrément plus cher.

Mon workflow reste très proche de l’ancien :

- Je discute avec `gpt-4o` pour affiner mon idée.  
- J’utilise le meilleur modèle de raisonnement disponible pour générer la spec : en ce moment o1-pro ou o3 (o1-pro est-il vraiment meilleur qu’o3 ou est-ce juste parce qu’il tourne plus longtemps ?).  
- Je me sers ensuite du même modèle pour produire les prompts ; faire écrire les prompts par un LLM est un hack magnifique — et, cerise sur le gâteau, ça rend les boomers dingues.  
- J’enregistre `spec.md` et `prompt_plan.md` à la racine du projet.  
- Puis je tape dans Claude Code :

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

- La magie de ce prompt, c’est qu’il lit `@prompt_plan.md`, repère ce qui n’est pas marqué comme terminé, exécute la prochaine tâche, s’assure que les tests passent et que le programme se compile/s’exécute, commite sur Git avec un message clair, met à jour le plan de prompts, puis s’arrête et me demande si l’on continue. 🤌  
- Je me cale dans mon siège et je tape simplement « yes » pendant qu’il travaille. Il me demande un retour, et la magie opère.  
- Encore plus de clics façon Cookie Clicker.

Ça fonctionne vraiment bien. Il existe quelques super-pouvoirs que vous pouvez intégrer à votre processus et qui aideront énormément.

## Code défensif !

### Tests

Les tests et le développement piloté par les tests (TDD) sont indispensables. Je vous recommande vivement de mettre en place une pratique TDD robuste.

J’étais nul en TDD et j’avais l’impression de perdre mon temps. Je me trompais, lol. Au fil des décennies, nous avons ajouté beaucoup de tests dans nos entreprises et projets, mais souvent APRÈS le travail principal ; c’est tolérable pour des humains.

C’EST MAUVAIS POUR LES ROBOTS.

Les robots ADORENT le TDD. Sérieusement, ils en raffolent.

Avec le TDD, votre pote robot écrit d’abord le test et le mock. Au prompt suivant, vous remplacez le mock par la vraie implémentation. Et le robot jubile. C’est, à ce jour, la contre-mesure la plus efficace que j’aie trouvée contre les hallucinations et le « scope drift » (dérive de périmètre) des LLM ; ça les aide vraiment à rester concentrés.

### Linting

Je suis un grand fan du linting : c’est tellement agréable. Ruff est excellent. Biome est chouette. Clippy est fun (et le nom est bon).

Pour une raison obscure, les robots tiennent à exécuter un bon linter.

Intégrer le linting en continu éloigne nombre de bugs, garde le code lisible et facile à maintenir. Vous connaissez déjà la chanson.

Ajoutez un bon formatter de code et tout devient superbe.

### Hooks pré-commit

Le vrai hack consiste à regrouper toutes ces vérifications dans un hook pré-commit. Je recommande le package Python `pre-commit`. Installez-le simplement avec `uv tools install pre-commit`, créez un joli fichier `.pre-commit-config.yaml` et bam : à chaque tentative de commit, il lance tous les tests, la vérification de types, le linting, etc., pour garantir un code A+++ prêt à s’exécuter.

C’est parfait avec Claude Code. Le robot VEUT vraiment commiter. Donc, quand vous lui demandez de coder puis de commiter (comme plus haut), il peut effectuer des changements audacieux, commiter, tout foutre en l’air, puis devoir réparer.

L’avantage : vous ne saturerez pas vos GitHub Actions avec du linting, du formatage ou du type-checking qui échouent parce que le robot était de mauvaise humeur.

> Un truc amusant avec Claude, c’est qu’il est INCAPABLE de comprendre comment utiliser `uv` correctement. Il va lancer des `pip install` partout si vous ne faites pas attention. Et si vous l’invitez à utiliser `uv`, il se contente de faire `uv pip install`. Peut-être que l’AGI n’arrivera pas en juin. Triste.

### Claude.md et commandes

Deux petites additions simples qui peuvent faire toute la différence.

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

J’ai repris un [CLAUDE.md](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md) de mon ami [Jesse Vincent](https://fsck.com/) qui a [énormément bossé pour le rendre très complet](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md). On y trouve notamment :

- une version allégée de la « big daddy rule » ;  
- des instructions TDD ;  
- mes préférences stylistiques de code.

> [@clint](https://instagram.com/clintecker) a configuré son CLAUDE.md pour qu’il l’appelle MR BEEF, et cela insère désormais des références à MR BEEF dans toute notre documentation : « If you're stuck, stop and ask for help—MR BEEF may know best. ». En écrivant ceci, j’ai décidé que mon CLAUDE.md m’appellerait « Harp Dog ». C’est une fonctionnalité, pas un bug.

Les commandes sont également très utiles. Vous pouvez voir les miennes dans mes dotfiles [ici](https://github.com/harperreed/dotfiles/tree/master/.claude/commands).

{{< image src="commands.png"  >}}

Je les utilisais beaucoup plus avant, mais c’est un excellent moyen de réutiliser des prompts fréquents. Vous pouvez même passer des arguments. Par exemple, dans ma commande GitHub issues, vous transmettez le numéro de l’issue : `/user:gh-issue #45`.

Claude exécutera alors le script décrit dans `gh-issue.md`.

Vous pouvez aussi placer ces commandes dans le répertoire d’un projet et y ajouter un CLAUDE.md spécifique. Je fais cela pour avoir des commandes dédiées à Hugo, Rust, Go ou JavaScript selon le projet.

## « Continue »

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

Parfois, je me sens comme le petit oiseau oscillant que Homer fait appuyer sur la touche « Y ». Je tape simplement « continue » ou j’appuie sur ↑ puis Entrée.

La plupart du temps, les plans comptent 8 à 12 étapes. Je termine généralement un projet *greenfield* en 30-45 minutes, quelle que soit la complexité apparente ou le langage.

Je discutais avec mon ami Bob, qui ne me croyait pas. Je lui ai dit : « Donne-moi quelque chose à construire et un langage, on verra ! »

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

Il a répliqué : « OK. Un interpréteur BASIC en C. »

Pas idéal : je ne connais pas vraiment le C, je sais à peine écrire un interpréteur et, pour être honnête, je n’en ai pas très envie. Mais fuck it.

J’ai suivi les étapes ci-dessus et Claude Code s’en est sorti. Nous avons désormais [un interpréteur BASIC fonctionnel](https://github.com/harperreed/basic). La première version tournait au bout d’une heure. J’ai encore peaufiné quelques heures et c’est plutôt bon. Est-ce que ça aurait pu sortir en 1982 ? Probablement pas. Vous pouvez consulter le [plan de prompts ici](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md).

## L’équipe

Toute notre équipe utilise actuellement Claude Code. Nous suivons tous à peu près le processus ci-dessus, chacun avec ses ajustements personnels.

Nous atteignons une couverture de tests bien plus élevée qu’auparavant. Le code est meilleur, et il semble tout aussi efficace que l’horreur que nous écrivions autrefois. C’est amusant de jeter un œil et de voir Claude Code tourner dans Ghostty, dans le terminal de VS Code, le terminal Zed, ou encore s’attaquer à des notebooks Python.

{{< image src="dril.jpg" >}}

Quelqu’un qui dispose de beaucoup de tokens : aidez-moi à budgéter tout ça, ma famille est en train de mourir.

## Merci

À toutes celles et ceux qui continuent de m’écrire : c’est fantastique de découvrir vos workflows et projets. J’adore vous lire. Continuez !