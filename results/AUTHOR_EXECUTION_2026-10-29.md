# Saved Maple execution record

Author-reported execution date: **29 October 2026**. This record is based on the two executed Maple worksheets supplied by the author; it is not the result of running Maple in the repository-assembly environment. The XML files preserve the actual displayed outputs and the full executable input groups.

- **Maple version reported by both worksheets:** `Maple 2026.1, X86 64 WINDOWS, Jun 04 2026, Build ID 2018217`.
- **Operating system:** Windows (as indicated by the Maple release string); further machine details not recorded.
- **Clean-session setup:** both source files begin with `restart:`.
- **Full symbolic rank comparison:** enabled in the moment-six worksheet (`RUN_UNIFORM_RANK_CHECK := true`), with a printed success result for equation (16).
- **Optional N=4 check:** enabled (`RUN_N4_CHECK := true`), with a printed result for rank 54.
- **Runtime:** not captured in the saved outputs; not claimed here.
- **Source consistency:** the executable input groups in each saved worksheet match the corresponding clean worksheet's input groups, after normalizing changes in Maple's XML escaping and whitespace. There is an additional encoded display-related input group in each saved worksheet.
- **Error messages:** none found in the saved XML output groups. Both files print their final completion line.
- **Original input files:** `notebooks/MomentLevel5.mw` and `notebooks/MomentLevel6.mw`; the saved files are kept in `results/executed/`.

## Moment five: saved outputs

- Moment five; Maple version: Maple 2026.1, X86 64 WINDOWS, Jun 04 2026, Build ID 2018217
- PASS: constructed 10 x 10 matrix, equation (13).
- PASS equation (14); determinant = -(N-4)*(N^2-3*N+1)^2
- PASS: moment-five N=4 kernel generator; PASS Proposition 7.3: rank 9 and proposed eta in kernel.
- PASS Proposition 7.3: all 4^5 entries of the discrete identity.; Moment-five source reached its final statement without a Maple error.

## Moment six: saved outputs (selected readable statements)

- Moment six; Maple version: Maple 2026.1, X86 64 WINDOWS, Jun 04 2026, Build ID 2018217
- Constructed the paper's 66 x 71 matrix.
- PASS: all 66 equations annihilate V; PASS: five-coordinate normalization; Read coordinates: alpha[67]=(N-2)t1, alpha[68]=t2,; alpha[69]=t3, alpha[70]=(N-2)t4, alpha[71]=t5.
- Computing and comparing the 66 x 66 determinant (can be expensive)...; PASS equation (16): determinant ratio = 1; PASS: rank M(4)=54
- PASS: R^3=I; PASS: actual rotation agrees with coordinate R; PASS: P is idempotent on the kernel
- PASS: reflected basis vectors lie in ker M
- PASS: B is real symmetric; Computed B = transpose(V) G V:
- PASS: DzMap P = 0, so z1,z2 are unchanged by I-P; PASS: q(Ct) depends only on z1,z2 through H; DERIVED d_N, e_N, A_N, B_N (in this order):
- PASS: both displayed formulas follow from the contraction.; PASS: q(Ct)=A_N |z1+z2|^2+B_N |z1-z2|^2 for COMPLEX t.
- PASS: A_N,B_N>0 for every real N>=6.; At N=6, expected A_N=26/9, B_N=34; calculated values:
- NiQjIiNFIiIqIiNN
- PASS: the displayed u,v lie in ker P; PASS: q(lambda*u+mu*v)=9*A_N*|mu|^2+B_N*|2*lambda-mu|^2
- PASS: input parameterization is fixed by R
- Computed all 71 crossing coefficients of theta.
- PASS: all 71 polynomials are homogeneous quadratic (or zero).
- Two actual necessary kernel equations (each must vanish):
- DERIVED necessary equations for theta in Fix(R):
- At N=6 the three derived forms are:
- SQUARING STAGE COMPLETE. No common-zero assertion has been assumed.
- PASS: manuscript equations (28)-(33) verified symbolically.; Moment-six source reached the final statement without a Maple error.
- Quadratic-form computation finished.; Keep the Maple version and outputs with the reproducibility files.

Some mathematical expressions are saved in Maple's encoded worksheet typesetting rather than as ordinary text. Their native rendering is in the two `.mw` files; this summary is intentionally limited to human-readable printed results.

## Interpretation and remaining steps

These outputs document successful execution and agreement with the explicit assertions in the source files. They do not independently establish the mathematical interpretation of every program operation. Before public publication, the author should still review the correspondence between the manuscript's operations and the corresponding routines, confirm the final equation numbers, and choose a software license. No independent third-party run is required as a precondition for making the code available.
