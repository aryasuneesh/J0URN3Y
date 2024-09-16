import requests
from bs4 import BeautifulSoup
import re

def search_local_experiences(destination: str, interests: list):
    try:
        # Combine destination and interests for search query
        search_query = f"{destination} local experiences {' '.join(interests)}"
        search_url = f"https://html.duckduckgo.com/html/?q={search_query.replace(' ', '+')}"

        # Send a request to DuckDuckGo search
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract search results
        search_results = []
        for result in soup.find_all('div', class_='result__body'):
            title = result.find('a', class_='result__a')
            snippet = result.find('a', class_='result__snippet')

            if title and snippet:
                search_results.append({
                    'title': title.text,
                    'url': title['href'],
                    'snippet': snippet.text
                })

        # Process and extract relevant information
        local_experiences = []
        for result in search_results[:10]: 
            local_experiences.append({
                'title': result['title'],
                'url': result['url'],
                'content': result['snippet']
            })

        return local_experiences

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the function
    print(search_local_experiences("Kyoto, Japan", ["traditional", "food"]))