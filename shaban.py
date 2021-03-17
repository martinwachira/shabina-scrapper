from selenium import webdriver
from datetime import datetime
from time import sleep
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html

browser=webdriver.Firefox()
#today = datetime.today().strftime('%Y-%m-%d')
today ='2019-10-11'
#url ="https://www.lamudi.com.ph/buy/"
url="https://www.lamudi.com.ph/rent/"
browser.get(url)


sleep(10)
links = set()
for a in browser.find_elements_by_class_name("js-listing-link"):
    links.add(a.get_attribute('href'))
	



new = list(links)
elements = []
for link in new:
	browser.get(link)
	sleep(10)
	page = BeautifulSoup(browser.page_source, "lxml")
	sleep(6)
	##Get Price
	db = {}
	try:
		overview = page.find('div', {'class':'Header-title-block small-12 columns'})
		loc = overview.find('h3',{'class':'Header-title-address'})
		name = overview.find('h1')
		name = name.text.strip()
		name = name.replace("\n",'')
		loc = loc.text.strip()
		loc = loc.replace("\n",'')
		db['Name'] = name
		db['Location'] = loc
		
	except Exception as e:
		#print(e)
		db['Location'] = 'NA'
		db['Name'] = 'NA'
	try:
		overview = page.find('div', {'class':'row Overview-pdp'})
		price = overview.find('span',{'class':'Overview-main FirstPrice'})
		price = price.text
		db['Price'] = price
	except Exception as e:
		price = 'NA'
		db['Price'] = price
	#elements.append(('price',price))	
	try:
		
		overview = page.find('div', {'class':'row Overview-pdp'})
		cont = overview.findAll('div',{'class':'medium-2 small-2 columns Overview-attribute-wrapper'})
		for div in cont:
			 key = ' '.join(div.select('i')[0]['class'])
			 key = key.strip()
			 key = key[5:]
			 key = key.title()
			 val =  div.find('span',{'class':'Overview-attribute'}).text
			 val = val.strip()
			 val = val.replace('\n', '')
			 val = val.replace('  ','')
			 db[key] = val
			 
			 
			
			
	except Exception as f:
		db['Bedrooms'] = 'N/A'
		db['Bathrooms'] = 'N/A'
		db['Livingsize'] = 'N/A'
		db['Land-Size'] = 'N/A'
		

		
	#Amenitiees
	
	try:
		amen = page.find('section',{'id':'listing-amenities'}) 
		divam = amen.findAll('div',{'class':'ellipsis'})  
		amenities = [s.text.replace("\n",'').strip() for s in divam]
		amenities_clean = ','.join(map(str, amenities)) 
		db['Amenities'] = amenities_clean
		
	except Exception as e:
		db['Amenities'] = 'N/A'	
		
	elements.append(db)
	
	
	
	

df = pd.DataFrame(elements)
#df.to_csv('job.csv',index=False)
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
time_now = time_now.replace(':','-')
time_now = time_now.replace(' ','_')
df.to_csv("job.csv at "+time_now+".csv", index=False)
print(df)