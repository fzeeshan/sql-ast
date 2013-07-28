from ast import Select, From, Where, List, Join

class Query(object):
	"""docstring for Query"""
	def __init__(self, _from):
		self._select = Select(_from)
		self.precompiled = False
		self.inline = False

	def select_from(self, _from):
		self._select._from = From(_from)
		self.precompiled = False
		return self

	def where(self, where):
		self._select.where = Where(where)
		self.precompiled = False
		return self

	def select(self, *args):
		self._select.what = List(*args)
		self.precompiled = False
		return self

	def join(self, what, _on):
		if self.precompiled:
			raise Exception('Cannot join to precompiled query')
		self._select.joins.append(Join(what, _on))
		return self

	def precompile(self):
		self._select._from = str(self._select._from)
		self._select.what = str(self._select.what)
		self._select.where = str(self._select.where)
		self._select.joins = str(self._select.joins)
		self.precompiled = True
		return self

	def __str__(self):
		self._select.inline = self.inline
		s = str(self._select)
		if not self.inline:
			s += ';'
		return s


def query(_from):
	q = Query(_from)
	return q
		