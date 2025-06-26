---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: ソフトウェアを開発するためにLLMを活用する際のブレインストーミングから計画立案、実装に至るまで、現在の私のワークフローを詳細に解説する。
draft: false

generateSocialImage: true
tags:
    - LLM
    - coding
    - ai
    - workflow
    - software-development
    - productivity
title: My LLM codegen workflow atm
slug: "my-llm-codegen-workflow-atm"
translationKey: My LLM codegen workflow atm
---

_tl;dr_  
まずブレインストーミングで仕様を固め、次に “計画そのものを計画” し、それから LLM のコード生成で実装。小さなループを回していき、あとは魔法 ✩₊˚.⋆☾⋆⁺₊✧

最近、LLM で小さなプロダクトを山ほど作ってる。楽しいし役立つけど、時間を溶かす落とし穴も多い。少し前に友人から「どうやって LLM でソフト書いてるの？」と聞かれ、「おいおい、どれだけ時間ある？」と思ったので、このポストを書くことにした。  
（追伸：AI 嫌いの人は一番下までスクロールしてね）

開発仲間と話すと細部は違えど、大筋は似たアプローチ。

これが俺のワークフロー。自分の経験、友人との会話（ありがとう [Nikete](https://www.nikete.com/)、[Kanno](https://nocruft.com/)、[Obra](https://fsck.com/)、[Kris](https://github.com/KristopherKubicki)、[Erik](https://thinks.lol/)）、そしてインターネットの “魔境” に転がってるベストプラクティスを全部ぶち込んでいる。

今は **バッチリ動く** けど、2 週間後には動かなくなってるか、倍の威力で動いてるかも。¯\\\_(ツ)\_/¯

## Let’s go

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="AI 生成画像はいつも怪しい。うちのジャガロ仕様コーディングロボ天使に挨拶して!" >}}

開発パターンは色々あるけど、俺の場合はほぼ 2 つ。

- Greenfield（新規プロジェクト）
- Brownfield（既存プロジェクトのモダンレガシーコード）

両方のやり方を紹介する。

## Greenfield

新規開発では、次のプロセスがかなり効く。ちゃんとした計画とドキュメントが手に入り、小さなステップで実装を進められる。

{{< image src="greenfield.jpg" alt="Green field" caption="技術的には右側がグリーンフィールド。Leica Q, 2016/05/14" >}}

### Step 1: アイデアを絞り込む

ChatGPT-4o / o3 みたいな対話型 LLM でアイデアを磨く。

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

ブレストが自然に終わったら:

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

これでかなり solid な `spec.md` が手に入る。

> 仕様書は万能。今回はコード生成に使うけど、別モデルに渡して穴を突かせたり、ホワイトペーパーやビジネスモデルを起こしたりもできる。深掘りさせれば 1 万字の裏付けドキュメントも返ってくる。

### Step 2: 計画

`spec.md` を推論重視のモデル（`o1*`, `o3*`, `r1` など）へ渡す。

（TDD 版プロンプト）

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

（非 TDD 版プロンプト）

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

これで `prompt_plan.md` が生成される。

チェックリストも作っておく。

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

コード生成ツールが `todo.md` を自動でチェックしてくれるので、セッションを跨いでも状態を保ちやすい。

#### Yay. Plan!

ここまで **15 分** くらい。マジで速い。

### Step 3: 実行

