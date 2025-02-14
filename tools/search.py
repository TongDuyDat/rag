from typing import List, Dict
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import BaseTool


class Search_web(BaseTool):
    """A tool for performing web searches using DuckDuckGo.
    This class inherits from BaseTool and provides functionality to search the web
    using the DuckDuckGo search engine. It returns search results in a list format.
    Attributes:
        name (str): Name identifier for the tool.
    Args:
        query (str): The search query string to look up.
    Returns:
        List[Dict]: A list of dictionaries containing search results from DuckDuckGo.
        Each dictionary contains information about a search result including title,
        link, and snippet.
    """

    name:str = "seach_imformation_from_web"
    description:str = """
        use this tool when you need to seach imformation that what you don't know about query.
    """

    def _run(self, query: str) -> List[Dict]:
        search = DuckDuckGoSearchResults(output_format="string")
        results = search.invoke(query)
        return results

    async def _arun(self, query: str):
        search = DuckDuckGoSearchResults(output_format="string")
        results = await search.ainvoke(query)
        return results
