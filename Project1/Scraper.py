import sys
import requests
from bs4 import BeautifulSoup

Pathurl = sys.argv[1]

response = requests.get(Pathurl, verify=False)
soup = BeautifulSoup(response.text, "html.parser")

print("Title:", soup.title.get_text())
print("Body:", soup.body.get_text())

for link in soup.find_all("a"):
    print("Link:", link.get("href"))