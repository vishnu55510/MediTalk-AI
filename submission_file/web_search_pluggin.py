from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
import aiohttp

class WebSearchEnginePlugin:
    """Semantic Kernel Plugin for web search using Google Custom Search API."""

    def __init__(self, api_key: str, search_engine_id: str):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    @kernel_function(name="search", description="Performs a web search and retrieves metadata and snippet only")
    async def search(
        self,
        query: Annotated[str, "The search query"],
        num_results: Annotated[int, "Number of search results to return"] = 1,
    ) -> list[dict]:
        """Returns search result metadata (title, link, snippet) without extracting full page content."""

        # Validate num_results (Google API supports max 10)
        num_results = max(1, min(num_results, 10))  # Keep between 1 and 10

        # Prepare parameters
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num_results,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status != 200:
                    try:
                        error_detail = await response.text()
                    except Exception:
                        error_detail = "No error details provided."
                    raise Exception(f"❌ Failed to fetch search results: HTTP {response.status}\nDetails: {error_detail}")

                data = await response.json()
                items = data.get("items", [])
                results = []

                for item in items:
                    title = item.get("title", "")
                    link = item.get("link", "")
                    snippet = item.get("snippet", "")

                    results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet,
                    })

                return results
