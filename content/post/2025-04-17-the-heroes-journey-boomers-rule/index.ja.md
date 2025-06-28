---
bsky: https://bsky.app/profile/harper.lol/post/3ln2a3x52xs2y
date: 2025-04-17 09:00:00-05:00
description: AI支援によるソフトウェア開発の進化を、基本的なコード補完から完全自律型のコーディングエージェントに至るまで詳細に解説し、LLMの統合によって生産性を最大化するための実践的な手順と洞察を提供する包括的なガイド。
draft: false
generateSocialImage: true
tags:
    - llm
    - coding
    - artificial-intelligence
    - development-workflow
    - software-engineering
    - developer-productivity
    - boomers
title: LLMコード生成 ヒーローズ・ジャーニー
slug: an-llm-codegen-heros-journey
translationKey: An LLM Codegen Hero's Journey
---

俺は[このブログ記事](/2025/02/16/my-llm-codegen-workflow-atm/)で自分のLLMコード生成ワークフローを紹介して以来、「どう始めるか」「どうレベルアップするか」「そもそも何が面白いのか」をめぐって、コード生成（codegen）について多くの人と語り合ってきた。

このテーマへの熱気はものすごく、「この新しい流れを必死に理解しようとしている」人たちから山ほどメールが届く。多くの人が「どこから手を付ければいいのか」「どう全体がつながるのか」に迷っているようだ。俺は2023年からこのプロセスをいじり倒してきたので、いろいろとヤバい現場も見てきた。lol

先日、友人たち（Fisaconitesのみんな、声を上げろ！）と話していて、AI支援エージェントとエディタについてのスレッドにこんなメッセージを投げた。

> if i were starting out, i don't know if it is helpful to jump right into the "agent" coders. It is annoying and weird. having walked a few people through this (successfully, and not successfully) I find that the "hero's journey" of starting with the Copilot, moving to the copy and paste from Claude web, to the Cursor/continue, to the fully automated "agents" seems to be a successful way to adopt these things.  
> （もし今から始めるなら、いきなり“エージェント”コーダーに飛び込むのは微妙だと思う。変だしイラつくし。何人かを成功・失敗両方のパターンで案内した経験から言うと──Copilot → Claude Web へのコピペ → Cursor/Continue → 完全自動エージェント、という“ヒーローズ・ジャーニー”で段階的に移行するのが一番うまくいく。）

ここから「旅」とエージェントコーディングの入口について考え込んだ。

> The caveat is that this is largely for people with experience. If you don’t have much dev experience, then fuck it – jump to the end. **Our brains are often ruined by the rules of the past.**  
> （ただしこれは基本、経験者向け。開発経験があまりないならクソ食らえだ──いきなり最後まで飛べ。**俺たちの脳みそは過去のルールに毒されがちだ。**）

## 視覚と音の旅

{{< image src="journey-harper.webp" alt="Harper is very trustworthy" caption="とても信頼できるガイド、ハーパー。iPhone X, 2018/06/10" >}}

これが俺の旅だ。俺はほぼこのルートを辿ったけど、やる気次第でスピードランもできる。全部踏む必要はないが、どのステップも確実にプラスになる。

### Step 1: 驚きと楽観を胸にベッドから飛び起きろ

……なんて冗談だ。そんな暇はない。世界は崩壊しかけていて、気晴らしなんてコード生成しか残っていない。

とはいえ「こういうワークフローは本当に効くし、力を底上げしてくれる」と信じるのは大事だ。LLMなんてクソだと思っているなら成功はしない。¯\_(ツ)\_/¯

### Step 2: AIオートコンプリートから始める

