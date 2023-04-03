import pytest
from practica_1.problems.missionary_and_cannibals_problem import *
from search import *


@pytest.fixture
def params():
    params = {}
    params['goal_state'] = CannibalAndMissionaryState((3, 3), (0, 0), Side.END)
    params['cannibals_and_missionary_problem'] = MissionariesAndCannibalsProblem(params['goal_state'])
    params['actions_list'] = params['cannibals_and_missionary_problem'].actions_list
    params['initial_state'] = params['cannibals_and_missionary_problem'].initial_state
    return params


def test_move_missionary_not_enable(params):
    action = MoveMissionaryAction()
    assert not action.is_enable(params['initial_state'])


def test_move_two_missionaries_not_enable(params):
    action = MoveTwoMissionaryAction()
    assert not action.is_enable(params['initial_state'])


def test_move_two_cannibals_enable(params):
    action = MoveTwoCannibalAction()
    assert action.is_enable(params['initial_state'])


def test_move_cannibal_is_enable(params):
    action = MoveCannibalAction()
    assert action.is_enable(params['initial_state'])


def test_move_cannibal(params):
    action = MoveCannibalAction()
    state = action.execute(params['initial_state'])
    assert state.begin == (0, 1) and state.end == (3, 2) and state.boat_side == Side.END


def test_move_missionary(params):
    action = MoveMissionaryAction()
    state = action.execute(params['initial_state'])
    assert state.begin == (1, 0) and state.end == (2, 3)


def test_move_two_cannibal(params):
    action = MoveTwoCannibalAction()
    state = action.execute(params['initial_state'])
    assert state.begin == (0, 2) and state.end == (3, 1) and state.boat_side == Side.END


def test_move_two_missionary(params):
    action = MoveTwoMissionaryAction()
    state = action.execute(params['initial_state'])
    assert state.begin == (2, 0) and state.end == (1, 3) and state.boat_side == Side.END


def test_move_one_missionary_one_cannibal(params):
    action = MoveOneCannibalOneMissionaryAction()
    state = action.execute(params['initial_state'])
    assert state.begin == (1, 1) and state.end == (2, 2) and state.boat_side == Side.END


def test_move_two_cannibals_not_enable(params):
    action = MoveMissionaryAction()
    state = action.execute(params['initial_state'])
    action = MoveTwoCannibalAction()
    assert not action.is_enable(state)


def test_move_one_cannibals_not_enable(params):
    action = MoveMissionaryAction()
    state = action.execute(params['initial_state'])
    action = MoveCannibalAction()
    state = action.execute(state)
    assert not action.is_enable(state)


def test_move_one_missionary_enable(params):
    action = MoveTwoCannibalAction()
    state = action.execute(params['initial_state'])
    state = MoveCannibalAction().execute(state)
    action = MoveMissionaryAction()
    assert action.is_enable(state)


def test_move_two_missionary_enable(params):
    state = MoveTwoCannibalAction().execute(params['initial_state'])
    state = MoveCannibalAction().execute(state)
    state = MoveTwoCannibalAction().execute(state)
    state = MoveCannibalAction().execute(state)
    assert MoveTwoMissionaryAction().is_enable(state)


def test_actions_list_initial_state(params):
    state = params['initial_state']
    problem = params['cannibals_and_missionary_problem']
    actions = problem.actions(state)
    assert actions == list(filter(lambda a: not (isinstance(a, MoveTwoMissionaryAction) or
                                            isinstance(a, MoveMissionaryAction))
                                  , problem.actions_list)
                           )


def test_breadth_first_graph_search_missionaries_and_cannibals(params):
    solution = breadth_first_graph_search(params['cannibals_and_missionary_problem']).solution()
    assert True #solutio n == [MTC, MC, MTC, MC, MTM, MC, MTM, MCM, MTM, MC, MTC, MM, MCM]


if __name__ == '__main__':
    pytest.main()
