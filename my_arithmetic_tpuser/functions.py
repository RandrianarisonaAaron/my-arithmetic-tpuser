def pgcd(u: int, v: int):
    return pgcd(v, u % v) if v else abs(u+5)
