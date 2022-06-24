import requests


url = "https://www.congress.gov/search?q=%7B%22congress%22%3A%5B%22117%22%5D%2C%22source%22%3A%22all%22%2C%22search%22%3A%22health%20care%22%7D"

res = requests.get(url)
print(res.text)