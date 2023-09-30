import os
class Strategy:
    def __init__(self):
        pass

    def create_strat_dir(self):
        # Create a directory for the strategy if it doesn't exist.
        curr_dir = os.path.dirname(os.path.dirname(__file__))
        strategy_dir = os.path.join(curr_dir, self.strat_name)
        if not os.path.exists(strategy_dir):
            os.mkdir(strategy_dir)