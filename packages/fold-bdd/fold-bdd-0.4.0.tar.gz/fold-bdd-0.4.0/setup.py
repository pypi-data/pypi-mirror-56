# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fold_bdd']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0', 'dd>=0.5.4,<0.6.0', 'funcy>=1.13,<2.0']

setup_kwargs = {
    'name': 'fold-bdd',
    'version': '0.4.0',
    'description': 'Library for folding (or reducing) over a Reduced Ordered Binary Decision Diagram.',
    'long_description': "# Fold-BDD\nLibrary for folding (or reducing) over a Reduced Ordered Binary Decision Diagram.\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/fold-bdd/status.svg)](https://cloud.drone.io/mvcisback/fold-bdd)\n[![codecov](https://codecov.io/gh/mvcisback/fold-bdd/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/fold-bdd)\n[![PyPI version](https://badge.fury.io/py/fold-bdd.svg)](https://badge.fury.io/py/fold-bdd)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->\n**Table of Contents**\n\n- [Fold-BDD](#fold-bdd)\n- [Installation](#installation)\n- [Usage](#usage)\n    - [Create ROBDD](#create-robdd)\n    - [Post-Order Examples](#post-order-examples)\n    - [Fold Path Examples](#fold-path-examples)\n- [Context Object Attributes](#context-object-attributes)\n\n<!-- markdown-toc end -->\n\n\n# Installation\n\nIf you just need to use `fold_bdd`, you can just run:\n\n`$ pip install fold-bdd`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\nThe `fold-bdd` library supports two types of folds:\n\n1. Folding over the DAG of a `BDD` starting at the root and then\n   recursively merging the low and high branches until the\n   `True`/`False` leaves. This is simply a compressed variant\n   of a post-order traversal.\n\n2. Folding over a path in the DAG, starting at the root and moving the\n   the corresponding leaf (left fold).\n\nIn both cases, local context such as the levels of the parent and\nchild nodes are passed in.\n\nAs input, each of these take in a bdd, from the\n[dd](https://github.com/tulip-control/dd) library and function for\naccumulating or merging. \n\nThe following example illustrates how to use `fold_bdd` to count the\nnumber of solutions to a predicate using `post_order` and evaluate a\npath using `fold_path`.\n\n## Create ROBDD\n```python\n# Create BDD.\nfrom dd.cudd import BDD\n\nmanager = BDD()\nmanager.declare('x', 'y')\nmanager.reorder({'x': 1, 'y': 0})\nmanger.configure(reordering=False)\n\nbexpr = manager.add_expr('x | y')\n```\n\n## Post-Order Examples\n\n```python\nfrom fold_bdd import post_order\n```\n\n### Count Number of Nodes in BDD\n\n```python\ndef merge1(ctx, low=None, high=None):\n    return 1 if low is None else low + high\n\ndef dag_size(bexpr):\n    return post_order(bexpr, merge1)\n\nassert bexpr.dag_size == dag_size(bexpr)\n```\n\n### Count Number of Solutions to bexpr.\n```python\ndef merge2(ctx, low, high):\n    if ctx.is_leaf:\n        return ctx.skipped_paths if ctx.node_val else 0\n    return (low + high) * ctx.skipped_paths\n\ndef count_solutions(bexpr):\n    return post_order(bexpr, merge2)\n\nassert count_solutions(bexpr) == 3\n```\n\n## Fold Path Examples\n\n### Count nodes along path.\n\n```python\ndef merge(ctx, val, acc):\n    return acc + 1\n\ndef count_nodes(bexpr, vals):\n    return fold_path(merge, bexpr, vals, initial=0)\n\nassert count_nodes(bexpr, (False, False)) == 3\nassert count_nodes(bexpr, (True, False)) == 2\n```\n\n### Count paths corresponding to BDD path\n\n```python\ndef merge(ctx, val, acc):\n    return acc * ctx.skipped_paths\n\ndef count_paths(bexpr, vals):\n    return fold_path(merge, bexpr, vals, initial=1)\n\nassert count_paths(bexpr, (False, True)) == 1\nassert count_paths(bexpr, (True, False)) == 2\n```\n\n# Context Object Attributes\n\nThe `Context` object contains exposes attributes\n\n- `node: Hashable`  # Reference to Node in ROBDD.\n- `node_val: Union[str, bool]`  # Node name or leaf value.\n- `negated: bool`  # Is the edge to prev node negated.\n- `max_lvl: int`  # How many decision variables are there. \n- `curr_lvl: int`  # Which decision is this.\n- `prev_lvl: Optional[int]`  # Which decision was the parent. None if root.\n- `low_lvl: Optional[int]`  # Which decision does the False edge point to. None if leaf.\n- `high_lvl: Optional[int]`  # Which decision does the True edge point to. None if leaf.\n- `is_leaf: bool`  # Is the current node a leaf.\n- `skipped: int`  # How many decisions were skipped on edge to this node.\n",
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'url': 'https://github.com/mvcisback/fold-bdd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
