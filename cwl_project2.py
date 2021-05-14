import requests
from bs4 import BeautifulSoup
from imdb import IMDb
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


print("Processing Wikipedia Titles")
pbar = tqdm(total=2022 - 1980)
year = 1980
wiki_titles = []
wiki_count = 0
while year < 2022:
  res = requests.get('https://en.wikipedia.org/wiki/List_of_Bollywood_films_of_' + str(year))
  soup = BeautifulSoup(res.content, 'html.parser')
  table = soup.find_all(class_="wikitable")
  table = table[len(table) - 1]
  rows = table.find_all('tr')[1:] #ignoring the header row
  for row in rows:
    data = row.find_all('td')
    if len(data) > 0:
      output = ""
      if 'a.k.a' in data[0].text:
        output = data[0].text[0: data[0].text.index(' a.k.a')]
      else:
        output = data[0].text


      if '\n' not in output:
        wiki_titles.append(output)
        wiki_count += 1
      
  
  pbar.update(1)
  year = year+1
  
pbar.close()
print(wiki_titles)
print("Processing IMDb Titles")

ia = IMDb()
#imdb_titles = []
imdb_count = 0
imdb_missed = list()
pbar = tqdm(total=len(wiki_titles))
for title in wiki_titles:
  movies = ia.search_movie(title)
  if len(movies) > 0:
    #imdb_titles.append(title)
    imdb_count += 1
  else:
    imdb_missed.append(title)
  pbar.update(1)

pbar.close()
  

rotten_count = 0
rotten_tomatoes_missed = list()
pbar = tqdm(total=len(wiki_titles))
for title in wiki_titles:
  temp = title.lower()
  temp = temp.replace(" ", "_")
  res = requests.get('https://www.rottentomatoes.com/m/' + temp)
  if res.status_code != 404:
    rotten_count += 1
  else:
    rotten_tomatoes_missed.append(title)

  pbar.update(1)
pbar.close()

  

print("Done With Processing")

print('IMDB Titles Not in Wikipedia:')
print(imdb_missed)
print()
print('Rotten Tomatoes Titles Not in Wikipedia:')
print(rotten_tomatoes_missed)

dbs = ['Wikipedia', 'IMDB', 'Rotten Tomatoes']
counts = [wiki_count, imdb_count, rotten_count]
counts = np.array(counts)
counts = counts/ wiki_count
plt.bar(dbs, counts, color='green')
plt.title('Proportion of Bollywood Movie Titles From 1980-Now Overlapping with Wikipedida')
plt.show()