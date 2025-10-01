---
description: harper.blog의 콜로폰
hideReply: true
menu:
    footer:
        name: 콜로폰
        weight: 3
nofeed: true
title: 콜로폰
translationKey: colophon
type: special
url: colophon
slug: colophon
weight: 6
---

이 웹사이트 [harper.blog](https://harper.blog)은 Harper Reed의 개인 블로그입니다. 최신 웹 기술과 다양한 정적 사이트 생성(Static Site Generation) 기법들로 구축되었습니다.

## 기술 스택

- **정적 사이트 생성기**: [Hugo](https://gohugo.io/)
- **호스팅**: [Netlify](https://www.netlify.com/)
- **버전 관리**: Git(저장소는 GitHub에 호스팅됨)

## 디자인 및 레이아웃

- 이 사이트는 [Bear Cub](https://github.com/clente/hugo-bearcub) 테마를 기반으로 한 맞춤형 테마를 사용합니다 ᕦʕ •ᴥ•ʔᕤ
- ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•！
- 타이포그래피: 최적의 성능과 네이티브한 외관을 위해 시스템 폰트를 사용합니다
- 반응형 디자인을 적용해 다양한 기기와 화면 크기에서도 문제없이 표시됩니다

## 콘텐츠 관리

- 콘텐츠는 Markdown으로 작성됩니다

## 빌드 및 배포

- Netlify를 통해 지속적 배포(Continuous Deployment)를 설정했습니다
- 메인 브랜치에 변경 사항을 푸시하면 사이트가 자동으로 빌드되고 배포됩니다
- 사용자 정의 빌드 명령과 설정은 `netlify.toml`에 정의되어 있습니다

## 성능 최적화

- 가능한 경우 이미지를 WebP 형식으로 최적화해 제공합니다
- 프로덕션 빌드 시 CSS를 최소화합니다
- Hugo의 내장 애셋 파이프라인으로 리소스를 최적화합니다

## 추가 기능

- 콘텐츠 배포를 위한 RSS 피드를 제공합니다
- Twitter, Facebook 등 플랫폼에서의 공유를 위해 소셜 미디어 메타 태그를 구현했습니다
- 콘텐츠를 풍부하게 하기 위해 사용자 정의 숏코드(shortcode)(예: Kit.co 통합)를 사용합니다

## 개발 도구

- `Makefile`을 사용해 자주 쓰는 개발 작업을 간소화했습니다
- Go 모듈로 의존성을 관리합니다

## 접근성 및 표준

- 사이트는 접근성을 지향하며 최신 웹 표준을 준수합니다
- 전반에 걸쳐 시맨틱 HTML을 사용합니다

## 분석

- 이 사이트는 [tinylytics](https://tinylytics.app/)를 활용해 bits(티니애널리틱스 특유 지표)와 hits(조회수)를 추적합니다. 결과는 [여기](https://tinylytics.app/public/cw1YY9KSGSE4XkEeXej7)에서 확인할 수 있습니다.
- 다음 국가에서 {{< ta_hits >}}회의 조회가 있었습니다: {{< ta_countries >}}.

## 작성자 및 유지보수

이 사이트는 Harper Reed가 관리합니다. 문의 사항은 [harper@modest.com](mailto:harper@modest.com)으로 연락해 주세요.

마지막 업데이트: 2024년 9월

## 변경 로그

이번 버전의 git 커밋 로그는 다음과 같습니다:

{{% readfile file="gitlog.md" markdown="true" %}}

---

❤️를 담아 Hugo로 빌드하고 Netlify로 배포했습니다.
