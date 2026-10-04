# Reader flow checks

`make check` runs the Python tools, i18n, contrast, TypeScript, and real browser
checks. Install Node from `.mise.toml`, Hugo 0.164.0, and the locked dependencies:

```sh
mise install
npx --yes yarn@1.22.22 install --frozen-lockfile
npx --yes yarn@1.22.22 exec e2e-web install chromium
make check
```

For browser checks alone, use `make check-e2e`. Filter a regression with
`npx --yes yarn@1.22.22 test:e2e --grep 'Spanish home'`.

The pinned tester-army/e2e runner starts production Hugo at
`http://127.0.0.1:23899`, builds into ignored `.e2e/site`, and stops the server.
Port conflicts fail clearly; do not stop another reader's server. One worker,
no retries, no AI credentials, and telemetry disabled. Browser requests to
external services are aborted without fake responses, so analytics, kudos,
comments, third-party covers, and embeds cannot make live writes. Local pages,
images, CSS, and JavaScript remain real. The JavaScript-disabled test uses a
real Playwright context because e2e's engine exposes no JavaScript option.

| Reader flow | Test in `blog.e2e.ts` |
| --- | --- |
| Home → posts/about → home | home navigation |
| Post list → article → related article | posts open articles |
| Notes → next/previous page → permalink | notes paginate |
| Spanish/Japanese/Korean/Chinese navigation | each language |
| Home language switch and back | language switcher |
| Media hub → book/music details and grids → music list | media hub |
| Photos → note → decoded, visible local image | photos open notes |
| RSS feeds, sitemap, robots, static 404 | feeds, sitemap |
| Spanish home → published English Now | Spanish home Now |
| Now → expand history → old entry → current Now | current Now |
| Media/books/music/links pagination; Spanish book list → grid | media lists |
| English article → Spanish translation → English original | translated articles |
| Mobile home → notes without horizontal overflow | mobile reader |
| Link permalink → external source metadata → list | saved link details |
| Missing route → 404 → home | missing routes |
| JavaScript disabled: home → posts → readable article; decoded, visible photo | readers without JavaScript |

Search and client-side filters are absent. The taxonomy config registers only
categories; current content has no categories, so there are no taxonomy term
links or filter flows. Tag templates exist but tags are not enabled. No theme
chooser UI exists. Translated media sections exist only in English/Spanish;
Spanish grid links intentionally reach English grids.

These checks cover representative entries and page transitions, not every
historical article, media resource, theme, browser, language translation, or
pagination page. External comments/kudos/outbound destinations need a separate
explicitly authorized live check. Hugo does not emulate Netlify redirects or
CSP; run the existing build checkers against `.e2e/site` to verify redirect
metadata, feeds, and inline-style constraints. Reports and screenshots live in
`.e2e/report.json` and `.e2e/artifacts`; server output is `.e2e/logs/hugo.log`.

The image fade uses the standard `(scripting: enabled)` media feature. Images
remain visible when scripting or media-feature support is absent. The real
Chromium tests cover enabled and disabled scripting; other engines remain
unverified. See [W3C Media Queries](https://www.w3.org/TR/mediaqueries-5/#scripting).
