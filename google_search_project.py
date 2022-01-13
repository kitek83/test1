import requests
import urllib
from googlesearch import search
from requests_html import HTMLSession

###################################################
query_to_search = input('Enter query to search: ') 
###################################################
def get_source(url):
    """Return the source code for the provided URL
    ARGS:
        url (string): URL of the page to scrape the
    RETURNS:
        response (object): HTTP response object from requests.html parser

    """
    try:
        session = HTMLSession()
        response =session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query):
    query = urllib.parse.quote_plus(query)
    response = get_source('https://www.google.com/search?q='+query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.',
                      'https://google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.',
                      'https://support.google.com',
                      'https://maps.google.',
                      'https://policies.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)


    return links
#---------------------------------------------------------------------------
#Function, that format an URL encode the query_to_search,send it to Google and show output
def get_results(query):
    query = urllib.parse.quote_plus(query) #parsing searched query_to_search
    response = get_source('https://www.google.com/search?q=' + query) #HTTP response object from request.html.parser

    return response
#------------------------------------------------------------------------------------------
def parse_results(response):  #argument is HTTP response object from request.html.parser

    css_identifier_result = '.tF2Cxc'
    css_identifier_title = 'h3'
    css_identifier_link = '.yuRUbf a'
    css_identifier_text = '.IsZvec'

    results = response.html.find(css_identifier_result)

    output = []  #list with the dictionaries

    for result in results:

        item = {'title': result.find(css_identifier_title, first=True).text,
                'link': result.find(css_identifier_link, first=True).attrs['href'], #attrs is a dictionary, not string. It holds key value pairs for each attribute in an HTML
                'text':result.find(css_identifier_text, first=True).text}

        output.append(item)

    return output
#----------------------------------------------------------------------------------------

def google_search(query):
    response = get_results(query) #HTTP response object from request.html.parser (htpps://google + query_to_search)
    return parse_results(response) #return list for response, which is HTTP response object from request.html.parser

#------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
def google_search2(query):
    counter = 0
    for j in search(query, tld='com', num=300, stop=300, pause=3):
        counter += 1
        print(f'{counter}.{j}')

#############################################################################################################

links = scrape_google(query_to_search)

print(3*'====================================')
print(f'Printing results from def scrape_google() for query:{query_to_search}')
counter = 0
for link in links:
    counter += 1
    print(f'{counter}.{link}')
print(3*'====================================')
#############################################################################################################

results = google_search(query_to_search) #results are from parse_results() function and this is the list

print(f'Printing links from google_search() function for query:{query_to_search}')
counter = 0
for link in results:
    counter += 1
    print(f'{counter}.{link}')
#############################################################################################################
print(3*'=======================================')
print()
print(f'Links from the function google_search2(), which uses search function from google search library\n'
      f'for the query_to_search: {query_to_search}')
google_search2(query_to_search)
print(3*'==================================')

























