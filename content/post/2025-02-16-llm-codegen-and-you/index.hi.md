---
bsky: https://bsky.app/profile/harper.lol/post/3lidixzdr5j2e
date: 2025-02-16 18:00:00-05:00
description: सॉफ्टवेयर बनाने के लिए LLMs का उपयोग करने की मेरी वर्तमान कार्यप्रणाली
  का विस्तृत विवरण, ब्रेनस्टॉर्मिंग से लेकर योजना और निष्पादन तक।
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
title: मेरी मौजूदा LLM कोडजन कार्यप्रणाली
translationKey: My LLM codegen workflow atm
---

_tl;dr; पहले स्पेक पर गहन ब्रेनस्टॉर्म करें, फिर ठोस योजना बनाएं, फिर LLM-आधारित कोड-जनरेशन से उसे अमल में लाएं। पृथक लूप, फिर जादू. ✩₊˚.⋆☾⋆⁺₊✧_

मैंने LLM की मदद से ढेर सारे छोटे-छोटे प्रोडक्ट बनाए हैं—मज़ेदार भी रहे और उपयोगी भी। लेकिन कुछ गड्ढे ऐसे हैं जहाँ काफी समय डूब सकता है। कुछ समय पहले एक दोस्त ने पूछा कि मैं LLM से सॉफ़्टवेयर कैसे लिखवा रहा हूँ। मैंने सोचा, “अरे, तुम्हारे पास कितना वक़्त है!” और इसी तरह यह पोस्ट बनी।

(p.s. अगर आप AI-हेटर हैं तो अंत तक स्क्रोल कर लें।)

मैंने कई डेवलपर दोस्तों से बात की और पाया कि तरीक़ा लगभग एक-सा है, बस हल्के-फुल्के बदलाव होते रहते हैं।

