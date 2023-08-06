"""
Various functions and dispatchers for testing effects.

Usually the best way to test effects is by using :func:`perform_sequence`.
"""

from contextlib import contextmanager
from functools import partial
from operator import attrgetter

import attr

from ._base import Effect, guard, _Box, NoPerformerFoundError, raise_
from ._sync import NotSynchronousError, sync_perform, sync_performer
from ._intents import Constant, Error, Func, ParallelEffects, base_dispatcher


__all__ = [
    "perform_sequence",
    "parallel_sequence",
    "nested_sequence",
    "SequenceDispatcher",
    "noop",
    "const",
    "conste",
    "intent_func",
    "resolve_effect",
    "fail_effect",
    "EQDispatcher",
    "EQFDispatcher",
    "Stub",
    "ESConstant",
    "ESError",
    "ESFunc",
    "resolve_stubs",
    "resolve_stub",
]


def perform_sequence(seq, eff, fallback_dispatcher=None):
    """
    Perform an Effect by looking up performers for intents in an ordered
    "plan".

    First, an example::

        @do
        def code_under_test():
            r = yield Effect(MyIntent('a'))
            r2 = yield Effect(OtherIntent('b'))
            return (r, r2)

        def test_code():
            seq = [
                (MyIntent('a'), lambda i: 'result1'),
                (OtherIntent('b'), lambda i: 'result2')
            ]
            eff = code_under_test()
            assert perform_sequence(seq, eff) == ('result1', 'result2')

    Every time an intent is to be performed, it is checked against the next
    item in the sequence, and the associated function is used to calculate its
    result. Note that the objects used for intents must provide a meaningful
    ``__eq__`` implementation, since they will be checked for equality. Using
    something like `attrs`_ or `pyrsistent`_'s `PClass`_ is recommended for
    your intents, since they will auto-generate __eq__ and many other methods
    useful for immutable objects.

    .. _`attrs`: https://pypi.python.org/pypi/attrs
    .. _`pyrsistent`: https://pypi.python.org/pypi/pyrsistent
    .. _`PClass`: http://pyrsistent.readthedocs.org/en/latest/api.html#pyrsistent.PClass

    If an intent can't be found in the sequence or the fallback dispatcher, an
    ``AssertionError`` is raised with a log of all intents that were performed
    so far. Each item in the log starts with one of three prefixes:

    * ``sequence``: this intent was found in the sequence
    * ``fallback``: a performer for this intent was provided by the fallback
      dispatcher
    * ``NOT FOUND``: no performer for this intent was found.
    * ``NEXT EXPECTED``: the next item in the sequence, if there is one. This
      will appear immediately after a ``NOT FOUND``.

    :param list sequence: List of ``(intent, fn)`` tuples, where ``fn`` is a
        function that should accept an intent and return a result.
    :param Effect eff: The Effect to perform.
    :param fallback_dispatcher: A dispatcher to use for intents that aren't
        found in the sequence. if None is provided, ``base_dispatcher`` is
        used.
    :return: Result of performed sequence
    """

    def fmt_log():
        next_item = ""
        if len(sequence.sequence) > 0:
            next_item = "\nNEXT EXPECTED: %s" % (sequence.sequence[0][0],)
        return "{{{\n%s%s\n}}}" % ("\n".join("%s: %s" % x for x in log), next_item)

    def dispatcher(intent):
        p = sequence(intent)
        if p is not None:
            log.append(("sequence", intent))
            return p
        p = fallback_dispatcher(intent)
        if p is not None:
            log.append(("fallback", intent))
            return p
        else:
            log.append(("NOT FOUND", intent))
            raise AssertionError(
                "Performer not found: %s! Log follows:\n%s" % (intent, fmt_log())
            )

    if fallback_dispatcher is None:
        fallback_dispatcher = base_dispatcher
    sequence = SequenceDispatcher(seq)
    log = []
    with sequence.consume():
        return sync_perform(dispatcher, eff)


@object.__new__
class _ANY(object):
    def __eq__(self, o):
        return True

    def __ne__(self, o):
        return False