成否は Step 2 の出来次第。  
[github workspace](https://githubnext.com/projects/copilot-workspace)、[aider](https://aider.chat/)、[cursor](https://www.cursor.com/)、[claude engineer](https://github.com/Doriandarko/claude-engineer)、[sweep.dev](https://sweep.dev/)、[chatgpt](https://chatgpt.com)、[claude.ai](https://claude.ai)――どれでもうまくいった。

俺は **生** Claude と aider 派。

### Claude

[claude.ai](https://claude.ai) とペアプロ。まず雛形とツール設定（`uv init`、`cargo init` など）だけ自分で用意し、言語やスタイルを固定しておくと Claude が勝手に React を吐く癖を抑えられる。

ワークフロー:

- repo をセットアップ（雛形・ツール設定）
- プロンプトを Claude に貼る
- 出力コードを IDE にコピペ
- 実行 & テスト
- ...
- 動いたら次のプロンプトへ
- こけたら [repomix](https://github.com/yamadashy/repomix) でコードベースを丸ごと渡してデバッグ
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) はクセ強だけど Step 2 のアウトプットと相性抜群。めちゃくちゃ楽できる。

- repo をセットアップ
- aider 起動
- プロンプトを貼る
- aider のダンスを眺める ♪┏(・o･)┛♪
- aider がテストを走らせるか、自分でアプリを動かして確認
- ...
- 動いたら次へ
- こけたら Q&A で修正
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

> ちなみに aider の [LLM ランキング](https://aider.chat/docs/leaderboards/) は新モデルの実力を測るのに最高。

### Results

この方法でスクリプト、Expo アプリ、Rust CLI など大量生産した。言語も環境も関係なし。

寝かせてるプロジェクトがあるなら試してみ。短時間でビビるほど進むぞ。

## Brownfield: 既存コードを小刻みに回す

{{< image src="brownfield.jpg" alt="a brown field" caption="これはグリーンフィールドじゃない。祖父のカメラに残ってた 60 年代ウガンダの写真" >}}

既存コードではタスクごとに計画する。

### コンテキストを LLM に流し込む

俺は [repomix](https://github.com/yamadashy/repomix) と [mise](https://mise.jdx.dev/) の組み合わせ。

```shell
LLM:clean_bundles           repomix で LLM バンドル生成
LLM:copy_buffer_bundle      output.txt をクリップボードへコピー
LLM:generate_code_review    output.txt からコードレビュー生成
LLM:generate_github_issues  output.txt から GitHub Issues 生成
LLM:generate_issue_prompts  output.txt から Issue プロンプト生成
LLM:generate_missing_tests  output.txt から足りないテスト抽出
LLM:generate_readme         output.txt から README.md 生成
```

`output.txt` ができたら、例えば

```shell
cat output.txt | LLM -t readme-gen > README.md
cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md
```

みたいにぶん回す。`LLM` コマンドがモデル切替やキー管理をやってくれて楽。

> `mise` は `.mise.toml` でタスクを上書きできるから、コードベースに合わせて違うパッカーを使ったり ignore パターンを増やしたり自由自在。

### 例: テスト補完

#### Claude

1. repo へ移動
2. `mise run LLM:generate_missing_tests`
3. `missing-tests.md` を確認
4. `mise run LLM:copy_buffer_bundle` で全文コピー
5. Claude に貼って最初の Issue を投げる
6. 出力コードを IDE に貼る
7. テスト実行
8. rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

1. repo へ移動（新しいブランチ推奨）
2. aider 起動
3. `mise run LLM:generate_missing_tests`
4. `missing-tests.md` を確認
5. Issue を aider に貼る
6. aider のダンスを眺める ♪┏(・o･)┛♪
7. テスト実行
8. rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

小さな改修からデカいタスクまでこれでいける。

### Prompt magic

既存プロジェクトを堅牢化する即効薬。お気に入りのプロンプトをいくつか。

#### Code review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply  before writing the code review. Review every part, and don't hallucinate.
```

#### GitHub Issue generation

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Missing tests

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues  will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

いわゆる “ブーマープロンプト” だから、いいアイデアあったら教えてくれ。

## Skiing ᨒ↟ 𖠰ᨒ↟ 𖠰

このプロセスを説明するとき、いつも「油断すると **over my skis**（前のめり）になるから状況をガチで追え」と言ってる。気持ち良く滑ってたら突然「何が起きてる!?」って崖から落ちる、あの感じ。

計画ドキュメントとテストは命綱。崖から落ちそうになったら散歩でもしてこい。

> ときどき LLM に「lore ファイル作って UI で参照して」みたいな無茶振りをする。Python CLI ツールなのに突然ロアが現れたり UI がグリッチしたり。空が限界じゃない。

## I am so lonely (｡•́︿•̀｡)

長年ソロ開発、ペアプロ、チーム開発を全部やってきたが、仲間とやる方が絶対楽しい。このワークフローは基本ソロプレイ。ボットは衝突するしマージは地獄、コンテキストはカオス。

誰か LLM コーディングをマルチプレイヤー化してくれ。頼む！

## ⴵ Time ⴵ

コード生成でアウトプットは激増。でも LLM がトークンを燃やしてる間の “待ち時間” も激増。

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="まるで昨日のことみたい" >}}

その間に

- 次プロジェクトをブレスト
- レコードを聴く
- [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/)
- 友達やロボと雑談

Hack Hack Hack。こんなに生産的だったこと、マジでない。

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

「Fuck LLMs、全部クソ」って友達も多い。懐疑は大事。俺も電力消費と環境負荷は怖い。でも…コードは流れたい。はぁ。

深入りせず様子見したい人には Ethan Mollick の  
[**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/) をおすすめ。テック脳筋本じゃなく、バランスよく利点を語ってくれる。読んだ友達ともめちゃくちゃ良い議論ができた。

興味はあるけど半信半疑？ 連絡くれ。狂気を一緒に覗きつつ何か作ろうぜ。

_thanks to [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com), and [Erik](https://thinks.lol/) for checking this post and suggesting edits. Appreciate it._
