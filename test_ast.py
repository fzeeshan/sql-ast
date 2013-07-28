from ast import *

fields = List('maker', 'mark', 'year')
_from = 'cars'
where = And('year>2010', 'maker="Dodge"')

select = Select(_from, fields, where)
print select

select = Select(select, fields, where)
print select

select = Select(_from, fields)
print select


delete = Delete(_from, returning=_all)
print delete

delete = Delete(_from, returning=fields)
print delete

delete = Delete(_from, returning=fields, where=Or('maker=1', And('1=1', Or('mark="Audi"', 'year<>2012'))))
print delete


insert = Insert(_from)
print insert

fields = List('maker', 'mark', 'year')
template = List('%(maker)s', '%(mark)s', '%(year)s')
insert = Insert(_from, fields=fields, values=template)
print insert


update = Update('cars', {'year': 2010}, returning=_all)
print update

update = Update('cars', {'year': 2010}, where=where, returning='id')
print update

update = Update('cars', {'year': 2010}, _from=Select('jobs'), where=where, returning='id')
print update
