from functools import reduce
from typing import Union, Optional, Hashable

import attr
import funcy as fn


@attr.s(auto_attribs=True, frozen=True)
class Context:
    node_val: Union[str, bool]
    negated: bool
    max_lvl: int
    node: Hashable
    path_negated: bool
    curr_lvl: Optional[int] = None
    prev_lvl: Optional[int] = None
    low_lvl: Optional[int] = None
    high_lvl: Optional[int] = None

    @property
    def is_leaf(self):
        return self.curr_lvl == self.max_lvl

    @property
    def skipped_decisions(self):
        if self.prev_lvl is None:
            return self.curr_lvl
        return self.curr_lvl - self.prev_lvl - 1

    @property
    def skipped_paths(self):
        return 2**self.skipped_decisions


def _ctx(node, manager, prev_ctx=None):
    max_lvl = len(manager.vars)
    path_negated = False if prev_ctx is None else \
        (prev_ctx.path_negated ^ prev_ctx.negated)
    common = {
        "node": node,
        "negated": node.negated,
        "path_negated": path_negated,
        "prev_lvl": None if prev_ctx is None else prev_ctx.curr_lvl,
        "max_lvl": max_lvl,
        "curr_lvl": min(node.level, max_lvl)
    }

    if node.var is None:
        specific = {
            "node_val": node == manager.true,
        }
    else:
        specific = {
            "node_val": node.var,
            "low_lvl": min(node.low.level, max_lvl),
            "high_lvl": min(node.high.level, max_lvl),
        }

    return Context(**common, **specific)


def post_order(node, merge, *, manager=None, prev_ctx=None):
    if manager is None:
        manager = node.bdd

    @fn.memoize
    def _post_order(node, prev_ctx=None):
        ctx = _ctx(node, manager, prev_ctx=prev_ctx)

        if ctx.is_leaf:
            return merge(ctx=ctx, low=None, high=None)

        def _reduce(c):
            return _post_order(c, prev_ctx=ctx)

        return merge(ctx=ctx, high=_reduce(node.high), low=_reduce(node.low))

    return _post_order(node)


def path(node, vals):
    vals = list(vals)
    prev_lvl, offset = node.level, 0
    while node.var is not None:
        prev_lvl = node.level
        if len(vals) > 1:
            val, *vals = vals[offset:]
        else:
            assert len(vals) > 0
            val = vals[0]

        yield node, val
        node = node.high if val else node.low
        offset = node.level - prev_lvl - 1
        assert offset >= 0

    yield node, None


def fold_path(merge, bexpr, vals, initial=None, manager=None):
    if manager is None:
        manager = bexpr.bdd

    def acc(prev_ctx_acc, node_val):
        prev_ctx, acc = prev_ctx_acc
        node, val = node_val
        ctx = _ctx(node, manager, prev_ctx=prev_ctx)
        return (ctx, merge(ctx, val, acc))

    return reduce(acc, path(bexpr, vals), (None, initial))[1]
