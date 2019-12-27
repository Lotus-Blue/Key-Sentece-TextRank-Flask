from flask import Flask, request, render_template
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    title = request.form['title']
    text = request.form['text']
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)# py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    processed_text = text.upper()
    print( '关键词：' )
    for item in tr4w.get_keywords(20, word_min_len=1):
        print(item.word, item.weight)
    print()
    print( '关键短语：' )
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
        print(phrase)
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')
    print()
    print( '摘要：' )
    sentence = "";
    for item in tr4s.get_key_sentences(num=3):
        print(item.index, item.weight, item.sentence)
        sentence = sentence+item.sentence;
    # return "title"+title+sentence
    return render_template('news.html',Title=title,Text=sentence)

if __name__ == '__main__':
	app.run()