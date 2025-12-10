"""
Base filter interface and classes for user_display module.
Filters provide extensible strategies for selecting users.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable


class Filter(ABC):
    """
    Abstract base class for user filters.
    Filters select users based on criteria.
    """
    
    @abstractmethod
    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply the filter to a list of users.
        
        Returns:
            Filtered list of users
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the filter's name."""
        pass


class LambdaFilter(Filter):
    """Simple filter using a lambda/callable predicate."""
    
    def __init__(self, predicate: Callable[[Dict[str, Any]], bool], name: str = "LambdaFilter"):
        """
        Initialize filter with a predicate function.
        
        Args:
            predicate: Function that returns True for users to include
            name: Name of the filter
        """
        self.predicate = predicate
        self._name = name
    
    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply the predicate to filter users."""
        return [u for u in users if self.predicate(u)]
    
    def get_name(self) -> str:
        return self._name


class CompositeFilter(Filter):
    """Combines multiple filters with AND/OR logic."""
    
    def __init__(self, filters: List[Filter], use_or: bool = False):
        """
        Initialize composite filter.
        
        Args:
            filters: List of filters to combine
            use_or: If True, use OR logic (any match); if False, use AND logic (all must match)
        """
        self.filters = filters
        self.use_or = use_or
    
    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply all filters with AND/OR logic."""
        if not self.filters:
            return users
        
        if self.use_or:
            # OR logic: include user if ANY filter matches
            result = set()
            for f in self.filters:
                filtered = f.apply(users)
                for user in filtered:
                    user_id = user.get("id")
                    if user_id is not None:
                        result.add(user_id)
            
            # Return users in original order
            return [u for u in users if u.get("id") in result]
        else:
            # AND logic: apply filters sequentially
            result = users
            for f in self.filters:
                result = f.apply(result)
            return result
    
    def get_name(self) -> str:
        logic = "OR" if self.use_or else "AND"
        names = [f.get_name() for f in self.filters]
        return f"Composite({logic}): {', '.join(names)}"
    
    def add_filter(self, f: Filter) -> None:
        """Add a filter to the composite."""
        self.filters.append(f)
