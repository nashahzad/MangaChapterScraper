from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib.request
from PIL import Image
import sys
import tldextract

class ImageCrawler:
    HTTPS = "https://"

    def __init__(self, args):
        website = args['website'] if 'http' in args['website'] else 'https://' + args['website']
        self.website = website
        self.chapter = args['chapter']
        extract = tldextract.extract(website)
        self.manga = extract.registered_domain
        self.visited = {}

    def _isNextPage(self, url, next_page):
        sub1 = str(self.chapter)
        sub2 = str(next_page)

        if sub1 in sub2:
            checklist = [sub2, sub1]
        else:
            checklist = [sub1, sub2]

        for check in checklist:
            if check not in url:
                return False
            url = url.replace(check, "", 1)
        return True

    def validateURL(self, url):
        if self.manga not in url:
            url = self.HTTPS + self.manga + url
        elif 'http' not in url:
            url = self.HTTPS + url
        return url

    def nextMangaURL(self, website, next_page):
        for link in BeautifulSoup(requests.get(website).content, 'html.parser', parse_only=SoupStrainer('a')):
            if link.has_attr('href') and self._isNextPage(link['href'], next_page):
                next_url = self.validateURL(link['href'])
                return next_url

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
            website = self.nextMangaURL(website, page)
            if not website:
                break
        return images_list


#Main method to test the Crawler class without having to run the whole app
if __name__ == "__main__":
   args = {
       "website": "http://www.mangatown.com/manga/nanatsu_no_taizai/c345/",
       "chapter": 345,
   }
   crawler = ImageCrawler(args)
   images_list = crawler.crawl()
   for key in crawler.visited.keys():
       print(key)

