import re
import requests
import spacy
from wordcloud import WordCloud
from bs4 import BeautifulSoup as bs

nlp = spacy.load('en_core_web_sm')
url = 'https://www.lyrics.com'

def process_artist_name(artistname):
    artistns = re.sub(r'[\s]', '+', str(artistname))
    artist = re.sub(r'[\']', '%27', str(artistns))
    artisturl = str(url) + str('/artist/') + str(artist)
    artist1 = requests.get(artisturl).text
    soup = bs(artist1, 'html.parser')
    linksp = soup.find_all(href=re.compile(r'[\/]lyric\D\d+\D\w+\D\w+'))
    return linksp
    
def get_links(linksp):
    links = []
    for i in linksp:
        links.append(url+i['href'])
    return links

def get_lyrics(links):
    cleanlyrics = []
    for i in links:
        all_lyrics_html = requests.get(i).text
        lyric_soup = bs(all_lyrics_html, 'html.parser')
        lyrics = lyric_soup.find_all(id='lyric-body-text')
        lyrics = re.sub(r'<a href=\"https.*a>', r' ', str(lyrics))
        lyrics = re.sub(r'<pre.*>', r' ', str(lyrics))
        lyrics = re.sub(r'</pre>', r' ', str(lyrics))
        lyrics = re.sub(r'\n|\r|\]|\[', r' ', str(lyrics))
        clyrics = bs(lyrics, 'html.parser')
        cleanlyrics.append([clyrics.text])
        with open('scrape.txt', 'w') as f:
            f.write(str(cleanlyrics))
    return

def tidy_lyrics():
    file = open('scrape.txt', 'r')
    doc = nlp(file.read())
    file.close()
    token_list = []
    lyrics = []
    for token in doc:
        if token.is_alpha:
            token_list.append(token.text.lower())
    for token in token_list:
        lyrics_token = nlp.vocab[token]
        if not lyrics_token.is_stop:
            lyrics.append(token)
    with open('cleanscrape.txt', 'w') as f:
        f.write(str(lyrics))
    
def build_wordcloud():
    file = open('cleanscrape.txt', 'r')
    text = file.read()
    file.close()
    text.split()
    text = re.sub(r'\'|\,|', r'', str(text))
    wordcloud = WordCloud(scale=5,
                          max_words=150,
                          background_color="white",
                          relative_scaling='auto',
                          collocations=False,
                          repeat=False).generate(str(text))
    wordcloud.to_file('static/wordcloud.png')
    return
