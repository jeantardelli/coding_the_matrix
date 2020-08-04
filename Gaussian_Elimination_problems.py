# version code c2eb1c41017f+
# Please fill out this stencil and submit using the provided submission script.

from matutil import *
from GF2 import one
from vecutil import *



## 1: (Problem 7.9.2) Recognizing Echelon Form
# Write each matrix as a list of row lists

echelon_form_1 = [[1,2,0,2,0],
                  [0,1,0,3,4],
                  [0,0,2,3,4],
                  [0,0,0,2,0],
                  [0,0,0,0,4]]

echelon_form_2 = [[0,4,3,4,4],
                  [0,0,4,2,0],
                  [0,0,0,0,1],
                  [0,0,0,0,0]]

echelon_form_3 = [[1,0,0,1],
                  [0,0,0,1],
                  [0,0,0,0]]

echelon_form_4 = [[1,0,0,0],
                  [0,1,0,0],
                  [0,0,0,0],
                  [0,0,0,0]]



## 2: (Problem 7.9.3) Is it echelon?
def is_echelon(A):
    '''
    Input:
        - A: a list of row lists
    Output:
        - True if A is in echelon form
        - False otherwise
    Examples:
        >>> is_echelon([[1,1,1],[0,1,1],[0,0,1]])
        True
        >>> is_echelon([[0,1,1],[0,1,0],[0,0,1]])
        False
        >>> is_echelon([[1,1]])
        True
        >>> is_echelon([[1]])
        True
        >>> is_echelon([[1],[1]])
        False
        >>> is_echelon([[0]])
        True
        >>> is_echelon([[0],[1]])
        False
        >>> is_echelon([[1,1,1],[0,1,0],[0,0,0],[0,0,0]])
        True
        >>> is_echelon([[1,1,1],[0,1,0],[0,0,0],[0,0,0], [0,0,0]])
        True
        >>> is_echelon([[1,1,1],[0,0,0],[0,0,1]])
        False
    '''
    # if # of rows equals 1 is in echelon
    if len(A) <= 1: 
        return True
    # if there is a zero row in the middle is not in echelon
    zerovecs = [all([i==0 for i in v]) for v in A]
    if not zerovecs[0] and not zerovecs[-1] and all(zerovecs[1:-1]):
        return False
    # removes irrelevant zero rows
    if not zerovecs[0]:
        A = [A[i] for i in range(len(A)) if not zerovecs[i]]
    
    nonzeros = []
    rowsleft = set(range(len(A)))
    for row in range(len(A)):
        for col in range(len(A[0])):
            if row in rowsleft:
                if A[row][col] != 0:
                    nonzeros.append(col)
                    rowsleft.remove(row)
    
    return len(set(nonzeros)) == len(A) and nonzeros == sorted(nonzeros)

## 3: (Problem 7.9.4) Solving with Echelon Form: No Zero Rows
# Give each answer as a list

echelon_form_vec_a = [1,0,3,0]
echelon_form_vec_b = [-3,0,-2,3]
echelon_form_vec_c = [-5,0,2,0,2]



## 4: (Problem 7.9.5) Solving with Echelon Form
# If a solution exists, give it as a list vector.
# If no solution exists, provide "None" (without the quotes).

solving_with_echelon_form_a = None
solving_with_echelon_form_b = [21,0,2,0,0]



## 5: (Problem 7.9.6) Echelon Solver
def echelon_solve(rowlist, label_list, b):
    '''
    Input:
        - rowlist: a list of Vecs
        - label_list: a list of labels establishing an order on the domain of
                      Vecs in rowlist
        - b: a vector (represented as a list)
    Output:
        - Vec x such that rowlist * x is b
    >>> D = {'A','B','C','D','E'}
    >>> U_rows = [Vec(D, {'A':one, 'E':one}), Vec(D, {'B':one, 'E':one}), Vec(D,{'C':one})]
    >>> b_list = [one,0,one]
    >>> cols = ['A', 'B', 'C', 'D', 'E']
    >>> echelon_solve(U_rows, cols, b_list) == Vec({'B', 'C', 'A', 'D', 'E'},{'B': 0, 'C': one, 'A': one})
    True
    
    '''
    D = rowlist[0].D
    x = zero_vec(D)
    for j in reversed(range(len(rowlist))):
        row = rowlist[j]
        nonzero_cols = [i for i in label_list if row[i] != 0]
        if nonzero_cols != []:
            col = nonzero_cols[0]
            x[col] = (b[j] - x*row)/row[col]
    return x


D = {'A','B','C','D'}
## 6: (Problem 7.9.7) Solving General Matrices via Echelon
row_list = [Vec(D, {'A':one, 'B':one, 'D':one}), Vec(D, {'B':one}), Vec(D, {'C':one}), Vec(D, {'D':one})]  # Provide as a list of Vec instances
label_list = ['A', 'B', 'C', 'D']  # Provide as a list
b = [one, one, 0, 0]          # Provide as a list of GF(2) values



## 7: (Problem 7.9.8) Nullspace A
null_space_rows_a = {3, 4} # Put the row numbers of M from the PDF



## 8: (Problem 7.9.9) Nullspace B
null_space_rows_b = {4} # Put the row numbers of M from the PDF

