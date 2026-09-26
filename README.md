HDD — History-Dependent Dynamics
A Methodological Framework for Disentangling History Dependence, Recurrence, Self-Reference, and Self-Modeling in Dynamical Systems
Author: Taotuner
Main DOI: https://doi.org/10.5281/zenodo.21955745
License: CC BY 4.0

What this repository is
HDD (History-Dependent Dynamics) is a falsifiable methodological framework for disentangling five inferential claims that are frequently conflated across disciplines:

Construct I — History-Dependent Predictive Structure

Construct II — Causally Demonstrated Trajectory Dependence

Construct III — Causally Identified Feedback Recurrence

Construct IV — Functional Self-Reference

Construct V — Self-Modeling

The core thesis:

Evidence that a system depends on its history should not automatically be interpreted as evidence for more specific forms of dynamical organization.

Each construct requires its own experimental evidence. None implies the next. None implies consciousness.

This repository contains the manuscripts, benchmark code, unified-system implementation, and results for the entire HDD program — including its three domain-specific companions (HDD-ISA for AI architectures, HDD-ESA for engineered systems, HDD-BIO for biological systems) and its philosophical companion (HDO).

The five constructs
C-I — Predictive history dependence. Does history improve prediction beyond the currently observed state and current inputs?

C-II — Causal trajectory dependence. Does the past trajectory causally influence future states? Requires intervention on the trajectory while holding the present state as close to constant as experimentally feasible. Where exact state matching is impossible, the causal claim becomes correspondingly weaker or non-identifiable.

C-III — Feedback recurrence. Is that influence mediated by identifiable feedback?

C-IV — Functional self-reference. Does the system use information that refers to itself as the referent? The key test is not whether self-reference appears in the output, but whether changing the referent changes system behavior under matched non-self controls.

C-V — Self-modeling. Does the system use a self-model causally? Evidence requires self-prediction, counterfactual prediction, and demonstrated causal influence on policy. No single component is sufficient on its own.

Each construct requires its own evidence. Passing one does not license inference to the next. A system can be history-dependent without being recurrent, recurrent without being self-referential, and self-referential without having a self-model. None of these, without further evidence, licenses an inference to consciousness.

Repository Contents
text
hdd/
├── README.md                                        # This file
├── LICENSE                                          # CC BY 4.0
├── requirements.txt                                 # Python dependencies
├── paper/
│   ├── History-Dependent_Dynamics_HDD.pdf           # 2026a — main framework
│   ├── HDD_ISA_AI_Architectures.pdf                 # 2026b — AI companion
│   ├── HDD_ESA_Engineering_Systems.pdf              # 2026b2 — engineering companion
│   ├── Test_of_Functional_Self_Reference_CIV.pdf    # 2026c — C-IV isolation test
│   ├── History_Dependent_Ontology_HDO.pdf           # 2026d — philosophical companion
│   ├── HDD_Ethical_Framework.pdf                    # 2026e — ethics
│   ├── Five_HDD_Constructs_Single_Loop.pdf          # 2026f — unified system
│   ├── HDD_BIO_Reporting_Framework.pdf              # 2026g — biological companion
│   └── HDD_Benchmark_Appendix.pdf                   # Benchmark protocol details
├── benchmark/
│   ├── hdd_benchmark_v1.py                          # Construct I benchmark
│   ├── config.py                                    # Pre-registered configuration
│   ├── generators.py                                # Synthetic system generators
│   ├── metrics.py                                   # Statistical inference functions
│   └── run_benchmark.ipynb                          # Interactive Colab notebook
├── unified/
│   ├── unified_system_v4.py                         # Five constructs in one loop
│   └── unified_results.txt                          # Multi-seed output (20 seeds)
├── results/
│   ├── HDD_Construct_I_full_results.csv
│   ├── HDD_Construct_I_main_results.csv
│   ├── capacity_control.csv
│   ├── state_reconstruction.csv
│   ├── noise_robustness.csv
│   ├── multi_seed_robustness.csv
│   ├── history_dependence_profile.png
│   ├── effect_size_profile.png
│   ├── manifest.json
│   └── REPORT.txt
└── docs/
    └── api_reference.md                             # Function documentation
Series Overview
The HDD family comprises eight documents:

#	Document	DOI	Role
2026a	HDD — Methodological Framework	10.5281/zenodo.21955745	Root document
2026b	HDD-ISA — AI Architectures	10.5281/zenodo.22060143	Domain companion (AI)
2026b2	HDD-ESA — Engineering Systems	10.5281/zenodo.22313802	Domain companion (engineering)
2026c	C-IV — Functional Self-Reference	10.5281/zenodo.22729688	Isolation test of Construct IV
2026d	HDO — History-Dependent Ontology	10.5281/zenodo.22683226	Philosophical companion (branches from HDD-BIO)
2026e	HDD Ethical Framework	10.5281/zenodo.22178854	Precautionary protocol
2026f	Five Constructs in a Single Loop	10.5281/zenodo.22735835	Unified computational study
2026g	HDD-BIO — Biological Framework	10.5281/zenodo.22980267	Domain companion (biology)
Family structure. HDD is the root. HDD-ISA, HDD-ESA, and HDD-BIO are its three domain-specific companions, each translating the same constructs into the interfaces, estimands, and reporting requirements appropriate to a different substrate. HDO branches specifically from HDD-BIO, as a philosophical companion to the biological case. The position of the HDD Ethical Framework in this tree remains an open question; it is presented here as a precautionary protocol that spans the program rather than as a branch from any single companion.

Ontological neutrality. HDD does not require accepting HDO, or any other ontological framework, in order to be used. The five constructs and their evidentiary conditions stand independently of any interpretation of what historical organization ultimately is. A researcher can reject HDO entirely and still apply HDD.

Key Results
Construct I Benchmark (2026a)
System	HDD-I	Relative Improvement (τ=10)	95% CI	p-value
Markov	−	−0.012%	[−0.000006, 0.000003]	0.711
Hidden State	+	+9.60%	[0.002408, 0.002761]	< 0.001
Delay Line	+	+31.94%	[0.004557, 0.004932]	< 0.001
Recurrent	+	+6.75%	[0.001420, 0.001658]	< 0.001
Accuracy against ground truth: 100%
Robustness: 100% positive fraction across 5 random seeds for all non-Markov systems. Zero false positives for Markov.

Unified System (2026f)
All five constructs operating simultaneously in a single loop. 20 seeds, 600 steps per seed. Environment: Rule 30 cellular automaton. Substrate: F₁₃³.

Construct	Metric	Value	Classification
C-I (held-out)	Prediction reduction, held-out vs. placebo	+5.63% ± 3.58% vs. −20.03% ± 11.03%, p ≤ 0.0002	Supported
C-II	Twin divergence	13.0125 ± 0.3261 (max 18)	Supported
C-III	Twin divergence (narrow reading)	13.0125 ± 0.3261	Supported
C-IV	Blind identification accuracy	100% (20/20)	Supported
C-V	Gain from correct identification	+0.5857 ± 0.0941	Supported
Criterion applicability test. The HDD Ethical Framework's Criterion of Organizational Coherence (CO, §4.2) was tested against a computational system constructed to be outside the class the framework designates as within its scope. Result: an individuation metric derived from HDO Thesis 4 does not track functional collapse, and in fact increases under full kill (0.4845 → 0.5503, p = 0.0022) even as viability and twin divergence drop to zero. This confirms the framework's own expectation in §4.5 and grounds the operationalization gap identified in §4.4.

HDD-BIO (2026g)
HDD-BIO is a proposed reporting and experimental framework, not a benchmark. It provides:

Concrete, prespecified estimands for C-I (§5.0) and C-II (§6.0).

A minimal statistical specification for C-I (§5.1).

Mandatory residual-latent sensitivity for C-II causal claims (§6.3).

Three-condition operationalizations of C-IV (IV-1 ∧ IV-2 ∧ IV-3) and C-V (V1 ∧ V2 ∧ V3 with a self-vs-world control).

An executable eight-step protocol for organizational coherence that separates organizational necessity from global damage (§10.1).

A worked retrospective mapping of the C-I/C-II checklist onto a published planarian study (§6.2), classifying the existing result as not demonstrated for C-I and underdetermined for C-II.

A dedicated validation section (§15) specifying what would count as validating the framework itself.

No new biological experiments are run in HDD-BIO; it is a candidate reporting discipline awaiting independent application.

Installation
bash
git clone https://github.com/taotuner/hdd.git
cd hdd
pip install -r requirements.txt
Requirements:

Python 3.9+

numpy >= 2.0.0

