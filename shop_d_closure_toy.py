#!/usr/bin/env python3
"""
shop_d_closure_toy.py
Toy computation of the external-maintenance load E_ext, of the progressive-
removal closure test (SHOP-D Sections 3.1 and 10.2) and of the substrate-closure
load (SHOP-D Section 10.3), plus a sensitivity analysis over the model's
free parameters.

THIS IS AN ILLUSTRATION OF THE PROCEDURE. Every result below follows from the
dependency structure that is assumed in each scenario. Nothing here is evidence
about any physical or digital system.

Usage
-----
    python shop_d_closure_toy.py             # Table A1 (scenarios A-E)
    python shop_d_closure_toy.py --sens      # Table A1 + sensitivity (Table A2)
    python shop_d_closure_toy.py --checks    # assertions on two extra cases
    python shop_d_closure_toy.py --struct    # structural sensitivity (A3-A5)

Model
-----
* A component c has a health h_c in [0, 1] (starts at 1.0).
* Each component has a set of required regenerators (all required, conjunctive).
  A regenerator is either another component (active if its health >= theta) or
  an external maintenance process (active unless the test removes it).
* A requirement is either a single regenerator or a group "at least k of these
  regenerators" (Any(...) is k = 1). Plain sets of requirements are conjunctive.
* If all requirements of c are met, h_c recovers; otherwise it decays.
* Resource dependencies (e.g. POWER) are tracked separately. They are not
  maintenance, so they are excluded from E_ext (SHOP-D 3.1). A resource is
  available while its external supply is on. When a test cuts the external
  supply, the resource stays available only if one of its declared internal
  regulators (a component) is active. These regulators are an assumption of
  the scenario, like every other dependency.
* Identity region I: every component in the declared constitutive set C_id has
  health >= theta at the end of the run.

Closure test (10.2): remove external maintenance processes progressively
(cumulatively, in alphabetical order, so the last step has all of them off); if
the system leaves I, reclassify the supports removed so far as constitutive;
report E_ext after reclassification against the bound eps. The variant that
removes each process alone ("each") is kept for comparison (--struct).

Substrate-closure load (10.3): a resource is a substrate dependency of I if
cutting its external supply (nothing else changed) expels the system from I.
Such a dependency counts as regulated if I survives when its external supply is
cut AND every external maintenance process is removed, so that only the system's
own operation can restore it. Load = regulated / substrate dependencies
(n/a if there are none). Regulation that works only while an external process
is active therefore does not count (the falsification condition of 10.3).
"""
import itertools
import random
import sys
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Params:
    theta: float = 0.5     # activity threshold
    rise: float = 0.2      # recovery per step
    decay: float = 0.2     # decay per step
    steps: int = 40        # simulation length
    eps: float = 0.10      # pre-registered bound on E_ext


BASE = Params()
RESOURCES = {"POWER"}                      # supplied, not maintained
EXTERNAL = {"OPERATOR", "OPERATOR2"}       # external maintenance processes


@dataclass(frozen=True)
class Group:
    """Requirement met when at least k of the members are met."""
    k: int
    members: tuple


def Any(*m):
    return Group(1, tuple(sorted(m)))


def AtLeast(k, *m):
    return Group(k, tuple(sorted(m)))


def leaves(r):
    if isinstance(r, Group):
        for m in r.members:
            yield from leaves(m)
    else:
        yield r


def req_leaves(c, required):
    return {x for r in required[c] for x in leaves(r)}


def satisfied(r, required, active, avail, removed):
    if isinstance(r, Group):
        return sum(satisfied(m, required, active, avail, removed)
                   for m in r.members) >= r.k
    if r in required:
        return r in active                 # another component
    if r in RESOURCES:
        return r in avail                  # a resource
    return r not in removed                # an external maintenance process


