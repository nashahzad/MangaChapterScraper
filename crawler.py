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
        self.manga = extract.domain
        self.visited = {}

    def nextMangaURL(self, soup, manga, chapter, page):
        urls = soup.findAll('a', href=True)
        for url in urls:
            link = url['href'] if 'http' in url['href'] else 'http:' + url['href']
            if link not in self.visited and manga in link and chapter in link and str(page) in link:
                return url['href'] if 'http' in url['href'] else 'http:' + url['href']
        return None

    def imageDimensions(self, image):
        url = image['src']
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
            return images[0]['src']
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
            images_list.append(image)
            website = self.nextMangaURL(soup, self.manga, self.chapter, page)
            if not website:
                break
        return images_list


#Main method to test the Crawler class without having to run the whole app
if __name__ == "__main__":
    soup = BeautifulSoup(requests.get('http://www.mangatown.com/manga/shokugeki_no_soma/c294/').content, 'html.parser')
    images = soup.findAll('img')
    for image in images:
        dimensions = requests.head(image['src'])
        print(dimensions.headers['content-length'])

