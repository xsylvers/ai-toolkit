"""
Advanced Research CLI - Specialized research commands and document management.

Provides high-level research workflows including:
- Multi-topic research campaigns
- Document organization and curation
- Research analysis and reporting
- Project-based research management
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .tools import WebResearchTool, ToolManager


class ResearchProject:
    """Manages a research project with multiple topics and documents."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.topics: List[str] = []
        self.documents: Dict[str, Dict] = {}
        self.metadata = {}
    
    def add_topic(self, topic: str) -> None:
        """Add a research topic."""
        if topic not in self.topics:
            self.topics.append(topic)
    
    def add_document(self, doc_id: str, doc_data: Dict, metadata: Optional[Dict] = None) -> None:
        """Add a document to the project."""
        self.documents[doc_id] = {
            "data": doc_data,
            "metadata": metadata or {},
            "added_at": datetime.now().isoformat()
        }
    
    def to_dict(self) -> Dict:
        """Convert project to dict."""
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "topic_count": len(self.topics),
            "document_count": len(self.documents),
            "topics": self.topics,
            "metadata": self.metadata
        }


class ResearchCampaign:
    """Manages a research campaign across multiple topics."""
    
    def __init__(self, campaign_name: str, topics: List[str]):
        self.campaign_name = campaign_name
        self.topics = topics
        self.results: Dict[str, Any] = {}
        self.created_at = datetime.now().isoformat()
        self.status = "initialized"
    
    def execute(self, tool: WebResearchTool, max_results_per_topic: int = 5) -> Dict[str, Any]:
        """Execute research campaign across all topics."""
        self.status = "running"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task(
                f"[cyan]Researching {len(self.topics)} topics...",
                total=len(self.topics)
            )
            
            for topic in self.topics:
                result = tool.execute(query=topic, max_results=max_results_per_topic)
                self.results[topic] = {
                    "success": result.success,
                    "data": result.data,
                    "timestamp": result.timestamp,
                    "metadata": result.metadata
                }
                progress.update(task, advance=1)
        
        self.status = "completed"
        return self.results
    
    def get_summary(self) -> Dict:
        """Get campaign summary."""
        total_results = sum(
            len(r.get("data", []))
            for r in self.results.values()
            if r.get("success")
        )
        
        return {
            "campaign": self.campaign_name,
            "created_at": self.created_at,
            "topics_researched": len([r for r in self.results.values() if r.get("success")]),
            "total_topics": len(self.topics),
            "total_results": total_results,
            "status": self.status
        }


# =====================================================================
# Research Commands
# =====================================================================

def research_campaign(
    campaign_name: str,
    topics: str,
    max_results: int = 5,
    save: bool = True
):
    """
    Execute a research campaign across multiple topics.
    
    Example: ai-toolkit research-campaign "AI 2024" "AI trends,LLMs,AGI" --max-results 5
    """
    topic_list = [t.strip() for t in topics.split(",")]
    
    print(f"\n[bold cyan]🚀 Research Campaign: {campaign_name}[/bold cyan]")
    print(f"   Topics: {', '.join(topic_list)}")
    print(f"   Results per topic: {max_results}\n")
    
    # Create campaign
    campaign = ResearchCampaign(campaign_name, topic_list)
    tool = WebResearchTool()
    
    # Execute
    results = campaign.execute(tool, max_results_per_topic=max_results)
    
    # Display results
    print("\n[bold green]✅ Campaign Complete[/bold green]")
    summary = campaign.get_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    # Show results by topic
    print("\n[bold]Results by Topic:[/bold]")
    for topic, result in results.items():
        if result.get("success"):
            print(f"\n   [cyan]{topic}[/cyan] - {len(result.get('data', []))} results")
            for i, item in enumerate(result.get("data", [])[:3], 1):
                print(f"      {i}. {item['title'][:50]}...")
    
    # Save campaign
    if save:
        manager = ToolManager(name="ResearchCampaignManager")
        manager.store_document(
            f"campaign_{campaign_name.replace(' ', '_')}",
            results,
            metadata=summary
        )
        print(f"\n[green]💾 Campaign saved to library[/green]")


