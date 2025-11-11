from __future__ import annotations
from decimal import Decimal
from typing import overload, Sequence, Optional, Union


def _to_decimal(x):
    """Convert int/float/Decimal to Decimal (use string for floats to preserve value)."""
    if isinstance(x, Decimal):
        return x
    if isinstance(x, int):
        return Decimal(x)
    if isinstance(x, float):
        return Decimal(str(x))
    raise ValueError("Only int, float or Decimal values are allowed")


class vector():
    @overload
    def __init__(self, stop: Union[int, float, Decimal]) -> None: ...

    @overload
    def __init__(self, start: Union[int, float, Decimal], stop: Union[int, float, Decimal]) -> None: ...

    @overload
    def __init__(self, start: Union[int, float, Decimal], stop: Union[int, float, Decimal], step: Union[int, float, Decimal]) -> None: ...

    def __init__(
        self,
        start: Union[int, float, Decimal] = 0,
        stop: Optional[Union[int, float, Decimal]] = None,
        step: Union[int, float, Decimal] = 1,
        data: Optional[Sequence[Union[int, float, Decimal]]] = None,
    ) -> None:
        """
        Create a vector instance.

        - No args: empty vector
        - 1 arg: stop (inclusive)
        - 2 args: start, stop (inclusive)
        - 3 args: start, stop, step (inclusive)

        You can also provide data from a list with .addData() method.
        """
        self.name= ""
        if data is not None:
            self.vec = [_to_decimal(x) for x in data]
            return

        if stop is None:
            stop = start
            start = 0

        if start == stop:
            self.vec = []
            return

        start = _to_decimal(start)
        stop = _to_decimal(stop)
        step_d = _to_decimal(step)

        if step_d == 0:
            raise ValueError("Step value cannot be zero")

        self.vec = []
        current = start
        if step_d > 0:
            while current <= stop:
                self.vec.append(current)
                current += step_d
        else:
            while current >= stop:
                self.vec.append(current)
                current += step_d

    def __len__(self) -> int:
        return len(self.vec)

    def __str__(self) -> str:
        txt= ""
        spaces= len(str(len(self.vec)+1))
        txt+= f"\nVector of length {len(self.vec)}:\n"
        txt+= " +--" + "-"*10 + "\n"
        txt+= f" |  {' ' * (spaces-1)}idx|val\n"
        for i, val in enumerate(self.vec):
            toUse= spaces - len(str(i))
            txt += f" |-> {' '*toUse}{i} | {val}\n"
        return txt

    def __add__(self, other: int | float | Decimal | "vector") -> "vector":
        if isinstance(other, (int, float, Decimal)):
            other_d = _to_decimal(other)
            return vector(data=[x + other_d for x in self.vec])
        if isinstance(other, vector):
            if len(self.vec) != len(other.vec):
                raise ValueError("vectors must be same length")
            return vector(data=[a + b for a, b in zip(self.vec, other.vec)])
        raise ValueError("Other must be int|float|Decimal|vector")

    def __sub__(self, other: int | float | Decimal | "vector") -> "vector":
        if isinstance(other, (int, float, Decimal)):
            other_d = _to_decimal(other)
            return vector(data=[x - other_d for x in self.vec])
        if isinstance(other, vector):
            if len(self.vec) != len(other.vec):
                raise ValueError("vectors must be same length")
            return vector(data=[a - b for a, b in zip(self.vec, other.vec)])
        raise ValueError("Other must be int|float|Decimal|vector")

    def __mul__(self, other: int | float | Decimal | "vector") -> "vector":
        if isinstance(other, (int, float, Decimal)):
            other_d = _to_decimal(other)
            return vector(data=[x * other_d for x in self.vec])
        if isinstance(other, vector):
            if len(self.vec) != len(other.vec):
                raise ValueError("vectors must be same length")
            return vector(data=[a * b for a, b in zip(self.vec, other.vec)])
        raise ValueError("Other must be int|float|Decimal|vector")

    def __div__(self, other: int | float | Decimal | "vector") -> "vector":
        if isinstance(other, (int, float, Decimal)):
            other_d = _to_decimal(other)
            return vector(data=[x / other_d for x in self.vec])
        if isinstance(other, vector):
            if len(self.vec) != len(other.vec):
                raise ValueError("vectors must be same length")
            return vector(data=[a / b for a, b in zip(self.vec, other.vec)])
        raise ValueError("Other must be int|float|Decimal|vector")

    def __truediv__(self, other: int | float | Decimal | "vector") -> "vector":
        return self.__div__(other)

    def __getitem__(self, s: slice | int):
        if isinstance(s, int):
            return self.vec[s]
        return vector(data=list(self.vec[s]))

    def sum(self) -> Decimal:
        """Return the sum of the vector elements."""
        return sum(self.vec, Decimal(0))
    
    suma= sum
    
    def diff(self) -> "vector":
        """Return the differences between consecutive elements as a new vector."""
        if len(self.vec) < 2:
            return vector()
        diffs = [self.vec[i+1] - self.vec[i] for i in range(len(self.vec)-1)]
        return vector(data=diffs)
    
    def addInfo(self, name="") -> None:
        """Add a name or description to the vector."""
        self.name= name

    def find(self, value: int | float | Decimal) -> int | None:
        """Find the index of a value in the vector. Returns None if not found."""
        try:
            value_d = _to_decimal(value)
            return self.vec.index(value_d)
        except Exception:
            return None
        
    encontrar= find
        
    def addData(self, data:list|tuple) -> None:
        """Add multiple values to the end of the vector from a list or tuple."""
        for item in data:
            self.append(item)

    agregarDatos= addData

    def append(self, obj: int | float | Decimal) -> None:
        """Append a value to the end of the vector."""
        if isinstance(obj, (int, float, Decimal)):
            self.vec.append(_to_decimal(obj))
        else:
            raise ValueError("Only int, float and Decimal values are allowed in vector")

    def combine(self, other: "vector") -> "vector":
        """Combine two vectors into a new vector by concatenation."""
        if not isinstance(other, vector):
            raise ValueError("Other must be a vector")
        return vector(data=(self.vec + other.vec))
    
    combinar= combine
    
    def toFloats(self) -> list[float]:
        """Convert the vector elements to a list of floats."""
        return [float(x) for x in self.vec]