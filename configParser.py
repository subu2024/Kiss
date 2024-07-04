from json import load as json_load

CONFIG_FILE = "config.json"


def read_file():
    with open(CONFIG_FILE) as config_file:
        data = json_load(config_file)
    return data


data = read_file()

site = data['site']

### all settings for the process including defaults

try:
    show_featured = data["defaults"]["show_featured"]
except:
    show_featured = False

try:
    themes_folder = data["defaults"]["themes_folder"]
except:
    themes_folder = "themes/dark_mode/"

try:
    content_folder = data["defaults"]["content_folder"]
except:
    content_folder = "content/blog/"

try:
    pages_folder = data["defaults"]["pages_folder"] 
except:
    pages_folder = "content/pages/"

try:
    static_folder = data["defaults"]["static_folder"] 
except:
    static_folder = "content/assets/"

try:
    output_folder = data["defaults"]["output_folder"]
except:
    output_folder = "output/"

try:
    github_folder = data["defaults"]["github_folder"]
except:
    github_folder = ""


try:
    related_article_count = int(data["defaults"]["related_article_count"])
except:
    related_article_count = 2

try:
    paginate_post_count = int(data["defaults"]["paginate_post_count"])
except:
    paginate_post_count = 10



try:
    delete_output_folder = data["defaults"]["delete_output_folder"]
except:
    delete_output_folder = True

try:
    file_ext = data["defaults"]["file_ext"]
except:
    file_ext = "md"

try:
    blank_val = data["defaults"]["blank_val"]
except:
    blank_val = ""

try:
    show_summary = data["settings"]["show_summary"]
except:
    show_summary = False

try:
    file_type = data["settings"]["file_type"]
except:
    file_type = ".html"


try:
    start_page = data["template_name"]["start_page"]
except:
    start_page = "index"

try:
    toc_page = data["template_name"]["toc_page"]
except:
    toc_page = "table-of-contents"

try:
    individual_page = data["template_name"]["individual_page"]
except:
    individual_page = "page"

try:
    article_page = data["template_name"]["article_page"]
except:
    article_page = "article"


try:
    tag_page = data["template_name"]["tag_page"]
except:
    tag_page = "tags"



