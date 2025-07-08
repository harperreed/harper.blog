---
bsky: https://bsky.app/profile/harper.lol/post/3loo3lnbmbi22
date: 2025-05-08
description: सॉफ़्टवेयर विकास के लिए क्लॉड कोड एआई सहायक के उपयोग पर विस्तृत मार्गदर्शन,
  जिसमें कार्यप्रवाह सुझाव, परीक्षण अभ्यास और वास्तविक परियोजनाओं से व्यावहारिक उदाहरण
  शामिल हैं। इसमें रक्षात्मक कोडिंग रणनीतियाँ, TDD और टीम कार्यान्वयन भी सम्मिलित
  हैं।
draft: false
generateSocialImage: true
slug: basic-claude-code
tags:
- ai
- coding
- claude
- development
- automation
- testing
- tdd
- programming
title: 'मौलिक क्लॉड कोड

  description: सॉफ़्टवेयर विकास के लिए क्लॉड कोड एआई सहायक के उपयोग पर विस्तृत मार्गदर्शन,
  जिसमें कार्यप्रवाह सुझाव, परीक्षण अभ्यास और वास्तविक परियोजनाओं से व्यावहारिक उदाहरण
  शामिल हैं। इसमें रक्षात्मक कोडिंग रणनीतियाँ, TDD और टीम कार्यान्वयन भी सम्मिलित
  हैं।'
translationKey: Basic Claude Code
---

मुझे यह ‘एजेंटिक कोडिंग’ वाक़ई बहुत पसंद है; यह कई मायनों में जबर्दस्त है।  

जब से मैंने [वह मूल ब्लॉग-पोस्ट](/2025/02/16/my-llm-codegen-workflow-atm/) लिखी, Claude-लैंड में बहुत कुछ बदल चुका है:

- Claude Code  
- MCP  
- वगैरह  

अब तक मुझे सैकड़ों (वॉट?!) ई-मेल मिले हैं जिनमें लोगों ने अपना workflow बताया और यह भी कि मेरी तरकीब अपना कर उन्होंने कैसे बढ़त पाई। मैं कुछ कॉन्फ़्रेंसों में बोल चुका हूँ और codegen पर कुछ क्लासें भी पढ़ा चुका हूँ। मज़ेदार बात—कंप्यूटर बार-बार codegen को codeine समझ बैठता है; किसे पता था!

{{< image src="codegen.png"  >}}

