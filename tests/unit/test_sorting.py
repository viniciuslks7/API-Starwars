"""Tests for sorting utilities."""

import pytest

from src.utils.sorting import sort_items, SortOrder


class TestSortItems:
    """Tests for sort_items function."""

    def test_sort_dicts_ascending(self):
        """Test sorting dictionaries in ascending order."""
        items = [
            {"name": "Charlie", "age": 30},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 35},
        ]
        
        result = sort_items(items, sort_by="name", sort_order=SortOrder.ASC)
        
        assert result[0]["name"] == "Alice"
        assert result[1]["name"] == "Bob"
        assert result[2]["name"] == "Charlie"

    def test_sort_dicts_descending(self):
        """Test sorting dictionaries in descending order."""
        items = [
            {"name": "Charlie", "age": 30},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 35},
        ]
        
        result = sort_items(items, sort_by="age", sort_order=SortOrder.DESC)
        
        assert result[0]["age"] == 35
        assert result[1]["age"] == 30
        assert result[2]["age"] == 25

    def test_sort_with_none_values(self):
        """Test that None values go to the end."""
        items = [
            {"name": "Charlie", "age": None},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 35},
        ]
        
        result = sort_items(items, sort_by="age", sort_order=SortOrder.ASC)
        
        # None should be at the end
        assert result[0]["age"] == 25
        assert result[1]["age"] == 35
        assert result[2]["age"] is None

    def test_sort_no_sort_by(self):
        """Test that no sorting happens when sort_by is None."""
        items = [{"a": 3}, {"a": 1}, {"a": 2}]
        
        result = sort_items(items, sort_by=None)
        
        assert result == items

    def test_sort_with_custom_key_mapper(self):
        """Test sorting with custom key mapper."""
        items = [
            {"name": "CHARLIE"},
            {"name": "alice"},
            {"name": "Bob"},
        ]
        
        key_mapper = {"name": lambda x: x["name"].lower()}
        result = sort_items(
            items, 
            sort_by="name", 
            sort_order=SortOrder.ASC,
            key_mapper=key_mapper
        )
        
        assert result[0]["name"] == "alice"
        assert result[1]["name"] == "Bob"
        assert result[2]["name"] == "CHARLIE"

    def test_sort_empty_list(self):
        """Test sorting empty list."""
        result = sort_items([], sort_by="name")
        assert result == []
