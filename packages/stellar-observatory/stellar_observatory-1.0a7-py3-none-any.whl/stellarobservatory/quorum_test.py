"""Tests for quorum functions"""
import pytest
from .utils.sets import deepfreezesets
from .quorum import remove_from_qset_definition, get_normalized_qset_definition, \
    get_minimal_quorum_intersection, generate_quorum_slices, quorum_intersection

QSET_DEFINITION = {'threshold': 2, 'validators': ['A', 'B', 'C'], 'innerQuorumSets': []}
QSET_DEFINITION_WITHOUT_B = {'threshold': 1, 'validators': ['A', 'C'], 'innerQuorumSets': []}

@pytest.mark.parametrize('qset_definition,node,expected', [
    (QSET_DEFINITION, 'B', QSET_DEFINITION_WITHOUT_B),
    (
        {'threshold': 2, 'validators': ['D', 'E'], 'innerQuorumSets': [QSET_DEFINITION]},
        'B',
        {'threshold': 2, 'validators': ['D', 'E'], 'innerQuorumSets': [QSET_DEFINITION_WITHOUT_B]}
    )
])
def test_removal(qset_definition, node, expected):
    """Test remove_from_qset_definition()"""
    result = remove_from_qset_definition(qset_definition, node)
    assert result == expected


def test_normalization():
    """Test get_normalized_qset_definition()"""
    node = {
        'publicKey': 'B',
        'quorumSet': QSET_DEFINITION
    }
    normalized_qset_definition = get_normalized_qset_definition(node)
    expected_qset_definition = {
        'threshold': 2,
        'validators': ['B'],
        'innerQuorumSets': [QSET_DEFINITION_WITHOUT_B]
    }
    assert normalized_qset_definition == expected_qset_definition

def test_qslice_generation():
    """Test generate_quorum_slices()"""
    expected_sets_economic = deepfreezesets([{'A', 'B'}, {'A', 'C'}, {'B', 'C'}])
    result_economic = generate_quorum_slices(QSET_DEFINITION)
    assert deepfreezesets(result_economic) == expected_sets_economic
    expected_sets_full = set(expected_sets_economic)
    expected_sets_full.add(frozenset(['A', 'B', 'C']))
    result_full = generate_quorum_slices(QSET_DEFINITION, mode='full')
    assert deepfreezesets(result_full) == expected_sets_full

def test_quorum_intersection():
    """Test quorum_intersection()"""
    quorums = deepfreezesets([{'A', 'B'}, {'A', 'C'}, {'B', 'C'}])
    has_intersection, intersection_quorums, split_quorums = \
        quorum_intersection(quorums)
    assert has_intersection is True
    assert len(intersection_quorums) == 3
    assert not split_quorums

def test_quorum_intersection_fail():
    """Test quorum_intersection()"""
    quorums = deepfreezesets([{'A', 'B'}, {'B', 'C'}, {'C', 'D'}])
    has_intersection, intersection_quorums, split_quorums = \
        quorum_intersection(quorums)
    assert has_intersection is False
    assert len(intersection_quorums) == 2
    assert len(split_quorums) == 1
    assert frozenset(split_quorums[0]) == deepfreezesets([{'A', 'B'}, {'C', 'D'}])

def test_minimal_intersection():
    """Test get_minimal_quorum_intersection()"""
    quorums = deepfreezesets([{'A', 'B'}, {'A', 'C'}, {'B', 'C'}])
    intersection, quorum_a, quorum_b = get_minimal_quorum_intersection(quorums)
    assert len(intersection) == 1
    assert len(quorum_a.intersection(quorum_b)) == 1

def test_minimal_intersection_fail():
    """Test get_minimal_quorum_intersection()"""
    quorums = deepfreezesets([{'A', 'B'}, {'B', 'C'}, {'C', 'D'}])
    intersection, quorum_a, quorum_b = get_minimal_quorum_intersection(quorums)
    assert intersection is None
    assert quorum_a.intersection(quorum_b) == set()
