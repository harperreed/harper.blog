---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: 브레인스토밍부터 계획 수립과 실행까지, LLM을 활용하여 소프트웨어를 개발할 때 내가 현재 사용하는 워크플로를 자세히 설명합니다.
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
translationKey: "My LLM codegen workflow atm"
---

_tl;dr: 스펙을 브레인스토밍한 뒤 → ‘계획을 위한 계획’을 세우고 → LLM 코드 생성(codegen)으로 실행한다. 각 단계는 독립 루프. 그리고 매직! ✩₊˚.⋆☾⋆⁺₊✧_

LLM 덕분에 작은 제품을 진짜 많이 만들었다. 재미있고 유용하다. 하지만 시간을 왕창 잡아먹는 함정도 수두룩하다. 얼마 전 친구가 “LLM으로 어떻게 소프트웨어를 짜?”라고 묻길래 “이야, 시간 좀 있어?” 싶어 이 글을 쓴다.

(p.s. AI가 싫다면 ― 맨 끝으로 스크롤!)

개발자 친구들과 이야기해 보면 저마다 약간씩 다르게 튜닝한다.

아래 워크플로는 내 경험, 친구들과의 대화(고마워요 [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki), [Erik](https://thinks.lol/)), 그리고 인터넷의 악명 높은 구석구석([Hacker News](https://news.ycombinator.com/), [X/Twitter](https://twitter.com) 같은)에서 떠도는 베스트 프랙티스를 뒤섞어 만들었다.

지금은 **엄청** 잘 통하지만 두 주 뒤엔 안 통하거나 두 배로 잘 통할 수도 있다. ¯\_(ツ)\_/¯

## 시작!

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="AI가 만든 이미지는 늘 수상하다. 저글로(Juggalo) 광대 분장의 코딩 로봇 천사에게 인사!" >}}

개발 방식은 여럿이지만 내 경우는 대체로 둘이다.

- 그린필드(Greenfield) 코드
- 레거시(?) ‘모던’ 코드

두 갈래 모두의 과정을 차례로 소개한다.

## Greenfield

그린필드 개발에는 다음 프로세스가 잘 맞는다. 탄탄한 계획과 문서를 갖추고, 작은 단계로 쉽게 실행할 수 있다.

{{< image src="greenfield.jpg" alt="Green field" caption="오른쪽에 진짜 그린필드가 있다. Leica Q, 2016-05-14" >}}

### Step 1: 아이디어 다듬기

대화형 LLM(ChatGPT 4o / o3)을 이용해 아이디어를 정제한다.

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

아이디어가 충분히 정리됐다고 느끼면:

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

꽤 괜찮은 스펙이 나온다. 리포지토리에 `spec.md`로 저장한다.

> 이 스펙은 여러 용도로 쓸 수 있다. 우리는 코드 생성에 쓸 거지만, 추론 모델에 넘겨 아이디어의 허점을 찾거나(더 깊이!), 백서를 만들거나 비즈니스 모델을 뽑아내거나, 1만 단어짜리 지원 문서를 받아내도 좋다.

### Step 2: Planning

`spec.md`를 추론 특화 모델(`o1*`, `o3*`, `r1`)에 보낸다.

(아래는 TDD용 프롬프트)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(TDD를 안 쓸 때)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

프롬프트 계획이 출력된다. `prompt_plan.md`로 저장한다.

이어 체크리스트용 `todo.md`를 만든다.

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

코드 생성 도구가 `todo.md`를 체크해 가며 상태를 유지하기 좋다.

#### 플랜 완성! 야호!

이제 탄탄한 계획과 문서를 손에 넣었으니 실행만 남았다.

전체 과정은 **15분**이면 끝난다. 솔직히 미친 속도다 (wild tbh).

### Step 3: Execution

도구는 정말 많다. 2단계를 잘 해두면 무엇으로 돌려도 성공 확률이 높다.

[GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude Engineer](https://github.com/Doriandarko/claude-engineer), [Sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [Claude.ai](https://claude.ai) 등 써본 도구마다 잘 작동했다.

나는 별도 래퍼 없이 **생(生) Claude**(API 직통 또는 기본 UI)와 Aider 조합을 선호한다.

### Claude

[Claude.ai](https://claude.ai)와 페어 프로그래밍하듯 프롬프트를 하나씩 넣는다. 왔다 갔다가 번거롭지만 대체로 잘 굴러간다.

초기 보일러플레이트와 툴 셋업은 내가 직접 한다. Claude가 React 코드만 던지는 버릇이 있어 원하는 언어·스타일·툴 체계를 먼저 잡아두면 편하다.

막히면 [repomix](https://github.com/yamadashy/repomix)로 코드베이스 전체를 넘겨 디버깅한다(뒤에서 다시 다룬다).

워크플로:

- 리포지토리를 초기화한다(보일러플레이트, `uv init`, `cargo init` 등)
- Claude에 프롬프트 붙여넣기
- Claude가 준 코드를 IDE에 붙여넣기
- 코드·테스트 실행
- …
- 잘 되면 다음 프롬프트
- 안 되면 repomix로 디버깅
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/)는 재미있고 묘하다. 2단계에서 뽑은 프롬프트 계획과 궁합이 특히 좋다.

워크플로는 거의 같지만, 프롬프트를 Aider에 붙여넣는다는 점만 다르다.

Aider가 “Just do it” 해주고 나는 [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/)를 두드리며 논다.

> 참고: Aider는 [LLM 리더보드](https://aider.chat/docs/leaderboards/)에서 새 모델의 코드 생성 성능을 깔끔하게 벤치마킹한다. 새 모델 효율을 보기 좋은 자료다.

테스트까지 자동으로 돌려주니 손이 훨씬 덜 간다.

워크플로:

- 리포지토리를 초기화한다(보일러플레이트, `uv init`, `cargo init` 등)
- Aider 실행
- 프롬프트 붙여넣기
- watch aider dance ♪┏(・o･)┛♪
- Aider가 테스트를 돌리거나 직접 앱을 실행해 확인
- 잘 되면 다음 프롬프트
- 안 되면 Q&A로 수정
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

### Results

이 방식으로 스크립트, Expo 앱, Rust CLI 등 정말 많~이 만들었다. 언어와 상황 가리지 않고 잘 된다.

영화를 보면서도 새로운 아이디어가 떠오르면 바로 만들어 버린다. 작은 프로젝트든 큰 프로젝트든 미뤄둔 게 있다면 한번 써보라. 짧은 시간에 놀랄 만큼 진도가 나간다.

내 ‘해킹 to-do 리스트’는, 다 만들어 버린 덕에 텅 비었다. 새 아이디어만 떠오르면 바로 구현하고 있다. 덕분에 오랜만에 새로운 언어와 툴을 만지며 프로그래밍 시야가 확 넓어졌다.

## Non-greenfield: 점진적 개선

때로는 그린필드가 아니라 이미 있는 코드베이스를 조금씩 다듬어야 한다.

{{< image src="brownfield.jpg" alt="a brown field" caption="이건 브라운필드다. 할아버지 카메라에 담긴 1960년대 우간다 어딘가" >}}

이 경우 방법이 조금 다르다. 프로젝트 전체가 아니라 작업 단위로 계획한다.

### Get context

AI 개발자마다 도구는 다르지만, 핵심은 소스 코드를 잘 추려 LLM에 효율적으로 집어넣는 것이다.

나는 [repomix](https://github.com/yamadashy/repomix)를 쓴다. 전역 `~/.config/mise/config.toml`에 작업 모음을 정의해 두었다([mise 규칙](https://mise.jdx.dev/)).

LLM 작업 목록:

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

`output.txt`로 컨텍스트를 추출한다. 토큰이 초과되면 관련 없는 부분을 제외하도록 명령을 수정한다.

> `mise`의 좋은 점은 작업을 해당 디렉터리의 `.mise.toml`에서 재정의·오버라이드할 수 있다는 것. 코드 덤프 도구를 바꿔도 `output.txt`만 나오면 LLM 작업을 그대로 쓸 수 있다. 코드베이스 구조가 제각각이라 자주 `repomix` 단계를 덮어쓰거나 더 효율적인 툴로 갈아탄다.

`output.txt`가 생기면 [LLM](https://github.com/simonw/LLM) 명령에 파이프로 넘겨 변환하고 결과를 마크다운으로 저장한다.

결국 mise 작업은  
`cat output.txt | LLM -t readme-gen > README.md`  
또는  
`cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md`  
같은 꼴이다. `LLM` 명령이 모델 선택, 키 관리, 프롬프트 템플릿을 맡아준다.

예컨대 테스트 커버리지를 빠르게 보강해야 할 때:

#### Claude

- 코드 디렉터리로 이동
- `mise run LLM:generate_missing_tests` 실행
- 생성된 `missing-tests.md` 확인
- `mise run LLM:copy_buffer_bundle`로 컨텍스트를 클립보드에 복사
- Claude에 붙여넣고 첫 번째 ‘누락 테스트’ 이슈부터 해결
- Claude가 준 코드를 IDE에 붙여넣기
- …
- 테스트 실행
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- 코드 디렉터리로 이동
- 새 브랜치에서 Aider 실행
- `mise run LLM:generate_missing_tests` 실행
- `missing-tests.md` 확인
- 첫 번째 ‘누락 테스트’ 이슈를 Aider에 붙여넣기
- watch aider dance ♪┏(・o･)┛♪
- …
- 테스트 실행
- rinse repeat ✩₊˚.⋆☾⋆⁺₊✧

이 방식으로 규모와 상관없이 어떤 작업도 해낼 수 있었다.

### Prompt magic

이런 퀵 해킹은 프로젝트를 더 탄탄하게 만든다. 빠르고 효과적이다.

기존 코드에 쓰는 내 단골 프롬프트 몇 가지:

#### Code review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply  before writing the code review. Review every part, and don't hallucinate.
```

#### GitHub Issue generation

(실제 이슈 등록은 아직 자동화 못 함!)

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Missing tests

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues  will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

이 프롬프트들은 좀 구닥다리(“boomer prompts”랄까). 더 좋은 아이디어가 있으면 꼭 알려 달라.

## Skiing ᨒ↟ 𖠰ᨒ↟ 𖠰

이 과정을 친구들에게 설명할 때면 “정신 바짝 차리고 진행 상황을 추적해야 한다, 안 그러면 금방 스스로를 앞질러 버린다”고 말한다.

나는 ‘over my skis’(스키가 너무 앞으로 나가 균형을 잃는 상황)라는 표현을 자주 쓴다. 왜인지는 모르지만 꽂힌다. 부드러운 파우더를 가르며 달리다가, 어느 순간 “WHAT THE FUCK IS GOING ON!” 하고 소리치며 절벽 아래로 곤두박질치는 그런 느낌이다.

**Planning 단계**(그린필드 과정 참조)를 두면 통제력이 생긴다. 문서를 보고 재확인할 수 있다. 특히 Aider처럼 와일드하게 코딩할 때는 테스트가 큰 도움이 된다.

그래도 가끔은 여전히 **over my skis** 상태가 온다. 잠깐 쉬거나 산책하면 머리가 리셋된다. 문제 해결 과정 자체는 평범하지만 속도가 광속이라 그렇다.

> 우리는 종종 LLM에게 엉뚱한 걸 코드에 끼워 넣으라고 시킨다. 예컨대 ‘lore 파일을 만들고 UI에서 참조하라’고 요구하면 파이썬 CLI 툴에도 lore와 글리치 UI가 생겨난다. 하늘이 한계다.

## I am so lonely (｡•́︿•̀｡)

단점 하나: 대부분 **싱글 플레이 모드**다. 팀으로 쓰기 어렵다. 봇끼리 충돌하고, 머지는 끔찍하고, 컨텍스트는 복잡하다.

LLM 코딩을 멀티플레이 게임으로 바꿔 줄 누군가가 절실하다. 솔로 해커 경험이 아니라 다 같이 즐길 수 있도록. 기회가 어마어마하다.

**어서 일해라!**

## ⴵ Time ⴵ

코드 생성 덕분에 한 사람이 찍어내는 코드 양이 폭증했다. 반면 LLM이 토큰을 태우는 동안 ‘대기 시간’도 길어졌다.

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="이 화면, 어제 본 것처럼 생생하다" >}}

그래서 기다리는 시간에는:

- 다른 프로젝트 브레인스토밍
- LP 꺼내 음악 듣기
- Cookie Clicker를 두드리며 놀기
- 친구·로봇과 수다

이렇게 해킹할 수 있다니 멋지다. Hack Hack Hack. 이렇게 생산적이었던 적이 또 있었나?

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

주변엔 “LLM 별로야, 다 못 해”라는 친구도 많다. 비판적 시각은 중요하다. 나도 전력 소모와 환경 영향을 걱정한다. 하지만… 코드는 흘러야지. 하아.

더 알고 싶지만 ‘사이보그 프로그래머’까지는 싫다면 Ethan Mollick의 책 [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/)을 권한다.

기술 낙관·자본 예찬이 아닌 균형 잡힌 시선으로 LLM 활용법을 설명한다. 읽은 친구들과 깊은 대화를 나눌 수 있었다. 강추!

회의적이지만 조금이라도 궁금하다면 언제든 연락하라. LLM을 어떻게 쓰는지 보여주고, 함께 뭔가 만들어 볼 수도 있다.

_thanks to [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com), and [Erik](https://thinks.lol/) for taking a look at this post and suggesting edits. I appreciate it._
