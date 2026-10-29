# Maximality Levels: Maple calculations

**Companion computational material to** J. P. McCarthy, *Maximality Levels of the Classical Permutation Group in the Quantum Permutation Group*.

**Execution status.** The author ran both worksheets successfully in Maple 2026.1 on 29 October 2026. The complete saved `.mw` files are in [`results/executed/`](results/executed/), with a readable summary and run conditions in [`results/AUTHOR_EXECUTION_2026-10-29.md`](results/AUTHOR_EXECUTION_2026-10-29.md). The optional Python checks performed during assembly are recorded separately; they are not substitutes for the symbolic Maple run.

## Start here

There are two self-contained worksheets:

- [`notebooks/MomentLevel5.mw`](notebooks/MomentLevel5.mw): Section 7.1, equations (13)-(14), Proposition 7.3.
- [`notebooks/MomentLevel6.mw`](notebooks/MomentLevel6.mw): Section 7.2, equations (15)-(33), Propositions 7.4, 7.6-7.9.

Each worksheet contains all its own 1-D Maple code. They **do not depend on the working directory or on execution of another worksheet**. Plain-text versions are in `src/` with matching names. These worksheets and the corresponding `src/` files form the complete reader-facing execution path; the underlying calculations do not require any historical research files.

**How to run:** Open either `.mw` file in a licensed Maple installation (the source files record Maple 2025.2 as the original worksheet format), select the command to execute all input groups in order, and check for any Maple error. Alternatively, execute the corresponding `.mpl` file as Maple input. To run both from the repository root, use `read "src/RunAll.mpl";` (note that the second source restarts the Maple session). In a Maple session, one may use `read "src/MomentLevel5.mpl";` or `read "src/MomentLevel6.mpl";` from the repository root. Both sources begin with `restart:`.

For the **complete** moment-six run, `RUN_UNIFORM_RANK_CHECK` must remain `true` (it is set this way by default). The exact determinant computation may be slow. For development only, set it to `false`; such a shortened run does not establish the rank formula. `RUN_N4_CHECK` controls the additional observation at N=4. `SHOW_ALL_SQUARING_ROWS` enables the display of all 71 quadratic output polynomials.

The author's executed worksheets are already included as `results/executed/MomentLevel5_executed.mw` and `results/executed/MomentLevel6_executed.mw`. The version and saved output have been recorded in [`results/AUTHOR_EXECUTION_2026-10-29.md`](results/AUTHOR_EXECUTION_2026-10-29.md). The reusable [`run log template`](results/RUN_LOG_TEMPLATE.md) is provided for subsequent independent reproductions. The clean input-only worksheets in `notebooks/` and matching `src/` files remain unchanged.

## How partitions and operations are encoded

A partition of `[k]` is a **restricted-growth word** (RGS) `[w_1,...,w_k]`, whose labels start at `0` and introduce a new label in first-occurrence order. For example, `[0,1,0,1]` is the basic four-point crossing. `Words(k)` visits all RGSs via appending each label from `0` to the current maximum plus one, in increasing order. `CR5` and `CR6` are the **filtered lists of crossing RGSs in this exact order**. The algorithm uses four distinct positions `a<b<c<d` with `w[a]=w[c]`, `w[b]=w[d]` and `w[a]<>w[b]` to detect crossing. A useful one-page algorithmic description is in [`pseudocode/ALGORITHMS.md`](pseudocode/ALGORITHMS.md).

An operation is `[output_groups, cap_groups, family]`. `output_groups` is an ordered list, with each group specifying input points merged into an output position; `cap_groups` are groups of points identified and then deleted. The common `Lower` operation builds the corresponding equivalence relation, returns the RGS at the output and counts connected components absent from the output. Each removed component contributes a factor `N`.

**Moment five:** 5 deletions of one leg; 4 merges `{j,j+1}` for `j=1,..,4`; and one cyclic merge `{1,5}`. Their order is the order just listed. Column order is `CR5`.

**Moment six:** the 66 operations are enumerated in five successive families: 15 four-position restrictions (lexicographic subsets); 30 cyclic singleton-delete-and-merge operations (outer `x=1..6`, inner `y=1..6` with `x<>y`); 6 cyclic adjacent pair caps (`x=1..6`); 9 pairs of disjoint cyclic adjacency edges (edge pairs lexicographically); 6 triple merges (`x=1..6`). The first 66 columns of `M66` refer to the first 66 items of `CR6` under this precise ordering. `SavedWords` verifies that the stored polynomial basis uses the identical row ordering.

The matrix entries are **derived by actual partition gluing**. They are not stored as a 66-by-71 collection of claimed formulas. The 71-by-5 polynomial kernel matrix `V` is stored explicitly, then tested against all rows of the reconstructed matrix.