def parallel_sequence(parallel_seqs, fallback_dispatcher=None):
    """
    Convenience for expecting a ParallelEffects in an expected intent sequence,
    as required by :func:`perform_sequence` or :obj:`SequenceDispatcher`.

    This lets you verify that intents are performed in parallel in the
    context of :func:`perform_sequence`. It returns a two-tuple as expected by
    that function, so you can use it like this::

        @do
        def code_under_test():
            r = yield Effect(SerialIntent('serial'))
            r2 = yield parallel([Effect(MyIntent('a')),
                                 Effect(OtherIntent('b'))])
            return (r, r2)

        def test_code():
            seq = [
                (SerialIntent('serial'), lambda i: 'result1'),
                nested_parallel([
                    [(MyIntent('a'), lambda i: 'a result')],
                    [(OtherIntent('b'), lambda i: 'b result')]
                ]),
            ]
            eff = code_under_test()
            assert perform_sequence(seq, eff) == ('result1', 'result2')


    The argument is expected to be a list of intent sequences, one for each
    parallel effect expected. Each sequence will be performed with
    :func:`perform_sequence` and the respective effect that's being run in
    parallel. The order of the sequences must match that of the order of
    parallel effects.

    :param parallel_seqs: list of lists of (intent, performer), like
        what :func:`perform_sequence` accepts.
    :param fallback_dispatcher: an optional dispatcher to compose onto the
        sequence dispatcher.
    :return: (intent, performer) tuple as expected by :func:`perform_sequence`
        where intent is ParallelEffects object
    """
    perf = partial(perform_sequence, fallback_dispatcher=fallback_dispatcher)

    def performer(intent):
        if len(intent.effects) != len(parallel_seqs):
            raise AssertionError(
                "Need one list in parallel_seqs per parallel effect. "
                "Got %s effects and %s seqs.\n"
                "Effects: %s\n"
                "parallel_seqs: %s"
                % (
                    len(intent.effects),
                    len(parallel_seqs),
                    intent.effects,
                    parallel_seqs,
                )
            )
        return list(map(perf, parallel_seqs, intent.effects))

    return (ParallelEffects(effects=_ANY), performer)


@attr.s
class Stub(object):
    """
    DEPRECATED in favor of using :func:`perform_sequence`.


    An intent which wraps another intent, to flag that the intent should
    be automatically resolved by :func:`resolve_stub`.

    :class:`Stub` is intentionally not performable by any default
    mechanism.
    """

    intent = attr.ib()


def ESConstant(x):
    """DEPRECATED. Return Effect(Stub(Constant(x)))"""
    return Effect(Stub(Constant(x)))


def ESError(x):
    """DEPRECATED. Return Effect(Stub(Error(x)))"""
    return Effect(Stub(Error(x)))


def ESFunc(x):
    """DEPRECATED. Return Effect(Stub(Func(x)))"""
    return Effect(Stub(Func(x)))


def resolve_effect(effect, result, is_error=False):
    """
    Supply a result for an effect, allowing its callbacks to run.

    Note that is a pretty low-level testing utility; it's much better to use a
    higher-level tool like :func:`perform_sequence` in your tests.

    The return value of the last callback is returned, unless any callback
    returns another Effect, in which case an Effect representing that
    operation plus the remaining callbacks will be returned.

    This allows you to test your code in a somewhat "channel"-oriented
    way:

        eff = do_thing()
        next_eff = resolve_effect(eff, first_result)
        next_eff = resolve_effect(next_eff, second_result)
        result = resolve_effect(next_eff, third_result)

    Equivalently, if you don't care about intermediate results::

        result = resolve_effect(
            resolve_effect(
                resolve_effect(
                    do_thing(),
                    first_result),
                second_result),
            third_result)

    NOTE: parallel effects have no special support. They can be resolved with
    a sequence, and if they're returned from another effect's callback they
    will be returned just like any other effect.

    :param bool is_error: Indicate whether the result should be treated as an
        exception or a regular result.

    :param result: If ``is_error`` is False, this can be any object and will be
        treated as the result of the effect. If ``is_error`` is True, this must
        be an exception.
    """
    for i, (callback, errback) in enumerate(effect.callbacks):
        cb = errback if is_error else callback
        if cb is None:
            continue
        is_error, result = guard(cb, result)
        if type(result) is Effect:
            return Effect(
                result.intent, callbacks=result.callbacks + effect.callbacks[i + 1 :]
            )
    if is_error:
        raise result
    return result


def fail_effect(effect, exception):
    """
    Resolve an effect with an exception, so its error handler will be run.
    """
    try:
        raise exception
    except Exception as e:
        return resolve_effect(effect, e, is_error=True)


