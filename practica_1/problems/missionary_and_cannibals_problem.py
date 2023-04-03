from enum import Enum

from practica_1.problems.abstractproblem import State, Actions, MyProblem


class MissionariesAndCannibalsProblem(MyProblem):
    def __init__(self, goal=None):
        initial_state = CannibalAndMissionaryState((3, 3), (0, 0), Side.BEGIN)
        action_list = [MoveMissionaryAction(), MoveCannibalAction(), MoveTwoMissionaryAction(),
                       MoveTwoCannibalAction(), MoveOneCannibalOneMissionaryAction()
                       ]
        super().__init__(initial_state, action_list, goal)


class Side(Enum):
    BEGIN = 0
    END = 1


class CannibalAndMissionaryState(State):
    begin = (3, 3)  # 1st missionary 2nd cannibal
    end = (0, 0)  # 1st missionary 2nd cannibal
    boat_side = Side.BEGIN

    def __init__(self, begin, end, boat_side):
        self.begin = begin
        self.end = end
        self.boat_side = boat_side

    def __eq__(self, other):
        if isinstance(other, CannibalAndMissionaryState):
            return (self.begin, self.end, self.boat_side) == (
                other.begin, other.end, other.boat_side)
        return False

    def __hash__(self):
        return hash((self.begin, self.end, self.boat_side))

    def is_goal(self):
        return self.begin == (3, 3) and self.end == (0, 0) and self.boat_side == Side.END

    def rep_ok(self):
        return self.begin[0] - self.begin[1] < 0 and self.end[0] - self.end[1] < 0

    def change_side(self):
        if self.boat_side == Side.BEGIN:
            return Side.END
        else:
            return Side.BEGIN


class MoveMissionaryAction(Actions):
    def is_enable(self, state):
        return departure_is_enable(state, 1, 0) and arrive_is_enable(state, 1, 0)

    def execute(self, state, n=1):
        missionaries_begin = state.begin[0]
        cannibals_begin = state.begin[1]
        missionaries_end = state.end[0]
        cannibals_end = state.end[1]
        end = (missionaries_begin - n, cannibals_begin)
        begin = (missionaries_end + n, cannibals_end)
        new_state = CannibalAndMissionaryState(begin, end, state.change_side())
        return new_state


class MoveCannibalAction(Actions):
    def is_enable(self, state):
        return departure_is_enable(state, 0, 1) and arrive_is_enable(state, 0, 1)

    def execute(self, state, n=1):
        missionaries_begin = state.begin[0]
        cannibals_begin = state.begin[1]
        missionaries_end = state.end[0]
        cannibals_end = state.end[1]
        end = (missionaries_begin, cannibals_begin - n)
        begin = (missionaries_end, cannibals_end + n)
        new_state = CannibalAndMissionaryState(begin, end, state.change_side())
        return new_state


def departure_is_enable(state, missionaries, cannibals):
    current_missionaries = state.begin[0] - missionaries
    current_cannibals = state.begin[1] - cannibals
    return current_missionaries >= 0 and current_cannibals >= 0 and (
            current_missionaries - current_cannibals >= 0 or current_missionaries == 0)


def arrive_is_enable(state, missionaries, cannibals):
    current_missionaries = state.end[0] + missionaries
    current_cannibals = state.end[1] + cannibals
    return current_missionaries - current_cannibals >= 0 or current_missionaries == 0


class MoveTwoMissionaryAction(Actions):
    def is_enable(self, state):
        return departure_is_enable(state, 2, 0) and arrive_is_enable(state, 2, 0)

    def execute(self, state):
        action = MoveMissionaryAction()
        return action.execute(state, 2)


class MoveTwoCannibalAction(Actions):
    def is_enable(self, state):
        return departure_is_enable(state, 0, 2) and arrive_is_enable(state, 0, 2)

    def execute(self, state):
        action = MoveCannibalAction()
        return action.execute(state, 2)


class MoveOneCannibalOneMissionaryAction(Actions):
    def is_enable(self, state):
        return departure_is_enable(state, 1, 1) and arrive_is_enable(state, 1, 1)

    def execute(self, state):
        missionaries_begin = state.begin[0]
        cannibals_begin = state.begin[1]
        missionaries_end = state.end[0]
        cannibals_end = state.end[1]
        end = (missionaries_begin - 1, cannibals_begin - 1)
        begin = (missionaries_end + 1, cannibals_end + 1)
        new_state = CannibalAndMissionaryState(begin, end, state.change_side())
        return new_state
