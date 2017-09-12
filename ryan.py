import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import urllib2
import requests
import sys

driver = webdriver.Chrome(executable_path='./chromedriver')
wait = WebDriverWait(driver, 10)

f = open('activate.csv')
csv_f = csv.reader(f)


h = 'https://www.yelp.com/biz/'
g = 'https://www.yelp.com/'
b = "https://www.mogl.com/admin/biz/reviews/"

foreignIDs = []
def splitThis(linksList):
	for link in linksList:
		if link.startswith(h):
			splitted = link[25:]
			foreignIDs.append(splitted)

		elif link.startswith(g):
			splitted = link[25:]
			foreignIDs.append(splitted)

		elif link == "":
			foreignIDs.append("")

		else:
			foreignIDs.append("")
			print('pass on ' + link)

def printList(someList):
	for row in someList:
		print row

def logIn():
	wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-mogl--green')))
	driver.find_element_by_name('username').send_keys('username')
	driver.find_element_by_name('password').send_keys('password')
	driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div/div[1]/form/button').click()
	wait.until(EC.presence_of_element_located((By.ID, 'contentSource')))

def inputData():
	html_source = driver.page_source
	wait.until(EC.presence_of_element_located((By.ID, 'contentSource')))
	if yelps[i] == "" or foreignIDs[i] == "":
		pass

	elif g in html_source:
		pass

	else:
		# pass
		Select(driver.find_element_by_name('contentSource')).select_by_visible_text('Yelp')
		urlfield = driver.find_element_by_name('url')
		urlfield.clear()
		urlfield.send_keys(yelps[i])
		fidfield = driver.find_element_by_name('foreignId')
		fidfield.clear()
		fidfield.send_keys(foreignIDs[i])
		driver.find_element_by_xpath('//*[@id="pageContent"]/div/div[3]/div/div[2]/div/table/tbody/tr[2]/td[7]/button').click()
		newpagesource = driver.page_source
		if '500 - Page Error' in newpagesource:
			print b + str(orders[i][0]) + "\n" + yelps[i] + "\n"

orders = []
for index, row in enumerate(csv_f):
	#skip first line; is header row
	if (index > 0):
		temp = []
		temp.append(row[0]) #0 bizID
		temp.append(row[1]) #1 name
		temp.append(row[2]) #2 address
		temp.append(row[3]) #3 city
		temp.append(row[4]) #4 state
		#temp.append(row[6]) #5 zip
		orders.append(temp)

f.close()


#printList(orders)

yelps = []

with open("yelp.txt", "w") as pl:
	for i in range(0,len(orders)):
	# for i in range(0, 10):
		print orders[i][0]

		query = orders[i][1] + '+' + orders[i][2] #+ ' ' + orders[i][3]
		goog_search = "https://www.google.com/search?q=yelp+" + query
		#print str(goog_search)
		output = "https://www.mogl.com/admin/biz/reviews/" + str(orders[i][0])

		try:
			r = requests.get(goog_search)
			soup = BeautifulSoup(r.text, "html.parser")

			cite = soup.find('cite')
			#print cite
			if cite != None:
				cite = cite.text

			if cite == None:

				pl.write(goog_search  + '\n' + output + '\n' + '\n')

				yelps.append("")
				print("Cite == None: %s - Wrote it to File") % cite
				#write to file that this link was not a yelp link

			elif cite != None:

				if cite.startswith(h):
					print cite
					yelps.append(cite)

				elif cite.startswith(g):

					pl.write(goog_search  + '\n' + output + '\n' + '\n')

					print cite + ' -no biz in link- wrote to file'
					yelps.append(cite)
					#write to file saying link needs to be fixed

				else:
					print cite
					pl.write(goog_search  + '\n' + output + '\n' + '\n')

					yelps.append("")
					print("Passed on %s and wrote it to a file and list as an empty string") % cite
					#write to file that this link was not a yelp link

			else:
				print 'wtf'

		except requests.exceptions.RequestException as e:
			print e
			sys.exit(1)



splitThis(yelps)
printList(yelps)
printList(foreignIDs)



for i in range(0,len(orders)):
# for i in range(0, 10):
	driver.get(b + str(orders[i][0]))

	if i == 0:
		logIn()
		inputData()

	else:
		inputData()
