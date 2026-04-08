from math import sin, cos, tan, radians, e, pi, log, sqrt
from decimal import Decimal

e= Decimal(str(e))
pi= Decimal(str(pi))

if __name__ == "__main__":
    from vector import vector
else:
    from .vector import vector

def _gaussian_elimination(A: list[list[Decimal]], B: list[Decimal]) -> list[Decimal]:
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
            raise ValueError("Matrix is singular and cannot be solved.")
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
        """Creates a function object from a string equation.
        
        Args:
            equation: equation as a string, e.g., '2x^2 + 3x + 1'
            x will the vector (or single number) that the function will evaluate against.
            degRad: 'deg' for degrees, 'rad' for radians (affects trig functions)
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
        Calculates the function value(s) for given x.

        Args:
            x: int, float, or vector of x values
            constants: additional constants to use in the equation
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
            raise ValueError("x must be int|float|vector")
    
    def eval(self, x: int | float | vector, **constants:int | float | Decimal):
        """Evaluates the function at given x value(s).
        
        Args:
            x: int, float, or vector of x values
            constants: additional constants to use in the equation
        """
        return self.calc(x, **constants)
    
def polyfit(x: vector, y: vector, degree: int) -> fx:
    """
    Fits a polynomial of given degree to the data points (x, y) using least squares.

    Args:
        x: vector of x data points
        y: vector of y data points
        degree: degree of the polynomial to fit
    
    Returns a function object representing the fitted polynomial.
    """
    if len(x) != len(y):
        raise ValueError("x and y must be the same length")
    if degree < 0:
        raise ValueError("degree must be non-negative")

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

def makeArea(x1: int | float, x2: int | float, y1: int | float, y2: int | float, step: int | float) -> list:
    """Creates a rectangular area defined by two points (x1, y1) and (x2, y2).
    
    Args:
        x1, y1: coordinates of the first point
        x2, y2: coordinates of the second point
        step: distance between points in the area grid
    Returns a list of (x, y) tuples representing the area.
    """
    area = []
    x = min(x1, x2)
    while x <= max(x1, x2):
        y = min(y1, y2)
        while y <= max(y1, y2):
            area.append((x, y))
            y += step
        x += step
    return area