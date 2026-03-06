# AI Toolkit - Quick Reference

## Installation
```bash
cd ai-toolkit
pip install -e .
```

## Environment Setup
Create `.env`:
```env
OPENAI_API_KEY=key
GEMINI_API_KEY=key
SERPAPI_KEY=key  # Optional, for real searches
```

## Most Common Commands

### Research
```bash
# Basic search
ai-toolkit research "your topic"

# Extract content
ai-toolkit research-extract "url"

# Multi-topic campaign
ai-toolkit research-campaign "Name" "topic1,topic2,topic3"

# Deep dive with extraction
ai-toolkit research-deep-dive "topic" --extract-content

# Compare topics
ai-toolkit research-compare "topic1" "topic2"
```

### Library
```bash
# List all research
ai-toolkit library-list

# Search documents
ai-toolkit library-search "query"

# Export
ai-toolkit library-export "doc_id" "file.json"

# Import
ai-toolkit library-import "file.json" "doc_id"

# Delete
ai-toolkit library-delete "doc_id" --confirm
```

### Reporting
```bash
# Statistics
ai-toolkit research-stats

# Generate report
ai-toolkit research-report "doc_id"
```

## Python API Quick Start

### Search
```python
from ai_toolkit.tools import WebResearchTool

tool = WebResearchTool()
result = tool.execute(query="topic", max_results=5)

if result.success:
    for item in result.data:
        print(f"{item['title']}: {item['url']}")
```

### Campaign
```python
from ai_toolkit.research_cli import ResearchCampaign

campaign = ResearchCampaign("Name", ["topic1", "topic2"])
results = campaign.execute(tool)
```

### Storage
```python
from ai_toolkit.tools import ToolManager

manager = ToolManager()
manager.store_document("key", data)
doc = manager.retrieve_document("key")
```

### Extract Content
```python
result = tool.extract_content("https://example.com")
if result.success:
    print(result.data['content'])
```

## File Locations

| What | Where |
|------|-------|
| Source Code | `src/ai_toolkit/` |
| Tools | `src/ai_toolkit/tools/` |
| CLI Commands | `src/ai_toolkit/cli.py` |
| Research CLI | `src/ai_toolkit/research_cli.py` |
| Docs | Root directory (*.md files) |
| Examples | `examples.py`, `research_examples.py` |
| Data/Library | `data/library/` |

## Documentation Map

- **QUICKSTART.md** → Getting started
- **TOOLS_README.md** → Complete API reference
- **RESEARCH_CLI.md** → Advanced commands
- **INTEGRATION_GUIDE.md** → Use in other projects
- **BUILD_SUMMARY.md** → What was built
- **This file** → Quick reference

## Common Workflows

### Workflow 1: Quick Research
```bash
ai-toolkit research "machine learning"
```

### Workflow 2: Comprehensive Study
```bash
ai-toolkit research-deep-dive "machine learning" --extract-content
ai-toolkit research-compare "ML" "Deep Learning"
ai-toolkit library-export "deepdive_machine_learning" "study.json"
```

### Workflow 3: Multi-Topic Campaign
```bash
ai-toolkit research-campaign "AI 2024" "AI,LLM,AGI,AI-safety" --max-results 10
ai-toolkit research-stats
ai-toolkit library-list
```

### Workflow 4: Export Research
```bash
# Do research...
ai-toolkit research-campaign "Study" "topic1,topic2"

# Find ID
ai-toolkit library-search "Study"

# Export
ai-toolkit library-export "campaign_Study" "study.json"
```

### Workflow 5: In Python
```python
from ai_toolkit.tools import WebResearchTool, ToolManager

manager = ToolManager()

# Research
tool = WebResearchTool()
for topic in ["AI", "ML", "DL"]:
    result = tool.execute(query=topic)
    manager.store_document(f"research_{topic}", result.data)

# Use later
doc = manager.retrieve_document("research_AI")
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Import error | `pip install -e .` in ai-toolkit root |
| API key missing | Create `.env` with keys |
| No web results | Results are placeholder until SERPAPI_KEY set |
| Content extraction fails | Install: `pip install requests beautifulsoup4` |
| Memory usage high | Run: `ai-toolkit library-delete <id> --confirm` |

## Performance Tips

1. Use `--max-results` to limit searches
2. Don't extract unless needed
3. Campaigns search all topics in parallel
4. Results are cached by default
5. Export old research and delete to save memory

## Getting Help

```bash
# General help
ai-toolkit --help

# Command help
ai-toolkit research --help
ai-toolkit research-campaign --help

# Run examples
python examples.py
python research_examples.py
```

## Typical Project Setup

```python
# myproject/research.py

from pathlib import Path
from dotenv import load_dotenv
from ai_toolkit.tools import WebResearchTool, ToolManager

load_dotenv()

class ResearchManager:
    def __init__(self):
        self.tool = WebResearchTool()
        self.manager = ToolManager()
    
    def research(self, topic: str):
        result = self.tool.execute(query=topic)
        self.manager.store_document(
            f"research_{topic}",
            result.data,
            metadata={"topic": topic}
        )
        return result
    
    def get_research(self, topic: str):
        return self.manager.retrieve_document(f"research_{topic}")

# Usage
if __name__ == "__main__":
    rm = ResearchManager()
    
    # Research
    rm.research("machine learning")
    
    # Use
    data = rm.get_research("machine learning")
    print(f"Found {len(data)} results")
```

## What's Different From Before

Before (basic web search only):
- Just WebResearchTool
- Basic CLI (research, research-extract)
- No document management

After (full agentic system):
- WebResearchTool + framework for more tools
- Advanced CLI with campaigns, comparisons, projects
- Complete document library with export/import
- Execution history and statistics
- Project organization
- Multiple research workflows

## Next: Custom Tools

To add your own tool:

```python
from ai_toolkit.tools import AgenticTool, ToolResult

class MyTool(AgenticTool):
    def __init__(self):
        super().__init__("MyTool", "Description")
    
    def validate_inputs(self, **kwargs):
        return True, None
    
    def execute(self, **kwargs):
        return ToolResult(success=True, data={"result": "value"})

# Register and use
manager.register_tool(MyTool())
result = manager.execute_tool("MyTool")
```

## CLI Syntax

```
ai-toolkit [command] [args] [--flags]

Examples:
ai-toolkit doctor
ai-toolkit research "query"
ai-toolkit research-campaign "name" "topic1,topic2"
ai-toolkit library-list
ai-toolkit research-stats
```

## Quick Debug

```bash
# Check setup
ai-toolkit doctor

# See what's stored
ai-toolkit library-list

# See stats
ai-toolkit research-stats

# Test search
ai-toolkit research "test"
```

## Remember

- ✅ All commands are CLI + Python API
- ✅ Results are cached by default
- ✅ Documents stored in `data/library/`
- ✅ Export documents as JSON anytime
- ✅ New tools follow AgenticTool pattern
- ✅ Manager orchestrates everything
- ✅ Metadata tracked automatically
- ✅ Full error handling included
