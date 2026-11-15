import pytest
from cs50project import pair_buy, pair_sell, spread_deque, deque_mean, deque_std_dev, deque_z_score, signal

def test_pair_buy():
    assert pair_buy([100, 200], [1, 10], [[100, 1], [200, 10]], 0, 1000, 0, 0, 0.001) == 5.4945
def test_pair_sell():
    ...
def test_spread_deque():
    ...
def test_deque_mean():
    assert deque_mean([1]) == 1
    assert deque_mean([1000, 1000, 1000, 500, 500, 500, 500, 3000]) == 1000

def test_deque_std_dev():
    assert deque_std_dev([0]) == 0.0
    assert deque_std_dev([1,2,3,4,5]) == 1.4142135623730951

def test_deque_z_score():
    assert deque_z_score([1, 2], 3/2, 0) == None
    assert deque_z_score([1, 2], 3/2, 1.4142135623730951) ==  0.35355339059327373

def test_signal():
    assert signal([1,2,3], 0, 0, 0, 0, "SIGNAL ACHAT", "ATTENTE", 0, 0) == "Window length inadequate, should be 10"
    assert signal([30.0] * 20, 0,0,0,0, "SIGNAL ACHAT", "ATTENTE", 0, 0) == "Standard deviation is equal to 0"
    