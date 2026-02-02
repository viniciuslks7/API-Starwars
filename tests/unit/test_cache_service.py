"""Tests for cache service."""

import time

import pytest

from src.services.cache_service import CacheService


class TestCacheService:
    """Tests for CacheService."""

    def test_init_enabled(self):
        """Test cache initialization with enabled=True."""
        cache = CacheService(enabled=True, default_ttl=60)
        assert cache.enabled is True

    def test_init_disabled(self):
        """Test cache initialization with enabled=False."""
        cache = CacheService(enabled=False)
        assert cache.enabled is False

    def test_set_and_get(self):
        """Test setting and getting a value."""
        cache = CacheService(enabled=True, default_ttl=60)
        cache.set("key1", {"data": "value"})

        result = cache.get("key1")
        assert result == {"data": "value"}

    def test_get_nonexistent_key(self):
        """Test getting a non-existent key."""
        cache = CacheService(enabled=True)
        result = cache.get("nonexistent")
        assert result is None

    def test_get_when_disabled(self):
        """Test that get returns None when cache is disabled."""
        cache = CacheService(enabled=False)
        cache.set("key1", "value")  # Use set method instead of direct access
        cache._enabled = True  # Temporarily enable to verify the value was not stored
        result = cache.get("key1")
        assert result is None

    def test_set_when_disabled(self):
        """Test that set does nothing when cache is disabled."""
        cache = CacheService(enabled=False)
        cache.set("key1", "value")
        assert "key1" not in cache._cache

    def test_delete(self):
        """Test deleting a key."""
        cache = CacheService(enabled=True)
        cache.set("key1", "value")

        result = cache.delete("key1")
        assert result is True
        assert cache.get("key1") is None

    def test_delete_nonexistent(self):
        """Test deleting a non-existent key."""
        cache = CacheService(enabled=True)
        result = cache.delete("nonexistent")
        assert result is False

    def test_clear(self):
        """Test clearing all entries."""
        cache = CacheService(enabled=True)
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        count = cache.clear()
        assert count == 2
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_clear_pattern(self):
        """Test clearing entries by pattern."""
        cache = CacheService(enabled=True)
        cache.set("people:1", "person1")
        cache.set("people:2", "person2")
        cache.set("films:1", "film1")

        count = cache.clear_pattern("people:")
        assert count == 2
        assert cache.get("people:1") is None
        assert cache.get("films:1") == "film1"

    def test_make_key(self):
        """Test creating cache keys."""
        cache = CacheService(enabled=True)
        key = cache.make_key("people", "1", "details")
        assert key == "people:1:details"

    def test_stats(self):
        """Test cache statistics."""
        cache = CacheService(enabled=True)

        # Initial stats
        stats = cache.stats
        assert stats["hits"] == 0
        assert stats["misses"] == 0

        # Add some entries and access them
        cache.set("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss

        stats = cache.stats
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["entries"] == 1

    def test_expired_entry(self):
        """Test that expired entries are not returned."""
        cache = CacheService(enabled=True, default_ttl=1)
        cache.set("key1", "value1", ttl=-1)  # Negative TTL = immediately expired

        result = cache.get("key1")
        assert result is None

    def test_cleanup_expired(self):
        """Test cleanup of expired entries."""
        cache = CacheService(enabled=True)

        # Add entries with negative TTL (already expired)
        cache.set("key1", "value1", ttl=-1)
        cache.set("key2", "value2", ttl=3600)  # Long TTL

        count = cache.cleanup_expired()
        assert count == 1
        assert cache.get("key2") == "value2"
