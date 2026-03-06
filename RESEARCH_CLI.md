# Advanced Research CLI Documentation

## Overview

The Advanced Research CLI provides powerful commands for conducting, organizing, and reporting on research. It extends the basic web research tool with high-level workflows for:

- **Research Campaigns**: Simultaneously research multiple topics
- **Deep Dives**: Comprehensive research on single topics with content extraction  
- **Comparisons**: Side-by-side comparison of different topics
- **Document Management**: Organize, search, export, and import research
- **Reporting**: Generate reports and statistics
- **Project Management**: Organize research into projects

## Core Concepts

### ResearchCampaign
Executes research across multiple topics simultaneously with progress tracking.

```python
from ai_toolkit.research_cli import ResearchCampaign
from ai_toolkit.tools import WebResearchTool

campaign = ResearchCampaign("AI 2024", ["AI trends", "LLMs", "AGI"])
tool = WebResearchTool()
results = campaign.execute(tool, max_results_per_topic=5)
summary = campaign.get_summary()
```

### ResearchProject
Groups research into projects for organization and tracking.

```python
from ai_toolkit.research_cli import ResearchProject

project = ResearchProject("Tech Research", "Studying emerging technologies")
project.add_topic("AI")
project.add_topic("Blockchain")
```

## Command Reference

### Research Commands

#### `research-campaign`
Execute research across multiple topics simultaneously.

**Syntax:**
```bash
ai-toolkit research-campaign <campaign_name> <topics> [--max-results N] [--save]
```

**Parameters:**
- `campaign_name`: Name of the campaign (e.g., "AI 2024")
- `topics`: Comma-separated list of topics (e.g., "AI,ML,NLP")
- `--max-results`: Results per topic (default: 5)
- `--save`: Save results to library (default: True)

**Examples:**
```bash
# Research top trends across multiple topics
ai-toolkit research-campaign "Tech Trends 2024" "AI,blockchain,quantum computing" --max-results 10

# Quick campaign without saving
ai-toolkit research-campaign "Quick Study" "Python,JavaScript" --save false
```

**Output:**
- Campaign summary with total results
- Results organized by topic
- Top 3 results for each topic
- Auto-saved to library with metadata

---

#### `research-deep-dive`
Deep investigation of a single topic with optional content extraction.

**Syntax:**
```bash
ai-toolkit research-deep-dive <topic> [--max-results N] [--extract-content]
```

**Parameters:**
- `topic`: Topic to research (e.g., "quantum computing")
- `--max-results`: Number of sources to retrieve (default: 10)
- `--extract-content`: Extract full content from pages (default: False)

**Examples:**
```bash
# Deep dive into a topic
ai-toolkit research-deep-dive "artificial general intelligence"

# Deep dive with content extraction
ai-toolkit research-deep-dive "machine learning" --max-results 15 --extract-content

# Extract from more sources
ai-toolkit research-deep-dive "blockchain" --max-results 20 --extract-content
```

**Output:**
- Numbered source list with titles and URLs
- Article snippets
- Extracted content (if requested)
- Saved to library for later access

---

#### `research-compare`
Compare research results between two topics side-by-side.

**Syntax:**
```bash
ai-toolkit research-compare <topic1> <topic2> [--max-results N]
```

**Parameters:**
- `topic1`: First topic to compare
- `topic2`: Second topic to compare
- `--max-results`: Results per topic (default: 5)

**Examples:**
```bash
# Compare two technologies
ai-toolkit research-compare "AI" "Machine Learning"

# Compare with more results
ai-toolkit research-compare "Python" "JavaScript" --max-results 10

# Compare concepts
ai-toolkit research-compare "supervised learning" "unsupervised learning"
```

**Output:**
- Side-by-side table comparison
- Top results for each topic
- Comparison saved with metadata

---

### Library Management Commands

#### `library-list`
List all documents in the research library.

**Syntax:**
```bash
ai-toolkit library-list [--filter-type TYPE]
```

