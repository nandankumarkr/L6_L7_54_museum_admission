"""Lab 6 - Part 1: tests written to reach >90% LINE coverage."""
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ---- starter examples ----
def test_adult_weekday():
    assert ticket_price("adult", 30, "tuesday", False) == 300


def test_small_group():
    assert group_discount(4, False) == 0


# ---- ticket_price ----
def test_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("alien", 30, "tuesday", False)


def test_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_free_entry_under_five():
    assert ticket_price("adult", 4, "tuesday", False) == 0


def test_monday_student_with_tour():
    # 150 // 2 = 75, student tour surcharge +50
    assert ticket_price("student", 20, "monday", True) == 125


def test_weekend_adult_with_tour():
    # 300 + 50 weekend + 100 tour
    assert ticket_price("adult", 30, "saturday", True) == 450


# ---- group_discount ----
def test_invalid_group_size():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)


def test_large_school_group():
    assert group_discount(20, True) == 40


def test_small_school_group():
    assert group_discount(5, True) == 25


def test_large_general_group():
    assert group_discount(15, False) == 20


def test_medium_general_group():
    assert group_discount(8, False) == 10


# ---- gallery_entry ----
def test_gallery_full():
    assert gallery_entry(10, 10, False) == "wait"


def test_gallery_queue():
    assert gallery_entry(9, 10, False) == "queue"


def test_gallery_enter():
    assert gallery_entry(2, 10, False) == "enter"
