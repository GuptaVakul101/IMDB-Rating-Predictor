import requests
import csv
from bs4 import BeautifulSoup

def GET_SOUP(my_url):
	url = my_url
	response = requests.get(url)
	html = response.content
	soup = BeautifulSoup(html, features='lxml')
	return soup


url = "https://www.imdb.com/chart/top?ref_=nv_mv_250"
soup=GET_SOUP(url)
table = soup.find('tbody', attrs={'class': 'lister-list'})

listofRows=[]
count = 0
for row in table.findAll('tr'):
    listOfCells = []
    rating = row.find('td', attrs={'class': 'ratingColumn imdbRating'}).text.replace('\n', '')
    title = row.find('td', attrs={'class': 'titleColumn'}).find('a').text.replace('\n', '')
    listOfCells.append(title)
    listOfCells.append(rating)
    
    url_2="https://www.imdb.com"+row.find('td', attrs={'class': 'titleColumn'}).find('a').get("href")
    soup_2=GET_SOUP(url_2)
    #print(url_2)
    url_3="https://www.imdb.com" + soup_2.find('div', attrs={'class': 'user-comments'}).findAll('a')[4].get("href")
    soup_3=GET_SOUP(url_3)
    #print(url_3)
    
    print("Start:", str(count))
    for item in soup_3.findAll('div', attrs={'class': 'review-container'}):
    	text_2=item.find('div', attrs={'class': 'lister-item-content'}).find('a').text
    	print(text_2)
    	listOfCells.append(text_2)

    print("End:", str(count))
    listofRows.append(listOfCells)
    count += 1
    if count == 2:
    	break

outfile = open("./imdb.csv", "w")
writer = csv.writer(outfile)
writer.writerow(['Movie','Rating'])
writer.writerows(listofRows)
