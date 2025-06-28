---
date: 2024-04-12 09:00:00-05:00
description:
    siglip/CLIP と画像のベクトルエンコーディングを使って、魔法のようなミーム検索エンジンを作りました。この強力な技術を学ぶのに最適で、とても楽しかったです。あなたも自分で構築して写真ライブラリに眠る忘れられた逸品を見つけられるよう、コードを共有しています。さあ、画像に
    AI の力を解き放ちましょう！
draft: false
generateSocialImage: true
tags:
    - meme-search-engine
    - vector-embeddings
    - applied-ai
    - siglip
    - image-search
title: うっかりミーム検索エンジンを作ってしまった
translationKey: I accidentally built a meme search engine
slug: i-accidentally-built-a-meme-search-engine
---

## 別名：CLIP/SigLIP と画像ベクトルエンコーディングを学ぶ方法

_tl;dr_: SigLIP／CLIP を使ってミーム検索エンジンを作った。めちゃ楽しかったし、学びも山盛りだった。

ここしばらく実用寄りの AI ツールを作りまくっているが、その中でもいちばん “魔法” 感があるのがベクトル埋め込みだ。[Word2Vec](https://en.wikipedia.org/wiki/Word2vec) を初めて触ったときなんて本当にブッ飛んだ。

先日、[Hacker News で見かけたシンプルなアプリ](https://news.ycombinator.com/item?id=39392582)が[マジで凄かった](https://mood-amber.vercel.app/)。誰かが Tumblr の画像をかき集めて [SigLIP](https://arxiv.org/abs/2303.15343) で埋め込みを作り、「画像をクリックすると似た画像が並ぶ」だけのアプリを公開していた。どうやればいいか皆目見当もつかなかったけど、手が届きそうにも見えた。

この勢いで「全部理解してやるか」と走り始めた。

## wut（何それ？）

ベクトル埋め込み、CLIP／SigLIP などのマルチモーダル埋め込み、ベクトルデータベース……初見でもビビる必要なし。

あの HN のハックを見るまでは、俺もベクトルのことなんて深く考えたことがなかった。FAISS（Facebook 製のシンプルなベクトル DB）や Pinecone（$$）を「動けば OK」で使った程度。テストが通ったら「はい終わり」。

ぶっちゃけ今でも「ベクトルって何だよ」って思ってる。Lol. RAG とか LLM 以外でどう使うかも、今回作るまでピンと来ていなかった。

俺は「作りながら学ぶ」派だ。結果が面白ければ燃えるし、今回はほんと魔法だった。

### WTF 用語集

公開前に友人に読んでもらったら「X って何？」が多発したので、当時ほぼ初見だったキーワードをざっくりまとめておく。

- **Vector Embeddings（ベクトル埋め込み）** — テキストや画像を数値ベクトルに変換し、似たもの検索を爆速にする仕組み。
- **Vector Database（ベクトルデータベース）** — エンコード済みベクトルを保存・検索できる DB。
- **Word2Vec** — 単語をベクトル化し、類似語や関係性を探れる革命的手法。
- **CLIP** — OpenAI のモデル。画像とテキストを同じベクトル空間に押し込む。
- **OpenCLIP** — CLIP の OSS 実装。誰でも使い放題。
- **FAISS** — 大量ベクトルを管理して近傍検索を激速にするライブラリ。
- **ChromaDB** — 画像・テキストのベクトルを保存し、似た結果を秒速で返す DB。

## シンプルにいこうぜ、harper

これはただの簡単ハックだ。テキトーにいじってるだけだからスケールなんて気にしない。でも **あなた** が再現できることは重視した。

目標その 1：ぜんぶ Mac ローカルで回す。せっかくの Apple シリコン GPU をフル回転させよう。

まずは画像ディレクトリをクロールするクソ雑なクローラを書く。Apple Photos 派なので手元に写真フォルダがない。そこで秘密のミームチャットから 1 万枚超のミームをエクスポートしてテスト画像にした。

### クローラ

世界一ひどいクローラを書いた。いや正確には、俺の指示で Claude が書いた “世界一ひどいクローラ” だ。

流れはこんな感じ：

1. 対象ディレクトリのファイル一覧を取得
2. その一覧を msgpack に保存
3. msgpack を読みつつ全画像を走査し、SQLite にメタデータを突っ込む
    - ハッシュ
    - ファイルサイズ
    - パス（location）
4. SQLite を回しながら CLIP で各画像をエンコード
5. 得たベクトルをまた SQLite に書き戻す
6. さらに SQLite を回し、ベクトル＋画像パスを ChromaDB に投入
7. 完了

ムダ多すぎるのは百も承知。画像→埋め込み→ChromaDB に一発で突っ込めばいい。でもこんな構成にした理由は：

- ミームのあと 140k 枚クロールしたから、途中で落ちても再開できる堅牢さが欲しかった
- 停電やクラッシュでも途中から走らせたかった
- ループ回すの大好き

多少ゴチャついてても結果は優秀。20 万枚超えてもトラブルなしでクロールできた。

### 埋め込みシステム

画像エンコードは楽しい。

まず SigLIP で [シンプルな Web サービス](https://github.com/harperreed/imbedding) を立てた。スタジオの GPU マシンで回したら速いとは言えないが、ローカルの [OpenCLIP](https://github.com/mlfoundations/open_clip) よりははるかに速かった。

それでもローカル完結させたい。そこで Apple の [ml-explore](https://github.com/ml-explore/) リポジトリを思い出す。中にある [CLIP 実装](https://github.com/ml-explore/mlx-examples/tree/main/clip) が爆速。大きめモデルでも RTX 4090 より速い。意味がわからんほど速い。

あとはスクリプトから簡単に呼び出せれば OK。

### MLX_CLIP

Claude と一緒にサンプルをいじって、どの Mac でも動く小さな Python クラスにした。モデルがなければ自動で DL＆変換、即推論。

リポジトリはこちら: <https://github.com/harperreed/mlx_clip>

出来栄えにけっこう満足。言わずもがなだけど、Apple シリコンはマジで速い。

使い方はこんな感じ：

```python
import mlx_clip

# モデルを初期化
clip = mlx_clip.mlx_clip("openai/clip-vit-base-patch32")

# 画像をエンコード
image_embeddings = clip.image_encoder("assets/cat.jpeg")
print(image_embeddings)

# テキストをエンコード
text_embeddings = clip.text_encoder("a photo of a cat")
print(text_embeddings)
```

SigLIP 版も動かしたい（CLIP よりはるかに良いと思っている）が、これは POC だし保守する気はない。SigLIP で動かすヒントがあったら連絡ちょうだい（hmu）。OpenCLIP を再発明したくはないし、理論上 Apple シリコンでも走るはずなんだよね。

### さて次は

画像ベクトルを ChromaDB にブチ込んだら、あとは UI。基準画像のベクトルを抜いて ChromaDB に投げる → 類似度順に画像 ID が返る。

これらを Tailwind と Flask で包んで一気に Web 化した。これが自分でも驚くほどイケてた。  
2015 年なら何人月かかったかわからんが、今回はトータル 10 時間。笑うしかない。

結果はガチで魔法。

### ミーム概念検索

最初のデータセットはミーム。約 12,000 枚。

まずこれ：

{{< image src="images/posts/vector-memes-bowie.png" caption="So true" >}}

エンコードして ChromaDB に投げると……

{{< image src="images/posts/vector-memes-bowie-results.png" >}}

もう一例：

{{< image src="images/posts/vector-memes-star-trek.png" >}}

返ってくるのがこれ：

{{< image src="images/posts/vector-memes-star-trek-results.png" >}}

クリックしてるだけで無限に遊べる。

### 「Namespaces?」って何だよ、みたいな話

「画像クリック→類似画像」はクールだけど、俺の脳を吹き飛ばしたのは “同じモデルで検索テキストもベクトル化し、似た画像を返せる” ことだ。テキスト→画像のマルチモーダル検索は完全に手品。

いくつか例を挙げよう。

**money** で検索：  
{{< image src="images/posts/vector-memes-money.png" >}}

**AI** で検索：  
{{< image src="images/posts/vector-memes-ai.png" >}}

**red** で検索（色？ ライフスタイル？ それともロシア？）：  
{{< image src="images/posts/vector-memes-red.png" >}}

延々と遊べる。忘れてたお宝ミームもザクザク。  
「ブログ執筆のミーム欲しいな」と思ったら──  
{{< image src="images/posts/vector-memes-writing-meme.jpg" >}}

（自覚はあるけど気にしない w）

### 写真ライブラリで試すと？

めちゃくちゃいい感じに動く。

自分のフォトライブラリで試すのを激しくオススメする。俺は Google Photos の Takeout を落として外付けディスクに展開。重複だらけだからスクリプトで整理し、ミームフォルダの代わりにそのディレクトリをクロール。

写真 140k 枚で約 6 時間。悪くない。結果は最高。

#### 例いろいろ

そっくり写真（Google Photos の重複問題はご愛敬）  
{{< image src="images/posts/vector-memes-harper.png" >}}

うちのプードルたち  
{{< image src="images/posts/vector-memes-poodles.png" >}}

ランドマーク検索：飛行機から撮った富士山に自分でも気づいてなかった  
{{< image src="images/posts/vector-memes-fuji-results.png" >}}

そこから類似の富士山写真  
{{< image src="images/posts/vector-memes-fuji-similar.png" >}}

場所もラクラク  
{{< image src="images/posts/vector-memes-chicago.png" >}}

感情系。「驚き顔」がこんなにあったとは  
{{< image src="images/posts/vector-memes-surprised.png" >}}

ニッチなテーマ、ローライダーのクルマ（渋谷で撮影）  
{{< image src="images/posts/vector-memes-low-riders.png" >}}

検索しづらい「ボケ味」も一発  
{{< image src="images/posts/vector-memes-bokeh.png" >}}

忘れてた名ショットも救出。2017 年に撮った Baratunde：  
{{< image src="images/posts/vector-memes-baratunde.png" >}}

### これはそのうち全部のアプリに入る

近いうちに主要フォトアプリは絶対この機能を積む。Google Photos にはもう入ってるかもしれないけど、Google がゴチャゴチャ手を入れすぎて誰も気づいてないだけかも。

画像を扱うプロダクトを持ってるなら、今すぐパイプライン組んでエンコードを始めた方がいい。

## 無料で使えるヨ！（原文見出し: “YOU CAN USE THIS FOR THE LOW PRICE OF FREE”）

ソースはここ: <https://github.com/harperreed/photo-similarity-search>

ぜひ触ってみてくれ。ちょっとハック感あるけど動く。  
conda などで環境を分けると楽。UI は Tailwind、サーバは Flask、コードは Python。ホストは harper reed でした。

## キミへのチャレンジ！

俺のフォトライブラリを快適にカタログ化できる Mac ネイティブアプリを作ってくれ。クラウドに上げるのはイヤ。ライブラリを指定して「クロール開始」押すだけ、みたいなのが理想。

- Llava／Moondream で自動キャプション
- キーワード／タグ付け
- ベクトル類似検索
- etc.

全部ローカルで動いて、シンプルで強力。Lightroom、Capture One、Apple Photos と連携できたら最高だ。

これ、マジで欲しい。誰か作って！

## 追加課題：Lightroom プレビュー JPEG 復旧

ハック仲間の Ivan もこの魔法を見て即参戦。彼の写真は外付け HDD にあるが、Lightroom のプレビューファイルはローカルにあった。そこでサムネとメタデータを抜き出して外付けに保存するスクリプトを書いた。

そのあと画像ベクトルクローラを回したら類似検索も問題なく動いた。BAM──完璧。

#### Lightroom の写真を救出 — サムネだけでも

Ivan のシンプルスクリプトは超便利。もし本体ライブラリが吹っ飛んでも .lrprev が残っていれば低解像度版だけでも救出できる。  
リポジトリ: <https://github.com/ibips/lrprev-extract>  
（訳注: 原文では “Light Room” と表記されているが、正しくは “Lightroom”。）

## Thanks for reading.

いつでも連絡ちょうだい（hmu: harper@modest.com）―AI、EC、写真、Hi-Fi、ハック、何でも語ろう。  
シカゴにいるならぜひ遊びに来て。
