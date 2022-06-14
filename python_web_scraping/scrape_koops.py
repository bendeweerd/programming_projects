from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://koops.com/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# soup.prettify()
# print(soup.prettify())

print("\nTitle: " + soup.title.string)

h1 = soup.find_all("h1")
h2 = soup.find_all("h2")
h3 = soup.find_all("h3")
# h4 = soup.find_all("h4")
# h5 = soup.find_all("h5")
a = soup.find_all("a")

print("\nh1:")
for heading in h1:
    if heading.string:
        print("   - " + heading.string)

print("\nh2:")
for heading in h2:
    if heading.string:
        print("   - " + heading.string)

print("\nh3:")
for heading in h3:
    if heading.string:
        print("   - " + heading.string)

# print("\nh4:")
# for heading in h4:
#     if heading.string:
#         print("   - " + heading.string)

# print("\nh5:")
# for heading in h5:
#     if heading.string:
#         print("   - " + heading.string)

print("\nlinks:")
for link in a:
    if link.string:
        print("   - " + link.string + ": " + link.attrs["href"])