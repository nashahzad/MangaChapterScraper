from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from crawler import ImageCrawler

app = Flask(__name__)
Bootstrap(app)
light = True

@app.route('/')
def hello_world():
    args = request.args.to_dict()
    global light
    light = True if args.get('light', 'true') == 'true' else False
    return render_template('query_page.html', light=light)

@app.route('/search')
def search():
    args = request.args.to_dict()
    crawler = ImageCrawler(args)
    images = crawler.crawl()
    global light
    return render_template('image_results.html', images=images, light=light)


if __name__ == '__main__':
    app.run("0.0.0.0", port=80)
