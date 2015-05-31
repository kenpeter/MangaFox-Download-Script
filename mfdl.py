#!/usr/bin/env python
# encoding: utf-8


"""Mangafox Download Script by Kunal Sarkhel <theninja@bluedevs.net>"""

# Gary
my_debug = 0 
my_root_dir = "/media/kenpeter/3E3C68780C3F137A/dell_backup_07022012/entertainment/manga"

# Gary
if my_debug == 1:
  import pdb

import sys
import os
import urllib
import glob
import shutil
import re
#http://stackoverflow.com/questions/9439480/from-import-vs-import
from zipfile import ZipFile
try:
    # http://en.wikipedia.org/wiki/Beautiful_Soup
    # Beautiful soup 4?
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

# http://pymotw.com/2/contextlib/
from contextlib import closing

#https://docs.python.org/2/library/collections.html#collections.OrderedDict
try:
	from collections import OrderedDict
except ImportError:
	from ordereddict import OrderedDict

#https://docs.python.org/2/library/itertools.html#itertools.islice
from itertools import islice

URL_BASE = "http://mangafox.me/"

# Gary
if my_debug == 1:
  pdb.set_trace()

def get_page_soup(url):
    """Download a page and return a BeautifulSoup object of the html"""
    with closing(urllib.urlopen(url)) as html_file:
        return BeautifulSoup(html_file.read())


def get_chapter_urls(manga_name):
    if my_debug == 1:
      pdb.set_trace()

    """Get the chapter list for a manga"""
    replace = lambda s, k: s.replace(k, '_')
    manga_url = reduce(replace, [' ', '-'], manga_name.lower())
    url = '{0}manga/{1}'.format(URL_BASE, manga_url)
    print('Url: ' + url)
    soup = get_page_soup(url)
    manga_does_not_exist = soup.find('form', {'id': 'searchform'})
    if manga_does_not_exist:
        search_sort_options = 'sort=views&order=za'
        url = '{0}/search.php?name={1}&{2}'.format(URL_BASE,
                                                   manga_url,
                                                   search_sort_options)
        soup = get_page_soup(url)
        results = soup.findAll('a', {'class': 'series_preview'})
        error_text = 'Error: Manga \'{0}\' does not exist'.format(manga_name)
        error_text += '\nDid you meant one of the following?\n  * '
        error_text += '\n  * '.join([manga.text for manga in results][:10])
        sys.exit(error_text)
    warning = soup.find('div', {'class': 'warning'})
    if warning and 'licensed' in warning.text:
        sys.exit('Error: ' + warning.text)
    chapters = OrderedDict()
    links = soup.findAll('a', {'class': 'tips'})
    if(len(links) == 0):
        sys.exit('Error: Manga either does not exist or has no chapters')

    # Gary
    if my_debug == 1:
      pdb.set_trace()

    #Gary
    tmp_manga_name = manga_name.replace('_', ' ')
    tmp_manga_name_1 = re.escape(tmp_manga_name)

    replace_manga_name = re.compile(re.escape(manga_name.replace('_', ' ')),
                                    re.IGNORECASE)
    for link in links:
        # Gary
        if my_debug == 1:
          pdb.set_trace() 

        tmp_text = link.text.replace(':', '')

        #chapters[replace_manga_name.sub('', link.text).strip()] = link['href']
        chapters[replace_manga_name.sub('', tmp_text).strip()] = link['href']
    return chapters


def get_page_numbers(soup):
    """Return the list of page numbers from the parsed page"""

    # Gary sample output
    # <select onchange="change_page(this)" class="m">
    #      <option value="1" selected="selected">1</option><option value="2" >2</option><option value="3" >3</option><option value="4" >4</option><option value="5" >5</option><option value="6" >6</option><option value="7" >7</option><option value="8" >8</option><option value="9" >9</option><option value="10" >10</option><option value="11" >11</option><option value="12" >12</option><option value="13" >13</option><option value="14" >14</option><option value="15" >15</option><option value="16" >16</option><option value="17" >17</option><option value="18" >18</option><option value="19" >19</option><option value="20" >20</option><option value="21" >21</option><option value="22" >22</option><option value="23" >23</option><option value="24" >24</option><option value="25" >25</option><option value="26" >26</option><option value="27" >27</option><option value="28" >28</option><option value="29" >29</option><option value="30" >30</option><option value="31" >31</option><option value="32" >32</option><option value="33" >33</option><option value="34" >34</option><option value="35" >35</option><option value="36" >36</option><option value="37" >37</option><option value="38" >38</option><option value="39" >39</option><option value="40" >40</option><option value="41" >41</option><option value="42" >42</option><option value="43" >43</option><option value="44" >44</option><option value="45" >45</option><option value="46" >46</option>         <option value="0" >Comments</option>
    #    </select>
    # 
    #
    raw = soup.findAll('select', {'class': 'm'})[0]

    return (html['value'] for html in raw.findAll('option'))


