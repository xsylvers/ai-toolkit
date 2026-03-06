"""
Base class for all agentic tools in the AI Toolkit.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class ToolResult:
    """Result object returned by tool execution."""
    
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class AgenticTool(ABC):
    """
    Base class for agentic tools.
    
    All tools inherit from this and implement the execute method.
    Tools can be chained together and managed by ToolManager.
    """
    
    def __init__(self, name: str, description: str, version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version
        self.metadata = {}
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with given parameters.
        
        Returns:
            ToolResult: Result of tool execution
        """
        pass
    
    @abstractmethod
    def validate_inputs(self, **kwargs) -> tuple[bool, Optional[str]]:
        """
        Validate input parameters before execution.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get tool information."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "metadata": self.metadata,
        }
    
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata for the tool."""
        self.metadata[key] = value
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, version={self.version})"
