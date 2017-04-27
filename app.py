from flask import Flask,render_template,request
import urllib.request
from bs4 import BeautifulSoup
from model import SynsAnts
from peewee import create_model_tables

app = Flask(__name__)

create_model_tables([SynsAnts], fail_silently=True)

url = 'http://www.synonym.com/synonym/'

def get_synonym(word):
	full_url = url + word
	response = urllib.request.urlopen(full_url)
	html = response.read()
	soup = BeautifulSoup(html,'html.parser')
	synonyms_ul = soup.find('ul',{'class':'synonyms'})
	synonyms = synonyms_ul.find_all('a')
	antonyms_ul = soup.find('ul' , {'class':'antonyms'})
	antonyms = antonyms_ul.find_all('a')
	synsants = {}
	synsants['word'] = word
	synsants['synonyms'] = [str(synonym.string) for synonym in synonyms]
	synsants['antonyms'] = [str(antonym.string) for antonym in antonyms]
	return synsants 


def exists(word):
	return SynsAnts.select().where(SynsAnts.word == word).exists()	


@app.route('/')
def base():
	return render_template('base.html')

@app.route('/result',methods=['GET','POST'])
def result():
	if request.method == 'POST':
		if request.form['word']:
			if not exists(request.form['word']):
				try:
					syns = get_synonym(request.form['word'])
					save_data = SynsAnts(**syns)
					print('saving to database:{}'.format(syns['word']))
					save_data.save()
				except:
					return 'No synonyms or antonyms found'
			else:
				data = SynsAnts.select().where(SynsAnts.word == request.form['word']).first()
				syns = {}
				syns['word'] = data.word
				syns['synonyms'] = data.synonyms
				syns['antonyms'] = data.antonyms
			return render_template('index.html',dict_syns=syns)	
		return 'Please Enter Word'

if __name__ == '__main__':
	app.run(debug = True) 
