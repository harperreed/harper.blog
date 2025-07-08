---
date: 2025-04-10
description: Une exploration de la manière dont l’IA accélère les méthodes de développement
  traditionnelles en cycles Waterfall rapides de 15 minutes, transformant ainsi les
  flux de travail de l’ingénierie logicielle et la dynamique des équipes.
draft: false
generateSocialImage: true
generated: true
slug: waterfall-in-15-minutes-or-your-money-back
tags:
- llm
- large-language-models
- code-generation
- ai
- artificial-intelligence
- coding
- programming
- workflow
- software-development
- development-practices
- productivity
- automation
title: La méthode Waterfall en 15 minutes ou remboursé
translationKey: Waterfall in 15 Minutes or Your Money Back
---

J’ai récemment discuté avec un ami ; ce qui devait être un simple rattrapage s’est vite mué en plongée profonde dans le codage assisté par l’IA et son impact sur nos flux de travail, nos équipes et notre dimension « artisanale ». On a parlé de réécrire d’anciennes bases de code et de la manière dont la couverture de tests automatisée transforme la programmation elle-même.

J’ai récupéré la transcription sur Granola et je l’ai copiée dans o1-pro pour lui demander d’en faire un billet de blog. Résultat : pas mal, et plutôt fidèle à mes convictions.

Je l’ai envoyé à quelques amis, qui ont tous voulu le transmettre à d’autres. Me voilà donc obligé de le publier : allons-y !

> Petit rappel : si vous recevez un e-mail impeccable, sans la moindre affectation, il a probablement été écrit par une IA. lol.

---

## Waterfall (cycle en cascade) en 15 minutes – sinon, on vous rembourse !

### La nouvelle norme : « La qualité du code, ça compte encore ? »

Pendant des années, nous avons décrit le code comme un artisanat : on entre dans l’état de flow, on sculpte une logique, et l’on ressort vainqueur, avec des correctifs faits main. Désormais, un nouveau paradigme s’installe : les outils de génération de code — les LLM (« large language models », ou grands modèles de langage) — peuvent littéralement cracher des fonctionnalités à la chaîne en quelques minutes.

Certains sont ébranlés par cette cadence, qui bouscule les vieux préceptes du « clean code ». Soudain, rédiger une suite de tests robuste — ou pratiquer le TDD — consiste surtout à laisser les bots s’auto-vérifier plutôt qu’à passer méthodiquement chaque ligne au peigne fin.

La qualité va-t-elle plonger ? Peut-être. Parallèlement, on voit émerger une programmation ultra-défensive : analyse statique, vérification formelle, couverture de tests omniprésente… autant de filets pour détecter illico la moindre régression qu’un agent IA pourrait introduire. Nous n’avons jamais eu autant besoin de pipelines CI/CD (intégration et déploiement continus) et de contrôles rigoureux.

---

### Waterfall en 15 minutes

{{< image src="waterfall.webp" alt="Waterfall" caption="En Islande, les cascades ne manquent pas. Leica Q, 30 septembre 2016" >}}

On opposait jadis Waterfall et Agile comme deux religions, Agile étant la seule voie vertueuse. Ironiquement, la génération de code nous ramène vers de micro-cycles en mode Waterfall : on définit soigneusement le cahier des charges (l’IA exige de la clarté), on appuie sur « Générer », on attend que le code sorte, puis on relit. Sur le papier, ça ressemble toujours à de l’itératif ; en pratique, c’est planification, exécution, revue, point. « Waterfall en 15 minutes ».

La vraie magie ? Vous pouvez lancer plusieurs agents simultanément. Tandis qu’une IA construit une fonctionnalité, une autre rédige la documentation, et une troisième analyse votre couverture de tests. Ce n’est plus l’ancienne cascade linéaire : c’est de la concurrence (et du parallélisme) sous stéroïdes.

---

### La culture d’équipe va changer

Si vous dirigez une équipe d’ingénierie, la direction vous demande sans doute : « Et l’IA pour booster notre productivité ? ». Pourtant, l’enthousiasme varie au sein de votre équipe. Certains sont à fond — des fonctionnalités entières générées par prompt — tandis que d’autres restent attachés à leur identité d’artisan.

Voici, selon moi, ce qui fonctionne :

1. **Lancez de petits pilotes**  
   Choisissez un projet interne ou un outil à faible risque, et laissez quelques esprits curieux se lâcher avec l’IA. Laissez-les casser des trucs, expérimenter, accorder (parfois trop) de confiance au modèle ; observez ensuite comment ils réintroduisent les bonnes pratiques.

