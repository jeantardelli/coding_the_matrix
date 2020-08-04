# version code c2eb1c41017f+
# Please fill out this stencil and submit using the provided submission script.

from vec import Vec
from mat import Mat

import svd
import matutil

from eigenfaces import load_images

## Task 1

D = {(x,y) for x in range(166) for y in range(189)}
# see documentation of eigenfaces.load_images
face_images = {i: Vec(D, {(x,y): face[y][x] for x in range(166) for y in range(189)}) for i,face in load_images('faces/').items()} # dict of Vecs

## Task 2

centroid = sum(face_images.values()) / len(face_images)
centered_face_images = {i: face - centroid for i,face in face_images.items()}

## Task 3

A = matutil.rowdict2mat(centered_face_images) # centered image vectors
U, S, V = svd.factor(A)

orthonormal_basis = matutil.rowdict2mat({k:v for k,v in matutil.mat2coldict(V).items() if k <10}) # 10 rows

## Task 4

#This is the "transpose" of what was specified in the text.
#Follow the spec given here.
def projected_representation(M, x):
    '''
    Input:
        - M: a matrix with orthonormal rows with M.D[1] == x.D
        - x: a vector
    Output:
        - the projection of x onto the row-space of M
    Examples:
        >>> from vecutil import list2vec
        >>> from matutil import listlist2mat
        >>> x = list2vec([1, 2, 3])
        >>> M = listlist2mat([[1, 0, 0], [0, 1, 0]])
        >>> projected_representation(M, x)
        Vec({0, 1},{0: 1, 1: 2})
        >>> M = listlist2mat([[3/5, 1/5, 1/5], [0, 2/3, 1/3]])
        >>> projected_representation(M, x)
        Vec({0, 1},{0: 1.6, 1: 2.333333333333333})
    '''
    return M * x

## Task 5

#This is the "transpose" of what was specified in the text.
#Follow the spec given here.
def projection_length_squared(M, x):
    '''
    Input:
        - M: matrix with orthonormal rows with M.D[1] == x.D
        - x: vector
    Output:
        - the square of the norm of the projection of x into the
          row-space of M
    Example:
        >>> from vecutil import list2vec
        >>> from matutil import listlist2mat
        >>> x = list2vec([1, 2, 3])
        >>> M = listlist2mat([[1, 0, 0], [0, 1, 0]])
        >>> projection_length_squared(M, x)
        5
        >>> M = listlist2mat([[3/5, 1/5, 1/5], [0, 2/3, 1/3]])
        >>> projection_length_squared(M, x)
        5.644424691358024
    '''
    return (projected_representation(M,x)*M) * (projected_representation(M,x)*M)

## Task 6

#This is the "transpose" of what was specified in the text.
#Follow the spec given here.
def distance_squared(M, x):
    '''
    Input:
        - M: matrix with orthonormal rows with M.D[1] == x.D
        - x: vector
    Output:
        - the square of the distance from x to the row-space of M
    Example:
        >>> from vecutil import list2vec
        >>> from matutil import listlist2mat
        >>> x = list2vec([1, 2, 3])
        >>> M = listlist2mat([[1, 0, 0], [0, 1, 0]])
        >>> distance_squared(M, x)
        9
        >>> M = listlist2mat([[3/5, 1/5, 1/5], [0, 2/3, 1/3]])
        >>> distance_squared(M, x)
        8.355575308641976
    '''
    return (x*x) - projection_length_squared(M,x)

## Task 7

distances_to_subspace = [distance_squared(orthonormal_basis, v) for v in centered_face_images.values()]

## Task 8
uclf_images = {i: Vec(D, {(x,y): face[y][x] for x in range(166) for y in range(189)}) for i,face in load_images('unclassified/',11).items()}
centered_uclf_images = {i: face - centroid for i,face in uclf_images.items()}
classified_as_faces  = set(k for k,v in centered_uclf_images.items() 
                             if distance_squared(orthonormal_basis, v) < 6*sum(distances_to_subspace)/len(distances_to_subspace)) # of dictionary keys

## Task 9

threshold_value = 6 * sum(distances_to_subspace)/len(distances_to_subspace)

## Task 10

#This is the "transpose" of what was specified in the text.
#Follow the spec given here.
def project(M, x):
    '''
    Input:
        - M: an orthogonal matrix with row-space equal to x's domain
        - x: a Vec
    Output:
        - the projection of x into the column-space of M
    Example:
        >>> from vecutil import list2vec
        >>> from matutil import listlist2mat
        >>> x = list2vec([1, 2, 3])
        >>> M = listlist2mat([[1, 0], [0, 1], [0, 0]])
        >>> project(M, x)
        Vec({0, 1, 2},{0: 1, 1: 2, 2: 0})
        >>> M = listlist2mat([[3/5, 0], [1/5, 2/3], [1/5, 1/3]])
        >>> project(M, x)
        Vec({0, 1, 2},{0: 0.96, 1: 1.8755555555555554, 2: 1.0977777777777777})
    '''
    return x * M.transpose() * M

## Task 11

# see documentation for image.image2display

## Task 12