def simulate(required, removed=frozenset(), cut=frozenset(), regulators=None,
             p=BASE, reliability=None, rng=None):
    """Final health of every component.
    removed:     external maintenance processes switched off.
    cut:         resources whose external supply is switched off.
    regulators:  {resource: set of components that can keep it available}.
    reliability: {resource: q}; a regulated resource is available on a given
                 step only with probability q (needs rng). Default: always."""
    regulators = regulators or {}
    reliability = reliability or {}
    h = {c: 1.0 for c in required}
    for _ in range(p.steps):
        active = {c for c in h if h[c] >= p.theta}
        avail = set()
        for r in RESOURCES:
            if r not in cut:
                avail.add(r)
            elif regulators.get(r, set()) & active:
                q = reliability.get(r, 1.0)
                if q >= 1.0 or rng.random() < q:
                    avail.add(r)
        new = {}
        for c, reqs in required.items():
            ok = all(satisfied(r, required, active, avail, removed)
                     for r in reqs)
            nh = h[c] + p.rise if ok else h[c] - p.decay
            new[c] = round(min(1.0, max(0.0, nh)), 9)   # rounding avoids
        h = new                                         # float artefacts
    return h


def in_identity_region(h, cid, p=BASE):
    return all(h[c] >= p.theta for c in cid)


def externally_maintained(c, required):
    return bool(req_leaves(c, required) & EXTERNAL)


def e_ext(cid, required):
    if not cid:
        return 0.0
    return sum(externally_maintained(c, required) for c in cid) / len(cid)


def naive_e_ext(cid, required):
    """E_ext if resource supply were (wrongly) counted as maintenance."""
    ext = EXTERNAL | RESOURCES
    return sum(bool(req_leaves(c, required) & ext) for c in cid) / len(cid)


def requirement_closure(cid, required):
    seen, stack = set(cid), list(cid)
    while stack:
        for r in req_leaves(stack.pop(), required):
            if r in required and r not in seen:
                seen.add(r); stack.append(r)
    return seen


def used_externals(required):
    return sorted({x for c in required for x in req_leaves(c, required)}
                  & EXTERNAL)


def closure_test(required, declared_cid, p=BASE, removal="cumulative"):
    """removal = "cumulative" (default, progressive) or "each" (one at a time)."""
    cid = set(declared_cid)
    declared = e_ext(cid, required)
    off = set()
    for proc in used_externals(required):              # progressive removal
        off = off | {proc} if removal == "cumulative" else {proc}
        h = simulate(required, removed=off, p=p)
        if not in_identity_region(h, cid, p):          # support is constitutive
            reach = requirement_closure(cid, required)
            cid |= {c for c in reach if off & req_leaves(c, required)}
    return declared, e_ext(cid, required), naive_e_ext(cid, required), cid


def substrate_load(required, cid, regulators, p=BASE):
    """Regulated / total substrate dependencies of I (None if there are none)."""
    deps, regulated = [], []
    for r in sorted(RESOURCES):
        h = simulate(required, cut={r}, p=p)           # no regulation, operator on
        if in_identity_region(h, cid, p):
            continue                                   # I does not depend on r
        deps.append(r)
        h = simulate(required, removed=EXTERNAL, cut={r},
                     regulators=regulators, p=p)       # only own operation helps
        if in_identity_region(h, cid, p):
            regulated.append(r)
    return len(regulated) / len(deps) if deps else None


def run(s, p=BASE, removal="cumulative"):
    declared, after, naive, cid = closure_test(s["required"], s["declared"], p,
                                               removal)
    sub = substrate_load(s["required"], cid, s.get("regulators", {}), p)
    return dict(declared=declared, after=after, naive=naive, substrate=sub,
                closure="supported" if after <= p.eps else "falsified",
                cid=sorted(cid))


