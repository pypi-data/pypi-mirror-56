#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright 2014-2019 by Alexis Pietak & Cecil Curry.
# See "LICENSE" for further details.

'''
Low-level **mapping utilities** (i.e., functions operating on dictionary-like
types and instances).
'''

# ....................{ IMPORTS                           }....................
import pprint
from betse.exceptions import BetseMappingException
from betse.util.type.types import (
    type_check, MappingType, HashableType,)
from copy import deepcopy

# ....................{ EXCEPTIONS                        }....................
@type_check
def die_unless_values_unique(mapping: MappingType) -> None:
    '''
    Raise an exception unless all values of the passed dictionary are unique.

    Equivalently, this function raises an exception if any two key-value pairs
    of this dictionary share the same values.

    Parameters
    ----------
    mapping : MappingType
        Dictionary to be inspected.

    Raises
    ----------
    BetseMappingException
        If at least one value of this dictionary is a duplicate.
    '''

    # Avoid circular import dependencies.
    from betse.util.type.iterable import iterables
    from betse.util.type.text import strs

    # If one or more values of this dictionary are duplicates...
    if not is_values_unique(mapping):
        # Set of all duplicate values in this dictionary.
        values_duplicate = iterables.get_items_duplicate(mapping.values())

        # Raise an exception embedding this set.
        raise BetseMappingException(
            'Dictionary values {} duplicate.'.format(
                strs.join_as_conjunction_double_quoted(*values_duplicate)))

# ....................{ TESTERS                           }....................
@type_check
def is_key(mapping: MappingType, *keys: HashableType) -> bool:
    '''
    ``True`` only if the passed dictionary contains *all* passed keys.

    Parameters
    ----------
    mapping : MappingType
        Dictionary to be tested.
    keys : tuple[HashableType]
        Tuple of all keys to be tested for.

    Returns
    ----------
    bool
        ``True`` only if this dictionary contains *all* passed keys.
    '''

    return (
        # If only one key is passed, optimize this common edge case with the
        # standard idiom for testing key containment.
        keys[0] in mapping if len(keys) == 1 else
        # Else, two or more keys are passed. In this case, fallback to a
        # general-case strategy testing key containment in a single one-liner.
        # And yes: this is ridiculously awesome.
        set(keys).issubset(mapping)
    )


@type_check
def is_values_unique(mapping: MappingType) -> bool:
    '''
    ``True`` only if all values of the passed dictionary are **unique** (i.e.,
    if *no* two key-value pairs of this dictionary share the same values).

    Parameters
    ----------
    mapping : MappingType
        Dictionary to be inspected.

    Returns
    ----------
    bool
        ``True`` only if *all* values of this dictionary are unique.
    '''

    # Avoid circular import dependencies.
    from betse.util.type.iterable import iterables

    # For sanity, defer to an existing low-level tester.
    return iterables.is_items_unique(mapping.values())

# ....................{ FORMATTERS                        }....................
@type_check
def format_map(mapping: MappingType) -> str:
    '''
    Convert the passed dictionary into a human-readable string.
    '''

    return pprint.pformat(mapping)

# ....................{ COPIERS                           }....................
@type_check
def copy_map(mapping: MappingType) -> MappingType:
    '''
    Dictionary of all key-value pairs deeply (i.e., recursively) duplicated
    from the passed dictionary.

    This function should *always* be called in lieu of the standard
    :meth:`dict.__init__` and :meth:`dict.copy` methods, which only perform
    shallow dictionary copies. These copies fail to copy data structures nested
    in the values of the original dictionary, inviting subtle synchronization
    woes on subsequently modifying either the original or copied dictionaries.

    Parameters
    ----------
    mapping: MappingType
        Dictionary to be deeply copied.

    Returns
    ----------
    MappingType
        Dictionary of all key-value pairs deeply (i.e., recursively) duplicated
        from the passed dictionary.
    '''

    #FIXME: Does this simplistic approach guarantee the returned mapping to be
    #of the same type as the passed mapping?
    return deepcopy(mapping)


@type_check
def copy_map_sans_key(mapping: MappingType, key: HashableType) -> MappingType:
    '''
    Dictionary of all key-value pairs excluding that whose key is the passed
    key deeply (i.e., recursively) duplicated from the passed dictionary.

    Parameters
    ----------
    mapping: MappingType
        Dictionary to be deeply copied.
    key : HashableType
        Key to be removed from this dictionary.

    Returns
    ----------
    MappingType
        Dictionary of all key-value pairs excluding that whose key is this
        key deeply (i.e., recursively) duplicated from this dictionary.

    Raises
    ----------
    :class:`KeyError`
        If this dictionary contains no such key.

    See Also
    ----------
    :func:`copy_map`
        Further details on map copying.
    :func:`remove_key`
        Further details on key removal.
    '''

    # Deep copy of this dictionary.
    mapping_copy = copy_map(mapping)

    # Remove this key from this copy in-place.
    remove_key(mapping=mapping_copy, key=key)

    # Return this copy.
    return mapping_copy

