"""
Tool Manager - Orchestrate and manage multiple agentic tools.
"""

from typing import Dict, List, Any, Optional
from .base import AgenticTool, ToolResult


class ToolManager:
    """
    Manages a collection of agentic tools and their execution.
    
    Features:
    - Register and unregister tools
    - Execute tools by name
    - Chain tool execution
    - Store and retrieve documents/results
    """
    
    def __init__(self, name: str = "DefaultToolManager"):
        self.name = name
        self.tools: Dict[str, AgenticTool] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.document_library: Dict[str, Any] = {}
    
    def register_tool(self, tool: AgenticTool, override: bool = False) -> bool:
        """
        Register an agentic tool.
        
        Parameters:
            tool: AgenticTool instance
            override: Whether to override existing tool with same name
        
        Returns:
            bool: True if registered, False otherwise
        """
        if tool.name in self.tools and not override:
            return False
        
        self.tools[tool.name] = tool
        return True
    
    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool by name."""
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False
    
    def get_tool(self, tool_name: str) -> Optional[AgenticTool]:
        """Get a tool by name."""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools and their information."""
        return [tool.get_info() for tool in self.tools.values()]
    
    def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Execute a tool by name with given parameters.
        
        Parameters:
            tool_name: Name of the tool to execute
            **kwargs: Parameters to pass to the tool
        
        Returns:
            ToolResult: Result of tool execution
        """
        if tool_name not in self.tools:
            result = ToolResult(
                success=False,
                data=None,
                error=f"Tool '{tool_name}' not found"
            )
        else:
            tool = self.tools[tool_name]
            result = tool.execute(**kwargs)
        
        # Record execution in history
        self.execution_history.append({
            "tool": tool_name,
            "parameters": kwargs,
            "result": {
                "success": result.success,
                "error": result.error,
                "metadata": result.metadata
            },
            "timestamp": result.timestamp
        })
        
        return result
    
    def store_document(self, key: str, document: Any, metadata: Optional[Dict] = None) -> None:
        """
        Store a document in the library for reuse.
        
        Parameters:
            key: Document key/identifier
            document: Document content
            metadata: Optional metadata
        """
        self.document_library[key] = {
            "content": document,
            "metadata": metadata or {},
            "stored_at": str(__import__("datetime").datetime.now().isoformat())
        }
    
    def retrieve_document(self, key: str) -> Optional[Any]:
        """Retrieve a document from the library."""
        if key in self.document_library:
            return self.document_library[key]["content"]
        return None
    
    def list_documents(self) -> List[str]:
        """List all stored documents."""
        return list(self.document_library.keys())
    
    def get_document_info(self, key: str) -> Optional[Dict[str, Any]]:
        """Get information about a stored document."""
        if key in self.document_library:
            doc = self.document_library[key]
            return {
                "key": key,
                "metadata": doc["metadata"],
                "stored_at": doc["stored_at"],
                "content_length": len(str(doc["content"]))
            }
        return None
    
    def delete_document(self, key: str) -> bool:
        """Delete a document from the library."""
        if key in self.document_library:
            del self.document_library[key]
            return True
        return False
    
    def get_execution_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get tool execution history."""
        if limit is None:
            return self.execution_history
        return self.execution_history[-limit:]
    
    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
    
    def get_info(self) -> Dict[str, Any]:
        """Get manager information."""
        return {
            "name": self.name,
            "total_tools": len(self.tools),
            "tools": [t.name for t in self.tools.values()],
            "total_documents": len(self.document_library),
            "execution_count": len(self.execution_history)
        }
    
    def __repr__(self) -> str:
        return f"ToolManager(name={self.name}, tools={len(self.tools)}, documents={len(self.document_library)})"
