import os
import requests

def search_web(query: str, max_results: int = 5) -> str:
    """Search the web using Serper API for real-time results.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.
    """
    api_key = os.environ.get("SERPER_API_KEY")
    
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("SERPER_API_KEY")
        except Exception:
            pass

    if not api_key:
        return "Web search unavailable: SERPER_API_KEY not configured."

    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json={"q": query, "num": max_results},
            timeout=10
        )
        data = response.json()
        results = []

        for item in data.get("organic", [])[:max_results]:
            results.append(
                f"Title: {item.get('title', '')}\n"
                f"URL: {item.get('link', '')}\n"
                f"Snippet: {item.get('snippet', '')}"
            )

        return "\n\n---\n\n".join(results) if results else "No results found."

    except Exception as e:
        return f"Web search error: {str(e)}"