P = "POWER"
_CORE = {"R": {"M", P}, "H": {"R", "SE", P}, "V": {"H", "SE", P}, "M": {"V", P}}
SCENARIOS = {
 "A. SHOP-D as specified; SE declared supporting": dict(
    declared={"R", "H", "V", "M"},
    required={**_CORE, "SE": {"OPERATOR", P}}),
 "B. SHOP-D as specified; SE declared constitutive": dict(
    declared={"R", "H", "V", "M", "SE"},
    required={**_CORE, "SE": {"OPERATOR", P}}),
 "C. SE gates nothing (truly supporting)": dict(
    declared={"R", "H", "V", "M"},
    required={"R": {"M", P}, "H": {"R", P}, "V": {"H", P},
              "M": {"V", P}, "SE": {"OPERATOR", P}}),
 "D. Hypothetical redesign: SE regenerated by V": dict(
    declared={"R", "H", "V", "M", "SE"},
    required={**_CORE, "SE": {"V", P}}),
 "E. As D, and M regulates the power supply": dict(
    declared={"R", "H", "V", "M", "SE"},
    required={**_CORE, "SE": {"V", P}},
    regulators={P: {"M"}}),
}


def fmt(x):
    return "n/a" if x is None else f"{x:.2f}"


def print_table():
    print(f"epsilon = {BASE.eps}, theta = {BASE.theta}, steps = {BASE.steps}\n")
    head = ("Scenario", "E_ext declared", "E_ext after removal",
            "E_ext if resources counted", "closure vs eps", "substrate load")
    print(" | ".join(head))
    for name, s in SCENARIOS.items():
        r = run(s)
        print(f"{name} | {r['declared']:.2f} | {r['after']:.2f} | "
              f"{r['naive']:.2f} | {r['closure']} | {fmt(r['substrate'])}   "
              f"(final C_id = {r['cid']})")


# ------------------------------------------------------- structural variants
O1, O2 = "OPERATOR", "OPERATOR2"
STRUCT_SCENARIOS = {
 "F. As A, but the SE has two operators (either suffices)": dict(
    declared={"R", "H", "V", "M"},
    required={**_CORE, "SE": {Any(O1, O2), P}}),
 "G. As A, plus internal backup B that can replace the SE": dict(
    declared={"R", "H", "V", "M"},
    required={"R": {"M", P}, "H": {"R", Any("SE", "B"), P},
              "V": {"H", Any("SE", "B"), P}, "M": {"V", P},
              "B": {"V", P}, "SE": {O1, P}}),
 "H. As A, but H and V need 2 of {SE, B1, B2}, B1 and B2 internal": dict(
    declared={"R", "H", "V", "M"},
    required={"R": {"M", P}, "H": {"R", AtLeast(2, "SE", "B1", "B2"), P},
              "V": {"H", AtLeast(2, "SE", "B1", "B2"), P}, "M": {"V", P},
              "B1": {"V", P}, "B2": {"V", P}, "SE": {O1, P}}),
}


def print_struct_table():
    print("\nTABLE A3  structural variants, closure claim at eps = 0.10")
    print("Scenario | E_ext after (each alone) | verdict | "
          "E_ext after (cumulative) | verdict")
    for name, s in STRUCT_SCENARIOS.items():
        a = run(s, removal="each")
        b = run(s, removal="cumulative")
        print(f"{name} | {a['after']:.2f} | {a['closure']} | "
              f"{b['after']:.2f} | {b['closure']}")


def regulated_fraction(q, seeds=range(1000), p=BASE):
    """Share of runs in which I survives with POWER cut, every external
    process removed, and M regulating POWER on each step with probability q."""
    s = SCENARIOS["E. As D, and M regulates the power supply"]
    ok = 0
    for sd in seeds:
        h = simulate(s["required"], removed=EXTERNAL, cut={P},
                     regulators=s["regulators"], p=p,
                     reliability={P: q}, rng=random.Random(sd))
        ok += in_identity_region(h, s["declared"], p)
    return ok / len(seeds)


QS = [1.0, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]


def print_reliability():
    print("\nTABLE A4  scenario E with an intermittent regulator "
          "(1000 seeded runs per row)")
    print("q (P[M restores POWER on a step]) | share of runs with substrate "
          "load 1.00")
    for q in QS:
        print(f"{q:.2f} | {regulated_fraction(q):.3f}")


def survivors(required, removed):
    """Analytic oracle: greatest set of components that sustain themselves."""
    alive = set(required)
    changed = True
    while changed:
        changed = False
        for c in sorted(alive):
            if not all(satisfied(r, required, alive, RESOURCES, removed)
                       for r in required[c]):
                alive.discard(c)
                changed = True
    return alive


