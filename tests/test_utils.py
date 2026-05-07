"""Unit tests for the helpers exposed in pymetadataeditor.utils."""

from typing import List, Tuple

import pandas as pd
import pytest

from pymetadataeditor.utils import (
    format_keywords,
    paginate_all_pages,
    validate_sort_by,
)

# ---------------------------------------------------------------------------
# paginate_all_pages
# ---------------------------------------------------------------------------


def _make_fake_pages(*sizes: int) -> List[pd.DataFrame]:
    """Build a list of DataFrames with the given row counts (and a unique 'val' column)."""
    pages: List[pd.DataFrame] = []
    next_id = 0
    for size in sizes:
        page = pd.DataFrame({"val": list(range(next_id, next_id + size))})
        pages.append(page)
        next_id += size
    return pages


def _scripted_fetch(pages: List[pd.DataFrame], call_log: List[Tuple[int, int]]):
    """Return a fetch_page callable that yields the given pages in order and records (offset, limit)."""
    iterator = iter(pages)

    def fetch_page(offset: int, limit: int) -> pd.DataFrame:
        call_log.append((offset, limit))
        return next(iterator)

    return fetch_page


def test_paginate_all_pages_single_short_page_returned_as_is():
    pages = _make_fake_pages(3)
    calls: List[Tuple[int, int]] = []
    fetch_page = _scripted_fetch(pages, calls)

    result = paginate_all_pages(fetch_page, page_size=10)

    assert list(result["val"]) == [0, 1, 2]
    assert calls == [(0, 10)]


def test_paginate_all_pages_concatenates_full_pages_until_short_page():
    pages = _make_fake_pages(5, 5, 2)
    calls: List[Tuple[int, int]] = []
    fetch_page = _scripted_fetch(pages, calls)

    result = paginate_all_pages(fetch_page, page_size=5)

    assert list(result["val"]) == list(range(12))
    assert calls == [(0, 5), (5, 5), (10, 5)]


def test_paginate_all_pages_empty_first_page_returns_empty_dataframe():
    pages = _make_fake_pages(0)
    calls: List[Tuple[int, int]] = []
    fetch_page = _scripted_fetch(pages, calls)

    result = paginate_all_pages(fetch_page, page_size=5)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert calls == [(0, 5)]


def test_paginate_all_pages_honours_starting_offset():
    pages = _make_fake_pages(2)
    calls: List[Tuple[int, int]] = []
    fetch_page = _scripted_fetch(pages, calls)

    paginate_all_pages(fetch_page, offset=20, page_size=5)

    assert calls == [(20, 5)]


def test_paginate_all_pages_advances_offset_by_page_size():
    pages = _make_fake_pages(3, 1)
    calls: List[Tuple[int, int]] = []
    fetch_page = _scripted_fetch(pages, calls)

    paginate_all_pages(fetch_page, offset=100, page_size=3)

    assert calls == [(100, 3), (103, 3)]


def test_paginate_all_pages_preserves_index_by_default():
    page = pd.DataFrame({"val": [1, 2]}, index=pd.Index([10, 11], name="id"))
    short = pd.DataFrame({"val": []}, index=pd.Index([], name="id"))
    calls: List[Tuple[int, int]] = []
    fetch_page = _scripted_fetch([page, short], calls)

    result = paginate_all_pages(fetch_page, page_size=2)

    assert list(result.index) == [10, 11]


def test_paginate_all_pages_resets_index_when_ignore_index_true():
    page_a = pd.DataFrame({"val": [1, 2]}, index=pd.Index([10, 11]))
    page_b = pd.DataFrame({"val": [3]}, index=pd.Index([12]))
    calls: List[Tuple[int, int]] = []
    fetch_page = _scripted_fetch([page_a, page_b], calls)

    result = paginate_all_pages(fetch_page, page_size=2, ignore_index=True)

    assert list(result.index) == [0, 1, 2]


# ---------------------------------------------------------------------------
# format_keywords
# ---------------------------------------------------------------------------


def test_format_keywords_none_passes_through():
    assert format_keywords(None) is None


def test_format_keywords_replaces_spaces_with_percent():
    assert format_keywords("hello world") == "hello%world"


def test_format_keywords_joins_iterable_with_percent():
    assert format_keywords(["foo", "bar"]) == "foo%bar"


def test_format_keywords_joins_then_replaces_spaces_within_elements():
    assert format_keywords(["foo", "bar baz"]) == "foo%bar%baz"


def test_format_keywords_single_element_list():
    assert format_keywords(["only"]) == "only"


def test_format_keywords_string_without_spaces_unchanged():
    assert format_keywords("plain") == "plain"


# ---------------------------------------------------------------------------
# validate_sort_by
# ---------------------------------------------------------------------------


def test_validate_sort_by_none_passes_through():
    assert validate_sort_by(None) is None


def test_validate_sort_by_lowercases_input():
    assert validate_sort_by("TITLE_ASC") == "title_asc"


@pytest.mark.parametrize("value", ["title_asc", "title_desc", "updated_asc", "updated_desc"])
def test_validate_sort_by_accepts_all_supported_values(value):
    assert validate_sort_by(value) == value


def test_validate_sort_by_rejects_invalid_value():
    with pytest.raises(ValueError):
        validate_sort_by("created_asc")
