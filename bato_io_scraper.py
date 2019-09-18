import cfscrape
import re
import os
import sys, getopt
import shutil
from bs4 import BeautifulSoup
from time import sleep
from time import time

def main(argv):
    name = ''
    url = ''
    chapter = 0
    overwrite = False
    try:
        opts, args = getopt.getopt(argv, "n:l:c:o", ["name=", "link=", "chapter="])
        print(args)
    except getopt.GetoptError:
        print ('bato_io_scraper.py -n <name> -l <link> -c <chapter>')
        sys.exit(2)
    if len(opts) < 3:
        print ('bato_io_scraper.py -n <name> -l <link> -c <chapter>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-o':
            overwrite = True
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-l", "--link"):
            url = arg
        elif opt in ("-c", "--chapter"):
            chapter = int(arg)

    print('Scraping', name, 'from', url, 'starting at chapter' , chapter)
    parent_directory = os.getcwd() + "\\" + name
    
    if os.path.exists(parent_directory):
        if overwrite == False:
            print(parent_directory + ' already exists.')
            sys.exit(0)
        elif chapter == 1:
            shutil.rmtree(parent_directory)
            os.mkdir(parent_directory)
            print(os.path.exists(parent_directory))
        else:
            pass
    elif chapter == 1:
        os.mkdir(parent_directory)
        

    scraper = cfscrape.create_scraper()
    homepage = url[0:15]

    starting_time = time()
    while (True):
        # Pull HTML from webpage
        r = scraper.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        link = soup.select('script')
        #print(link)

        # Find valid script tag with images list
        images = 0
        for l in link:
            if l.text.find('images') >= 0:
                images = l
                break
        # Create list of img links
        xa = images.text.replace("\"", " ")
        xy = xa.split(" ")
        links = []
        # print(xy)
        for i in xy:
            if re.search("[^\n]jpg$", i) or re.search("[^\n]png$", i):
                links.append(i)
         # print(links)

        if (os.path.exists(parent_directory + "\\Chapter_" + str(chapter)) == False):
            os.mkdir(os.getcwd() + "\\" + name + "\\Chapter_" + str(chapter))
        for i in range(len(links)):
            f = open(name + "\\Chapter_" + str(chapter) + "\\" + str(i) + '.jpg','wb')
            f.write(scraper.get(links[i]).content)
            f.close()
            print(time() - starting_time)
            sleep(10)

        # Next chapter contained in this tag
        #   <div class="col-12 col-md-4 nav-next">
        #   <a class="btn btn-outline-primary" href="/chapter/725600">
        # If this is in place it means that this is the last chapter
        #   <a href="/series/41014" class="btn btn-outline-primary"></a>
        next_chapter = soup.select('.nav-next .btn-outline-primary')
        print(type(next_chapter[0]))
        if next_chapter[0] == None:
            break
        print(next_chapter[0]['href'])
        chapter = chapter + 1
        url = homepage + next_chapter[0]['href']

if __name__ == "__main__":
    main(sys.argv[1:])
