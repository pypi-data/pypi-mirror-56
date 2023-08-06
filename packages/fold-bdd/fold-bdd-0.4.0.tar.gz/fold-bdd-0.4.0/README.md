# Fold-BDD
Library for folding (or reducing) over a Reduced Ordered Binary Decision Diagram.

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/fold-bdd/status.svg)](https://cloud.drone.io/mvcisback/fold-bdd)
[![codecov](https://codecov.io/gh/mvcisback/fold-bdd/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/fold-bdd)
[![PyPI version](https://badge.fury.io/py/fold-bdd.svg)](https://badge.fury.io/py/fold-bdd)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Fold-BDD](#fold-bdd)
- [Installation](#installation)
- [Usage](#usage)
    - [Create ROBDD](#create-robdd)
    - [Post-Order Examples](#post-order-examples)
    - [Fold Path Examples](#fold-path-examples)
- [Context Object Attributes](#context-object-attributes)

<!-- markdown-toc end -->


# Installation

If you just need to use `fold_bdd`, you can just run:

`$ pip install fold-bdd`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

The `fold-bdd` library supports two types of folds:

1. Folding over the DAG of a `BDD` starting at the root and then
   recursively merging the low and high branches until the
   `True`/`False` leaves. This is simply a compressed variant
   of a post-order traversal.

2. Folding over a path in the DAG, starting at the root and moving the
   the corresponding leaf (left fold).

In both cases, local context such as the levels of the parent and
child nodes are passed in.

As input, each of these take in a bdd, from the
[dd](https://github.com/tulip-control/dd) library and function for
accumulating or merging. 

The following example illustrates how to use `fold_bdd` to count the
number of solutions to a predicate using `post_order` and evaluate a
path using `fold_path`.

## Create ROBDD
```python
# Create BDD.
from dd.cudd import BDD

manager = BDD()
manager.declare('x', 'y')
manager.reorder({'x': 1, 'y': 0})
manger.configure(reordering=False)

bexpr = manager.add_expr('x | y')
```

## Post-Order Examples

```python
from fold_bdd import post_order
```

### Count Number of Nodes in BDD

```python
def merge1(ctx, low=None, high=None):
    return 1 if low is None else low + high

def dag_size(bexpr):
    return post_order(bexpr, merge1)

assert bexpr.dag_size == dag_size(bexpr)
```

### Count Number of Solutions to bexpr.
```python
def merge2(ctx, low, high):
    if ctx.is_leaf:
        return ctx.skipped_paths if ctx.node_val else 0
    return (low + high) * ctx.skipped_paths

def count_solutions(bexpr):
    return post_order(bexpr, merge2)

assert count_solutions(bexpr) == 3
```

## Fold Path Examples

### Count nodes along path.

```python
def merge(ctx, val, acc):
    return acc + 1

def count_nodes(bexpr, vals):
    return fold_path(merge, bexpr, vals, initial=0)

assert count_nodes(bexpr, (False, False)) == 3
assert count_nodes(bexpr, (True, False)) == 2
```

### Count paths corresponding to BDD path

```python
def merge(ctx, val, acc):
    return acc * ctx.skipped_paths

def count_paths(bexpr, vals):
    return fold_path(merge, bexpr, vals, initial=1)

assert count_paths(bexpr, (False, True)) == 1
assert count_paths(bexpr, (True, False)) == 2
```

# Context Object Attributes

The `Context` object contains exposes attributes

- `node: Hashable`  # Reference to Node in ROBDD.
- `node_val: Union[str, bool]`  # Node name or leaf value.
- `negated: bool`  # Is the edge to prev node negated.
- `max_lvl: int`  # How many decision variables are there. 
- `curr_lvl: int`  # Which decision is this.
- `prev_lvl: Optional[int]`  # Which decision was the parent. None if root.
- `low_lvl: Optional[int]`  # Which decision does the False edge point to. None if leaf.
- `high_lvl: Optional[int]`  # Which decision does the True edge point to. None if leaf.
- `is_leaf: bool`  # Is the current node a leaf.
- `skipped: int`  # How many decisions were skipped on edge to this node.
