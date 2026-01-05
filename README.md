# 📝 Harper Reed's Blog Repository


Welcome to my personal blog repository! This project showcases my thoughts, experiences, and random musings on technology, politics, and everything in between. It's built using modern web technologies and static site generation techniques.

## 📖 Summary of Project

The blog is powered by [Hugo](https://gohugo.io/), a fast and flexible static site generator, and hosted on [Netlify](https://www.netlify.com/). This repository contains all the necessary files, configurations, and contents for a fully functioning blog setup.

### Key Features:
- Custom theme based on Hugo Vitae
- Continuous Deployment with Netlify
- Markdown support for content creation
- Responsive design for all devices
- Integrated SEO features for better visibility

---

## 🔧 How to Use

### Prerequisites
Make sure you have the following installed:
- [Go](https://golang.org/doc/install) (version 1.19 or higher)
- [Hugo](https://gohugo.io/getting-started/quick-start)

### Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/harperreed/harper.blog.git
   cd harper.blog
   ```

2. **Install Dependencies**
   Go modules will automatically manage dependencies.

3. **Run the Development Server**
   Start the Hugo server to preview your blog locally:
   ```bash
   hugo server -D
   ```
   Navigate to `http://localhost:1313` to view your blog in your web browser.

4. **Make Changes**
   Edit posts in the `content` directory using Markdown. You can create new posts using the provided templates in the `archetypes` folder.

5. **Deploy to Netlify**
   For deployment, push your changes to the main branch. The site will automatically build and deploy to Netlify.

### Environment Variables
For specific configurations, you may need to define environment variables in a `.env` file for local development:
```
NOTES_JSON_FEED_URL=your_json_feed_url_here
NOTES_HUGO_CONTENT_DIR=your_hugo_content_directory_here
LINKS_RSS_URL=your_rss_feed_url_here
LINKS_HUGO_CONTENT_DIR=your_hugo_content_directory_here
```

---

## 🛠️ Tech Info

- **Languages and Frameworks**: Hugo (Go)
- **Key Libraries**:
  - `requests`: For making HTTP requests
  - `feedparser`: Used to parse RSS feeds
  - `html2text`: Converts HTML to Markdown

- **Directory Structure**:
  ```
  .
  ├── .github/
  ├── archetypes/
  ├── config/
  ├── content/
  ├── layouts/
  ├── tools/
  ├── README.md
  └── netlify.toml
  ```

- **Hosting**: The site is hosted on Netlify, allowing for continuous deployment and easy management.
- **Version Control**: The project is maintained using Git, with a clear commit history to track changes over time.

Feel free to explore and contribute! If you have any questions, please reach out to me at [harper@modest.com](mailto:harper@modest.com).

Happy blogging! 🎉
