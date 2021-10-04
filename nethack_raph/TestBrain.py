from nethack_raph.Brain import *
from nethack_raph.Pathing import dijkstra_pathing, mcp_pathing, check_neighbours
from nethack_raph.myconstants import DUNGEON_WIDTH


class TestBrain(Brain):
    def __init__(self, kernel):
        Brain.__init__(self, "TestBrain", kernel)

        self.actions = {
            'Elbereth': Elbereth(kernel),
            'RestoreHP': RestoreHP(kernel),
            'AttackMonster': AttackMonster(kernel),
            'EatFromInventory': EatFromInventory(kernel),
            'Eat': Eat(kernel),
            'Pray': Pray(kernel),
            'PickUpStuff': PickUpStuff(kernel),
            'FixStatus': FixStatus(kernel),
            'Explore': Explore(kernel),
            'OpenDoors': OpenDoors(kernel),
            # 'Descend': Descend(kernel),
            'Search': Search(kernel),
            'RandomWalk': RandomWalk(kernel),
        }
        self.prev_action = -1
        self.prev_path = []

    def execute_next(self, level):
        for action, action_instance in self.actions.items():
            can_act, coords = action_instance.can(level)
            if not can_act:
                action_instance.after_search(None)
                continue

            path = self.find_path(level, coords, action)
            action_instance.after_search(path)
            if path is not None:
                self.prev_action, self.prev_path = action, path
                self.kernel().log(f'found path length {len(path)} for {action}')
                action_instance.execute(path)
                return
            else:
                self.kernel().log(f"Didn't find path for {action}")

    def find_path(self, level, coords, action):
        if coords[self.kernel().hero.coords()]:  # we are at the aim already
            return [self.kernel().hero.coords()]

        start = int(self.kernel().hero.x * DUNGEON_WIDTH + self.kernel().hero.y)
        flat_coords = coords.reshape(-1)

        use_prev_path = True
        if action != self.prev_action:  # doing not the same action as before
            use_prev_path = False
        elif len(self.prev_path) <= 3:  # less then 2 steps remaining
            use_prev_path = False
        elif self.prev_path[-2] != self.kernel().hero.coords():  # didn't make a step to the right direction
            use_prev_path = False
        elif level.tiles.walk_cost[self.prev_path[-3]] != 1:  # Next step is not save
            use_prev_path = False
        elif check_neighbours(start, flat_coords):  # there is a goal nearby
            use_prev_path = False

        if use_prev_path:
            self.kernel().log(f'Use previous path')
            return self.prev_path[:-1]

        path = dijkstra_pathing(level.tiles.walk_cost.reshape(-1), start, [lambda _, xy: flat_coords[xy]])[0]

        return path
