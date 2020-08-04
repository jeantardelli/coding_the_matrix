from math import sqrt
from The_Matrix_problems import dictlist_helper
from mat import Mat
from vec import Vec

# Task 10.9.1:
def forward_no_normalization(v):
    '''
    input:
        a list representing a vector in Rn where n is some power of two.
    output:
        a dictionary giving the representation of the input vector in terms of the
        unnormalized Haar wavelet basis. The key for the coefficient of wj i should
        be the tuple (j, i)

    >>> forward_no_normalization([1,2,3,4]) == {(2, 0): -1, (1, 0): -2.0, (0, 0): 2.5, (2, 1): -1}
    True
    >>> v=[4,5,3,7,4,5,2,3,9,7,3,5,0,0,0,0]
    >>> forward_no_normalization(v) == {(8,3): -1, (0,0): 3.5625, (8,2): -1, (8,1): -4, (4,1): 2.0, (4,3): 0.0, (8,0): -1, (2,1): 6.0, (2,0): 1.25, (8,7): 0, (4,2): 4.0, (8,6): 0, (1,0): 1.125, (4,0): -0.5, (8,5): -2, (8,4): 2}
    True
    '''
    D = {}
    while len(v) > 1:
        k = len(v)
        # v is a k-element list
        vnew = [(v[2*i]+v[2*i+1])/2 for i in range(k//2)]
        # vnew is a k//2-element list
        w = [v[2*i]-v[2*i+1] for i in range(k//2)]
        # w is a list of coefficients
        D.update({(k//2,i): w[i] for i in range(k//2)})
        v = vnew
    # v is a 1-element list
    D[(0,0)] = v[0] # store the last coefficient
    return D

# Task 10.9.2:
def normalize_coefficients(n, D):
    '''
    Given the dimension n of the original space and a dictionary D of the form returned by
    forward_no_normalization(v), returns the corresponding dictionary with the coefficients
    normalized.

    >>> normalize_coefficients(4, {(2,0):1, (2,1):1, (1,0):1, (0,0):1}) == {(2, 0): 0.7071067811865476, (1, 0): 1.0, (0, 0): 2.0, (2, 1): 0.7071067811865476}
    True
    >>> normalize_coefficients(4, forward_no_normalization([1,2,3,4])) == {(2, 0): -0.7071067811865476, (1, 0): -2.0, (0, 0): 5.0, (2, 1): -0.7071067811865476}
    True
    '''
    return {k: v * sqrt(n/(4*k[0])) if k[0] != 0 else v * sqrt(n) for k,v in D.items()}

# Task 10.9.3:
def forward(v):
    '''
    Find the representation with respect to  the normalized Haar wavelet basis. This 
    procedure should simply combine forward_no_normalization with normalize_coefficients.

    >>> forward([1,2,3,4]) == {(2, 0): -sqrt(1/2), (2,1): -sqrt(1/2), (1, 0): -2, (0, 0): 5}
    True
    '''
    return normalize_coefficients(len(v), forward_no_normalization(v))

#Task 10.9.4:
def suppress(D, threshold):
    '''
    Given a dictionary D giving the representation of a vector with respect to the normalized basis,
    returns a dictionary of the same form but where every value whose absolute value is less than threshold is
    replaced with zero. You should be able to use a simple comprehension for this.

    >>> suppress(forward([1,2,3,4]), 1) == {(2, 0): 0, (1, 0): -2.0, (0, 0): 5.0, (2, 1): 0}
    True
    '''
    return {k:v if abs(v) > threshold else 0 for k,v in D.items()}

# Task 10.9.5:
def sparsity(D):
    '''
    Given such a dictionary, returns the percentage of its values that are nonzero. The
    smaller this value, the better the compression achieved.
    
    >>> D = forward([1,2,3,4])
    >>> sparsity(D)
    1.0
    >>> sparsity(suppress(D, 1))
    0.5
    '''
    return sum([1 for v in D.values() if v !=0]) / len(D)

# Task 10.9.6:
def unnormalize_coefficients(n, D):
    '''
    Corresponds to the functional inverse of normalize_coefficients(n, D).

    >>> unnormalize_coefficients(4, normalize_coefficients(4, forward_no_normalization([1,2,3,4]))) == forward_no_normalization([1,2,3,4])
    True
    '''
    return {k: v / sqrt(n/(4*k[0])) if k[0] != 0 else v / sqrt(n) for k,v in D.items()}

# Task 10.9.7:
def backward_no_normalization(D):
    '''
    Given a dictionary of unnormalized wavelet coefficients, produces the corresponding list.
    It should be the inverse of foward_no_normalization(v).
    
    >>> backward_no_normalization(forward_no_normalization([1,2,3,4])) == [1.0,2.0,3.0,4.0]
    True
    '''
    n = len(D)
    v = [D[(0,0)]]
    while len(v) < n:
        k = 2 * len(v)
        v = [b for i in range(k//2) for b in [(2*v[i]+D[(len(v),i)])/2, (2*v[i]-D[(len(v),i)])/2]]
    return v

# Task 10.9.8:
def backward(D):
    '''
    Computes the inverse wavelet transform. This involves just combining unnormalize 
    coefficients(n, D) and backward no normalization(D).
    
    >>> backward(forward([1,2,3,4])) == [1.0, 2.0, 3.0, 4.0]
    True
    '''
    return backward_no_normalization(unnormalize_coefficients(len(D), D))

# Task 10.9.9:
def forward2d(listlist):
    '''
    Transforms the listlist representation of an image into the dictdict representation of the wavelet coefficients.
    The input listlist is an m-element list of n-element lists. Each inner list is a row of pixel intensities. 
    We assume for simplicity that m and n are powers of two.
    '''
    D_list = [forward(v) for v in listlist]
    L_list = {k: dictlist_helper(D_list, k) for k in D_list[0].keys()}
    return {k: forward(v) for k,v in L_list.items()}

# Task 10.9.10:
def suppress2d(D_dict, threshold):
    '''
    A two-dimensional version of suppress(D,threshold) that suppresses values with absolute
    value less than threshold in a dictionary of dictionaries such as is returned by forward2d(vlist).
    '''
    return {k: suppress(v, threshold) for k,v in D_dict.items()}

# Task 10.9.11:
def sparsity2d(D_dict):
    '''
    A two dimensional version of sparsity(D).
    '''
    return sum([sparsity(D_dict[d]) for d in D_dict]) / len(D_dict)
    

# Task 10.9.12:
def listdict2dict(L_dict, i):
    '''
    input: a dictionary L_dict of lists, all the same length, and an index i into such a list
    output: a dictionary with the same keys as L dict, in which key k maps to element i of L dict[i]
    '''
    return {k: v[i] for k,v in L_dict.items()}

# Task 10.9.13:
def listdict2dictlist(listdict):
    '''
    Converts from a listdict representation (a dictionary of lists) to a dictlist representation (a list of dictionaries).
    '''
    return  [listdict2dict(listdict, i) for i in range(len(list(listdict.values())[0]))]

# Task 10.9.14:
def backward2d(dictdict):
    '''
    The functional inverse of forward2d(vlist). Test it to make sure it is really the inverse.
    
    >>> backward2d(forward2d([[1,2,3,4]])) == [[1.0, 2.0, 3.0, 4.0]]
    True
    '''
    L_dict = {k: backward(v) for k,v in dictdict.items()}
    D_list = listdict2dictlist(L_dict)
    return [backward(l) for l in D_list]

# Task 10.9.16:
def image_round(image):
    '''
    input: a grayscale image, represented as a list of lists of floats
    output: the corresponding grayscale image, represented as a list of lists of integers,
    obtained by rounding the floats in the input image and taking their absolute values,
    and replacing numbers greater than 255 with 255.
    '''
    return [[round(v) if v < 255 else 255 for v in l] for l in image]

# Problem 10.11.1:
def orthogonal_vec2rep(Q,b):
    '''
    input: An orthogonal matrix Q, and a vector b whose label set equals the column-label set of Q
    output: the coordinate representation of b in terms of the rows of Q.
    >>> Q = Mat(({0, 1, 2}, {0, 1, 2}), {(0, 0): 0.7071067811865475, (0, 1): 0.7071067811865475, (0, 2): 0, (1, 0): 0.5773502691896258, (1, 1): -0.5773502691896258, (1, 2): 0.5773502691896258, (2, 0): -0.4082482904638631, (2, 1): 0.4082482904638631, (2, 2): 0.8164965809277261})
    >>> b = Vec({0,1,2}, {0:10, 1:20, 2:30})
    >>> Q * b == Vec({0, 1, 2},{0: 21.213203435596423, 1: 11.547005383792516, 2: 28.577380332470415})
    True
    '''
    return Q * b

# Problem 10.11.2:
def orthogonal_change_of_basis(A, B, a):
    '''
    input:
    – two orthogonal matrices A and B, such that the row-label set of A equals its columnlabel set 
      which equals the row and column-label sets of B as well.
    – the coordinate representation a of a vector v in terms of the rows of A.
    output: the coordinate representation of v in terms of the columns of B.
    >>> A = Mat(({0, 1, 2}, {0, 1, 2}), {(0, 0): 0.7071067811865475, (0, 1): 0.7071067811865475, (0, 2): 0, (1, 0): 0.5773502691896258, (1, 1): -0.5773502691896258, (1, 2): 0.5773502691896258, (2, 0): -0.4082482904638631, (2, 1): 0.4082482904638631, (2, 2): 0.8164965809277261})
    >>> B = A
    >>> a = Vec({0, 1, 2},{0: 1.4142135623730951, 1: 0.5773502691896258, 2: 0.8164965809277261})
    >>> orthogonal_change_of_basis(A, B, a) == Vec({0, 1, 2},{0: 0.8762087599123101, 1: 0.5380048024607849, 2: 1.3938468501173522})
    True
    '''
    return a * A * B

# Problem 10.11.3:
def orthonormal_projection_orthogonal(W, b):
    '''
    input: a matrix W whose rows are orthonormal, and a vector b whose label set is the column-label set of W.
    output: output: the projection of b orthogonal to the row space of W.
    >>> W = Mat(({0, 1}, {0, 1, 2}), {(0, 0): 0.7071067811865475, (0, 1): 0.7071067811865475, (0, 2): 0, (1, 0): 0.5773502691896258, (1, 1): -0.5773502691896258, (1, 2): 0.5773502691896258})
    >>> b = Vec({0, 1, 2},{0: 10, 1: 20, 2: 30})
    >>> orthonormal_projection_orthogonal(W, b) == Vec({0, 1, 2},{0: -11.666666666666664, 1: 11.666666666666671, 2: 23.333333333333332})
    True
    '''
    return b - W * b * W