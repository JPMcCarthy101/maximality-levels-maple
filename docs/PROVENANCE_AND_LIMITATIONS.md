# Computational provenance and scope

This repository contains the computational material accompanying J. P. McCarthy's *Maximality Levels of the Classical Permutation Group in the Quantum Permutation Group*.

The author's original Maple investigations provided the underlying computations. Some earlier development involved Claude; the moment-six completion and the consolidation into the current reader-facing files involved ChatGPT. The paper contains the fuller declaration of AI assistance.

The two self-contained worksheets in `notebooks/` and their matching plain-text Maple programs in `src/` provide the reproducible calculations. Historical exploratory worksheets have been retained privately and are **not required** by the public code.

The author executed both worksheets in Maple 2026.1 (64-bit Windows) on 29 October 2026. The saved outputs and observed results are available in `results/executed/` and `results/AUTHOR_EXECUTION_2026-10-29.md`. Maple was not available in the separate code-assembly environment, where selected independent finite-parameter checks were performed in Python/SymPy. Execution durations were not recorded.

The source calculations derive matrix entries from partition gluing, and check the symbolic expressions stated in the paper. The mathematical justification for the Tannaka–Krein operations and for the deductions from the computed identities remains part of the manuscript, not the software. The optional Python finite-parameter checks are supplementary, not a replacement for the author's exact symbolic Maple execution.

The source code and accompanying documentation are provided for research inspection and reproduction. A separate explicit reuse licence has not yet been selected.
