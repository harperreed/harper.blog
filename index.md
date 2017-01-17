---
layout: internal
menu: true
---

# Writing

I don't write very often. The last post was on {% for post in site.posts  limit:1%}{{ post.date | date: "%b %d, %Y"  }}{% endfor %}. I spend a lot of my time [tweeting](http://twitter.com/{{site.twitter_username}}){:target="_blank"} or, if I do write, posting to [medium](http://medium.com/@{{site.medium_username}}){:target="_blank"}.

I blogged regularly at [nata2.org](https://web.archive.org/web/*/nata2.org){:target="_blank"} for a bunch of years ({{ site.posts.size }} post between 2000-2015). It was a lot of fun and was a great outlet. Around the launch of Twitter, I stopped doing it regularly.

Here are the last 20 posts I made. If you want, you can check out the full [archives](/archives).

## Most recent twenty posts

<div class="post">
  <ul>
  {% for post in site.posts  limit:20%}
    <li>
      {{ post.date | date: "%b %d, %Y"  }} &mdash; <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
  </ul>
</div>

Check out the full [archives](/archives).
