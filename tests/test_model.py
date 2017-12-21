
from haive import model, hexes
import random
import pytest

@pytest.fixture(autouse=True)
def m():
    m = model.Model()
    yield m
    m.assert_consistent()

lookup_colour = {colour[0]: colour for colour in model.colours}
lookup_kind = {kind[0]: kind for kind in model.kinds}

def add_tokens(m, string, step=6):
    tokens = string.split()
    for factor, token in enumerate(tokens):
        if token == '-':
            pass
        else:
            colour = lookup_colour[token[0]]
            kind = lookup_kind[token[1]]
            for offset in hexes.offsets[::step]:
                m.state[hexes.mul(offset, factor)] = model.Token(colour, kind)

def test_create(m):
    assert m is not None

def test_save_empty(m):
    assert m.save() is not None

def test_save_nonempty(m):
    add_tokens(m, 'wB')
    assert m.save() is not None

def test_save_multiple(m):
    add_tokens(m, 'bb wB bh')
    assert m.save() is not None

def test_neighbours_none(m):
    assert len(m.neighbours(hexes.centre)) == 0

def test_neighbours_some(m):
    add_tokens(m, 'wB wa', step=2)
    assert len(m.neighbours(hexes.centre)) == 3

def test_move_sources_empty(m):
    assert len(m.move_sources()) == 0

def test_move_sources_one(m):
    add_tokens(m, 'wB')
    assert len(m.move_sources()) == 1

def test_move_sources_two(m):
    add_tokens(m, 'wB ba')
    assert len(m.move_sources()) == 2

def test_move_sources_line(m):
    add_tokens(m, 'ba wB ba wh bb ws bs wa')
    assert len(m.state) == 1 + 7
    assert len(m.move_sources()) == 2

def test_move_sources_star(m):
    add_tokens(m, 'ba wB ba wh bb ws bs wa', step=2)
    assert len(m.state) == 1 + 3*7
    assert len(m.move_sources()) == 3

def test_move_sources_loop(m):
    add_tokens(m, '- wB', step=1)
    assert len(m.state) == 6
    assert len(m.move_sources()) == 6

def test_places_empty(m):
    assert len(m.places(model.white)) == 1
    assert len(m.places(model.black)) == 1

def test_places_single(m):
    add_tokens(m, 'wB')
    assert len(m.places(model.white)) == 6
    assert len(m.places(model.black)) == 6

def test_places_pair(m):
    add_tokens(m, 'wB bB')
    assert len(m.places(model.white)) == 3
    assert len(m.places(model.black)) == 3

def test_places_line(m):
    add_tokens(m, 'bB wB bB')
    assert len(m.places(model.white)) == 0
    assert len(m.places(model.black)) == 6

def test_places_dont_intersect(m):
    add_tokens(m, 'bB bB')
    assert len(m.places(model.white)) == 0
    assert len(m.places(model.black)) == 8

def test_bee_destinations_end(m):
    add_tokens(m, 'wB wa wa wa')
    assert len(m.bee_destinations(hexes.centre)) == 2

def test_bee_destinations_middle(m):
    add_tokens(m, 'wB wa wa wa', step=3)
    assert len(m.bee_destinations(hexes.centre)) == 4

def test_bee_destinations_star(m):
    add_tokens(m, 'wB wa wa wa', step=2)
    assert len(m.bee_destinations(hexes.centre)) == 0

def test_bee_destinations_trapped(m):
    add_tokens(m, 'wB wa wa wa', step=1)
    assert len(m.bee_destinations(hexes.centre)) == 0