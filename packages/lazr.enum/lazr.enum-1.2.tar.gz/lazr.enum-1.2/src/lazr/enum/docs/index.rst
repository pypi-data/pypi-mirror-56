..
    This file is part of lazr.enum.

    lazr.enum is free software: you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License.

    lazr.enum is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with lazr.enum.  If not, see <http://www.gnu.org/licenses/>.

Enumerated Types
****************

Enumerated types are used primarily in two distinct places in the Launchpad
code: selector types; and database types.

Simple enumerated types do not have values, whereas database enumerated
types are a mapping from an integer value to something meaningful in the
code.

    >>> from lazr.enum import (
    ...     EnumeratedType, DBEnumeratedType, Item, DBItem, use_template)

The `enum` values of EnumeratedTypes are instances of Item.

    >>> class Fruit(EnumeratedType):
    ...     "A choice of fruit."
    ...     APPLE = Item('Apple')
    ...     PEAR = Item('Pear')
    ...     ORANGE = Item('Orange')

===================
IVocabulary support
===================

Enumerated types support IVocabularyTokenized.

    >>> from zope.interface.verify import verifyObject
    >>> from zope.schema.interfaces import (
    ...     ITitledTokenizedTerm, IVocabularyTokenized)
    >>> verifyObject(IVocabularyTokenized, Fruit)
    True

The items themselves do not support any interface.  Items returned
by the methods for vocabularies return wrapped items that support
the ITitledTokenizedTerm interface.

The token used to identify terms in the vocabulary is the name of the
Item variable.

    >>> item = Fruit.getTermByToken('APPLE')
    >>> type(item)
    <class 'lazr.enum...TokenizedItem'>
    >>> verifyObject(ITitledTokenizedTerm, item)
    True

TokenizedItems have three attributes (in order to support
ITitledTokenizedTerm):

    >>> item.value
    <Item Fruit.APPLE, Apple>
    >>> item.token
    'APPLE'
    >>> item.title
    'Apple'

    >>> Fruit.getTermByToken('apple').value
    <Item Fruit.APPLE, Apple>

The length of an EnumeratedType returns the number of items it has.

    >>> print(len(Fruit))
    3

===========================
The EnumeratedType registry
===========================

All enumerated types that are created are added to the
enumerated_type_registry.

    >>> from lazr.enum import enumerated_type_registry

The enumerated_type_registry maps the name of the enumerated type to the type
itself.

    >>> 'Fruit' in enumerated_type_registry
    True
    >>> enumerated_type_registry['Fruit']
    <EnumeratedType 'Fruit'>

You cannot redefine an existing enumerated type, nor create another enumerated
type with the same name as an existing type.

    >>> class BranchType(EnumeratedType):
    ...     BAR = Item('Bar')
    ...
    >>> BranchType.name = 'AltBranchType'
    >>> class BranchType(EnumeratedType):
    ...     FOO = Item('Foo')
    Traceback (most recent call last):
    ...
    TypeError: An enumerated type already exists with the name BranchType
    (...AltBranchType).

======================
Enumerated Type basics
======================

An EnumeratedType has a name and a description.  The name is the same as the
class name, and the description is the docstring for the class.

    >>> print(Fruit.name)
    Fruit
    >>> print(Fruit.description)
    A choice of fruit.

If you do not specify an explicit sort_order for the items of the
EnumeratedType one is created for you.  This is tuple of the tokens.

    >>> print(Fruit.sort_order)
    ('APPLE', 'PEAR', 'ORANGE')

The items of an enumerated type can be iterated over.  However the type that
is returned by the iteration is the TokenizedItem, not the item itself.

    >>> for item in Fruit:
    ...     print(item.token, item.title)
    APPLE Apple
    PEAR Pear
    ORANGE Orange

Items can also optionally have a url associated with them.

    >>> class Guitar(EnumeratedType):
    ...     FENDER = Item('Fender', url='http://www.fender.com')
    ...     RICK = Item('Rickenbacker', url='http://www.rickenbacker.com')
    ...     GIBSON = Item('Gibson', url='http://www.gibson.com')
    ...     FRANKENBASS = Item('Home built')

    >>> print(Guitar.FENDER.url)
    http://www.fender.com
    >>> print(Guitar.FRANKENBASS.url)
    None

