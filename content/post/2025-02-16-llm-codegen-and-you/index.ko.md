---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: 브레인스토밍부터 기획과 실행까지, LLM을 활용해 소프트웨어를 개발하는 현재 나의 워크플로우를 자세히 안내합니다.
draft: false
generateSocialImage: true
slug: my-llm-codegen-workflow-atm
tags:
    - LLM
    - coding
    - ai
    - workflow
    - software-development
    - productivity
title: "현재 나의 LLM 코드 생성 워크플로우"
translationKey: My LLM codegen workflow atm
---

_tl;dr: 아이디어를 브레인스토밍해 스펙을 만든 뒤, 그 스펙을 다시 한번 ‘계획’으로 세분화하고, LLM 코드 생성을 통해 실행한다. 단계마다 분리된(discrete) 루프가 있고, 마지막엔 마법이 찾아온다. ✩₊˚.⋆☾⋆⁺₊✧_

LLM으로 자잘한 제품을 정말 많이 만들어 왔다. 재미있고 유용하지만, 시간을 날려 버리는 함정도 곳곳에 있다. 얼마 전 친구가 “LLM으로 어떻게 소프트웨어를 짜?”라고 물었고, 나는 ‘이야기하려면 길어!’ 싶어 이 글을 쓰게 됐다.

(p.s. AI가 싫다면 맨 끝으로 바로 내려가도 좋다)

여러 개발자 친구들과 이야기해 보면 접근 방식은 거의 비슷하고, 각자 작은 변주만 있을 뿐이다.

아래 워크플로는 내 경험, 친구들의 조언(고마워요 [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki), [Erik](https://thinks.lol/)), 그리고 인터넷의 끔찍한 [나쁜](https://news.ycombinator.com/) [곳](https://twitter.com)들에서 건져 올린 베스트 프랙티스를 한데 모아 정리한 것이다.

이 방식은 **지금**은 잘 통한다. 2주 뒤에는 안 통하거나 두 배로 잘 통할 수도 있다. ¯\\\_(ツ)\_/¯

## 시작해 보자

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="AI가 만든 이미지는 늘 수상하다. 내 저글로 코딩 로봇 천사에게 인사!" >}}

개발 상황은 대체로 두 가지다.

- 그린필드(완전 신규) 코드
- 레거시(기존) 코드

두 경우 모두 내가 쓰는 과정을 보여 주겠다.

## 그린필드

신규 프로젝트에서는 다음 절차가 효과적이다. 견고한 기획·문서를 먼저 확보하고, 작은 단계로 나눠 부드럽게 실행할 수 있다.

{{< image src="greenfield.jpg" alt="Green field" caption="오른쪽에 보이는 초원이 technically 그린필드. Leica Q, 2016-05-14" >}}

### Step 1: 아이디어 다듬기

대화형 LLM(나는 ChatGPT 4o / o3를 주로 쓴다)으로 아이디어를 구체화한다.

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

브레인스토밍이 자연스럽게 마무리되면 이렇게 요청한다.

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

꽤 그럴싸한 스펙이 출력된다. 저장소에 `spec.md`로 저장해 두자.

> 이 스펙은 코드 생성뿐 아니라 추론 모델에게 “허점 좀 찾아 줘”라고 시켜 아이디어를 보강하거나, 화이트페이퍼·비즈니스 모델을 뽑아내는 데도 쓸 수 있다. 심층 리서치를 돌리면 약 1만 단어(5~6만 자) 분량의 해설서도 금세 받아볼 수 있다.

### Step 2: 계획 세우기

스펙을 추론 특화 모델(`o1*`, `o3*`, `r1`)에 넘긴다.

(다음은 테스트 주도 개발(TDD) 버전 프롬프트)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(다음은 비-TDD 버전)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

모델은 프롬프트 실행 계획서(prompt plan)를 내놓는다. `prompt_plan.md`로 저장해 두는 편이 좋다.

그리고 체크리스트용 `todo.md`도 요청한다.

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

코드 생성 도구가 작업하면서 `todo.md`를 체크해 주면 세션이 바뀌어도 상태를 유지하기 좋다.

#### 야호, 계획 끝!

이제 문서와 계획까지 갖췄다. 여기까지 **15 분**이면 충분하다. 정말 빠르다.

### Step 3: 실행

