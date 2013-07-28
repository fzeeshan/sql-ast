from query import query

q = query('cars')\
		.select('a', query('mark').where('1=1'))\
		.join('maker', 'maker.x="audi"')\
		.where('year=1950')

print q
