---
date: 2024-04-12 09:00:00-05:00
description:
    siglip/CLIP과 벡터 이미지 인코딩을 활용해 마법 같은 밈 검색 엔진을 만들었다. 이 과정은 이 강력한 기술을 배우는
    재미있는 방법이었다. 여러분도 직접 만들어 보고 사진 라이브러리 속 숨겨진 보석을 발견할 수 있도록 코드를 공유한다. 우리의 이미지에 AI의 힘을
    마음껏 발휘해 보자!
draft: false
generateSocialImage: true
slug: i-accidentally-built-a-meme-search-engine
tags:
    - meme-search-engine
    - vector-embeddings
    - applied-ai
    - siglip
    - image-search
title: "실수로 밈 검색 엔진을 만들어버렸다"
translationKey: I accidentally built a meme search engine
---

## 혹은: CLIP·SigLIP과 이미지 벡터 인코딩을 배우는 법

_tl;dr_: SigLIP/CLIP으로 이미지 벡터를 활용해 밈 검색 엔진을 만들었다. 정말 재미있었고 배운 것도 많았다.

나는 한동안 실용적인 AI 도구를 이것저것 만들어 왔다. 그중에서도 가장 마법처럼 느껴졌던 구성 요소가 벡터 임베딩이었다. [Word2Vec](https://en.wikipedia.org/wiki/Word2vec)을 처음 봤을 때 머리가 멍해질 정도였다. 정말 마술 같았다.

[해커뉴스에서 본 간단한 앱](https://news.ycombinator.com/item?id=39392582)이 [매우 인상적](https://mood-amber.vercel.app/)이었다. 누군가 텀블러 이미지를 긁어 온 뒤 [SigLIP](https://arxiv.org/abs/2303.15343)으로 임베딩을 만들어 “이미지를 클릭하면 비슷한 이미지를 보여주는” 앱을 뚝딱 만든 것이다. 진짜 마술 같았다. 방법은 몰랐지만, 왠지 나도 해볼 수 있을 것만 같았다.

그래서 이 갑작스러운 동기를 “도대체 이게 어떻게 돌아가는지” 직접 배울 기회로 삼았다.

## wut

벡터 임베딩, CLIP·SigLIP, 벡터 데이터베이스 같은 개념이 낯설다면 걱정 마시라.

해커뉴스 글을 보기 전까지 나도 벡터 임베딩이나 멀티모달 임베딩, 벡터 데이터베이스에 대해 깊이 고민해 본 적이 없었다. 예전에 FAISS(페이스북의 간단한 벡터 스토어)와 Pinecone(유료)을 써서 간단히 테스트해 본 정도였다. “돌아가네? 테스트 통과!” 하고 말았던 수준이다.

사실 아직도 벡터가 뭔지 제대로 안다기보다는 어렴풋이 알고 있는 정도다, lol. 이번에 직접 만들어 보기 전까지는 RAG나 다른 LLM 프로세스 외에 어디에 쓸 수 있을지 감이 없었다.

나는 만들어 보면서 배우는 타입이다. 결과가 흥미롭고, 약간 마법 같으면 더 열심히 하게 된다.

### WTF 용어집

원고를 미리 읽어 준 친구들 중 몇 명이 “X가 뭐냐?”고 묻길래, 나도 처음엔 생소했던 단어를 짧게 정리했다.

- **Vector Embedding(벡터 임베딩)** – 텍스트나 이미지를 수치 벡터로 변환해 비슷한 항목을 효율적으로 찾을 수 있게 해 준다.
- **Vector Database(벡터 데이터베이스)** – 이렇게 인코딩된 벡터를 저장·검색해 유사 항목을 빠르게 찾아 주는 데이터베이스.
- **Word2Vec** – 단어를 벡터로 변환해 유사어를 찾고 의미 관계를 탐색할 수 있게 만든 혁신적 기법.
- **CLIP** – OpenAI가 만든 모델로 이미지와 텍스트를 동일한 벡터 공간에 인코딩한다.
- **OpenCLIP** – OpenAI의 CLIP을 오픈소스로 구현한 버전으로, 누구나 자유롭게 사용하고 확장할 수 있다.
- **FAISS** – 대규모 벡터 컬렉션을 빠르게 관리·검색할 수 있게 해 주는 라이브러리.
- **ChromaDB** – 이미지·텍스트 벡터를 저장하고 즉시 비슷한 결과를 반환해 주는 벡터 데이터베이스.

## Keep it simple, Harper.

이건 꽤 단순한 해킹 프로젝트다. 그냥 이것저것 만지작거리는 수준이라 확장성에는 크게 신경 쓰지 않았다. 대신 **누구나** 적은 노력으로 그대로 실행할 수 있게 만드는 데 관심이 있었다.

또 다른 목표는 모든 과정을 노트북에서 로컬로 돌리는 것이었다. 새 Mac의 GPU를 제대로 달궈 보자는 마음이었다.

첫 단계는 이미지 폴더를 훑는 간단한 크롤러를 만드는 것이었다. Apple Photos를 쓰고 있어서 폴더가 따로 없었지만, 비밀 밈 단톡방에 쌓아 둔 방대한 밈 이미지가 있었다. 채팅을 내보내 폴더에 모으니 테스트 이미지 세트가 완성됐다.

### 크롤러

아마 세상에서 가장 조악한 크롤러일 거다. 정확히 말하면, Claude가 내 지시에 따라 만들어 준 작품이다.

조금 복잡해 보이지만 흐름은 이렇다.

1. 대상 디렉터리의 파일 목록을 가져온다.
2. 목록을 msgpack 파일에 저장한다.
3. msgpack을 읽어 이미지마다 SQLite 데이터베이스에 기록하면서 다음 메타데이터를 저장한다.
    - 해시
    - 파일 크기
    - 경로
4. SQLite 레코드를 하나씩 읽어 CLIP으로 벡터 임베딩을 추출한다.
5. 그 벡터를 다시 SQLite에 저장한다.
6. SQLite를 다시 순회하며 벡터와 이미지 경로를 ChromaDB에 삽입한다.
7. 끝.

사실 이건 불필요하게 단계가 많다. 이미지를 읽으면서 바로 임베딩을 만들어 ChromaDB에 넣어도 된다(ChromaDB는 간단하고 무료이며 별도 인프라가 필요 없다).

그럼에도 이렇게 짠 이유는 다음과 같다.

- 밈 이후로 14만 장이 넘는 이미지를 처리해야 했는데, 중간에 크래시가 나면 바로 이어서 실행할 수 있어야 했다.
- 정전이나 오류가 나더라도 쉽게 재개할 수 있어야 했다.
- 나는 반복 루프를 좋아한다.

복잡해 보여도 완벽하게 작동했다. 지금까지 20만 장 이상을 크롤링했는데 한 번도 문제없었다.

### 임베딩 시스템

이미지 인코딩 과정이 특히 재미있었다.

먼저 SigLIP으로 [간단한 웹 서비스](https://github.com/harperreed/imbedding)를 만들어 이미지를 업로드하면 벡터를 반환하도록 했다. 스튜디오의 GPU 서버에서 돌렸는데, 로컬에서 OpenCLIP을 돌릴 때보다 훨씬 빨랐다.

그래도 로컬에서 돌리고 싶었다. [ml-explore](https://github.com/ml-explore/) 레포를 떠올렸는데, 마침 [CLIP 구현](https://github.com/ml-explore/mlx-examples/tree/main/clip)이 있었다. 큰 모델을 돌려도 RTX 4090보다 빠르다니, 정말 놀라웠다.

### MLX_CLIP

Claude와 함께 Apple 예제 스크립트를 변형해 로컬에서 바로 쓸 수 있는 파이썬 클래스로 만들었다.

https://github.com/harperreed/mlx_clip

생각보다 잘 나왔다. 역시 Apple Silicon은 무척 빠르다.

사용법도 의외로 간단했다.

```python
import mlx_clip

# 모델 초기화
clip = mlx_clip.mlx_clip("openai/clip-vit-base-patch32")

# 이미지 임베딩
image_embeddings = clip.image_encoder("assets/cat.jpeg")
print(image_embeddings)

# 텍스트 임베딩
text_embeddings = clip.text_encoder("a photo of a cat")
print(text_embeddings)
```

SigLIP도 이렇게 돌리고 싶지만, 이번 프로젝트는 개념 증명(POC)에 가깝다. SigLIP을 MLX에서 돌리는 방법을 아시는 분은 연락 주시면(hmu, 연락 주세요) 감사하겠다 👉 [harper@modest.com](mailto:harper@modest.com). OpenCLIP을 새로 만들고 싶지는 않다—Apple Silicon에서도 잘 돌아갈 테니 말이다.

### Now what

이미지 벡터를 모두 벡터 데이터베이스(ChromaDB)에 넣었으니 이제 인터페이스를 만들 차례였다. 시작 이미지의 벡터를 가져와 ChromaDB에 질의하면, ChromaDB가 유사도 순으로 이미지 ID를 반환한다.

나는 이를 Tailwind와 Flask로 감싸 웹 인터페이스를 만들었다. 결과는 놀라웠다.

2015년에 이런 걸 만들려면 엄청난 시간을 들여야 했을 텐데, 이번에는 대략 10시간 정도로 끝났다.

결과는 말 그대로 마법 같았다.

### 밈 개념 검색

테스트 세트는 밈 1만 2천 장이다.

예를 들어 다음 이미지를 인코딩해 ChromaDB에 질의하면:

{{< image src="images/posts/vector-memes-bowie.png" caption="So true" >}}

비슷한 이미지가 이렇게 나온다:  
{{< image src="images/posts/vector-memes-bowie-results.png" >}}

또 다른 예시:  
{{< image src="images/posts/vector-memes-star-trek.png" >}}

결과:  
{{< image src="images/posts/vector-memes-star-trek-results.png" >}}

클릭하며 돌아다니는 재미가 쏠쏠하다.

### Namespaces?

이미지를 클릭해 비슷한 이미지를 찾는 것도 멋지지만, **같은 모델로 텍스트를 임베딩해 이미지와 매칭**할 때의 놀라움은 또 다르다. 텍스트와 이미지가 하나의 벡터 공간에서 만나는 느낌이랄까.

예시 몇 가지:

**money**  
{{< image src="images/posts/vector-memes-money.png" >}}

**AI**  
{{< image src="images/posts/vector-memes-ai.png" >}}

**red**(색상? 라이프스타일? 러시아?)  
{{< image src="images/posts/vector-memes-red.png" >}}

끝도 없이 탐색할 수 있다. 잊고 있던 보물 같은 이미지도 계속 발견된다. 예를 들어 “블로그 글쓰기” 밈을 찾고 싶다면:  
{{< image src="images/posts/vector-memes-writing-meme.jpg" >}}

(자기 인지 충분하지만 상관없다, lol.)

### 사진 라이브러리에서는?

결론부터 말하면 **아주 잘 된다**.

시도해 보고 싶다면 구글 포토 ‘Takeout’ 아카이브를 받아 외장 디스크에 풀어 두자. 중복 데이터가 많아 간단한 스크립트로 정리한 뒤, 스크립트의 대상 폴더를 밈 폴더 대신 그 디렉터리로 바꿔 주면 된다.

약 14만 장을 처리하는 데 6시간 정도 걸렸고, 결과는 훌륭했다.

#### 재미있는 예시

비슷한 사진은 당연히 묶이고(구글 포토의 중복 문제는 꽤 심각하다)  
{{< image src="images/posts/vector-memes-harper.png" >}}

우리 집엔 푸들이 많았다  
{{< image src="images/posts/vector-memes-poodles.png" >}}

랜드마크도 찾기 쉽다—비행기에서 찍은 후지산!  
{{< image src="images/posts/vector-memes-fuji-results.png" >}}

후지산과 비슷한 사진도 한눈에  
{{< image src="images/posts/vector-memes-fuji-similar.png" >}}

도시 검색: 시카고  
{{< image src="images/posts/vector-memes-chicago.png" >}}

감정 검색: ‘surprised’  
{{< image src="images/posts/vector-memes-surprised.png" >}}

조금 특이한 주제 ‘low rider’(시부야 컷)  
{{< image src="images/posts/vector-memes-low-riders.png" >}}

‘bokeh’처럼 텍스트로 찾기 어려운 것도 문제없다.  
{{< image src="images/posts/vector-memes-bokeh.png" >}}

덕분에 잊고 있던 멋진 사진을 다시 발견했다. 예를 들어 2017년에 찍은 Baratunde:  
{{< image src="images/posts/vector-memes-baratunde.png" >}}

### 이 기술은 곧 어디에나 쓰일 것

조만간 모든 사진 앱에 이런 기능이 들어갈 거라고 본다. 구글 포토에는 이미 있을지도 모르지만, 구글식 UI에 묻혀 잘 안 보이는 것 같다.

사진이나 이미지를 다루는 서비스가 있다면, 당장 파이프라인을 구축해 임베딩을 추출해 보라. 어떤 흥미로운 기능이 열릴지 모른다.

## 무료로 사용해 보세요

소스 코드: [harperreed/photo-similarity-search](https://github.com/harperreed/photo-similarity-search)

설치 방법은 비교적 단순하지만 다소 즉흥적이므로 conda 같은 가상 환경을 권장한다. 인터페이스는 Tailwind, 웹 서버는 Flask, 코드는 Python, 호스트는 Harper Reed다.

## 당신에게 주는 도전 과제!

내 사진 라이브러리를 깔끔하게 정리해 줄 간단한 Mac 네이티브 앱을 만들어 달라! 다른 곳으로 업로드하지 않고 완전히 로컬에서 동작했으면 좋겠다. 라이브러리 위치만 지정하고 “크롤링 시작” 버튼을 누르면 끝나는 그런 앱 말이다.

추가하면 좋을 기능:

- Llava/Moondream 자동 캡션
- 키워드·태그 생성
- 벡터 유사도 검색
- 기타 재미있는 아이디어

Lightroom·Capture One·Apple Photos 플러그인이어도 좋다. 정말 갖고 싶다. 만들어 주시길!

## 보너스: Lightroom 프리뷰 JPEG 복구

해킹 친구 Ivan도 이 프로젝트를 보자마자 바로 써 보고 싶어 했다. 그의 사진 카탈로그는 외장 하드에 있었지만 Lightroom 프리뷰 캐시 파일은 로컬에 있었다.

Ivan은 프리뷰 파일에서 썸네일과 메타데이터를 추출해 외장 디스크에 저장하는 간단한 스크립트를 작성했다. 그리고 이미지 벡터 크롤러를 돌리니 비슷한 사진 검색이 완벽하게 작동했다.

#### Lightroom 썸네일 복구

만약 원본 사진 라이브러리를 잃었는데 lrpreview 파일만 남았다면, 이 스크립트로 저해상도 이미지만이라도 건질 수 있다. 꽤 유용하니 기억해 두자.

[LR Preview JPEG Extractor](https://github.com/ibips/lrprev-extract)

## Thanks for reading.

언제든지 연락 주세요(hmu) 👉 [harper@modest.com](mailto:harper@modest.com). 요즘 AI, 이커머스, 사진, 하이파이, 해킹 같은 것에 푹 빠져 있다.

시카고에 계시다면 만나서 이야기해요.
