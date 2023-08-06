import abc
import typing
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Sequence
from typing import Union

from icecream import ic

from filedb.key import Value


class BSONType(Enum):
    Double = 'double'
    String = 'string'
    Object = 'object'
    Array = 'array'
    BinaryData = 'binData'
    ObjectId = 'objectId'
    Boolean = 'bool'
    Date = 'date'
    Null = 'null'
    RegularExpression = 'regex'
    JavaScript = 'javascript'
    JavaScriptWithScope = 'javascriptWithScope'
    Int32 = 'int'
    Int64 = 'long'
    Timestamp = 'timestamp'
    Decimal128 = 'decimal'
    MinKey = 'minKey'
    MaxKey = 'maxKey'
    Number = 'number'


class _Constraint(abc.ABC):

    def __and__(self, other: '_Constraint'):
        return _AllConstraint([self, other])

    def __or__(self, other: '_Constraint'):
        return _AnyConstraint([self, other])

    def __invert__(self):
        return _NotConstraint(self)

    @classmethod
    def parse(cls, constraint: 'Constraint') -> '_Constraint':
        if isinstance(constraint, _Constraint):
            return constraint
        elif isinstance(constraint, dict):
            return _DictConstraint({k: _Operator.parse(v) for k, v in constraint.items()})

    @abc.abstractmethod
    def value(self):
        ...

    @abc.abstractmethod
    def lift_explicit(self) -> '_Constraint':
        ...

    @abc.abstractmethod
    def simplify(self) -> '_Constraint':
        ...

    @abc.abstractmethod
    def __repr__(self):
        ...


"""
{'a': q.aba & q.baba,
 'b': q.zxz | z.xzxz,
 'c': 3}

to

{'and': [{'a': q.aba},
         {'a': q.baba},
         {'or': [{'b': q.zxz,
                  'b': q.xzxz}]},
         {'c': 3}]}
"""


def wrap(prefix, suffix, contents, lb='\n'):
    sep = ' ' * len(prefix) + lb
    return prefix + sep.join(contents) + suffix


class _DictConstraint(_Constraint):
    def __init__(self, operator_dict: Dict[str, '_Operator']):
        self.operator_dict = operator_dict

    def __repr__(self):
        return wrap('_DictConstraint({', '})', [f'{k}: {v}' for k, v in self.operator_dict.items()])

    def value(self):
        return {k: v.value() for k, v in self.operator_dict.items()}

    def lift_explicit(self):

        key_ops = [(k, op.lift_explicit()) for k, op in self.operator_dict.items()]

        any_key_ops = []
        all_key_ops = []
        rest_key_ops = []
        for k, op in key_ops:
            if isinstance(op, _AnyOperator):
                any_key_ops.append((k, op))
            elif isinstance(op, _AllExplicitOperator):
                all_key_ops.append((k, op))
            else:
                rest_key_ops.append((k, op))

        if any_key_ops or all_key_ops:
            parts: List[_Constraint] = [_DictConstraint(dict(rest_key_ops))] if rest_key_ops else []
            for k, all_op in all_key_ops:
                parts.extend([_DictConstraint({k: op}) for op in all_op.ops])
            for k, any_op in any_key_ops:
                parts.append(_AnyConstraint([_DictConstraint({k: op}) for op in any_op.ops]))
            return _AllConstraint(*parts)
        else:
            return self

    def simplify(self) -> '_Constraint':
        return _DictConstraint({k: v.simplify() for k, v in self.operator_dict.items()})


class _NotConstraint(_Constraint):
    def __init__(self, const: _Constraint):
        self.const = const

    def __repr__(self):
        return f'~{self.const}'

    def value(self):
        return {'$not': self.const.value()}

    def lift_explicit(self) -> '_Constraint':
        return _NotConstraint(self.const.lift_explicit())

    def simplify(self) -> '_Constraint':
        if isinstance(self.const, _NotConstraint):
            return self.const.const.simplify()
        else:
            return _NotConstraint(self.const.simplify())


class _AnyConstraint(_Constraint):
    def __init__(self, consts: Sequence[_Constraint]):
        self.consts = consts

    def __repr__(self):
        return wrap('_Any([', '])', [f'{c}' for c in self.consts], ', ')

    def value(self):
        return {'$or': [c.value() for c in self.consts]}

    def lift_explicit(self) -> '_Constraint':
        return _AnyConstraint(*[c.lift_explicit() for c in self.consts])

    def simplify(self) -> '_Constraint':
        simple_consts = [c.simplify() for c in self.consts]
        any_consts = []
        rest = []
        for c in simple_consts:
            if isinstance(c, _AnyConstraint):
                any_consts.append(c)
            else:
                rest.append(c)

        return _AnyConstraint(rest + [c for any_c in any_consts for c in any_c.consts])


