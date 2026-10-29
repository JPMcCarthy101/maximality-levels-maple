"""Optional independent, finite-N spot checks using only Python and SymPy.

They are NOT a replacement for the Maple full symbolic determinant or the
mathematical argument for every N>=6. Run with:
    python tests/python_spot_checks.py
No user data or network access is required.
"""
from pathlib import Path
from itertools import combinations,product
from math import factorial
import ast,re
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
MPL=(ROOT/'src/MomentLevel6.mpl').read_text()

def rg_words(k):
    a=[[]]
    for _ in range(k):a=[w+[n] for w in a for n in range(max(w)+2 if w else 1)]
    return a

def canon(w):
    d={};o=[]
    for x in w:
        if x not in d:d[x]=len(d)
        o.append(d[x])
    return o

def crossing(w):
    return any(w[a]==w[c] and w[b]==w[d] and w[a]!=w[b] for a,b,c,d in combinations(range(len(w)),4))

def gluing(w,groups,caps=()):
    uf=list(range(max(w)+1))
    def root(i):
        while uf[i]!=i:i=uf[i]
        return i
    def join(x,y):uf[root(x)]=root(y)
    for g in list(groups)+list(caps):
        for j in g[1:]:join(w[g[0]-1],w[j-1])
    out=[root(w[g[0]-1]) for g in groups]
    return canon(out),len({root(i) for i in range(len(uf))}-{*out})

def maps6():
    maps=[]
    for aa,bb,cc,dd in combinations(range(1,7),4):
        maps.append(([[aa],[bb],[cc],[dd]],[],'restriction'))
    for x in range(1,7):
        for y in range(1,7):
            if x==y:continue
            cyc=[1+((y+i-1)%6) for i in range(6)]
            cyc=[j for j in cyc if j!=x]
            maps.append(([[cyc[0],cyc[1]]]+[[j] for j in cyc[2:]],[],'delete-merge'))
    for x in range(1,7):
        cyc=[1+((x+i-1)%6) for i in range(6)]
        maps.append(([[j] for j in cyc[2:]],[[cyc[0],cyc[1]]],'cap'))
    edges=[{1,2},{2,3},{3,4},{4,5},{5,6},{6,1}]
    for i,j in combinations(range(6),2):
        if edges[i]&edges[j]:continue
        used=edges[i]|edges[j]
        gs=[sorted(edges[i]),sorted(edges[j])]+[[x] for x in range(1,7) if x not in used]
        gs.sort(key=lambda g:g[0]);maps.append((gs,[],'double-merge'))
    for x in range(1,7):
        cyc=[1+((x+i-1)%6) for i in range(6)]
        maps.append(([cyc[:3]]+[[j] for j in cyc[3:]],[],'triple-merge'))
    return maps

def matrix6(words,maps,n):
    rows=[]
    for g,c,_ in maps:
        r=[]
        for w in words:
            o,loops=gluing(w,g,c)
            r.append(n**loops if o==[0,1,0,1] else 0)
        rows.append(r)
    return sp.Matrix(rows)

def vmatrix(n):
    text=MPL
    match=re.search(r'\nV := Matrix\(\[\s*(\[.*?\])\s*\]\):\s*\n\s*# END GENERATED BASIS',text,re.S)
    if not match:raise AssertionError('Cannot locate stored V')
    # Both brackets needed: match.group(1) consists of a list of row lists, without
    # the outer Matrix-specific opening/closing bracket.
    data='['+match.group(1)+']'
    data=data.replace('^','**')
    return sp.Matrix(eval(data,{'__builtins__':{}},{'N':n}))

def swap_rows_by_word(words,V, transform):
    d={tuple(w):i for i,w in enumerate(words)}
    x=sp.zeros(71,5)
    for i,w in enumerate(words):
        j=d[tuple(canon(transform(w)))]
        x[j,:]=V[i,:]
    return x

