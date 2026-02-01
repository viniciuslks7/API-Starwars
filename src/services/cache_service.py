"""In-memory cache service with TTL support."""

import time
from typing import Any


class CacheEntry:
    """Cache entry with value and expiration."""

    def __init__(self, value: Any, ttl: int):
        self.value = value
        self.expires_at = time.time() + ttl

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        return time.time() > self.expires_at


class CacheService:
    """
    In-memory cache service with TTL support.

    For production, this could be replaced with Redis or Firestore.
    The in-memory cache works well for Cloud Functions as it persists
    across warm starts.
    """

    # TTL constants
    TTL_SHORT = 300  # 5 minutes
    TTL_MEDIUM = 3600  # 1 hour
    TTL_LONG = 86400  # 24 hours

    def __init__(self, enabled: bool = True, default_ttl: int = TTL_MEDIUM):
        self._cache: dict[str, CacheEntry] = {}
        self._enabled = enabled
        self._default_ttl = default_ttl
        self._hits = 0
        self._misses = 0

    @property
    def enabled(self) -> bool:
        """Check if cache is enabled."""
        return self._enabled

    @property
    def stats(self) -> dict:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "entries": len(self._cache),
        }

    def get(self, key: str) -> Any | None:
        """
        Get value from cache.

        Returns None if not found or expired.
        """
        if not self._enabled:
            return None

        entry = self._cache.get(key)
        if entry is None:
            self._misses += 1
            return None

        if entry.is_expired():
            del self._cache[key]
            self._misses += 1
            return None

        self._hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """
        Set value in cache with TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default if not provided)
        """
        if not self._enabled:
            return

        ttl = ttl or self._default_ttl
        self._cache[key] = CacheEntry(value, ttl)

    def delete(self, key: str) -> bool:
        """
        Delete a key from cache.

        Returns True if key existed.
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> int:
        """
        Clear all cache entries.

        Returns number of entries cleared.
        """
        count = len(self._cache)
        self._cache.clear()
        return count

    def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching a pattern.

        Simple prefix matching (e.g., "people:" clears all people keys).
        Returns number of entries cleared.
        """
        keys_to_delete = [k for k in self._cache.keys() if k.startswith(pattern)]
        for key in keys_to_delete:
            del self._cache[key]
        return len(keys_to_delete)

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.

        Returns number of entries removed.
        """
        expired_keys = [k for k, v in self._cache.items() if v.is_expired()]
        for key in expired_keys:
            del self._cache[key]
        return len(expired_keys)

    def make_key(self, *parts: str) -> str:
        """Create a cache key from parts."""
        return ":".join(str(p) for p in parts)
