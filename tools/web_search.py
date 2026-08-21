import requests


def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo Instant Answer API.
    """

    url = "https://api.duckduckgo.com/"

    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = []

        # Main abstract
        abstract = data.get("AbstractText")

        if abstract:
            results.append(
                f"Summary:\n{abstract}"
            )

        # Related topics
        for topic in data.get("RelatedTopics", []):

            if len(results) >= max_results:
                break

            if isinstance(topic, dict):

                text = topic.get("Text")
                first_url = topic.get("FirstURL")

                if text:
                    result = text

                    if first_url:
                        result += f"\nURL: {first_url}"

                    results.append(result)

        if not results:
            return "No useful search results were found."

        return "\n\n".join(results)

    except requests.RequestException as e:
        return f"Web search error: {e}"

    except ValueError as e:
        return f"Invalid response from search API: {e}"

if __name__ == "__main__":
    print(web_search("Python programming language"))