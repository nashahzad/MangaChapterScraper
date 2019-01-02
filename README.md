### Manga Chapter Scraper
Given a starting url for first page a of a manga chapter and the chapter number, this will scrape all the pages of the chapter and create a page with all the chapter images stacked up on each other allowing for more convenient reading of a chapter without having to click through each and every individual page.
- Python 3.5.4, flask, requests, Pillow, urllib3
- Currently tested on mangatown and mangastream(still WIP for mangastream)


### Future Updates

- Extend functionality/logic to work on other manga sites
    - Look into how to generically parse for url of next page
- Put flask app into a docker container that can just stay running in the background or something
