# version code 0caa61797a35+
# Please fill out this stencil and submit using the provided submission script.

from mat import Mat
from vec import Vec
from vecutil import list2vec
from matutil import mat2rowdict, listlist2mat
from math import sqrt



## 1: (Problem 11.8.1) Procedure for computing squared Frobenius norm
def squared_Frob(A):
    '''
    Computes the square of the frobenius norm of A.

    Example:
    >>> squared_Frob(Mat(({1, 2}, {1, 2, 3, 4}), {(1, 1): 1, (1, 2): 2, (1, 3): 3, (1, 4): 4, (2, 1): -4, (2, 2): 2, (2, 3): -1}))
    51
    '''
    return sum([v*v for k,v in mat2rowdict(A).items()])



## 2: (Problem 11.8.2) Frobenius_norm_counterexample
#Give a numerical counterxample.
A = listlist2mat([[3,2], [4,5], [-1,2]])
Q = listlist2mat([[1,0], [1,2]])



## 3: (Problem 11.8.3) Multiplying a vector by a matrix in terms of the SVD of the matrix
# Use lists instead of Vecs
# Part 1
vT_x_1 = [2, 1]
Sigma_vT_x_1 = [4, 1]
U_Sigma_vT_x_1 = [1, 4, 0]

# Part 2
vT_x_2 = [0, 2]
Sigma_vT_x_2 = [0, 2]
U_Sigma_vT_x_2 = [2, 0, 0]



## 4: (Problem 11.8.4) The SVD of a small simple matrix
# A.D = ({'r1','r2'},{'c1','c2'})
# Row and column labels of SA should be {0,1, ...}
UA = Mat(({'r1', 'r2'}, {0, 1}), {('r1', 0): 1, ('r2', 1): -1})
SA = Mat(({0, 1}, {0, 1}), {(0, 0): 3, (1, 1): 1})
VA = Mat(({'c1', 'c2'}, {0, 1}), {('c1', 0): 1, ('c2', 1): 1})

# B.D = ({'r1','r2'},{'c1','c2'})
# Row- and column-labels of SB should be {0,1, ...}
UB = Mat(({'r1', 'r2'}, {0, 1}), {('r1', 1): 1, ('r2', 0): 1})
SB = Mat(({0, 1}, {0, 1}), {(0, 0): 4, (1, 1): 3})
VB = Mat(({'c1', 'c2'}, {0, 1}), {('c1', 1): 1, ('c2', 0): 1})

# C.D = ({'r1','r2','r3'},{'c1','c2'})
# Row- and column-labels of SC should be {0,1, ...}
UC = Mat(({'r1', 'r2', 'r3'}, {0}), {('r1', 0): 1})
SC = Mat(({0}, {0}), {(0, 0): 4})
VC = Mat(({'c1', 'c2'}, {0}), {('c2', 0): 1})



## 5: (Problem 11.8.5) Closest rank-$k$ matrix
# In both parts, your matrices must use 0, 1, 2, ... , n as the indices.

# Part 1
G1 = listlist2mat([[0, -sqrt(2)], [2,0], [0, -sqrt(2)], [1, 0]])
H1 = listlist2mat([[0,1,0], [-sqrt(.5), 0, -sqrt(.5)]])

# Part 2
G2 = listlist2mat([[1,0], [1,0], [0,0], [0,-1]])
H2 = listlist2mat([[0,0,1], [0,-1,0]])



## 6: (Problem 11.8.7) Writing SVD_solve
def SVD_solve(U, Sigma, V, b):
    '''
    Input:
      - U: orthogonal matrix
      - Sigma: diagonal matrix with non-negative elements
      - V: orthogonal matrix
      - b: vector
    Output:
      - x: a vector such that U*Sigma*V.tranpose()*x = b
      - 'FAIL': if U*Sigma*V.transpose() has no inverse

    Example:
      >>> U = Mat(({0, 1, 2}, {0, 1, 2}), {(0, 1): -0.44072022797538285, (1, 2): -0.4580160039142736, (0, 0): -0.15323906505773385, (2, 0): -0.8716906349733183, (1, 0): -0.4654817137547351, (2, 2): 0.08909472804179724, (0, 2): 0.8844679019577585, (2, 1): 0.4818895789856551, (1, 1): -0.7573295942443791})
      >>> Sigma = Mat(({0, 1, 2}, {0, 1, 2}), {(0, 0): 39.37043356298421, (1, 1): 2.2839722460456144, (2, 2): 0.867428292102265})
      >>> V = Mat(({0, 1, 2}, {0, 1, 2}), {(0, 1): 0.8797721734901444, (1, 2): -0.7977287698474189, (0, 0): -0.46693900110435005, (2, 0): -0.682398941975231, (1, 0): -0.5624052393414894, (2, 2): 0.5963722979461945, (0, 2): 0.08926865071288784, (2, 1): -0.42269583181462916, (1, 1): -0.21755265229127096})
      >>> b = Vec({0,1,2}, {0:0, 1:1, 2:2})
      >>> x = SVD_solve(U, Sigma, V, b)
      >>> res = b -U*(Sigma*(V.transpose()*x))
      >>> res*res < 1e-20
      True
    '''
    Sigma_inv = listlist2mat([[1/Sigma[r,c] if Sigma[r,c] != 0 else 0 for r in Sigma.D[0]] for c in Sigma.D[1]])
    try:
        I = (U * (Sigma * (V.transpose()))) * (V * (Sigma_inv * (U.transpose())))
    except:
        return 'FAIL'
    return V * (Sigma_inv * (U.transpose() * b))