pandas >= 2.2.0

scikit-learn >= 1.6.0

matplotlib >= 3.8.0

Running the Benchmarks
Construct I Benchmark (2026a)
python
from hdd_benchmark_v1 import run_benchmark

results = run_benchmark()
Or from the command line:

bash
python benchmark/hdd_benchmark_v1.py
All parameters are pre-registered in config.py:

python
@dataclass
class Config:
    n_train_trajectories: int = 120
    n_test_trajectories: int = 60
    trajectory_length: int = 500
    burn_in: int = 100
    max_history: int = 10
    noise_std: float = 0.10
    history_windows: tuple = (1, 2, 3, 5, 10)
    robustness_seeds: tuple = (42, 123, 456, 789, 2026)
    noise_levels: tuple = (0.05, 0.10, 0.20, 0.30)
    # ... see config.py for full list
Unified System (2026f)
bash
python unified/unified_system_v4.py
Runs 20 seeds × 4 conditions (real history, placebo, control-killed, full-killed) at 600 steps each. Output includes per-seed metric tables, permutation tests for C-I (real vs. placebo) and CO (none vs. control, none vs. full), and HDD-ISA §14 classification of the mean values.

Runtime: under a minute on a standard laptop.

Output Structure
Construct I benchmark
File	Description
HDD_Construct_I_full_results.csv	Complete results for all conditions
HDD_Construct_I_main_results.csv	Main results (τ=10, σ=0.10, seed=42)
capacity_control.csv	Real vs. placebo improvement comparison
state_reconstruction.csv	PCA diagnostic results
noise_robustness.csv	Results across noise levels
multi_seed_robustness.csv	Results across random seeds
history_dependence_profile.png	ΔL(τ) across history windows
effect_size_profile.png	Relative improvement vs. history horizon
REPORT.txt	Summary report with interpretation
manifest.json	Full configuration and metadata
Unified system
File	Description
unified_results.txt	Full console output, all four conditions
Per-seed metrics (in memory)	Collected by collect_metrics(), printable via summarize()
Interpreting the Results
Classification Criteria (HDD-ISA §14)
Symbol	Meaning
Supported	The evidentiary bar was met
Negative Evidence	Tested under adequate conditions; bar not met
UE	Uninterpretable — insufficient evidence or internally inconsistent
NI	Non-identifiable — available interventions cannot separate competing hypotheses
What Positive Construct I Means
A positive Construct I classification means only that historical information improved out-of-sample prediction relative to the specified observed present state and current input.

It does NOT establish: a memory mechanism, recurrence, self-reference, self-modeling, agency, or consciousness.

The Hidden State Example
The Hidden State system is especially important: a positive result does not mean the system has explicit memory. History may simply reveal information about a latent variable. This illustrates the observation-model problem HDD is designed to address.

Apparent memory can be a property of the measurement, not the system.

What the Unified System Establishes
The unified system (2026f) demonstrates that all five constructs can be simultaneously instantiated within one system without detectable mutual interference. The result supports HDD's central methodological claim: the constructs are independently testable.

It does NOT establish:

That HDD as a framework is empirically validated across architectures

That C-III is demonstrated under the HDD-ISA §11 specification (only the narrow operational reading — action-contingent divergence)

