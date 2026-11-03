"""Lab 6 - Part 2: tests written to reach >90% BRANCH coverage (aiming for 100%)."""
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ---------------- ticket_price: error paths ----------------
def test_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("alien", 30, "tuesday", False)


def test_unknown_category_checked_before_age():
    # category validation runs first, even for a "free" age
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("alien", 3, "tuesday", False)


def test_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


# ---------------- ticket_price: age boundary ----------------
@pytest.mark.parametrize("age, expected", [(0, 0), (4, 0), (5, 300)])
def test_age_boundary(age, expected):
    assert ticket_price("adult", age, "tuesday", False) == expected


# ---------------- ticket_price: day branches ----------------
@pytest.mark.parametrize(
    "category, day, expected",
    [
        ("adult", "tuesday", 300),    # neither monday nor weekend
        ("adult", "monday", 150),     # half price
        ("child", "monday", 50),
        ("senior", "monday", 100),
        ("adult", "saturday", 350),   # weekend surcharge
        ("child", "sunday", 150),
    ],
)
def test_day_pricing(category, day, expected):
    assert ticket_price(category, 30, day, False) == expected


# ---------------- ticket_price: guided tour branches ----------------
@pytest.mark.parametrize(
    "category, day, expected",
    [
        ("adult", "tuesday", 400),    # +100 non-student
        ("student", "tuesday", 200),  # +50 student
        ("student", "monday", 125),   # 75 + 50
        ("senior", "sunday", 350),    # 200 + 50 + 100
    ],
)
def test_guided_tour(category, day, expected):
    assert ticket_price(category, 30, day, True) == expected


def test_no_tour_has_no_surcharge():
    assert ticket_price("student", 30, "tuesday", False) == 150


# ---------------- group_discount ----------------
@pytest.mark.parametrize("size", [0, -3])
def test_invalid_group_size(size):
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(size, False)


@pytest.mark.parametrize(
    "size, is_school, expected",
    [
        (1, True, 25), (19, True, 25),     # school below threshold
        (20, True, 40), (50, True, 40),    # school at/above threshold
        (1, False, 0), (7, False, 0),      # general: no discount
        (8, False, 10), (14, False, 10),   # general: medium
        (15, False, 20), (100, False, 20), # general: large
    ],
)
def test_group_discount(size, is_school, expected):
    assert group_discount(size, is_school) == expected


# ---------------- gallery_entry ----------------
@pytest.mark.parametrize(
    "inside, capacity, slot, expected",
    [
        (10, 10, False, "wait"),   # exactly full
        (11, 10, True, "wait"),    # over capacity, slot irrelevant
        (9, 10, False, "queue"),   # 90% full, no slot
        (9, 10, True, "enter"),    # 90% full but has timed slot
        (8, 10, False, "enter"),   # below 90%
        (0, 10, False, "enter"),   # empty
    ],
)
def test_gallery_entry(inside, capacity, slot, expected):
    assert gallery_entry(inside, capacity, slot) == expected