## Paper-to-code index

| Paper result | Source / computation | Expected result |
|---|---|---|
| Eq. (13), Section 7.1 | `src/MomentLevel5.mpl` / section 2 | Ten crossing partitions, ten operations, 10x10 matrix |
| Eq. (14) | Moment 5 / section 3 | `abs(det M5)=(N-4)(N^2-3N+1)^2` |
| Prop. 7.3 (N=4) | Moment 5 / sections 4-5 | rank 9; stated `eta`; exact discrete-vector identity at all 4^5 index tuples |
| Eq. (15), Prop. 7.4 | Moment 6 / section 2 | 71 crossing partitions; 66 operations; matrix 66x71 |
| Eq. (16) | Moment 6 / section 3b | `abs(det A)=(N-4)^12 (N-2)(N^2-3N+1)^23` |
| Note after Prop. 7.4 | Moment 6 / section 3b | rank `M(4)=54` |
| Prop. 7.6 | Moment 6 / sections 3, 4, 4b | `MV=0`, basis normalisation; rotation and reflection actions |
| Eqs. (17)-(19), Prop. 7.7 | Moment 6 / section 4 | matrix `R`, `R^3=I`, `P^2=P` and fixed space |
| Eq. (20), Prop. 7.8 | Moment 6 / sections 5-7 | gluing-based contraction, `A_N` and `B_N`, positivity over `N>=6` |
| Eqs. (21)-(23), Prop. 7.9 | Moment 6 / square sections 1-4 | full 71-entry crossing coefficient vector `beta` |
| Eqs. (24)-(26) | Moment 6 / square sections 5-6 | derived `g_N,h_N,k_N` and literal equality to paper expressions |
| Eqs. (28)-(33) | Moment 6 / final section 7 | printed product factorisation and both case reductions |

The structured version is at [`data/PAPER_CODE_INDEX.json`](data/PAPER_CODE_INDEX.json).

The Maple source checks algebraic identities and gluing calculations. It does **not** replace the mathematical arguments about categorical closure, projection, complex coefficients, nonvanishing for every integer `N>=6`, or the number-theoretic contradictions in the manuscript. Equations (31) and (34) are implications under hypotheses, **not identities to assert for arbitrary parameters**.

## Folder navigation

- `notebooks/` — reader-facing `.mw` files, self-contained 1-D Maple input groups.
- `src/` — equivalent plain-text `.mpl` sources; best suited for GitHub diffs and code review.
- `pseudocode/` — mathematical algorithms with no Maple-specific commands.
- `data/` — structured index linking manuscript results to code.
- `docs/` — mathematical assumptions, provenance of the consolidated code, and release checks.
- `results/` — the author's saved executed worksheets and run summary, a reusable blank run-log template, and the Python assembly checks.

## Additional independent finite-N cross-checks

Optionally install Python with SymPy and run `python tests/python_spot_checks.py`. This separate, shorter implementation reconstructs the matrix and checks selected values N=4,6,7. It is a debugging and comparison aid, not a substitute for the paper's uniform symbolic argument. Actual output from the package assembly is in `results/ASSEMBLY_TESTS.txt`.

## Validation and provenance

The research calculations and earlier worksheets originate from the author. A number of recent worksheets and the present consolidation are AI-assisted, as disclosed in the manuscript. Earlier exploratory worksheets are preserved privately by the author and are not required to run or examine the released computations. This is a description of development history, **not a claim of independent third-party verification**. Both worksheets were executed by the author in Maple 2026.1; their saved output and execution record are retained in `results/`.

Source-level checks performed during preparation: the package contains the stated paths; `.mw` files are well-formed XML; the moment-five determinant and N=4 rank were independently checked using exact symbolic arithmetic; the optional `tests/python_spot_checks.py` reconstructs the moment-six matrix, kernel, rotation/reflection, contraction and squaring data at N=6 and N=7, along with the N=4 rank. Those finite-N checks are supplementary and do not substitute for Maple symbolic execution. Such structural checks do not replace the full symbolic Maple execution. The saved run record identifies the version and the reported results; runtime details were not captured.

## Releasing a stable version

1. Review the saved executed worksheets and [`author execution record`](results/AUTHOR_EXECUTION_2026-10-29.md), including the full symbolic determinant result.
2. Align manuscript equation numbers and repository references with the final mathematical text.
3. Confirm that the public package excludes historical explorations; review reuse permissions and add an explicit software license.
4. Review all instructions from a fresh checkout and confirm that the source files reproduce the stated results.
5. Publish a tagged GitHub release and, if desired, archive that exact version with a persistent identifier.

This package does not itself represent a public GitHub release or archived version.
