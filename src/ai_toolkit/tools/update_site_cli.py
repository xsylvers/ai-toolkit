import typer
from pathlib import Path
from rich import print

from ai_toolkit.tools.portfolio_update import PortfolioUpdateTool

app = typer.Typer(help="Website automation tools")

SITE_REPO_PATH = Path("../xaviersylvers.github.io").resolve()


@app.command("update-site")
def update_site(new_text: str):
    """
    Update the website tagline and push changes.
    """

    print(f"[cyan]Using site repo:[/cyan] {SITE_REPO_PATH}")

    tool = PortfolioUpdateTool(str(SITE_REPO_PATH))

    result = tool.update_tagline(new_text)

    if not result["success"]:
        print(f"[red]Error:[/red] {result['error']}")
        raise typer.Exit()

    print("[green]Content updated[/green]")

    git_result = tool.git_commit_and_push()

    if not git_result["success"]:
        print(f"[red]Git error:[/red] {git_result['error']}")
        raise typer.Exit()

    print("[bold green]Website updated successfully[/bold green]")