from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from crawler import ImageCrawler

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def hello_world():
    return render_template('query_page.html')

@app.route('/search')
def search():
    args = request.args.to_dict()
    crawler = ImageCrawler(args)
    images = crawler.crawl()
    return render_template('image_results.html', images=images)


if __name__ == '__main__':
    app.run("0.0.0.0", port=80, debug=True)