class _AllConstraint(_Constraint):
    def __init__(self, consts: Sequence[_Constraint]):
        self.consts = consts

    def __repr__(self):
        return wrap('_All([', '])', [f'{c}' for c in self.consts], ', ')

    def value(self):
        return {'$and': [v.value() for v in self.consts]}

    def lift_explicit(self) -> '_Constraint':
        return _AllConstraint(*[c.lift_explicit() for c in self.consts])

    def simplify(self) -> '_Constraint':
        simple_consts = [c.simplify() for c in self.consts]
        all_consts = []
        rest = []
        for c in simple_consts:
            if isinstance(c, _AnyConstraint):
                all_consts.append(c)
            else:
                rest.append(c)

        return _AllConstraint(rest + [c for all_c in all_consts for c in all_c.consts])


class _Operator(abc.ABC):

    def __and__(self, other):
        if set(self.types) & set(other.types):
            return _AllExplicitOperator([self, other])
        else:
            return _AllImplicitOperator([self, other])

    def __or__(self, other):
        return _AnyOperator([self, other])

    def __invert__(self):
        return _NotOperator(self)

    @classmethod
    def parse(cls, operator: 'Operator'):
        if isinstance(operator, _Operator):
            return operator
        elif isinstance(operator, Value):
            return _Value(operator)

    @abc.abstractmethod
    def value(self):
        ...

    @property
    @abc.abstractmethod
    def types(self):
        ...

    @abc.abstractmethod
    def __repr__(self):
        ...

    def lift_explicit(self):
        return self

    def simplify(self):
        return self


class _Value(_Operator):
    types = ['value']

    def __init__(self, value_: Value):
        self.value_ = value_

    def __repr__(self):
        return f'{self.value}'

    def value(self):
        return self.value


class _NotOperator(_Operator):
    types = ['not']

    def __init__(self, op: _Operator):
        self.op = op

    def __repr__(self):
        return f'~{self.op}'

    def value(self):
        return {'$not': self.op.value()}

    def lift_explicit(self):
        if isinstance(self.op, _AnyOperator):
            return _AllExplicitOperator([_NotOperator(op) for op in self.op.ops])
        if isinstance(self.op, _AllExplicitOperator):
            return _AnyOperator([_NotOperator(op) for op in self.op.ops])

    def simplify(self) -> '_Operator':
        if isinstance(self.op, _NotOperator):
            return self.op.op.simplify()
        else:
            return _NotOperator(self.op.simplify())


class _AnyOperator(_Operator):
    types = ['or']

    def __init__(self, ops: Sequence[_Operator]):
        self.ops = ops

    def __repr__(self):
        return wrap('AnyOp([', ')]', [f'{op}' for op in self.ops], ', ')

    def value(self):
        return {'$or': [v.value() for v in self.ops]}

    def lift_explicit(self):
        return _AnyOperator([op.lift_explicit() for op in self.ops])

    def simplify(self) -> '_Operator':
        simple_ops = [c.simplify() for c in self.ops]
        any_ops = []
        rest = []
        for c in simple_ops:
            if isinstance(c, _AnyOperator):
                any_ops.append(c)
            else:
                rest.append(c)

        return _AnyOperator(rest + [c for any_c in any_ops for c in any_c.ops])


class _AllImplicitOperator(_Operator):
    def __init__(self, ops: Sequence[_Operator]):
        self.ops = ops

    def __repr__(self):
        return wrap('[', ']', [f'{op}' for op in self.ops], ', ')

    def value(self):
        v = {}
        for op in self.ops:
            v.update(op.value())
        return v

    @property
    def types(self):
        return sum((op.types for op in self.ops), [])

    def lift_explicit(self):
        return _AllImplicitOperator([op.lift_explicit() for op in self.ops])

    def simplify(self) -> '_Operator':
        simple_ops = [c.simplify() for c in self.ops]
        all_ops = []
        rest = []
        for c in simple_ops:
            if isinstance(c, _AllImplicitOperator):
                all_ops.append(c)
            else:
                rest.append(c)

        return _AllImplicitOperator(rest + [c for all_c in all_ops for c in all_c.ops])


