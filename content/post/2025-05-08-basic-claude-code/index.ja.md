---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description: ソフトウェア開発におけるClaude Code AIアシスタントの活用方法を、ワークフローのコツ、テスト手法、実際のプロジェクト事例を交えて詳細に解説します。防御的コーディング戦略、TDD、チームへの導入も取り上げます。
draft: false
generateSocialImage: true
tags:
- ai
- coding
- claude
- development
- automation
- testing
- tdd
- programming
title: 基本的なClaude Code
translationKey: Basic Claude Code
---

この “エージェンティックコーディング” がマジで気に入ってる。いろんな意味でめちゃくちゃ魅力的だ。

[あのブログ記事](/2025/02/16/my-llm-codegen-workflow-atm/) を書いてからというもの、Claude 界隈ではいろいろ起こった。

- Claude Code  
- MCP  
- etc  

数百通（wat）ものメールが届き、「あなたのワークフローのおかげでめっちゃ捗りました！」という報告が山ほど来た。いくつかのカンファレンスでしゃべったり、コード生成の講座もやったりした。その過程でわかったのは、コンピュータは “codegen” を “codeine” に直したがって仕方ないってこと。誰が想像したよ！

{{< image src="codegen.png"  >}}

先日 [友人](https://www.elidedbranches.com/) と「**俺たち完全に詰んでるし、AI が仕事を奪う**」（これについてはまた今度）という話をしていたら、彼女が「Claude Code の記事も書けよ」と言うので――

それじゃ、いってみよう。

Claude Code は俺がオリジナルのワークフロー記事を書いてから 8 日後にリリースされて、予想どおり記事の大半を過去のものにした。それ以来、Aider から Claude Code に乗り換えて振り返ってない。Aider にも出番はあるけど、今のところ Claude Code のほうが役立つ。

Claude Code はパワフル――その代わり **クソ高い**。

とはいえ、ワークフロー自体はほぼ前と同じ。

- `gpt-4o` と雑談しながらアイデアを磨く  
- 一番イケてる推論モデルで仕様を書く。最近は o1-pro か o3（o1-pro のほうが良い気がするのは遅いから？）  
- そいつでプロンプトも生成させる。LLM にプロンプトを書かせるってマジで神ハックだし、ブーマーどもをキレさせるので最高。  
- `spec.md` と `prompt_plan.md` をプロジェクト直下に保存  
- それから Claude Code にこう打ち込む  

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

- このプロンプトのキモは `prompt_plan.md` を読んで “未完了” を探し、次のタスクを片っ端から片づけて Git にコミット、プランを更新し、終わったら「続ける？」と聞いてくるところ 🤌  
- あとは背もたれに寄りかかって Claude に `yes` と返すだけ。フィードバックを求められたら応じればいい。まさに魔法。  
- さらに『Cookie Clicker』状態になる。

この方法は驚くほどよく効く。ここに仕込めるチート能力をいくつか紹介しよう。

## ディフェンシブ・プログラミング！

### テスト

テスト、とりわけ TDD は必須だ。ガチで腰を据えて TDD をやることを強く推す。

昔の俺は TDD アンチで、下手くそだったし「時間のムダ」とか思ってた。でも完全に間違ってた。ここ数十年で俺たちの会社やプロジェクトにはテストを山ほど追加してきたが、大抵はコアが出来てから追加するパターンだ。人間同士ならこれでもまあ回る。

だが **ロボット――つまり LLM には最悪** だ。

ロボットは TDD に **目がない**。マジで。**貪り食うレベルで**。

まずロボットにテストとモックを書かせて、次のプロンプトでモックを本物に差し替える――これが幻覚やスコープドリフトへの今のところ最強の対策だ。ロボットがタスクに集中できる。

### lint

俺は lint を走らせるのが大好きだ。Ruff は最高だし、Biome もいいし、Clippy は楽しいし名前のセンスも最高。

そしてロボットも良いリンターを回すのが大好き。

常時 lint を走らせる習慣がバグを遠ざけ、可読性も保守性も上がる。フォーマッタも入れれば完璧。

### pre-commit フック

真の魔法はこれら全部を pre-commit フックに突っ込むこと。Python の `pre-commit` パッケージを推奨。`uv tools install pre-commit` で入れて `.pre-commit-config.yaml` を書けば、コミットのたびにテスト・型チェック・lint などが走り、コードはいつでも A+++（何度でも実行するぜ！）。

ロボットは **とにかくコミットしたくて仕方ない**。だから指示すると、野生のコード変更をドバッとやってコミットし、コードを **盛大にぶっ壊し**、そのあと自分で直す羽目になる。

おかげで GitHub Actions が lint 落ちで詰まることもなくなる。

> おもしろいことに、Claude は `uv` をまともに扱えない。気を抜くとそこらじゅうで `pip install` しまくるし、`uv` を使えと指示すると `uv pip install` としか書かない。6 月に AGI が来る？　無理くさくて泣ける。

### `CLAUDE.md` と `commands`

この 2 つを足すだけでも効果はデカい。

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

友人 [Jesse Vincent](https://fsck.com/) が作り込んだ [CLAUDE.md](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md) をパクってきた。特徴は――

- Big Daddy Rule のライト版  
- TDD のやり方  
- 俺の好きなコーディングスタイル  

> [@clint](https://instagram.com/clintecker) は `CLAUDE.md` に自分を “MR BEEF” と呼ばせていて、そのせいでドキュメントに「困ったら MR BEEF に聞け」みたいな文言が混入してる。この記事を書きながら、俺も “Harp Dog” と呼ばせることにした。これは機能であってバグじゃない。

`commands` も便利だ。俺の例は [dotfiles](https://github.com/harperreed/dotfiles/tree/master/.claude/commands) に置いてある。

{{< image src="commands.png"  >}}

昔はもっと多用してたけど、よく使うプロンプトを瞬時に叩き込めるのはやっぱり便利。引数も渡せる。たとえば GitHub Issue を見てもらうコマンドなら `/user:gh-issue #45` みたいに番号を渡せば、`gh-issue.md` に書いたスクリプトが走る。

プロジェクトごとに `commands` と `CLAUDE.md` を置くこともできる。俺は Hugo、Rust、Go、JavaScript など言語別にカスタムしてる。

## “Continue”

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

ときどき、ホーマーが ‘Y’ キーを押させる首振り鳥になった気分になる。ひたすら「continue」と打つか、↑ で同じプロンプトを貼り付けるだけ。

プランはたいてい 8〜12 ステップで、グリーンフィールド（既存コードなしの）開発でも言語や複雑さに関係なく 30〜45 分で完了することが多い。

友人の Bob に話したら信じてくれなかったので、「作るものと使う言語を決めてみ？」と聞いた。

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

彼の答えは「じゃあ C で BASIC インタプリタを」。

最高のチョイスとは言えない。俺は C もインタプリタもよく知らないし、正直やりたくもない。でも――もういい、やったれ。

上記の手順に従ったら Claude Code が大活躍して、[動く BASIC インタプリタ](https://github.com/harperreed/basic) ができた。初版は 1 時間以内に動き、さらに数時間いじり倒して、かなりイケてる出来になった。1982 年に出荷できたか？ **たぶんムリ。** でも [プロンプトプラン](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md) を見てみてほしい。

## チーム

うちのチーム全員が今 Claude Code を使っていて、上記プロセスをベースに各自チューニングしてる。

テストカバレッジは過去最高、コード品質も向上。それでも開発速度は昔のクソコード時代と同じくらい速い。席を見渡すと、ghostty、VS Code、Zed のターミナルや Python ノートで Claude Code がガシガシ走っているのが見えて面白い。

{{< image src="dril.jpg" >}}

トークンを山ほど持ってる人、どうか予算の組み方を教えてくれ。家族が死にかけてるんだ。

## thanks

メールをくれるみんな、あなたのワークフローやプロジェクトの話を聞くのは本当に楽しい。心から感謝！　これからもどんどん送ってくれ！