"""Tests for pagination utilities."""

import pytest

from src.utils.pagination import paginate, get_pagination_params


class TestPaginate:
    """Tests for paginate function."""

    def test_basic_pagination(self):
        """Test basic pagination."""
        items = list(range(25))

        result = paginate(items, page=1, page_size=10)

        assert result.count == 25
        assert result.page == 1
        assert result.page_size == 10
        assert result.total_pages == 3
        assert result.has_next is True
        assert result.has_previous is False
        assert len(result.results) == 10
        assert result.results == list(range(10))

    def test_second_page(self):
        """Test getting second page."""
        items = list(range(25))

        result = paginate(items, page=2, page_size=10)

        assert result.page == 2
        assert result.has_next is True
        assert result.has_previous is True
        assert result.results == list(range(10, 20))

    def test_last_page(self):
        """Test getting last page."""
        items = list(range(25))

        result = paginate(items, page=3, page_size=10)

        assert result.page == 3
        assert result.has_next is False
        assert result.has_previous is True
        assert len(result.results) == 5
        assert result.results == list(range(20, 25))

    def test_page_beyond_range(self):
        """Test requesting page beyond available range."""
        items = list(range(25))

        result = paginate(items, page=10, page_size=10)

        # Should clamp to last page
        assert result.page == 3

    def test_negative_page(self):
        """Test handling negative page number."""
        items = list(range(25))

        result = paginate(items, page=-1, page_size=10)

        assert result.page == 1

    def test_empty_list(self):
        """Test pagination with empty list."""
        items = []

        result = paginate(items, page=1, page_size=10)

        assert result.count == 0
        assert result.page == 1
        assert result.total_pages == 1
        assert result.has_next is False
        assert result.has_previous is False
        assert result.results == []

    def test_page_size_cap(self):
        """Test that page size is capped at 100."""
        items = list(range(200))

        result = paginate(items, page=1, page_size=150)

        assert result.page_size == 100
        assert len(result.results) == 100


class TestGetPaginationParams:
    """Tests for get_pagination_params function."""

    def test_default_values(self):
        """Test getting default values."""
        page, page_size = get_pagination_params()

        assert page == 1
        assert page_size == 10

    def test_custom_values(self):
        """Test custom values."""
        page, page_size = get_pagination_params(page=5, page_size=25)

        assert page == 5
        assert page_size == 25

    def test_max_page_size(self):
        """Test page size is capped at max."""
        page, page_size = get_pagination_params(page_size=200, max_page_size=100)

        assert page_size == 100

    def test_negative_values(self):
        """Test handling negative values."""
        page, page_size = get_pagination_params(page=-5, page_size=-10)

        assert page == 1
        assert page_size == 1
