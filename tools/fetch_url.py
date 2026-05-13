import httpx
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

def fetch_url(url: str, max_chars: int = 4000) -> dict:
    try:
        console.log(f"Fetching URL: [bold blue]{url}[/bold blue]")
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else ""
            
            # Strip unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()
                
            # Extract specific tags
            extracted_text = []
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
                text = tag.get_text(separator=' ', strip=True)
                if text:
                    extracted_text.append(text)
                    
            cleaned_text = " ".join(extracted_text)
            
            # Truncate to max_chars
            if len(cleaned_text) > max_chars:
                cleaned_text = cleaned_text[:max_chars] + "... [truncated]"
                
            console.log(f"Successfully fetched {len(cleaned_text)} characters.")
            return {
                "url": url,
                "content": cleaned_text,
                "title": title
            }
    except Exception as e:
        console.log(f"[red]Error fetching URL: {e}[/red]")
        return {"url": url, "error": str(e)}