यह है मेरा वर्कफ़्लो—मेरे अपने अनुभव, दोस्तों की बातचीत (धन्यवाद [Nikete](https://www.nikete.com/), [Kanno](https://nocruft.com/), [Obra](https://fsck.com/), [Kris](https://github.com/KristopherKubicki) और [Erik](https://thinks.lol/)) तथा इंटरनेट की कुख्यात [bad](https://news.ycombinator.com/) [places](https://twitter.com) पर साझा की गई बेस्ट प्रैक्टिस का निचोड़।

यह तरीक़ा **अभी** बढ़िया चल रहा है; दो हफ्ते में फेल भी हो सकता है या दोगुना तेज़। ¯\\\_(ツ)\_/¯

## चलिए शुरू करें

{{< image src="llm-coding-robot.webp" alt="Juggalo Robot" caption="AI-जनित चित्र अक्सर अविश्वसनीय-से लगते हैं। मेरे जग्गालो कोडिंग-रोबोट एंजल को नमस्ते कहें!" >}}

डेवलपमेंट के कई रास्ते हैं, पर मेरे लिए आमतौर पर दो ही स्थितियाँ होती हैं:

- ग्रीनफ़ील्ड कोड
- विरासती-पर-आधुनिक (Legacy-Modern) कोडबेस

दोनों के लिए मेरा क्रम नीचे है।

## ग्रीनफ़ील्ड

ग्रीनफ़ील्ड विकास के लिए यह प्रक्रिया बेहतरीन काम करती है। इससे सुदृढ़ योजना व प्रलेखन मिलता है, और छोटे-छोटे चरणों में कार्यान्वयन आसान रहता है।

{{< image src="greenfield.jpg" alt="Green field" caption="दाएँ तरफ सचमुच हरा मैदान है। Leica Q, 14/05/2016" >}}

### चरण 1 : विचार तराशना

संवादी LLM (मैं ChatGPT 4o / o3 का उपयोग करता हूँ) से विचार को निखारें:

```prompt
Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s the idea:

<IDEA>
```

ब्रेनस्टॉर्म के प्राकृतिक समापन पर:

```prompt
Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
```

इससे एक ठोस और सरल स्पेक तैयार होगा; इसे रिपो में `spec.md` नाम से सहेज लें।

> इस स्पेक का कई तरह से इस्तेमाल हो सकता है। हम यहाँ कोड-जनरेशन कर रहे हैं, पर मैंने इसी से आइडिया में खामियाँ ढूँढीं, वाइट-पेपर लिखवाया, बिज़नेस-मॉडल बनवाया, या गहन शोध कर के 10 हज़ार शब्द का सहायक डॉक्यूमेंट तैयार कराया है।

### चरण 2 : योजना बनाना

स्पेक को किसी सक्षम रीजनिंग मॉडल (`o1*`, `o3*`, `r1`) को दें:

(TDD वाला प्रॉम्प्ट)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

(नॉन-TDD प्रॉम्प्ट)

```prompt
Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. review the results and make sure that the steps are small enough to be implemented safely, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step. Prioritize best practices, and incremental progress, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

<SPEC>
```

आउटपुट में एक प्रॉम्प्ट-प्लान मिलेगा; उसे `prompt_plan.md` में सहेजें।

इसके बाद पूछें:

```prompt
Can you make a `todo.md` that I can use as a checklist? Be thorough.
```

`todo.md` तैयार हो जाएगा, जिसे आपका कोड-जनरेशन टूल प्रक्रिया के दौरान बिंदुवार टिक करता रहेगा।

#### Yay, योजना बन गयी!

अब आपके पास पक्की योजना और प्रलेखन है, जिससे प्रोजेक्ट बनाना आसान होगा। यह पूरा काम **लगभग 15 मिनट** लेता है—वाकई जंगली रफ़्तार!

### चरण 3 : कार्यान्वयन

उपलब्ध साधन कई हैं; सफलता काफ़ी हद तक चरण 2 की गुणवत्ता पर निर्भर है।

मैंने इस वर्कफ़्लो को [GitHub Workspace](https://githubnext.com/projects/copilot-workspace), [Aider](https://aider.chat/), [Cursor](https://www.cursor.com/), [Claude Engineer](https://github.com/Doriandarko/claude-engineer), [sweep.dev](https://sweep.dev/), [ChatGPT](https://chatgpt.com), [Claude.ai](https://claude.ai) आदि के साथ आज़माया है; सबमें ठीक चलता है। मुझे **सादा** Claude और Aider ज़्यादा पसंद आते हैं।

### Claude

मैं [Claude.ai](https://claude.ai) के साथ पेयर-प्रोग्राम करता हूँ—प्रत्येक प्रॉम्प्ट क्रमवार भेजता हूँ। आगे-पीछे का यह संवाद कभी-कभी झुँझलाता है, पर परिणाम अच्छे मिलते हैं।

शुरुआती बायलरप्लेट और टूलिंग मैं स्वयं सेट-अप करता हूँ ताकि चाही गई भाषा, शैली और उपकरण सुनिश्चित रहें—Claude अक्सर React का कोड दे देता है, इसलिए ठोस आधार ज़रूरी है।

यदि कहीं अटकूँ, तो [repomix](https://github.com/yamadashy/repomix) से पूरा कोडबेस Claude को भेज कर डिबग करा लेता हूँ।

वर्कफ़्लो:

- रिपो तैयार करना (बायलरप्लेट, `uv init`, `cargo init`, आदि)
- Claude में प्रॉम्प्ट पेस्ट करना
- Claude से मिला कोड IDE में डालना
- कोड चलाना, परीक्षण चलाना
- …
- सब ठीक तो अगला प्रॉम्प्ट
- समस्या हो तो repomix से डिबग
- यही क्रम दोहराते जाएँ ✩₊˚.⋆☾⋆⁺₊✧

### Aider

[Aider](https://aider.chat/) थोड़ा अनोखा है, पर चरण 2 के आउटपुट पर अद्भुत ढंग से फिट बैठता है।

वर्कफ़्लो लगभग वही है; बस Claude की जगह Aider में प्रॉम्प्ट डालते हैं।

Aider “बस कर देता है” और मैं [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/) पर क्लिक कर लेता हूँ।

> Aider अपने [LLM लीडरबोर्ड](https://aider.chat/docs/leaderboards/) पर नए मॉडल की बेंचमार्किंग करता है—नए मॉडल कितने असरदार हैं, देखने का बढ़िया स्रोत।

परीक्षण के मामले में Aider ख़ासा सहायक है, क्योंकि वह परीक्षण स्वतः चलाकर त्रुटियाँ सुधार लेता है।

वर्कफ़्लो:

- रिपो तैयार करना (बायलरप्लेट, `uv init`, `cargo init`, आदि)
- Aider चालू करना
- प्रॉम्प्ट Aider में पेस्ट करना
- Aider का करतब देखना ♪┏(・o･)┛♪
- परीक्षण चलाना या एप चलाकर जाँचना
- सब ठीक तो अगला प्रॉम्प्ट
- त्रुटि हो तो प्रश्न-उत्तर कर के सुधारना
- क्रम दोहराना ✩₊˚.⋆☾⋆⁺₊✧

### नतीजे

इस वर्कफ़्लो से मैंने ढेरों चीज़ें बनाईं—स्क्रिप्ट, Expo ऐप, Rust CLI टूल आदि। अलग-अलग भाषाओं व संदर्भों में भी काम आया। मुझे यह तरीका सच-मुच पसंद है।

अगर कोई छोटा या बड़ा प्रोजेक्ट टाल रखा है, तो इसे आज़मा कर देखिए—कम समय में जितना आगे बढ़ेंगे, देखकर चकित रह जाएँगे।

मेरी हैक TODO-लिस्ट खाली है—जो भी सूझा, बना डाला। पहली बार वर्षों बाद मैं नई भाषाएँ और उपकरण आजमा रहा हूँ; मेरा प्रोग्रामिंग दृष्टिकोण फैल रहा है।

## नॉन-ग्रीनफ़ील्ड: क्रमिक इटेरेशन

कभी-कभी ग्रीनफ़ील्ड नहीं, बल्कि पहले से मौजूद कोडबेस में सुधार करना होता है।

{{< image src="brownfield.jpg" alt="a brown field" caption="यह ‘ग्रीनफ़ील्ड’ तो बिल्कुल नहीं—पक्की ‘ब्राउनफ़ील्ड’ है। दादाजी के कैमरे से, कहीं युगांडा (60s)" >}}

यहाँ तरीका थोड़ा अलग है—पूरे प्रोजेक्ट की बजाय हर कार्य के लिए अलग योजना बनती है।

### कॉन्टेक्स्ट जुटाना

AI-डेव करने वालों के पास अलग-अलग उपकरण होंगे, पर किसी तरह स्रोत कोड समेट कर LLM में सटीक रूप से देना ज़रूरी है।

मैं अभी [repomix](https://github.com/yamadashy/repomix) का उपयोग करता हूँ। मेरी ग्लोबल `~/.config/mise/config.toml` में LLM-टास्कों की यह सूची है:

```shell
LLM:clean_bundles           Generate LLM bundle output file using repomix
LLM:copy_buffer_bundle      Copy generated LLM bundle from output.txt to system clipboard for external use
LLM:generate_code_review    Generate code review output from repository content stored in output.txt using LLM generation
LLM:generate_github_issues  Generate GitHub issues from repository content stored in output.txt using LLM generation
LLM:generate_issue_prompts  Generate issue prompts from repository content stored in output.txt using LLM generation
LLM:generate_missing_tests  Generate missing tests for code in repository content stored in output.txt using LLM generation
LLM:generate_readme         Generate README.md from repository content stored in output.txt using LLM generation
```

`output.txt` में पूरा कॉन्टेक्स्ट आ जाता है। यदि टोकन अधिक खर्च हो रहे हों, तो अनावश्यक फ़ाइलें-फोल्डर अनदेखा कर देता हूँ।

> `mise` की खासियत है कि इन्हीं टास्क को कार्य-डायरेक्ट्री की `.mise.toml` में ओवरराइड किया जा सकता है। चाहे कोई और टूल प्रयोग करें, बस `output.txt` बन जाए तो बाकी LLM-टास्क चलेंगे। अलग-अलग कोडबेस में यह बहुत सहायक है।

`output.txt` बनने के बाद मैं उसे [LLM](https://github.com/simonw/LLM) कमांड में पाइप कर विभिन्न रूपांतरण कराता हूँ और Markdown फाइलें बना लेता हूँ—जैसे  
`cat output.txt | LLM -t readme-gen > README.md` या  
`cat output.txt | LLM -m claude-3.5-sonnet -t code-review-gen > code-review.md`

मान लीजिए मुझे परीक्षण कवरेज सुधारना है—

#### Claude

- उस डायरेक्ट्री में जाएँ जहाँ कोड है  
- `mise run LLM:generate_missing_tests` चलाएँ  
- बने हुए `missing-tests.md` को देखें  
- `mise run LLM:copy_buffer_bundle` से पूरा कॉन्टेक्स्ट क्लिपबोर्ड में लें  
- उसे Claude में पेस्ट करें, साथ में पहला “missing test” इश्यू  
- Claude का कोड IDE में डालें  
- …  
- परीक्षण चलाएँ  
- यही क्रम दोहराएँ ✩₊˚.⋆☾⋆⁺₊✧

#### Aider

- कोड वाली डायरेक्ट्री में नई ब्रांच बनाएँ  
- Aider चलाएँ  
- `mise run LLM:generate_missing_tests`  
- `missing-tests.md` खोलें  
- पहला इश्यू Aider में पेस्ट करें  
- Aider का करतब देखें ♪┏(・o･)┛♪  
- …  
- परीक्षण चलाएँ  
- क्रम दोहराएँ ✩₊˚.⋆☾⋆⁺₊✧

बड़े कोडबेस में धीरे-धीरे मजबूती लाने का यह शानदार रास्ता है; किसी भी आकार के कार्य निपट जाते हैं।

### प्रॉम्प्ट-जादू

ये त्वरित हैक प्रोजेक्ट को गहराई से टटोलने में जबरदस्त असरदार हैं। यह बहुत तेज़ और असरदार है।

#### Code review

```prompt
You are a senior developer. Your job is to do a thorough code review of this code. You should write it up and output markdown. Include line numbers, and contextual info. Your code review will be passed to another teammate, so be thorough. Think deeply  before writing the code review. Review every part, and don't hallucinate.
```

#### GitHub Issue generation

_(मुझे असली इश्यू पोस्ट करना अभी ऑटोमेट करना है!)_

```prompt
You are a senior developer. Your job is to review this code, and write out the top issues that you see with the code. It could be bugs, design choices, or code cleanliness issues. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

#### Missing tests

```prompt
You are a senior developer. Your job is to review this code, and write out a list of missing test cases, and code tests that should exist. You should be specific, and be very good. Do Not Hallucinate. Think quietly to yourself, then act - write the issues. The issues will be given to a developer to executed on, so they should be in a format that is compatible with github issues
```

ये प्रॉम्प्ट अब थोड़े “बूमर” हो चुके हैं—अगर आपके पास इन्हें बेहतर बनाने का विचार हो तो बताइए।

## Skiing ᨒ↟ 𖠰ᨒ↟ 𖠰

मैं अकसर कहता हूँ, “जो हो रहा है उस पर पैनी नज़र रखें, वर्ना पल-भर में अपने ही ‘स्की’ से आगे निकल जाएँगे।”

पता नहीं क्यों LLM की बात आते ही “over my skis” मुँह से निकल जाता है—शुरू में सब कुछ मुलायम पाउडर-स्की जैसा लगता है और फिर अचानक “WHAT THE FUCK IS GOING ON!” कहते हुए खाई में गिरने-सा एहसास।

ऊपर वाला **योजना-चरण** चीज़ें काबू में रखता है; कम से कम एक दस्तावेज़ रहता है जिसे दोबारा जाँच सकते हैं। परीक्षण भी मददगार हैं—विशेषकर Aider वाली वाइल्ड स्टाइल में।

फिर भी कभी-कभी **over my skis** हो ही जाता हूँ; छोटा-सा ब्रेक या टहलना मदद करता है। मूलतः वही समस्या-समाधान की प्रक्रिया है, बस रफ़्तार ब्रेकनेक।

> हम अकसर LLM से अपने साधारण-से कोड में भी अजीब चीजें जोड़ने को कह देते हैं—जैसे lore फ़ाइल बना दो और UI में उसका ज़िक्र कर दो, वह भी Python CLI में! आसमान ही सीमा है।

## I am so lonely (｡•́︿•̀｡)

इन वर्कफ़्लो का सबसे बड़ा रोना यह है कि ये लगभग _सिंगल-प्लेयर मोड_ हैं।

मैंने अकेले, जोड़ी में और टीम के साथ—तीनों तरह से कोड किया है; लोगों के साथ हमेशा बेहतर लगता है। इन वर्कफ़्लो को टीम में अपनाना मुश्किल है—बॉट टकराते हैं, मर्ज़ डरावने, कॉन्टेक्स्ट भारी।

काश कोई इसे मल्टी-प्लेयर बना दे—सोलो हैकर अनुभव नहीं, बल्कि टीम-गेम! मौका बड़ा है—काम पर लगिए!

## ⴵ Time ⴵ

इस कोड-जनरेशन ने मेरी व्यक्तिगत उत्पादकता आसमान पर पहुँचा दी है, पर एक अजीब साइड-इफेक्ट है—LLM के टोकन जलने तक “खाली” समय बहुत मिलता है।

{{< image src="apple-print-shop-printing.png" alt="Printing" caption="यह दृश्य जैसे कल ही देखा हो" >}}

इंतज़ार का समय खाने के लिए मैंने कुछ आदतें डाल ली हैं—

- किसी और प्रोजेक्ट की ब्रेनस्टॉर्मिंग शुरू कर देता हूँ  
- रिकॉर्ड सुनता हूँ  
- [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/) खेलता हूँ  
- दोस्तों और बॉटों से बात करता हूँ  

ऐसे Hack Hack Hack करने में बड़ा मज़ा है। शायद पहले कभी इतना उत्पादक नहीं रहा।

## Haterade ╭∩╮( •̀\_•́ )╭∩╮

कई दोस्त कहते हैं, “LLM हर चीज़ में फेल है।” यह नज़रिया मुझे बुरा नहीं लगता—मैं सहमत नहीं, पर शक ज़रूरी है। AI से नफ़रत करने के तमाम कारण हैं। मेरी सबसे बड़ी चिंता बिजली की खपत और पर्यावरणीय असर है। पर… कोड तो बहना ही है, है ना? *साँस*।

यदि आप सीखने को खुले हैं पर “साइबॉर्ग प्रोग्रामर” नहीं बनना चाहते, तो Ethan Mollick की किताब पढ़ें: [**Co-Intelligence: Living and Working with AI**](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/)

यह फ़ायदों को बिना टेक-अर्नाचो-कैपिटलिस्ट शोरगुल के समझाती है। मुझे बहुत काम की लगी और जिन दोस्तों ने पढ़ी, उनसे संतुलित बातचीत हुई। सिफ़ारिश है।

यदि आप संदेह में हैं पर थोड़े जिज्ञासु भी—तो मुझसे बात करें; यह पागलपन दिखाऊँ और शायद मिलकर कुछ बना लें।

_thanks to [Derek](https://derek.broox.com), [Kanno](https://nocruft.com/), [Obra](https://fsck.com), and [Erik](https://thinks.lol/) for taking a look at this post and suggesting edits. I appreciate it._