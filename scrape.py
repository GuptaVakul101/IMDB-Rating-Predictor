import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

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
    # print(url_2)
    url_3="https://www.imdb.com" + soup_2.find('div', attrs={'class': 'user-comments'}).findAll('a')[4].get("href")
    
    # print(url_3)

    count_2=0
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    driver.get(url_3)
    while True:
    	try:
    		count_2+=1
    		loadMoreButton = driver.find_element_by_id("load-more-trigger")
    		time.sleep(1)
    		loadMoreButton.click()
    		time.sleep(1)
    		if count_2==10:
    			break
    	except Exception as e:
    		print(e)
    		break
    print("Complete")
    #time.sleep(10)

    soup_3=BeautifulSoup(driver.page_source)    


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

    driver.quit()

outfile = open("./imdb.csv", "w")
writer = csv.writer(outfile)
writer.writerow(['Movie','Rating'])
writer.writerows(listofRows)
