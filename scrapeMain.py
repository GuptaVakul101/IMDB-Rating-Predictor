import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool
import time

def GET_SOUP(my_url):
	url = my_url
	response = requests.get(url)
	html = response.content
	soup = BeautifulSoup(html, features='lxml')
	return soup

def scrapeData(url):
	soup=GET_SOUP(url)
	table = soup.find('div', attrs={'class': 'lister-list'})
	listOfComments=[]

	for row in table.findAll('div', attrs={'class': 'lister-item mode-detail'}):
		rating = row.find('span', attrs={'class': 'ipl-rating-star__rating'}).text.replace('\n', '')
		title = row.find('h3', attrs={'class': 'lister-item-header'}).find('a').text.replace('\n', '')

		url_2="https://www.imdb.com"+row.find('h3', attrs={'class': 'lister-item-header'}).find('a').get("href")
		soup_2=GET_SOUP(url_2)
		url_3="https://www.imdb.com" + soup_2.find('div', attrs={'class': 'user-comments'}).findAll('a')[4].get("href")

		driver = webdriver.Chrome('/usr/bin/chromedriver')
		driver.get(url_3)
		count = 0
		while True:
			try:
				loadMoreButton = driver.find_element_by_id("load-more-trigger")
				time.sleep(0.1)
				loadMoreButton.click()
				count = 0
				time.sleep(0.1)
			except Exception as e:
				count += 1
				if count == 20:
					break

		soup_3=BeautifulSoup(driver.page_source, features="lxml")

		for item in soup_3.findAll('div', attrs={'class': 'review-container'}):
			try:
				headComment = item.find('div', attrs={'class': 'lister-item-content'}).find('a').text.replace('\n', '')
			except Exception as e:
				headComment = ""

			try:
				mainComment = item.find('div', attrs={'class': 'text show-more__control'}).text.replace('\n', '')
			except Exception as e:
				mainComment = ""

			try:
				commentRating = item.find('span', attrs={'class': 'rating-other-user-rating'}).find('span').text
			except Exception as e:
				commentRating = ""

			listOfComments.append([headComment, mainComment, commentRating])

		driver.quit()
		outfile = open("./data/"+title.replace(' ', '_')+"_"+rating+".tsv", "w")
		writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
		writer.writerow(['Comment Head','Comment Body', 'Comment Rating'])
		writer.writerows(listOfComments)

mainUrl = "https://www.imdb.com/list/ls057823854/"
url = "https://www.imdb.com/list/ls057823854/?sort=list_order,asc&st_dt=&mode=detail&page="

listOfUrls=[]
listOfUrls.append(mainUrl)
for i in range(2, 101):
	listOfUrls.append(url+str(i))

numCores = 4

parProcess = Pool(numCores)
parProcess.map(scrapeData, listOfUrls)
