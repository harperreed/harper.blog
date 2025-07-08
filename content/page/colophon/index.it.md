---
description: Colophon per harper.blog
hideReply: true
menu:
  footer:
    name: Colophon
    weight: 3
nofeed: true
slug: colophon
title: Colophon
translationKey: colophon
type: special
url: colophon
weight: 6
---

Questo sito, [harper.blog](https://harper.blog), è il blog personale di Harper Reed. È realizzato con tecnologie web moderne e tecniche di static site generation.

## Stack tecnologico

- **Static Site Generator**: [Hugo](https://gohugo.io/)
- **Hosting**: [Netlify](https://www.netlify.com/)
- **Version Control**: Git (hosted on GitHub)

## Design e layout

- Il sito utilizza un tema personalizzato basato su [Bear Cub](https://github.com/clente/hugo-bearcub) ᕦʕ •ᴥ•ʔᕤ
- ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•!
- Tipografia: si utilizzano font di sistema per garantire prestazioni ottimali e un aspetto nativo
- Il design responsive assicura compatibilità sui diversi dispositivi e dimensioni di schermo

## Gestione contenuti

- I contenuti sono scritti in Markdown

## Build e deployment

- Il Continuous Deployment è gestito tramite Netlify
- Il sito viene generato e distribuito automaticamente quando le modifiche vengono pushate sul branch principale (main)
- I comandi di build personalizzati e le relative impostazioni sono definiti in `netlify.toml`

## Ottimizzazioni delle prestazioni

- Le immagini sono ottimizzate e servite in formato WebP quando possibile
- Il CSS viene minificato per le build di produzione
- Si utilizza la pipeline integrata di Hugo per l’ottimizzazione degli asset

## Funzionalità aggiuntive

- È disponibile un feed RSS per la sindacazione dei contenuti
- Sono presenti meta tag per i social media per una condivisione ottimale su piattaforme come Twitter e Facebook
- Si impiegano shortcode personalizzati (shortcodes) per arricchire la formattazione dei contenuti (ad esempio l’integrazione con Kit.co)

## Strumenti di sviluppo

- Il `Makefile` semplifica le attività di sviluppo più frequenti
- Il progetto utilizza moduli Go per la gestione delle dipendenze

## Accessibilità e standard

- Il sito punta a essere accessibile e a rispettare gli standard web moderni
- Viene impiegato HTML semantico in tutto il sito

## Analytics

- Il sito usa [tinylytics](https://tinylytics.app/) per tracciare diverse metriche e visite (“bits and hits”). I risultati sono visibili [qui](https://tinylytics.app/public/cw1YY9KSGSE4XkEeXej7).
- Questo sito ha ricevuto {{< ta_hits >}} visite dai seguenti paesi: {{< ta_countries >}}.

## Autore e manutenzione

Il sito è mantenuto da Harper Reed. Per domande, contatta [harper@modest.com](mailto:harper@modest.com).

Ultimo aggiornamento: Settembre 2024

## Changelog

Ecco il log dei commit Git per questa iterazione:

{{< readfile file="gitlog.md" markdown="true" >}}

---

Creato con ❤️ con Hugo e distribuito su Netlify.