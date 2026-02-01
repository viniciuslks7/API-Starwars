"""Sorting utilities."""

from enum import Enum
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class SortOrder(str, Enum):
    """Sort order enum."""

    ASC = "asc"
    DESC = "desc"


def sort_items(
    items: list[T],
    sort_by: str | None = None,
    sort_order: SortOrder = SortOrder.ASC,
    key_mapper: dict[str, Callable[[T], Any]] | None = None,
) -> list[T]:
    """
    Sort a list of items by a field.

    Args:
        items: List of items to sort
        sort_by: Field name to sort by
        sort_order: Sort order (asc/desc)
        key_mapper: Optional dict mapping field names to key functions

    Returns:
        Sorted list
    """
    if not sort_by:
        return items

    # Default key function - works with dicts and objects
    def default_key(item: T) -> Any:
        if isinstance(item, dict):
            value = item.get(sort_by)
        else:
            value = getattr(item, sort_by, None)

        # Handle None values - put them at the end
        if value is None:
            return (1, "")  # Tuple ensures None goes last
        return (0, value)

    key_func = default_key
    if key_mapper and sort_by in key_mapper:
        base_func = key_mapper[sort_by]
        # Wrap to handle None values
        key_func = lambda x: (0, base_func(x)) if base_func(x) is not None else (1, "")

    reverse = sort_order == SortOrder.DESC

    return sorted(items, key=key_func, reverse=reverse)


# Common sort key mappers
PEOPLE_SORT_KEYS: dict[str, Callable] = {
    "name": lambda p: p.name.lower() if hasattr(p, "name") else p.get("name", "").lower(),
    "height": lambda p: p.height if hasattr(p, "height") else p.get("height"),
    "mass": lambda p: p.mass if hasattr(p, "mass") else p.get("mass"),
    "birth_year": lambda p: (
        p.birth_year if hasattr(p, "birth_year") else p.get("birth_year", "")
    ),
}

STARSHIP_SORT_KEYS: dict[str, Callable] = {
    "name": lambda s: s.name.lower() if hasattr(s, "name") else s.get("name", "").lower(),
    "length": lambda s: s.length if hasattr(s, "length") else s.get("length"),
    "cost_in_credits": lambda s: (
        s.cost_in_credits if hasattr(s, "cost_in_credits") else s.get("cost_in_credits")
    ),
    "hyperdrive_rating": lambda s: (
        s.hyperdrive_rating if hasattr(s, "hyperdrive_rating") else s.get("hyperdrive_rating")
    ),
}

PLANET_SORT_KEYS: dict[str, Callable] = {
    "name": lambda p: p.name.lower() if hasattr(p, "name") else p.get("name", "").lower(),
    "diameter": lambda p: p.diameter if hasattr(p, "diameter") else p.get("diameter"),
    "population": lambda p: p.population if hasattr(p, "population") else p.get("population"),
}

FILM_SORT_KEYS: dict[str, Callable] = {
    "title": lambda f: f.title.lower() if hasattr(f, "title") else f.get("title", "").lower(),
    "episode_id": lambda f: (
        f.episode_id if hasattr(f, "episode_id") else f.get("episode_id", 0)
    ),
    "release_date": lambda f: (
        f.release_date if hasattr(f, "release_date") else f.get("release_date")
    ),
}
