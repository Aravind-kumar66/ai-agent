import urllib.parse
import requests

def search_web(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo JSON API.
    
    Args:
        query: The search query string.
        max_results: Maximum number of results to return.
    """
    try:
        # Use requests instead of urllib - better SSL handling on cloud
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        response = requests.get(url, headers=headers, timeout=10)
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        for result in soup.find_all("div", class_="result__body"):
            title = result.find("a", class_="result__a")
            snippet = result.find("a", class_="result__snippet")
            if title and snippet:
                results.append(
                    f"Title: {title.get_text(strip=True)}\n"
                    f"Snippet: {snippet.get_text(strip=True)}"
                )
            if len(results) >= max_results:
                break
        
        return "\n\n---\n\n".join(results) if results else "No results found."
    
    except Exception as e:
        return f"Web search error: {str(e)}"