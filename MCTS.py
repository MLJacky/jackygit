import sys
import math
import random
import numpy as np

AVAILABLE_CHOICES = [1, -1, 2, -2]
AVAILABLE_CHOICE_NUMBER = len(AVAILABLE_CHOICES)
MAX_ROUND_NUMBER = 10

class State(object):
	"""
	MCTS的游戏状态，记录在某一个Node节点下的状态数据，包含当前的游戏得分、当前游戏的round、从开始到当前的执行记录。
	需要实现判断当前状态是否达到结束，支持从Action集合中随机去除操作。
	"""

	def __init__(self):
		self.current_value = 0.0
		self.current_round_index = 0
		self.cumulative_choices = hero_dict

	def get_current_value(self):
		return self.current_value

	def set_current_value(self, value):
		self.current_value = value

	def get_current_round_index(self):
		return self.current_round_index

	def set_current_round_index(self, turn):
		self.current_round_index = turn

	def get_cumulative_choices(self):
		return self.cumulative_choices

	def set_cumulative_choices(self, choices):
		self.cumulative_choices = choices

	def is_terminal(self):
		#The round index starts from 1 to max round number
		if self.current_round_index == MAX_ROUND_NUMBER:
			return True
		else:
			return False

	def compute_reward(slef):
		return -abs(1-self.current_value)

	def get_next_state_with_random_choice(self):
		random_choice = random.choice([choice for choice in AVAILABLE_CHOICES])

		next_state = State()
		next_state.set_current_value(self.current_value + random_choice)
		next_state.set_current_round_index(self.current_round_index + 1)
		next_state.set_cumulative_choices(self.cumulative_choices+[random_choice])