from pymongo import MongoClient
from datetime import datetime

class Database():


	def __init__(self, dbpath, dbtype=None, url=None):
		self.type= dbtype;
		self.url = url
		self.path = dbpath;



	def save(self, o, name=None, collection=None):
		if self.type == None:
			name = self.path+'/temp_'+str(gen_uid()) if name==None else self.path+"/"+name;
			with open(name, 'w') as f:
				file = f.dump(o.to_json());
				f.close();
		else:
			name = 'temp_'+str(gen_uid()) if name==None else name;
			db = MongoClient(self.url).Db('db')
			return db[collection].insert_many([{'name': name, 'data': o.to_json(), 'created_at': datetime()}]);




class QDatabase():



	def __init__():
		pass



	def save(self):
		pass



	def update(self):
		pass



	def get(self):
		pass



	def search(self):
		pass




	def delete(self):
		pass