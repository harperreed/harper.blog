---
title: Colophon
type: special
url: /colophon/
nofeed: true
description: About page for harper.blog
weight: 6
menu:
  footer:
    name: Colophon
    weight: 6

---

This website, [harper.blog](https://harper.blog), is the personal blog of Harper Reed. It is built using modern web technologies and static site generation techniques.

## Technology Stack

- **Static Site Generator**: [Hugo](https://gohugo.io/)
- **Hosting**: [Netlify](https://www.netlify.com/)
- **Version Control**: Git (hosted on GitHub)

## Design and Layout

- The site uses a custom theme based on the [Hugo Vitae](https://github.com/dataCobra/hugo-vitae) theme
- Typography: System fonts are used for optimal performance and native appearance
- Responsive design ensures compatibility across various devices and screen sizes

## Content Management

- Blog posts are written in Markdown
- [Netlify CMS](https://www.netlifycms.org/) is integrated for content management
- The site supports both blog posts and static pages

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

## Author and Maintenance

This site is maintained by Harper Reed. For inquiries, please contact harper@modest.com.

Last updated: September 2024


## Change log

Here is the git commit log for this iteration:

{{< readfile file="gitlog.md" markdown="true" >}}

---

Built with ❤️ using Hugo and deployed with Netlify.