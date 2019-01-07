from bs4 import BeautifulSoup
import requests
import urllib.request
from PIL import Image
import sys
import tldextract

class ImageCrawler:
    def __init__(self, args):
        website = args['website'] if 'http' in args['website'] else 'https://' + args['website']
        self.website = website
        self.chapter = args['chapter']
        extract = tldextract.extract(website)
        self.manga = extract.registered_domain
        self.visited = {}

    def validateURL(self, website):
        if self.manga not in website:
            website = 'https://' + self.manga + website
        elif 'http' not in website:
            website = 'https:' + website
        return website

    #Grabs next page url from parent 'a' tag
    def nextMangaURL(self, image, manga, chapter, page):
        parent = image.parent
        if parent.get('href', None) is None:
            return None
        website = parent['href']
        website = self.validateURL(website)
        if manga not in website or chapter not in website or str(page) not in website:
            return None
        return website

    def replaceLastOccurrence(self, string, old, new):
        size = len(old)
        end = len(string)
        start = len(string)-size

        while start >= 0:
            segment = string[start:end]
            if segment == old:
                string = string[:start] + new + string[end:]
                return string
            start -= size
            end -= size
        # One last check from beginning to end just in case
        start = 0
        end = size
        while end <= len(string):
            segment = string[start:end]
            if segment == old:
                string = string[:start] + new + string[end:]
                return string
            start += size
            end += size

    def manipulateURL(self, url, page):
        url_split = url.split('/')
        chapterFound = False
        for i in range(len(url_split)):
            segment = url_split[i]
            if not chapterFound and self.chapter in segment:
                chapterFound = True
            elif chapterFound and str(page) in segment:
                num = ''
                for c in segment:
                    if c.isdigit():
                        num = num + c
                if page != int(num):
                    continue
                url_split[i] = self.replaceLastOccurrence(segment, str(page), str(page+1))
                url = '/'.join(url_split)
                return url
        return None

    def doesURLExist(self, url):
        response = requests.get(url)
        if response.status_code == 404:
            return False
        else:
            return True


    def imageDimensions(self, url):
        if 'png' not in url and 'jpeg' not in url:
            return sys.maxsize
        url = url if 'http' in url else 'http:' + url
        dimensions = Image.open(urllib.request.urlopen(url))
        w, h = dimensions.size
        return w*h

    def getBiggestImage(self, soup):
        images = soup.findAll('img')
        images = sorted(images, key=lambda x: self.imageDimensions(x), reverse=True)
        if images:
            return images[0]
        else:
            return None

    def crawl(self):
        website = self.website
        images_list = []
        page = 1
        while True:
            page += 1
            self.visited[website] = None
            soup = BeautifulSoup(requests.get(website).content, 'html.parser')
            image = self.getBiggestImage(soup)
            if not image:
                break
            images_list.append(image['src'])
            # website = self.nextMangaURL(image, self.manga, self.chapter, page)
            website = self.manipulateURL(website, page-1)
            if website is None:
                website = self.nextMangaURL(image, self.manga, self.chapter, page)
            if not self.doesURLExist(website):
                break
        return images_list

#Main method to test the Crawler class without having to run the whole app
if __name__ == "__main__":
    soup = BeautifulSoup(requests.get('http://www.mangatown.com/manga/shokugeki_no_soma/c294/').content, 'html.parser')
    images = soup.findAll('img')
    for image in images:
        dimensions = requests.head(image['src'])
        print(dimensions.headers['content-length'])

