from math import sin, cos, tan, radians, e, pi, log, sqrt
from decimal import Decimal

e= Decimal(str(e))
pi= Decimal(str(pi))

if __name__ == "__main__":
    from vector import vector
else:
    from .vector import vector

def _gaussian_elimination(A: list[list[Decimal]], B: list[Decimal]) -> list[Decimal]:
    """
    Resuelve el sistema lineal A * x = B usando eliminación gaussiana.

    Args:
        A: matriz (lista de listas) de Decimals (se modifica en el proceso).
        B: vector (lista) de Decimals (se modifica en el proceso).
        Devuelve: lista de Decimals con las soluciones.
    
    Lanza ValueError si la matriz es singular y no puede ser resuelta.
    """
    n = len(B)
    # Forward elimination
    for i in range(n):
        # Pivoting
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        B[i], B[max_row] = B[max_row], B[i]

        # Make the diagonal contain all 1s
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("La matriz es singular y no puede resolverse.")
        for j in range(i, n):
            A[i][j] /= pivot
        B[i] /= pivot

        # Eliminate below
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            B[k] -= factor * B[i]

    # Back substitution
    x = [Decimal(0) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = B[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
    return x

class fx():
    def __init__(self, equation:str, degRad= "deg"):
        """
        Crea un objeto función a partir de una ecuación dada como cadena.

        Args:
            equation: ecuación como cadena, ej. '2x^2 + 3x + 1'.
            x será el vector (o número) sobre el que se evalúa la función.
            degRad: 'deg' para grados, 'rad' para radianes (afecta funciones trigonométricas).
        """
        eq= equation.replace(" ", "")
        eq= eq.lower()
        eq= eq.replace("sen", "sin")
        self.original= eq
        eq= eq.replace("^", "**")
        while True:
            for i, val in enumerate(eq):
                if val == "x" and i != 0:
                    if eq[i-1].isdigit() or eq[i-1] == ")":
                        eq = eq[:i] + "*" + eq[i:]
                        break
            else:
                break

        if degRad == "deg":
            if any(["sin" in eq, "cos" in eq, "tan" in eq]):
                for i in ["sin", "cos", "tan"]:
                    From= 0
                    while eq.find(i, From) != -1:
                        From= eq.find(i, From) + 4
                        to= From + 1
                        opens= 1
                        while opens != 0:
                            if eq[to] == "(":
                                opens+= 1
                            elif eq[to] == ")":
                                opens-= 1
                            to+= 1

                        lst= list(eq)
                        lst.insert(to, ")")
                        lst.insert(From, "radians(")
                        eq= "".join(lst)

        self.equation= eq

    def __str__(self):
        return self.original

    def calc(self, x: int | float | vector, **constants:int | float | Decimal):
        """
        Calcula el/los valor(es) de la función para el x dado.

        Args:
            x: int | float | vector (lista de valores de x).
            constants: constantes adicionales disponibles por nombre en la ecuación.
        
        Devuelve: Decimal o vector de Decimals con los resultados.
        """
        # Build a safe environment for eval: include math functions and any passed constants.
        env = {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "radians": radians,
            "e": e,
            "pi": pi,
            "log": log,
            "sqrt": sqrt,
            "Decimal": Decimal,
            "vector": vector,
        }
        # Add user-provided constants into the environment (they'll be available by name in eval)
        env.update(constants)

        toEval = x
        x = 0
        newVec= vector()
        newVec.addInfo(self.original)
        if isinstance(toEval, vector):
            for xi in toEval:
                env["x"] = float(xi)
                # evaluate using our environment; avoid exposing builtins by using empty globals
                newVec.append(Decimal(str(eval(self.equation, {}, env))))
            return newVec
        elif isinstance(toEval, (int, float, Decimal)):
            x= toEval
            env["x"] = float(toEval)
            return Decimal(str(eval(self.equation, {}, env)))
        else:
            raise ValueError("x debe ser int|float|vector")
    
    def eval(self, x: int | float | vector, **constants:int | float | Decimal):
        """Evalúa la función en los valores x dados.

        Args:
            x: int, float o vector de valores de x.
            constants: constantes adicionales a usar en la ecuación.
        
        Equivalente a calc().
        """
        return self.calc(x, **constants)
    
def polyfit(x: vector, y: vector, degree: int) -> fx:
    """
    Ajusta un polinomio de grado dado a los puntos de datos (x, y) usando mínimos cuadrados.
    
    Args:
        x: vector de valores independientes.
        y: vector de valores dependientes.
        degree: grado del polinomio (>= 0).
        Devuelve: objeto fx que representa el polinomio ajustado.
    Lanza ValueError si las longitudes de x e y difieren o si degree < 0.
    """
    if len(x) != len(y):
        raise ValueError("x e y deben tener la misma longitud")
    if degree < 0:
        raise ValueError("degree debe ser un entero no negativo")

    n = len(x)
    A = [[Decimal(0) for _ in range(degree + 1)] for _ in range(degree + 1)]
    B = [Decimal(0) for _ in range(degree + 1)]

    for i in range(n):
        xi = x[i]
        yi = y[i]
        for j in range(degree + 1):
            B[j] += yi * (xi ** j)
            for k in range(degree + 1):
                A[j][k] += xi ** (j + k)

    coeffs = _gaussian_elimination(A, B)

    equation_terms = []
    for i, coeff in enumerate(coeffs):
        if i == 1:
            equation_terms.append(f"{coeff}x")
        elif i == 0:
            equation_terms.append(f"{coeff}")
        else:
            equation_terms.append(f"{coeff}x^{i}")
    equation = " + ".join(equation_terms).replace("+ -", "- ")

    return fx(equation)