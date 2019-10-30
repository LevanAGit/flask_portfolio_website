from flask import Flask, render_template, request, url_for
from recommender import recommendations, train_nmf, fuzz_lookup
from wordcloudbuilder import process_artist_name, get_links, get_lyrics, tidy_lyrics, build_wordcloud 

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/recommender')
def get_recommendations():
    user_input = dict(request.args)
    return render_template('recommender.html'), user_input

@app.route('/recommender/result')
def show_data():
    user_input = dict(request.args)
    train_nmf()
    mlist, movid = fuzz_lookup(user_input)
    result = recommendations(mlist, movid)    
    return render_template('rec_result.html', 
                           movies = result)
    
@app.route('/scraper')
def lyrics_scraper():
    return render_template('lyrics.html')

@app.route('/scraper/wordcloud')
def show_wordcloud():
    artistnamedict = dict(request.args)
    artistname = artistnamedict['1']
    linksp = process_artist_name(artistname)
    links = get_links(linksp)
    get_lyrics(links)
    tidy_lyrics()
    build_wordcloud()
    return render_template('wordcloud.html')