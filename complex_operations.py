import math

def scales(z, scalar):
    """
    scales a complex number
    input   : complex number z = x + yi
    output  : a scaled complex number z = scalar * x + scalar * yi

    example : given 2 + 4 j and scaler 0.5, returns 1 + 2j
    """
    return z * scalar

def translates (z, z0):
    """
    translates a complex number
    input   : complex number z = x + yi
    output  : a translated complex number z + z0

    example : given z = 1 + ij and z0 = 0 - 1j, return (1 + 0j)
    """
    return z + z0

def rotates (z, ang):
    """
    Rotates by pi a complex number. Use euler notation and the angle in radians
    input   : a complex number z = x + yi
    output  : a rotated complex number such that g(z) = z * e ** pi *1j
    """
    return z * math.e ** (ang * 1j )

def center (S):
    """
    calculate the center of a set of complex numbers.
    input   : set of complex numbers S
    output  : a unique complex number representing the centre of the group

    example : given {1 + 1j, -1 -1j, 3 + 0j), returns 1 + 0j
    """
    return sum(S) / len(S)
