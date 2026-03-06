"""
Web Research Tool - Search and research information from the web.
"""

import os
import json
from typing import Optional, List, Dict, Any
from .base import AgenticTool, ToolResult

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None


class WebResearchTool(AgenticTool):
    """
    Agentic web research tool that performs web searches and extracts information.
    
    Supports:
    - Web search via search APIs
    - Content extraction and summarization
    - Document caching and reuse
    """
    
    def __init__(self):
        super().__init__(
            name="WebResearchTool",
            description="Search and research information from the web",
            version="1.0.0"
        )
        self.cache_enabled = True
        self.cache_dir = None
        self.search_results_cache = {}
        self._validate_dependencies()
    
    def _validate_dependencies(self) -> None:
        """Check if required dependencies are installed."""
        if requests is None or BeautifulSoup is None:
            self.set_metadata("warnings", "requests or BeautifulSoup4 not installed")
    
    def validate_inputs(self, **kwargs) -> tuple[bool, Optional[str]]:
        """Validate input parameters."""
        query = kwargs.get("query")
        if not query or not isinstance(query, str):
            return False, "query parameter is required and must be a string"
        
        if len(query.strip()) == 0:
            return False, "query cannot be empty"
        
        return True, None
    
    def execute(self, **kwargs) -> ToolResult:
        """
        Execute web research.
        
        Parameters:
            query (str): Search query
            max_results (int): Maximum number of results to fetch (default: 5)
            use_cache (bool): Whether to use cached results (default: True)
        
        Returns:
            ToolResult: Contains search results and metadata
        """
        is_valid, error = self.validate_inputs(**kwargs)
        if not is_valid:
            return ToolResult(
                success=False,
                data=None,
                error=error
            )
        
        query = kwargs.get("query", "").strip()
        max_results = kwargs.get("max_results", 5)
        use_cache = kwargs.get("use_cache", True)
        
        # Check cache first
        if use_cache and query in self.search_results_cache:
            return ToolResult(
                success=True,
                data=self.search_results_cache[query],
                metadata={"source": "cache", "query": query}
            )
        
        # Perform search
        results = self._perform_search(query, max_results)
        
        if results is None:
            return ToolResult(
                success=False,
                data=None,
                error="Web search requires API keys or manual search configuration"
            )
        
        # Cache results
        if use_cache and self.cache_enabled:
            self.search_results_cache[query] = results
        
        return ToolResult(
            success=True,
            data=results,
            metadata={
                "source": "web_search",
                "query": query,
                "result_count": len(results),
                "cached": False
            }
        )
    
    def _perform_search(self, query: str, max_results: int) -> Optional[List[Dict[str, Any]]]:
        """
        Perform web search. Currently returns mock data.
        
        To enable real searches, configure:
        - GOOGLE_SEARCH_API_KEY + GOOGLE_SEARCH_ENGINE_ID for Google Custom Search
        - SERPAPI_KEY for SerpAPI
        - Or implement your preferred search provider
        """
        # Try to use configured API if available
        api_key = os.getenv("SERPAPI_KEY")
        if api_key:
            return self._search_with_serpapi(query, api_key, max_results)
        
        # Return mock/placeholder results for demonstration
        return self._generate_placeholder_results(query, max_results)
    
    def _search_with_serpapi(self, query: str, api_key: str, max_results: int) -> Optional[List[Dict[str, Any]]]:
        """Search using SerpAPI (if available)."""
        if requests is None:
            return None
        
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": api_key,
                "num": max_results,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for result in data.get("organic_results", [])[:max_results]:
                results.append({
                    "title": result.get("title"),
                    "url": result.get("link"),
                    "snippet": result.get("snippet"),
                    "source": "serpapi"
                })
            
            return results
        except Exception as e:
            self.set_metadata("last_error", str(e))
            return None
    
    def _generate_placeholder_results(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate placeholder results for demonstration."""
        return [
            {
                "title": f"Research Result {i+1}: {query}",
                "url": f"https://example.com/result-{i+1}",
                "snippet": f"This is a placeholder result for '{query}'. Configure SERPAPI_KEY to enable real web searches.",
                "source": "placeholder"
            }
            for i in range(max_results)
        ]
    
    def extract_content(self, url: str) -> ToolResult:
        """
        Extract and summarize content from a URL.
        
        Parameters:
            url (str): URL to extract content from
        
        Returns:
            ToolResult: Contains extracted content and metadata
        """
        if requests is None or BeautifulSoup is None:
            return ToolResult(
                success=False,
                data=None,
                error="requests or BeautifulSoup4 not installed for content extraction"
            )
        
        if not url or not isinstance(url, str):
            return ToolResult(
                success=False,
                data=None,
                error="url parameter is required and must be a string"
            )
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)
            
            return ToolResult(
                success=True,
                data={
                    "url": url,
                    "title": soup.title.string if soup.title else "No title",
                    "content": text[:1000],  # First 1000 chars
                    "content_length": len(text)
                },
                metadata={"source": "web_extraction"}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Failed to extract content: {str(e)}"
            )
    
    def clear_cache(self) -> None:
        """Clear the search results cache."""
        self.search_results_cache.clear()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache information."""
        return {
            "cache_enabled": self.cache_enabled,
            "cached_queries": len(self.search_results_cache),
            "queries": list(self.search_results_cache.keys())
        }