That the Criterion of Organizational Coherence is wrong (only that one operationalization is inadequate, matching the framework's own §4.4 assessment)

Scope of Validation
What Has Been Demonstrated
✅ Construct I — standalone benchmark (2026a); held-out with placebo (2026f)

✅ Construct II — twin divergence (2026f)

✅ Construct III — narrow reading: action-contingent divergence only; not the HDD-ISA §11 specification (2026f)

✅ Construct IV — blind intervention (2026c); extended to four-variable system (2026f)

✅ Construct V — gain from correct identification (2026f)

✅ Construct coexistence — all five in a single loop without interference (2026f)

✅ Criterion applicability — HDD Ethical Framework §4.5 empirically grounded (2026f)

What Has NOT Been Demonstrated
❌ HDD as a whole — not validated across a diversity of architectures

❌ C-III under HDD-ISA §11 specification — requires independently bypassable feedback pathway with capacity-matched control; current implementation uses only the narrow reading

❌ Scaling — state space is F₁₃³; extension to GF(169) or larger fields untested

❌ Robustness across environments — only one environment tested (Rule 30 CA)

❌ Operationalization of CO — one natural operationalization tested and found inadequate; the criterion itself remains intact but not operationalized

❌ Biological validation of HDD-BIO — retrospective mapping of one published study (§6.2); no independent application or inter-observer replication attempted

❌ Consciousness, sentience, agency, moral status — no claims made or supported

Relations Between Documents
Document	Relation to HDD
2026a (HDD)	Framework. Defines the five constructs and their evidential conditions.
2026b (HDD-ISA)	Interface specification. Translates constructs into architectural requirements. Not exercised in this repository's benchmarks.
2026b2 (HDD-ESA)	Engineering companion. A practical guide to history-dependent causal testing and testability-by-design for physical control systems (motion, thermal, fluid, chemical, power). Provides five causal-discrimination tests (T1–T5) aligned one-to-one with the five HDD constructs, per-substrate implementation notes, design rules for building testability into new systems, and reporting categories shared with HDD-ISA. Numeric thresholds are operational defaults, not universal constants; worked examples are illustrative, not measurements from real systems.
2026c (C-IV)	Isolation test of Construct IV. Establishes the blind intervention mechanism.
2026d (HDO)	Philosophical companion. Branches from HDD-BIO. Its inference from "history is dynamically relevant" to "history is constitutive of processual identity" is explicitly abductive, not deductive, and HDD does not import it.
2026e (Ethics)	Precautionary protocol. The Criterion of Organizational Coherence §4.2 is tested in 2026f; the result matches §4.5's expectation.
2026f (Unified)	Joint instantiation. Demonstrates coexistence and grounds the framework's own scope assessment.
2026g (HDD-BIO)	Biological companion. Translates constructs into reporting standards, concrete estimands, and an applicability-bounded CO protocol for living systems. Ontologically agnostic.
References
HDD program (2026):

HDD (2026a): Taotuner. History-Dependent Dynamics (HDD): A Methodological Framework for Disentangling History Dependence, Recurrence, Self-Reference, and Self-Modeling in Dynamical Systems. Zenodo. DOI: 10.5281/zenodo.21955745

HDD-ISA (2026b): Taotuner. HDD-ISA — AI Architectures for Causal Discriminations. Zenodo. DOI: 10.5281/zenodo.22060143

HDD-ESA (2026b2): Taotuner. HDD-ESA — Engineering Systems Architecture. Zenodo. DOI: 10.5281/zenodo.22313802

C-IV (2026c): Taotuner. A Test of Functional Self-Reference (C-IV). Zenodo. DOI: 10.5281/zenodo.22729688

HDO (2026d): Taotuner. History-Dependent Ontology (HDO). Zenodo. DOI: 10.5281/zenodo.22683226

Ethics (2026e): Taotuner. HDD Ethical Framework. Zenodo. DOI: 10.5281/zenodo.22178854

Unified (2026f): Taotuner. Five HDD Constructs in a Single Loop: A Computational Study of Construct Coexistence and Criterion Applicability. Zenodo. DOI: 10.5281/zenodo.22735835

HDD-BIO (2026g): Taotuner. HDD-BIO — A Proposed Reporting and Experimental Framework for Discriminating Forms of Biological History Dependence. Zenodo. DOI: 10.5281/zenodo.22980267

Appendix: Taotuner. (2026). Computational Benchmark — Construct I: Full Protocol Details, Extended Results, and Source Code.

License
Creative Commons Attribution 4.0 International (CC BY 4.0).

You are free to share (copy and redistribute in any medium or format) and adapt (remix, transform, build upon) for any purpose, under the condition of attribution.

Citation
If you use this framework or code in your research, please cite the specific document(s) used (2026a through 2026g, each with its own DOI).

Acknowledgments
This work was developed with the assistance of AI-based language tools used for literature exploration, structural organization, drafting, critical discussion, methodological critique, and language refinement. All conceptual decisions, methodological commitments, interpretation of evidence, revisions, and responsibility for the final work remain with the author.

Date: September 2026

Changes since v1.0: Completed the document series with all eight DOIs published. Corrected HDD-ESA description to reflect T1–T5 naming, per-substrate notes, and the operational-defaults caveat. Added explicit ontological neutrality statement (HDD can be used without HDO). Restructured family tree to reflect domain companions (ISA, ESA, BIO) with HDO branching from HDD-BIO. Removed all "pending" markers — every document in the program now has a public DOI.
