from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

df = pd.read_csv('IndiaglitzUrls.csv')
movie_urls = df['MovieUrls']

def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
    
def getDetails(soup):
    det = []
    if soup.find('h2', class_ = 'movie_title'):
        title = soup.find('h2', class_ = 'movie_title').text
    else:
        title = np.NaN
    container = soup.find('div', class_ = 'movie_main_detail')
    if container:
        details = container.findAll('div', class_ = 'movie_main_detail_cell')
        limit = len(details)
        for i in range(1, limit, 2):
            det.append(details[i].text)   
    return title, det
    
def otherDetails(soup):
    data, story, analysis, verdict = [], '', '', ''
    container = soup.find('div', class_ = 'news_content newscontent_img')
    if container:
        for i in container.findAll('p'):
            data.append(i.text)
        story_index = data.index('Story:') if 'Story:' in data else None
        analysis_index = data.index('Analysis:') if 'Analysis:' in data else None
        verdict_index = data.index('Verdict:') if 'Verdict:' in data else None    
        if story_index:
            if analysis_index:
                story += ' '.join([data[j] for j in range(story_index + 1, analysis_index)])
            elif verdict_index:
                story += ' '.join([data[j] for j in range(story_index + 1, verdict_index)])
            else:
                story += ' '.join([data[j] for j in range(story_index + 1, len(data))])
        if analysis_index:
            if verdict_index:
                analysis += ' '.join([data[j] for j in range(analysis_index + 1, verdict_index)])
            else:
                analysis += ' '.join([data[j] for j in range(analysis_index + 1, len(data))])
        if verdict_index:
            verdict += ' '.join([data[j] for j in range(verdict_index + 1, len(data))])
    
        
    return story, analysis, verdict
    
def getRating(soup):
    rating = np.NaN
    container = soup.find('h2', class_ = 'rating_txt')
    if container:
        rating = container.text.split(':')[1].split('/')[0]
    return rating
    
frame = pd.DataFrame()
titles, banner, cast, direction, production, music, verdict, analysis, story, rating = [], [], [], [], [], [], [], [], [], []
movies = [movie_urls[i] for i in range(450, 500)]
for url in movies:
    html_soup = getSoup(url)
    t, det = getDetails(html_soup)
    s, a, v = otherDetails(html_soup)
    r = getRating(html_soup)
    if len(det) > 4:
        ba = det[0]
        ca = det[1]
        dire = det[2]
        pro = det[3]
        mu = det[4]
    else:
        ba = np.NaNurl = movie_urls[0]
        ca = np.NaN
        dire = np.NaN
        pro = np.NaN
        mu = np.NaN

    titles.append(t)
    banner.append(ba)
    cast.append(ca)
    direction.append(dire)
    production.append(pro)
    music.append(mu)
    verdict.append(v)
    analysis.append(a)
    story.append(s)
    rating.append(r)
    print(movies.index(url))

frame['Title'] = titles
frame['Banner'] = banner
frame['Cast'] = cast
frame['Direction'] = direction
frame['Production'] = production
frame['Music'] = music
frame['Verdict'] = verdict
frame['Analysis'] = analysis
frame['Story'] = story
frame['Rating'] = rating
frame.to_csv('Iglitz.csv')
