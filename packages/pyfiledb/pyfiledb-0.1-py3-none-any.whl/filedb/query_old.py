from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from filedb.key import Value

# if set(self.value) & set(other.value):  # have common keys
#     return Operator({'$and': [self.value, other.value]})
# else:


class Operator:
    value = None

    def __init__(self, value=None):
        self.value = value

    def __and__(self, other):
        return Operator({**self.value, **other.value})

    def __or__(self, other):
        return Operator({'$or': [self.value, other.value]})

    def __invert__(self):
        return Operator({'$not': self.value})

    def nor(self, other):
        return Operator({'$nor': [self.value, other.value]})


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


class TypeComparisonOperator(Operator):
    def __init__(self):
        super().__init__()

    def __call__(self, type_: BSONType):
        """

        Parameters
        ----------
        type_: Value to compare against

        Returns
        -------
        RawMongoQuery
            corresponding mongo db query
        """
        self.value = {'$type': type_.value}
        return self


class SingleComparisonOperator(Operator):
    def __init__(self, op_string: str):
        self.op_string = op_string
        super().__init__()

    def __call__(self, value: Value):
        """

        Parameters
        ----------
        value: Value to compare against

        Returns
        -------
        RawMongoQuery
            corresponding mongo db query
        """
        self.value = {self.op_string: value}
        return self


class MultipleComparisonOperator(Operator):
    def __init__(self, op_string: str):
        self.op_string = op_string
        super().__init__(None)

    def __call__(self, values: List[Value]):
        """

        Parameters
        ----------
        values: Value to compare against

        Returns
        -------
        RawMongoQuery
            corresponding mongo db query
        """
        self.value = {self.op_string: values}
        return self


class Exists(Operator):
    def __init__(self, yes_or_no: bool):
        super().__init__({'$exists': yes_or_no})


equal = SingleComparisonOperator('$eq')
not_equal = SingleComparisonOperator('$ne')
greater_than = SingleComparisonOperator('$gt')
greater_or_equal = SingleComparisonOperator('$gte')
less_than = SingleComparisonOperator('$lt')
less_or_equal = SingleComparisonOperator('$lte')
is_in = MultipleComparisonOperator('$in')
not_in = MultipleComparisonOperator('$nin')
exists = Exists(True)
not_exists = Exists(False)
has_type = TypeComparisonOperator()

RawMongoQuery = Dict[str, Any]
DSLMongoQuery = Dict[str, Union[Value, Operator]]
Query = Union[RawMongoQuery, DSLMongoQuery]
