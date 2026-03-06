"""
Advanced Research CLI Examples

Demonstrates practical usage of the research CLI for various real-world scenarios.
"""

from pathlib import Path
from ai_toolkit.tools import ToolManager, WebResearchTool
from ai_toolkit.research_cli import ResearchCampaign, ResearchProject
import json


# =====================================================================
# EXAMPLE 1: Technology Landscape Campaign
# =====================================================================

def example_tech_landscape():
    """Survey the current technology landscape."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Technology Landscape Survey")
    print("="*70 + "\n")
    
    # Topics to research
    topics = [
        "AI and machine learning 2024",
        "Cloud computing trends",
        "Cybersecurity threats",
        "web3 and blockchain",
        "quantum computing",
        "edge computing"
    ]
    
    # Create campaign
    campaign = ResearchCampaign("Tech Landscape 2024", topics)
    tool = WebResearchTool()
    
    print("🔍 Researching technology landscape...")
    results = campaign.execute(tool, max_results_per_topic=5)
    
    # Display summary
    summary = campaign.get_summary()
    print("\n📊 Campaign Summary:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    # Store campaign
    manager = ToolManager()
    manager.store_document(
        "campaign_tech_landscape_2024",
        results,
        metadata={
            "campaign_type": "landscape_survey",
            **summary
        }
    )
    
    return results


# =====================================================================
# EXAMPLE 2: Competitive Analysis
# =====================================================================

def example_competitive_analysis():
    """Analyze competitive landscape."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Competitive Analysis")
    print("="*70 + "\n")
    
    companies = ["company_a", "company_b", "company_c"]
    tech_areas = ["AI capabilities", "cloud infrastructure", "customer experience"]
    
    manager = ToolManager()
    tool = WebResearchTool()
    
    analyses = {}
    
    for company in companies:
        print(f"Analyzing {company}...")
        
        company_results = {}
        for tech_area in tech_areas:
            query = f"{company} {tech_area}"
            result = tool.execute(query=query, max_results=3)
            company_results[tech_area] = result.data if result.success else []
        
        analyses[company] = company_results
        
        # Store individual company analysis
        manager.store_document(
            f"analysis_{company}",
            company_results,
            metadata={"type": "company_analysis", "company": company}
        )
    
    # Store combined analysis
    manager.store_document(
        "competitive_analysis_2024",
        analyses,
        metadata={"type": "competitive", "companies": len(companies)}
    )
    
    print("\n✅ Competitive analysis completed")
    return analyses


# =====================================================================
# EXAMPLE 3: Research Project with Deep Dives
# =====================================================================

