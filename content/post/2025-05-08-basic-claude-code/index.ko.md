---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description: 워크플로 팁, 테스트 실천법, 실제 프로젝트 사례를 포함해 소프트웨어 개발에 Claude Code AI 어시스턴트를 활용하는
  방법을 자세히 안내합니다. 방어적 코딩 전략, TDD, 팀 적용 방법을 다룹니다
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
title: '클로드 코드 기초

  description: 워크플로 팁, 테스트 실천법, 실제 프로젝트 사례를 포함해 소프트웨어 개발에 Claude Code AI 어시스턴트를 활용하는
  방법을 자세히 안내합니다. 방어적 코딩 전략, TDD, 팀 적용 방법을 다룹니다'
translationKey: Basic Claude Code
---

나는 요즘 ‘에이전틱(Agentic) 코딩’에 푹 빠져 있다. 여러모로 *존나* 매력적이다.

[그 원본 블로그 글](/2025/02/16/my-llm-codegen-workflow-atm/)을 올린 뒤 Claude 월드(land)에서는 우후죽순 일이 터져 나왔다.

- Claude Code  
- MCP  
- etc

내 워크플로우 얘기, 그리고 *내 방식을 베껴 써서 앞서 나갔다*는 내용의 이메일을 수백 통(wat; “뭐라고?” 싶은 숫자)이나 받았다. 몇몇 컨퍼런스에서 발표도 하고, 코드 생성(codegen) 수업도 몇 번 했다. 한 가지 깨달은 건—컴퓨터는 ‘codegen’을 ‘codeine’으로 자꾸 교정하더라. ㅋㅋ

{{< image src="codegen.png"  >}}

