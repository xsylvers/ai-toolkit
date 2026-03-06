# AI Toolkit - Deployment & Usage Checklist

## Pre-Deployment Checklist

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] AI Toolkit installed: `pip install -e .`
- [ ] `.env` file created in project root
- [ ] API keys configured:
  - [ ] `OPENAI_API_KEY` (required if using OpenAI features)
  - [ ] `GEMINI_API_KEY` (required if using Gemini features)
  - [ ] `SERPAPI_KEY` (optional, for real web searches)

### Verification
- [ ] Run `ai-toolkit doctor` - all checks pass
- [ ] Run `ai-toolkit research "test"` - returns results
- [ ] Run `python examples.py` - completes without errors
- [ ] Review documentation in this order:
  - [ ] INDEX.md
  - [ ] QUICK_REFERENCE.md
  - [ ] QUICKSTART.md

### Project Integration
- [ ] Add `ai-toolkit` to `requirements.txt`
- [ ] Add `ai-toolkit @ file://../ai-toolkit` if using local installation
- [ ] Copy `.env` template to project
- [ ] Load environment variables in startup: `load_dotenv()`

## Common Usage Patterns

### Pattern 1: First Run
**Goal**: Verify installation works
```bash
# 1. Check setup
ai-toolkit doctor

# 2. Do a simple search
ai-toolkit research "artificial intelligence"

# 3. View what was stored
ai-toolkit library-list

# 4. Run examples
python examples.py
```
**Time**: ~5 minutes

### Pattern 2: Research Workflow
**Goal**: Conduct organized research
```bash
# 1. Create campaign
ai-toolkit research-campaign "Project 2024" \
  "machine learning,neural networks,deep learning" \
  --max-results 10

# 2. Do deep dives
ai-toolkit research-deep-dive "machine learning" --extract-content

# 3. Compare topics
ai-toolkit research-compare "ML" "Deep Learning"

# 4. Export results
ai-toolkit library-export "campaign_Project_2024" "research_2024.json"

# 5. View stats
ai-toolkit research-stats
```
**Time**: ~10-20 minutes

### Pattern 3: Project Integration
**Goal**: Use in your application code
```python
import sys
from dotenv import load_dotenv
from ai_toolkit.tools import WebResearchTool, ToolManager
from ai_toolkit.research_cli import ResearchCampaign

# 1. Setup
load_dotenv()
manager = ToolManager()
tool = WebResearchTool()

# 2. Research
campaign = ResearchCampaign("MyResearch", ["topic1", "topic2"])
results = campaign.execute(tool)

# 3. Store
manager.store_document("my_research", results)

# 4. Use
data = manager.retrieve_document("my_research")
print(f"Found {len(data)} research items")
```
**Time**: Depends on implementation

### Pattern 4: Scheduled Automation
**Goal**: Run research on schedule (Python)
```python
# research_scheduler.py
import schedule
import time
from dotenv import load_dotenv
from ai_toolkit.tools import WebResearchTool, ToolManager

load_dotenv()

def daily_research():
    """Run daily research."""
    tool = WebResearchTool()
    manager = ToolManager()
    
    topics = ["AI", "ML", "DL"]
    campaign = ResearchCampaign("Daily", topics)
    results = campaign.execute(tool)
    
    manager.store_document(f"daily_{date.today()}", results)
    print(f"Daily research complete: {len(results)} topics")

# Schedule
schedule.every().day.at("09:00").do(daily_research)

# Run
while True:
    schedule.run_pending()
    time.sleep(1)
```

## Troubleshooting Guide

### Issue: "ModuleNotFoundError: No module named 'ai_toolkit'"
**Solution**:
```bash
# Make sure you're in the right virtual environment
which python  # Check which Python is active
pip install -e .  # Reinstall in current environment
```

### Issue: "OPENAI_API_KEY not found"
**Solution**:
```bash
# Create .env file in project root
echo "OPENAI_API_KEY=your_key" > .env
echo "GEMINI_API_KEY=your_key" >> .env

# Or use the template:
# Create .env with:
# OPENAI_API_KEY=your_actual_key
# GEMINI_API_KEY=your_actual_key
# SERPAPI_KEY=your_actual_key (optional)
```

### Issue: "Web research returns placeholder results"
**Solution**:
```bash
# Set up a real search API
# Option 1: Use SerpAPI
echo "SERPAPI_KEY=your_serpapi_key" >> .env

# Option 2: Use Google Custom Search
echo "GOOGLE_SEARCH_API_KEY=your_key" >> .env
echo "GOOGLE_SEARCH_ENGINE_ID=your_engine_id" >> .env
```

### Issue: "Memory usage is high"
**Solution**:
```bash
# Delete old documents
ai-toolkit library-list  # See what's stored

ai-toolkit library-delete "old_doc_id" --confirm

# Or export and delete
ai-toolkit library-export "doc_id" "backup.json"
ai-toolkit library-delete "doc_id" --confirm
```

### Issue: "Content extraction failing"
**Solution**:
```bash
# Install required packages
pip install requests beautifulsoup4

# Try extraction again
ai-toolkit research-extract "https://example.com"
```

### Issue: "Commands not found"
**Solution**:
```bash
# Verify installation
pip list | grep ai-toolkit

# Reinstall
pip install -e .

# Verify setup
ai-toolkit --help
```

## Performance Optimization

### Tip 1: Use Campaigns for Multiple Topics
**Instead of**:
```bash
ai-toolkit research "topic1"
ai-toolkit research "topic2"
ai-toolkit research "topic3"
```

