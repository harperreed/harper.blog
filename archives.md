---
layout: internal
title: Archives
active: archives
menu: true
---

# The list of all {{ site.posts.size }} archived posts.

Most of these are from years ago and are representative of a youth long forgotten and often still enjoyed.

<div class="post">
  <ul>
  {% for post in site.posts %}
    <li>
      {{ post.date | date: "%b %d, %Y"  }} &mdash; <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
  </ul>
</div>