**Examples:**
```bash
ai-toolkit library-list
ai-toolkit library-list --filter-type campaign
```

**Output:**
- Formatted table with document IDs
- Size information
- Document types

---

#### `library-search`
Search for documents in the library by ID.

**Syntax:**
```bash
ai-toolkit library-search <query>
```

**Examples:**
```bash
ai-toolkit library-search "quantum"
ai-toolkit library-search "campaign"
ai-toolkit library-search "2024"
```

**Output:**
- Matching document IDs
- Metadata and storage info

---

#### `library-export`
Export a document from library to a JSON file.

**Syntax:**
```bash
ai-toolkit library-export <doc_id> <output_file>
```

**Examples:**
```bash
ai-toolkit library-export "campaign_AI_2024" "ai_research.json"
ai-toolkit library-export "deepdive_quantum" "quantum_study.json"
```

**Output:**
- Document exported as JSON
- Can be used for external analysis

---

#### `library-import`
Import a previously exported document into library.

**Syntax:**
```bash
ai-toolkit library-import <input_file> <doc_id> [--metadata JSON]
```

**Examples:**
```bash
ai-toolkit library-import "research.json" "imported_study"

# Import with metadata
ai-toolkit library-import "data.json" "my_research" --metadata '{"source": "manual", "date": "2024-01-01"}'
```

**Output:**
- Document imported with specified ID
- Ready for use in other tools

---

#### `library-delete`
Delete a document from the library.

**Syntax:**
```bash
ai-toolkit library-delete <doc_id> [--confirm]
```

**Parameters:**
- `doc_id`: ID of document to delete
- `--confirm`: Confirm deletion (required)

**Examples:**
```bash
ai-toolkit library-delete "old_research" --confirm
```

**Output:**
- Confirmation of deletion

---

### Reporting Commands

#### `research-report`
Generate a report from stored research.

**Syntax:**
```bash
ai-toolkit research-report <campaign_id> [--output-format FORMAT]
```

**Parameters:**
- `campaign_id`: ID of campaign or deep dive
- `--output-format`: text or json (default: text)

**Examples:**
```bash
ai-toolkit research-report "campaign_AI_2024"
ai-toolkit research-report "deepdive_quantum" --output-format json
```

**Output:**
- Formatted report with document contents
- JSON export option available

---

#### `research-stats`
Display library statistics and usage information.

**Syntax:**
```bash
ai-toolkit research-stats
```

**Examples:**
```bash
ai-toolkit research-stats
```

**Output:**
- Total documents count
- Total tool executions
- Storage statistics
- Top documents by size

---

### Project Management Commands

#### `project-create`
Create a new research project.

**Syntax:**
```bash
ai-toolkit project-create <project_name> [--description TEXT]
```

**Examples:**
```bash
ai-toolkit project-create "AI Research 2024"

ai-toolkit project-create "Tech Study" --description "Comprehensive study of emerging technologies"
```

**Output:**
- Project created and added to library

---

#### `project-list`
List all research projects.

**Syntax:**
```bash
ai-toolkit project-list
```

**Examples:**
```bash
ai-toolkit project-list
```

**Output:**
- All projects with creation dates
- Topic counts
- Document references

---

## Workflow Examples

### Example 1: Comprehensive Market Research

```bash
# Create a project
ai-toolkit project-create "Market Analysis Q1 2024"

# Research multiple market segments
ai-toolkit research-campaign "Market Q1" \
  "AI market,cloud computing,web3,cybersecurity" \
  --max-results 10

# Deep dive into top segment
ai-toolkit research-deep-dive "AI market" --max-results 20 --extract-content

# Compare with previous quarter trends
ai-toolkit research-compare "AI market Q1" "AI market Q4" --max-results 10

# Get statistics
ai-toolkit research-stats
```

### Example 2: Competitive Analysis

