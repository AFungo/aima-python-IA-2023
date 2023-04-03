import pytest
from practica_1.problems.abstractproblem import *
from practica_1.problems.missionary_and_cannibals_problem import *
from search import *

actions_list = [MoveMissionaryAction()]
goal_state = CannibalAndMissionaryState((0, 0), (3, 3))
initial_state = CannibalAndMissionaryState((0, 0), (3, 3)).initial_state()
# cannibals_and_missionary_problem = Problem(initial_state, goal_state, actions_list)

romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)


# _move_missionary_is_enable
# def test_missionary():
#     action = MoveMissionaryAction()
#     assert action.is_enable(initial_state) == True

def test_depth_first_search():
    assert depth_first_tree_search(romania_problem).solution() == ['Timisoara', 'Lugoj', 'Mehadia', 'Drobeta',
                                                                   'Craiova', 'Pitesti', 'Bucharest']


if __name__ == '__main__':
    pytest.main()
