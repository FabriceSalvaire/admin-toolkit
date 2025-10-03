####################################################################################################

from collections import namedtuple
from dataclasses import dataclass
from pprint import pprint
import dataclasses

####################################################################################################
#
# namedtuple are not mutable
#

# collections.namedtuple(
#  typename,
#  field_names,  ('x', 'y')  'x y'  'x, y'
#  *,
#  rename=False,
#  defaults=None,
#  module=None)

Point = namedtuple('Point', ('x', 'y'))

p = Point(11, y=22)

Point._make([11, 22])
p._asdict()
p._fields
p._field_defaults

p.x + p.y
getattr(p, 'x')
x, y = p
p[0] + p[1]

# typing.NamedTuple
# p.x = 100
# Return a new instance of the named tuple replacing specified fields with new value
p._replace(x=33)


class Point(namedtuple('Point', ['x', 'y'])):
    # keep memory requirements low by preventing the creation of instance dictionaries
    __slots__ = ()
    @property
    def hypot(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def __str__(self):
        return 'Point: x=%6.3f  y=%6.3f  hypot=%6.3f' % (self.x, self.y, self.hypot)

Point3D = namedtuple('Point3D', Point._fields + ('z',))

# see also typing.NamedTuple for typed version

####################################################################################################

# dataclasses.make_dataclass(cls_name, fields, *, bases=(), namespace=None, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False, module=None)

@dataclass
class Foo:
    field1: str
    field2: float
    field3: int = 0

#  dataclasses.field(*, default=MISSING, default_factory=MISSING, init=True, repr=True, hash=None, compare=True, metadata=None, kw_only=MISSING)

####################################################################################################

_ = Foo('abc', 1.2)
_ = Foo(field1='abc', field2=1.2)
# _ = Foo(field1='abc')
pprint(_)
# pprint(_.__dict__)
pprint(dataclasses.fields(Foo))
pprint(dataclasses.asdict(_))
pprint(dataclasses.astuple(_))

_.field1 = 'abc'
