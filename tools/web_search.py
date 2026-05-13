from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

def web_search(query: str, max_results: int = 5) -> list[dict]:
    try:
        console.log(f"Searching the web for: [bold cyan]{query}[/bold cyan] (max_results: {max_results})")
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key or api_key == "your_key_here":
            return [{"error": "TAVILY_API_KEY is not set or invalid."}]
            
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)
        
        results = []
        for result in response.get('results', []):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("content", ""),
                "score": result.get("score", 0.0)
            })
        
        console.log(f"Found {len(results)} results.")
        return results
    except Exception as e:
        console.log(f"[red]Error during web search: {e}[/red]")
        return [{"error": str(e)}]
