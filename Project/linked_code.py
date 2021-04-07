"""
file: linked_code.py
language: python3
author: RIT CS Dept.
description:
   lecture code for data type, and length and reversal functions
   using linked structures with Python data classes

   ################################################
   Data type definition

   A Linked Sequence is either
   - the Empty Linked Sequence, represented by the value None, or
   - an instance of LinkNode, which consists of
             * value, and
             * rest, which is a Linked Sequence

   We use the notation Linked(T) to refer to the
   Linked Sequence type, where T is the type of
   values.
   ################################################

   The Empty Linked Sequence is represented by None.
   LinkNode is represented using a Python data class.
"""

from dataclasses import dataclass
from typing import Any, Union

@dataclass(frozen=True)
class LinkNode:
    """
    A singly linked node structure
    :field value: the element value stored in this node, i.e.,
                  at the head of this sequence
    "field rest: a reference to the next node in the sequence, i.e.,
                 the tail of this sequence
    """
    value: Any
    rest: Union[None, 'LinkNode']

#############################################################################
#
# Building a linked list from nodes makes the data structures involved
# very clear. For example:
#
# pep_boys = LinkNode("Manny",LinkNode("Moe",LinkNode("Jack",None)))
#
# We clearly see how the three instances of the LinkNode class are put
# together. However, it gets rather long-winded to keep building lists
# this way for testing purposes. The following two methods show convenience
# methods for building linked lists from Python lists. This is rarely
# useful in real life because we don't typically write code that builds
# lists of known values.
#
#############################################################################

def mk_linked_list_rec( pylist ):
    """ mk_linked_list_rec: list or tuple -> LinkNode or None
        Use recursion to build a linked list from a Python list.
        Since linked lists are recursive structures, this is
        a good fit.
    """
    if len( pylist ) == 0:
        return None
    else:
        return LinkNode( pylist[ 0 ], mk_linked_list_rec( pylist[ 1: ] ) )

def mk_linked_list_iter( pylist ):
    """ mk_linked_list_iter: list or tuple -> LinkNode or None
        Use looping techniques to build a linked list from a Python list.
        This has the potential to work a bit faster than the recursive
        maker function, since it does not have to slice. However, we
        need to go through the Python list backwards.
    """
    result = None
    for idx in range( len( pylist ) - 1, -1, -1 ):
        result = LinkNode( pylist[ idx ], result )
    return result

# We will use the recursive one as the standard one for our tests. Here
# is a shorter alias for it.

mk_ll = mk_linked_list_rec

##########################
# Recursive length
##########################

def length_rec(lnk):
    """ length_rec: Linked(T) -> NatNum
    Compute the length of lnk recursively.
    """
    if lnk is None:
        return 0
    else:
        return 1 + length_rec(lnk.rest)


def length_rec_traced(lnk):
    print( "length_rec( " + str( lnk ) + " ) =" )
    return lrt("    =",lnk)

def lrt(prefix,lnk):
    if lnk is None:
        print( prefix + ' ' + str(0) )
        return 0
    else:
        prefix2a = prefix + " 1 +"
        prefix2 = prefix2a + " length_rec( " + str(lnk.rest) + " )"
        print( prefix2 )
        result = 1 + lrt( prefix2a, lnk.rest )
        print( prefix + ' ' + str( result ) )
        return result


##########################
# Recursive search
##########################

def contains(lnk,x):
    """ contains: LinkNode * Any -> Boolean
        :param lnk: the head node of a linked list
        :param x: the value to search for in the sequence
        :return: True iff the value exists in the sequence
    """
    if lnk is None:
        return False
    elif lnk.value == x:
        return True
    else:
        return contains(lnk.rest,x)


##########################
# Recursive indexing
##########################

