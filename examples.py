"""
Integration Examples: Using AI Toolkit in Different Projects

This file demonstrates how to integrate the AI Toolkit tools library
into different projects for research, analysis, and document management.
"""

from ai_toolkit.tools import ToolManager, WebResearchTool, ToolResult


# =====================================================================
# EXAMPLE 1: Simple Web Research
# =====================================================================

def example_simple_research():
    """Basic web research example."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Web Research")
    print("="*60)
    
    tool = WebResearchTool()
    result = tool.execute(query="Python async/await patterns")
    
    if result.success:
        print(f"✅ Found {result.metadata['result_count']} results:")
        for i, item in enumerate(result.data[:3], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   URL: {item['url']}")
            print(f"   {item['snippet'][:80]}...")
    else:
        print(f"❌ Error: {result.error}")


# =====================================================================
# EXAMPLE 2: Research with Content Extraction
# =====================================================================

def example_research_with_extraction():
    """Research and extract content from top result."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Research with Content Extraction")
    print("="*60)
    
    # Step 1: Search
    search_tool = WebResearchTool()
    search_result = search_tool.execute(query="climate change solutions")
    
    if search_result.success and search_result.data:
        print(f"✅ Found {len(search_result.data)} results")
        
        # Step 2: Extract content from first result
        top_url = search_result.data[0]['url']
        print(f"\n📖 Extracting content from: {top_url}")
        
        extract_result = search_tool.extract_content(top_url)
        
        if extract_result.success:
            content = extract_result.data
            print(f"✅ Title: {content['title']}")
            print(f"   Length: {content['content_length']} characters")
            print(f"\n   Preview:\n{content['content'][:200]}...")
        else:
            print(f"❌ Extraction error: {extract_result.error}")


# =====================================================================
# EXAMPLE 3: Using ToolManager for Multi-Tool Orchestration
# =====================================================================

def example_tool_manager():
    """Use ToolManager to orchestrate tools."""
    print("\n" + "="*60)
    print("EXAMPLE 3: ToolManager Orchestration")
    print("="*60)
    
    # Create manager
    manager = ToolManager(name="ResearchManager")
    
    # Register tools
    manager.register_tool(WebResearchTool())
    
    # List available tools
    print("\n📋 Registered Tools:")
    for tool_info in manager.list_tools():
        print(f"  - {tool_info['name']}: {tool_info['description']}")
    
    # Execute tool through manager
    print("\n🔍 Executing research...")
    result = manager.execute_tool(
        "WebResearchTool",
        query="machine learning frameworks"
    )
    
    if result.success:
        print(f"✅ Completed in {result.timestamp}")
        print(f"   Result count: {result.metadata.get('result_count')}")
        print(f"   Source: {result.metadata.get('source')}")


# =====================================================================
# EXAMPLE 4: Document Library Management
# =====================================================================

def example_document_library():
    """Store and manage research documents."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Document Library Management")
    print("="*60)
    
    manager = ToolManager(name="DocumentLibrary")
    
    # Perform research
    result = manager.execute_tool(
        WebResearchTool(),
        query="quantum computing"
    )
    
    # Store research document
    print("\n💾 Storing research document...")
    manager.store_document(
        "quantum_research_q1_2024",
        {
            "query": "quantum computing",
            "results": result.data if result.success else [],
            "research_date": result.timestamp
        },
        metadata={
            "category": "technology",
            "priority": "high",
            "researcher": "system"
        }
    )
    
    # List documents
    print("\n📚 Documents in library:")
    for doc_key in manager.list_documents():
        info = manager.get_document_info(doc_key)
        print(f"  - {doc_key}")
        print(f"    Stored: {info['stored_at']}")
        print(f"    Size: {info['content_length']} chars")
        print(f"    Meta: {info['metadata']}")
    
    # Retrieve document
    print("\n🔎 Retrieving document...")
    doc = manager.retrieve_document("quantum_research_q1_2024")
    if doc:
        print(f"✅ Retrieved document with {len(doc.get('results', []))} results")


# =====================================================================
# EXAMPLE 5: Tracking Execution History
# =====================================================================

def example_execution_history():
    """Track and analyze tool execution history."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Execution History Tracking")
    print("="*60)
    
    manager = ToolManager(name="HistoryTracker")
    manager.register_tool(WebResearchTool())
    
    # Execute multiple tools
    queries = [
        "AI safety",
        "blockchain technology",
        "renewable energy"
    ]
    
    print("\n🔄 Executing multiple queries...")
    for query in queries:
        manager.execute_tool("WebResearchTool", query=query)
        print(f"  ✓ Executed: {query}")
    
    # Get history
    print("\n📊 Execution History:")
    history = manager.get_execution_history()
    for i, entry in enumerate(history, 1):
        print(f"\n  {i}. {entry['tool']}")
        print(f"     Time: {entry['timestamp']}")
        print(f"     Query: {entry['parameters'].get('query')}")
        print(f"     Success: {entry['result']['success']}")


