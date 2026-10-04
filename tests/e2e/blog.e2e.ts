// ABOUTME: Covers reader navigation, archives, translations, media, and feeds.
// ABOUTME: Uses real Hugo pages; external services are blocked to avoid writes.
import { beforeEach, test } from "@e2e-dev/web";
import { expect } from "e2e";
import { chromium } from "playwright-core";

beforeEach(async ({ browser }) => {
  await browser.route(/^https?:\/\/(?!127\.0\.0\.1:23899\/)/, async (route) => {
    await route.abort();
  });
});

test("home navigation opens archives, about, and returns home", async ({
  app,
  browser,
  screen,
}) => {
  await app.open("/");
  const nav = screen.getByRole("navigation", "Main Navigation");
  await nav.getByRole("link", "Posts").tap();
  await expect(browser).toHaveURL("/posts/");
  await expect(browser.locator(".blog-posts li")).not.toHaveCount(0);
  await nav.getByRole("link", "About").tap();
  await expect(browser).toHaveURL("/about/");
  await expect(screen.getByRole("main")).toContainText("Harper");
  await nav.getByRole("link", "Home").tap();
  await expect(browser).toHaveURL("/");
});

test("posts open articles and related posts", async ({
  app,
  browser,
  screen,
}) => {
  await app.open("/posts/");
  await browser.locator(".blog-posts li a").first().tap();
  await expect(screen.getByRole("heading", /.*/, { level: 1 })).toBeVisible();
  await expect(browser.locator(".byline")).toContainText("words");
  await expect(browser.locator("main article")).toBeVisible();
  await browser.locator(".related-post-link").first().tap();
  await expect(screen.getByRole("heading", /.*/, { level: 1 })).toBeVisible();
});

