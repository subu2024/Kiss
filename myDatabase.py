# myDatabase.py

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

import os, shutil
from markdown2 import markdown
from datetime import date, datetime
import re


# ML libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS 
from sklearn.metrics.pairwise import cosine_similarity

# constants
BLANK_VAL = ''
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')




# funtion to remove extraneous characters from string
def cleanHTML(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

# date utility for user friendly date
def convertDate(blogDate):
    m = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    blogYear = blogDate[0:4]
    blogMonth = m[int(blogDate[5:7])-1]
    return blogMonth + " " + blogYear


# count the number of words in a given text
def countWordsInText(textList, wordLength):
    totalWords = 0
    for text in textList:
        totalWords += len(text)/wordLength
    return totalWords

# get reading time for posts
def estimateReadingTime(content):
    str = ""
    WPM = 150 #words you can read per minute
    wordLength = 5
    minutes = round(countWordsInText(content, wordLength) / WPM)
    if minutes > 1:
        str = "{minutes} minutes read".format(minutes=minutes)
    else:
        str = "< 1 minute read"
    return str

# read all content and compute related content..
def read_data(config, pwatch):

    pwatch.summary_write("reading data file", config.show_summary)
    all_data = {'POSTS': read_content(config.content_folder, config.file_ext, config.blank_val)}

    all_data["total_posts"] = str(len(all_data["POSTS"]))

    pwatch.summary_write("computing related articles", config.show_summary)
    all_data["all_related"] = get_related_content(all_data["POSTS"], config.related_article_count)

    pwatch.summary_write("reading individual page content", config.show_summary)
    all_data["pages"] = read_content(config.pages_folder, config.file_ext, config.blank_val)

    return all_data



# read content files from specific folder with specific extension..
def read_content(content_folder, file_ext, blank_val):
    # root_dir needs a trailing slash (i.e. /root/dir/) 
    
    content_folder = content_folder +"/"  
    POSTS = []
    ctr=0
    for dirpath, dirnames, files in os.walk(content_folder):
       # if dirpath != ignore_folder:
            for file_name in files:
               
                if file_name.endswith(file_ext):
                    file = os.path.join(dirpath, file_name)
                    #print('processing file', file)
                    with open(file, 'r') as file:
                        posts_content = markdown(file.read(), extras=['metadata'])

                        # Fetch metadata of each article
                        title = posts_content.metadata['title']
                        postDate = posts_content.metadata['date'] if 'date' in posts_content.metadata else str(date.today())
                        displayDate = convertDate(postDate)
                        slug = posts_content.metadata['slug']
                        #if has_category:
                        #    category = posts_content.metadata['category'] if 'category' in posts_content.metadata else blank_val
                        #else:
                        #    category = blank_val
                        summary = posts_content.metadata['summary'] if 'summary' in posts_content.metadata else posts_content[:25]
                        readingTime = estimateReadingTime(posts_content)
                        # if the status is not present in the file, it's assumed that the post is published.
                        status = posts_content.metadata['status'] if 'status' in posts_content.metadata else 'published'
                        #image = posts_content.metadata['image'] if 'image' in posts_content.metadata else no_image
                        tags = posts_content.metadata['tags'] if 'tags' in posts_content.metadata else blank_val
                            
                        # Only published posts must be stored
                        #if status == 'published':
                        POSTS.extend([
                                    {
                                        
                                        'title': title,
                                        'date': displayDate,
                                        'realDate': postDate,
                                        'slug': slug,
                                        #'category': category,
                                        'summary': summary,
                                        'readingTime': readingTime,
                                        'tags': tags,
                                        'status': status,
                                        'content':  posts_content,
                                        #'image': image,
                                        'ctr': ctr
                                        
                                    }
                        ])
                        ctr=ctr+1

    # sort posts by date
    POSTS.sort(key=lambda post: datetime.strptime(post['realDate'], '%Y-%m-%d'), reverse=True)
   
    return POSTS


#function to generate related content 
def get_related_content(all_posts, related_article_count=3):
    #print("in related content TBD")
    
    all_posts_content = []
    
    all_related = []


    # grab the content and title
    for each_post in all_posts:
        
        all_posts_content.extend([
            each_post['title'] + cleanHTML(each_post['content'])
         ])

    vect = TfidfVectorizer(min_df=2, lowercase=True, ngram_range=(1,2),stop_words='english')
    vectors = vect.fit_transform(all_posts_content)
    #print("TFID Matrix:", vectors.toarray())

    cosine_sim = cosine_similarity(vectors)


    # for each individual post ..
    article_index = 0
    for each_post in all_posts:
        
        #print(each_post['title'])
        similar_articles = list(enumerate(cosine_sim[article_index]))
        #sorted_similar_articles = sorted(similar_articles, key=lambda x:x[1], reverse=True)
        top = sorted(similar_articles, key=lambda x:x[1], reverse=True)[:4]
        #print(top)
        #for i in top:
        #    print(i[0])
        related = get_recommendations(all_posts, top, article_index)
        all_related.extend([
                            {"originalTitle": each_post["title"],
                             "posts": related
                             }
                    ])

        article_index = article_index + 1
    return all_related
        
    



def get_recommendations(all_posts, top, current_post):
    recommended_posts = []
    for i in top:
            index=0
            for each_post in all_posts:
                if i[0] == index and i[0] != current_post:
                    recommended_posts.extend([
                            {
                             'title': each_post["title"],
                             'slug': each_post["slug"],
                             'ctr': each_post["ctr"],
                             'date': each_post['date'],
                             #'category': each_post['category'],
                             'tags': each_post['tags'],
                             'summary': each_post['summary'],
                             'readingTime': each_post['readingTime'],
                             #'image': each_post['image'],

                             }
                    ])
                index=index+1
    return recommended_posts