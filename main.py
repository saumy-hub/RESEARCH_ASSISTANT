import os
import time
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from agent import ResearchAgent

console = Console()

def main():
    console.print(Panel.fit("[bold green]🧠 Smart Research Assistant[/bold green]\n[dim]Powered by Groq & Agentic Tools[/dim]"))
    
    # Ensure outputs directory exists
    os.makedirs("outputs", exist_ok=True)
    
    while True:
        try:
            query = console.input("\n[bold cyan]Enter your research query (or 'quit' to exit): [/bold cyan]")
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("[dim]Goodbye![/dim]")
                break
                
            if not query.strip():
                continue
                
            agent = ResearchAgent()
            
            with console.status("[bold green]Researching...[/bold green]") as status:
                report = agent.run(query)
                
            console.print("\n")
            console.print(Panel(Markdown(report), title="[bold blue]Research Report[/bold blue]", border_style="blue"))
            
            save_prompt = console.input("\n[bold yellow]Save report to file? (y/n): [/bold yellow]")
            if save_prompt.lower() == 'y':
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                slug = "".join(c if c.isalnum() else "_" for c in query[:20]).strip("_")
                filename = f"outputs/{timestamp}_{slug}.md"
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(report)
                console.print(f"[bold green]✓ Report saved to {filename}[/bold green]")
                
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye![/dim]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
