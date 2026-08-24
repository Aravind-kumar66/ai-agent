import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


def search_web(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo HTML search.

    Args:
        query: The search query string.
        max_results: Maximum number of search results to return.
    """
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")
        results = []

        for result in soup.find_all("div", class_="result"):
            title_tag = result.find("a", class_="result__a")
            snippet_tag = result.find("a", class_="result__snippet")

            if title_tag and snippet_tag:
                results.append(
                    f"Title: {title_tag.get_text(strip=True)}\n"
                    f"URL: {title_tag['href']}\n"
                    f"Snippet: {snippet_tag.get_text(strip=True)}"
                )

            if len(results) >= max_results:
                break

        return (
            "\n\n---\n\n".join(results)
            if results
            else "No search results found."
        )
    except Exception as e:
        return f"Web search error: {str(e)}"