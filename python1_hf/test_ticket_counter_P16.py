from P16_ticket_counter import ticket_counter
import pytest


def test_ticket_counter_regular():
    assert 350 == ticket_counter(350, 30, 100)


def test_ticket_counter_baby():
    assert 0 == ticket_counter(350, 1, 100)


def test_ticket_counter_pensioner():
    assert 0 == ticket_counter(350, 65, 100)


def test_ticket_counter_youth():
    assert 175 == ticket_counter(350, 17, 100)


def test_ticket_counter_youth2():
    assert 175 == ticket_counter(350, 6, 100)


def test_ticket_counter_regular_distance_101():
    assert 700 == ticket_counter(350, 30, 101)


def test_ticket_counter_regular_distance_200():
    assert 700 == ticket_counter(350, 30, 200)


def test_ticket_counter_regular_distance_201():
    assert 1050 == ticket_counter(350, 30, 201)