def resolve_stub(dispatcher, effect):
    """
    DEPRECATED in favor of :func:`perform_sequence`.

    Automatically perform an effect, if its intent is a :obj:`Stub`.

    Note that resolve_stubs is preferred to this function, since it handles
    chains of stub effects.
    """
    if type(effect.intent) is Stub:
        performer = dispatcher(effect.intent.intent)
        if performer is None:
            raise NoPerformerFoundError(effect.intent.intent)
        result_slot = []
        box = _Box(result_slot.append)
        performer(dispatcher, effect.intent.intent, box)
        if len(result_slot) == 0:
            raise NotSynchronousError(
                "Performer %r was not synchronous during stub resolution for "
                "effect %r" % (performer, effect)
            )
        if len(result_slot) > 1:
            raise RuntimeError(
                "Pathological error (too many box results) while running "
                "performer %r for effect %r" % (performer, effect)
            )
        return resolve_effect(effect, result_slot[0][1], is_error=result_slot[0][0])
    else:
        raise TypeError("resolve_stub can only resolve stubs, not %r" % (effect,))


def resolve_stubs(dispatcher, effect):
    """
    DEPRECATED in favor of using :func:`perform_sequence`.

    Successively performs effects with resolve_stub until a non-Effect value,
    or an Effect with a non-stub intent is returned, and return that value.

    Parallel effects are supported by recursively invoking resolve_stubs on
    the child effects, if all of their children are stubs.
    """
    if type(effect) is not Effect:
        raise TypeError("effect must be Effect: %r" % (effect,))

    while type(effect) is Effect:
        if type(effect.intent) is Stub:
            effect = resolve_stub(dispatcher, effect)
        elif type(effect.intent) is ParallelEffects:
            if not all(isinstance(x.intent, Stub) for x in effect.intent.effects):
                break
            else:
                effect = resolve_effect(
                    effect,
                    list(
                        map(partial(resolve_stubs, dispatcher), effect.intent.effects)
                    ),
                )
        else:
            break

    return effect


@attr.s
class EQDispatcher(object):
    """
    An equality-based (constant) dispatcher.

    This dispatcher looks up intents by equality and performs them by returning
    an associated constant value.

    This is sometimes useful, but :func:`perform_sequence` should be
    preferred, since it constrains the order of effects, which is usually
    important.

    Users provide a mapping of intents to results, where the intents are
    matched against the intents being performed with a simple equality check
    (not a type check!).

    The mapping must be provided as a sequence of two-tuples. We don't use a
    dict because we don't want to require that the intents be hashable (in
    practice a lot of them aren't, and it's a pain to require it). If you want
    to construct your mapping as a dict, you can, just pass in the result of
    ``d.items()``.

    e.g.::

        >>> sync_perform(EQDispatcher([(MyIntent(1, 2), 'the-result')]),
        ...              Effect(MyIntent(1, 2)))
        'the-result'

    assuming MyIntent supports ``__eq__`` by value.

    :param list mapping: A sequence of tuples of (intent, result).
    """

    mapping = attr.ib()

    def __call__(self, intent):
        # Avoid hashing, because a lot of intents aren't hashable.
        for k, v in self.mapping:
            if k == intent:
                return sync_performer(lambda d, i: v)


@attr.s
class EQFDispatcher(object):
    """
    An Equality-based function dispatcher.

    This dispatcher looks up intents by equality and performs them by invoking
    an associated function.

    This is sometimes useful, but :func:`perform_sequence` should be
    preferred, since it constrains the order of effects, which is usually
    important.

    Users provide a mapping of intents to functions, where the intents are
    matched against the intents being performed with a simple equality check
    (not a type check!). The functions in the mapping will be passed only the
    intent and are expected to return the result or raise an exception.

    The mapping must be provided as a sequence of two-tuples. We don't use a
    dict because we don't want to require that the intents be hashable (in
    practice a lot of them aren't, and it's a pain to require it). If you want
    to construct your mapping as a dict, you can, just pass in the result of
    ``d.items()``.

    e.g.::

        >>> sync_perform(
        ...     EQFDispatcher([(
        ...         MyIntent(1, 2), lambda i: 'the-result')]),
        ...     Effect(MyIntent(1, 2)))
        'the-result'

    assuming MyIntent supports ``__eq__`` by value.

    :param list mapping: A sequence of two-tuples of (intent, function).
    """

    mapping = attr.ib()

    def __call__(self, intent):
        # Avoid hashing, because a lot of intents aren't hashable.
        for k, v in self.mapping:
            if k == intent:
                return sync_performer(lambda d, i: v(i))