[GitHub Copilot Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude Engineer](https://github.com/Doriandarko/claude-engineer), [Sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [Claude.ai](https://claude.ai) 등 선택지는 무궁무진하다. 성공 여부는 2단계를 얼마나 잘했느냐에 달려 있다.

나는 웹 인터페이스 그대로의 Claude(순정 Claude)와 Aider 조합을 가장 좋아한다.

### Claude

[Claude.ai](https://claude.ai)와 페어 프로그래밍하듯 프롬프트를 하나씩 넣는다. 초기 보일러플레이트와 도구 설정은 사람이 직접 잡아 주는 편이 자유도가 높다. Claude가 리액트 코드를 남발하는 경향이 있어, 초기에 언어·스타일·툴 체계를 확실히 못 박아 두면 도움이 된다.

막히면 [repomix](https://github.com/yamadashy/repomix)로 코드베이스 전체를 넘겨 디버깅한다.

작업 흐름은 대략 이렇다.

- 저장소 초기화(보일러플레이트, `uv init`, `cargo init` 등)
- Claude에 프롬프트 붙여넣기
- Claude가 생성한 코드를 IDE에 붙여넣기
- 코드·테스트 실행
- …
- 잘되면 다음 프롬프트
- 안 되면 repomix + Claude로 디버깅
- 같은 과정을 반복 ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/)는 앞서 만든 프롬프트 실행 계획서와 궁합이 좋다. 적은 손질로도 멀리 갈 수 있다. “그냥 알아서 해준다” 모드라, 옆에서 [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/)를 돌려도 된다.

> 참고: Aider는 새로운 모델을 꼼꼼히 벤치마킹한 [LLM 리더보드](https://aider.chat/docs/leaderboards/)를 운영한다. 새 모델의 코드 생성 성능이 궁금할 때 큰 도움이 된다.

Aider는 테스트 스위트까지 실행하며 스스로 디버깅하기 때문에 훨씬 손이 덜 간다.

작업 흐름은 비슷하다.

- 저장소 초기화(보일러플레이트, `uv init`, `cargo init` 등)
- Aider 실행
- 프롬프트 붙여넣기
- Aider 춤 감상 ♪┏(・o･)┛♪
- Aider가 테스트 실행, 또는 직접 앱 실행
- 잘되면 다음 프롬프트
- 안 되면 Aider와 Q&A
- 같은 과정을 반복 ✩₊˚.⋆☾⋆⁺₊✧

### 결과

이 흐름으로 스크립트, Expo 앱, Rust CLI 툴 등 별별 것을 쏟아 냈다. 언어와 상황을 가리지 않고 잘 통한다.

미뤄 둔 프로젝트가 있다면 한번 시도해 보자. 짧은 시간에 생각보다 멀리 갈 수 있다.

## 레거시: 기존 코드, 한 뼘씩 개선하기

가끔은 그린필드가 아닌, 이미 돌아가는 코드베이스에 기능을 추가하거나 수정해야 할 때가 있다. 이때는 프로젝트 전체 대신 **작업 단위**로 계획을 세운다.

{{< image src="brownfield.jpg" alt="a brown field" caption="초원이 아닌 브라운필드. 할아버지가 60년대 우간다에서 찍은 랜덤 사진" >}}

### 컨텍스트 확보

AI 개발자마다 도구는 다르겠지만, 코드베이스를 묶어 효율적으로 LLM에 투입할 무언가가 필요하다. 나는 [repomix](https://github.com/yamadashy/repomix)와 `mise` 태스크 조합을 쓴다.

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

`output.txt`가 너무 크면 작업과 무관한 디렉터리를 제외하도록 명령어를 살짝 수정한다.

> `mise`의 장점은 저장소별 `.mise.toml`에서 태스크를 덮어쓸 수 있다는 점이다. 다른 도구로 코드를 묶더라도 `output.txt`만 만들어 주면 기존 LLM 태스크를 그대로 사용할 수 있다.

`output.txt`를 [LLM](https://github.com/simonw/LLM) CLI로 파이프해 마크다운으로 변환한다.

예를 들어 테스트 커버리지를 빠르게 보강하려면 다음과 같이 진행한다.

#### Claude

- 코드 저장소로 이동
- `mise run LLM:generate_missing_tests` 실행
- 생성된 `missing-tests.md` 확인
- `mise run LLM:copy_buffer_bundle`로 컨텍스트를 클립보드에 복사
- 그걸 Claude에 붙여넣고 첫 번째 이슈부터 처리
- Claude가 준 코드를 IDE에 붙여넣기
- …
- 테스트 실행
- 같은 과정을 반복 ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- 새 브랜치에서 Aider 실행
- `mise run LLM:generate_missing_tests` 실행
- `missing-tests.md` 확인
- 첫 번째 이슈를 Aider에 붙여넣기
- Aider 춤 감상 ♪┏(・o･)┛♪
- …
- 테스트 실행
- 같은 과정을 반복 ✩₊˚.⋆☾⋆⁺₊✧

이 방법은 거대한 코드베이스도 한 뼘씩 튜닝하기에 아주 좋다. 크든 작든 어떤 작업이든 무리 없이 처리할 수 있었다.

### 프롬프트 매직

아래 빠른 프롬프트들은 프로젝트를 더 탄탄하게 만드는 데 꽤 효과적이다.

#### Code Review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply  before writing the code review. Review every part, and don't hallucinate.
```

#### GitHub Issue Generation

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Missing Tests

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues  will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

솔직히 이 프롬프트들은 좀 구닥다리다(일명 ‘부머 프롬프트’). 더 좋은 아이디어가 있다면 꼭 알려 달라.

## 스키 타다 곤두박질 ᨒ↟ 𖠰ᨒ↟ 𖠰

이 과정을 설명할 때 나는 늘 이렇게 말한다.  
“지금 무슨 일이 진행 중인지 **적극적으로** 추적하지 않으면 금세 일을 앞질러 버릴 수 있다.”

왜인지 모르겠지만, LLM 얘기를 할 때마다 “over my skis”라는 표현이 떠오른다. 잘 닦인 파우더에서 순항하다가, 갑자기 방향을 잃고 절벽 아래로 굴러떨어지는 기분—딱 그 느낌이다.

계획 단계(앞서 말한 그린필드 방식)는 브레이크 역할을 해 준다. 특히 다소 공격적인 Aider 코딩에서는 테스트가 안전벨트다.

그래도 종종 **over my skis** 상태가 되곤 한다. 그럴 땐 잠깐 쉬거나 산책하면 의외로 금세 풀린다. 결국 일반적인 문제 해결 과정이지만, 속도가 광속이라는 점이 다를 뿐이다.

> 우리는 때때로 LLM에게 터무니없는 요구를 한다. 예를 들어 “lore 파일을 만들고 UI에서 참조해 줘”라면, 파이썬 CLI 툴에 갑자기 세계관과 글리치 UI가 탄생한다. 하늘이 한계다.

## 나, 너무 외로워 (｡•́︿•̀｡)

이 워크플로의 가장 큰 불만은 ‘싱글 플레이어 모드’라는 점이다. 혼자 코딩, 페어 프로그래밍, 팀 개발을 모두 해 봤지만—사람들과 함께할 때가 **항상 더 낫다**.  
지금 도구들은 팀으로 쓰기 꽤 까다롭다. 봇끼리 충돌하고 머지는 끔찍하며 컨텍스트도 복잡하다.

LLM 코딩을 멀티플레이 게임으로 만들어 줄 솔루션이 절실하다.

**GET TO WORK!**

## ⴵ 시간 ⴵ

코드 생산량은 폭증했지만, LLM이 토큰을 태우는 동안 대기 시간도 만만치 않다.

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="어제 일처럼 생생하다" >}}

나는 그 시간을 이렇게 보낸다.

- 다음 프로젝트 브레인스토밍
- 레코드 감상
- Cookie Clicker
- 친구·봇과 수다

이렇게 해킹! 해킹! 해킹! 해 본 적은 처음이다. 생산성이 폭발한다.

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

친구 중엔 “젠장, LLM은 다 구려”라고 말하는 이도 많다. 그런 시각을 존중한다. 내 걱정도 주로 전력 소모와 환경 영향이다. 그래도… 코드는 돌아가야 하니까. 휴.

사이보그 프로그래머가 될 생각은 없지만 조금이라도 궁금하다면 Ethan Mollick의 책 [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/)을 추천한다. 테크 광신서가 아니라 장단점을 균형 있게 짚어 준다.

‘약간 궁금하지만 여전히 회의적’이라면 언제든 연락해 달라. 우리가 LLM을 어떻게 쓰는지 보여 주고, 함께 무언가 만들어 보자.

_thanks to [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com), and [Erik](https://thinks.lol/) for taking a look at this post and suggesting edits. I appreciate it._