def get_chapter_image_urls(url_fragment):
    """Find all image urls of a chapter and return them"""
    print('Getting chapter urls')

    # http://mangafox.me/manga/shingeki_no_kyojin/v15/c059/
    url_fragment = os.path.dirname(url_fragment) + '/'

    chapter_url = url_fragment

    # Gary   
    # chapter === full html: http://mangafox.me/manga/shingeki_no_kyojin/v15/c059/1.html 
    chapter = get_page_soup(chapter_url)
    pages = get_page_numbers(chapter)
    image_urls = []
    print('Getting image urls...')

    # Gary
    # page is page number
    counter = 0
    for page in pages:
        # Gary, comment out for debugging
        print('url_fragment: {0}'.format(url_fragment))
        print('page: {0}'.format(page))
        print('Getting image url from {0}{1}.html'.format(url_fragment, page))
        page_soup = get_page_soup(chapter_url + page + '.html')
        images = page_soup.findAll('img', {'id': 'image'})
        if images:
            # Gary
            # Only interested on images[0]
            image_urls.append(images[0]['src'])
    # Gary
    # Source of image url
    # http://a.mfcdn.net/store/manga/9011/15-059.0/compressed/s001.jpg
  
        # Gary: don't want to get too much url
        if my_debug == 1: 
          counter = counter + 1        
          if counter >= 2:
            break

    return image_urls


def get_chapter_number(url_fragment):
    """Parse the url fragment and return the chapter number."""
    return ''.join(url_fragment.rsplit("/")[5:-1])


def download_urls(image_urls, manga_name, chapter_number):
    # Gary
    #if my_debug == 1:
    #  pdb.set_trace()

    """Download all images from a list"""
    download_dir = my_root_dir + '/{0}/{1}/'.format(manga_name, chapter_number)
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)
    for i, url in enumerate(image_urls):
        
        # Gary
        #if my_debug == 1:
        #  pdb.set_trace()  
    
        filename = my_root_dir + '/{0}/{1}/{2:03}.jpg'.format(manga_name, chapter_number, i)
        print('Downloading {0} to {1}'.format(url, filename))
        urllib.urlretrieve(url, filename)


def make_cbz(dirname):
    """Create CBZ files for all JPEG image files in a directory."""
    zipname = dirname + '.cbz'
    images = glob.glob(os.path.abspath(dirname) + '/*.jpg')
    with closing(ZipFile(zipname, 'w')) as zipfile:
        for filename in images:
            print('writing {0} to {1}'.format(filename, zipname))
            zipfile.write(filename)


def download_manga_range(manga_name, range_start, range_end):
    """Download a range of a chapters"""
    print('Getting chapter urls')
    

    chapter_urls = get_chapter_urls(manga_name)

    # Up to here.
    iend = chapter_urls.keys().index(range_start) + 1
    istart = chapter_urls.keys().index(range_end)
    for url_fragment in islice(chapter_urls.itervalues(), istart, iend):
        chapter_number = get_chapter_number(url_fragment)
        print('===============================================')
        print('Chapter ' + chapter_number)
        print('===============================================')
        image_urls = get_chapter_image_urls(url_fragment)
        download_urls(image_urls, manga_name, chapter_number)
        download_dir = my_root_dir + '/{0}/{1}'.format(manga_name, chapter_number)
        make_cbz(download_dir)
        shutil.rmtree(download_dir)


def download_manga(manga_name, chapter_number=None):
    # Gary
    if my_debug == 1:
      pdb.set_trace()

    """Download all chapters of a manga"""
    chapter_urls = get_chapter_urls(manga_name)

    # Gary
    if my_debug == 1:
      pdb.set_trace()

    if chapter_number:
        if chapter_number in chapter_urls:
            url_fragment = chapter_urls[chapter_number]
        else:
            error_text = 'Error: Chapter {0} does not exist'
            sys.exit(error_text.format(chapter_number))

        # Gary
        #if my_debug == 1:
        #  pdb.set_trace()

        # Gary
        # url_fragment === http://mangafox.me/manga/shingeki_no_kyojin/v15/c059/1.html e.g.
        # chapter_number === v15c059
        chapter_number = get_chapter_number(url_fragment)

        print('===============================================')
        print('Chapter ' + chapter_number)
        print('===============================================')
        image_urls = get_chapter_image_urls(url_fragment)

        # Gary
        #if my_debug == 1:
        #  pdb.set_trace()

        download_urls(image_urls, manga_name, chapter_number)
        download_dir = my_root_dir + '/{0}/{1}'.format(manga_name, chapter_number)
        make_cbz(download_dir)
        shutil.rmtree(download_dir)
    else:
        for chapter_number, url_fragment in chapter_urls.iteritems():
            chapter_number = get_chapter_number(url_fragment)
            print('===============================================')
            print('Chapter ' + chapter_number)
            print('===============================================')
            image_urls = get_chapter_image_urls(url_fragment)
            download_urls(image_urls, manga_name, chapter_number)
            download_dir = my_root_dir + '/{0}/{1}'.format(manga_name, chapter_number)
            make_cbz(download_dir)
            shutil.rmtree(download_dir)

# Gary
if my_debug == 1:
  pdb.set_trace()

if __name__ == '__main__':
    if len(sys.argv) == 4:
        download_manga_range(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        download_manga(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        # Gary
        #if my_debug == 1:
        #  pdb.set_trace()

        download_manga(sys.argv[1])
    else:
        print('USAGE: mfdl.py [MANGA_NAME]')
        print('       mfdl.py [MANGA_NAME] [CHAPTER_NUMBER]')
        print('       mfdl.py [MANGA_NAME] [RANGE_START] [RANGE_END]')
