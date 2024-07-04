# KISS - simple HTML blog generator in python
# this is the very basic, rudimentary version 
# v 1.0
# build May 2022
# Subu Sangameswar, Lumos AI

# The MIT License (MIT)
#
# Copyright (c) Lumos AI LLC
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 

from jinja2 import Environment, PackageLoader
from markdown2 import markdown


MAIN_FILE = "main"
file_path = "/"

def main():

    # create a placeholder for data
    POSTS = []

    # read the data file which is in mardown format
    with open("post_1.md", 'r') as file:
        posts_content = markdown(file.read(), extras=['metadata'])

        # Fetch metadata of each article
        title = posts_content.metadata['title']
        postDate = posts_content.metadata['date']
        
        POSTS.extend([
                        {
                                        
                                        'title': title,
                                        'date': postDate,
                                        'content':  posts_content 
                                    }
                        ])

    
    # create the environment for jinja2
    env = Environment(loader=PackageLoader(MAIN_FILE,file_path))

    # using the environment, generate the template for the page
    page_template = env.get_template("index_template.html")

    # render the HTML from the data and the template
    page_html = page_template.render(pageContent=POSTS)

    file_name = "index.html"

    # finally save the newly created HTML 
    with open(file_name, 'w') as file:
        file.write(page_html)
        file.close()


# letting python know explicitly where to start
if __name__ == '__main__':
    main()