def research_deep_dive(
    topic: str,
    max_results: int = 10,
    extract_content: bool = False
):
    """
    Deep dive into a single topic with optional content extraction.
    
    Example: ai-toolkit research-deep-dive "quantum computing" --max-results 10 --extract-content
    """
    print(f"\n[bold cyan]🔍 Deep Dive: {topic}[/bold cyan]\n")
    
    tool = WebResearchTool()
    manager = ToolManager(name="DeepDiveManager")
    
    # Search
    print("[yellow]Searching for sources...[/yellow]")
    search_result = tool.execute(query=topic, max_results=max_results)
    
    if not search_result.success:
        print(f"[red]❌ Search failed: {search_result.error}[/red]")
        return
    
    print(f"[green]✅ Found {len(search_result.data)} sources[/green]\n")
    
    # Display and optionally extract
    extracted_docs = []
    
    for i, item in enumerate(search_result.data[:max_results], 1):
        print(f"[cyan][{i}] {item['title']}[/cyan]")
        print(f"    URL: {item['url']}")
        print(f"    {item['snippet'][:100]}...\n")
        
        # Extract content if requested
        if extract_content:
            print(f"    [yellow]Extracting content...[/yellow]")
            extract_result = tool.extract_content(item['url'])
            
            if extract_result.success:
                doc = extract_result.data
                extracted_docs.append({
                    "title": doc['title'],
                    "url": item['url'],
                    "content": doc['content'],
                    "extracted_at": extract_result.timestamp
                })
                print(f"    [green]✓ Content extracted ({doc['content_length']} chars)[/green]\n")
            else:
                print(f"    [yellow]⚠ Could not extract content[/yellow]\n")
    
    # Store results
    manager.store_document(
        f"deepdive_{topic.replace(' ', '_')}",
        {
            "topic": topic,
            "search_results": search_result.data,
            "extracted_documents": extracted_docs
        },
        metadata={
            "total_sources": len(search_result.data),
            "extracted_count": len(extracted_docs),
            "timestamp": search_result.timestamp
        }
    )
    
    print(f"[green]💾 Deep dive saved ({len(extracted_docs)} documents extracted)[/green]")


def research_compare(topic1: str, topic2: str, max_results: int = 5):
    """
    Compare research on two topics side-by-side.
    
    Example: ai-toolkit research-compare "AI" "Machine Learning" --max-results 5
    """
    print(f"\n[bold cyan]⚖️  Comparing: {topic1} vs {topic2}[/bold cyan]\n")
    
    tool = WebResearchTool()
    
    # Research both topics
    print("[yellow]Researching both topics...[/yellow]")
    result1 = tool.execute(query=topic1, max_results=max_results)
    result2 = tool.execute(query=topic2, max_results=max_results)
    
    if not (result1.success and result2.success):
        print("[red]❌ Research failed[/red]")
        return
    
    # Display comparison
    table = Table(title=f"Comparison: {topic1} vs {topic2}")
    table.add_column(topic1, style="cyan", width=40)
    table.add_column(topic2, style="magenta", width=40)
    
    max_rows = max(len(result1.data), len(result2.data))
    
    for i in range(max_rows):
        item1 = result1.data[i]['title'] if i < len(result1.data) else ""
        item2 = result2.data[i]['title'] if i < len(result2.data) else ""
        table.add_row(item1[:40], item2[:40])
    
    print(table)
    
    # Store comparison
    manager = ToolManager(name="ComparisonManager")
    manager.store_document(
        f"comparison_{topic1.replace(' ', '_')}_vs_{topic2.replace(' ', '_')}",
        {
            "topic1": topic1,
            "topic2": topic2,
            "results1": result1.data,
            "results2": result2.data
        },
        metadata={
            "results_count_1": len(result1.data),
            "results_count_2": len(result2.data)
        }
    )
    
    print(f"\n[green]💾 Comparison saved[/green]")


# =====================================================================
# Document Management Commands
# =====================================================================

