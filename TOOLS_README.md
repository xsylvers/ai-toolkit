# AI Toolkit Tools Library

A reusable, agentic tool library for building intelligent applications. Designed to be used across multiple projects with consistent interfaces and document management.

## Overview

The AI Toolkit provides:
- **AgenticTool Base Class**: Template for building tools
- **WebResearchTool**: Search the web and extract content
- **ToolManager**: Orchestrate multiple tools and manage documents
- **Document Library**: Store and retrieve reusable documents

## Core Concepts

### AgenticTool
Base class for all tools. Key features:
- `execute(**kwargs) -> ToolResult`: Run the tool
- `validate_inputs(**kwargs) -> (bool, error)`: Validate params before execution
- Tool metadata and versioning
- Integration with ToolManager

### WebResearchTool
Performs web searches and content extraction.

**Usage:**
```python
from ai_toolkit.tools import WebResearchTool

tool = WebResearchTool()
result = tool.execute(query="AI trends 2024", max_results=5)
if result.success:
    for item in result.data:
        print(f"- {item['title']}: {item['url']}")
```

**Features:**
- Web search with caching
- Content extraction from URLs
- Support for multiple search APIs (SerpAPI, Google Custom Search)
- Placeholder results for demo purposes

**Extract Content:**
```python
result = tool.extract_content("https://example.com/article")
if result.success:
    print(f"Title: {result.data['title']}")
    print(f"Content: {result.data['content']}")
```

### ToolManager
Orchestrate and manage multiple tools.

**Usage:**
```python
from ai_toolkit.tools import ToolManager, WebResearchTool

manager = ToolManager(name="MyManager")
manager.register_tool(WebResearchTool())

# List tools
manager.list_tools()

# Execute tool
result = manager.execute_tool("WebResearchTool", query="Python")

# Store documents
manager.store_document("doc1", {"content": "..."}, metadata={"type": "research"})

# Retrieve documents
doc = manager.retrieve_document("doc1")
```

## CLI Usage

### Research Commands

**Web Search:**
```bash
python -m ai_toolkit research "machine learning"
python -m ai_toolkit research "AI trends 2024" --max-results 10
```

**Extract Content:**
```bash
python -m ai_toolkit research-extract "https://example.com/article"
```

### Tool Management

**List Available Tools:**
```bash
python -m ai_toolkit tools-list
```

**Get Tool Information:**
```bash
python -m ai_toolkit tools-info WebResearchTool
```

## Configuration

### Environment Variables

Set up a `.env` file in your project:

```env
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
SERPAPI_KEY=your_key_here (optional, for real web searches)
```

### API Keys for Web Search

**SerpAPI** (Recommended for web search):
1. Get key from https://serpapi.com
2. Add to `.env`: `SERPAPI_KEY=your_key`

**Google Custom Search**:
1. Get credentials from Google Cloud Console
2. Add to `.env`: `GOOGLE_SEARCH_API_KEY` and `GOOGLE_SEARCH_ENGINE_ID`

## Creating Custom Tools

Extend `AgenticTool` to create custom tools:

```python
from ai_toolkit.tools import AgenticTool, ToolResult

class MyCustomTool(AgenticTool):
    def __init__(self):
        super().__init__(
            name="MyCustomTool",
            description="Does something useful",
            version="1.0.0"
        )
    
    def validate_inputs(self, **kwargs):
        param = kwargs.get("param")
        if not param:
            return False, "param is required"
        return True, None
    
    def execute(self, **kwargs):
        is_valid, error = self.validate_inputs(**kwargs)
        if not is_valid:
            return ToolResult(success=False, data=None, error=error)
        
        # Your tool logic here
        data = {"result": "success"}
        
        return ToolResult(
            success=True,
            data=data,
            metadata={"custom_field": "value"}
        )

# Use in manager
manager = ToolManager()
manager.register_tool(MyCustomTool())
result = manager.execute_tool("MyCustomTool", param="value")
```

## ToolResult

All tools return a `ToolResult` with:
- `success`: Boolean indicating success
- `data`: Actual result data
- `error`: Error message if failed
- `metadata`: Additional info (source, cache status, etc.)
- `timestamp`: When the tool executed

## Document Library

Store and reuse documents across projects:

```python
manager = ToolManager()

# Store a research document
manager.store_document(
    "research_2024", 
    {"findings": "...", "sources": [...]},
    metadata={"date": "2024-01-01", "topic": "AI"}
)

# List all documents
manager.list_documents()

# Retrieve document
doc = manager.retrieve_document("research_2024")

# Get document info
info = manager.get_document_info("research_2024")

# Delete document
manager.delete_document("research_2024")
```

## Execution History

Track tool execution:

```python
# Get last 10 executions
history = manager.get_execution_history(limit=10)

# Get all execution history
all_history = manager.get_execution_history()

# Clear history
manager.clear_history()
```

## Best Practices

1. **Validate Inputs**: Always implement `validate_inputs()` in custom tools
2. **Use Caching**: Enable cache for expensive operations (web searches)
3. **Document Results**: Use metadata in ToolResult for tracking provenance
4. **Organize Documents**: Use meaningful keys and metadata for document library
5. **Error Handling**: Always check `result.success` before accessing `result.data`

## Example: Multi-Project Setup

**Project Structure:**
```
shared-toolkit/           # This toolkit
  src/ai_toolkit/tools/
  
project-a/
  requirements.txt        # Includes ai-toolkit
  my_research.py         # Uses WebResearchTool
  
project-b/
  requirements.txt        # Includes ai-toolkit
  data_analysis.py       # Uses WebResearchTool + custom tools
```

**Usage in Projects:**
```python
# project-a/my_research.py
from ai_toolkit.tools import ToolManager, WebResearchTool

def research_market():
    manager = ToolManager()
    manager.register_tool(WebResearchTool())
    
    result = manager.execute_tool("WebResearchTool", query="market trends")
    
    # Store for reuse in other projects
    manager.store_document("market_research", result.data)
```

## Extending the Toolkit

Future tools to implement:
- **DocumentSearchTool**: Search local documents and files
- **SummarizationTool**: Summarize long documents
- **AnalysisTool**: Analyze and extract insights
- **DataVisualizationTool**: Create visualizations
- **APIIntegrationTool**: Call external APIs
- **DatabaseTool**: Query and store in databases

## Contributing

To add new tools:
1. Create a new file in `src/ai_toolkit/tools/`
2. Extend `AgenticTool` base class
3. Implement `execute()` and `validate_inputs()`
4. Add to `__init__.py`
5. Register in ToolManager
6. Add CLI commands if needed

## Support

For issues or questions, refer to:
- Tool documentation in docstrings
- CLI help: `python -m ai_toolkit --help`
- Example usage: See integration examples below
