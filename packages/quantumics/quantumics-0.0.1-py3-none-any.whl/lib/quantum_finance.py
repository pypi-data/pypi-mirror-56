from quantumics import QUnit, QTUnit, QData, QTData, Operator, Quantumic, Quantumics
from processors import Processor;
from mappings import Map;






class QFinance(QData, Operator, Hilbertspace):


	def __init__(self, processor=Processor(database=Database()), mapping=Map(), hilbertspace=Hilbertspace()):
		self.processor = processor;