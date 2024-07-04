# blogEngine.py

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


import random
import os, shutil
from jinja2 import Environment, PackageLoader

MAIN_FILE = 'main'


# copy all files
def copy_all(src_folder, dest_folder):

    for src_dir, dirs, files in os.walk(src_folder):
        dst_dir = src_dir.replace(src_folder, dest_folder, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:

            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)

            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


# copy all files related to the theme
def copy_theme_assets(ref_folder, src_folder, output_folder):

    src_folder = src_folder  + "/"+ get_asset_folder_name(ref_folder)
    dest_folder = output_folder  + get_asset_folder_name(ref_folder)
    print(src_folder)
    print(dest_folder)
    copy_all(src_folder, dest_folder)

# copy all files from a speficied to another folder
def copy_assets(src_folder, output_folder):

    dest_folder = output_folder  + get_asset_folder_name(src_folder)
    copy_all(src_folder, dest_folder)

# get the assets folder name from the string
def get_asset_folder_name(src_folder):

    str_to_search = "/"
    num = src_folder.count(str_to_search)
    res = [i for i in range(len(src_folder)) if src_folder.startswith(str_to_search, i)]
    folder_name = src_folder[res[num-2]+1:]
    return folder_name

# delete all files in a specific folder
def delete_files(folder_name):
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            os.remove(os.path.join(root, file))
            
# load the templates
def load_template(env, template_name):
    return env.get_template(template_name)

# get random posts
def get_random_posts(POSTS, num_posts=1):
    return next((x for x in random.sample(POSTS, num_posts)), None)
    #return random.sample(POSTS, num_posts)

# get featured posts
def get_featured_posts(POSTS):
    return next((x for x in POSTS if x['status']=='featured'), None)

# creates a file name with default extension of html
def get_file_name(key, ext='html'):
    return key + '.' + ext


# utility function to return a filename with path
def get_file_name_with_folder(base_file_path, base_file_name, curr_page):
    curr_file_path = base_file_name
    if curr_page != 0:
        curr_file_path = curr_file_path + '-'+ str(curr_page)
    
    return get_file_name(base_file_path + curr_file_path )


# write to file
def write_to_file(path, content):
    with open(path, 'w') as file:
        file.write(content)
        file.close()

# create the menu items
def create_site_menu(page_data, menu_dict):
    page_menu = menu_dict
    
    for page in page_data:
        page_menu.extend([{
            'title': page['title'],
            'slug': get_file_name(page['slug']),

         }])
    # sort the tag list by title in reverse order
    page_menu.sort(key=lambda post: post['title'], reverse=True)

    return page_menu


def posts_grouped_by_tags(POSTS):

    posts_metadata = POSTS
    group_by_tags = {}

    comma = ","

    for item in posts_metadata:
        key = item['tags']
        #split the tags
        #sometimes there is a comma as the last character..remove that
        for word in key.split():
            last_chr =  word[-1]
            if last_chr == comma:
                new_word = word[:-1]
            else:
                new_word = word
        
            group_by_tags.setdefault(new_word,[]).append(item)
    return group_by_tags

# create a menu for displaying tags
def get_tag_menu(POSTS):
    grouped_by_tags = posts_grouped_by_tags(POSTS)
    tag_menu = []
    for tag in grouped_by_tags:
        tag_menu.extend([{
            'title': tag,
            'slug': get_file_name(tag),

         }])
    # sort the tag list by title in reverse order
    tag_menu.sort(key=lambda post: post['title'], reverse=True)

    return tag_menu

# create a menu for pagination
def get_pagination_menu(base_file_path, curr_page, start_page, end_page):
    
    curr_file_path = base_file_path

    pagination_menu = []
    for i in range(start_page, end_page+1):
        if (i==0):
            file_path = get_file_name(curr_file_path)
        else:
            file_path = get_file_name(curr_file_path + '-' + str(i)) 
        
        if (i==curr_page):
            file_path = ''
    
        pagination_menu.extend([
            {'title':i+1, 'slug': file_path}
        ])

    return pagination_menu



def create_index_page(posts, all_data, page_template, output_folder, file_name, number_per_page=5):

    total_posts = len(posts)
    
    
    if number_per_page < total_posts and number_per_page != 0:
    
        start_page = 0
        end_page = (int(total_posts/number_per_page) + (total_posts % number_per_page>0))
    
        curr_start_page = start_page
        curr_end_page = number_per_page

        for x in range(start_page, end_page):
            pagination_menu = get_pagination_menu(file_name, x, start_page, end_page-1)
            all_data["paginate"] = pagination_menu
            file_path = get_file_name_with_folder(output_folder, file_name, x)
            all_data["currentPost"] = posts[curr_start_page:curr_end_page]
            curr_start_page = curr_start_page + number_per_page
            curr_end_page = curr_end_page + number_per_page
            write_page(all_data, page_template, file_path , page_title=file_name)

    else:

            all_data["paginate"] = ''
            all_data["currentPost"]=posts
            file_path = output_folder + get_file_name(file_name)
            write_page(all_data, page_template, file_path , page_title=file_name)


