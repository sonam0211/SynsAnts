from flask import Flask,render_template,request
import urllib2
from bs4 import BeautifulSoup


app = Flask(__name__)

url = 'http://www.synonym.com/synonym/'

def get_synonym(word):
	full_url = url+word
	response = urllib2.urlopen(full_url)
	html = response.read()
	soup = BeautifulSoup(html,'html.parser')
	synonyms_ul = soup.find('ul',{'class':'synonyms'})
	synonyms = synonyms_ul.find_all('a')
	antonyms_ul = soup.find('ul' , {'class':'antonyms'})
	antonyms = antonyms_ul.find_all('a')
	synsants = {}
	synsants['synonyms'] = [str(synonym.string) for synonym in synonyms]
	synsants['antonyms'] = [str(antonym.string) for antonym in antonyms]
	return synsants 


@app.route('/')
def base():
	return render_template('base.html')

@app.route('/result',methods=['GET','POST'])
def result():
	if request.method == 'POST':
		if request.form['word']:
			syns = get_synonym(request.form['word'])
			return render_template('index.html',dict_syns = syns)

if __name__ == '__main__':
	app.run(debug = True) 
