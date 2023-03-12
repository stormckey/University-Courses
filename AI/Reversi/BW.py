# 导入随机包
from board import Board
import random
import copy
import math
import time

class RandomPlayer:
    """
    随机玩家, 随机返回一个合法落子位置
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color
        

    def random_choice(self, board):
        """
        从合法落子位置中随机选一个落子位置
        :param board: 棋盘
        :return: 随机合法落子位置, e.g. 'A1' 
        """
        # 用 list() 方法获取所有合法落子位置坐标列表
        action_list = list(board.get_legal_actions(self.color))

        # 如果 action_list 为空，则返回 None,否则从中选取一个随机元素，即合法的落子坐标
        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        action = self.random_choice(board)
        return action

class HumanPlayer:
    """
    人类玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color
    

    def get_move(self, board):
        """
        根据当前棋盘输入人类合法落子位置
        :param board: 棋盘
        :return: 人类下棋落子位置
        """
        # 如果 self.color 是黑棋 "X",则 player 是 "黑棋"，否则是 "白棋"
        if self.color == "X":
            player = "黑棋"
        else:
            player = "白棋"

        # 人类玩家输入落子位置，如果输入 'Q', 则返回 'Q'并结束比赛。
        # 如果人类玩家输入棋盘位置，e.g. 'A1'，
        # 首先判断输入是否正确，然后再判断是否符合黑白棋规则的落子位置
        while True:
            action = input(
                    "请'{}-{}'方输入一个合法的坐标(e.g. 'D3'，若不想进行，请务必输入'Q'结束游戏。): ".format(player,
                                                                                 self.color))

            # 如果人类玩家输入 Q 则表示想结束比赛
            if action == "Q" or action == 'q':
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                # 检查人类输入是否正确
                if row in '12345678' and col in 'ABCDEFGH':
                    # 检查人类输入是否为符合规则的可落子位置
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("你的输入不合法，请重新输入!")



class TreeNode:
    def __init__(self,board,color,parent,time=0,reward=0,action=""):
        self.board = board
        self.time = time 
        self.reward = reward
        self.color = color
        self.children=[]
        self.UCB = 0
        self.action = action
        self.parent = parent
    def add_child(self,treenode):
        self.children.append(treenode)
    
class AIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """

        self.color = color
        self.totaltime =0
    def initial_tree(self,board):
        """从头开始创建树"""
        self.root = TreeNode(board,self.rev(self.color),0)
        

    def UCTSearch(self,board):
        # board.display()
        self.initial_tree(board)
        t_begin = time.perf_counter()
        while time.perf_counter() - t_begin< 3 :
            leaf = self.SelectPolicy(self.root)
            # leaf.board.display()
            expanded = self.expand(leaf)
            if expanded == self.root:
                break
        # expanded.board.display()
            res = self.SimulatePolicy(expanded)
            self.BackPropogate(res,expanded)
            self.totaltime += 1
            # print(self.root.time)
            # print(self.root.reward)
        best = self.root.children[0]
        bestUCB = self.UCB(self.root.children[0],1)
        for child in self.root.children[1:] :
            if self.UCB(child,1)>bestUCB :
                bestUCB = self.UCB(child,1)
                best = child
        return best.action
        # new = self.SelectPolicy(self.root)
        # new.board.display()
        # expanded = self.expand(new)
        # res = self.SimulatePolicy(expanded)
        # self.BackPropogate(res,expanded)
        # self.totaltime += 1
        # print(self.root.time)
        # print(self.root.reward)
        # new = self.SelectPolicy(self.root)
        # new.board.display()
        # expanded = self.expand(new)
        # res = self.SimulatePolicy(expanded)
        # self.BackPropogate(res,expanded)
        # self.totaltime += 1
        # print(self.root.time)
        # print(self.root.reward)
        # new = self.SelectPolicy(self.root)
        # new.board.display()
        # expanded = self.expand(new)
        # res = self.SimulatePolicy(expanded)
        # self.BackPropogate(res,expanded)
        # self.totaltime += 1
        # print(self.root.time)
        # print(self.root.reward)
        # new = self.SelectPolicy(self.root)
        # new.board.display()
        # expanded = self.expand(new)
        # expanded.board.display()
        # res = self.SimulatePolicy(expanded)
        # print(res)
        # expanded.board.display()
        # self.BackPropogate(res,expanded)
        # self.totaltime = 1
        # print(self.root.time)
        # print(self.root.reward)

            # print(time.perf_counter() - t_begin)
    def BackPropogate(self,res,v):
        while v!= self.root:
            if v.color == "X" :
                res = abs(res)
            if v.color == "O" :
                res = -abs(res)
            v.time += 1
            v.reward += res
            # v.board.display()
            # print(v.time)
            # print(v.reward)
            v = v.parent
        res *= -1
        v.reward += res 
        v.time += 1

    def SimulatePolicy(self,tree):
        state = copy.deepcopy(tree)
        while list(state.board.get_legal_actions("X")) or list(state.board.get_legal_actions("O")):
            if list(state.board.get_legal_actions(self.rev(state.color))):
                action = random.choice(list(state.board.get_legal_actions(self.rev(state.color))))
                state.board._move(action,self.rev(state.color))
            state.color = self.rev(state.color)
            # state.board.display()
        winner,number = state.board.get_winner()
        # state.board.display()
        if winner == 2:
            winner = 0.5
        elif winner == 1:
            winner =0
        elif winner == 0:
            winner = 1
        return winner


    def expand(self,leaf):
        if not(list(leaf.board.get_legal_actions("X")) or list(leaf.board.get_legal_actions("O"))):
            return self.root
        if list(leaf.board.get_legal_actions(self.rev(leaf.color))):
            action_list = list(leaf.board.get_legal_actions(self.rev(leaf.color)))
            # for child in leaf.children :
            #     print(child.action)
            # print(action_list)
            for child in leaf.children:
                if child.action in action_list :
                    action_list.remove(child.action)
            # if not action_list:
                # return self.root
            action = random.choice(action_list)
            newboard = copy.deepcopy(leaf.board)
            newboard._move(action,self.rev(leaf.color))
            newtree = TreeNode(newboard,self.rev(leaf.color),leaf,action = action)
            leaf.children.append(newtree)
        else:
            newboard = copy.deepcopy(leaf.board)
            newtree = TreeNode(newboard,self.rev(leaf.color),leaf)
            leaf.children.append(newtree)
        return newtree
    
    def SelectPolicy(self,root):
        now_node = root
        # print(len(now_node.children))
        # print(list(now_node.board.get_legal_actions(.color)))
        while now_node.children and len(list(now_node.board.get_legal_actions(self.rev(now_node.color))))==len(now_node.children):
            bestUCB = self.UCB(now_node.children[0],1)
            best = now_node.children[0]
            for child in now_node.children[1:]:
                # print(self.UCB(child,1))
                if self.UCB(child,1) > bestUCB :
                    bestUCB = self.UCB(child,1)
                    best = child
            now_node = best
        return now_node

    def UCB(self,node,C):
        return node.reward/node.time + C*math.sqrt(2*math.log(self.totaltime)/node.time)

    def rev(self,color):
        if color == "X" :
            return "O"
        return "X"

                
                


    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------
        action = None
        if board.get_legal_actions(self.color):
            action = self.UCTSearch(board)
        # ------------------------------------------------------------------------

        return action

# board = Board()
# aiplayer = AIPlayer("X")
# print(aiplayer.UCTSearch(board))
# aiplayer.initial_tree(board)
# aiplayer.SelectPolicy(aiplayer.tree)
# aiplayer.tree.board.display()
# aiplayer.UCTSearch(board)
# 导入黑白棋文件
from game import Game  

# 人类玩家黑棋初始化
black_player = AIPlayer("X")

# 随机玩家白棋初始化
white_player = RandomPlayer("O")

# 游戏初始化，第一个玩家是黑棋，第二个玩家是白棋
game = Game(black_player, white_player)

# 开始下棋
game.run()