---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: ブレインストーミングから計画策定と実行まで、LLMを活用してソフトウェアを構築する現在のワークフローを詳細に解説します。
draft: false
generateSocialImage: true
tags:
- LLM
- coding
- ai
- workflow
- software-development
- productivity
title: '現時点での私のLLMコード生成ワークフロー

  description: ブレインストーミングから計画策定と実行まで、LLMを活用してソフトウェアを構築する現在のワークフローを詳細に解説します。'
translationKey: My LLM codegen workflow atm
---

_tl;dr: まず仕様をブレストし、その後プランをさらに“計画”して、最後に LLM でコード生成→実行。それぞれ独立したループで回す。あとは魔法。✩₊˚.⋆☾⋆⁺₊✧_

LLM を使って小さなプロダクトを山ほど作ってきた。めちゃくちゃ楽しくて役に立つ一方、時間を浪費する落とし穴も多い。少し前に友人から「どうやって LLM にソフトを書かせてるの？」と聞かれ、「おっと、どれくらい時間ある？」となり──この投稿を書くことになった。

（P.S. AI が大嫌いな人は中身を読まずに末尾まで飛ばしてください）

開発仲間と話すと、みな同じようなワークフローを持ちつつ細部が微妙に違う。

以下が自分のワークフローだ。自分の経験、友人たち（ありがとう [Nikete](https://www.nikete.com/)、[Kanno](https://nocruft.com/)、[Obra](https://fsck.com/)、[Kris](https://github.com/KristopherKubicki)、[Erik](https://thinks.lol/)）との会話、そしてインターネットのいろいろな[悪い](https://news.ycombinator.com/) [場所](https://twitter.com)で拾ったベストプラクティスを土台にしている。

これは **今** はうまく回っているが、2 週間後には通用しなくなるか、逆に倍速になるかもしれない。¯\\\_(ツ)\_/¯

## さあ行こう

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="AI 生成画像はいつも怪しい。うちのジャガロのコーディング・ロボット天使にご挨拶！" >}}

開発パターンはいろいろあるが、基本的に次の 2 つ。

- グリーンフィールド開発（ゼロから新規）
- “最新だけど実質レガシー”なコードベースの改修

両方のプロセスを紹介しよう。

## グリーンフィールド開発

次のプロセスはグリーンフィールドで特にうまく機能する。堅牢な計画とドキュメントを用意し、小さなステップで実装できる。

{{< image src="greenfield.jpg" alt="Green field" caption="厳密には右側がグリーンフィールド。Leica Q, 2016/05/14" >}}

### Step 1: アイデアのブラッシュアップ

対話型 LLM（自分は ChatGPT-4o / ChatGPT-4o3 を使用）でアイデアを磨く。

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

ブレインストーミングが自然に終わったら次を投げる。

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

これでかなりしっかりした仕様が出力されるので、`spec.md` としてリポジトリに保存しておく。

> この仕様はコード生成だけでなく、推論モデルに欠点を突っ込ませたり、ホワイトペーパーやビジネスモデルを生成したりにも使える。深掘りリサーチに突っ込めば 1 万語級の補足資料が返ってくる。マジでワイルド。

### Step 2: 計画

作成した仕様を高性能推論モデル（`o1*` / `o3*` / `r1` など）に渡す。

（TDD 版プロンプト）

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

（非 TDD 版プロンプト）

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

モデルは **プロンプトプラン**（`prompt_plan.md`）を出力してくれる。これは aider や cursor などにそのまま食わせて実行できる。

続けてチェックリストを作成。

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

`todo.md` をリポジトリに保存し、コード生成ツールにチェックを付けてもらえばセッションをまたいでも状態を保持できる。

#### やったー、計画完成！

これで堅牢な計画とドキュメントが揃い、実装に集中できる。ここまででかかる時間はせいぜい **15 分**。正直ぶっ飛んでる。

### Step 3: 実装

実装段階ではツールが山ほどあるが、成否は Step 2 の質次第。