def value_at(lnk,idx):
    """ value_at: LinkNode * int -> Any
        :param lnk: the head node of a linked list
        :param idx: the 0-based ordinal position in the sequence
        :return: True iff the value exists in the sequence
        :except: IndexError if idx is out of range
    """
    if lnk is None:
        raise IndexError( "index out of range" )
    elif idx == 0:
        return lnk.value
    else:
        return value_at(lnk.rest,idx-1)


####################
# Concatenation
####################

def concatenate(lnk, lnk2):
    """ concatenate: Linked(T) * Linked(T) -> Linked(T)
    Compute concatenation of lnk and lnk2.
    """
    if lnk is None:
        return lnk2
    else:
        return LinkNode(lnk.value, concatenate(lnk.rest, lnk2))


###############################
# Recursive reverse
###############################

def reverse_rec(lnk):
    """ reverse_rec: Linked(T) -> Linked(T)
    Compute reverse of lnk recursively.
    (Slow, because concatenate and reverse_rec are both O(N) => O(N^2).)
    """
    if lnk is None:
        return None
    else:
        return concatenate(reverse_rec(lnk.rest), LinkNode(lnk.value, None))

################################################
# Accumulative, tail recursive length
################################################

def length_acc(lnk, acc):
    """ length_acc: Linked(T) * NatNum -> NatNum
    Compute length of lnk + acc.
    """
    if lnk is None:
        return acc
    else:
        return length_acc(lnk.rest, acc + 1)


def length_tail_rec(lnk):
    """ length_tail_rec: Linked(T) -> NatNum
    Compute length of lnk tail recursively.
    """
    return length_acc(lnk, 0)


################################################
# Iterative length: derived Iterative form
################################################

def length_iter(lnk):
    """ length_iter: Linked(T) -> NatNum
    Compute length of lnk iteratively.
    """
    acc = 0
    while lnk is not None:
        lnk = lnk.rest
        acc = acc + 1
    return acc


##################################################
# Accumulative, tail recursive reverse
##################################################

def reverse_acc(lnk, acc):
    """ reverse_acc: Linked(T) * Linked(T) -> Linked(T)
    Compute reverse of lnk and acc with accumulator.
    """
    if lnk is None:
       return acc
    else:
       return reverse_acc(lnk.rest, LinkNode(lnk.value, acc))


def reverse_tail_rec(lnk):
    """ reverse_tail_rec: Linked(T) -> Linked(T)
    Compute tail recursive reverse of lnk.
    """
    return reverse_acc(lnk, None)


################################################
# Iterative reverse: derived Iterative form
################################################

def reverse_iter(lnk):
    """ reverse_iter: Linked(T) -> Linked(T)
    Compute reverse of lnk iteratively.
    """
    acc = None
    while lnk is not None:
        acc = LinkNode(lnk.value, acc)
        lnk = lnk.rest
    return acc


###########
# Insert_at
###########

def insert_at(index, val, lnk):
    """ insert_at: NatNum * T * Linked(T) -> Linked(T)
    Compute insertion of value at index of lnk.
    """
    if index == 0:
        return LinkNode(val, lnk)
    elif lnk != None:
        return LinkNode(lnk.value, insert_at(index-1, val, lnk.rest))
    else:
        raise IndexError("index out of bounds in insert_at")


###########
# Remove_at
###########

def remove_at(index, lnk):
    """ remove_at: NatNum * Linked(T) -> Linked(T)
    Compute removal of value at index from lnk.
    """
    if lnk is None:
        raise IndexError("index out of bounds in remove_at")
    elif index == 0:
        return lnk.rest
    else:
        return LinkNode(lnk.value, remove_at(index-1, lnk.rest))


#########
# Remove
#########

def remove(val, lnk):
    """ remove: T * Linked(T) -> Linked(T)
    Compute removal of value from lnk.
    """
    if lnk is None:
        return None
    elif lnk.value == val:
        return lnk.rest
    else:
        return LinkNode(lnk.value, remove(val, lnk.rest))


############
# Run tests
############

if __name__ == "__main__": # run tests for this module.

    print( "Please run test_linked_code.py for testing." )
