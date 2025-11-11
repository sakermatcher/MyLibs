from __future__ import annotations
from decimal import Decimal
from typing import overload, Sequence, Optional, Union


def _to_decimal(x):
    """Convierte int/float/Decimal a Decimal (usa la representación en cadena para los float y preservar el valor)."""
    if isinstance(x, Decimal):
        return x
    if isinstance(x, int):
        return Decimal(x)
    if isinstance(x, float):
        return Decimal(str(x))
    raise ValueError("Solo se permiten valores int, float o Decimal")


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
        Crea una instancia de vector.

        - Sin argumentos: vector vacío
        - 1 argumento: stop (incluyente)
        - 2 argumentos: start, stop (incluyente)
        - 3 argumentos: start, stop, step (incluyente)

        También puedes proporcionar datos desde una lista con el método .addData().
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
            raise ValueError("El valor de step no puede ser cero")

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
                raise ValueError("los vectores deben tener la misma longitud")
            return vector(data=[a + b for a, b in zip(self.vec, other.vec)])
        raise ValueError("El parámetro 'other' debe ser int|float|Decimal|vector")

    def __sub__(self, other: int | float | Decimal | "vector") -> "vector":
        if isinstance(other, (int, float, Decimal)):
            other_d = _to_decimal(other)
            return vector(data=[x - other_d for x in self.vec])
        if isinstance(other, vector):
            if len(self.vec) != len(other.vec):
                raise ValueError("los vectores deben tener la misma longitud")
            return vector(data=[a - b for a, b in zip(self.vec, other.vec)])
        raise ValueError("El parámetro 'other' debe ser int|float|Decimal|vector")

    def __mul__(self, other: int | float | Decimal | "vector") -> "vector":
        if isinstance(other, (int, float, Decimal)):
            other_d = _to_decimal(other)
            return vector(data=[x * other_d for x in self.vec])
        if isinstance(other, vector):
            if len(self.vec) != len(other.vec):
                raise ValueError("los vectores deben tener la misma longitud")
            return vector(data=[a * b for a, b in zip(self.vec, other.vec)])
        raise ValueError("El parámetro 'other' debe ser int|float|Decimal|vector")

    def __div__(self, other: int | float | Decimal | "vector") -> "vector":
        if isinstance(other, (int, float, Decimal)):
            other_d = _to_decimal(other)
            return vector(data=[x / other_d for x in self.vec])
        if isinstance(other, vector):
            if len(self.vec) != len(other.vec):
                raise ValueError("los vectores deben tener la misma longitud")
            return vector(data=[a / b for a, b in zip(self.vec, other.vec)])
        raise ValueError("El parámetro 'other' debe ser int|float|Decimal|vector")

    def __truediv__(self, other: int | float | Decimal | "vector") -> "vector":
        return self.__div__(other)

    def __getitem__(self, s: slice | int):
        if isinstance(s, int):
            return self.vec[s]
        return vector(data=list(self.vec[s]))

    def sum(self) -> Decimal:
        """Devuelve la suma de los elementos del vector."""
        return sum(self.vec, Decimal(0))
    
    suma= sum
    
    def diff(self) -> "vector":
        """Devuelve las diferencias entre elementos consecutivos como un nuevo vector."""
        if len(self.vec) < 2:
            return vector()
        diffs = [self.vec[i+1] - self.vec[i] for i in range(len(self.vec)-1)]
        return vector(data=diffs)
    
    def addInfo(self, name="") -> None:
        """Añade un nombre o descripción al vector."""
        self.name= name

    def find(self, value: int | float | Decimal) -> int | None:
        """Busca el índice de un valor en el vector. Devuelve None si no se encuentra."""
        try:
            value_d = _to_decimal(value)
            return self.vec.index(value_d)
        except Exception:
            return None
        
    encontrar= find
        
    def addData(self, data:list|tuple) -> None:
        """Añade varios valores al final del vector desde una lista o tupla."""
        for item in data:
            self.append(item)
    
    agregarDatos= addData

    def append(self, obj: int | float | Decimal) -> None:
        """Añade un valor al final del vector."""
        if isinstance(obj, (int, float, Decimal)):
            self.vec.append(_to_decimal(obj))
        else:
            raise ValueError("Solo se permiten valores int, float y Decimal en el vector")

    def combine(self, other: "vector") -> "vector":
        """Combina dos vectores en un nuevo vector por concatenación."""
        if not isinstance(other, vector):
            raise ValueError("El parámetro 'other' debe ser un vector")
        return vector(data=(self.vec + other.vec))
    
    combinar= combine
    
    def toFloats(self) -> list[float]:
        """Convierte los elementos del vector a una lista de floats."""
        return [float(x) for x in self.vec]