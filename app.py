from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from crawler import ImageCrawler

app = Flask(__name__)
app.secret_key = '....'
Bootstrap(app)
light = True

@app.route('/')
def hello_world():
    args = request.args.to_dict()
    global light
    page_light = args.get('light', None)
    if page_light is None:
        if 'light' in session:
            light = session['light']
        else:
            light = True
    else:
        light = True if page_light == 'true' else False
        session['light'] = light

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