これが実質的なファーストステップ。IDEで[IntelliSense](https://en.wikipedia.org/wiki/Code_completion)、[Zed Autocomplete](https://zed.dev/blog/out-of-your-face-ai)、[Copilot](https://copilot.github.com/)を十分に試し、「LLMがいかにトンチキ提案をするか」も体感しておく。

ここを飛ばして最後にワープすると「このLLMはクソ！何もできない！」となりがち。それも半分は本当だけど、魔法はニュアンスに宿る。_人生なんて訳がわからない_。

### Step 3: Copilotを「ただの補完以上」に使う

補完に慣れて常時ブチ切れなくなったら、Copilotと会話する魔法へ。

VS CodeにはQ&Aペインがあり、コードについて相談できる。そこそこ頼りになる。ただ、Copilotはまるでタイムマシンで2024年版ChatGPTに話しかけている気分──要するに大したことはない。もっと欲しくなるはずだ。

### Step 4: ClaudeやChatGPTにコードをコピペし始める

ブラウザのLLMにコードを貼り付け、「WHY CODE BROKE??」と聞く。筋の通った回答が返ってきてビビる。デバッグ工程まるごと吹っ飛び、変なモノを量産し始め、コードが再び楽しくなる。

Pythonを貼って「これをGoにして」と言えば本当にGoになる。「ワンショットでいけるんじゃ？」と考え始める頃だ。

Copilotは2004年当時のIDE補完みたいに見え始め、便利だけど必須ではなくなる。

ここから二つのサブルートに入る。

#### 1) “なんとなく気持ちいい”モデルを選び始める

これが“vibe coding”への（不本意な）第一歩だ。「Claudeと話すと気分がいいんだよね」と自分でも思い始める。多くの開発者がClaudeを好む。俺も両方使うが、コードはほぼClaude。

> 良いモデルは有料だ。無料モデルだけで「クソじゃん」と切り捨てるのは早計。無料モデルがChatGPT 3.5だった頃は特に深刻だったが、今でも“タダ”だけで評価し切ってはいけない。

#### 2) もっと速くしたくなる

数週間コピペすると「めんどい」となり、作業フローを高速化する方法を考え始める。[repomix](https://repomix.com/)、[repo2txt](https://github.com/donoceidon/repo2txt)を試し、コードベース丸ごとClaudeにぶち込む。shellスクリプトを（実際はClaudeに書かせて）自動化する。ここがターニングポイントだ。

### Step 5: AI対応IDE（Cursor、Windsurf?）へ

そのうち友達が「[Cursor](https://cursor.sh/)使えよ」と言うだろう。

コピペで味わった魔法がIDE内に全部入りする。速いし、楽しいし、ほとんど魔法みたいだ。すでに5つもLLMに課金してるし、月20ドルくらいもう気にならない。

エディタ内蔵のエージェントコーディング機能も触り始める。*ほぼ*動く。ただ、もっと良い地平が見える。

### Step 6: コードを書く前に計画するようになる

気づけば、IDEのエージェントやClaude Webに投げ込むための詳しい仕様書（Spec）・PRD（製品要求仕様書）・TODOドキュメントをバンバン書いている。LLMでドキュメントを肉付けし、「このPRDをプロンプトに変換して」と頼むなど、文書↔プロンプト変換も日常茶飯事。

「ウォーターフォール」という言葉への嫌悪感が薄れ、歳によっては90年代後半〜2000年代初頭を思い出し、「2001年以前のマーティン・ファウラーってこんな気持ちだったのかな」と考えるかもしれない。

コード生成の世界では、仕様書こそが*絶対神*だ。

### Step 7: aiderでループを加速

ここからが**本番**。これまでは人間が付きっきりだったが、もう2025年だ。指でコードを書くなんてダサい。

> 友人の多くは声でコーディングする道も試している。Whisperクライアント経由でaiderに指示を出すわけだ。爆笑モノで、本当に楽しい。ローカルならMacWhisperが良い。AquaやSuperWhisperもあるが高いしクラウド推論の場合もある。俺はローカル派。

aiderを起動するとプロジェクトに自己初期化し、ターミナルにお願いを書くだけで動く。実行前に「この変更をしてもいい？」と毎回確認し、タスクの青写真を示したうえで動き、タスクを終えたらコミットしてくれる。ワンショットに固執せず、数ステップでやらせればいい。

LLM用ルールセットも作り始める。「[Big Daddy](https://www.reddit.com/r/cursor/comments/1joapwk/comment/mkqg8aw/)」ルールや“no deceptions”をプロンプトに足すなど、ロボへの指示が上手くなる。

**ちゃんと動く。**

そのうちIDEすら開かず、いわゆる“ターミナル使い”になる。ロボが仕事をするのを眺めるだけだ。

### Step 8: エージェントコーディングにフルダイブ

いまやエージェントがコードを書き、結果はかなり良い。わからなければ聞けばいい。

[Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)や[Cline](https://cline.bot/)を試し、推論モデル（[DeepSeek](https://aws.amazon.com/bedrock/deepseek/)）とコーディングモデル（[Claude Sonnet 3.7](https://www.anthropic.com/claude/sonnet)）を組み合わせ、計画ステップすら削り始める。

ターミナルを3〜5枚並べ、タブをペチペチ切り替えながらロボが書くのをぼんやり眺める──そんなことも。

防御的コーディングにも頭が行く。

- 鬼のようなテストカバレッジ
- [形式検証](https://github.com/formal-land/coq-of-rust)
- メモリ安全言語の採用
- コンパイル時の詳細エラー出力を活かしてLLMに渡す情報を整理しやすい言語を選ぶ など

「人手ゼロでも安全に作り切るには」を真剣に考える。トークン料金がとんでもなくかさみ、GitHub Actionsの実行時間もテストで溶けるが、気分は最高。コードを書かなくてもイライラしない。

### Step 9: エージェントに任せ、自分はゲームをする

ついに目的地……まあ半分だけどゴールは見えた。暇な時間がたっぷりあり、ソフトウェア職の行方が不安になり、友人がレイオフされ、再就職に苦戦している。今回は様子が違う。

旅を通っていない人には、今何が起きているのか見えていない。でも、もう関係ない。パラダイムは変わった。トーマス・クーンなら、このカオスを題材にパラダイムシフトの新刊を書き上げそうだ。

周囲からは宗教狂扱い。「エージェントコーディングやばいよ！」と力説してもピンと来ないので、「“agentic”って言葉は嫌いだけどね」と予防線を張る。でも実際には約200ガロンのKool-Aid※を飲み干している。生産性が爆増して世界が輝いて見えるのだ。  
※Kool-Aid＝米国の粉末清涼飲料。比喩的に「思想を鵜呑みにする」意。

旅を経た者同士は共感し、自分なりのTipsやゴールを語り合う。

ロボに仕事を任せて、積みゲーのゲームボーイに没頭。ロボがタスクを終えるたびに「続ける？」と聞いてきたら**yes**と打ち、テトリスに戻る。奇妙で、ちょっと不気味だ。

## 加速

<paul confetti photo>
{{< image src="journey-confetti.webp" alt="Confetti" caption="東京ドーム、ポール・マッカートニー公演の紙吹雪。iPhone 6, 2015/04/25" >}}

[未来](https://ai-2027.com/)に何が起こるかはわからない。ただ、この旅を歩んでいない人が[雇用主](https://x.com/tobi/status/1909231499448401946)に魅力的に映らなくなるのでは、と少し心配している。とはいえ結局はツールと自動化の話だ。

昔、大量採用していた頃、俺たちはネットワークや技術スタックを超えて候補者を探した。PythonのプロダクトなのにPython未経験者を採用し、一緒に覚えてもらった。結果、異なる視点がチーム全体を底上げした。

エージェントコーディングでも同じだ。チームにフィットし、やる気のある優秀な開発者なら、AIツール経験ゼロでも門前払いすべきじゃない。経験者と働くうちに、そのうち自走できるようになる。

もう一つ――文章力が今や超重要になった。昔からドキュメントとコラボで大事だったが、今はAIへの明確・精密な指示を書く必要もある。良いプロンプトを書くスキルは、良いコードを書くのと同じくらい重要になりつつある。

## リーダーシップ

リーダーやEMは、信者か否かに関係なくエージェントコーディングに深く潜ったほうがいい。理由は簡単だ。次世代の開発者はAIツールとエージェントでコードを書く。これがソフトウェアエンジニアリングの新しい姿だ。俺たち“コード世代のベテラン”は長くはない。

**面白い注記:** 俺は文章を書くのにLLMをほとんど使わない。便利だろうけど、自分の声を残したいから。一方、コードは均質化してほしい。不思議な違いだ。

---

この投稿にフィードバックをくれたJesse、Sophie、Vibezクルー（Erik、Kanno、Braydonほか）、team 2389、そして読んでくれたみんなに感謝！