며칠 전 [친구](https://www.elidedbranches.com/)랑 “우리 **다 같이 좆됐다**, **AI가 우리 일자리 싹 쓸어갈 거다**”(자세한 얘기는 다음 글에서!) 따위 얘기를 하다가, 그녀가 “클로드 코드 얘기도 좀 써 봐”라고 하더라.

자, 고!

Claude Code는 내 워크플로우 글이 올라간 지 딱 여드레 만에 출시됐다. 예측한 대로 글의 상당 부분이 바로 구닥다리가 됐다. 나는 Aider에서 Claude Code로 갈아탄 뒤 뒤돌아본 적 없다. Aider도 좋고 용도는 분명하지만, 지금은 Claude Code 쪽이 더 쓸만하다.

Claude Code는 강력하고, 전보다 *살벌하게* 겁나 비싸다.

내 워크플로우는 예전과 거의 같다.

- 아이디어는 `gpt-4o`랑 수다 떨면서 갈고닦는다.  
- 사양(spec)은 최고 추론 모델로 뽑아낸다. 요즘은 o1-pro나 o3(도대체 o1-pro가 더 나은 걸까, 아니면 오래 걸려서 그렇게 느끼는 걸까?).  
- 같은 모델로 프롬프트(prompt)도 짜게 한다. LLM에게 프롬프트를 쓰게 하는 건 정말 기가 막힌 해킹이다. 그러면 붐머들 혈압이 치솟는다.  
- `spec.md`와 `prompt_plan.md`를 프로젝트 최상위 경로에 저장한다.  
- 그리고 Claude Code에 이렇게 입력한다:

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

- 이 프롬프트의 묘미는 `prompt_plan.md`를 열어 “완료 표시 안 된 항목”을 찾은 다음, *가장 먼저 남아 있는* 작업을 처리한다는 점이다. Git에 커밋하고 `prompt_plan.md`에 완료 체크까지 해 둔 뒤, 멈춰서 사용자 리뷰·피드백을 기다리고 “계속할까요?”를 묻는다. 🤌  
- 나는 의자 뒤로 기대 “yes”만 치면 된다. 피드백 타임이 오면 마법이 펼쳐진다.  
- 그동안 쿠키 클릭커나 더 돌리면서 손가락만 까딱하면 된다.

이 방식, 기가 막히게 잘 먹힌다. 여기에 몇 가지 ‘슈퍼파워’를 더하면 효과가 훨씬 커진다.

## Defensive coding!

### Testing

테스트, 특히 테스트 주도 개발(TDD)은 필수다. 정말, 빡세게 TDD 습관을 들이길 권한다.

나도 한때 TDD 혐오자였다. 서툴렀고, 시간 낭비 같았다. 완전 착각이었다. ㅋㅋ 지난 수십 년 동안 회사와 프로젝트에 테스트를 잔뜩 달아 왔지만, 대개는 핵심 기능을 만든 *뒤에* 테스트를 붙였다. 사람한텐 그럭저럭 괜찮다.

**로봇한텐 최악이다.**

로봇들은 TDD를 *게걸스럽게* 받아먹는다.

TDD를 쓰면 로봇 친구가 테스트와 모의(mock) 객체를 먼저 짜고, 다음 프롬프트에서 그 모의를 실제 구현으로 바꾼다. 내가 찾은 환각·스코프 드리프트 방지책 중 가장 효과적이다. 로봇이 한눈 안 팔고 일한다.

### Linting

나는 린트(lint)를 정말 사랑한다. Ruff는 훌륭하고, Biome도 멋지며, Clippy는 귀엽다.

희한하게도 로봇은 좋은 린트를 돌리는 걸 **엄청** 좋아한다.

린트를 수시로 돌리면 버그가 줄고 코드가 더 읽기 쉬워진다. 포매터까지 더하면 뿅.

### Pre-commit 훅

진짜 마법은 이 모든 작업을 pre-commit 훅에 넣는 것이다. Python 패키지 `pre-commit`을 `uv tools install pre-commit` 한 줄로 깔고 `.pre-commit-config.yaml`만 작성하면 끝. 커밋할 때마다 테스트·타입 검증·린트가 돌아서 코드가 A+++ 등급이라 *언제든 다시 돌려도 될* 정도로 깔끔하게 유지된다.

Claude Code와 함께 쓰면 더욱 쾌적하다. 로봇은 *커밋하고 싶어 몸이 근질근질*하다. “코드 짜고 커밋해”라고 시키면 로봇은 코드를 마구 갈아엎고 커밋하고, 깨진 걸 다시 고친다.

덕분에 GitHub Actions가 린트·포맷 실패 로그로 범람하지 않는다.

> 웃긴 점 하나: Claude는 `uv`를 *도저히* 제대로 못 쓴다. 방심하면 `pip install`을 난사한다. `uv`를 쓰라고 지시해도 결국 `uv pip install`만 반복한다. AGI가 6월에 온다더니 글렀나. 슬프다.

### CLAUDE.md와 commands

작지만 생산성을 확 끌어올리는 두 가지 추가 옵션이다.

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

나는 친구 [Jesse Vincent](https://fsck.com/)이 [피 땀 흘려 만든](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md) [CLAUDE.md](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md)를 슬쩍 훔쳐 쓴다. 주요 내용은 다음과 같다.

- Big Daddy Rule의 라이트 버전  
- TDD 가이드  
- 내가 선호하는 코딩 스타일  

> [@clint](https://instagram.com/clintecker)은 CLAUDE.md에서 자길 ‘MR BEEF’라 부르도록 해 두었는데, 덕분에 문서마다 “막히면 MR BEEF에게 물어봐”라는 문구가 삽입되고 있다. 이 글을 쓰다가 나도 ‘Harp Dog’로 바꿨다. 기능이지 버그 아니다.

명령어(commands)도 꽤 쏠쏠하다. 내 dotfiles 예시는 [여기](https://github.com/harperreed/dotfiles/tree/master/.claude/commands).

{{< image src="commands.png"  >}}

예전엔 더 자주 썼지만, 자주 쓰는 프롬프트를 불러다 쓰기엔 여전히 훌륭한 수단이다. 인자를 넘길 수도 있다. 예컨대 GitHub 이슈는 이렇게: `/user:gh-issue #45`

그러면 Claude가 `gh-issue.md`에 정의된 프롬프트 스크립트를 수행한다.

이 명령어와 커스텀 CLAUDE.md를 프로젝트 디렉터리에 두면 Hugo, Rust, Go, JavaScript 등 언어·프레임워크별 전용 세팅도 가능하다.

## “Continue”

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

가끔은 ‘y’ 키를 눌러 주는 새를 책상 위에 올려 놓은 호머 심슨이 된 기분이다. 그저 “continue”를 입력하거나 ↑를 눌러 직전 프롬프트를 붙여 넣는다.

대부분 계획은 8~12단계다. 언어가 무엇이든, 겉보기 난도가 어떻든, 그린필드 프로젝트 하나를 30~45분이면 뚝딱 끝낸다.

친구 Bob은 못 믿겠다고 했다. 그래서 “뭘 만들고 싶은데? 언어도 골라 봐”라고 했다.

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

그가 “C로 BASIC 인터프리터”라고 했다.

썩 좋진 않았다. C도 잘 모르고, 인터프리터를 쓰고 싶지도 않았지만—그냥 X까고 해 보자.

위 단계를 그대로 밟았더니 Claude Code가 일을 냈다. [작동하는 BASIC 인터프리터](https://github.com/harperreed/basic)가 나왔다. 첫 버전은 한 시간도 안 돼 돌아갔고, 몇 시간 더 만지니 꽤 괜찮아졌다. 1982년에 출시했을까? 글쎄. [prompt_plan.md는 여기](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md)서 볼 수 있다.

## 팀 이야기

우리 팀 전원이 Claude Code를 쓰고 있다. 위 과정을 기본으로 깔고, 각자 살짝 튜닝했다.

테스트 커버리지는 역대 최고, 코드 품질도 좋아졌다. 과거의 끔찍한 코드랑 결과는 비슷하다. 사무실을 둘러보면 Ghostty, VS Code 터미널, Zed 터미널, 파이썬 노트북 등에서 Claude Code가 돌아가는 모습이 한눈에 들어온다.

{{< image src="dril.jpg" >}}

토큰이 남아도는 분, 제발 예산 좀 짜 달라. 우리 가족이 죽어 간다.

## thanks

이메일을 보내 준 모든 분께 감사한다. 여러분의 워크플로우와 프로젝트 이야기를 듣는 건 정말 즐겁다. 계속 보내 달라!