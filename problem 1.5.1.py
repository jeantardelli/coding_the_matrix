import string

def gf2(A, B):
    """
    Galois Field 2 has just two elements: 0 and 1
    Sum is the same for subtracting
    """
    return ''.join(['1' if x!=y else '0' for (x, y) in zip(A, B)])

cyphertext = '10101', '00100', '10101', '01011', '11001', '00011', '01011', '10101', '00100', '11001', '11010'
letters = {number : letter for (number, letter) in enumerate(string.ascii_uppercase + ' ')}

if __name__ == '__main__':
    j = 0
    while j != 27:
        bits = {'{0:05b}'.format(number) : number for number in range(len(letters))}
        key  = '{0:05b}'.format(j)
        msg  = [letters[bits[gf2(c, key) if gf2(c, key) in bits else '11010']] for c in cyphertext]
        print(''.join(msg))
        j += 1