def example_research_project():
    """Organize research into a structured project."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Structured Research Project")
    print("="*70 + "\n")
    
    # Create project
    project = ResearchProject(
        "AI Safety and Ethics",
        "Comprehensive study of AI safety, ethics, and governance"
    )
    
    # Add topics
    topics = [
        "AI alignment",
        "AI safety research",
        "AI ethics",
        "responsible AI governance",
        "AI bias and fairness"
    ]
    
    for topic in topics:
        project.add_topic(topic)
    
    # Research each topic
    tool = WebResearchTool()
    manager = ToolManager()
    
    print(f"📁 Project: {project.name}")
    print(f"   Topics: {len(project.topics)}\n")
    
    for i, topic in enumerate(topics, 1):
        print(f"   [{i}] Researching: {topic}")
        result = tool.execute(query=topic, max_results=5)
        
        if result.success:
            # Store individual topic research
            manager.store_document(
                f"project_ai_safety_topic_{i}_{topic.replace(' ', '_')}",
                result.data,
                metadata={"project": "AI Safety", "topic": topic}
            )
            
            project.add_document(
                f"topic_{i}",
                result.data,
                metadata={"timestamp": result.timestamp, "source": topic}
            )
    
    # Store project
    manager.store_document(
        "project_AI_Safety_and_Ethics",
        project.to_dict(),
        metadata={"type": "project", "topic_count": len(topics)}
    )
    
    print("\n✅ Project research completed")
    return project


# =====================================================================
# EXAMPLE 4: Comparative Analysis
# =====================================================================

def example_comparative_analysis():
    """Compare different topics or approaches."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Comparative Analysis")
    print("="*70 + "\n")
    
    comparisons = [
        ("supervised learning", "unsupervised learning"),
        ("traditional AI", "generative AI"),
        ("cloud computing", "edge computing"),
    ]
    
    tool = WebResearchTool()
    manager = ToolManager()
    
    comparison_results = {}
    
    for topic1, topic2 in comparisons:
        print(f"Comparing: {topic1} vs {topic2}")
        
        result1 = tool.execute(query=topic1, max_results=3)
        result2 = tool.execute(query=topic2, max_results=3)
        
        comparison_data = {
            "topic1": {
                "name": topic1,
                "results": result1.data if result1.success else []
            },
            "topic2": {
                "name": topic2,
                "results": result2.data if result2.success else []
            }
        }
        
        comparison_results[f"{topic1}_vs_{topic2}"] = comparison_data
        
        # Store comparison
        manager.store_document(
            f"comparison_{topic1.replace(' ', '_')}_vs_{topic2.replace(' ', '_')}",
            comparison_data,
            metadata={
                "type": "comparison",
                "topic1": topic1,
                "topic2": topic2
            }
        )
    
    print("\n✅ Comparisons completed")
    return comparison_results


# =====================================================================
# EXAMPLE 5: Research Campaign with Content Extraction
# =====================================================================

def example_deep_research():
    """Perform deep research with content extraction."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Deep Research with Content Extraction")
    print("="*70 + "\n")
    
    topic = "large language models"
    
    print(f"🔍 Deep dive into: {topic}\n")
    
    tool = WebResearchTool()
    manager = ToolManager()
    
    # First, search for sources
    search_result = tool.execute(query=topic, max_results=10)
    
    if not search_result.success:
        print("Search failed")
        return None
    
    print(f"Found {len(search_result.data)} sources\n")
    
    # Extract content from top sources
    extracted_content = []
    
    for i, item in enumerate(search_result.data[:3], 1):
        print(f"   {i}. Extracting: {item['title'][:50]}...")
        
        extract_result = tool.extract_content(item['url'])
        
        if extract_result.success:
            doc = extract_result.data
            extracted_content.append({
                "title": doc['title'],
                "url": item['url'],
                "content": doc['content'],
                "content_length": doc['content_length']
            })
            print(f"      ✓ Extracted {doc['content_length']} characters")
        else:
            print(f"      ✗ Extraction failed")
    
    # Store deep research
    deep_research_data = {
        "topic": topic,
        "search_results": search_result.data,
        "extracted_documents": extracted_content,
        "summary": {
            "total_sources": len(search_result.data),
            "documents_extracted": len(extracted_content)
        }
    }
    
    manager.store_document(
        f"deepresearch_{topic.replace(' ', '_')}",
        deep_research_data,
        metadata={
            "type": "deep_research",
            "topic": topic,
            "extracted_count": len(extracted_content)
        }
    )
    
    print(f"\n✅ Deep research completed ({len(extracted_content)} documents)")
    return deep_research_data


# =====================================================================
# EXAMPLE 6: Export and Archive Research
# =====================================================================

def example_export_archive():
    """Export research for archival and sharing."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Export and Archive Research")
    print("="*70 + "\n")
    
    manager = ToolManager()
    
    # First, create some research
    campaign = ResearchCampaign("Archive Test", ["AI", "ML", "DL"])
    tool = WebResearchTool()
    results = campaign.execute(tool, max_results_per_topic=3)
    
    manager.store_document("test_campaign", results)
    
    # Export to file
    export_file = Path("research_archive.json")
    doc = manager.retrieve_document("test_campaign")
    
    with open(export_file, 'w') as f:
        json.dump(doc, f, indent=2)
    
    print(f"✅ Exported to: {export_file}")
    print(f"   File size: {export_file.stat().st_size} bytes")
    
    # Later, reimport
    with open(export_file, 'r') as f:
        imported_doc = json.load(f)
    
    manager.store_document("imported_campaign", imported_doc)
    
    print(f"✅ Reimported as: imported_campaign")
    
    return export_file


