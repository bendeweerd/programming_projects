import re
from urllib.request import urlopen

url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")

pattern = "<title.*?>.*?</title.*?>"
match_results = re.search(pattern, html, re.IGNORECASE)
title = match_results.group()
title = re.sub("<.*?>", "", title)	# Remove HTML tags

print(title)

nameStartIndex = html.find("Name:")
trimmedHtml = html[nameStartIndex:]
nameEndStep = trimmedHtml.find("<")
name = html[nameStartIndex:(nameStartIndex + nameEndStep)].strip(" \r\n\t")
print(name)

colorStartIndex = html.find("Favorite Color:")
trimmedHtml = html[colorStartIndex:]
colorEndStep = trimmedHtml.find("<")
color = html[colorStartIndex:(colorStartIndex + colorEndStep)].strip(" \r\n\t")
print(color)