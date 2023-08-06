import funcy as fn
from itertools import combinations_with_replacement as combinations
from itertools import product

try:
    from dd.cudd import BDD
except ImportError:
    from dd.autoref import BDD

from fold_bdd import post_order, fold_path
from fold_bdd.folds import path


def create_manager():
    manager = BDD()
    manager.declare('x', 'y')
    manager.reorder({'x': 1, 'y': 0})
    manager.configure(reordering=False)
    return manager


def test_post_order():
    @fn.memoize
    def merge1(ctx, low=None, high=None):
        return 1 if low is None else low + high

    manager = create_manager()
    bexpr = manager.add_expr('x & y')

    val = post_order(bexpr, merge1)
    assert val == bexpr.dag_size

    # Convert BDD to function.
    def merge2(ctx, low=None, high=None):
        if ctx.is_leaf:
            return lambda _: ctx.node_val

        def _eval(vals):
            val, *vals2 = vals
            out = high(vals2) if val else low(vals2)
            return ctx.negated ^ out

        return _eval

    _eval = post_order(bexpr, merge2)
    for vals in combinations([True, False], 2):
        assert all(vals) == _eval(vals)

    def merge3(ctx, low, high):
        if ctx.is_leaf:
            return ctx.skipped_paths if ctx.node_val else 0

        return (low + high) * ctx.skipped_paths

    bexpr2 = manager.add_expr('x | y')

    assert post_order(bexpr, merge3) == 1
    assert post_order(bexpr2, merge3) == 3


def test_path():
    manager = create_manager()
    bexpr = manager.add_expr('x | y')

    questions = {
        (False, False): 3,
        (False, True): 3,
        (True, False): 2,
        (True, True): 2,
    }

    for q, a in questions.items():
        assert len(list(path(bexpr, q))) == a


def test_fold_path():
    manager = create_manager()
    bexpr = manager.add_expr('x | y')
    bexpr2 = manager.true

    def merge(ctx, val, acc):
        return acc + 1

    def count_nodes(bexpr, vals):
        return fold_path(merge, bexpr, vals, initial=0)

    assert count_nodes(bexpr, (False, False)) == 3
    assert count_nodes(bexpr, (False, True)) == 3
    assert count_nodes(bexpr, (True, False)) == 2
    assert count_nodes(bexpr, (True, True)) == 2

    assert count_nodes(bexpr2, (True, True)) == 1
    assert count_nodes(bexpr2, (False, True)) == 1

    def merge2(ctx, val, acc):
        return acc * ctx.skipped_paths

    def count_paths(bexpr, vals):
        return fold_path(merge2, bexpr, vals, initial=1)

    assert count_paths(bexpr, (False, False)) == 1
    assert count_paths(bexpr, (False, True)) == 1
    assert count_paths(bexpr, (True, False)) == 2
    assert count_paths(bexpr, (True, True)) == 2

    assert count_paths(bexpr2, (True, True)) == 4
    assert count_paths(bexpr2, (False, True)) == 4


def test_path_negation():
    levels = {'c1': 0, 'a1': 1, 'c2': 2, 'a2': 3}
    manager = BDD(levels)
    manager.configure(reordering=False)

    c1, a1, c2, a2 = map(manager.var, ['c1', 'a1', 'c2', 'a2'])
    bexpr = ((c1 & a1) | (~c1 & ~a1)) & ((c2 & a2) | (~c2 & ~a2))

    assert bexpr.low.negated
    assert not bexpr.high.negated

    assert len(list(path(bexpr, (True, False, False, False)))) == 3
    assert len(list(path(bexpr, (True, True, True, True)))) == 5

    def merge(ctx, val, acc):
        if ctx.is_leaf:
            return ctx.path_negated ^ ctx.node_val
        return None

    def evaluate(vals):
        return fold_path(merge, bexpr, vals, initial=[])

    for val in product(*(4*[[False, True]])):
        expected = (val[0] == val[1]) and (val[2] == val[3])
        assert evaluate(val) == expected
