from __future__ import annotations
from decimal import Decimal
import pandas as pd
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

        You can also provide data from a list with data=[values].
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
    
    def __setitem__(self, s: slice | int, value) -> None:
        if isinstance(s, int):
            self.vec[s] = _to_decimal(value)
            return

        if not isinstance(value, Sequence):
            raise ValueError("Slice assignment requires a sequence of values")

        self.vec[s] = [_to_decimal(x) for x in value]

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
    
    def __pow__(self, other: int | float | Decimal | "vector") -> "vector":
        if isinstance(other, (int, float, Decimal)):
            other_d = _to_decimal(other)
            return vector(data=[x ** other_d for x in self.vec])
        if isinstance(other, vector):
            if len(self.vec) != len(other.vec):
                raise ValueError("vectors must be same length")
            return vector(data=[a ** b for a, b in zip(self.vec, other.vec)])
        raise ValueError("Other must be int|float|Decimal|vector")

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
        """Find the index of a value in the vector. Returns None if not found.
        
        Args:
            value: value to find in the vector
        """
        try:
            value_d = _to_decimal(value)
            return self.vec.index(value_d)
        except Exception:
            return None
        
    encontrar= find
        
    def addData(self, data:list|tuple) -> None:
        """Add multiple values to the end of the vector from a list or tuple.
        
        Args:
            data: list or tuple of values to add to the vector
        """
        for item in data:
            self.append(item)

    agregarDatos= addData

    def append(self, obj: int | float | Decimal) -> None:
        """Append a value to the end of the vector.
        
        Args:
            obj: value to append (int, float, or Decimal)
        """
        if isinstance(obj, (int, float, Decimal)):
            self.vec.append(_to_decimal(obj))
        else:
            raise ValueError("Only int, float and Decimal values are allowed in vector")

    def combine(self, other: "vector") -> "vector":
        """Combine two vectors into a new vector by concatenation.
        
        Args:
            other: another vector to combine with.
        """
        if not isinstance(other, vector):
            raise ValueError("Other must be a vector")
        return vector(data=(self.vec + other.vec))
    
    combinar= combine
    
    def _toFloats(self) -> list[float]:
        """Convert the vector elements to a list of floats."""
        return [float(x) for x in self.vec]
    
class vector2D():
    @overload
    def __init__(self, stop_x: Union[int, float, Decimal], stop_y: Union[int, float, Decimal]) -> None: ...

    @overload
    def __init__(self, start_x: Union[int, float, Decimal], stop_x: Union[int, float, Decimal], start_y: Union[int, float, Decimal], stop_y: Union[int, float, Decimal]) -> None: ...

    @overload
    def __init__(self, start_x: Union[int, float, Decimal], stop_x: Union[int, float, Decimal], step_x: Union[int, float, Decimal], start_y: Union[int, float, Decimal], stop_y: Union[int, float, Decimal], step_y: Union[int, float, Decimal]) -> None: ...

    def __init__(self, *args, points: Optional[Sequence[Sequence[Union[int, float, Decimal]]]] = None) -> None:
        """
        Create a 2D vector/grid.

        Supported overloads:
        - vector2D(stop_x, stop_y)
        - vector2D(start_x, stop_x, start_y, stop_y)
        - vector2D(start_x, stop_x, step_x, start_y, stop_y, step_y)
        - vector2D(points=[[x1, y1], [x2, y2], ...])
        """
        self.name = ""
        self.points: list[tuple[Decimal, Decimal]] = []
        self.x_axis: list[Decimal] = []
        self.y_axis: list[Decimal] = []

        if points is not None:
            self._init_from_points(points)
            return

        if len(args) == 2:
            start_x, stop_x, step_x = 0, args[0], 1
            start_y, stop_y, step_y = 0, args[1], 1
        elif len(args) == 4:
            start_x, stop_x, start_y, stop_y = args
            step_x, step_y = 1, 1
        elif len(args) == 6:
            start_x, stop_x, step_x, start_y, stop_y, step_y = args
        else:
            raise ValueError("vector2D expects 2, 4, or 6 positional values, or points=[(x, y), ...]")

        self.x_axis = self._build_axis(start_x, stop_x, step_x)
        self.y_axis = self._build_axis(start_y, stop_y, step_y)
        self._rebuild_points_from_axes()

    def _init_from_points(self, points: Sequence[Sequence[Union[int, float, Decimal]]]) -> None:
        x_vals: list[Decimal] = []
        y_vals: list[Decimal] = []
        for p in points:
            if len(p) != 2:
                raise ValueError("Each point must have exactly 2 values: (x, y)")
            x_d = _to_decimal(p[0])
            y_d = _to_decimal(p[1])
            self.points.append((x_d, y_d))
            x_vals.append(x_d)
            y_vals.append(y_d)

        self.x_axis = sorted(set(x_vals))
        self.y_axis = sorted(set(y_vals))

    def _build_axis(self, start, stop, step) -> list[Decimal]:
        start_d = _to_decimal(start)
        stop_d = _to_decimal(stop)
        step_d = _to_decimal(step)

        if step_d == 0:
            raise ValueError("Step value cannot be zero")

        if start_d == stop_d:
            return [start_d]

        values: list[Decimal] = []
        current = start_d
        if step_d > 0:
            while current <= stop_d:
                values.append(current)
                current += step_d
        else:
            while current >= stop_d:
                values.append(current)
                current += step_d

        return values

    def _rebuild_points_from_axes(self) -> None:
        self.points = []
        for y in self.y_axis:
            for x in self.x_axis:
                self.points.append((x, y))

    def __len__(self) -> int:
        return len(self.points)

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, s: slice | int):
        if isinstance(s, int):
            return self.points[s]
        return self.points[s]

    def __str__(self) -> str:
        return f"\nvector2D with {len(self.points)} points ({len(self.x_axis)} x {len(self.y_axis)})\n"

    def addInfo(self, name="") -> None:
        self.name = name

    def toX(self) -> list[float]:
        """Get all the x values (repeating) of the points as a list of floats."""
        return [float(x) for x, _ in self.points]

    def toY(self) -> list[float]:
        """Get all the y values (repeating) of the points as a list of floats."""
        return [float(y) for _, y in self.points]
    
    def getX(self) -> list[float]:
        """Get the unique x-axis values as a list of floats."""
        return [float(x) for x in self.x_axis]
    
    def getY(self) -> list[float]:
        """Get the unique y-axis values as a list of floats."""
        return [float(y) for y in self.y_axis]

    def _toFloats(self) -> tuple[list[float], list[float]]:
        return (self.toX(), self.toY())

    def asVectors(self) -> tuple[vector, vector]:
        return (vector(data=self.toX()), vector(data=self.toY()))

    def mesh(self) -> tuple[list[list[float]], list[list[float]]]:
        x_grid = []
        y_grid = []
        for y in self.y_axis:
            x_row = []
            y_row = []
            for x in self.x_axis:
                x_row.append(float(x))
                y_row.append(float(y))
            x_grid.append(x_row)
            y_grid.append(y_row)
        return x_grid, y_grid
    

def linspace(start: Union[int, float, Decimal], stop: Union[int, float, Decimal], num: int) -> vector:
    """Generate a vector with linearly spaced values between start and stop.
    
    Args:
        start: starting value
        stop: ending value
        num: number of values to generate
    """
    if num <= 0:
        return vector()
    if num == 1:
        return vector(data=[start])
    
    start_d = _to_decimal(start)
    stop_d = _to_decimal(stop)
    step = (stop_d - start_d) / _to_decimal(num - 1)
    
    values = [start_d + step * _to_decimal(i) for i in range(num)]
    return vector(data=values)