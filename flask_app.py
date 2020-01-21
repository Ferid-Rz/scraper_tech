from flask import Flask
import requests
import json
from bs4 import	BeautifulSoup
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    instagram_url = 'https://www.instagram.com'

    def get_followers_count(profile_url: str, session):
    	response = session.get(f"{instagram_url}/{profile_url}")
    	if response.ok:
    		html = response.text
    		bs_html = BeautifulSoup(html,features="html.parser")
    		scripts = bs_html.select('script[type="application/ld+json"]')
    		scripts_content = json.loads(scripts[0].text.strip())
    		main_entity_of_page = scripts_content['mainEntityofPage']
    		interaction_statistic = main_entity_of_page['interactionStatistic']
    		followers_count = interaction_statistic['userInteractionCount']
    		return followers_count


    if request.method == 'GET':
        ins= []
        ins1 = request.args.get('ins1', '')
        ins2 = request.args.get('ins2', '')
        ins3 = request.args.get('ins3', '')

        ins.append(ins1)
        ins.append(ins2)
        ins.append(ins3)
        list = []

        profiles = [ins1,ins2,ins3]
        if (ins1=='' and ins2=='' and ins3==''):
            return '<h1>write account name as GET query</h1>'
        for profile in profiles:
            if profile == "":
                continue
            count = get_followers_count(profile,requests)
            list.append(f"{profile} has {count} followers")
        dictionary = dict(zip(list,range(len(list))))
        return dictionary


if __name__ == '__main__':
    app.run()

