---
title: Colophon
type: special
url: colophon
nofeed: true
hideReply: true
translationKey: "colophon"
description: Colophon for harper.blog
weight: 6
slug: colophon
menu:
    footer:
        name: Colophon
        weight: 3
---

This website, [harper.blog](https://harper.blog), is the personal blog of Harper Reed. It is built using modern web technologies and static site generation techniques.

## Technology Stack

- **Static Site Generator**: [Hugo](https://gohugo.io/)
- **Hosting**: [Netlify](https://www.netlify.com/)
- **Version Control**: Git (hosted on GitHub)

## Design and Layout

- The site uses a custom theme based on the [Bear Cub](https://github.com/clente/hugo-bearcub) theme ᕦʕ •ᴥ•ʔᕤ
- ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•！
- Typography: System fonts are used for optimal performance and native appearance
- Responsive design ensures compatibility across various devices and screen sizes

## Content Management

- Content is written in Markdown

## Build and Deployment

- Continuous Deployment is set up through Netlify
- The site is automatically built and deployed when changes are pushed to the main branch
- Custom build commands and settings are defined in `netlify.toml`

## Performance Optimizations

- Images are optimized and served in WebP format where possible
- CSS is minified for production builds
- Hugo's built-in asset pipeline is used for resource optimization

## Additional Features

- RSS feed is available for content syndication
- Social media meta tags are implemented for better sharing on platforms like Twitter and Facebook
- Custom shortcodes are used for enhanced content formatting (e.g., Kit.co integration)

## Development Tools

- A `Makefile` is used to simplify common development tasks
- The project uses Go modules for dependency management

## Accessibility and Standards

- The site aims to be accessible and adheres to modern web standards
- Semantic HTML is used throughout the site

## Analytics

- The site is using [tinylytics](https://tinylytics.app/) to track various bits and hits. You can see the results [here](https://tinylytics.app/public/cw1YY9KSGSE4XkEeXej7).

- This site has recieved {{< ta_hits >}} hits from the following countries: {{< ta_countries >}}.

## Author and Maintenance

This site is maintained by Harper Reed. For inquiries, please contact [harper@modest.com](mailto:harper@modest.com).

Last updated: September 2024

## Change log

Here is the git commit log for this iteration:

{{< readfile file="gitlog.md" markdown="true" >}}

---

Built with ❤️ using Hugo and deployed with Netlify.
