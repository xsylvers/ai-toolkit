import typer
from .cli import doctor, research, research_extract, tools_list, tools_info
from . import research_cli

app = typer.Typer(help="AI Toolkit - Agentic tools for research and document management")

# Build/Setup commands
app.command("doctor")(doctor)

# Basic Research commands
app.command("research")(research)
app.command("research-extract")(research_extract)

# Advanced Research commands
app.command("research-campaign")(research_cli.research_campaign)
app.command("research-deep-dive")(research_cli.research_deep_dive)
app.command("research-compare")(research_cli.research_compare)

# Document Library Management
app.command("library-list")(research_cli.library_list)
app.command("library-search")(research_cli.library_search)
app.command("library-export")(research_cli.library_export)
app.command("library-import")(research_cli.library_import)
app.command("library-delete")(research_cli.library_delete)

# Reporting commands
app.command("research-report")(research_cli.research_report)
app.command("research-stats")(research_cli.research_stats)

# Project Management commands
app.command("project-create")(research_cli.project_create)
app.command("project-list")(research_cli.project_list)

# Tool Management commands
app.command("tools-list")(tools_list)
app.command("tools-info")(tools_info)

if __name__ == "__main__":
    app()
