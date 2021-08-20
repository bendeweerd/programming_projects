from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://bendeweerd.github.io/resume/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

print("Title: " + soup.title.string)

skills = soup.find_all("h5", {"class": "card-title"})

print("Skills:")
for skill in skills:
	print("   " + skill.string)