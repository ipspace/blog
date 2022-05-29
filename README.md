This is the source code repository for the ipSpace.net blog. The
blog posts are grouped by year and month in the `/content/posts` directory tree, the images are within the `static` directory tree.

Please feel free to contribute to the blog (keeping in mind the [copyright terms](LICENSE.md)). You can

* [fix errors in existing blog posts](#fix-errors)
* [contribute guest blog posts](#contribute-a-guest-blog-post)

## Fix Errors

To fix errors in a blog post:

* Clone the repository
* Find the offending blog post -- use the post URL to find the corresponding Markdown (`.md`) or HTML (`.html`) file in the `/content/posts` directory. Contact me before trying to fix a blog post in HTML format; I can easily convert it into Markdown.
* Fix my blunders
* Commit the changes
* Submit a pull request against the master branch

## Contribute a Guest Blog Post

Contributing a guest blog post couldn't be easier:

* Clone the repository
* Create a new file with `.md` extension in `/content/draft` directory
* Start with the standard YAML front matter. Try to use existing tags (you need a REALLY GOOD reason to introduce a new tag)

```
---
title: "your-title"
draft: True
tags: [ list-of-tags ]
---
```

* Write the blog post in Markdown format
* Commit the changes and submit a pull request

There is no guarantee that your post will be accepted[^SANE], in particular if you write about a topic not directly related to the usual blog content. We might edit your writing, and we will remove all links pointing to blatant self-promotional content, or content not directly relevant to the blog post.

[^SANE]: Sane people would consider the content of this paragraph superfluous common sense. Unfortunately I'm repeatedly pestered by individuals outside of this category.