```bash
# Deep dive into competitor tech
ai-toolkit research-deep-dive "Company A technology" --extract-content

# Compare with your technology
ai-toolkit research-compare "Company A technology" "Our technology" --max-results 15

# Export for report
ai-toolkit library-export "comparison_Company_A_vs_Our" "competitive_report.json"
```

### Example 3: Building a Research Archive

```bash
# Research multiple topics
ai-toolkit research-campaign "Archive 2024" \
  "machine learning,natural language processing,computer vision,robotics" \
  --max-results 8

# Do deep dives on key areas
ai-toolkit research-deep-dive "machine learning advancements" --extract-content
ai-toolkit research-deep-dive "neural networks" --extract-content

# Export complete archive
ai-toolkit library-export "campaign_Archive_2024" "2024_ml_research.json"

# View stats
ai-toolkit research-stats
```

### Example 4: Focused Study with Comparisons

```bash
# Study a topic
ai-toolkit research-deep-dive "quantum computing" --max-results 15 --extract-content

# Compare with related topics
ai-toolkit research-compare "quantum computing" "quantum algorithms"
ai-toolkit research-compare "quantum computing" "classical computing"

# Generate report
ai-toolkit research-report "deepdive_quantum_computing" --output-format json
```

## Data Organization

### Document Structure

Research documents are stored with the following structure:

```
Document ID Format: [type]_[name]
├── campaign_[name]
├── deepdive_[name]
├── comparison_[name1]_vs_[name2]
├── project_[name]
└── extracted_content_[index]
```

### Metadata Tracked

Each document stores metadata including:
- `timestamp`: When research was conducted
- `type`: Document type (campaign, deepdive, etc.)
- `result_count`: Number of results/sources
- `topics`: Topics researched
- `extracted_count`: Number of extracted documents

## Integration with Tools

### Using ToolManager Directly

```python
from ai_toolkit.tools import ToolManager
from ai_toolkit.research_cli import ResearchCampaign
from ai_toolkit.tools import WebResearchTool

# Create manager
manager = ToolManager()
manager.register_tool(WebResearchTool())

# Use research CLI to store data
campaign = ResearchCampaign("My Research", ["topic1", "topic2"])
results = campaign.execute(WebResearchTool())

# Store via manager
manager.store_document("my_campaign", results)

# Retrieve and use
campaign_data = manager.retrieve_document("my_campaign")
```

### Custom Research Workflows

```python
manager = ToolManager(name="CustomWorkflow")

# Execute research
result = manager.execute_tool("WebResearchTool", query="your topic")

# Process results
if result.success:
    # Store with custom metadata
    manager.store_document(
        "processed_results",
        process_data(result.data),
        metadata={
            "source": "web_research",
            "processed": True,
            "processing_time": "2024-01-01 10:00:00"
        }
    )
```

## Best Practices

1. **Organize by Project**: Create projects for large research initiatives
2. **Use Campaigns for Breadth**: Research multiple topics simultaneously
3. **Deep Dives for Depth**: Extract content for important topics
4. **Compare Strategically**: Use comparisons to validate differences
5. **Export Regularly**: Backup important research as JSON files
6. **Monitor Stats**: Check `research-stats` to track library growth

## Performance Considerations

- **Campaign Size**: Large campaigns (20+ topics) may take time
- **Content Extraction**: Enabling extraction increases processing time
- **Storage**: Each extracted document increases storage usage
- **Caching**: Searches are cached by default for performance

## Troubleshooting

### High Memory Usage
- Delete old documents: `ai-toolkit library-delete <id> --confirm`
- Export and clear: `ai-toolkit library-export <id> <file.json>`

### Slow Content Extraction
- Reduce `--max-results` parameter
- Run extraction on fewer documents
- Check network connectivity

### Organization Issues
- Use `library-search` to find documents
- Export data for external organization
- Create projects to group related research

## Future Enhancements

Planned additions:
- Scheduled/automated research campaigns
- Research alerts and notifications
- Sentiment analysis of research
- Trend analysis over time
- Collaboration and sharing features
- Advanced filtering and tagging
