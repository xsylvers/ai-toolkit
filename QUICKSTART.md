# AI Toolkit - Quick Start for Projects

## Setup

### 1. Add to Your Project

**Install from your workspace:**
```bash
# In your project directory
pip install -e ../path/to/ai-toolkit
```

Or add to `requirements.txt`:
```
ai-toolkit @ file://<path-to-ai-toolkit>
```

### 2. Set Environment Variables

Create a `.env` file in your project root:
```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
SERPAPI_KEY=your_key_for_web_search  # Optional but recommended
```

### 3. Minimal Example

```python
from ai_toolkit.tools import WebResearchTool

# Create tool
tool = WebResearchTool()

# Execute research
result = tool.execute(query="your research topic")

# Check results
if result.success:
    for item in result.data:
        print(f"Title: {item['title']}")
        print(f"URL: {item['url']}")
        print(f"Summary: {item['snippet']}\n")
else:
    print(f"Error: {result.error}")
```

## Common Use Cases

### Use Case 1: Gather Research for a Report

```python
from ai_toolkit.tools import ToolManager, WebResearchTool

manager = ToolManager()
manager.register_tool(WebResearchTool())

# Research multiple topics
topics = ["AI trends", "cloud computing", "web3"]

for topic in topics:
    result = manager.execute_tool("WebResearchTool", query=topic)
    manager.store_document(
        f"research_{topic.replace(' ', '_')}",
        result.data,
        metadata={"topic": topic}
    )

# Later, retrieve stored research
docs = manager.list_documents()
print(f"Stored {len(docs)} research documents")
```

### Use Case 2: Research-Driven Application

```python
from ai_toolkit.tools import WebResearchTool

def get_market_insights(company_name: str):
    """Get web-based insights about a company."""
    tool = WebResearchTool()
    
    query = f"{company_name} market analysis trends"
    result = tool.execute(query=query, max_results=5)
    
    return {
        "company": company_name,
        "timestamp": result.timestamp,
        "insights": result.data if result.success else []
    }

# Use in your app
insights = get_market_insights("Tesla")
```

### Use Case 3: Document Extraction Pipeline

```python
from ai_toolkit.tools import WebResearchTool

def extract_documentation(topic: str):
    """Find and extract documentation for a topic."""
    tool = WebResearchTool()
    
    # Search
    search_result = tool.execute(query=f"{topic} documentation")
    
    # Extract content
    extracted = []
    for item in search_result.data[:3]:  # Top 3 results
        content_result = tool.extract_content(item['url'])
        if content_result.success:
            extracted.append({
                "title": item['title'],
                "url": item['url'],
                "content": content_result.data['content']
            })
    
    return extracted

docs = extract_documentation("Python asyncio")
```

## API Reference Quick Guide

### WebResearchTool

**Search:**
```python
result = tool.execute(
    query="search term",
    max_results=5,           # default: 5
    use_cache=True           # default: True
)
```

**Extract:**
```python
result = tool.extract_content("https://example.com")
```

**Cache:**
```python
info = tool.get_cache_info()        # Get cache status
tool.clear_cache()                  # Clear cache
```

### ToolManager

**Register:**
```python
manager.register_tool(tool)
manager.register_tool(tool, override=True)
```

**Execute:**
```python
result = manager.execute_tool("ToolName", param1="value")
```

**Documents:**
```python
manager.store_document(key, content, metadata={})
doc = manager.retrieve_document(key)
manager.list_documents()
manager.delete_document(key)
```

**History:**
```python
history = manager.get_execution_history()     # All
history = manager.get_execution_history(10)   # Last 10
manager.clear_history()
```

## Troubleshooting

### Web Search Returns Placeholder Results
**Solution:** Set `SERPAPI_KEY` in `.env` for real web searches
```env
SERPAPI_KEY=your_actual_key
```

### Content Extraction Fails
**Solution:** Install required library
```bash
pip install beautifulsoup4 requests
```

### Import Errors
**Solution:** Ensure ai-toolkit is installed
```bash
pip install -e <path-to-ai-toolkit>
```

## Best Practices

1. **Always check result.success**
   ```python
   result = tool.execute(...)
   if result.success:
       data = result.data
   else:
       error = result.error
   ```

2. **Use metadata for tracking**
   ```python
   manager.store_document(
       "key",
       data,
       metadata={"source": "web_research", "date": "2024-01-01"}
   )
   ```

3. **Cache expensive operations**
   ```python
   result = tool.execute(query=query, use_cache=True)
   ```

4. **Validate inputs**
   ```python
   is_valid, error = tool.validate_inputs(query=query)
   if not is_valid:
       print(f"Invalid: {error}")
   ```

## Extending for Your Project

Create custom tools by extending `AgenticTool`:

```python
from ai_toolkit.tools import AgenticTool, ToolResult

class MyCustomTool(AgenticTool):
    def __init__(self):
        super().__init__(
            name="MyCustomTool",
            description="My custom tool",
            version="1.0.0"
        )
    
    def validate_inputs(self, **kwargs):
        param = kwargs.get("required_param")
        if not param:
            return False, "required_param is required"
        return True, None
    
    def execute(self, **kwargs):
        is_valid, error = self.validate_inputs(**kwargs)
        if not is_valid:
            return ToolResult(success=False, data=None, error=error)
        
        # Your logic here
        data = {"result": "your_result"}
        
        return ToolResult(
            success=True,
            data=data,
            metadata={"tool_specific": "metadata"}
        )

# Use in your project
manager = ToolManager()
manager.register_tool(MyCustomTool())
result = manager.execute_tool("MyCustomTool", required_param="value")
```

## File Organization for Your Project

Suggested project structure:

```
my-project/
├── requirements.txt
├── .env
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── research.py          # Uses WebResearchTool
│       ├── analysis.py          # Uses custom tools
│       └── tools/               # Custom tools
│
└── data/
    └── research_docs/           # Store retrieved documents
```

## Support

- **CLI Help:** `python -m ai_toolkit --help`
- **Tool Examples:** See [examples.py](../examples.py)
- **Full Documentation:** See [TOOLS_README.md](../TOOLS_README.md)
