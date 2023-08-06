import attr
import funcy as fn

import aiger_bv as BV
from aiger_bv import atom, identity_gate, AIGBV
from bidict import bidict
from pyrsistent import pmap
from pyrsistent.typing import PMap

import aiger_coins as aigc


def _create_input2dist(input2dist):
    return pmap({
        k: dist.with_output(k) if k != dist.output else dist
        for k, dist in input2dist.items()
    })


@attr.s(frozen=True, auto_attribs=True, eq=False, order=False)
class MDP:
    _aigbv: AIGBV
    input2dist: PMap[str, aigc.Distribution] = attr.ib(
        default=pmap(), converter=_create_input2dist
    )

    @property
    def env_inputs(self):
        return set(self.input2dist.keys())

    @property
    def inputs(self):
        return self._aigbv.inputs - self.env_inputs

    @property
    def outputs(self):
        return self._aigbv.outputs

    @property
    def aigbv(self):
        assert "##valid" not in self.outputs

        circ = self._aigbv
        is_valid = atom(1, 1, signed=False)
        for dist in self.input2dist.values():
            circ <<= dist.expr.aigbv
            is_valid &= dist.valid

        circ |= is_valid.with_output("##valid").aigbv
        return circ

    @property
    def aig(self):
        return self.aigbv.aig

    def __lshift__(self, other):
        if isinstance(other, aigc.Distribution):
            other = dist2mdp(other)
        elif isinstance(other, AIGBV):
            other = circ2mdp(other)

        assert isinstance(other, MDP)
        assert not (self.env_inputs & other.env_inputs)
        return circ2mdp(
            circ=self._aigbv << other._aigbv,
            input2dist=self.input2dist + other.input2dist,
        )

    def __rshift__(self, other):
        assert not isinstance(other, aigc.Distribution)
        return other << self

    def __or__(self, other):
        assert not (self.env_inputs & other.env_inputs)
        return circ2mdp(
            circ=self._aigbv | other._aigbv,
            input2dist=self.input2dist + other.input2dist,
        )

    def feedback(self, inputs, outputs, initials=None, latches=None,
                 keep_outputs=False):
        assert set(inputs) <= self.inputs
        circ = self._aigbv.feedback(
            inputs, outputs, initials, latches, keep_outputs
        )
        return circ2mdp(circ, input2dist=self.input2dist)

    def encode_trc(self, sys_actions, states):
        coin_flips = find_coin_flips(sys_actions, states, mdp=self)
        return [fn.merge(a, c) for a, c in zip(sys_actions, coin_flips)]

    def decode_trc(self, actions):
        circ = self.aigbv
        sys_actions = [fn.project(a, self.inputs) for a in actions]

        states = fn.lpluck(0, circ.simulate(actions))
        assert all(s['##valid'] for s in states)
        states = [fn.omit(s, {'##valid'}) for s in states]

        return sys_actions, states

    @fn.memoize
    def _reach_bdd(self):
        try:
            from aiger_bdd import to_bdd
        except ImportError:
            raise ImportError(
                "Need to install py-aiger-bdd to use this method."
            )

        circ = self.aigbv
        assert not ((circ.inputs | circ.outputs) & circ.latches)
        step, lmap = (self.aigbv >> BV.sink(1, ['##valid'])).cutlatches()

        for name, _ in lmap.values():
            step >>= BV.sink(step.omap[name].size, [name])

        check_eq = None
        for v in step.outputs:
            tmp = BV.atom(step.omap[v].size, v, signed=False) \
                == BV.atom(step.omap[v].size, f"{v}##next", signed=False)

            if check_eq is None:
                check_eq = tmp
            else:
                check_eq &= tmp

        reachable = step >> check_eq.aigbv
        assert len(reachable.outputs) == 1
        bexpr, _, _ = to_bdd(reachable, renamer=lambda _, x: x)
        prev_latch = dict(lmap.values())
        new2old = {v[0]: k for k, v in lmap.items()}
        return bexpr, prev_latch, reachable.imap, bidict(new2old)


def circ2mdp(circ, input2dist=None):
    if not isinstance(circ, AIGBV):
        circ = circ.aigbv

    if input2dist is None:
        return MDP(circ)

    return MDP(circ, input2dist=input2dist)


def dist2mdp(dist):
    circ = identity_gate(dist.size, dist.output)
    return circ2mdp(circ=circ, input2dist={dist.output: dist})


def find_coin_flips(actions, states, mdp):
    return list(_find_coin_flips(actions, states, mdp))


def _constraint(k, v):
    var = atom(len(v), k, signed=False)
    return var == BV.decode_int(v, signed=False)


def _find_coin_flips(actions, states, mdp):
    assert len(actions) == len(states)
    circ1 = mdp.aigbv
    bexpr, prev_latch, imap, relabels = mdp._reach_bdd()

    for action, state in zip(actions, states):
        state = fn.walk_keys("{}##next".format, state)

        assignment = fn.merge(prev_latch, action, state)
        coin_flips = bexpr.let(**imap.blast(assignment)).pick()
        coin_flips = imap.project(mdp.env_inputs).unblast(coin_flips)

        yield coin_flips

        if len(prev_latch) > 0:
            ext_action = fn.merge(action, coin_flips)

            latch_vals = fn.walk_keys(relabels.get, prev_latch)
            next_latch = circ1(ext_action, latches=latch_vals)[1]
            assert next_latch.keys() == latch_vals.keys()
            prev_latch = fn.walk_keys(relabels.inv.get, next_latch)