# create individual pages
def create_individual_page(all_data, page_template, output_folder, file_name):

    for page in all_data["pages"]:
            #post_file_path  = output_folder + '{slug}'.format(slug=page['slug'])
            post_file_path = output_folder + get_file_name(page['slug'])
            all_data["currentPage"] = page
            write_page(all_data, page_template, post_file_path, page_title='', related_post='')


# create tag pages
def create_tag_pages(all_data, page_template, output_folder, paginate_post_count):
    group_by_tags = posts_grouped_by_tags(all_data["POSTS"])
    
    #loop through each category to create a page
    for tag in group_by_tags:
            posts = group_by_tags[tag]
            create_index_page(posts, all_data, page_template, output_folder, tag, paginate_post_count)



# create article page
def create_article_page(all_data, page_template, output_folder, file_name):

    for post in all_data["POSTS"]:
        
        postTitle = post["title"]
        related_post='' # these are the specific related posts from the list of all 'related'
        
        for each_item in all_data["all_related"]:
            if postTitle == each_item['originalTitle']:
                related_post = each_item['posts']

        all_data["currentPost"] = post
        all_data["currentRelated"] = related_post
        
        post_file_path  = output_folder + '{slug}.html'.format(slug=post['slug'])
        write_page(all_data, page_template, post_file_path, page_title="you may also like ..", related_post='')


# create the main page
def create_home_page(all_data, page_template, config):
   
    POSTS = all_data["POSTS"]

    if config.show_featured:
        all_data["currentPost"] = get_featured_posts(POSTS) # this is a dict - correct
    else:
        #randomPost = get_random_posts(POSTS) # this is a list
        all_data["currentPost"] = get_random_posts(POSTS)

    file_path = config.output_folder + get_file_name(config.start_page)

    try:
        related_post = POSTS[0:3]
    except:
        related_post = POSTS
    
    all_data["currentRelated"] = related_post
    
    write_page(all_data, page_template, file_path, page_title='Our newest posts ..', related_post=related_post)

# introducing the blog engine starter..
# this should kick off the entire blog development process
def start(all_data, config, pwatch):

    # 0 - create the environment
    pwatch.summary_write("creating the jinja2 environment ", config.show_summary)
    env = Environment(loader=PackageLoader(MAIN_FILE,config.themes_folder))
    
    if config.delete_output_folder:
        pwatch.summary_write("deleting output folder @ " + config.output_folder, config.show_summary)
        delete_files(config.output_folder)

    # 1 - tag menu is created
    pwatch.summary_write("gathering all tags", config.show_summary)
    all_data["tags"] = get_tag_menu(all_data["POSTS"])

    # 2 - create the menu layer
    pwatch.summary_write("creating the menu items", config.show_summary)
    menu_dict = [{'title': 'home', 'slug': get_file_name(config.start_page)}, {'title':'table of contents', 'slug': get_file_name(config.toc_page)}]
    all_data["menu"] = create_site_menu(all_data["pages"], menu_dict)
    #print(all_data["menu"])

    
    # 3 - create the home page
    pwatch.summary_write("writing home page", config.show_summary)
    page_template = load_template(env, get_file_name(config.start_page))   
    create_home_page(all_data, page_template, config)
   
    
    # 4 - individual article page
    pwatch.summary_write("writing individual blog page", config.show_summary)
    page_template = load_template(env, get_file_name(config.article_page))   
    create_article_page(all_data, page_template, config.output_folder, config.article_page)

    # 5 - individual page
    pwatch.summary_write("writing individual page like about..", config.show_summary)
    page_template = load_template(env, get_file_name(config.individual_page))
    create_individual_page(all_data, page_template, config.output_folder, config.individual_page )
   

    # 6 - creating an index of all posts
    page_template = load_template(env, get_file_name(config.toc_page))
    create_index_page(all_data["POSTS"], all_data, page_template, config.output_folder, config.toc_page, number_per_page = config.paginate_post_count)
    

    # 7 - creating an index of all tags
    pwatch.summary_write("writing tag page(s)", config.show_summary)
    page_template = load_template(env, get_file_name(config.tag_page))
    create_tag_pages(all_data, page_template, config.output_folder,  config.paginate_post_count)

    # 8 - copy assets
    pwatch.summary_write("copying all assets", config.show_summary)
    copy_assets(config.static_folder, config.output_folder)
    
    # 9 - copy theme assets
    pwatch.summary_write("finally copying assets related to theme", config.show_summary)
    copy_theme_assets(config.static_folder, config.themes_folder, config.output_folder)


#generic function to create a html page using a template
def write_page(data, template, page_path, page_title='',  related_post=''):

    page_html = template.render(pageContent=data, pageTitle=page_title, relatedContent=related_post)

    write_to_file(page_path, page_html)



            
