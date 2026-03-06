# Integration Guide: Using AI Toolkit in Other Projects

This guide explains how to integrate the AI Toolkit library into your other projects (Assignment 1 and beyond).

## Quick Integration

### Step 1: Install AI Toolkit

Add to your project's `requirements.txt`:
```
ai-toolkit @ file://../ai-toolkit
```

Or install directly:
```bash
pip install -e ../ai-toolkit
```

### Step 2: Set Environment Variables

Create `.env` in your project root:
```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
SERPAPI_KEY=your_key  # Optional, for real web searches
```

### Step 3: Use in Your Code

```python
from ai_toolkit.tools import WebResearchTool, ToolManager
from ai_toolkit.research_cli import ResearchCampaign

# Simple search
tool = WebResearchTool()
result = tool.execute(query="your topic")

# Campaign research
campaign = ResearchCampaign("My Research", ["topic1", "topic2"])
results = campaign.execute(tool)

# Manage documents
manager = ToolManager()
manager.store_document("key", data)
```

## Real-World Integration Scenarios

### Scenario 1: Assignment 1 Integration

**Use Case**: Enhance your C# assignment with research capabilities

```csharp
// In C#, call Python toolkit via subprocess or API
Process.Start("python", "-m ai_toolkit research \"your query\"");
```

Or create a wrapper:

```python
# research_wrapper.py - to be called from C#
import sys
from ai_toolkit.tools import WebResearchTool

if __name__ == "__main__":
    query = sys.argv[1]
    tool = WebResearchTool()
    result = tool.execute(query=query)
    
    if result.success:
        for item in result.data:
            print(f"{item['title']}|{item['url']}")
```

### Scenario 2: Data Analysis Project

```python
from ai_toolkit.tools import ToolManager, WebResearchTool

class ResearchAnalyzer:
    def __init__(self):
        self.manager = ToolManager()
        self.tool = WebResearchTool()
    
    def research_and_analyze(self, topics):
        """Research topics and store for analysis."""
        analyses = {}
        
        for topic in topics:
            result = self.tool.execute(query=topic)
            
            # Store for later use
            self.manager.store_document(
                f"analysis_{topic}",
                result.data,
                metadata={"analysis_type": "web_research"}
            )
            
            analyses[topic] = result.data
        
        return analyses
    
    def export_for_further_analysis(self, filename):
        """Export all research for external tools."""
        docs = {}
        for doc_id in self.manager.list_documents():
            docs[doc_id] = self.manager.retrieve_document(doc_id)
        
        import json
        with open(filename, 'w') as f:
            json.dump(docs, f, indent=2)
```

### Scenario 3: Content Generation

```python
from ai_toolkit.research_cli import ResearchCampaign
from ai_toolkit.tools import WebResearchTool

def generate_article(topic):
    """Research a topic and prepare content outline."""
    
    tool = WebResearchTool()
    
    # Deep dive research
    search_result = tool.execute(query=topic, max_results=5)
    
    # Extract key sources
    sources = []
    for i, item in enumerate(search_result.data[:3]):
        extract = tool.extract_content(item['url'])
        if extract.success:
            sources.append({
                "title": item['title'],
                "url": item['url'],
                "excerpt": extract.data['content'][:300]
            })
    
    # Structure for content generation
    article_outline = {
        "topic": topic,
        "sources": sources,
        "outline": generate_outline(sources)
    }
    
    return article_outline

def generate_outline(sources):
    """Generate article outline from sources."""
    return {
        "introduction": "Could be written from sources",
        "main_points": len(sources),
        "conclusion": "Summary of findings",
        "references": sources
    }
```

### Scenario 4: Competitive Intelligence

```python
from ai_toolkit.research_cli import ResearchCampaign
from ai_toolkit.tools import ToolManager

class CompetitiveIntelligence:
    def __init__(self):
        self.manager = ToolManager()
        self.campaign_results = {}
    
    def analyze_company(self, company_name, areas):
        """Analyze a company across multiple areas."""
        content_areas = [
            f"{company_name} {area}"
            for area in areas
        ]
        
        campaign = ResearchCampaign(
            f"{company_name} Analysis",
            content_areas
        )
        
        from ai_toolkit.tools import WebResearchTool
        results = campaign.execute(WebResearchTool())
        
        self.campaign_results[company_name] = results
        
        # Store for later access
        self.manager.store_document(
            f"competitive_{company_name}",
            results,
            metadata={"type": "competitive_analysis"}
        )
        
        return results
    
    def compare_companies(self, company1, company2, area):
        """Compare two companies in an area."""
        tool = WebResearchTool()
        
        result1 = tool.execute(query=f"{company1} {area}")
        result2 = tool.execute(query=f"{company2} {area}")
        
        return {
            "company1": {
                "name": company1,
                "results": result1.data
            },
            "company2": {
                "name": company2,
                "results": result2.data
            }
        }
```

### Scenario 5: Learning & Documentation

