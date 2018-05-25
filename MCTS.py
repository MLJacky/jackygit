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
		self.cumulative_choices = []

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

	def compute_reward(self):
		return -abs(1-self.current_value)

	def get_next_state_with_random_choice(self):
		random_choice = random.choice([choice for choice in AVAILABLE_CHOICES])

		next_state = State()
		next_state.set_current_value(self.current_value + random_choice)
		next_state.set_current_round_index(self.current_round_index + 1)
		next_state.set_cumulative_choices(self.cumulative_choices+[random_choice])

		return next_state

	def __eq__(self, other):
		if hash(self) == hash(other):
			return True
		return False

	def __repr__(self):
		return "State:{}, value:{}, round:{}, choices:{}".format(
			hash(self),self.current_value,self.current_round_index,self.cumulative_choices)

class Node(object):



	def __init__(self):
		self.parent = None
		self.children = []

		self.visit_times = 0
		self.quality_value = 0.0

		self.state = None

	def set_state(self, state):
		self.state = state

	def get_state(self):
		return self.state

	def get_parent(self):
		return self.parent

	def set_parent(self, parent):
		self.parent = parent

	def get_children(self):
		return self.children

	def get_visit_times(self):
		return self.visit_times

	def visit_times_add_one(self):
		self.visit_times +=1

	def set_visit_times(self,times):
		self.visit_times = times

	def get_quality_value(self):
		return self.quality_value

	def set_quality_value(self, value):
		self.quality_value = value

	def quality_value_add_n(self, n):
		self.quality_value+=n

	def is_all_expand(self):
		if len(self.children) == AVAILABLE_CHOICE_NUMBER:
			return True
		else:
			return False

	def add_child(self,sub_node):
		sub_node.set_parent(self)
		self.children.append(sub_node)

	def __repr__(self):
		return "Node:{}, Q/N:{},state:{}".format(
			hash(self),self.quality_value, self.visit_times, self.state)

def tree_policy(node):
	while node.get_state().is_terminal() == False:
		if node.is_all_expand():
			node = best_child(node, True)
		else:
			sub_node = expand(node)
			return sub_node

	return node

def default_policy(node):

	current_state = node.get_state()

	while current_state.is_terminal() == False:
		current_state = current_state.get_next_state_with_random_choice()

	final_state_reward = current_state.compute_reward()
	return final_state_reward

def expand(node):

	tried_sub_node_states = [
		sub_node.get_state() for sub_node in node.get_children()
	]

	new_state = node.get_state().get_next_state_with_random_choice()

	while new_state in tried_sub_node_states:
		new_state = node.get_state().get_next_state_with_random_choice()

	sub_node = Node()
	sub_node.set_state(new_state)
	node.add_child(sub_node)

	return sub_node

def best_child(node, is_exploration):
	best_score = -sys.maxsize
	best_sub_node = None

	for sub_node in node.get_children():

		if is_exploration:
			C = 1/math.sqrt(2.0)
		else:
			C = 0.0

		left = sub_node.get_quality_value() / sub_node.get_visit_times()
		right = 2.0 * math.log(node.get_visit_times()) / sub_node.get_visit_times()
		score = left + C * math.sqrt(right)

		if score > best_score:
			best_sub_node = sub_node
			best_score = score

	return best_sub_node

def backup(node, reward):
	while node != None:
		node.visit_times_add_one()

		node.quality_value_add_n(reward)

		node = node.parent

def monte_carlo_tree_search(node):

	computation_budget = 2

	for i in range(computation_budget):
		expand_node = tree_policy(node)

		reward = default_policy(expand_node)

		backup(expand_node, reward)

	best_next_node = best_child(node, False)

	return best_next_node

def main():
	init_state = State()
	init_node = Node()
	init_node.set_state(init_state)
	current_node = init_node

	for i in range(10):
		print("Play round:{}".format(i+1))
		current_node = monte_carlo_tree_search(current_node)
		print("choose node:{}".format(current_node))

if __name__ == "__main__":
	main()