**Use**:
```bash
ai-toolkit research-campaign "Name" "topic1,topic2,topic3"
```
**Benefit**: Parallel execution, ~30% faster

### Tip 2: Enable Caching
```python
# Cache is enabled by default
result = tool.execute(query="topic", use_cache=True)  # Default

# Disable if you need fresh results
result = tool.execute(query="topic", use_cache=False)
```
**Benefit**: ~100x faster for repeated queries

### Tip 3: Limit Results
```bash
# Don't get more than you need
ai-toolkit research "topic" --max-results 5  # Instead of 20

ai-toolkit research-campaign "Name" "t1,t2" --max-results 5
```
**Benefit**: 50% faster, less storage

### Tip 4: Batch Extract Strategically
```python
# Extract only from top results
results = tool.execute(query="topic", max_results=10)

for item in results.data[:3]:  # Only extract top 3
    content = tool.extract_content(item['url'])
```
**Benefit**: 5-10x faster for large campaigns

### Tip 5: Archive Old Research
```bash
# Export before delete
ai-toolkit library-export "campaign_old" "archive_2024_q1.json"

# Delete to save memory
ai-toolkit library-delete "campaign_old" --confirm
```

## Deployment Scenarios

### Scenario 1: Local Development
```bash
# Setup
pip install -e .
cp .env.example .env
# Edit .env with your keys

# Daily usage
ai-toolkit research "your topic"
ai-toolkit library-list
```

### Scenario 2: Team Project
```
shared-ai-toolkit/
├── .env.example (commit)
├── requirements.txt (commit)
└── src/

project-a/
├── .env (local, DO NOT commit)
├── requirements.txt → includes ai-toolkit
└── src/

project-b/
├── .env (local, DO NOT commit)
└── [similar structure]
```

**In each project:**
```bash
pip install -e ../shared-ai-toolkit
cp ../shared-ai-toolkit/.env.example .env
# Edit .env with your keys
```

### Scenario 3: Production Environment
```python
# main.py
import os
from dotenv import load_dotenv

# Load from environment variables (not from file)
load_dotenv(override=False)

# Verify all keys present
required_keys = ['OPENAI_API_KEY', 'GEMINI_API_KEY']
for key in required_keys:
    if not os.getenv(key):
        raise RuntimeError(f"Missing {key}")

# Now use toolkit
from ai_toolkit.tools import WebResearchTool
```

### Scenario 4: Docker Deployment
```dockerfile
FROM python:3.11

WORKDIR /app

# Copy toolkit
COPY shared-ai-toolkit /app/ai-toolkit

# Install
RUN pip install -e /app/ai-toolkit

# Copy project
COPY . /app/project

# Set environment
ENV PYTHONUNBUFFERED=1

# Run
CMD ["python", "project/main.py"]
```

## Monitoring & Maintenance

### Weekly Tasks
- [ ] Check storage usage: `ai-toolkit research-stats`
- [ ] Archive old research if needed
- [ ] Update if new features available: `pip install -e . --upgrade`

### Monthly Tasks
- [ ] Review execution history: `manager.get_execution_history()`
- [ ] Clean up unused documents
- [ ] Test functionality: `python examples.py`

### As-Needed Tasks
- [ ] Troubleshoot failures
- [ ] Optimize queries
- [ ] Archive important research

## Integration Testing

### Test 1: Basic Functionality
```bash
ai-toolkit doctor
ai-toolkit research "test"
ai-toolkit library-list
```

### Test 2: Python API
```python
from ai_toolkit.tools import WebResearchTool

tool = WebResearchTool()
result = tool.execute(query="test")
assert result.success
assert len(result.data) > 0
print("✓ Basic tests passed")
```

### Test 3: Full Workflow
```bash
ai-toolkit research-campaign "test" "topic1,topic2"
ai-toolkit library-list
ai-toolkit library-export "campaign_test" "test_export.json"
ai-toolkit library-delete "campaign_test" --confirm
```

## Best Practices

✅ **DO**:
- Always check `result.success` before using data
- Use campaigns for multiple topics
- Cache results when appropriate
- Export important research
- Store with meaningful metadata
- Test before production use
- Keep `.env` secure (in .gitignore)

❌ **DON'T**:
- Commit `.env` files
- Extract from every result
- Store duplicate research
- Use placeholders in production (without API keys)
- Ignore error messages
- Leave large documents in memory

## Quick Deployment Script

```bash
#!/bin/bash
# deploy.sh

set -e

echo "🚀 Deploying AI Toolkit..."

# 1. Setup
echo "1. Installing AI Toolkit..."
pip install -e .

# 2. Verify
echo "2. Running doctor check..."
ai-toolkit doctor

# 3. Test
echo "3. Running quick test..."
ai-toolkit research "test" > /dev/null

# 4. Examples
echo "4. Running examples..."
python examples.py > /dev/null

echo "✅ Deployment complete!"
echo "📖 Read INDEX.md for documentation"
echo "🎯 Try: ai-toolkit research \"your topic\""
```

## Maintenance Checklist

### Monthly
- [ ] Check API key validity
- [ ] Review storage usage
- [ ] Clean up old documents
- [ ] Update documentation if needed

### Quarterly
- [ ] Review performance metrics
- [ ] Archive old research
- [ ] Test disaster recovery
- [ ] Update dependencies if available

### Annually
- [ ] Full audit of stored research
- [ ] Performance optimization review
- [ ] Security review
- [ ] Planning for new tools

---

**Last Updated**: February 6, 2026
**Version**: 1.0.0
