from processors import CPUProcessor
from qserver import QServer


class QMetric(dict):

	def __init__(self, value):
		dict.__init__(self, value);




class QConfig():


	def __init__(self, processor=CPUProcessor(), metric=QMetric({}), server=QServer()):
		self.processor = processor;
		self.metric = metric
		self.server = server;


	def get_metric(self, qa_state, qb_state):
		if self.metric.keys().__len__() == 0:
			if qa_state == qb_state:
				return 1;
			else :
				return 0;
		else:
			return self.metric[qa_state][qb_state];