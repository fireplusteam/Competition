

def FourD(rows, columns, z, w, def_val):
    """
    Create array of 4 dimensions like this
    array[rows][columns][z][w]
    """
    return [[[[def_val for _ in range(w)] for _ in range(z)] for _ in range(columns)] for _ in range(rows)]


def ThreeD(rows, columns, z, def_val):
    """
    Create array of 3 dimensions like this
    array[rows][columns][z]
    """
    return [[[def_val for _ in range(z)] for _ in range(columns)] for _ in range(rows)]

    
def TwoD(rows, columns, def_val):
    """
    Create array of 2 dimensions like this
    array[rows][columns]
    """
    return [[def_val for _ in range(columns)] for _ in range(rows)]