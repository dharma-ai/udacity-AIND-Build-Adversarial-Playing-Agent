
from sample_players import DataPlayer
import random

class CustomPlayer(DataPlayer):
    """ Implement customized agent to play knight's Isolation """

    def get_action(self, goalState):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least
        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.
        See RandomPlayer and GreedyPlayer in sample_players for more examples.
        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        if goalState.ply_count < 2:
            self.queue.put(random.choice(goalState.actions()))
        else:
            self.queue.put(self.alpha_beta_search(goalState, 3))
        
    def alpha_beta_search(self, goalState, depth):    

        def min_value(goalState, depth, alpha, beta):
            if goalState.terminal_test(): return goalState.utility(self.player_id)
            if depth <= 0 : return self.score(goalState)
            value = float("inf")
            for action in goalState.actions():
                value = min(value, max_value(goalState.result(action), depth - 1, alpha, beta))
                if value <= alpha: return value
                beta = min(beta, value)
            return value 

        def max_value(goalState, depth, alpha, beta):
            if goalState.terminal_test(): return goalState.utility(self.player_id)
            if depth <= 0 : return self.score(goalState)
            value = float("-inf")
            for action in goalState.actions():
                value = max(value, min_value(goalState.result(action), depth - 1, alpha, beta))
                if value >= beta: return value
                alpha = max(alpha, value)
            return value
        
        return max(goalState.actions(), key=lambda x: min_value(goalState.result(x), depth - 1, float('-inf'), float('inf')))       
        
    def score(self, goalState):
        my_loc = goalState.locs[self.player_id]
        opp_loc = goalState.locs[1 - self.player_id]
        my_liberties = goalState.liberties(my_loc)     
        opp_liberties = goalState.liberties(opp_loc)
        future_my_liberties = sum(len(goalState.liberties(l)) for l in my_liberties)
        future_opp_liberties = sum(len(goalState.liberties(l)) for l in opp_liberties)
        return len(my_liberties) - 2 * len(opp_liberties) +  future_my_liberties - 2 * future_opp_liberties        