def det_mod(A,p):
    n=A.rows; T=[[int(A[i,j])%p for j in range(n)] for i in range(n)]
    sign=1; det=1
    for j in range(n):
        ix=next((i for i in range(j,n) if T[i][j]%p),None)
        if ix is None:return 0
        if ix!=j:T[ix],T[j]=T[j],T[ix];sign=-sign
        pivot=T[j][j];det=det*pivot%p
        inv=pow(pivot,-1,p)
        for i in range(j+1,n):
            k=T[i][j]*inv%p
            if k:
                for col in range(j+1,n):T[i][col]=(T[i][col]-k*T[j][col])%p
    return sign*det%p

def contraction(w,v,n):
    parent=list(range(9))  # 1-based labels 1,...,8
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    def join(x,y):parent[root(x)]=root(y)
    slots=[[1,2,3,4,5,6],[8,7,3,4,5,6]]
    for ww,ss in [(w,slots[0]),(v,slots[1])]:
        for i,j in combinations(range(6),2):
            if ww[i]==ww[j]:join(ss[i],ss[j])
    out=[root(j) for j in [1,2,7,8]]
    if canon(out)!=[0,1,0,1]:return 0
    return n**len({root(j) for j in range(1,9)}-{*out})

def test_quadratic(n,words,V,R):
    G=sp.Matrix(71,71,lambda i,j:contraction(words[i],words[j],n))
    B=V.T*G*V
    assert B==B.T
    P=(sp.eye(5)+R+R**2)/3
    C=sp.eye(5)-P
    Q=C.T*B*C
    dz=sp.Matrix([[1,0,0,-1,0],[0,1,0,0,-1]])
    H=Q[:2,:2]
    assert Q==dz.T*H*dz
    d=H[0,0];e=H[0,1]
    A=(d+e)/2;Bval=(d-e)/2
    expectedA=sp.Rational((n-4)*(2*n*n-9*n+8),18)
    expectedB=sp.Rational((n-4)*(2*n*n-7*n+4),2)
    assert A==expectedA and Bval==expectedB,(n,A,Bval,expectedA,expectedB)
    print(f'PASS independent: contraction and A({n})={A}, B({n})={Bval}')

def square_image(w,v):
    parent=list(range(10))
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    def join(i,j):parent[root(i)]=root(j)
    for ww,slots in [(w,[1,2,3,6,5,4]),(v,[4,5,6,9,8,7])]:
        for i,j in combinations(range(6),2):
            if ww[i]==ww[j]:join(slots[i],slots[j])
    out=[root(i) for i in [1,2,3,9,8,7]]
    loops=len({root(i) for i in range(1,10)}-{*out})
    return canon(out),loops

def test_squaring(n,words,V,M):
    index={tuple(w):i for i,w in enumerate(words)}
    pairs=[]
    for i,w in enumerate(words):
        for j,ww in enumerate(words):
            out,loops=square_image(w,ww)
            if crossing(out):pairs.append((i,j,index[tuple(out)],n**loops))
    delta=n**3-7*n*n+13*n-4
    samples=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
    for a,b,c in samples:
        alpha=V*sp.Matrix([b,c,a,b,c])
        beta=[0]*71
        for i,j,row,weight in pairs:
            beta[row]+=weight*int(alpha[i])*int(alpha[j])
        cap=sum(int(M[47,j])*beta[j] for j in range(71))
        merge=sum(int(M[58,j])*beta[j] for j in range(71))
        g=sp.Rational((3-n)*cap+(n-2)*merge,delta)
        h=sp.Rational(-(n*n-4*n+2)*cap+n*merge,delta)
        k=beta[66]-beta[69]
        ge=a*a-2*(n-2)**2*a*b+4*a*c+(n-2)**2*(n+2)*b*b-4*(n-2)*(n-3)*b*c+(n*n-8*n+17)*c*c
        he=(2*n-5)*a*a-2*(n-2)*(n*n-4*n+6)*a*b+2*(n+1)*a*c+(n-2)**2*(5*n-4)*b*b-4*(n-2)*(2*n-5)*b*c+(n*n-8*n+19)*c*c
        ke=2*a*a-2*(n-2)*(n-4)*a*b-2*a*c+(n-2)**2*(n*n-8*n+10)*b*b+4*(n-2)**2*b*c-(n-4)*(2*n-5)*c*c
        assert (g,h,k)==(ge,he,ke),(n,(a,b,c),(g,h,k),(ge,he,ke))
    print(f'PASS independent: squaring and g,h,k at N={n} on six quadratic test inputs')