2. **Faites tourner les membres de l’équipe**  
   Un projet annexe « codé par IA » permet de faire passer les membres tour à tour : une ou deux semaines dans ce nouvel environnement, chacun apprend des autres, puis ramène ces leçons dans la base de code principale.

3. **Prenez la documentation très au sérieux**  
   Les agents IA exigent des spécifications limpides. Générer du code coûte peu, mais guider un LLM demande une préparation minutieuse. Pour que toute l’équipe en profite, placez vos meilleures specs et documents d’architecture dans un dépôt partagé. Vous vous remercierez lors des rotations.

---

### Et si le flow était surcoté ?

Découverte surprenante : beaucoup d’entre nous se sont mis au code pour l’état de flow — ce moment où l’on est « dans la zone ». Or le codage assisté par IA ne déclenche pas toujours cette immersion. On peut passer une heure à préparer des prompts (instructions), laisser l’IA travailler en arrière-plan, et revenir de temps à autre pour valider ou ajuster.

Pour certains, c’est déroutant ; pour d’autres — parents ou jongleurs de mille tâches — c’est libérateur. Pouvoir changer de contexte : examiner la sortie de l’IA, retourner à la vie réelle, puis revenir sur un snippet fonctionnel… voilà un nouveau mode de productivité qui ne dépend plus de longues plages de silence.

---

### Sommes-nous à l’« apogée du développeur » ?

On entend dire que si l’IA génère le code, on aura bientôt besoin de moins d’ingénieurs. Cela peut être vrai pour les fonctionnalités basiques ou le simple raccordement à une API. Mais de nouvelles complexités surgissent : sécurité, conformité, couverture de tests, architecture…

La différence ? Les ingénieurs stratégiques vont prospérer : capables d’orchestrer plusieurs outils d’IA, de surveiller la qualité et de concevoir des systèmes qui passent à l’échelle. À la fois chef·fe de produit, architecte, analyste QA et développeur·se, ils rédigent les prompts, définissent les tests, maintiennent la qualité et gèrent tous les cas limites qu’un LLM n’anticipe pas.

---

### Conseils de terrain

Quelques leçons apprises à la dure :

1. **Commencez manuellement, puis activez l’IA**  
   Pour une app iOS, initialisez d’abord le projet dans Xcode afin que les fichiers auto-générés n’embrouillent pas le modèle. Ensuite, laissez-le compléter.

2. **Des prompts courts et clairs valent parfois mieux que de longues instructions détaillées**  
   Étonnamment, demander à un LLM « améliore ce code » fonctionne parfois aussi bien qu’un prompt ultra-développé. Expérimentez : certains modèles préfèrent moins de contraintes.

3. **Adoptez des points de contrôle**  
   Committez souvent, même un `git commit -m "Ça passe les tests, je suppose !"`. Une IA peut tout casser aussi vite qu’elle répare. Ces commits servent de points de retour pratiques.

4. **Évitez de tester l’évidence**  
   L’IA adore tout tester, y compris vérifier qu’une boucle `for` boucle encore. Restez vigilant : élaguez les tests inutiles pour garder votre pipeline léger.

5. **Documentez absolument tout**  
   Laissez l’IA générer de grands « Guides d’implémentation ». Ils vous aident… et aident aussi le modèle lors des passes suivantes.

---

### Dernières réflexions

{{< image src="waterfall-road.webp" alt="Road to the future" caption="Route vers le futur. Le Colorado est étonnamment plat. Leica Q, 14 mai 2016" >}}

Notre secteur évolue plus vite que jamais. Certaines de nos certitudes — l’importance du flow, les grandes célébrations autour de fonctionnalités méticuleusement codées à la main — vont bientôt paraître désuètes. Mais notre créativité ne disparaît pas ; elle devient une orchestration stratégique : savoir quoi construire, comment le décrire et empêcher que tout parte en fumée.

Au final, ce qui fera gagner votre produit, ce n’est pas la masse de code produite, mais l’expérience offerte aux utilisateurs. Si l’on peut cloner Instagram dix fois en un week-end, le critère décisif ne sera pas l’élégance du code, mais le produit qui résonnera le plus avec les gens — un défi de design et de produit, pas seulement d’ingénierie.

Bienvenue donc dans cette nouvelle cascade : des cycles de 15 minutes, une IA comme junior inépuisable et un pipeline en surmultipliée. C’est à la fois étrange, merveilleux et parfois terrifiant. Et il y a fort à parier que nous allons tous devoir apprendre cette chorégraphie, d’une façon ou d’une autre.

---

_C’est quand même un drôle de monde. Je pense que les choses vont continuer à devenir étranges. Creusons._