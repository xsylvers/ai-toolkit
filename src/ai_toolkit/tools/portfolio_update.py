from pathlib import Path
import subprocess
import yaml


class PortfolioUpdateTool:
    def __init__(self, site_repo_path: str):
        self.site_repo = Path(site_repo_path).resolve()
        self.content_file = self.site_repo / "content.yml"

    def update_tagline(self, new_tagline: str) -> dict:
        if not self.site_repo.exists():
            return {"success": False, "error": f"Site repo not found: {self.site_repo}"}

        if not self.content_file.exists():
            return {"success": False, "error": f"content.yml not found: {self.content_file}"}

        with open(self.content_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if "tagline" in data:
            data["tagline"] = new_tagline
        elif "hero" in data and isinstance(data["hero"], dict) and "tagline" in data["hero"]:
            data["hero"]["tagline"] = new_tagline
        elif "bio" in data:
            data["bio"] = new_tagline
        else:
            data["tagline"] = new_tagline

        with open(self.content_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

        return {
            "success": True,
            "message": f"Updated content.yml with new tagline: {new_tagline}",
            "content_file": str(self.content_file),
        }

    def git_commit_and_push(
        self, commit_message: str = "Update portfolio content via AI toolkit"
    ) -> dict:
        try:
            subprocess.run(["git", "add", "."], cwd=self.site_repo, check=True)
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.site_repo, check=True)
            subprocess.run(["git", "push"], cwd=self.site_repo, check=True)

            return {"success": True, "message": "Changes committed and pushed successfully."}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"Git command failed: {e}"}