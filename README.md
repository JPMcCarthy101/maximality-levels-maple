# Maximality Levels — Maple computations

Computational material accompanying J. P. McCarthy, *Maximality Levels of the Classical Permutation Group in the Quantum Permutation Group*.

This repository provides the Maple calculations supporting the paper's results on the inclusion \(S_N\subseteq S_N^+\), including maximality at **easiness level three** and **moment level six**. The code focuses on the paper's computational arguments in Section 7; the categorical and number-theoretic proofs are in the paper itself. The full Maximality Conjecture is **not** claimed here.

## Reproducing the calculations

**Software:** Maple. The author executed the worksheets successfully using **Maple 2026.1 on 64-bit Windows** on 29 October 2026. No additional Maple packages or external data files are required. Other Maple releases have not been tested here.

Two self-contained Maple worksheets are provided:

- [`notebooks/MomentLevel5.mw`](notebooks/MomentLevel5.mw) — moment five: the \(10\times10\) matrix, determinant, and the special case \(N=4\).
- [`notebooks/MomentLevel6.mw`](notebooks/MomentLevel6.mw) — moment six: the \(66\times71\) matrix, rank, polynomial kernel, rotation/reflection, contraction, squaring and final polynomial reductions.

To reproduce the saved results, open either worksheet in Maple and **execute all input groups from the beginning**. They start with `restart:` and can be run independently. Matching plain-text Maple programs are supplied in `src/`. From the repository root, they can also be run in Maple with:

```maple
read "src/MomentLevel5.mpl";
read "src/MomentLevel6.mpl";
```

The optional launcher `src/RunAll.mpl` reads both programs in order. The two worksheet runs, rather than the launcher, are the runs documented below.

**Important:** The complete moment-six computation requires `RUN_UNIFORM_RANK_CHECK := true`, which is the default in `src/MomentLevel6.mpl` and the matching worksheet. This performs the exact symbolic determinant comparison and may take considerably longer than the other checks. `RUN_N4_CHECK` controls the additional \(N=4\) rank check. `SHOW_ALL_SQUARING_ROWS` controls whether all 71 quadratic output entries are printed.

Both completed worksheets, including the saved Maple outputs, are available in [`results/executed/`](results/executed/). The [author's execution record](results/AUTHOR_EXECUTION_2026-10-29.md) identifies the software version and summarises the observed results. The execution time was not recorded.

## Locating computations cited in the paper

| Manuscript location | Computation | Where to look |
|---|---|---|
| Eq. (13)–(14), Prop. 7.3 | Moment-five matrix, determinant, \(N=4\) rank and partition identity | [`src/MomentLevel5.mpl`](src/MomentLevel5.mpl), sections 2–5 |
| Eq. (15)–(16), Prop. 7.4 | Moment-six matrix, first 66-column minor and determinant | [`src/MomentLevel6.mpl`](src/MomentLevel6.mpl), sections 2–3b |
| Prop. 7.6 | Five polynomial kernel vectors and rotation/reflection tests | Moment-six source, sections 3–4b |
| Eq. (17)–(19), Prop. 7.7 | Rotation matrix and fixed-space projection | Moment-six source, section 4 |
| Eq. (20), Prop. 7.8 | Contraction and the two positive coefficients | Moment-six source, sections 5–7 |
| Eq. (21)–(23), Prop. 7.9 | Rotate–square–rotate and 71 crossing coefficients | Moment-six source, squaring sections 1–4 |
| Eq. (24)–(26) | Polynomial expressions \(g_N,h_N,k_N\) | Moment-six source, squaring sections 5–6 |
| Eq. (28)–(33) | Factorisation and final case reductions | Moment-six source, final section 7 |

The [structured paper-to-code index](data/PAPER_CODE_INDEX.json) gives more detailed references and expected outputs. Equation numbers follow the accompanying manuscript version and should be checked against any later revisions.

## How the computations are encoded

Partitions are represented by **restricted-growth words**: a sequence `[w1,...,wk]` whose labels start at zero and increase only when a new block is introduced. For example, `[0,1,0,1]` represents the basic four-point crossing. Partitions are generated deterministically in the order implemented by `Words(k)`; the lists `CR5` and `CR6` retain only crossing partitions in that order.

Each partition operation specifies ordered output groups and capped (deleted) groups. The `Lower` procedure glues the corresponding blocks, returns the resulting partition and counts closed components; every closed component contributes a factor of \(N\). **Matrix entries are computed from these operations**, not entered as a precomputed matrix.

For moment six the 66 operations are ordered in five families of sizes **15 + 30 + 6 + 9 + 6**, as specified in the source. The determinant uses the **first 66 columns** of the resulting \(66\times71\) matrix, with columns ordered by `CR6`. The polynomial kernel basis is stored explicitly and checked against the reconstructed matrix. These conventions matter when comparing a particular row or column with the manuscript.

The software-independent description is in [`pseudocode/ALGORITHMS.md`](pseudocode/ALGORITHMS.md).

## Repository contents

| Directory | Contents |
|---|---|
| [`notebooks/`](notebooks/) | Two clean Maple worksheets (`.mw`) |
| [`src/`](src/) | Equivalent plain-text Maple code (`.mpl`) and launcher |
| [`data/`](data/) | Detailed manuscript-to-code index |
| [`pseudocode/`](pseudocode/) | Algorithm descriptions independent of Maple syntax |
| [`results/`](results/) | Author-executed worksheets, execution record and selected comparison output |
| [`tests/`](tests/) | Optional supplementary Python/SymPy checks at selected values of \(N\) |
| [`docs/`](docs/) | Provenance and scope of the computations |

The supplementary Python checks can be run with `python tests/python_spot_checks.py` after installing SymPy. They compare selected finite cases (including \(N=4,6,7\)); they are not a substitute for the **symbolic** Maple computation proving the displayed identities in the parameter \(N\).

## Scope and provenance

The Maple computations test the explicit partition constructions, matrix identities, polynomial expressions and algebraic reductions stated in the manuscript. They do not, by themselves, replace the mathematical arguments establishing that the operations are valid Tannaka–Krein operations or that the resulting identities yield the stated maximality results. In particular, the divisibility contradictions are argued mathematically in the paper.

The research calculations originated with the author. Some earlier computational work involved Claude, and the moment-six completion and consolidation involved ChatGPT. See [`docs/PROVENANCE_AND_LIMITATIONS.md`](docs/PROVENANCE_AND_LIMITATIONS.md) for context. The accompanying manuscript gives the fuller account of AI assistance.

## Citation

Please cite the accompanying paper when using these computations, and identify the exact repository commit or tagged release used. Citation metadata for the software is provided in [`CITATION.cff`](CITATION.cff).