def random_structure(rng, p_ext=0.25, p_group=0.25):
    """p_ext: chance that a leaf requirement is an external process;
    p_group: chance that a requirement is a k-of-n group."""
    n = rng.randint(3, 7)
    comps = [f"c{i}" for i in range(n)]

    def leaf(c):
        x = rng.random()
        if x < p_ext:
            return rng.choice([O1, O2])
        if x < p_ext + 0.15:
            return P
        return rng.choice([d for d in comps if d != c])

    required = {}
    for c in comps:
        items = set()
        for _ in range(rng.randint(1, 3)):
            if rng.random() < p_group:
                m = {leaf(c) for _ in range(rng.randint(2, 3))}
                if len(m) < 2:
                    continue
                items.add(Group(rng.randint(1, len(m)), tuple(sorted(m))))
            else:
                items.add(leaf(c))
        required[c] = items
    declared = set(rng.sample(comps, rng.randint(2, n)))
    return dict(required=required, declared=declared)


SWEEP_GRID = [(0.25, 0.25), (0.10, 0.25), (0.10, 0.50), (0.05, 0.50)]


def structural_sweep(p_ext, p_group, n=5000, seed=0):
    rng = random.Random(seed)
    mism = 0                              # simulation vs analytic oracle
    cnt = dict(total=0, dep=0, miss_each=0, miss_cum=0, cons=0,
               cons_direct=0, miss_each_multi=0)
    for _ in range(n):
        s = random_structure(rng, p_ext, p_group)
        req = s["required"]
        for off in ({O1}, {O2}, {O1, O2}, set()):
            h = simulate(req, removed=off)
            if {c for c in h if h[c] >= BASE.theta} != survivors(req, off):
                mism += 1
        exts = used_externals(req)
        dep = not (s["declared"] <= survivors(req, set(exts)))
        each = run(s, removal="each")["closure"] == "falsified"
        cum = run(s, removal="cumulative")["closure"] == "falsified"
        direct = any(externally_maintained(c, req) for c in s["declared"])
        cnt["total"] += 1
        cnt["dep"] += dep
        cnt["miss_each"] += dep and not each
        cnt["miss_cum"] += dep and not cum
        cnt["miss_each_multi"] += dep and not each and len(exts) >= 2
        cnt["cons"] += (not dep) and cum      # falsified although I survives
        cnt["cons_direct"] += (not dep) and cum and direct
    return mism, cnt


def print_struct_sweep():
    print("\nTABLE A5  random dependency structures (3-7 components, "
          "AND / k-of-n requirements, external processes OPERATOR and "
          "OPERATOR2, seed 0, 5000 structures per row)")
    print("p_ext | p_group | oracle mismatches | I depends on externals | "
          "missed (each alone) | missed (cumulative) | "
          "falsified though I survives (all of them name an external)")
    for pe, pg in SWEEP_GRID:
        mism, c = structural_sweep(pe, pg)
        assert c["cons"] == c["cons_direct"]
        print(f"{pe:.2f} | {pg:.2f} | {mism} | {c['dep']} | "
              f"{c['miss_each']} | {c['miss_cum']} | {c['cons']}")


# ---------------------------------------------------------------- sensitivity
SWEEPS = {                       # one-at-a-time ranges around BASE
    "theta": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    "rise":  [0.05, 0.1, 0.2, 0.3, 0.5, 1.0],
    "decay": [0.05, 0.1, 0.2, 0.3, 0.5, 1.0],
    "steps": [1, 2, 3, 5, 10, 20, 40, 80, 160],
    "eps":   [0.0, 0.05, 0.10, 0.15, 0.19, 0.20, 0.25],
}
GRID = {                         # full factorial grid
    "theta": [0.3, 0.4, 0.5, 0.6, 0.7],
    "rise":  [0.1, 0.2, 0.4],
    "decay": [0.1, 0.2, 0.4],
    "steps": [10, 20, 40, 80],
    "eps":   [0.05, 0.10, 0.15],
}