class _AllExplicitOperator(_Operator):
    types = ['and']

    def __repr__(self):
        return wrap('All([', '])', [f'{op}' for op in self.ops], ', ')

    def __init__(self, ops: Sequence[_Operator]):
        self.ops = ops

    def value(self):
        raise ValueError('All explicit operator has to be lifted to All constraint!')

    def lift_explicit(self):
        return _AllExplicitOperator([op.lift_explicit() for op in self.ops])

    def simplify(self) -> '_Operator':
        simple_ops = [c.simplify() for c in self.ops]
        all_ops = []
        rest = []
        for c in simple_ops:
            if isinstance(c, _AllExplicitOperator):
                all_ops.append(c)
            else:
                rest.append(c)

        return _AllExplicitOperator(rest + [c for all_c in all_ops for c in all_c.ops])


class _TypeComparisonOperator(_Operator):
    types = ['type']

    def __init__(self, type_: BSONType):
        self.type_ = type_

    def __repr__(self):
        return f'type({self.type_})'

    def value(self):
        return {'$type': self.type_.value}


class _SingleComparisonOperator(_Operator):
    def __init__(self, op_string: str, value_: Value):
        self.op_string = op_string
        self.value_ = value_

    def __repr__(self):
        return f'{self.op_string} {self.value_})'

    def value(self):
        return {self.op_string: self.value_}

    @property
    def types(self):
        return [self.op_string]


class _MultipleComparisonOperator(_Operator):
    def __init__(self, op_string: str, values: Sequence[Value]):
        self.op_string = op_string
        self.values = values

    def __repr__(self):
        return f'{self.op_string} {self.values})'

    def value(self):
        return {self.op_string: self.values}

    @property
    def types(self):
        return [self.op_string]


class _Exists(_Operator):
    types = ['exists']

    def __init__(self, yes_or_no: bool):
        self.yes_or_no = yes_or_no

    def __repr__(self):
        return 'exists' if self.yes_or_no else 'not exists'

    def value(self):
        return {'$exists': self.yes_or_no}


class _Query:

    @staticmethod
    @typing.overload
    def any(*args: _Operator):
        ...

    @staticmethod
    @typing.overload
    def any(*args: _Constraint):
        ...

    @staticmethod
    def any(*args):
        if all(isinstance(a, _Operator) for a in args):
            return _AnyOperator(args)
        elif all(isinstance(a, _Constraint) for a in args):
            return _AnyConstraint(args)

    @staticmethod
    @typing.overload
    def all(*args: _Operator):
        ...

    @staticmethod
    @typing.overload
    def all(*args: _Constraint):
        ...

    @staticmethod
    def all(*args):
        if all(isinstance(a, _Operator) for a in args):
            if sum(len(set(a.types)) for a in args) == len(set(sum((a.types for a in args), []))):
                return _AllImplicitOperator(args)
            else:
                return _AllExplicitOperator(args)
        elif all(isinstance(a, _Constraint) for a in args):
            return _AllConstraint(args)

    @staticmethod
    def equal(value):
        return _SingleComparisonOperator('$eq', value)

    @staticmethod
    def not_equal(value):
        return _SingleComparisonOperator('$ne', value)

    @staticmethod
    def greater_than(value):
        return _SingleComparisonOperator('$gt', value)

    @staticmethod
    def greater_or_equal(value):
        return _SingleComparisonOperator('$gte', value)

    @staticmethod
    def less_than(value):
        return _SingleComparisonOperator('$lt', value)

    @staticmethod
    def less_or_equal(value):
        return _SingleComparisonOperator('$lte', value)

    @staticmethod
    def is_in(values):
        return _MultipleComparisonOperator('$in', values)

    @staticmethod
    def not_in(values):
        return _MultipleComparisonOperator('$nin', values)

    @property
    def exists(self):
        return _Exists(True)

    @property
    def not_exists(self):
        return _Exists(False)

    @staticmethod
    def has_type(type_):
        return _TypeComparisonOperator(type_)


def expand(x: 'Query'):
    print(x)
    parsed = _Constraint.parse(x)
    print(parsed)
    simple = parsed.simplify()
    print(simple)
    lifted = simple.lift_explicit()
    print(lifted)
    value = lifted.value()
    print(value)
    return value


q = _Query()

Operator = Union[_Operator, Value]
Constraint = Union[_Constraint, Dict[str, Operator]]
DSLMongoQuery = Constraint
RawMongoQuery = Dict[str, Any]  # TODO more precise
Query = Union[RawMongoQuery, Constraint]
