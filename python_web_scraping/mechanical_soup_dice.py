import mechanicalsoup
import time

browser = mechanicalsoup.Browser()

for i in range(50):
	page = browser.get("http://olympus.realpython.org/dice")
	tag = page.soup.select("#result")[0]
	result = tag.text

	print(f"The result of your dice roll is: {result}")

	# if(i < 3):
		# time.sleep(10)