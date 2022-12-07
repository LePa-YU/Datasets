from bs4 import BeautifulSoup, SoupStrainer
import codecs
import requests
import time
import os
from os import walk
import codecs

START_TIME = time.time()
READ_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'EECS2311\\Webpages'))
WRITE_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'EECS2311\\'))

def read_files(READ_PATH):
    print("read_files")
    print(READ_PATH)
    filenames = next(walk(READ_PATH), (None, None, []))[2]  # [] if no file

    # Go through all files individually
    for file in filenames:
        filename = READ_PATH+'\\'+file
        file_location = WRITE_PATH+'\\'+file.replace(" ", "_").split('.html')[0]+"\\"
        text_file_name = file_location+file.replace(" ", "_").split('.')[0]+'_content.txt'
        link_file_name = file_location+file.replace(" ", "_").split('.')[0]+'_links.txt'
        print(file)
        print(file_location)
        print(text_file_name)
        print(link_file_name)

        # Checks if the result file exists
        if not os.path.exists(text_file_name):
            find_links(file_location, filename, text_file_name, link_file_name)
        else:
            print(text_file_name+" file exists.")


    return 0

def find_links(file_location, html_file, text_file_name, link_file_name):

    # Make new folder if it doesn't exist
    try:
        os.makedirs(file_location, exist_ok=False)
        print(file_location)
    except:
        print("File already exists")

    # Grab all links in html file
    file = codecs.open(html_file, 'r', 'utf-8')
    for links in BeautifulSoup(file, features="html.parser", parse_only=SoupStrainer('a')):
        if links.has_attr('href'):
            link = links['href']
            # Save all links into file
            with open(link_file_name,"a") as txt:
                txt.write(link+'\n')
            # Open and save all pdf, txt and xlsx files
            if link.endswith('pdf') or link.endswith('txt') or link.endswith('xlsx') :
                filename = link.split('/')[-1]
                r = requests.get(link, stream = True)
                with open(file_location+"\\"+filename,"wb") as pdf:
                    for chunk in r.iter_content(chunk_size=1024):
                        # writing one chunk at a time to pdf file
                        if chunk:
                            pdf.write(chunk)

    # Get all text in html file
    soup = BeautifulSoup(file, "html.parser")
    text = soup.get_text()

    with codecs.open(text_file_name, 'w', encoding='utf-8') as f_write:
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Write to file
        f_write.write(text)

    # input("Press enter to continue...")

    return 0

read_files(READ_PATH)
print("My program took", time.time() - START_TIME, "to run")
