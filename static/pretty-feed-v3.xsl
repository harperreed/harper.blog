<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en" dir="ltr">
      <head>
        <title><xsl:value-of select="/rss/channel/title"/> - Web Feed</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5"/>
        <meta name="description">
          <xsl:attribute name="content">
            <xsl:value-of select="/rss/channel/description"/>
          </xsl:attribute>
        </meta>
        <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
        <!-- Fallback styles in case Tailwind fails to load -->
        <style>
          @media (prefers-reduced-motion: reduce) {
            * {
              animation: none !important;
              transition: none !important;
            }
          }
          img {
            max-width: 20% !important;
            height: auto !important;
            display: block;
            margin: 1rem 0;
          }
        
        </style>
      </head>
      <body class="bg-white text-gray-900 m-0 font-sans leading-normal min-h-screen">
        <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:p-4">Skip to main content</a>
        
        <nav class="max-w-3xl mx-auto px-4 pb-8 mt-2 md:mt-12 border-b border-gray-200" role="navigation" aria-label="Feed information">
          <div class="bg-yellow-50 p-4 border-2 border-dotted border-yellow-200 mb-1 -ml-1 rounded-lg shadow-sm" role="alert">
            <p class="mb-2">
              <strong class="font-semibold">This is a web feed,</strong> also known as an RSS feed. <strong class="font-semibold">Subscribe</strong> by copying the URL from the address bar into your newsreader.
            </p>
            <p class="text-gray-600 text-sm mt-2">
              Visit <a href="https://aboutfeeds.com" class="text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded" target="_blank" rel="noopener noreferrer">About Feeds<span class="sr-only"> (opens in new window)</span></a> to get started with newsreaders and subscribing. It's free.
            </p>
          </div>
        </nav>

        <main id="main-content" class="max-w-3xl mx-auto px-4" role="main">
          <header class="py-8 border-b border-gray-100">
            <h1 class="text-4xl font-bold mb-4 text-gray-900"><xsl:value-of select="/rss/channel/title"/> Feed Preview</h1>
            
            <p class="mb-4 text-gray-700 max-w-prose">
              <xsl:value-of select="/rss/channel/description"/>
            </p>
            <a class="inline-flex items-center text-blue-600 no-underline hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-1 font-medium" target="_blank" rel="noopener noreferrer">
              <xsl:attribute name="href">
                <xsl:value-of select="/rss/channel/link"/>
              </xsl:attribute>
              Visit Website
              <span class="ml-1">→</span>
              <span class="sr-only"> (opens in new window)</span>
            </a>
          </header>

          <section class="py-8" aria-label="Recent feed items">
            <h2 class="text-2xl font-semibold mt-4 mb-6 text-gray-800">Recent Items</h2>
            <div class="space-y-12">
              <xsl:for-each select="/rss/channel/item">
                <article class="group">
                  <h3 class="text-xl font-medium mb-2">
                    <a class="text-blue-600 no-underline group-hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-1" target="_blank" rel="noopener noreferrer">
                      <xsl:attribute name="href">
                        <xsl:value-of select="link"/>
                      </xsl:attribute>
                      <xsl:value-of select="title"/>
                      <span class="sr-only"> (opens in new window)</span>
                    </a>
                  </h3>
                  <time class="text-gray-600 text-sm" datetime="{pubDate}">
                    Published: <xsl:value-of select="pubDate"/>
                  </time>
                  <xsl:if test="description">
                    <div class="mt-2 text-gray-700 line-clamp-3">
                      <xsl:value-of select="description" disable-output-escaping="yes"/>
                    </div>
                  </xsl:if>
                </article>
              </xsl:for-each>
            </div>
          </section>
        </main>

        <footer class="mt-16 py-8 bg-gray-50">
          <div class="max-w-3xl mx-auto px-4 text-center text-gray-600 text-sm">
            This is a web feed, also known as an RSS feed. Subscribe by copying the URL from the address bar into your newsreader.
          </div>
        </footer>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
