# Launch from the repository root. Each file begins with restart:
# This runs the complete moment-five and moment-six calculations in sequence.
# The moment-six exact 66x66 determinant is enabled in MomentLevel6.mpl.
read "src/MomentLevel5.mpl":
read "src/MomentLevel6.mpl":
printf("Both complete calculation scripts returned. Review all PASS lines and warnings.\n"):
