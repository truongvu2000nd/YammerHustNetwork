from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import csv
import re
import json

userName = ''
passWord = ''

driver = webdriver.Chrome(executable_path ='C:/Users/VietAnh/Downloads/chromedriver.exe')
titl = "All Company"
driver.get("https://web.yammer.com/main/groups/eyJfdHlwZSI6Ikdyb3VwIiwiaWQiOiI0MzY1MTAwNjQ2NCJ9/all")
sleep(3)
driver.find_element_by_name("loginfmt").send_keys(userName)
driver.find_element_by_id("idSIButton9").click()
sleep(5)
driver.find_element_by_id("passwordInput").send_keys(passWord)
driver.find_element_by_id("submitButton").click()
sleep(3)
driver.find_element_by_id("idSIButton9").click()
sleep(5)
linkBegin = "https://www.yammer.com/api/v1/messages/in_group/43651006464.json?threaded=true"
driver.get(linkBegin)
sleep(3)
tes = driver.find_element_by_xpath("/html/body/pre")
data = json.loads(tes.text)
dem = len(data['messages'])
de = 1
with open('tett.csv', 'w', newline='',encoding='utf-8') as csvfile:
	spamwriter = csv.writer(csvfile,delimiter='|', quoting=csv.QUOTE_MINIMAL)
	for i in range(0,dem):
		# if (data['messages'][i]['replied_to_id'] != None):
			print("lan ",de," : ",data['messages'][i]['body']['parsed'])
			print(" ")
			de += 1
			spamwriter.writerow([data['messages'][i]['sender_id'],data['messages'][i]['created_at'],data['messages'][i]['body']['parsed'],data['messages'][i]['liked_by']['count'],titl])
	while dem == 20:
	   minID = data['messages'][dem-1]['id']
	   link2 = linkBegin + "&older_than="+str(minID)
	   driver.get(link2)
	   tes = driver.find_element_by_xpath("/html/body/pre")
	   data = json.loads(tes.text)
	   dem = len(data['messages'])
	   for i in range(0,dem):
	   	# if (data['messages'][i]['replied_to_id'] != None):
		      print("lan ",de," : ",data['messages'][i]['body']['parsed'])
		      print(" ")
		      print(data['messages'][i]['created_at'])
		      de += 1
		      spamwriter.writerow([data['messages'][i]['sender_id'],data['messages'][i]['created_at'],data['messages'][i]['body']['parsed'],data['messages'][i]['liked_by']['count'],titl])
	   print(dem)
	   if(de > 40):
	   	break
	   # print(len(data['messages']))
	   sleep(2)
	spamwriter.writerow(["///","///","///","///","///"])
print("end--------------------------")