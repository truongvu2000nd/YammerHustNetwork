from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
userName = 'anh.nv183479@sis.hust.edu.vn'
passWord = 'vietanh2204'


driver = webdriver.Chrome(executable_path ='C:/Users/VietAnh/Downloads/chromedriver.exe')

driver.get("https://www.yammer.com/login?locale=en-US&locale_type=standard")

driver.find_element_by_id( "login").send_keys(userName)
driver.find_element_by_id("password").click()
driver.find_element_by_id("password").send_keys(passWord)
sleep(10)
driver.find_element_by_id( "userNameInput").send_keys(userName)
driver.find_element_by_id("passwordInput").send_keys(passWord)
driver.find_element_by_id("submitButton").click()

sleep(10)
driver.find_element_by_id("idSIButton9").click()
sleep(15)

driver.maximize_window();
for i in range(1,5):
	driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
	sleep(5)
sleep(15)
post_list = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[1]/main/div/ul/li")

print(len(post_list))
for post in range(1,len(post_list)+1):
	userX="/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[1]/main/div/ul/li["+str(post)+"]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/span/div/div[1]/div/div/a/span/span"
	timeX="/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[1]/main/div/ul/li["+str(post)+"]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/ul/li[1]/a/time"
	contentX="/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[1]/main/div/ul/li["+str(post)+"]/div/div/div/div/div[1]/div[3]/div/div/div/span"
	likeX1= "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[1]/main/div/ul/li["+str(post)+"]/div/div/div/div/div[1]/div[4]/div[2]/div/div/div/div/div[2]/div"
	likeX2= "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[1]/main/div/ul/li["+str(post)+"]/div/div/div/div/div[1]/div[5]/div[2]/div/div/div/div/div[2]/div"
	user = driver.find_element_by_xpath(userX)
	timee= driver.find_element_by_xpath(timeX)
	print("* ",user.text,": ",timee.text)
	try:
		like = driver.find_element_by_xpath(likeX1)
		print("  -",like.text)
	except:
		like = driver.find_element_by_xpath(likeX2)
		print("  -",like.text)

	try:
		content = driver.find_element_by_xpath(contentX)
		print("  +",content.text)
	except:
		pass
	print(" ")

