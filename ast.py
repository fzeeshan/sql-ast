empty = ''
_all = '*'


class ASTNode(object):
    visited = False
    inline = False
    
    def __init__(self):
        pass
    
    def children(self):
        for c in self._children:
            yield c

    def __str__(self):
        pass


class BinaryNode(ASTNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '({left} {middle} {right})'.format(
            left=self.left,
            middle=self.middle,
            right=self.right
        )


class And(BinaryNode):
    middle = 'AND'


class Or(BinaryNode):
    middle = 'OR'


class List(ASTNode):

    def __init__(self, *args):
        for arg in args:
            if hasattr(arg, 'inline'):
                arg.inline = True
        self.items = args

    def __str__(self):
        lst = ', '.join(map(lambda x: str(x), self.items))
        if self.inline:
            lst = '(' + lst + ')'
        return lst


class Set(ASTNode):

    def __init__(self, **kwargs):
        self.items = kwargs

    def __str__(self):
        return ', '.join(['{0}={1}'.format(key, val) for key, val in self.items.items()])


class Returning(ASTNode):

    def __init__(self, _list=_all):
        self._list = _list

    def __str__(self):
        return 'RETURNING {_list}'.format(_list=self._list)


class Where(ASTNode):

    def __init__(self, logic):
        if hasattr(logic, 'inline'):
            logic.inline = True
        self.logic = logic

    def __str__(self):
        return "WHERE " + str(self.logic)


class From(ASTNode):
    
    def __init__(self, _from):
        if hasattr(_from, 'inline'):
            _from.inline = True
        self._from = _from

    def __str__(self):
        return 'FROM {_from}'.format(_from=self._from)


class Joins(list):

    def __str__(self):
        return ' '.join(map(lambda x: str(x), self))


class Join(ASTNode):
    
    def __init__(self, what, _on):
        self.what = what
        self._on = _on

    def __str__(self):
        s = 'JOIN ' + self.what + ' ON ' + self._on
        if self.inline:
            s = '(' + s + ')'
        return s


class Select(ASTNode):

    def __init__(self, _from, what=_all, where=empty, joins=[]):
        self._from = _from
        self.what = what
        self.where = where and Where(where)
        self.inlint = False
        self.joins = Joins(joins)

    def __str__(self):
        s = 'SELECT ' + str(self.what) + ' FROM ' + str(self._from) + ' ' + str(self.joins) + ' ' + str(self.where)
        if self.inline:
            s = '(' + s + ')'
        return s


class Delete(ASTNode):

    def __init__(self, _from, where=empty, returning=empty):
        self._from = From(_from)
        self.where = where and Where(where)
        self.returning = returning and Returning(returning)

    def __str__(self):
        return "DELETE {_from} {where} {returning};".format(
            _from=self._from,
            where=self.where,
            returning=self.returning
        )


class Insert(ASTNode):

    def __init__(self, to, fields='DEFAULT VALUES', values=empty, returning=empty):
        self.to = to
        if hasattr(fields, 'inline'):
            fields.inline = True
        self.fields = fields
        if hasattr(values, 'inline'):
            values.inline = True
        self.values = values and 'VALUES {0}'.format(values)
        self.returning = returning and Returning(returning)

    def __str__(self):
        return 'INSERT INTO {to} {fields} {values} {returning};'.format(
            to=self.to,
            fields=self.fields,
            values=self.values,
            returning=self.returning
        )


# @TODO: ADD INLINE FLAG AND VERSION FOR SELECT AND OTHERS
class Update(ASTNode):

    def __init__(self, to, fields, _from=empty, where=empty, returning=empty):
        self.to = to
        self.fields = Set(**fields)
        self._from = _from and From(_from)
        self.where = where and Where(where)
        self.returning = returning and Returning(returning)

    def __str__(self):
        return 'UPDATE {to} SET {fields} {_from} {where} {returning};'.format(
            to=self.to,
            fields=self.fields,
            _from=self._from,
            where=self.where,
            returning=self.returning
        )
