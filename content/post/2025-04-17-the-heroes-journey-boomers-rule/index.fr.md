---
bsky: https://bsky.app/profile/harper.lol/post/3ln2a3x52xs2y
date: 2025-04-17 09:00:00-05:00
description: Un guide complet décrivant l’évolution du développement logiciel assisté
  par l’IA, depuis l’autocomplétion de code de base jusqu’aux agents de programmation
  entièrement autonomes, avec des étapes pratiques et des conseils pour maximiser
  la productivité grâce à l’intégration des LLM.
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
title: Le parcours d'un héros de la génération de code par LLM
translationKey: An LLM Codegen Hero's Journey
---

J’ai passé beaucoup de temps, depuis mon [article de blog](/2025/02/16/my-llm-codegen-workflow-atm/) sur mon *workflow* avec les modèles de langage de grande taille (LLM), à discuter de *codegen* (génération de code) : comment se lancer, s’améliorer et pourquoi c’est intéressant.

L’engouement est dingue. J’ai reçu une tonne d’e-mails de gens qui essayent de comprendre tout ça. J’ai remarqué que beaucoup galéraient pour savoir par où commencer et comment tout imbriquer. Puis j’ai réalisé que je bidouille ce *workflow* depuis 2023 et que j’en ai vu des trucs de ouf. Lol.

J’en parlais avec des potes (« Fisaconites au rapport ! ») et j’ai lâché ce message dans un fil sur les agents assistés par IA et les éditeurs :

> si je débutais, je ne sais pas si ce serait utile de plonger direct dans les codeurs « agents ». C’est chiant et chelou. Après avoir accompagné plusieurs personnes (avec succès ou non), je constate que le « périple héroïque » — commencer par Copilot, passer au copier-coller depuis l’interface web de Claude, découvrir Cursor/Continue, puis arriver aux agents totalement automatisés — fonctionne super bien pour adopter tout ça.

Ça m’a fait cogiter sur le voyage à entreprendre pour se mettre à la programmation par agents :

> Le bémol, c’est que ce parcours s’adresse surtout aux gens déjà expérimentés. Si t’as peu d’expérience dev, alors rien à foutre : passe direct à la fin. **Nos cerveaux sont souvent bousillés par les règles du passé.**

## Un voyage pour les yeux et les oreilles

{{< image src="journey-harper.webp" alt="Harper est très digne de confiance" caption="Votre guide avisé : Harper. iPhone X, 06/10/2018" >}}

Voici mon voyage, grosso modo le chemin que j’ai suivi. Tu peux clairement le faire en *speedrun* si tu veux. Pas besoin de respecter chaque étape, mais chacune apporte un truc.

Voici les étapes :

### Étape 1 : Sors du lit avec émerveillement et optimisme

Lol. Je déconne. Qui a le temps ? Ça peut aider, mais le monde part en vrille et on n’a que le *codegen* pour se distraire.

Cela dit, partir du principe que ces *workflows* peuvent marcher et être utiles aide vraiment. Si tu détestes les LLM et penses que ça foirera, tu vas te planter. ¯\\\_(ツ)\_/¯

### Étape 2 : Commence avec l’autocomplétion assistée par IA