test("notes paginate both ways and open individual permalinks", async ({
  app,
  browser,
  screen,
}) => {
  await app.open("/notes/");
  const firstText = await browser
    .locator(".notes article")
    .first()
    .textContent();
  await screen.getByRole("link", "Next page →").tap();
  await expect(browser).toHaveURL("/notes/page/2/");
  await expect(browser.locator(".notes article").first()).not.toHaveText(
    firstText ?? "",
  );
  await screen.getByRole("link", "← Previous page").tap();
  await expect(browser).toHaveURL("/notes/");
  await browser.locator(".notes article header a").first().tap();
  await expect(browser).toHaveURL(/\/notes\/(?!page)[^/]+\//);
  await expect(screen.getByRole("main")).toBeVisible();
});

test("each language keeps its own navigation", async ({ app, browser }) => {
  const languages = [
    ["es", "Inicio", "Publicaciones"],
    ["ja", "ホーム", "投稿"],
    ["ko", "홈", "게시물"],
    ["zh", "主页", "文章"],
  ];
  for (const [language, home, posts] of languages) {
    await app.open(`/${language}/`);
    await expect(browser.locator("html")).toHaveAttribute(
      "lang",
      language === "zh" ? "zh-CN" : language,
    );
    const nav = browser.locator("header nav").first();
    await expect(nav.getByRole("link", home)).toHaveAttribute(
      "href",
      new RegExp(`/${language}/$`),
    );
    await nav.getByRole("link", posts).tap();
    await expect(browser).toHaveURL(`/${language}/posts/`);
  }
});

test("language switcher reaches the matching home", async ({
  app,
  browser,
}) => {
  await app.open("/");
  await browser.locator('.language-link[hreflang="es"]').tap();
  await expect(browser).toHaveURL("/es/");
  await browser.locator('.language-link[hreflang="en"]').first().tap();
  await expect(browser).toHaveURL("/");
});

test("media hub opens book and music details and grids", async ({
  app,
  browser,
  screen,
}) => {
  await app.open("/media/");
  await expect(browser.locator(".media-link")).not.toHaveCount(0);
  await expect(browser.locator(".media-music")).not.toHaveCount(0);
  await browser.locator(".media-hub-book").tap();
  await expect(screen.getByRole("heading", /.*/, { level: 1 })).toBeVisible();
  await app.open("/media/books/grid/");
  await expect(browser.locator(".book-grid-item")).not.toHaveCount(0);
  // Published fixture facts: content/books/2026-01-14-red-storm-rising/index.md.
  await browser
    .locator(".book-grid-item")
    .filter({ hasText: "Red Storm Rising" })
    .tap();
  await expect(browser).toHaveURL("/books/2026-01-14-red-storm-rising/");
  await expect(
    screen.getByRole("heading", "Red Storm Rising", { level: 1 }),
  ).toBeVisible();
  await expect(browser.locator(".byline")).toContainText("Tom Clancy");
  await app.open("/media/music/grid/");
  await browser.locator(".music-grid a").first().tap();
  await expect(screen.getByRole("heading", /.*/, { level: 1 })).toBeVisible();
  await screen.getByRole("link", "Back to music").tap();
  await expect(browser).toHaveURL(/\/media\/music\/?$/);
});

test("photos open notes and load a real local image", async ({
  app,
  browser,
}) => {
  await app.open("/photos/");
  await expect(browser.locator(".photo-item")).not.toHaveCount(0);
  await browser.locator(".photo-item a").first().tap();
  const image = browser.locator("main img").first();
  await expect(image).toBeVisible();
  await expect
    .poll(() =>
      browser.evaluate(() => {
        const image = document.querySelector(
          "main img",
        ) as HTMLImageElement | null;
        return !!image?.complete && image.naturalWidth > 0;
      }),
    )
    .toBe(true);
  await expect
    .poll(() =>
      browser.evaluate(() => {
        const image = document.querySelector("main img");
        return image ? getComputedStyle(image).opacity : "";
      }),
    )
    .toBe("1");
});

test("feeds, sitemap, robots, and 404 render real output", async ({ app }) => {
  for (const route of [
    "/index.xml",
    "/posts/index.xml",
    "/notes/index.xml",
    "/photos/index.xml",
    "/media/books/index.xml",
    "/media/music/index.xml",
    "/media/links/index.xml",
  ]) {
    const response = await fetch(new URL(route, app.baseUrl));
    await expect(response.status).toBe(200);
    await expect(await response.text()).toContain("<rss");
  }
  for (const route of ["/sitemap.xml", "/robots.txt", "/404.html"]) {
    const response = await fetch(new URL(route, app.baseUrl));
    await expect(response.status).toBe(200);
    await expect((await response.text()).length).toBeGreaterThan(0);
  }
});

test("Spanish home Now link opens the published English archive", async ({
  app,
  browser,
  screen,
}) => {
  await app.open("/es/");
  const link = screen.getByRole("main").getByRole("link", "Now");
  await expect(link).toHaveAttribute("href", /\/now\/?$/);
  await link.tap();
  await expect(browser).toHaveURL(/\/now\/?$/);
  await expect(browser.locator(".now-posts li")).not.toHaveCount(0);
});

test("current Now expands history and returns from an old entry", async ({
  app,
  browser,
  screen,
}) => {
  await app.open("/now/");
  await screen.getByText("Previous Nows", { exact: true }).tap();
  await browser.locator(".now-posts li a").first().tap();
  await expect(screen.getByRole("heading", /.*/, { level: 1 })).toBeVisible();
  await screen.getByRole("link", "Back to the current Now").tap();
  await expect(browser).toHaveURL(/\/now\/?$/);
});

test("media lists paginate and Spanish books retain the real catalogue", async ({
  app,
  browser,
  screen,
}) => {
  for (const route of [
    "/media/",
    "/media/books/",
    "/media/music/",
    "/media/links/",
  ]) {
    await app.open(route);
    await expect(browser.locator(".media-posts li")).not.toHaveCount(0);
    await screen.getByRole("link", "Next page →").tap();
    await expect(browser).toHaveURL(route + "page/2/");
    await expect(browser.locator(".media-posts li")).not.toHaveCount(0);
    await screen.getByRole("link", "← Previous page").tap();
    await expect(browser).toHaveURL(route);
  }
  await app.open("/es/media/books/");
  await expect(browser.locator(".media-book")).not.toHaveCount(0);
  await screen.getByRole("link", "verlas en formato cuadrícula").tap();
  await expect(browser).toHaveURL(/\/media\/books\/grid\/?$/);
  await expect(browser.locator(".book-grid-item")).not.toHaveCount(0);
});

test("translated articles return to the same English original", async ({
  app,
  browser,
}) => {
  await app.open("/2025/02/16/my-llm-codegen-workflow-atm/");
  await browser.locator('.translation-link[hreflang="es"]').tap();
  await expect(browser).toHaveURL(/\/es\/2025\/02\/16\//);
  await browser.locator(".original-link").tap();
  await expect(browser).toHaveURL("/2025/02/16/my-llm-codegen-workflow-atm/");
});

test("mobile reader navigation and notes remain within the viewport", async ({
  app,
  browser,
  screen,
}) => {
  await browser.setViewport({ width: 390, height: 844 });
  await app.open("/");
  await screen
    .getByRole("navigation", "Main Navigation")
    .getByRole("link", "Notes")
    .tap();
  await expect(browser).toHaveURL("/notes/");
  await expect
    .poll(() =>
      browser.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    )
    .toBe(true);
  await app.screenshot("mobile-notes");
});

test("saved link details expose the source and return to the list", async ({
  app,
  browser,
  screen,
}) => {
  const response = await fetch(new URL("/en/sitemap.xml", app.baseUrl));
  const sitemap = await response.text();
  const path = sitemap.match(/<loc>([^<]*\/links\/[^<]+)<\/loc>/)?.[1];
  await expect(typeof path).toBe("string");
  await app.open(new URL(path!).pathname);
  await expect(screen.getByRole("heading", /.*/, { level: 1 })).toBeVisible();
  await expect(
    browser.locator('main article a[data-tinylytics-event="outbound.link"]'),
  ).toHaveAttribute("href", /^https?:\/\//);
  await screen.getByRole("link", "Back to the current links").tap();
  await expect(browser).toHaveURL("/media/links/");
});

test("missing routes show a helpful 404 and navigation home", async ({
  app,
  browser,
  screen,
}) => {
  await app.open("/e2e-missing-page/");
  await expect(screen.getByRole("heading", "404")).toBeVisible();
  await screen
    .getByRole("navigation", "Main Navigation")
    .getByRole("link", "Home")
    .tap();
  await expect(browser).toHaveURL("/");
});

test("readers without JavaScript can read articles and see photos", async ({
  app,
}) => {
  const browser = await chromium.launch();
  try {
    const context = await browser.newContext({ javaScriptEnabled: false });
    await context.route(/^https?:\/\/(?!127\.0\.0\.1:23899\/)/, (route) =>
      route.abort(),
    );
    const page = await context.newPage();
    await page.goto(app.baseUrl!);
    await page
      .getByRole("navigation", { name: "Main Navigation" })
      .getByRole("link", { name: "Posts", exact: true })
      .click();
    await expect(new URL(page.url()).pathname).toBe("/posts/");
    await page.locator(".blog-posts li a").first().click();
    await expect(await page.locator("main h1").isVisible()).toBe(true);
    await expect(
      (await page.locator("main article").innerText()).length,
    ).toBeGreaterThan(100);
    await page.goto(new URL("/photos/", app.baseUrl).href);
    await page.locator(".photo-item img").first().scrollIntoViewIfNeeded();
    await expect
      .poll(() =>
        page.evaluate(() => {
          const image = document.querySelector(
            ".photo-item img",
          ) as HTMLImageElement | null;
          return !!image?.complete && image.naturalWidth > 0;
        }),
      )
      .toBe(true);
    await expect(
      await page
        .locator(".photo-item img")
        .first()
        .evaluate((image) => getComputedStyle(image).opacity),
    ).toBe("1");
  } finally {
    await browser.close();
  }
});
