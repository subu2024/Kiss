# KISS Static Site Generator, Powered by Python

Introduction
-----------

KISS is a static site generator that requires no database or server-side logic. The project is maintained by Subu Sangameswar (@subusangam). It started out as a fun learning project and has evolved as a useful tool.   
KISS stands for **Keep it simple senorita**  

>This is ver 3.20 released Jun 2022
>No more updates or enhancements planned
>see live version at [chasing a rainbow](https://www.chasingarainbow.org)

Written in Python 3.6

Requires the following libraries
    - [jinja2](https://jinja2docs.readthedocs.io/en/stable/) as template engine
    - [markdown](https://www.markdownguide.org/cheat-sheet) to write content
    - json for config file
    - [w3.css](https://www.w3schools.com/w3css/) as the css framework
    - google fonts for display
    - sklearn
    - re 

Take full control of your static website/blog generation by using your
own simple, lightweight, and magic-free static site generator in
Python. 


Some of features include:

- Write content in Markdown markup
- Generate static output 
- Easy to host anywhere
- Themes helps customize your way

… and many other features see below.


1. Generate home page with featured post or random post
2. Generate blog page for each post
3. Display a list of tags
4. Blogs and tags are paginated
5. Set config varaibles in **config.json** file that will help control many features of the blog
6. Themes allow full customization of the display
7. Google analytics included .. set google analytics id in the config file
8. Generate related articles using TFID and Cosine-similarity
9. Interactivity with AWS API and Lambda can be added if needed


Ver 1
-------
1. This is an introduction on how to build the HTML blog using python
2. Simple one page blog derived from a content in a markdown file
3. Download at [ver1](https://github.com/dvader2021/KISS/tree/main/ver_1)

Ver 2
-------
1. This is an expansion of the introduction on how to build the HTML blog using python - inludes a table of contents
2. Expansion includes multiple pages derived from markdown and a table of contents page
3. Download at [ver2](https://github.com/dvader2021/KISS/tree/main/ver_2)


Ver 3 or this version
---------------------

Get Started
-----------

This section provides some quick steps to get you off the ground as
quickly as possible.

***config.json***

> site
> - title: name of the site displayed on all pages
> - description: brief descrption mainly for search engines
> - keywords: less useful but specifically for search engines
> - url: url of the site
> - ver: the last published version
> - published: the last published date
> - copyright: specific copyright language to be included in the footer
> - contact (name, email, twitter): contact info specific to the site  
> - google_analytics: specify the google analytics id .. otherwise leave it blank
> - aws_api: specify the aWS api .. otherwise leave it blank

> defaults
> - show_featured: setting it to **TRUE** will show featured posts on the home page requires at least one post to be marked with status = featured. Defaults to FALSE
> - themes_folder: the folder name where the current theme is located. requires a leading "/" to the folder name
> - content_folder: the folder name where content is being saved. requires a leading "/" to the folder name
> - pages_folder: the folder name where individual page like about is being saved. requires a leading "/" to the folder name
> - static_folder: the folder name where static info like images is being saved. requires a leading "/" to the folder name
> - output_folder: the folder name where final output is being written to. requires a leading "/" to the folder name
> - related_article_count: the count of related articles to be displayed. default is 3
> - paginate_post_count: numeric value. setting to 0 disables pagination. Blogs, categories and tags are controlled by this variable
> - delete_output_folder: setting to **true** deletes all files in output folder before a new build
> - file_ext: currently not used. set to "md". do not change
> - blank_val: internal usage. do not change

> settings
> - show_summary: ability to print summary on console during the build process
> - file_type: the suffix for files. not used currently. set to .HTML


> template_name {DO NOT CHANGE ANYTHING IN THIS SECTION}
> - start_page: set to "index.html"
> - toc_page: set to "all_posts.html"
> - individual_page: set to "page.html"
> - article_page: set to "article.html"
> - tag_page: set to "tags.html"


Get Started
-----------

- download files from github
- create a folder
- create additional folders for content, output. Within content folder, create pages and blog folder.
- update config.json with updated folder names (if required)
- update config.json with google analytics id, if required
- create content and drop into content/blog folder
- run the main.py to create a html output in the output folder
- that's all.. you are good to go..

Code
-----------

- bloggerEngine.py .. this is the heart of this application. Does the heavy lifting 
- configParser.py .. this piece of code reads the config.json file. config provides ample customization. see below for details
- myDatabase.py .. simple code to read .md files
- main.py .. this is the main program   

The data is combined into a large JSON file that the jinja parser can use to fill in the templates
- more details TBD

AWS
----------

- if AWS is the chosen option, then provide the API in the config file
- Lambda and API Gateway is used for "claps" count 
- The lambda receives 
{title_str: title of the post}
and returns with
{title_str: title of the post,
clap_int: count of total claps}
- within the lambda function, the following functionality happens
- search for a record with the title. if found, get the count and add 1 to it. if not found, insert the title and count of 1 .. response is sent back with the title and updated count

Themes
----------
- Includes one theme 

- to build your own theme.. requires the following files ..
- base.html .. the page where you define the fonts and css
- article.html
- page.html
- index.html
- table-of-contents.html
- tags.html
- inc-article-details.html
- inc-article-list.html
- inc-article-related.html
- inc-pagination.html
- inc-google-analytics.html
- inc-aws-connectivity.html


FAQ
---

Here are some frequently asked questions along with answers to them:

 1. Can you add feature X to this project?

    ***I do not have any plans to add new features to this project***. It is
    intended to be as minimal and as simple as reasonably possible. This
    project is meant to be a quick-starter-kit for developers who want
    to develop their own static site generators. Someone who needs more
    features is free to fork this project repository and customize the
    project as per their needs in their own fork.

 2. Do you accept bug fixes and improvements?

    Yes, I accept bug fixes and minor improvements that do not increase
    the scope and complexity of this project.


 3. How do I add my own copyright notice to the source code without
    violating the terms of license while customizing this project in my
    own fork?

    This project is released under the terms of the MIT license. One of
    the terms of the license is that the original copyright notice and
    the license text must be preserved. However, at the same time, when
    you edit and customize this project in your own fork, you hold the
    copyright to your changes. To fulfill both conditions, please add
    your own copyright notice above the original copyright notice and
    clarify that your software is a derivative of the original.

    Here is an example of such a notice where a person named J. Doe
    wants to reserve all rights to their changes:

        # Copyright (c) 2021-2023 J. Doe
        # All rights reserved

        # This software is a derivative of the original rhythm.
        # The license text of the original rhythm is included below.

    Anything similar to the above notice or something to this effect is
    sufficient.



License
-------

This is free and open source software. You can use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of it,
under the terms of the [MIT License](LICENSE.md).

This software is provided "AS IS", WITHOUT WARRANTY OF ANY KIND,
express or implied. See the [MIT License](LICENSE.md) for details.


Support
-------

To report bugs, suggest improvements, or ask questions, please visit github.
