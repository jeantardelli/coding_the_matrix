# version code 53ead35ddb8a+
# Please fill out this stencil and submit using the provided submission script.

from vec import Vec
from mat import Mat
from math import sqrt
import pagerank



## 1: (Task 12.12.1) Find Number of Links
def find_num_links(L):
    '''
    Input:
        - L: a square matrix representing link structure
    Output:
        - A vector mapping each column label of L to
          the number of non-zero entries in the corresponding
          column of L
    Example:
        >>> from matutil import listlist2mat
        >>> find_num_links(listlist2mat([[1,1,1],[1,1,0],[1,0,0]]))
        Vec({0, 1, 2},{0: 3, 1: 2, 2: 1})
    '''
    return Vec(L.D[1], {c: sum([L[r,c] for r in L.D[0]]) for c in L.D[1]})



## 2: (Task 12.12.2) Make Markov
def make_Markov(L):
    '''
    Input:
        - L: a square matrix representing link structure
    Output:
        - None: changes L so that it plays the role of A_1
    Example:
        >>> from matutil import listlist2mat
        >>> M = listlist2mat([[1,1,1],[1,0,0],[1,0,1]])
        >>> make_Markov(M)
        >>> M == Mat(({0, 1, 2}, {0, 1, 2}), {(0, 1): 1.0, (2, 0): 0.3333333333333333, (0, 0): 0.3333333333333333, (2, 2): 0.5, (1, 0): 0.3333333333333333, (0, 2): 0.5})
        True
    '''
    num_links = find_num_links(L)
    for r in L.D[0]:
        for c in L.D[1]:
            L[r,c] /= num_links[c]



## 3: (Task 12.12.3) Power Method
def power_method(A1, i):
    '''
    Input:
        - A1: a matrix
        - i: number of iterations to perform
    Output:
        - An approximation to the stationary distribution
    Example:
        >>> from matutil import listlist2mat
        >>> v = power_method(listlist2mat([[0.6,0.5],[0.4,0.5]]), 10)
        >>> (listlist2mat([[0.6,0.5],[0.4,0.5]]) * v - v).is_almost_zero()
        True
    '''
    v = Vec(A1.D[0], {r: 1 for r in A1.D[0]})
    for iter in range(i):
        norm_before = (v*v) / sqrt(v*v)
        v = A1 * v
        norm_after  = (v*v) / sqrt(v*v)
        print('iter: {}\nNorm before / Norm after: {}'.format(iter, norm_before/norm_after))
    return v / sqrt(v*v)



## 4: (Task 12.12.4) Jordan
number_of_docs_with_jordan = len(pagerank.find_word('jordan'))



## 5: (Task 12.12.5) Wikigoogle
def wikigoogle(w, k, p):
    '''
    Input:
        - w: a word
        - k: number of results
        - p: pagerank eigenvector
    Output:
        - the list of the names of the kth heighest-pagerank Wikipedia
          articles containing the word w
    '''
    articles = pagerank.find_word(w)
    articles.sort(key=lambda x: p[x], reverse=True)
    return articles[:k]



## 6: (Task 12.12.6) Using Power Method

A1 = make_Markov(pagerank.read_data())
p  = power_method(.85 * A1 + .15 * Mat(A1.D, {(r,c): 1/len(A1.D[0]) for r in A1.D[0] for c in A1.D[1]}), 5)

results_for_jordan = wikigoogle('jordan', 5, p) # give 5 of them as a list
results_for_obama  = wikigoogle('obama', 5, p)
results_for_tiger  = wikigoogle('tiger', 5, p)
results_for_matrix = wikigoogle('matrix', 5, p)




## 7: (Task 12.12.7) Power Method Biased
def power_method_biased(A1, i, r):
    '''
    Input:
        - A1: a matrix, as in power_method
        - i: number of iterations
        - r: bias label
    Output:
        - Approximate eigenvector of .55A_1 + 0.15A_2 + 0.3A_r
    '''
    biased_articles = pagerank.find_word(r)
    A_r = Mat(A1.D, {(r,c): 1 for c in biased_articles for r in A1.D[0] if A1[r,c] > 0})
    A   = .55 * A1 + .15 * Mat(A1.D, {(r,c): 1/len(A1.D[0]) for r in A1.D[0] for c in A1.D[1]}) + .30 * A_r
    return power_method(A, i)

p_sport = power_method_biased(A1, 5, 'sport') 
sporty_results_for_jordan = wikigoogle('jordan', 5, p_sport)
sporty_results_for_obama  = wikigoogle('obama', 5, p_sport)
sporty_results_for_tiger  = wikigoogle('tiger', 5, p_sport)
sporty_results_for_matrix = wikigoogle('matrix', 5, p_sport)

