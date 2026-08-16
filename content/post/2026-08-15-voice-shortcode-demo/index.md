---
title: Voice shortcode demo
date: 2026-08-15T12:00:00-05:00
draft: true
description: Draft demo of the voice dialogue shortcode — safe to delete once a real post uses it
tags:
    - meta
---

Two characters, back and forth. Slot `a` tints from the theme's link color, slot `b` from its secondary color, so both survive the deploy-time theme roulette.

{{< voice a "Karen" >}}
You did *what* with the production database?
{{< /voice >}}

{{< voice b "Dale" >}}
I renamed it. `db-final-FINAL-2`. For clarity.

Look, the old name had a typo and it was bothering me.
{{< /voice >}}

{{< voice a "Karen" >}}
The typo **was** the name, Dale. Every config file on earth points at the typo.
{{< /voice >}}

{{< voice b >}}
(An unlabeled voice block still gets the border and color — the label is optional.)
{{< /voice >}}