[GitHub Workspace](https://githubnext.com/projects/copilot-workspace)、[aider](https://aider.chat/)、[Cursor](https://www.cursor.com/)、[Claude Engineer](https://github.com/Doriandarko/claude-engineer)、[sweep.dev](https://sweep.dev/)、[ChatGPT](https://chatgpt.com)、[Claude.ai](https://claude.ai)──どれでも問題なく動いた。たぶんほとんどのコード生成ツールでいける。

とはいえ自分は **素の Claude** と **aider** が好きだ。

### Claude

[Claude.ai](https://claude.ai) でペアプロ的に作業し、プロンプトを順番に投げる。行き来はやや面倒だが概ねうまくいく。

自分は最初のひな型コードやツールチェーンを整える役目を担う。ここを好きな言語・スタイル・ツールで固めておくと指針ができる。Claude は React コードを生成しがちなので、土台をしっかり決めておくと助かる。

詰まったら [repomix](https://github.com/yamadashy/repomix) でコードベースを打包し、Claude に渡してデバッグを依頼する。

ワークフローはこうだ。

- リポジトリをセットアップ（ひな型コード作成、`uv init`、`cargo init` など）
- プロンプトを Claude に貼る
- Claude の出力を IDE にコピペ
- コードを実行し、テストを走らせる
- 動けば次のプロンプトへ
- 動かなければ repomix でコード全体を渡してデバッグ
- これを繰り返す ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) は楽しくて少し風変わりだが、Step 2 のアウトプットと相性抜群で、少ない労力でぐいぐい進む。

Testing is nice with aider, because it can be even more hands off as aider will run the test suite and debug things for you.  
→ Aider の良い点はテストも自動で走らせ、失敗したらそのままデバッグまでしてくれるので、さらに手離れがいいことだ。

ワークフローはほぼ同じ。

- リポジトリをセットアップ
- Aider を起動
- プロンプトを Aider に貼る
- Aider のダンスを見る ♪┏(・o･)┛♪
- Aider がテストを走らせる／自分でアプリを起動して確認
- 動けば次のプロンプトへ
- 動かなければ Q&A で修正
- これを繰り返す ✩₊˚.⋆☾⋆⁺₊✧

> Aider では [LLM リーダーボード](https://aider.chat/docs/leaderboards/) で新モデルのベンチ結果を公開しており、モデルの実力を把握するのに便利だ。

### 結果

このフローでスクリプト、Expo アプリ、Rust の CLI ツールなど大量に作った。言語も用途も選ばない。もし眠っているプロジェクトがあるなら試してみてほしい。短時間で驚くほど前進する。

ハック用 TODO は空っぽだ。何か思いつくたびに映画を見ながらサクッと作れる。久々に新しい言語やツールに触れ、プログラミングの視野が広がっている。

## グリーンフィールドでない場合：既存コードを段階的に改修

ときにはグリーンフィールドではなく、既存コードベースを少しずつ育てる必要がある。

{{< image src="brownfield.jpg" alt="a brown field" caption="ここはグリーンフィールドではない。祖父のカメラに残っていた 60 年代ウガンダの一枚" >}}

この場合は少し違う。プロジェクト全体ではなくタスク単位で計画する。

### コンテキスト取得

ソースコード全体を LLM に食わせるツールが必要だ。自分は [repomix](https://github.com/yamadashy/repomix) を [`mise`](https://mise.jdx.dev/) のタスクと組み合わせて使っている。

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

`output.txt` にコードベースのコンテキストを詰める。トークンが足りない場合は、無関係な部分を除外してサイズを調整する。

> `mise` の良いところは、作業ディレクトリの `.mise.toml` でタスクを上書きできる点だ。別ツールでパッキングしても `output.txt` さえ作れば同じタスクが動く。

`output.txt` ができたら `LLM` コマンドで変換し、Markdown に保存する。実際は

```
cat output.txt | LLM -t readme-gen > README.md
```

や

```
cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md
```

のようにシンプル。高度な処理は LLM コマンド側が担ってくれるので、実際にやっていることはこれだけだ。

テスト不足を素早く補う例を示そう。

#### Claude

- ディレクトリに移動  
- `mise run LLM:generate_missing_tests` を実行  
- 生成された `missing-tests.md` を確認  
- `mise run LLM:copy_buffer_bundle` で全コンテキストをクリップボードへ  
- それを Claude に貼り付け、最初の “missing test” Issue を渡す  
- Claude の出力を IDE に貼り付けてテスト  
- これを繰り返す ✩₊˚.⋆☾⋆⁺₊✧  

#### Aider

- ディレクトリに移動（必ず新しいブランチで作業）  
- Aider を起動  
- `mise run LLM:generate_missing_tests` を実行  
- `missing-tests.md` の最初の Issue を Aider に貼る  
- Aider のダンスを見る ♪┏(・o･)┛♪  
- テストを回す  
- これを繰り返す ✩₊˚.⋆☾⋆⁺₊✧  

### プロンプト・マジック

既存コードを掘り下げる際に使っているお気に入りプロンプトをいくつか紹介。

#### コードレビュー

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply before writing the code review. Review every part, and don't hallucinate.
```

#### GitHub Issue 生成

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### テスト不足の抽出

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues  will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

これらは正直 “ブーマー・プロンプト” だがまだ役立つ。より良い案があればぜひ教えてほしい。

## スキー ᨒ↟ 𖠰ᨒ↟ 𖠰

このプロセスを人に説明するとき、「状況を積極的に追わないとすぐ **オーバー・マイ・スキー**になる」と言う。最初は美しいパウダーを滑っているのに、突然「何が起きてるんだ！」と崖っぷち──そんな感覚だ。

グリーンフィールドでは **計画ステップ** を挟むことで混乱を抑えられる。特に Aider でワイルドに書くときはテストが重要だ。

それでもオーバー・マイ・スキーになることはある。そんなときは短い休憩や散歩が効く。普通の問題解決と同じだが、速度が桁違いなのだ。

> ときには LLM に「ロア（世界観）ファイルを作成して UI から参照せよ」と頼むこともある。Python CLI ツールでも突然ロアやグリッチ風 UI が生える。可能性は無限大。

## さみしい (｡•́︿•̀｡)

最大の欠点は **ソロプレイ** であること。長年ソロ開発もペアプロもチーム開発も経験したが、人と一緒の方が絶対に面白い。現状のツールはマルチプレイヤーに向いておらず、ボットは衝突し、マージは地獄、コンテキスト共有も大変だ。

誰かが LLM コーディングをマルチプレイヤーにする解決策を出してくれるのを心待ちにしている。チャンスしかない。頼む、GET TO WORK!

## ⴵ 時間 ⴵ

コード生成で一人でも大量のコードを書けるようになった一方、LLM がトークンを燃やす **待ち時間** が増えた。

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="まるで昨日のことのように覚えている" >}}

その間にやること：

- 次のプロジェクトのブレスト  
- レコードを聴く  
- [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/) を叩く  
- 友人やロボットとおしゃべり  

ここまでハックし続けた時期は他にない。今が一番生産的かもしれない。

## Haterade ╭∩╮( •̀_•́ )╭∩╮

「クソ LLM なんて全部ダメ」と言う友人も多い。それも理解できる。AI を嫌う理由は山ほどあり、自分も電力消費と環境負荷が一番怖い。が……コードは流れねばならない。はぁ。

深入りしたくないけど少し学んでみたい人には、Ethan Mollick の [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/) を勧める。テック至上主義ではなく、LLM の利点を丁寧に説明している。読んだ友人とも良い議論ができた。

懐疑的でも少し興味があるなら、気軽に連絡してほしい。この狂気を一緒に眺めて、何か作ろう。

_thanks to [Derek](https://derek.broox.com)、[Kanno](https://nocruft.com/)、[Obra](https://fsck.com)、[Erik](https://thinks.lol/) for taking a look at this post and suggesting edits. I appreciate it._