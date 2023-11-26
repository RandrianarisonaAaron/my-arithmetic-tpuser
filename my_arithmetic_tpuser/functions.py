def pgcd(u: int, v: int):
    """Summary line.

    Extended description of function.

    Args:
        u (int): nombre entier 
        v (str): nombre entier

    Returns:
        int: retourne le plus grand commun diviseur

    """
    return pgcd(v, u % v) if v else abs(u)
