from structure import BaseAIPlayer
from GomokuBoard import GomokuBoard

class MiniMaxAIPlayer(BaseAIPlayer):
    __corners = None
    __depth = 3
    def __init__(self, board: GomokuBoard ):
        super().__init__(board)

    def minimax(self, maximizingPlayer : bool ,depth: int ) -> int:
        if self.board.is_winner():
            return 500000000 - self.board.moves()
        elif self.board.moves() == 225:
            return 0
        elif depth ==0 :
            return self.board.heuristic()
            

        if(maximizingPlayer):
            maxEval = -500000000
            for i in range(225):
                if self.board.update_board(i):
                    eval = self.minimax( False, depth-1)
                    maxEval = max(maxEval, eval)
                    self.board.reset(i)
            return maxEval                    
        else:
            minEval = 500000000
            for i in range(225):
                if self.board.update_board(i):
                    eval = self.minimax( True, depth-1)
                    minEval = min(minEval, eval)
                    self.board.reset(i)
            return minEval


    def get_move(self) -> int:
        maximizingPlayer = (self.board.moves() % 2) == 0 
        index = -1
        if(maximizingPlayer):
            maxEval = -500000000
            for i in range(225):
                if self.board.update_board(i):
                    value = self.minimax( False ,self.__depth -1)
                    if(value > maxEval):
                        index = i
                        maxEval = value    
                    
                    self.board.reset(i)                   
        else:
            minEval = 500000000
            for i in range(225):
                if self.board.update_board(i):
                    value = self.minimax( True, self.__depth -1)
                    if(value < minEval):
                        index = i
                        minEval = value 
                    self.board.reset(i)
        if(index == -1):
            raise ValueError("george is stupid")
        return index 
            

        

    
