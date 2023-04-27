import requests

def newsInit():
    # set the API endpoint and parameters
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',  # set the country to get headlines from
        'apiKey': '023225675d1e49c59a6e149eb70f62cc'  # replace with your actual API key
    }

    # make the HTTP GET request to the API
    response = requests.get(url, params=params)
    return response

def getNews(response):
    # parse the JSON response
    data = response.json()
    articles_str = ''
    # display the headlines and news stories
    for index, article in enumerate (data['articles']):
        if index < 5:
            articles_str += article['title'] + '\n' + article['description'] + '\n\n'
        else:
            break
    return articles_str

def news():
    response = newsInit()
    articles = getNews(response)
    print(articles)

news()