# ....................{ INVERTERS                         }....................
@type_check
def invert_map_unique(mapping: MappingType) -> MappingType:
    '''
    Dictionary inverted from the passed dictionary if no two key-value pairs of
    this dictionary share the same values *or* raise an exception otherwise.

    Specifically, the returned dictionary maps from each value to each key of
    the passed dictionary *and* is guaranteed to be the same type as that of
    the passed dictionary.

    Parameters
    ----------
    mapping : MappingType
        Dictionary to be inverted. The type of this dictionary *must* define an
        ``__init__`` method accepting a single parameter whose value is an
        iterable of 2-iterables ``(key, value)`` providing all key-value pairs
        with which to initialize a new such dictionary. See the
        :meth:`dict.__init__` method for further details.

    Returns
    ----------
    MappingType
        Dictionary inverted from this dictionary as detailed above.

    Raises
    ----------
    BetseMappingException
        If one or more key-value pairs of this dictionary share the same
        values.

    See Also
    ----------
    https://stackoverflow.com/a/1679702/2809027
        StackOverflow answer strongly inspiring this implementation.
    '''

    # If any values of this dictionary are are duplicates, raise an exception.
    die_unless_values_unique(mapping)

    # Type of this dictionary.
    mapping_type = type(mapping)

    # If this is an unordered dictionary, return a dictionary comprehension
    # efficiently inverting this dictionary in the trivial way.
    if mapping_type is dict:
        return {value: key for key, value in mapping.items()}
    # Else, this is possibly an ordered dictionary. In this case, a
    # considerably less trivial and slightly less efficient approach is needed.
    else:
        # Iterable of reversed 2-iterables "(value, pair)" for each key-value
        # pair of the passed dictionary. Dismantled, this is:
        #
        # * "mapping.items()", an iterable of 2-iterables "(key, value)" for
        #   each key-value pair of the passed dictionary.
        # * "reversed", a builtin which when passed such a 2-iterable returns
        #   the reversed 2-iterable "(value, pair)" for that key-value pair.
        # * "map(...)", a builtin applying the prior builtin to each such pair.
        value_key_pairs = map(reversed, mapping.items())

        # Return a new instance of this type of dictionary by invoking the
        # "dict(iterable)" form of this type's __init__() method. To quote the
        # dict.__init__() docstring:
        #
        # "dict(iterable) -> new dictionary initialized as if via:
        #      d = {}
        #      for k, v in iterable:
        #          d[k] = v"
        return mapping_type(value_key_pairs)

# ....................{ MERGERS                           }....................
@type_check
def merge_maps(*mappings: MappingType) -> MappingType:
    '''
    Dictionary of all key-value pairs deeply (i.e., recursively) merged
    together from all passed dictionaries (in the passed order).

    **Order is significant.** Dictionaries passed later take precedence over
    dictionaries passed earlier. Ergo, the last passed dictionary takes
    precedence over *all* other passed dictionaries. Whenever any two passed
    dictionaries collide (i.e., contain the same key), the returned dictionary
    contains a key-value pair for that key whose value is that of the key-value
    pair for the same key of whichever of the two dictionaries was passed last.

    Parameters
    ----------
    mappings : Tuple[MappingType]
        Tuple of all dictionaries to be merged.

    Returns
    ----------
    MappingType
        Dictionary merged from and of the same type as the passed dictionaries.
        Note lastly that the class of the passed dictionary *must* define an
        ``__init__()`` method accepting a dictionary comprehension.

    See Also
    ----------
    :meth:`dict.update`
        Standard method merging two dictionaries, which should typically be
        called instead of this slower function in this specific use case.
    '''

    # Type of dictionary to be returned.
    dict_type = type(mappings[0])

    # Dictionary merged from the passed dictionaries via a doubly-nested
    # dictionary comprehension. While there exist a countably infinite number
    # of approaches to merging dictionaries in Python, this approach is known
    # to be the most efficient for general-purpose merging of arbitrarily many
    # dictionaries under Python >= 3.4. See also Trey Hunter's exhaustive
    # commentary replete with timings at:
    #     http://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python
    dict_merged = {
        # For safety, deeply copy rather than reuse this value.
        key: deepcopy(value)
        for mapping in mappings
        for key, value in mapping.items()
    }

    # Return a dictionary of this type converted from this dictionary. If the
    # desired type is a "dict", this dictionary is returned as is; else, this
    # dictionary is converted into an instance of the desired type.
    return dict_merged if dict_type is dict else dict_type(dict_merged)

# ....................{ REMOVERS                          }....................
@type_check
def remove_key(mapping: MappingType, key: HashableType) -> None:
    '''
    Remove the key-value pair whose key is the passed key from the passed
    dictionary **in-place** (i.e., by modifying this dictionary rather than
    creating and returning a new dictionary with this key removed) if this
    dictionary contains this key *or* raise an exception otherwise.

    This function is a caller convenience improving codebase readability and
    efficiency. Although there exist multiple means of removing key-value pairs
    from dictionaries, this function implements the most efficient approach.
    These include:

    * The ``del mapping[key]`` idiom, known to be the most efficient approach.
    * The :meth:`dict.pop` method, known to be slightly less efficient than the
      idiomatic approach.

    Parameters
    ----------
    mapping : MappingType
        Dictionary to remove this key from.
    key : HashableType
        Key to be removed from this dictionary.

    Raises
    ----------
    :class:`KeyError`
        If this dictionary contains no such key.

    See Also
    ----------
    :func:`copy_map_sans_key`
        Function creating and returning a new dictionary with this key removed.
    '''

    # The best things in life are free.
    del mapping[key]