def test_moment_five():
    cr5=list(filter(crossing,rg_words(5)))
    assert len(cr5)==10
    maps5=[]
    for x in range(1,6):maps5.append(([[j] for j in range(1,6) if j!=x],[]))
    for x in range(1,5):
        gs=[[x,x+1]]+[[j] for j in range(1,6) if j not in [x,x+1]]
        gs.sort(key=lambda g:g[0]); maps5.append((gs,[]))
    maps5.append(([[1,5],[2],[3],[4]],[]))
    N=sp.Symbol('N')
    M5=sp.Matrix([[N**loops if q==[0,1,0,1] else 0
                    for w in cr5 for q,loops in [gluing(w,*f)]] for f in maps5])
    assert sp.simplify(M5.det()+(N-4)*(N*N-3*N+1)**2)==0
    m4=M5.subs(N,4)
    assert m4.rank()==9
    eta=sp.Matrix([1 if len(set(w))==3 else -2 for w in cr5])
    assert m4*eta==sp.zeros(10,1)
    parts=rg_words(5)
    def mu(w):
        x=(-1)**len(set(w))
        for b in set(w):x*=factorial(w.count(b)-1)
        return x
    def part_indicator(w,inds):
        return int(all(w[i]!=w[j] or inds[i]==inds[j]
                       for i,j in combinations(range(5),2)))
    for inds in product(range(4),repeat=5):
        total=sum(mu(w)*part_indicator(w,inds) for w in parts if w!=[0,1,2,3,4])
        assert total==1,inds
    print('PASS independent: moment five determinant, rank 9, eta, 4^5 discrete-vector identity')

if __name__=='__main__':
    test_moment_five()
    words=list(filter(crossing,rg_words(6)));f=maps6()
    assert len(words)==71 and len(f)==66
    saved=ast.literal_eval('['+re.search(r'SavedWords := \[(.*?)\]:\s*V :=',MPL,re.S).group(1)+']')
    assert words==saved
    R=sp.Matrix([[0,0,0,1,0],[0,0,0,0,1],[0,-1,1,0,1],[1,-1,0,0,1],[1,0,0,-1,1]])
    for n in [4,6,7]:
        M=matrix6(words,f,n)
        if n==4:
            assert M.rank()==54;print('PASS independent: M(4) rank 54')
            continue
        V=vmatrix(n)
        assert M*V==sp.zeros(66,5)
        assert V[66:71,:]==sp.diag(n-2,1,1,n-2,1)
        rotated=swap_rows_by_word(words,V,lambda w:[w[5]]+w[:5])
        assert rotated==V*R
        reflected=swap_rows_by_word(words,V,lambda w:w[::-1])
        assert M*reflected==sp.zeros(66,5)
        p=10007
        d=det_mod(M[:66,:66],p)
        expected=((n-4)**12*(n-2)*(n*n-3*n+1)**23)%p
        assert d==expected or d==(-expected)%p,(n,d,expected)
        print(f'PASS independent: M({n})V({n})=0, symmetries, determinant mod {p}')
        test_quadratic(n,words,V,R)
        test_squaring(n,words,V,M)
    print('All finite-N independent spot checks passed. These do not prove a uniform symbolic claim.')
