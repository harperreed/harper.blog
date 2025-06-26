---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description: ソフトウェア開発におけるClaude Code AIアシスタントの活用方法を詳細に解説し、ワークフローのヒント、テスト手法、実プロジェクトの実践例を紹介します。防御的コーディング戦略、TDD、チームでの導入も扱います。
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
title: Basic Claude Code
translationKey: Basic Claude Code
---

いわゆる “agentic coding（エージェント指向コーディング）” がとにかく気に入っている。もう、あらゆる意味で魅力しかない。

[あの最初のブログ記事](/2025/02/16/my-llm-codegen-workflow-atm/)を書いてからというもの、Claude 界隈ではいろんなことが起きた。

- Claude Code
- MCP
- ほか

俺のワークフローを真似したとか、自分のやり方を語ってくれるメールが何百通も届いた（wat──「は？」ってレベルの数）。いくつかカンファレンスで登壇し、codegen のワークショップも何度か開いた。あと、スペルチェッカーは “codegen” を “codeine” に直したがるってことも学んだ。誰が想像した？

{{< image src="codegen.png" >}}

こないだ [友人](https://www.elidedbranches.com/)（彼女）と「**俺たち全員終わってる**し **AI が仕事を奪う**」なんて話（詳細はまた別の記事で）をしていたら、「Claude Code の記事を書けば？」と言われた。さぁ始めよう。

---

Claude Code がリリースされたのは、俺がワークフロー記事を書いてからわずか 8 日後で、予想どおり記事の多くが陳腐化した。それ以来 Aider から Claude Code に乗り換え、振り返っていない。Aider にも使い道はあるけど、今のところ Claude Code のほうが便利だ。

Claude Code は強力だし、そしてクソ高い。

とはいえワークフロー自体はほぼ変わっていない。

- `gpt-4o` とチャットしてアイデアを磨く
- 推論が強いモデルで仕様を生成する。最近は `o1-pro` か `o3`（`o1-pro` のほうが良い気がするのは、単に処理が遅いからかもしれない）
- そのモデルにプロンプトも書かせる。LLM にプロンプトを書かせるのは最高のハックだし、しかもオジサン世代がブチ切れるのがまた痛快
- 仕様書 spec.md と prompt_plan.md をプロジェクトルートに保存
- それから Claude Code に次を打ち込む

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

このプロンプトのキモは、prompt_plan.md をチェックして未完のタスクだけ拾い、実装→テスト→Git へコミット→prompt_plan.md 更新まで済ませたら一旦止まって指示を待つところだ。🤌

あとはソファに寝そべりつつ Claude に「yes」と返すだけ。フィードバックを求められたら応える。その間は Cookie Clicker をひたすら連打してる。そして気づけば魔法が起きている。

これがほんとにうまくいく。さらに威力を底上げする“スーパーパワー”をいくつか仕込める。

## ディフェンシブ・コーディング！

### テスト

テスト、特に TDD は必須だ。本気で TDD に取り組むことを全力で勧める。

昔の俺は TDD アンチで、下手だし時間のムダだと思ってた。でも完全に間違ってた。これまで数十年、会社やプロジェクトに大量のテストを足してきたけど、大半はコアを書いた後に付け足してきた。人間ならそれでいい。

これは **ロボットにとっては最悪** だ。

ロボは TDD が大好き。まずロボにテストとモックを書かせ、次のプロンプトでモックを実装に置き換える──この流れが最強だ。幻覚や LLM のスコープ逸脱へのいちばん効果的な対策だと思う。

### リンティング

リンティングは最高。Ruff は神、Biome もイケてる、Clippy は名前が秀逸。

ロボも良いリンターを回すのが大好物だ。

常にリンターを走らせる習慣はバグを減らし、保守性と可読性を高める。フォーマッタも入れれば完璧。

### pre-commit フック

真の魔法は、これら全部を pre-commit フックに突っ込むことだ。Python の `pre-commit` パッケージがおすすめ。`uv tools install pre-commit` で入れて `.pre-commit-config.yaml` を用意すれば、コミットのたびにテスト・型チェック・リンティングが自動実行され、コード品質は A+++、再実行してもバッチリ通る。

Claude Code と組み合わせると特に効果大。ロボは「コミットしたくてたまらない」ので、メチャクチャなコード変更をかまし、確実に全部ぶっ壊しやがる→直す…をやりがちだけど、pre-commit が止めてくれるおかげで GitHub Actions が詰まることもない。

> 面白いことに Claude は `uv` の使い方がまったく分からない。油断すると `pip install` を乱射するし、「uv を使え」と指示すると `uv pip install` とかやりだす。6 月に AGI が来るって？　ないない、残念。

### `CLAUDE.md` と commands

どちらもシンプルだけど効果はデカい。

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

友人の [Jesse Vincent](https://fsck.com/) から [`CLAUDE.md`](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md) を拝借した。彼が[めちゃくちゃ強化](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md)していて──

- 「ビッグダディ・ルール」のライト版
- TDD のやり方
- 俺流のコーディングスタイル

> [@clint](https://instagram.com/clintecker) は `CLAUDE.md` に自分を「MR BEEF」と呼ばせる設定にしていて、ドキュメント中に「困ったら MR BEEF に聞け」みたいなのが紛れ込んでいる。この記事を書きながら、俺も「Harp Dog」と名乗らせることにした。これは仕様だ、バグじゃない。

commands も便利だ。俺の例は [dotfiles](https://github.com/harperreed/dotfiles/tree/master/.claude/commands) をどうぞ。

{{< image src="commands.png" >}}

以前は commands をもっと使っていたが、よく使うプロンプトをサッと呼び出すのに最適だ。引数も渡せる。たとえば GitHub Issue なら `/user:gh-issue #45` のように番号を渡せば OK。Claude が `gh-issue.md` に定義した “prompt” スクリプトを実行してくれる。

プロジェクト直下に commands と `CLAUDE.md` を置けば、Hugo・Rust・Go・JavaScript みたいに言語や環境固有のコマンドも作れる。

## “Continue”

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

ときどき「y」を押すだけの鳥になった気分で、ひたすら「continue」と打つか、↑キーで同じプロンプトを貼り付ける。

プランはだいたい 8〜12 ステップ。新規開発なら言語や難易度を問わず 30〜45 分で完走できる。

友人 Bob にその話をしたら信じてくれなかったので、「作るものと言語を指定してみて」と頼んだ。

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

Bob「じゃあ C で BASIC インタプリタ」

正直キツい。C もインタプリタも詳しくないし、作りたいわけでもない。でもクソくらえ、やってみる。

例の手順で進めたら Claude Code が大活躍。結果、[動く BASIC インタプリタ](https://github.com/harperreed/basic) が完成した。初版は 1 時間以内に動いた。その後数時間いじってかなり良くなった。1982 年にリリースできたか？　たぶん無理。でも [prompt_plan.md](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md) を見れば流れが分かるはず。

## チーム

うちのチーム全員が今 Claude Code を使っている。基本は上の手順で、あとは各自で微調整。

テストカバレッジは過去最高、コードもキレイ。昔の汚いコードと同じくらい──いやそれ以上に──動く。ふと周りを見ると、ghostty や VS Code、Zed のターミナルで Claude Code が走り、Python ノートブックをいじっているのが見えて面白い。

{{< image src="dril.jpg" >}}

誰か大量にトークンを持ってる人、マジで予算を立てるのを手伝ってくれ。家族が死にそうだ。

## thanks

メールをくれる皆さんへ。あなたたちのワークフローやプロジェクトの話を聞くのは本当に楽しいし嬉しい。感謝しかない。これからもどしどし送ってくれ！
