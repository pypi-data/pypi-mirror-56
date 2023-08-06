from functools import partial

import attr

from testtools.matchers import MatchesStructure, Equals

from . import Effect, raise_
from ._intents import Constant, Func, FirstError, parallel
from ._sync import sync_perform
from ._test_utils import MatchesReraisedExcInfo


@attr.s(hash=True)
class EquitableException(Exception):
    message = attr.ib()


class ParallelPerformerTestsMixin(object):
    """Common tests for any performer of :obj:`effect.ParallelEffects`."""

    def test_empty(self):
        """
        When given an empty list of effects, ``perform_parallel_async`` returns
        an empty list synchronusly.
        """
        result = sync_perform(self.dispatcher, parallel([]))
        self.assertEqual(result, [])

    def test_parallel(self):
        """
        'parallel' results in a list of results of the given effects, in the
        same order that they were passed to parallel.
        """
        result = sync_perform(
            self.dispatcher, parallel([Effect(Constant("a")), Effect(Constant("b"))])
        )
        self.assertEqual(result, ["a", "b"])

    def test_error(self):
        """
        When given an effect that results in a Error,
        ``perform_parallel_async`` result in ``FirstError``.
        """
        expected_exc = EquitableException(message="foo")
        reraise = partial(raise_, expected_exc)
        try:
            sync_perform(self.dispatcher, parallel([Effect(Func(reraise))]))
        except FirstError as fe:
            self.assertThat(
                fe,
                MatchesStructure(
                    index=Equals(0), exception=MatchesReraisedExcInfo(expected_exc)
                ),
            )
        else:
            self.fail("sync_perform should have raised FirstError.")

    def test_error_index(self):
        """
        The ``index`` of a :obj:`FirstError` is the index of the effect that
        failed in the list.
        """
        expected_exc = EquitableException(message="foo")
        reraise = partial(raise_, expected_exc)
        try:
            sync_perform(
                self.dispatcher,
                parallel(
                    [Effect(Constant(1)), Effect(Func(reraise)), Effect(Constant(2))]
                ),
            )
        except FirstError as fe:
            self.assertThat(
                fe,
                MatchesStructure(
                    index=Equals(1), exception=MatchesReraisedExcInfo(expected_exc)
                ),
            )
