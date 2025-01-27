<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <title><xsl:value-of select="/rss/channel/title"/> Web Feed</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
        <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
        <style>
          body {
            background-color: white;
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.5;
          }

          .nav-container {
            max-width: 768px;
            margin: 0 auto;
            padding: 0.5rem 1rem;
            padding-bottom: 2rem;
            margin-top: 0.5rem;

            border-bottom: 1px solid #e1e4e8;
          }

          @media (min-width: 768px) {
            .nav-container {
              margin-top: 3rem;
            }
          }

          .alert-box {
            background-color: #fff5b1;
            padding: 1rem;
            border: 2px dotted #f9e79f;
            margin-bottom: 0.25rem;
            margin-left: -0.25rem;
          }

          .text-muted {
            color: #586069;
          }

          .main-container {
            max-width: 768px;
            margin: 0 auto;
            padding: 1rem;
          }

          .header {
            padding: 2rem 0;
          }

          h1 {
            border: 0;
            margin-bottom: 1rem;
          }

          h2 {
            margin-top: 1rem;
            margin-bottom: 1rem;
          }

          .head-link {
            color: #0366d6;
            text-decoration: none;
          }

          .head-link:hover {
            text-decoration: underline;
          }

          .item-container {
            padding-bottom: 3rem;
          }

          .item-title {
            margin-bottom: 0;
          }

          .item-title a {
            color: #0366d6;
            text-decoration: none;
          }

          .item-title a:hover {
            text-decoration: underline;
          }

          .item-date {
            color: #586069;
            font-size: 0.875rem;
          }
        </style>
      </head>
      <body>
        <nav class="nav-container">
          <p class="alert-box">
            <strong>This is a web feed,</strong> also known as an RSS feed. <strong>Subscribe</strong> by copying the URL from the address bar into your newsreader.
          </p>
          <p class="text-muted">
            Visit <a href="https://aboutfeeds.com">About Feeds</a> to get started with newsreaders and subscribing. It's free.
          </p>
        </nav>

        <div class="main-container">
          <header class="header">
            <h1>Web Feed Preview</h1>
            <h2><xsl:value-of select="/rss/channel/title"/></h2>
            <p><xsl:value-of select="/rss/channel/description"/></p>
            <a class="head-link" target="_blank">
              <xsl:attribute name="href">
                <xsl:value-of select="/rss/channel/link"/>
              </xsl:attribute>
              Visit Website &#x2192;
            </a>
          </header>
          <h2>Recent Items</h2>
          <xsl:for-each select="/rss/channel/item">
            <div class="item-container">
              <h3 class="item-title">
                <a target="_blank">
                  <xsl:attribute name="href">
                    <xsl:value-of select="link"/>
                  </xsl:attribute>
                  <xsl:value-of select="title"/>
                </a>
              </h3>
              <small class="item-date">
                Published: <xsl:value-of select="pubDate" />
              </small>
            </div>
          </xsl:for-each>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