@attr.s
class SequenceDispatcher(object):
    """
    A dispatcher which steps through a sequence of (intent, func) tuples and
    runs ``func`` to perform intents in strict sequence.

    This is the dispatcher used by :func:`perform_sequence`. In general that
    function should be used directly, instead of this dispatcher.

    It's important to use `with sequence.consume():` to ensure that all of the
    intents are performed. Otherwise, if your code has a bug that causes it to
    return before all effects are performed, your test may not fail.

    :obj:`None` is returned if the next intent in the sequence is not equal to
    the intent being performed, or if there are no more items left in the
    sequence (this is standard behavior for dispatchers that don't handle an
    intent). This lets this dispatcher be composed easily with others.

    :param list sequence: Sequence of (intent, fn).
    """

    sequence = attr.ib()

    def __call__(self, intent):
        if len(self.sequence) == 0:
            return
        exp_intent, func = self.sequence[0]
        if intent == exp_intent:
            self.sequence = self.sequence[1:]
            return sync_performer(lambda d, i: func(i))

    def consumed(self):
        """Return True if all of the steps were performed."""
        return len(self.sequence) == 0

    @contextmanager
    def consume(self):
        """
        Return a context manager that can be used with the `with` syntax to
        ensure that all steps are performed by the end.
        """
        yield
        if not self.consumed():
            raise AssertionError(
                "Not all intents were performed: {0}".format(
                    [x[0] for x in self.sequence]
                )
            )


def nested_sequence(
    seq, get_effect=attrgetter("effect"), fallback_dispatcher=base_dispatcher
):
    """
    Return a function of Intent -> a that performs an effect retrieved from the
    intent (by accessing its `effect` attribute, by default) with the given
    intent-sequence.

    A demonstration is best::

        SequenceDispatcher([
            (BoundFields(effect=mock.ANY, fields={...}),
             nested_sequence([(SomeIntent(), perform_some_intent)]))
        ])

    The point is that sometimes you have an intent that wraps another effect,
    and you want to ensure that the nested effects follow some sequence in the
    context of that wrapper intent.

    ``get_effect`` defaults to ``attrgetter('effect')``, so you can override it if
    your intent stores its nested effect in a different attribute. Or, more
    interestingly, if it's something other than a single effect, e.g. for
    ParallelEffects see the :func:`parallel_sequence` function.

    :param list seq: sequence of intents like :obj:`SequenceDispatcher` takes
    :param get_effect: callable to get the inner effect from the wrapper
        intent.
    :param fallback_dispatcher: an optional dispatcher to compose onto the
        sequence dispatcher.
    :return: ``callable`` that can be used as performer of a wrapped intent
    """

    def performer(intent):
        effect = get_effect(intent)
        return perform_sequence(seq, effect, fallback_dispatcher=fallback_dispatcher)

    return performer


def noop(intent):
    """
    Return None. This is just a handy way to make your intent sequences (as
    used by :func:`perform_sequence`) more concise when the effects you're
    expecting in a test don't return a result (and are instead only performed
    for their side-effects)::

        seq = [
            (Prompt('Enter your name: '), lambda i: 'Chris')
            (Greet('Chris'), noop),
        ]

    """
    return None


def const(value):
    """
    Return function that takes an argument but always return given `value`.
    Useful when creating sequence used by :func:`perform_sequence`. For example,

    >>> dt = datetime(1970, 1, 1)
    >>> seq = [(Func(datetime.now), const(dt))]

    :param value: This will be returned when called by returned function
    :return: ``callable`` that takes an arg and always returns ``value``
    """
    return lambda intent: value


def conste(excp):
    """
    Like :func:`const` but takes and exception and returns function that raises
    the exception

    :param excp: Exception that will be raised
    :type: :obj:`Exception`
    :return: ``callable`` that will raise given exception
    """
    return lambda intent: raise_(excp)


def intent_func(fname):
    """
    Return function that returns Effect of tuple of fname and its args. Useful
    in writing tests that expect intent based on args. For example, if you are
    testing following function::

        @do
        def code_under_test(arg1, arg2, eff_returning_func=eff_returning_func):
            r = yield Effect(MyIntent('a'))
            r2 = yield eff_returning_func(arg1, arg2)
            return (r, r2)

    you will need to know the intents which ``eff_returning_func`` generates
    to test this using :func:`perform_sequence`. You can avoid that by doing::

        def test_code():
            test_eff_func = intent_func("erf")
            seq = [
                (MyIntent('a'), const('result1')),
                (("erf", 'a1', 'a2'), const('result2'))
            ]
            eff = code_under_test('a1', 'a2', eff_returning_func=test_eff_func)
            assert perform_sequence(seq, eff) == ('result1', 'result2')

    Here, the ``seq`` ensures that ``eff_returning_func`` is called with arguments
    ``a1`` and ``a2``.

    :param str fname: First member of intent tuple returned
    :return: ``callable`` with multiple positional arguments
    """
    return lambda *a: Effect((fname,) + a)
