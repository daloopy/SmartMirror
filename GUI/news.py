import requests

# set the API endpoint and parameters
url = 'https://newsapi.org/v2/top-headlines'
params = {
    'country': 'us',  # set the country to get headlines from
    'apiKey': '023225675d1e49c59a6e149eb70f62cc'  # replace with your actual API key
}

# make the HTTP GET request to the API
response = requests.get(url, params=params)

# parse the JSON response
data = response.json()

# display the headlines and news stories
for article in data['articles']:
    print(article['title'])
    print(article['description'])
    print(article['url'])
    print()