Items in an enumerator support comparison and equality checks.  Comparison
is based on the sort order of the items.

    >>> apple = Fruit.APPLE
    >>> pear = Fruit.PEAR
    >>> orange = Fruit.ORANGE
    >>> apple < pear
    True
    >>> apple == pear
    False
    >>> apple == apple
    True
    >>> apple != pear
    True
    >>> apple > pear
    False
    >>> pear < orange
    True
    >>> apple < orange
    True

Items which are not in an enumerator always compare as False.

    >>> import warnings
    >>> from lazr.enum import Item
    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter('ignore', category=UserWarning)
    ...     Item('a') == Item('b')
    False

The string representation of an Item is the title, and the representation
also shows the enumeration that the Item is from.

    >>> print(apple)
    Apple
    >>> print(repr(apple))
    <Item Fruit.APPLE, Apple>

The `items` attribute of an enumerated type is not a list, but a class that
provides iteration over the items, and access to the Item attributes through
either the name of the Item, or the database value if there is one.

The primary use of this is to provide a backwards compatible accessor for
items, but it also provides a suitable alternative to getattr.

    >>> name = 'APPLE'
    >>> Fruit.items[name]
    <Item Fruit.APPLE, Apple>
    >>> getattr(Fruit, name)
    <Item Fruit.APPLE, Apple>

=========================
Database Enumerated Types
=========================

A very common use of enumerated types are to give semantic meaning to integer
values stored in database columns.  EnumeratedType Items themselves don't have
any integer values.

The DBEnumeratedType provides the semantic framework for a type that is used to
map integer values to python enumerated values.

    >>> # Remove the existing reference to BranchType from the registry
    >>> del enumerated_type_registry['BranchType']
    >>> class BranchType(DBEnumeratedType):
    ...     HOSTED = DBItem(1, """
    ...         Hosted
    ...
    ...         Hosted braches use the supermirror as the main repository
    ...         for the branch.""")
    ...
    ...     MIRRORED = DBItem(2, """
    ...         Mirrored
    ...
    ...         Mirrored branches are "pulled" from a remote location.""")
    ...
    ...     IMPORTED = DBItem(3, """
    ...         Imported
    ...
    ...         Imported branches are natively maintained in CVS or SVN""")

Note carefully that the value of a DBItem is the integer representation.  But
the value of the TokenizedItem is the DBItem itself.

    >>> hosted = BranchType.HOSTED
    >>> hosted.value
    1
    >>> hosted == BranchType.HOSTED
    True
    >>> tokenized_item = BranchType.getTermByToken('HOSTED')
    >>> tokenized_item.value
    <DBItem BranchType.HOSTED, (1) Hosted>

DBEnumeratedTypes also support IVocabularyTokenized

    >>> verifyObject(IVocabularyTokenized, BranchType)
    True

The items attribute of DBEnumeratedTypes provide a mapping from the database
values to the DBItems.

    >>> BranchType.items[3]
    <DBItem BranchType.IMPORTED, (3) Imported>

The items also support the url field.

    >>> class Bass(DBEnumeratedType):
    ...     FENDER = DBItem(10, 'Fender', url='http://www.fender.com')
    ...     RICK = DBItem(20, 'Rickenbacker',
    ...                   url='http://www.rickenbacker.com')
    ...     GIBSON = DBItem(30, 'Gibson', url='http://www.gibson.com')
    ...     FRANKENBASS = DBItem(40, 'Home built')

    >>> print(Bass.FENDER.url)
    http://www.fender.com
    >>> print(Bass.FRANKENBASS.url)
    None

Items in a DBEnumeratedType class must be of type DBItem.

    >>> class BadItemType(DBEnumeratedType):
    ...     TESTING = Item("Testing")
    Traceback (most recent call last):
    ...
    TypeError: Items must be of the appropriate type for the DBEnumeratedType,
    ...builtin...BadItemType.TESTING

You are not able to define a DBEnumeratedType that has two different
DBItems that map to the same numeric value.

    >>> class TwoMapping(DBEnumeratedType):
    ...     FIRST = DBItem(42, 'First')
    ...     SECOND = DBItem(42, 'Second')
    Traceback (most recent call last):
    ...
    TypeError: Two DBItems with the same value 42 (FIRST, SECOND)

=========================
Overriding the sort order
=========================

By default the sort order of the items in an enumerated type is defined by the
order in which the Items are declared.  This my be overridden by specifying
a sort_order attribute in the class.

