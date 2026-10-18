import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

class SearchTool:
    def __init__(self, num_results=5):
        self.num_results = num_results

    def search_and_scrape(self, query):
        print(f"Searching for: {query}")
        search_results = []
        try:
            # googlesearch-python search
            for url in search(query, stop=self.num_results, pause=2):
                search_results.append(url)
        except Exception as e:
            print(f"Search error: {e}")
            return []

        scraped_data = []
        for url in search_results:
            content = self._scrape_url(url)
            if content:
                scraped_data.append({
                    "url": url,
                    "content": content[:2000]  # Limit content size for LLM context
                })
        return scraped_data

    def _scrape_url(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                
                text = soup.get_text()
                # Break into lines and remove leading/trailing whitespace
                lines = (line.strip() for line in text.splitlines())
                # Break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # Drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
                return text
            return None
        except Exception as e:
            print(f"Scraping error for {url}: {e}")
            return None

if __name__ == "__main__":
    tool = SearchTool(num_results=2)
    results = tool.search_and_scrape("AI latest trends 2024")
    for res in results:
        print(f"Source: {res['url']}\nContent Snippet: {res['content'][:200]}...\n")