# =====================================================================
# EXAMPLE 7: Research Statistics and Reporting
# =====================================================================

def example_reporting():
    """Generate reports and statistics."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Reporting and Statistics")
    print("="*70 + "\n")
    
    manager = ToolManager()
    
    # Build up some research
    topics = ["machine learning", "neural networks", "deep learning", "transformers"]
    
    for topic in topics:
        tool = WebResearchTool()
        result = tool.execute(query=topic, max_results=3)
        manager.store_document(f"research_{topic.replace(' ', '_')}", result.data)
    
    # Generate statistics
    info = manager.get_info()
    docs = manager.list_documents()
    
    print("📊 Research Statistics:")
    print(f"   Total documents: {len(docs)}")
    print(f"   Total tool executions: {info['execution_count']}")
    print(f"   Registered tools: {info['total_tools']}")
    print(f"   Tools: {', '.join(info['tools'])}")
    
    print(f"\n📚 Documents:")
    total_size = 0
    for doc_id in docs[:10]:  # Show first 10
        doc_info = manager.get_document_info(doc_id)
        size = doc_info['content_length']
        total_size += size
        print(f"   • {doc_id}: {size} chars")
    
    print(f"\n   Total storage: {total_size} characters")
    
    # Execution history
    history = manager.get_execution_history()
    print(f"\n📈 Recent executions: {len(history)}")
    for entry in history[-3:]:
        print(f"   • {entry['tool']}: {entry['timestamp']}")


# =====================================================================
# EXAMPLE 8: Integration with Projects
# =====================================================================

def example_project_integration():
    """Integrate research CLI with project management."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Project-Based Research Organization")
    print("=" * 70 + "\n")
    
    # Create main project
    project = ResearchProject(
        "2024 Technology Overview",
        "Comprehensive study of major technology trends"
    )
    
    # Define research areas
    areas = {
        "Artificial Intelligence": ["AI trends", "LLMs", "AI safety"],
        "Cloud & Infrastructure": ["cloud computing", "kubernetes", "serverless"],
        "Data": ["big data", "data science", "analytics"],
    }
    
    manager = ToolManager()
    tool = WebResearchTool()
    
    print(f"📁 Project: {project.name}\n")
    
    # Research each area
    for area, topics in areas.items():
        print(f"   Area: {area}")
        project.add_topic(area)
        
        for topic in topics:
            result = tool.execute(query=topic, max_results=2)
            
            # Store with hierarchical naming
            doc_id = f"project_{area.replace(' ', '_')}_{topic.replace(' ', '_')}"
            
            manager.store_document(
                doc_id,
                result.data if result.success else [],
                metadata={
                    "project": project.name,
                    "area": area,
                    "topic": topic
                }
            )
            print(f"      ✓ {topic}")
    
    # Store project metadata
    manager.store_document(
        "project_2024_technology_overview",
        project.to_dict(),
        metadata={"type": "project"}
    )
    
    print(f"\n✅ Project research completed")
    print(f"   Total documents: {len(manager.list_documents())}")


# =====================================================================
# MAIN: Run All Examples
# =====================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("ADVANCED RESEARCH CLI EXAMPLES")
    print("="*70)
    
    try:
        example_tech_landscape()
        example_competitive_analysis()
        example_research_project()
        example_comparative_analysis()
        example_deep_research()
        example_export_archive()
        example_reporting()
        example_project_integration()
        
        print("\n" + "="*70)
        print("✅ ALL EXAMPLES COMPLETED")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()
