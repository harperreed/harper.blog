---
date: 2024-04-12 09:00:00-05:00
description: J'ai créé un moteur de recherche de mèmes magique grâce à siglip/CLIP
  et à l'encodage vectoriel des images. C'était une façon amusante de découvrir cette
  technologie puissante. Je partage le code pour que vous puissiez créer le vôtre
  et redécouvrir des pépites oubliées dans votre bibliothèque de photos. Libérons
  la puissance de l'IA sur nos images !
draft: false
generateSocialImage: true
slug: i-accidentally-built-a-meme-search-engine
tags:
- meme-search-engine
- vector-embeddings
- applied-ai
- siglip
- image-search
title: J'ai accidentellement créé un moteur de recherche de mèmes
translationKey: I accidentally built a meme search engine
---

## Ou : comment découvrir CLIP/SigLIP et l’encodage vectoriel d’images

_tl;dr_ : j’ai bricolé un moteur de recherche de mèmes avec SigLIP/CLIP et l’encodage vectoriel des images. C’était fun et j’ai beaucoup appris.

Je bidouille des outils d’IA appliquée depuis un moment. Un composant qui m’a toujours paru carrément magique, ce sont les embeddings (représentations vectorielles). [Word2Vec](https://en.wikipedia.org/wiki/Word2vec) et consorts m’ont littéralement retourné le cerveau : on dirait de la sorcellerie.

J’ai vu une [petite appli sur Hacker News](https://news.ycombinator.com/item?id=39392582) qui était [vraiment bluffante](https://mood-amber.vercel.app/). Quelqu’un a aspiré un paquet d’images Tumblr, a utilisé [SigLIP](https://arxiv.org/abs/2303.15343) pour générer les embeddings, puis a pondu une appli toute simple : « clique sur une image et découvre celles qui lui ressemblent ». Magique. Je n’avais aucune idée de la recette, mais ça paraissait faisable.

J’ai profité de cette montée d’adrénaline pour comprendre « comment tout ça fonctionne ».

## wut

Si vous n’avez jamais croisé d’embeddings, de CLIP/SigLIP ou de bases de données vectorielles, pas d’inquiétude.

Avant de tomber sur ce hack sur Hacker News, je ne réfléchissais pas trop aux embeddings, aux embeddings multimodaux ni aux bases de données vectorielles. J’avais déjà joué avec FAISS (la base vectorielle open source de Meta) et Pinecone ($$) pour deux-trois bidouilles, sans creuser : ça tournait, les tests passaient, basta.

Je ne sais toujours quasiment pas ce qu’est un vecteur, lol. Avant ce projet, je ne voyais pas trop comment m’en servir en dehors d’une chaîne de traitement (pipeline) de type RAG ou autre LLM.

J’apprends en construisant. Et quand le résultat a un petit goût de magie, c’est encore mieux.

### Glossaire WTF

Des amis ont relu ce billet et m’ont demandé : « wtf, c’est quoi X ? » Petit lexique des trucs qui étaient quasi neufs pour moi :

- **Vector Embeddings** : transforment vos textes et vos images en vecteurs numériques, ce qui permet de repérer les contenus similaires et de fouiller efficacement votre photothèque.  
- **Vector Database** : base de données qui stocke ces vecteurs et permet des recherches par similarité pour dénicher les éléments proches.  
- **Word2Vec** : technique révolutionnaire qui convertit les mots en vecteurs numériques afin de trouver des mots voisins et d’explorer leurs relations.  
- **CLIP** : modèle d’OpenAI qui encode images et textes en vecteurs.  
- **OpenCLIP** : implémentation open source de CLIP, accessible à tout le monde sans passe-droit.  
- **FAISS** : bibliothèque efficace pour gérer et interroger de grandes collections de vecteurs, qui permet de retrouver rapidement et simplement les images (ou autres objets) que vous cherchez.  
- **ChromaDB** : base qui stocke et récupère vos vecteurs image/texte, en renvoyant rapidement les résultats similaires.

## Reste simple, Harper.

C’est une bidouille assez simple. Je suis juste en train de m’amuser ; je n’étais pas spécialement soucieux de la scalabilité. En revanche, je voulais que **vous** puissiez la reproduire sans prise de tête.

Objectif : tout faire tourner en local sur mon laptop. On a ces jolis GPU Apple Silicon : faisons-les chauffer.

Première étape : un petit crawler (explorateur) qui scanne un dossier d’images. J’utilise Apple Photos, donc pas de répertoire plein de photos qui traîne. Mais j’avais un énorme bucket de mèmes de mon précieux (et très secret) groupe de mèmes — ne le dites à personne. J’exporte le chat, je fous les images dans un dossier et BAM ! jeu de test prêt.

### Le crawler

J’ai pondu le pire crawler du monde. Enfin, soyons honnêtes : Claude a pondu le pire crawler du monde d’après mes directives.

C’est un peu usine à gaz, mais voici le flow :

1. Récupérer la liste des fichiers du dossier cible.  
2. Stocker cette liste dans un fichier msgpack.  
3. Parcourir ce fichier et insérer chaque image dans une base SQLite avec quelques métadonnées :  
   - hash  
   - taille du fichier  
   - chemin  
4. Parcourir SQLite et, pour chaque image, utiliser CLIP pour calculer l’embedding.  
5. Enregistrer ces vecteurs dans la même base.  
6. Parcourir à nouveau et insérer vecteurs + chemin de l’image dans ChromaDB.  
7. Finito.

Oui, c’est beaucoup de travail superflu : on pourrait traiter les images et les balancer directement dans ChromaDB (choisie parce que simple, gratuite et sans infra).

Pourquoi tant de boucles ?  
- Après les mèmes, j’ai aspiré 140 000 images : je voulais un truc résilient.  
- Il fallait pouvoir reprendre la construction si ça plantait ou si le courant sautait.  
- J’adore les boucles.

Malgré la complexité, ça tourne nickel : plus de 200 000 images sans accroc.

### Un système d’embeddings

Encoder les images, c’était fun.

J’ai commencé par SigLIP et monté un [petit service web](https://github.com/harperreed/imbedding) : vous uploadez l’image, vous récupérez les vecteurs. Ça tournait sur un GPU du studio : pas ultra-rapide, mais toujours plus speed que de faire tourner [OpenCLIP](https://github.com/mlfoundations/open_clip) en local.

Mais je voulais du full local. Je me suis rappelé que le repo [ml-explore](https://github.com/ml-explore/) d’Apple avait des exemples sympas. Et BAM ! ils avaient une [implémentation CLIP](https://github.com/ml-explore/mlx-examples/tree/main/clip) ultra-rapide (fast AF). Même avec le gros modèle, elle dépassait une 4090 : dingue ! (wildstyle)

Il ne restait plus qu’à l’intégrer simplement dans mon script.

### MLX_CLIP

Avec Claude, on a torturé le script d’Apple pour en faire une petite classe Python que vous pouvez lancer sur n’importe quel Mac. Elle télécharge le modèle si besoin, le convertit et l’utilise à la volée.

Check : https://github.com/harperreed/mlx_clip

Je suis vraiment ravi du résultat ; les puces Apple Silicon dépottent grave.

Utilisation hyper simple :

```python
import mlx_clip

# Initialise le modèle.
clip = mlx_clip.mlx_clip("openai/clip-vit-base-patch32")

# Encode l’image et récupère les embeddings.
image_embeddings = clip.image_encoder("assets/cat.jpeg")
print(image_embeddings)

# Encode la description texte et récupère les embeddings.
text_embeddings = clip.text_encoder("a photo of a cat")
print(text_embeddings)
```

J’adorerais que ça tourne avec SigLIP ; je préfère ce modèle (bien meilleur que CLIP). Mais c’est une preuve de concept (POC) plus qu’un produit que je veux maintenir. Si quelqu’un a des pistes, *hmu* (contactez-moi) : [harper@modest.com](mailto:harper@modest.com). Pas envie de réinventer OpenCLIP, qui devrait tourner crème sur Apple Silicon et fait déjà le taf.

### Et maintenant ?

Les vecteurs d’image sont dans la base, passons à l’interface. J’ai utilisé la fonction de requête intégrée de ChromaDB pour afficher les images similaires.

On récupère les vecteurs de l’image de départ, on interroge ChromaDB ; ChromaDB renvoie la liste des IDs d’images classées par similarité décroissante.

J’ai emballé le tout dans une mini-appli Tailwind + Flask.  
Incroyable.

En 2015, on se serait tués à la tâche. Là, dix heures max : trivial.

C’est franchement magique.

### Recherche conceptuelle de mèmes

Rappel : mon premier set, ce sont 12 000 mèmes.

On part de :

{{< image src="images/posts/vector-memes-bowie.png" caption="So true" >}}

On l’encode, on balance à ChromaDB, et ça ressort :

{{< image src="images/posts/vector-memes-bowie-results.png" >}}

Autre exemple :

{{< image src="images/posts/vector-memes-star-trek.png" >}}

Résultats :

{{< image src="images/posts/vector-memes-star-trek-results.png" >}}

C’est vraiment fun de cliquer partout.

### Espaces de noms ?

La magie ne vient pas juste du « clique → similaires ». Ça, c’est cool, mais pas le *holy shit*.

Ce qui me retourne le cerveau, c’est d’utiliser le même modèle pour encoder un texte de recherche et retrouver les images associées.

Exemples :

Recherche **money** :

{{< image src="images/posts/vector-memes-money.png" >}}

Recherche **AI** :

{{< image src="images/posts/vector-memes-ai.png" >}}

Recherche **red** (couleur ? lifestyle ? Russie ?) :

{{< image src="images/posts/vector-memes-red.png" >}}

Et ainsi de suite, à l’infini. Magique. On retombe sur des pépites oubliées. Tiens, j’ai besoin d’un mème sur « écrire un article » :

{{< image src="images/posts/vector-memes-writing-meme.jpg" >}}

(Je suis lucide, je m’en fous, lol.)

### Et avec une photothèque ?

Ça marche du tonnerre.

Essayez sur votre propre photothèque. J’ai téléchargé mon Google Photos Takeout, extrait sur un disque externe. Deux-trois scripts pour gérer la masse de doublons, puis j’ai pointé le crawler sur ce répertoire. Roulez jeunesse !

Environ 140 000 photos, six heures de traitement. Pas si mal. Le résultat est dingue.

#### Quelques exemples fun :

Évidemment similaires (j’ai un problème de doublons) :

{{< image src="images/posts/vector-memes-harper.png" >}}

On a eu pas mal de caniches :

{{< image src="images/posts/vector-memes-poodles.png" >}}

On peut chercher des paysages : je ne savais même pas que j’avais photographié Fuji-san depuis un avion !

{{< image src="images/posts/vector-memes-fuji-results.png" >}}

Et hop, des images similaires du mont Fuji :

{{< image src="images/posts/vector-memes-fuji-similar.png" >}}

Recherche de lieux :

{{< image src="images/posts/vector-memes-chicago.png" >}}

Ou d’émotions : apparemment je fais souvent une tête surprise :

{{< image src="images/posts/vector-memes-surprised.png" >}}

Des trucs pointus comme les low riders (shootés à Shibuya) :

{{< image src="images/posts/vector-memes-low-riders.png" >}}

Ou des notions difficiles à filtrer autrement, comme le bokeh :

{{< image src="images/posts/vector-memes-bokeh.png" >}}

C’est génial : on clique et on redécouvre des clichés oubliés. Par exemple ce portrait de Baratunde que j’ai pris en 2017 :

{{< image src="images/posts/vector-memes-baratunde.png" >}}

### Bientôt partout

Je parie que cette techno va vite se retrouver dans toutes les applis photo. Google Photos le fait sans doute déjà, mais tellement « googlé » qu’on ne le remarque plus.

C’est trop bon pour être ignoré. Si j’avais un produit d’envergure basé sur des images, je lancerais illico un pipeline d’encodage pour voir quelles fonctionnalités de dingue ça débloque.

## VOUS POUVEZ L’UTILISER GRATUITEMENT !

Le code source est là : [harperreed/photo-similarity-search](https://github.com/harperreed/photo-similarity-search).

Allez jeter un œil.

La mise en route est plutôt simple, même si c’est un peu bricolé (hacky).

Prenez Conda ou équivalent pour garder un environnement propre. Interface : Tailwind. Web : Flask. Code : Python. Votre hôte : Harper Reed.

## Mon défi pour vous !

Bâtissez une appli qui catalogue ma photothèque proprement. Pas d’upload ailleurs. Une appli Mac native : je la pointe sur ma photothèque Apple Photos et je lance « crawl ». On peut imaginer :

- Auto-légendes Llava/Moondream  
- Mots-clés / Tags  
- Similarité vectorielle  
- etc.

Elle doit tourner en local, être native, simple et efficace. Peut-être un plugin pour Lightroom, Capture One ou Apple Photos.

Je la veux. Faites-la. Redécouvrons toutes nos photos grâce à la magie de l’IA.

## Bonus : récupération des JPEG de prévisualisation Lightroom

Mon pote hacker Ivan était là pendant la bidouille. Il a tout de suite capté la magie et a voulu tester.

Son catalogue est sur un disque externe, mais il avait le fichier de prévisualisation Lightroom en local. Il a pondu un petit script qui extrait vignettes et métadonnées du fichier preview et les enregistre sur un disque externe.

On a lancé le crawler et BAM ! images similaires, tout ça. Parfait.

#### Récupérez vos photos Lightroom… ou au moins les miniatures

Le script d’Ivan est vraiment cool. Si vous avez perdu vos originaux (disque HS, etc.) mais gardé le .lrpreview, il peut au moins extraire la version basse def.

Un script bien utile à garder sous le coude.

C’est ici : [LR Preview JPEG Extractor](https://github.com/ibips/lrprev-extract).

## Merci d’avoir lu.

Comme toujours, *hmu* (contactez-moi) : [harper@modest.com](mailto:harper@modest.com) et passons du temps ensemble. Je pense beaucoup à l’IA, l’e-commerce, les photos, la hifi, le hacking et autres conneries.

Si vous êtes à Chicago, passez dire bonjour.