If a sort_order is specified, it has to specify every item in the enumeration.

    >>> class AnimalClassification(EnumeratedType):
    ...     sort_order = "REPTILE", "INSECT", "MAMMAL"
    ...     INSECT = Item("Insect")
    ...     MAMMAL = Item("Mammal")
    ...     FISH = Item("Fish")
    ...     REPTILE = Item("Reptile")
    Traceback (most recent call last):
    ...
    TypeError: sort_order for EnumeratedType must contain all and only Item instances ...

The sort_order may also appear anywhere in the definition of the class,
although convention has it that it appears first, before the Item instances.

    >>> class AnimalClassification(EnumeratedType):
    ...     sort_order = "REPTILE", "FISH", "INSECT", "MAMMAL"
    ...     INSECT = Item("Insect")
    ...     MAMMAL = Item("Mammal")
    ...     FISH = Item("Fish")
    ...     REPTILE = Item("Reptile")

The items attribute of the enumerated type is ordered based on the sort_order.
The items attribute is also used to control iteration using __iter__.

    >>> for item in AnimalClassification.items:
    ...     print(item.title)
    Reptile
    Fish
    Insect
    Mammal

The sort order also drives the comparison operations.

    >>> reptile, fish, insect, mammal = AnimalClassification.items
    >>> reptile < fish < insect < mammal
    True

==========================
Extending enumerated types
==========================

The simplest way to extend a class is to derive from it.

    >>> class AnimalClassificationExtended(AnimalClassification):
    ...     INVERTEBRATE = Item("Invertebrate")

    >>> for item in AnimalClassificationExtended:
    ...     print(item.title)
    Reptile
    Fish
    Insect
    Mammal
    Invertebrate

The use_template function inserts the items from the specified enumerated type
into the new enumerated type.  The default case is to take all the enumerated
items.

    >>> class UIBranchType(EnumeratedType):
    ...     use_template(BranchType)
    >>> for item in UIBranchType:
    ...     print(item.title)
    Hosted
    Mirrored
    Imported

You can also specify items to be excluded by referring to the attribute name
in the exclude parameter.  This can be either a string referring to one name
or a tuple or list that refers to multiple attribute names.

    >>> class UIBranchType2(EnumeratedType):
    ...     use_template(BranchType, exclude='IMPORTED')
    >>> for item in UIBranchType2:
    ...     print(item.title)
    Hosted
    Mirrored

Or limit the items to those specified:

    >>> class UIBranchType3(EnumeratedType):
    ...     use_template(BranchType, include=('HOSTED', 'MIRRORED'))
    >>> for item in UIBranchType3:
    ...     print(item.title)
    Hosted
    Mirrored

================================================
Getting from an item back to the enumerated type
================================================

Each Item in an EnumeratedType has a reference back to the EnumeratedType.

    >>> print(repr(apple))
    <Item Fruit.APPLE, Apple>
    >>> print(repr(apple.enum))
    <EnumeratedType 'Fruit'>
    >>> for item in apple.enum:
    ...     print(item.title)
    Apple
    Pear
    Orange

============
Item.sortkey
============

The sortkey attribute of the Items are defined by the sort_order that is
defined for the enumerated type.  The value is often used as a hidden value
in columns in order to ensure appropriate sorting.

    >>> for item in Fruit.items:
    ...     print(item.title, item.sortkey)
    Apple  0
    Pear   1
    Orange 2

    >>> for item in BranchType.items:
    ...     print(item.title, item.sortkey)
    Hosted   0
    Mirrored 1
    Imported 2

============
JSON Support
============

Enumerated types instances can be serialised to/from json. This library provides the
necessary encode and decode classes which can be used directly or as part of the
lazr.json package where they are registered as default handlers for lazr enums.

A enum instance is serialised as a dict containing:
- the enumerated type name as per the enumerated_type_registry
- the enum instance name

    >>> import json
    >>> from lazr.enum import EnumJSONEncoder

    >>> json_enum = json.dumps(
    ...     Fruit.APPLE, cls=EnumJSONEncoder, sort_keys=True)
    >>> print(json_enum)
    {"name": "APPLE", "type": "Fruit"}

To deserialse, we can specify a json object_hook as follows.
This is done transparently when using the lazr.json package.

    >>> def fruit_enum_decoder(value_dict):
    ...      return EnumJSONDecoder.from_dict(Fruit, value_dict)

    >>> from lazr.enum import EnumJSONDecoder
    >>> json.loads(json_enum, object_hook=fruit_enum_decoder)
    <Item Fruit.APPLE, Apple>

.. pypi description ends here

===============
Other Documents
===============

.. toctree::
   :glob:

   NEWS
