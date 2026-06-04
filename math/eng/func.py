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
        self.degRad= degRad
        self.original= eq
        eq= eq.replace("^", "**")
        while True:
            for i, val in enumerate(eq):
                if val.isalpha() and i != 0:
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

    def getDeriv(self, var: str) -> fx:
        """Returns the simple derivative of the function with respect to a variable.
        
        Note: This is still a simple implementation, but supports nested chain rule
        for basic operators/functions (sum, product, powers of var, sin/cos/tan/sqrt/radians/log).
        
        Args:
            var: variable to differentiate with respect to (e.g., 'x')
        """
        if var not in self.equation:
            return fx("0", self.degRad)

        def _strip_outer_parens(expr: str) -> str:
            expr = expr.strip()
            while expr.startswith("(") and expr.endswith(")"):
                depth = 0
                valid = True
                for i, ch in enumerate(expr):
                    if ch == "(":
                        depth += 1
                    elif ch == ")":
                        depth -= 1
                        if depth == 0 and i != len(expr) - 1:
                            valid = False
                            break
                if valid:
                    expr = expr[1:-1].strip()
                else:
                    break
            return expr

        def _split_top_level_sum(expr: str) -> list[str]:
            parts = []
            start = 0
            depth = 0
            for i, ch in enumerate(expr):
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                elif depth == 0 and ch in "+-" and i != 0:
                    parts.append(expr[start:i])
                    start = i
            parts.append(expr[start:])
            return [p for p in parts if p]

        def _split_top_level_product(expr: str) -> tuple[list[str], list[str]]:
            factors = []
            ops = []
            start = 0
            depth = 0
            i = 0
            while i < len(expr):
                ch = expr[i]
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                elif depth == 0 and ch in "*/":
                    prev_ch = expr[i - 1] if i > 0 else ""
                    next_ch = expr[i + 1] if i + 1 < len(expr) else ""
                    if ch == "*" and (prev_ch == "*" or next_ch == "*"):
                        i += 1
                        continue
                    factors.append(expr[start:i])
                    ops.append(ch)
                    start = i + 1
                i += 1
            factors.append(expr[start:])
            return [f for f in factors if f], ops

        def _is_number(expr: str) -> bool:
            try:
                Decimal(expr)
                return True
            except Exception:
                return False

        def _is_one(expr: str) -> bool:
            return _strip_outer_parens(expr) in ("1", "+1")

        def _is_zero(expr: str) -> bool:
            expr = _strip_outer_parens(expr)
            if expr in ("0", "+0", "-0"):
                return True
            if _is_number(expr):
                return Decimal(expr) == 0
            return False

        def _make_product(parts: list[str]) -> str:
            coeff = Decimal("1")
            symbolic = []
            for part in parts:
                if not part:
                    continue
                token = _strip_outer_parens(part)
                if _is_one(token):
                    continue
                if _is_number(token):
                    coeff *= Decimal(token)
                else:
                    probe = token
                    start = 1 if probe.startswith(("+", "-")) else 0
                    i = start
                    while i < len(probe) and (probe[i].isdigit() or probe[i] == "."):
                        i += 1
                    if i > start and i < len(probe) and probe[i].isalpha():
                        try:
                            coeff *= Decimal(probe[:i])
                            symbolic.append(probe[i:])
                        except Exception:
                            symbolic.append(token)
                    else:
                        symbolic.append(token)

            if coeff == 0:
                return "0"

            if not symbolic:
                return str(coeff)

            if coeff == 1:
                return "*".join(symbolic)

            if coeff == -1:
                if len(symbolic) == 1:
                    return f"-{symbolic[0]}"
                return f"-({'*'.join(symbolic)})"

            return f"{coeff}*{'*'.join(symbolic)}"

        def _parse_function(expr: str) -> tuple[str, str] | None:
            expr = _strip_outer_parens(expr)
            if "(" not in expr or not expr.endswith(")"):
                return None
            idx = expr.find("(")
            name = expr[:idx]
            if not name.isalpha():
                return None
            arg = expr[idx + 1:-1]
            depth = 0
            for ch in arg:
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth < 0:
                        return None
            if depth != 0:
                return None
            return name, arg

        def _derive_factor(factor: str) -> str:
            factor = _strip_outer_parens(factor)
            if factor == "":
                return "0"

            if factor == var:
                return "1"
            if _is_number(factor):
                return "0"

            sign = ""
            core = factor
            if core.startswith("+"):
                core = core[1:]
            elif core.startswith("-"):
                sign = "-"
                core = core[1:]
            core = _strip_outer_parens(core)

            if core == var:
                return "-1" if sign else "1"
            if _is_number(core):
                return "0"

            if core.startswith(var + "**"):
                exp_str = core[len(var) + 2:]
                try:
                    n = int(exp_str)
                    coeff = n
                    p = n - 1
                    if p == 0:
                        base = f"{coeff}"
                    elif p == 1:
                        base = f"{coeff}{var}"
                    else:
                        base = f"{coeff}{var}**{p}"
                    return f"-{base}" if sign else base
                except Exception:
                    pass

            func = _parse_function(core)
            if func is not None:
                name, arg = func
                d_arg = _derive_expr(arg)
                if _is_zero(d_arg):
                    return "0"

                if name == "sin":
                    base = _make_product([f"cos({arg})", d_arg])
                elif name == "cos":
                    base = _make_product([f"-sin({arg})", d_arg])
                elif name == "tan":
                    base = _make_product([f"1/cos({arg})**2", d_arg])
                elif name == "sqrt":
                    base = _make_product([f"1/(2*sqrt({arg}))", d_arg])
                elif name == "radians":
                    base = _make_product(["(pi/180)", d_arg])
                elif name == "log":
                    base = _make_product([f"1/({arg})", d_arg])
                else:
                    return "0"

                return f"-{base}" if sign else base

            return "0"

        def _derive_expr(expr: str) -> str:
            expr = _strip_outer_parens(expr)
            if expr == "":
                return "0"

            terms = _split_top_level_sum(expr)
            if len(terms) > 1:
                d_terms = []
                for term in terms:
                    d_term = _derive_expr(term)
                    if not _is_zero(d_term):
                        d_terms.append(d_term)
                if not d_terms:
                    return "0"
                return " + ".join(d_terms)

            factors, ops = _split_top_level_product(expr)
            if len(factors) == 1:
                return _derive_factor(factors[0])

            # Product/quotient handling.
            if all(op == "*" for op in ops):
                pieces = []
                for i, factor in enumerate(factors):
                    d_factor = _derive_factor(factor)
                    if _is_zero(d_factor):
                        continue
                    product_parts = [d_factor] + [factors[j] for j in range(len(factors)) if j != i]
                    pieces.append(_make_product(product_parts))
                if not pieces:
                    return "0"
                return " + ".join(pieces)

            # Simple quotient rule for a/b (single division).
            if len(factors) == 2 and len(ops) == 1 and ops[0] == "/":
                a, b = factors
                da = _derive_factor(a)
                db = _derive_factor(b)
                if _is_zero(da) and _is_zero(db):
                    return "0"
                num_left = _make_product([da, b]) if not _is_zero(da) else "0"
                num_right = _make_product([a, db]) if not _is_zero(db) else "0"
                numerator = num_left if _is_zero(num_right) else (f"-{num_right}" if _is_zero(num_left) else f"{num_left}-{num_right}")
                return f"({numerator})/({b})**2"

            return "0"

        derived = _derive_expr(self.equation)
        if _is_zero(derived):
            return fx("0", self.degRad)
        derived = derived.replace("+-", "-")
        derived = derived.replace("+ -", "-")
        while "++" in derived or "--" in derived or "+-" in derived or "-+" in derived:
            derived = derived.replace("++", "+")
            derived = derived.replace("--", "+")
            derived = derived.replace("+-", "-")
            derived = derived.replace("-+", "-")
        return fx(derived, self.degRad)

    def __evaling__(self, constants, variables, equations, preventDivZero):
        env = {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "radians": radians,
            # math trig/log functions return float, so keep e/pi as float
            # to avoid mixed float*Decimal TypeError inside eval.
            "e": float(e),
            "pi": float(pi),
            "log": log,
            "sqrt": sqrt,
            "Decimal": Decimal,
            "vector": vector,
        }
        env.update(constants)
        newVec= vector()
        if len(variables) == 1:
            newConstants= constants.copy()
            for val in list(variables.values())[0]:
                newConstants[list(variables.keys())[0]]= float(val)
                for eqName, eq in equations.items():
                    newConstants[eqName]= eq.__evaling__(newConstants, [], equations, preventDivZero)
                env[list(variables.keys())[0]]= float(val)
                try:
                    newVec.append(Decimal(str(eval(self.equation, {}, env))))
                except ZeroDivisionError:
                    newVec.append(Decimal(str(preventDivZero)))
        elif len(variables) == 0:
            try: 
                res= float(eval(self.equation, {}, env))
            except ZeroDivisionError:
                res= float(preventDivZero)
            return res
        else:
            newConstants= constants.copy()
            newVariables= variables.copy()
            newVariables.pop(list(variables.keys())[0])
            for val in list(variables.values())[0]:
                newConstants[list(variables.keys())[0]]= float(val)
                newVec= newVec.combine(self.__evaling__(newConstants, newVariables, equations, preventDivZero= preventDivZero))
        return newVec


    def __str__(self):
        return self.original

    def calc(self, preventDivZero:int =0, **values:int | float | Decimal):
        """
        Calculates the function value(s) for given x.

        Args:
            values: dictionary of variable names and their values (e.g., x=5, k=10)
            preventDivZero: if > 0, replaces any zero denominators with this value to prevent division by zero errors.
        """
        # Build a safe environment for eval: include math functions and any passed constants.

        variables= {}
        constants= {}
        equations= {}

        for i, v in enumerate(list(values.values())):
            if isinstance(v, (int, float, Decimal)):
                constants[list(values.keys())[i]]= values[list(values.keys())[i]]
            elif isinstance(v, (vector, list, tuple)):
                variables[list(values.keys())[i]]= values[list(values.keys())[i]]
            elif isinstance(v, fx):
                equations[list(values.keys())[i]]= values[list(values.keys())[i]]
            else:
                raise ValueError("Values must be int, float, Decimal, or vector")

        return self.__evaling__(constants, variables, equations, preventDivZero)
    
    def eval(self, preventDivZero: int= 0, **values:int | float | Decimal):
        """Evaluates the function at given x value(s).
        
        Args:
            values: dictionary of variable names and their values (e.g., x=5, k=10)
            preventDivZero: if > 0, replaces any zero denominators with this value to prevent division by zero errors.
        """
        return self.calc(**values, preventDivZero= preventDivZero)
    
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