def signature(r):
    return (r["closure"], r["substrate"])


def sensitivity():
    base = {n: signature(run(s)) for n, s in SCENARIOS.items()}
    print("\nSENSITIVITY ANALYSIS (verdict = closure claim, substrate load)")
    print("\nBaseline:", {n[0]: v for n, v in base.items()})

    print("\n(1) One-at-a-time sweeps: values at which a verdict differs "
          "from baseline")
    for par, values in SWEEPS.items():
        flips = {}
        for v in values:
            p = replace(BASE, **{par: v})
            for n, s in SCENARIOS.items():
                if signature(run(s, p)) != base[n]:
                    flips.setdefault(n[0], []).append(v)
        print(f"  {par:6s} tested {values}")
        print(f"         changed: {flips if flips else 'none'}")

    print("\n(2) Full factorial grid:",
          " x ".join(f"{len(v)} {k}" for k, v in GRID.items()), "=",
          len(list(itertools.product(*GRID.values()))), "settings")
    keys = list(GRID)
    changed = {n[0]: [] for n in SCENARIOS}
    total = 0
    for vals in itertools.product(*GRID.values()):
        p = Params(**dict(zip(keys, vals)))
        total += 1
        for n, s in SCENARIOS.items():
            if signature(run(s, p)) != base[n]:
                changed[n[0]].append(vals)
    for k, lst in changed.items():
        print(f"  scenario {k}: verdict unchanged in {total - len(lst)}/{total}"
              f" settings")
        if lst:
            steps_involved = sorted({v[keys.index('steps')] for v in lst})
            print(f"      changed only at steps in {steps_involved}; "
                  f"e.g. (theta, rise, decay, steps, eps) = {lst[0]}")
    return changed


def min_steps_to_detect():
    """Smallest horizon at which each scenario reaches its baseline verdict."""
    print("\n(3) Minimum simulation length that reproduces the baseline "
          "verdicts (theta=0.5, decay=0.2):")
    base = {n: signature(run(s)) for n, s in SCENARIOS.items()}
    for n, s in SCENARIOS.items():
        for k in range(1, 200):
            if signature(run(s, replace(BASE, steps=k))) == base[n]:
                print(f"  scenario {n[0]}: steps >= {k}")
                break


def checks():
    """Two cases that are not rows of Table A1."""
    # (a) the regulator of POWER is itself maintained by the external operator:
    #     regulation that disappears with external maintenance does not count.
    s = dict(declared={"R", "H", "V", "M", "SE"},
             required={**_CORE, "SE": {"OPERATOR", P}},
             regulators={P: {"SE"}})
    assert run(s)["substrate"] == 0.0
    # (b) two resources, only one regulated by the system: load is 0.5.
    RESOURCES.add("CLOCK")
    try:
        req = {"R": {"M", P, "CLOCK"}, "H": {"R", "SE", P},
               "V": {"H", "SE", P}, "M": {"V", P}, "SE": {"V", P}}
        s = dict(declared=set(req), required=req, regulators={P: {"M"}})
        assert run(s)["substrate"] == 0.5
    finally:
        RESOURCES.discard("CLOCK")
    # (c) structural variants (Table A3): removal 'each alone' misses F.
    F, G, H = STRUCT_SCENARIOS.values()
    assert run(F, removal="each")["closure"] == "supported"
    assert run(F, removal="cumulative")["closure"] == "falsified"
    for s in (G, H):
        assert run(s, removal="each")["closure"] == "supported"
        assert run(s, removal="cumulative")["closure"] == "supported"
    print("checks passed: externally mediated regulation -> 0.00; "
          "one of two resources regulated -> 0.50; structural variants F, G, H")


if __name__ == "__main__":
    print_table()
    if "--checks" in sys.argv:
        checks()
    if "--struct" in sys.argv:
        print_struct_table()
        print_reliability()
        print_struct_sweep()
    if "--sens" in sys.argv:
        sensitivity()
        min_steps_to_detect()
