---
description: harper.blogの奥付
hideReply: true
menu:
    footer:
        name: コロフォン
        weight: 3
nofeed: true
title: コロフォン
translationKey: colophon
type: special
url: colophon
weight: 6
---

本サイト [harper.blog](https://harper.blog) は Harper Reed の個人ブログです。最新のWeb技術と静的サイト生成手法で構築しています。

## 技術スタック

- **静的サイトジェネレーター**: [Hugo](https://gohugo.io/)
- **ホスティング**: [Netlify](https://www.netlify.com/)
- **バージョン管理**: Git（GitHub上でホスティング）

## デザインとレイアウト

- [Bear Cub](https://github.com/clente/hugo-bearcub) テーマをベースにしたカスタムテーマを使用 ᕦʕ •ᴥ•ʔᕤ
- ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•！
- 最適なパフォーマンスとネイティブな外観を実現するため、システムフォントを使用
- レスポンシブデザインで各種デバイスと画面サイズに対応

## コンテンツ管理

- コンテンツはMarkdown形式で執筆

## ビルドとデプロイ

- NetlifyによるContinuous Deploymentを設定
- mainブランチへプッシュすると自動でビルドとデプロイが実行
- `netlify.toml`でカスタムビルドコマンドと設定を定義

## パフォーマンス最適化

- 画像を最適化し、可能な限りWebP画像形式で配信
- CSSを本番ビルド時に圧縮
- Hugoの組み込みアセットパイプラインでリソースを最適化

## 追加機能

- RSSフィードを提供
- TwitterやFacebookなどでの共有性向上のため、ソーシャルメディア用メタタグを実装
- Kit.co連携などに対応するカスタムショートコードでコンテンツを拡張

## 開発ツール

- 一般的な開発タスクを簡略化する `Makefile` を用意
- 依存関係管理に Go modules を使用

## アクセシビリティと標準

- アクセシビリティに配慮し、最新のWeb標準に準拠
- サイト全体でセマンティックHTMLを採用

## アナリティクス

- [tinylytics](https://tinylytics.app/) により “bits and hits”（アクセス統計）を計測。結果は [こちら](https://tinylytics.app/public/cw1YY9KSGSE4XkEeXej7) で公開
- このサイトは次の国々から {{< ta_hits >}} 件のアクセスを受けています: {{< ta_countries >}}

## 作者とメンテナンス

本サイトは Harper Reed が管理・運用。お問い合わせは [harper@modest.com](mailto:harper@modest.com) まで

最終更新: 2024年9月

## 変更履歴

今回のリリースのgitコミットログ:

{{< readfile file="gitlog.md" markdown="true" >}}

---

Hugoで構築し、Netlifyでデプロイ。💖 愛を込めてお届けしています。