def library_list(filter_type: Optional[str] = None):
    """
    List all documents in the research library.
    
    Example: ai-toolkit library-list
    """
    manager = ToolManager(name="LibraryBrowser")
    documents = manager.list_documents()
    
    if not documents:
        print("[yellow]No documents in library[/yellow]")
        return
    
    print(f"\n[bold cyan]📚 Research Library ({len(documents)} documents)[/bold cyan]\n")
    
    table = Table()
    table.add_column("Document ID", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Size", style="yellow")
    
    for doc_id in documents:
        info = manager.get_document_info(doc_id)
        doc_type = info['metadata'].get('type', 'research')
        size = f"{info['content_length']} chars"
        table.add_row(doc_id, doc_type, size)
    
    print(table)


def library_search(query: str):
    """
    Search the research library by document ID.
    
    Example: ai-toolkit library-search "quantum"
    """
    manager = ToolManager(name="LibraryBrowser")
    documents = manager.list_documents()
    
    matches = [d for d in documents if query.lower() in d.lower()]
    
    if not matches:
        print(f"[yellow]No documents matching '{query}'[/yellow]")
        return
    
    print(f"\n[bold cyan]🔍 Search Results: {len(matches)} matches[/bold cyan]\n")
    
    for doc_id in matches:
        info = manager.get_document_info(doc_id)
        print(f"[cyan]{doc_id}[/cyan]")
        print(f"   Stored: {info['stored_at']}")
        print(f"   Size: {info['content_length']} chars")
        if info['metadata']:
            print(f"   Meta: {info['metadata']}\n")


def library_export(doc_id: str, output_file: str):
    """
    Export a document from library to file.
    
    Example: ai-toolkit library-export "campaign_AI_2024" "research.json"
    """
    manager = ToolManager(name="LibraryBrowser")
    doc = manager.retrieve_document(doc_id)
    
    if not doc:
        print(f"[red]❌ Document '{doc_id}' not found[/red]")
        return
    
    try:
        with open(output_file, 'w') as f:
            json.dump(doc, f, indent=2)
        print(f"[green]✅ Exported to {output_file}[/green]")
    except Exception as e:
        print(f"[red]❌ Export failed: {str(e)}[/red]")


def library_import(input_file: str, doc_id: str, metadata: Optional[str] = None):
    """
    Import a document into library from file.
    
    Example: ai-toolkit library-import "research.json" "my_study"
    """
    try:
        with open(input_file, 'r') as f:
            doc = json.load(f)
        
        meta = {}
        if metadata:
            meta = json.loads(metadata)
        
        manager = ToolManager(name="LibraryImporter")
        manager.store_document(doc_id, doc, metadata=meta)
        
        print(f"[green]✅ Imported as '{doc_id}'[/green]")
    except Exception as e:
        print(f"[red]❌ Import failed: {str(e)}[/red]")


def library_delete(doc_id: str, confirm: bool = False):
    """
    Delete a document from library.
    
    Example: ai-toolkit library-delete "old_doc" --confirm
    """
    if not confirm:
        print("[yellow]Use --confirm to delete[/yellow]")
        return
    
    manager = ToolManager(name="LibraryBrowser")
    if manager.delete_document(doc_id):
        print(f"[green]✅ Deleted '{doc_id}'[/green]")
    else:
        print(f"[red]❌ Document not found[/red]")


# =====================================================================
# Reporting Commands
# =====================================================================

def research_report(campaign_id: str, output_format: str = "text"):
    """
    Generate a research report from campaign or deep dive.
    
    Example: ai-toolkit research-report "campaign_AI_2024" --output-format text
    """
    manager = ToolManager(name="ReportGenerator")
    doc = manager.retrieve_document(campaign_id)
    
    if not doc:
        print(f"[red]❌ Document '{campaign_id}' not found[/red]")
        return
    
    print(f"\n[bold cyan]📊 Research Report: {campaign_id}[/bold cyan]\n")
    
    if output_format == "text":
        print("[bold]Document Contents:[/bold]")
        
        if isinstance(doc, dict):
            for key, value in doc.items():
                if key == "data" or isinstance(value, list) and len(str(value)) > 200:
                    print(f"  {key}: {len(str(value))} characters")
                else:
                    print(f"  {key}: {value}")
    
    elif output_format == "json":
        print(json.dumps(doc, indent=2))
    
    print(f"\n[green]✅ Report generated[/green]")


def research_stats():
    """
    Display statistics about research library and usage.
    
    Example: ai-toolkit research-stats
    """
    manager = ToolManager(name="StatisticsCollector")
    
    docs = manager.list_documents()
    info = manager.get_info()
    
    print("\n[bold cyan]📈 Research Statistics[/bold cyan]\n")
    
    panel_content = f"""
[cyan]Documents:[/cyan] {len(docs)}
[cyan]Tool Executions:[/cyan] {info['execution_count']}
[cyan]Total Storage:[/cyan] ~{sum(manager.get_document_info(d)['content_length'] for d in docs)} characters
[cyan]Registered Tools:[/cyan] {info['total_tools']}
"""
    
    print(Panel(panel_content, title="Library Statistics"))
    
    if docs:
        print("\n[bold]Top Documents:[/bold]")
        doc_sizes = [
            (d, manager.get_document_info(d)['content_length'])
            for d in docs
        ]
        doc_sizes.sort(key=lambda x: x[1], reverse=True)
        
        for doc_id, size in doc_sizes[:5]:
            print(f"   • {doc_id}: {size} chars")


# =====================================================================
# Project Management Commands
# =====================================================================

def project_create(project_name: str, description: str = ""):
    """
    Create a new research project.
    
    Example: ai-toolkit project-create "AI Study 2024" "Research on AI trends"
    """
    project = ResearchProject(project_name, description)
    
    manager = ToolManager(name="ProjectManager")
    manager.store_document(
        f"project_{project_name.replace(' ', '_')}",
        project.to_dict(),
        metadata={"type": "project", "created_at": project.created_at}
    )
    
    print(f"[green]✅ Project '{project_name}' created[/green]")


def project_list():
    """
    List all research projects.
    
    Example: ai-toolkit project-list
    """
    manager = ToolManager(name="ProjectManager")
    documents = manager.list_documents()
    
    projects = [d for d in documents if d.startswith("project_")]
    
    if not projects:
        print("[yellow]No projects found[/yellow]")
        return
    
    print(f"\n[bold cyan]📁 Research Projects ({len(projects)})[/bold cyan]\n")
    
    table = Table()
    table.add_column("Project", style="cyan")
    table.add_column("Created", style="yellow")
    table.add_column("Topics", style="green")
    
    for proj_id in projects:
        info = manager.get_document_info(proj_id)
        print(f"   • {proj_id.replace('project_', '').replace('_', ' ')}")
