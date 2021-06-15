from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os


def scrape_info():
	#Splinter
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=False)


	#Python Dictionary of all scraped data
	listings = {}


	#Nasa Mars News
	url = 'https://redplanetscience.com/'
	browser.visit(url)


	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	title = soup.find_all('div', class_='content_title')
	news_p = soup.find_all('div', class_='article_teaser_body')

	#Title and Paragraph variables
	news_title = title[0].text
	news_paragraph = news_p[0].text

	
	listings.update({'news_title':title[0].text})
	listings.update({'news_p':news_p[0].text})
	


	#Mars Image
	image_url = 'https://spaceimages-mars.com/'
	browser.visit(image_url)

	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	image = soup.find_all('img', class_='headerimage fade-in')
	for h in image:
		featured_image_url = 'https://spaceimages-mars.com/' + h["src"]
    
    ####################################
	listings.update({'featured_image_url':featured_image_url})
	####################################

	# Mars Facts Table
	mars_fact_url = "https://galaxyfacts-mars.com/"

	tables = pd.read_html(mars_fact_url)

	df = tables[0]
	df = df.rename(columns = {0 :' ', 1 : 'Mars', 2 : 'Earth'})

	###############################################
	html_table = df.to_html(justify="left", classes="table table-striped")
	listings.update({'table':html_table})
	html_table.replace('\n', '')
	################################################
	df.to_html('table.html')


	#Mars Hemispheres 
	mars_hemispheres_url = "https://marshemispheres.com/"
	browser.visit(mars_hemispheres_url)

	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	image = soup.find_all('a', class_='itemLink product-item')

	hemishere_image_urls = []
	#The range(len)-1 below was to allow us to reduce the duplicate anchor rows appearing to one row each
	for i in range(len(image)-1):
	    #The mod below is to display only one url by taking only the even numbers in the range(len) list
	    if(i%2==0):
	        #To loop through all four links we need to first find the url and concantenate 
	        full_res_image_ = 'https://marshemispheres.com/' + image[i]["href"]
	        #browser.visit on each concantenated url from above
	        browser.visit(full_res_image_)
	        
	        html = browser.html
	        soup = BeautifulSoup(html, 'html.parser')
	        #Since each image and title have the same parent line in the html, we can use beautifulsoup to find url/title for each
	        image1 = soup.find_all('img', class_='wide-image')
	        title = soup.find('h2', class_='title')
	        #The for-loop below is for grabbing the "src" section of the img tag
	        for h in image1:
	            #Concantenate
	            featured_resolution = 'https://marshemispheres.com/' + h["src"]
	            #Append both title and url to dictionary
	            hemishere_image_urls.append({'title':title.text,'img_url':featured_resolution})

	#############################################           
	listings["hemishere_image_urls"] = hemishere_image_urls
	#############################################

	print(listings)

	browser.quit()

    # Return results
	return listings

scrape_info()