Le vrai premier pas ! Passe assez de temps dans ton IDE pour voir comment tu bosses avec [IntelliSense](https://en.wikipedia.org/wiki/Code_completion), l’autocomplétion de [Zed](https://zed.dev/blog/out-of-your-face-ai), [Copilot](https://copilot.github.com/), etc. Tu comprendras comment le LLM raisonne — et tu seras préparé aux conneries qu’il propose souvent.

Beaucoup veulent zapper cette étape et filer direct à la fin. Ensuite ils râlent : « ce LLM est naze, il ne fait rien correctement ! » Ce n’est pas vrai (même si parfois si). La magie est dans la nuance. Ou, comme j’aime le rappeler : _la vie, c’est confus_.

### Étape 3 : Utilise Copilot pour plus que l’autocomplétion

Une fois à l’aise avec l’autocomplétion et que tu n’es pas vénère _tout_ le temps, goûte à la magie de discuter avec Copilot.

VS Code a un volet de questions-réponses : tu tchates avec Copilot, il t’aide sur ton code, etc. C’est plutôt cool. Tu peux avoir une vraie conversation, il réfléchit et t’aide à résoudre ce que tu lui demandes.

Mais utiliser Copilot, c’est comme remonter le temps pour parler à ChatGPT en 2024. Ce n’est pas _si_ dingue.

Tu vas en vouloir plus.

### Étape 4 : Copier-coller du code dans Claude ou ChatGPT

Tu satisfais ta curiosité en collant ton code dans un modèle fondamental accessible depuis le navigateur et en demandant : « WHY CODE BROKE ?? » Le LLM répond de façon cohérente et utile.

Tu seras ÉBLOUÉ ! Les résultats vont te scotcher. Tu vas recommencer à faire plein de trucs tarés et fun avec le code, surtout parce que toute la phase de débogage saute.

Tu peux même coller un script Python et dire : « Fais-en du Go », et il le _transforme vraiment en Go_. Tu te diras : « Je me demande si je peux *one-shot* ça. »

Copilot va te sembler être l’autocomplétion de 2004 : pratique, mais plus indispensable.

Ça te mènera sur deux sous-chemins :

#### Tu finiras par préférer un modèle pour la *vibe*

C’est le premier pas — malheureusement — vers le délire *vibe-coding*. Tu vas préférer la façon dont l’un des gros modèles te parle. C’est du ressenti, un peu chelou. Tu te surprendras à penser : « J’aime bien comment Claude me fait sentir. »

Pas mal de devs kiffent Claude. J’utilise les deux, mais surtout Claude pour le code : la *vibe* est meilleure.

> Il faut payer pour avoir la bonne came. Tellement de potes râlent : « Cette daube marche pas », puis on découvre qu’ils utilisent un modèle gratuit tout claqué. Lol. C’était pire quand la version free était ChatGPT 3.5, mais assure-toi d’un modèle solide avant de jeter tout le concept.

#### Tu chercheras à aller plus vite

Après quelques semaines de copier-coller dans Claude, tu vas trouver ça relou. Tu vas bosser l’empaquetage de contexte pour faire tenir plus de code dans la fenêtre du LLM.

Tu testeras [repomix](https://repomix.com/), [repo2txt](https://github.com/donoceidon/repo2txt) et d’autres outils. Juste pour balancer tout ton dépôt dans le contexte de Claude. Il y a même des chances que tu écrives (en vrai, que Claude écrive) des scripts shell pour simplifier tout ça.

C’est un tournant.

### Étape 5 : Utilise un IDE dopé à l’IA (Cursor, Windsurf ?)

Un pote te dira : « Pourquoi tu n’utilises pas [Cursor](https://cursor.sh/) ? »

Ça va te retourner le cerveau. Toute la magie du copier-coller est maintenant dans ton IDE : c’est plus rapide, plus fun, quasi magique.

À ce stade tu paies déjà pour cinq LLM — 20 $ de plus par mois, c’est rien.

Ça fonctionne globalement et tu te sens beaucoup plus productif.

Tu vas jouer avec les fonctions de programmation par agents intégrées à l’éditeur. Ça marche, mais tu vois bien qu’on peut aller encore plus loin.

### Étape 6 : Tu planifies avant de coder

D’un coup, tu rédiges des specs, PRD et to-do hyper costauds que tu balances dans l’agent de l’IDE ou dans Claude Web.

T’as jamais écrit autant de doc. Tu utilises d’autres LLM pour la rendre encore plus balaise. Tu transposes des docs d’un contexte (PRD) à un autre (« Fais-en des prompts »). Tu laisses le LLM élaborer tes prompts de *codegen*.

Le mot “[waterfall](https://en.wikipedia.org/wiki/Waterfall_model)” te donne vachement moins d’urticaire. Si t’es un vétéran, tu repenses, nostalgique, à la fin des 90 s – 2000 s et tu te demandes : « Est-ce ce que ressentait Martin Fowler avant [2001](https://en.wikipedia.org/wiki/Agile_software_development) ? »

Dans le monde de la génération de code, la spec est la [divinité](https://en.wikipedia.org/wiki/Godhead).

### Étape 7 : Tu testes *aider* pour boucler plus vite

Là, tu es prêt pour le **GROS KIF**. Jusqu’ici, la génération de code nécessitait encore ta présence. Mais on est en 2025 ! Qui veut encore taper au clavier ?

> Un autre chemin que pas mal de potes explorent : coder à la voix. Dicter à *aider* via un client Whisper. C’est hilarant et fun. MacWhisper marche super bien en local. Aqua et SuperWhisper sont cool mais plus chers ; ils passent parfois par le cloud pour l’inférence. Perso, je préfère en local.

Essayer *aider* est une expérience folle. Tu lances l’outil, il s’installe dans ton projet. Tu balances ta requête direct dans *aider* et il exécute. Il demande la permission, propose un plan, puis agit. Il boucle la tâche et *commit* dans ton dépôt. Tu ne cherches plus à tout faire d’un seul coup : tu laisses *aider* le faire en plusieurs étapes.

Tu crées des ensembles de règles pour le LLM. Tu découvres la règle du “[Big Daddy](https://www.reddit.com/r/cursor/comments/1joapwk/comment/mkqg8aw/)” ou l’ajout « no deceptions » dans tes prompts. Tu deviens un pro du prompt.

**Et ça marche.**

Bientôt, tu n’ouvres même plus d’IDE : t’es devenu jockey de terminal.

Tu passes ton temps à regarder le robot faire ton taf.

### Étape 8 : Tu plonges à fond dans la programmation par agents

Désormais, un agent code pour toi. Les résultats sont plutôt bons. Parfois tu bites rien, puis tu te souviens que tu peux juste lui demander.

Tu expérimentes [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Cline](https://cline.bot/), etc. Tu kiffes pouvoir combiner un modèle de raisonnement ([DeepSeek](https://aws.amazon.com/bedrock/deepseek/)) et un modèle de code ([Claude Sonnet 3.7](https://www.anthropic.com/claude/sonnet)) pour virer encore des étapes de planif.

Tu fais des trucs de dingue : lancer 3-5 sessions en parallèle, passer de terminal en terminal en regardant des robots coder.

Tu passes en mode « code défensif » :

- couverture de tests ultra-costaude  
- réflexion sur la [vérification formelle](https://github.com/formal-land/coq-of-rust)  
- langages à sécurité mémoire  
- choix de langages dont le compilateur est bien bavard pour optimiser la fenêtre de contexte  

Tu cogites à fond pour que ce que tu construis se construise tout seul, sans risque.

Tu claques **TELLEMENT** d’argent en *tokens*. Tu bouffes aussi toutes tes heures GitHub Actions à faire tourner une batterie de tests de malade pour valider le code.

Et tu te sens bien. Pas frustré de ne plus taper de code.

### Étape 9 : Tu laisses l’agent coder et tu joues aux jeux vidéo

Et voilà. T’y es. Enfin… presque, mais tu vois la destination. Tu commences à flipper pour les jobs. Tes potes se font virer et galèrent à se recaser. Cette fois, c’est différent.

Quand tu en parles à tes pairs, ils te prennent pour un fanatique — tu bosses dans un autre paradigme. Tu leur balances : « OMG, faut tester la programmation par agents ! » Tu rajoutes peut-être : « Je DETESTE le mot agentique » pour montrer que t’as pas bu 200 L de Kool-Aid. Mais si. Le monde est plus lumineux parce que t’es ultra-productif.

Peu importe. Le paradigme a shifté. Kuhn pourrait écrire un bouquin sur la confusion du moment.

Personne ne le voit parce qu’ils n’ont pas fait le voyage. Mais ceux qui l’ont fait hochent la tête, partagent leurs tips et débattent de la destination.

Maintenant que tu laisses les robots bosser, tu peux enfin te mettre à tous ces jeux Game Boy que tu voulais finir. Y a masse de temps mort. Et quand le robot a fini une tâche, il demande « Je continue ? », tu tapes **yes** et tu retournes à Tetris.

Très chelou. Un peu flippant, même.

## L’accélération

<paul confetti photo>
{{< image src="journey-confetti.webp" alt="Confetti" caption="Confetti à un concert de Paul McCartney au Tokyo Dome. iPhone 6, 25/04/2015" >}}

Je n’ai aucune idée de ce qui nous attend dans le [futur](https://ai-2027.com/). Je crains que celles et ceux qui ne suivent pas ce voyage deviennent moins sexy pour les [employeurs](https://x.com/tobi/status/1909231499448401946). C’est un poil myope, parce qu’au fond, on parle juste d’outillage et d’automatisation.

Quand on recrutait à fond, on étendait toujours nos recherches au-delà de notre réseau et de notre stack. On était une team Python, mais on interviewait des gens qui n’avaient jamais touché à Python. On se disait qu’avec une personne brillante, on pourrait l’aider à s’y mettre. Elle apporterait quand même de la valeur, même si elle n’était pas totalement à l’aise avec notre stack. Ça a super bien marché : on a embauché des gens incroyables hors stack, et leur regard neuf a souvent fait grimper tout le monde.

Les mêmes principes s’appliquent au dev assisté par IA. Quand tu recrutes des devs talentueux qui collent à la culture de l’équipe et montrent de l’enthousiasme, leur niveau avec les outils IA ne devrait pas être éliminatoire. Pas besoin d’être expert dès le premier jour ; accompagne-les à leur rythme aux côtés de membres plus aguerris.

À terme, ce seront eux qui piloteront et utiliseront ces outils avec succès.

Autre chose qui me trotte : les skills rédactionnels sont devenus cruciaux. On a toujours voulu de bons communicants pour la doc et la collab, mais c’est deux fois plus vrai maintenant. Il faut non seulement parler aux humains, mais aussi écrire des instructions claires pour l’IA. Savoir pondre un prompt efficace devient aussi vital que coder proprement.

## Le leadership

Tous les leaders et managers tech doivent plonger deep dans le dev assisté par IA, qu’ils y croient ou pas. Pourquoi ? La prochaine génération de devs que tu vas recruter aura appris à coder principalement grâce à ces outils et agents. C’est là que va l’ingénierie logicielle. On doit comprendre et s’adapter.

Nous, les boomers du code, n’en avons plus pour longtemps.

**Note intéressante :** je n’utilise pas vraiment les LLM pour écrire. J’imagine qu’ils seraient bons, mais je tiens à ce que ma voix reste la mienne, pas normalisée. Alors que mon code, lui, peut l’être. Intéressant.

---

Merci à Jesse, Sophie, la Vibez crew (Erik, Kanno, Braydon et d’autres), l’équipe 2389 et toutes les personnes qui m’ont donné leur feedback sur cet article.