import os
import json
from pathlib import Path
from dotenv import load_dotenv
from rich import print
from rich.table import Table
from .tools import WebResearchTool, ToolManager
from . import research_cli

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
LIBRARY = DATA / "library"

def doctor():
    """Check environment + folder setup."""
    load_dotenv(ROOT / ".env")

    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    LIBRARY.mkdir(parents=True, exist_ok=True)

    print("[bold]AI Toolkit Doctor[/bold]")
    print(f"Project root: {ROOT}")
    print(f"Library path: {LIBRARY}")

    if not openai_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")
    if not gemini_key:
        raise RuntimeError("Missing GEMINI_API_KEY in .env")

    print("[green]✅ OPENAI_API_KEY found[/green]")
    print("[green]✅ GEMINI_API_KEY found[/green]")
    print("[green]✅ data/library ready[/green]")


def research(query: str, max_results: int = 5):
    """
    Perform web research on a query.
    
    Example: ai-toolkit research "machine learning trends 2024"
    """
    print(f"\n[bold]Web Research: {query}[/bold]")
    
    tool = WebResearchTool()
    result = tool.execute(query=query, max_results=max_results)
    
    if result.success:
        print(f"\n[green]✅ Found {result.metadata.get('result_count', 0)} results[/green]")
        for i, item in enumerate(result.data, 1):
            print(f"\n[cyan][{i}] {item['title']}[/cyan]")
            print(f"    URL: {item['url']}")
            print(f"    {item['snippet'][:100]}...")
    else:
        print(f"[red]❌ Error: {result.error}[/red]")


def research_extract(url: str):
    """
    Extract content from a URL after web research.
    
    Example: ai-toolkit research-extract "https://example.com/article"
    """
    print(f"\n[bold]Extracting content from: {url}[/bold]")
    
    tool = WebResearchTool()
    result = tool.extract_content(url)
    
    if result.success:
        data = result.data
        print(f"\n[green]✅ Content extracted[/green]")
        print(f"Title: {data['title']}")
        print(f"Content length: {data['content_length']} characters\n")
        print(f"Preview:\n{data['content'][:500]}...")
    else:
        print(f"[red]❌ Error: {result.error}[/red]")


def tools_list():
    """List all available tools."""
    manager = ToolManager()
    manager.register_tool(WebResearchTool())
    
    print("\n[bold]Available Tools:[/bold]")
    table = Table()
    table.add_column("Tool Name", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Version", style="yellow")
    
    for tool_info in manager.list_tools():
        table.add_row(
            tool_info["name"],
            tool_info["description"],
            tool_info["version"]
        )
    
    print(table)


def tools_info(tool_name: str):
    """Get detailed information about a tool."""
    manager = ToolManager()
    manager.register_tool(WebResearchTool())
    
    tool = manager.get_tool(tool_name)
    if tool:
        info = tool.get_info()
        print(f"\n[bold]{tool_name}[/bold]")
        print(f"Description: {info['description']}")
        print(f"Version: {info['version']}")
        if info['metadata']:
            print(f"Metadata: {json.dumps(info['metadata'], indent=2)}")
    else:
        print(f"[red]Tool '{tool_name}' not found[/red]")