# =====================================================================
# EXAMPLE 6: Custom Workflow Pipeline
# =====================================================================

def example_custom_workflow():
    """Complex workflow combining multiple operations."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Custom Workflow Pipeline")
    print("="*60)
    
    manager = ToolManager(name="ResearchPipeline")
    manager.register_tool(WebResearchTool())
    
    research_topic = "emerging technologies 2024"
    
    # Step 1: Research
    print(f"\n📍 Step 1: Researching '{research_topic}'...")
    research_result = manager.execute_tool(
        "WebResearchTool",
        query=research_topic
    )
    
    # Step 2: Store results
    print("\n📍 Step 2: Storing results...")
    if research_result.success:
        manager.store_document(
            f"research_{research_topic.replace(' ', '_')}",
            research_result.data,
            metadata={
                "timestamp": research_result.timestamp,
                "query": research_topic,
                "result_count": research_result.metadata.get('result_count')
            }
        )
    
    # Step 3: Extract content from top results
    print("\n📍 Step 3: Extracting content from top results...")
    if research_result.success and research_result.data:
        tool = WebResearchTool()
        for i, item in enumerate(research_result.data[:2], 1):
            print(f"   Extracting from result {i}...")
            extract_result = tool.extract_content(item['url'])
            if extract_result.success:
                # Store extracted content
                doc_key = f"extracted_content_{i}"
                manager.store_document(
                    doc_key,
                    extract_result.data,
                    metadata={"source": item['url']}
                )
                print(f"   ✓ Stored: {doc_key}")
    
    # Step 4: Generate report
    print("\n📍 Step 4: Generating report...")
    report = {
        "topic": research_topic,
        "total_documents": len(manager.list_documents()),
        "execution_count": len(manager.get_execution_history()),
        "documents": manager.list_documents(),
        "manager_info": manager.get_info()
    }
    
    print("\n📄 Report Generated:")
    print(f"   Topic: {report['topic']}")
    print(f"   Documents stored: {report['total_documents']}")
    print(f"   Tool executions: {report['execution_count']}")
    print(f"   Storage: {report['manager_info']}")


# =====================================================================
# EXAMPLE 7: Error Handling and Validation
# =====================================================================

def example_error_handling():
    """Proper error handling and input validation."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Error Handling")
    print("="*60)
    
    tool = WebResearchTool()
    
    # Test invalid inputs
    test_cases = [
        ("", "empty query"),
        (None, "None query"),
        ("   ", "whitespace only"),
        ("valid query", "valid query")
    ]
    
    print("\n🔍 Testing input validation:")
    for query, label in test_cases:
        is_valid, error = tool.validate_inputs(query=query)
        if is_valid:
            print(f"  ✅ {label}: Valid")
        else:
            print(f"  ❌ {label}: {error}")
    
    # Execute with valid input and handle result
    print("\n🔍 Executing with error handling:")
    try:
        result = tool.execute(query="Python development")
        
        if result.success:
            print(f"  ✅ Success: {result.metadata}")
        else:
            print(f"  ❌ Failed: {result.error}")
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")


# =====================================================================
# MAIN: Run All Examples
# =====================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI TOOLKIT INTEGRATION EXAMPLES")
    print("="*60)
    
    try:
        example_simple_research()
        example_research_with_extraction()
        example_tool_manager()
        example_document_library()
        example_execution_history()
        example_custom_workflow()
        example_error_handling()
        
        print("\n" + "="*60)
        print("✅ ALL EXAMPLES COMPLETED")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()
