---
bsky: https://bsky.app/profile/harper.lol/post/3lflrbeqy4s2u
date: 2025-01-12 20:59:59-05:00
description: 自動データ収集によってオンラインで自分が読んでいるもの、聴いているもの、ブックマークしているものを追跡・表示するメディアセクションを自分のウェブサイトに追加する。
draft: false
generateSocialImage: true
tags:
- personal-data
- hugo
- rss
- media-tracking
- automation
- web-development
title: '新しいメディア

  description: 自動データ収集によってオンラインで自分が読んでいるもの、聴いているもの、ブックマークしているものを追跡・表示するメディアセクションを自分のウェブサイトに追加する。'
translationKey: new-media
---

_tl;dr: 自動でデータを収集し、「今読んでいる／聴いている／ブックマークしている」ものを記録＆一覧表示できる “media” セクションをサイトに追加した。詳しくは[こちら](/media)_

最近、友人の Claude、Aider、そして ChatGPT と数時間あれこれ試行錯誤し、このサイトに新しく [media](/media) セクションを追加した。AI を使った開発は本当に楽しい（この話はそのうち別エントリにするかも）。

media セクションでは、Goodreads で読了マークを付けた本の [ログ](/media/books)、Spotify で最近保存した [トラック](/media/music)、そして Feedbin／NetNewsReader などから取得した [リンク](/media/links) を一望できる。

リンクを公開し始めたのは 1 か月ほど前。ワークフローの使い勝手を確かめたかったんだ。こういう仕組みは、余計な BS※ や自分の手間を増やす追加操作なしに “ただ動く” ことが大事。ひと月も経つと、保存したリンクがサイトに勝手に現れる――まるで魔法みたいだ。  
※BS = bullshit の略

{{< image src="L1060869.jpeg" width="1024" alt="New Media" caption="Sufjan Stevens, Leica Q, 7/17/2016" >}}

## なんで記録するの？

ひとつ目の理由は、昔の自分のサイトでひたすら記録しまくっていた頃が懐かしくなったから。毎日、自分が消費したものや参加したことを一覧できるのは最高に楽しかった。でも時が過ぎ、全部が崩壊した（原因のほとんどは cron ジョブが落ちて）。

もうひとつは、友人 Simon のプロジェクト [dog sheep beta](https://github.com/dogsheep/dogsheep-beta) に刺激を受けたこと。大量データを堅牢に保存できる仕組みが欲しかった。SQLite に突っ込んで GitHub の隅に放置――という手も考えたけど、それじゃ退屈だ。どうせなら、みんなに無理やりありのままドヤ顔で見せつけたい。

そこで SQLite の代わりに、エンティティを YAML ファイルに吐き出し、Hugo の記事を生成するスクリプトを数本書くだけで済ませた。結果は同じでも、データも投稿も両方手に入る。

自分のメディア消費を眺められるし、みんなにも見せつけられるし、あとで振り返るための保存にもなる――最高！

### RSS フィード

各セクションの RSS フィードはこちら：

- [Full Media RSS](/media/index.xml)
- [Books RSS](/media/books/index.xml)
- [Music RSS](/media/music/index.xml)
- [Links RSS](/media/links/index.xml)

僕は [NetNewsWire](https://netnewswire.com/) と [Feedbin](https://feedbin.com) を使っていて、両方とも超おすすめ。RSS についてはまた後日、詳しく書くつもり！

## シンプルなツールこそいいツール

Hugo をいじるのが大好きだ。楽しいし、制限が多いのもいい。無限のオプションや過度な魔法はいらない――ほんの少しの魔法だけで充分。

Hugo なら、front-matter 付き Markdown をフォルダに放り込むだけで、あとは勝手に動く。

美しいね。

### YOU IN THE CORNER!

そこのあなた！ 自分でもこういうことをやってみたいなら、[micro.blog](https://micro.blog) をチェックしてみてほしい。似たようなことが簡単にできるし、最新の [micro.one](https://micro.one) サービスなら安価にさくっと始められるよ。

## New Media

{{< image src="harper-politics.jpeg" width="1024" alt="New Media" caption="やたら真面目そうに見えるオフィス、カメラ不明、2012/11/8" >}}

完全に余談だけど、昔政治の仕事をしていた頃は、技術系の人たちのことをまとめて “new media” と呼んでいたんだ。僕には全然 “ニュー” じゃなく、ただのメディアにしか思えなくて笑ってた、という小話。