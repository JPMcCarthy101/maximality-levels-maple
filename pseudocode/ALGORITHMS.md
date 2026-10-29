# Algorithms underlying the Maple calculations

This is descriptive pseudocode, not an additional implementation. The data structures and ordering agree with the Maple source and its README. It is intended to make an implementation in another computer algebra system possible.

## 1. Enumerate partitions in restricted-growth-word order

```
PARTITIONS(k):
    words = [[]]
    repeat k times:
        next = []
        for word in words, preserving order:
            largest = -1 if word is empty else max(word)
            for label = 0,1,...,largest+1:
                append word+[label] to next
        words = next
    return words

CROSSING(word):
    for 1 <= a < b < c < d <= len(word):
        if word[a]==word[c] and word[b]==word[d] and word[a]!=word[b]:
            return TRUE
    return FALSE

CROSSING_PARTITIONS(k):
    return [w in PARTITIONS(k) for which CROSSING(w)]
```

This gives ten crossing partitions on five points and 71 on six points. Lexicographic order of the growing words is part of the specification, not arbitrary presentation.

## 2. Gluing an input partition into a specified operation

```
LOWER(word, ordered_output_groups, cap_groups):
    make one disjoint-set node per block of word
    for each group in ordered_output_groups and cap_groups:
        union all original block labels corresponding to positions in group
    output_labels = [root(block(word, first(group))) for group in ordered_output_groups]
    output_word = canonicalize(output_labels) in first-occurrence order
    all_components = set(roots of every original input block)
    output_components = set(output_labels)
    closed = count(all_components - output_components)
    return (output_word, closed)
```

A row of the moment matrix has entry `N^closed` if the output word is the basic crossing `[0,1,0,1]`, otherwise zero. The coefficient is exactly the power from deleted closed blocks. This is why a plain rank computation is not enough: the gluing procedure itself must reflect the partition operation claimed in the paper.

## 3. Construct the moment-five matrix

```
CR5 = CROSSING_PARTITIONS(5)
MAPS5 = []
for x=1,...,5:
    append delete position x, keeping other four in original order
for x=1,...,4:
    append merge positions {x,x+1}, keeping other three separately
append merge cyclic pair {1,5}, keeping positions 2,3,4 separately
for i in 1..10:
    for j in 1..10:
        output, loops = LOWER(CR5[j], MAPS5[i])
        M5[i,j] = N^loops if output==[0,1,0,1] else 0
```

Compute the exact determinant over rational functions in `N`. At `N=4`, compute rank and test the candidate null vector. The candidate has coefficient +1 on each crossing partition with three blocks and -2 on each crossing partition with two blocks.

The `N=4` discrete-vector identity can be tested without constructing an ambient `4^5` by `52` matrix: enumerate every five-index tuple from `{1,2,3,4}`; for each partition `p` compute its indicator `xi_p(tuple)`, and sum `(-1)^|p| product_{B in p} (|B|-1)!` over all partitions except the discrete one. Every total must equal 1.

## 4. Construct the moment-six matrix

```
CR6 = CROSSING_PARTITIONS(6)
MAPS6 = concatenate in this exact order:
    15 restrictions to sorted four-element subsets of [6]
    30 singleton deletion/adjacent merging maps, outer x=1..6, inner y=1..6, x!=y
    six cyclic adjacent pair caps
    nine disjoint pairs of cyclic adjacent merges, ordered by edge numbers
    six cyclic triple merges
for map_i in MAPS6:
    for partition_j in CR6:
        output, loops = LOWER(partition_j, map_i)
        M66[i,j] = N^loops if output==[0,1,0,1] else 0
A66 = first 66 columns of M66
```

The source stores `V`, a polynomial `71x5` matrix with rows in `CR6` order. Test `M66*V=0`, compare the final five rows to `diag(N-2,1,1,N-2,1)`, and calculate the rank-related determinant in the paper. Unlike a finite parameter sweep, the symbolic factorisation makes the uniform assertion for integer `N>=6` accessible.

## 5. Rotation and reflection on crossing words

```
ROTATE_LAST_TO_FIRST(w) = canonicalize([w[6],w[1],...,w[5]])
REFLECT(w) = canonicalize([w[6],...,w[1]])
```

Permute coefficient rows accordingly. For the stored basis `V`, test `ROTATE(V)=V*R` and `M66*REFLECT(V)=0`. Check `R^3=I`; construct `P=(I+R+R^2)/3` and verify `P^2=P`. Compare the stated fixed-space parametrisation.

## 6. Contraction giving the quadratic form

```
CONTRACT(w,v):
    label the first input six-tuple by [1,2,3,4,5,6]
    label the reflected second input six-tuple by [8,7,3,4,5,6]
    glue blocks according to w and v, using union-find
    read the four output slots [1,2,7,8]
    if their RGS is the basic crossing:
        return N^(number of components disjoint from outputs)
    return 0
G[i,j] = CONTRACT(CR6[i],CR6[j])
B = transpose(V)*G*V
```

For a coefficient column `t`, calculate the matrix form restricted to `C*t`, where `C=I-P`. Use `z1=t1-t4`, `z2=t2-t5`, extract the symmetric `2x2` form, and derive `A_N` and `B_N` by equating diagonal/off-diagonal coefficients. Test the complex Hermitian identity by treating `z1,z2` and their formal conjugates as independent indeterminates. Positivity for `N>=6` is an ordinary argument about the derived polynomial factors.

## 7. Rotate–square–rotate

```
INPUT_FIXED(a,b,c):
    alpha[i] = a*V[i,3] + b*(V[i,1]+V[i,4]) + c*(V[i,2]+V[i,5])

SQUARE_GLUE(w,v):
    use the first six input slots [1,2,3,6,5,4]
    use the second six input slots [4,5,6,9,8,7]
    glue all equal-block labels of w and v via union-find
    read six output slots [1,2,3,9,8,7]
    return canonical output word and number of closed components

beta = vector(71, all zero)
for each ordered pair (i,j) in [1..71]x[1..71]:
    q,loops = SQUARE_GLUE(CR6[i],CR6[j])
    if q is crossing:
        r = the row index of q in CR6
        beta[r] += N^loops * alpha[i]*alpha[j]
```

Compute `M66*beta`. The two specific rows in the paper yield `g_N` and `h_N` after an invertible two-variable transformation. The difference `beta[67]-beta[70]` yields `k_N` under the stated normalization. The code derives these first, **then** compares them to the printed formulas.

## 8. Final algebraic reductions

Starting with the *derived* polynomials `g_N,h_N,k_N`, expand and compare the product formula in equation (28). Under the first factor, substitute the corresponding linear expression for `a` and reproduce the formulas in equation (29); eliminate the `b^2` term and compare the remaining linear relation. Under the other factor, substitute `b=(v+c)/(N-2)` and `a=-2v+(N-4)c`, reproduce equation (32), and compare the elimination identity (33). The contradictory **equalities** (31) and (34) arise only under assumptions and are not asserted as polynomial identities.
