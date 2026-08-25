import urllib.parse
import urllib.request
import json

def search_web(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo Instant Answer API.
    
    Args:
        query: The search query string.
        max_results: Maximum number of results to return.
    """
    url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_redirect=1&no_html=1"
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        results = []
        
        # Abstract (main answer)
        if data.get("AbstractText"):
            results.append(f"Summary: {data['AbstractText']}\nSource: {data.get('AbstractURL', '')}")
        
        # Related topics
        for topic in data.get("RelatedTopics", []):
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(f"Result: {topic['Text']}\nURL: {topic.get('FirstURL', '')}")
            if len(results) >= max_results:
                break
        
        return "\n\n---\n\n".join(results) if results else "No results found for this query."
    
    except Exception as e:
        return f"Web search error: {str(e)}"