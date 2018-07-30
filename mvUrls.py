from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
df = pd.DataFrame()
urls = []
for i in range(1, 41):
    st = '\rCollecting urls from page ' + str(i)
    sys.stdout.write(st) 
    url = 'http://www.indiaglitz.com/telugu-movie-reviews?pg=%s' %(i)
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")    
    for i in range(20):
        l = soup.find('div', id = 'ad_column_content_' + str(i) )
        m = l.find('a', href = True)
        urls.append(m.attrs['href'])
    
df['MovieUrls'] = urls
df.to_csv('IndiaglitzUrls.csv')
print('\nUrls collected!!')