```python
from ai_toolkit.research_cli import ResearchProject
from ai_toolkit.tools import WebResearchTool, ToolManager

class LearningPath:
    def __init__(self, topic):
        self.topic = topic
        self.project = ResearchProject(topic, f"Learning path for {topic}")
        self.manager = ToolManager()
        self.tool = WebResearchTool()
    
    def build_learning_path(self, subtopics):
        """Build structured learning materials."""
        
        for i, subtopic in enumerate(subtopics, 1):
            print(f"Learning Module {i}: {subtopic}")
            
            # Research each subtopic
            result = self.tool.execute(query=f"{self.topic} {subtopic}")
            
            # Store with clear structure
            self.manager.store_document(
                f"learning_{self.topic}_{i}_{subtopic}",
                {
                    "module": i,
                    "subtopic": subtopic,
                    "resources": result.data
                },
                metadata={
                    "learning_path": self.topic,
                    "sequence": i
                }
            )
            
            self.project.add_topic(subtopic)
    
    def export_learning_materials(self, output_dir):
        """Export all learning materials."""
        import os
        import json
        
        os.makedirs(output_dir, exist_ok=True)
        
        for doc_id in self.manager.list_documents():
            doc = self.manager.retrieve_document(doc_id)
            filename = os.path.join(output_dir, f"{doc_id}.json")
            
            with open(filename, 'w') as f:
                json.dump(doc, f, indent=2)
```

## Project Structure with AI Toolkit

```
my-project/
├── requirements.txt           # Includes ai-toolkit
├── .env                       # API keys
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── research/
│   │   ├── __init__.py
│   │   ├── researcher.py      # Uses WebResearchTool
│   │   └── campaigns.py       # Uses ResearchCampaign
│   └── analysis/
│       ├── __init__.py
│       └── analyzer.py        # Analyzes research data
├── data/
│   ├── research/              # Stored research documents
│   └── exports/               # Exported JSON files
└── tests/
    └── test_research.py       # Test research integration
```

## Testing Research Integration

```python
import pytest
from ai_toolkit.tools import WebResearchTool, ToolManager

def test_web_research():
    tool = WebResearchTool()
    result = tool.execute(query="test")
    
    assert result.success
    assert result.data is not None
    assert len(result.data) > 0

def test_tool_manager():
    manager = ToolManager()
    manager.register_tool(WebResearchTool())
    
    result = manager.execute_tool("WebResearchTool", query="test")
    
    assert result.success

def test_document_storage():
    manager = ToolManager()
    test_doc = {"test": "data"}
    
    manager.store_document("test_doc", test_doc)
    retrieved = manager.retrieve_document("test_doc")
    
    assert retrieved == test_doc
```

## Common Patterns

### Pattern 1: Research Once, Use Many Times

```python
manager = ToolManager()

# Research
result = tool.execute(query="important topic")

# Store for reuse
manager.store_document("reusable_research", result.data)

# Use in multiple places
data = manager.retrieve_document("reusable_research")
# Use in analysis
# Use in reporting
# Use in exports
```

### Pattern 2: Batch Research with Error Handling

```python
def batch_research(queries):
    tool = WebResearchTool()
    manager = ToolManager()
    
    results = {}
    errors = []
    
    for query in queries:
        try:
            result = tool.execute(query=query)
            if result.success:
                manager.store_document(f"batch_{query}", result.data)
                results[query] = result.data
            else:
                errors.append(f"{query}: {result.error}")
        except Exception as e:
            errors.append(f"{query}: {str(e)}")
    
    return results, errors
```

### Pattern 3: Research Lifecycle

```python
class ResearchLifecycle:
    def __init__(self, topic):
        self.topic = topic
        self.manager = ToolManager()
        
    def discover(self):
        """Initial broad research."""
        tool = WebResearchTool()
        result = tool.execute(query=self.topic)
        self.manager.store_document(f"{self.topic}_discover", result.data)
        return result
    
    def deep_dive(self):
        """Detailed research with extraction."""
        tool = WebResearchTool()
        search = tool.execute(query=self.topic, max_results=10)
        
        extracted = []
        for item in search.data[:5]:
            content = tool.extract_content(item['url'])
            if content.success:
                extracted.append(content.data)
        
        self.manager.store_document(f"{self.topic}_deepdive", extracted)
        return extracted
    
    def analyze(self):
        """Analyze collected research."""
        discover_data = self.manager.retrieve_document(f"{self.topic}_discover")
        deepdive_data = self.manager.retrieve_document(f"{self.topic}_deepdive")
        
        # Combine and analyze
        analysis = {
            "sources": len(discover_data),
            "extracted": len(deepdive_data),
            "summary": self.generate_summary(discover_data, deepdive_data)
        }
        
        return analysis
    
    def export(self, filename):
        """Export final research."""
        analysis = self.analyze()
        import json
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
```

## Performance Tips

1. **Cache Searches**: Enable caching (default) to avoid duplicate searches
2. **Batch Operations**: Research multiple topics at once using campaigns
3. **Lazy Loading**: Only extract content when needed
4. **Clean Storage**: Regularly delete old documents to manage memory
5. **Export Archives**: Export and delete old campaigns to archive

## Troubleshooting Integration

### Import Errors
```bash
# Reinstall ai-toolkit in development mode
pip install -e ../ai-toolkit
```

### Missing Environment Variables
```python
from dotenv import load_dotenv
load_dotenv()  # Load from .env
```

### Storage Issues
```python
# Check what's stored
docs = manager.list_documents()
print(f"Stored: {len(docs)} documents")

# Delete unused docs
for doc in docs:
    manager.delete_document(doc)
```

## Next Steps

1. **Try Basic Integration**: Start with simple web search in your project
2. **Add Research Workflows**: Implement research campaigns for your use case
3. **Build Custom Tools**: Extend AgenticTool for domain-specific tools
4. **Create Pipelines**: Chain multiple tools together
5. **Automate Research**: Schedule research tasks

## Support

- **CLI Help**: `python -m ai_toolkit --help`
- **Documentation**: See QUICKSTART.md and TOOLS_README.md
- **Examples**: Run examples.py and research_examples.py
- **Issues**: Check error messages in result.error