चंद रोज़ पहले मैं [एक दोस्त](https://www.elidedbranches.com/) से बात कर रहा था कि हम सबकी तो **वाट लग चुकी है** और **AI हमारी नौकरियाँ ले उड़ेगा** (इस पर अलग पोस्ट में लिखूँगा)। वह बोली, “तुम Claude Code पर ही एक पोस्ट ठोंक दो।”

तो लीजिए, पेश है।

Claude Code मेरी मूल workflow-पोस्ट के सिर्फ़ आठ दिन बाद रिलीज़ हुआ और, जैसा मैंने अंदाज़ा लगाया था, उसने उस पोस्ट का अच्छा-खासा हिस्सा बेकार कर दिया। तब से मैं Aider छोड़कर Claude Code पर आ चुका हूँ और पीछे मुड़कर नहीं देखा। Aider अब भी अपना अलग काम आता है, पर फिलहाल Claude Code ज़्यादा काम का साबित हो रहा है।

Claude Code ताक़तवर है—और बेहिसाब महँगा भी।

मेरा workflow अब भी तक़रीबन वही है:

- आइडिया तराशने के लिए पहले `gpt-4o` से चैट करता हूँ।  
- उसके बाद सबसे बढ़िया reasoning-मॉडल (इन दिनों o1-pro या o3) से spec बनवाता हूँ। (o1-pro वाक़ई o3 से बेहतर है या मुझे बस इसलिए लगता है कि वह ज़्यादा वक़्त लेता है?)  
- उसी मॉडल से prompts भी जनरेट करवाता हूँ। LLM से prompt बनवाना एक खूबसूरत हैक है—बूमर लोग भड़क उठते हैं।  
- `spec.md` और `prompt_plan.md` प्रोजेक्ट की root में डाल देता हूँ।  
- फिर Claude Code को यह लिखता हूँ:

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

- इस prompt का जादू यह है कि यह `prompt_plan.md` पढ़कर जो काम अभी पूरे नहीं हुए उन्हें ढूँढता है, अगला बचा काम उठाता है, उस पर कोड लिखता है, सारे टेस्ट चलाता है, Git में साफ़-सुथरा कमिट करता है, `prompt_plan.md` में उसे “completed” कर देता है और फिर रुककर पूछता है—“आगे बढ़ूँ?” 🤌  
- मैं बस ‘yes’ टाइप करता हूँ और आराम से बैठ जाता हूँ; Claude अपना काम करता रहता है।  
- बाक़ी समय मैं ‘Cookie Clicker’ (एक idle-गेम) पर क्लिक करता रहता हूँ।  

यह तरीका धुआँधार चलता है। अपने प्रोसेस में कुछ और “सुपर-पावर” डाल दें तो नतीजे और भी आगे निकल जाते हैं।

## Defensive coding!

### Testing

Testing और टेस्ट-ड्रिवन डेवलपमेंट अनिवार्य हैं—इन्हें गले लगाइए।

कभी मैं TDD-हेटर था; लगता था यह टाइम-वेस्ट है। मैं गलत था—LOL। हम सालों तक प्रोजेक्ट के Core खत्म होने के बाद टेस्ट जोड़ते रहे; इंसानों के लिए यह ठीक चलता था।

**THIS IS BAD FOR ROBOTS.**

रोबोट TDD के दीवाने हैं—सचमुच निगल जाते हैं।

पहले रोबोट-मित्र से टेस्ट और mock लिखवाइए; अगली prompt में mock को असली कोड से भरिये। hallucination और LLM-scope drift पर यह अब तक की सबसे असरदार चाबी है—रोबोट पटरी पर बने रहते हैं।

### Linting

मैं लिंटिंग का क्रेज़ी फ़ैन हूँ। Ruff शानदार है, Biome बढ़िया है, Clippy मज़ेदार (और नाम भी धाँसू) है।

रोबोटों को बढ़िया linter चलाना बेहद भाता है।

लगातार lint चलाने से ढेरों बग दूर रहते हैं, कोड पढ़ने-लायक और मेंटेन करने-लायक बनता है। ऊपर से अच्छा formatter जोड़ दें तो सबकुछ चकाचक।

### Pre-commit hooks

असल जादू तब होता है जब इन सबको pre-commit hook में बाँध दें। `pre-commit` पायथन पैकेज लगाइए (`uv tools install pre-commit`), फिर एक `.pre-commit-config.yaml` बना दीजिए—हर कमिट की कोशिश पर ये सारे शानदार टेस्ट, टाइप-चेक और लिंटर फिर से चलेंगे ताकि आपका कोड ‘A+++’ ग्रेड पर दोबारा पास हो सके।

Claude Code के साथ यह ख़ास काम आता है। रोबोट कमिट करने को उतावला रहता है; आप कहेंगे तो वह जंगली बदलाव करेगा, कमिट करेगा, सब तोड़ देगा और फिर खुद ही फिक्स करेगा।

इससे GitHub Actions बेवजह फेल नहीं होते; गड़बड़ियाँ लोकल में ही पकड़ी जाती हैं।

> मज़ेदार बात: Claude ज़िंदगी में भी `uv` को सही से नहीं समझ पाता। अगर ध्यान न दिया तो हर जगह शिट फैलाकर `pip install` कर देगा। और अगर आप उसे `uv` यूज़ करने कहें तो वह बस `uv pip install ...` लिख देता है। लगता है जून में AGI शायद नहीं आने वाला—so sad.

### CLAUDE.md और commands

ये दोनों छोटे-से जोड़ बहुत रस निचोड़ लेते हैं।

{{< image src="_SDI8149.jpg" alt="Jesse at the studio, Sept 15, 2023, Ricoh GRiii" caption="Jesse at the studio, Sigma fp, 11/15/2023" >}}

मैंने दोस्त [Jesse Vincent](https://fsck.com/) से एक [CLAUDE.md](https://github.com/harperreed/dotfiles/blob/master/.claude/CLAUDE.md) चुरा ली, जिसे उसने [खूब जतन से तगड़ा बनाया](https://github.com/obra/dotfiles/blob/main/.claude/CLAUDE.md)। इसमें शामिल है:

- Big Daddy Rule का हल्का वर्ज़न  
- TDD करने के साफ़ निर्देश  
- मेरी मनपसंद कोड-स्टाइल की गाइड  

> [@clint](https://instagram.com/clintecker) ने अपनी CLAUDE.md में खुद को “MR BEEF” बुलवाया, तो अब हमारी हर डॉक्यूमेंटेशन में लाइन आ जाती है—“If you're stuck, stop and ask for help—MR BEEF may know best.” यह लिखते-लिखते मैंने भी फ़ाइल में खुद को “Harp Dog” बुलवाना जोड़ दिया। फीचर है, बग नहीं।

Commands भी कमाल के होते हैं। मेरे कुछ कमांड आप [मेरी dotfiles](https://github.com/harperreed/dotfiles/tree/master/.claude/commands) में देख सकते हैं।

{{< image src="commands.png"  >}}

पहले मैं commands बहुत चलाता था, पर ये बार-बार इस्तेमाल होने वाले prompts को रॉकेट-स्पीड दे देते हैं। आप कमांड को आर्ग्युमेंट भी दे सकते हैं। मसलन GitHub issue वाले कमांड में issue-नंबर पास करें:  
`/user:gh-issue #45`

Claude अब `gh-issue.md` में लिखी “prompt” स्क्रिप्ट चला देगा।

इन्हें आप किसी प्रोजेक्ट डायरेक्टरी में भी रख सकते हैं और उसी प्रोजेक्ट के लिए अलग CLAUDE.md बना सकते हैं—चाहे वह hugo हो, rust, go या javascript।

## "Continue"

{{< image src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDk3ZTZpdWYwdG5sdmpnaTJqNzJhYXlvcmp6bnNmdmhxaGdoeHJ4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Je3fIeeXyYEM85G/giphy.gif" >}}

कभी-कभी मैं उस पंछी जैसा महसूस करता हूँ जिसे Homer ने ‘y’ दबाने को बिठा दिया था—बस “continue” लिखो या वही prompt फिर से टपका दो।

अकसर प्लान आठ-बारह स्टेप के होते हैं। कोई भी बिलकुल नई (greenfield) development योजना, भाषा चाहे जो हो, मैं 30-45 मिनट में निपटा लेता हूँ।

मैं दोस्त Bob से बात कर रहा था; उसे यक़ीन नहीं हुआ। मैंने कहा, “कुछ भी बनाने को बोलो, किस भाषा में—चलो देखते हैं!”

{{< image src="R0000693.jpeg" caption="Bob Swartz, Ricoh GRiiix, 11/17/2024" >}}

वह बोला, “ठीक है—C में एक BASIC interpreter।”

यह आदर्श नहीं था; मुझे C नहीं आती, न interpreter लिखने का खास शौक। पर **अबे, छोड़ यार—कर डालते हैं**।

ऊपर वाले स्टेप्स फॉलो किए और Claude Code ने धमाल कर दिया। हमारे पास [एक चलने-लायक BASIC interpreter](https://github.com/harperreed/basic) है। पहला वर्ज़न घंटे-भर में बन गया; मैंने कुछ घंटे और घिसाई की तो और सँवर गया। क्या इसे 1982 में शिप करता? शायद नहीं। [prompt_plan यहाँ देखें](https://raw.githubusercontent.com/harperreed/basic/refs/heads/main/docs/prompt_plan.md)।

## The Team

हमारी पूरी टीम इस वक्त Claude Code इस्तेमाल कर रही है। सब मोटे-तौर पर वही प्रोसेस फॉलो करते हैं, अपनी-अपनी छोटी tweaks के साथ।

इतनी test coverage हमने पहले कभी नहीं रखी थी। कोड बेहतर है, और उतना ही असरदार जितना हमारा पुराना घटिया कोड था। मज़ा आता है जब किसी की स्क्रीन पर झाँकता हूँ—ghostty हो, VS Code टर्मिनल, Zed टर्मिनल या python notebooks—हर जगह Claude Code भाग रहा है।

{{< image src="dril.jpg" >}}

अगर किसी के पास ढेर सारे टोकन हों तो ज़रा मेरा बजट बना दो; मेरा परिवार मर रहा है।

## thanks

सभी दोस्तों का शुक्रिया जो लगातार ई-मेल भेजते रहते हैं—आपके workflows और प्रोजेक्ट्स के बारे में पढ़ना मज़ेदार है। भेजते रहिए!