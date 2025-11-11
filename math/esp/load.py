from pandas import read_csv, read_excel, read_json
import pandas as pd
from sak.math.eng.vector import vector

class load:
    def __init__(self, filepath: str, type: str = "xlsx"):
        """
        Inicializa la clase de importación con la ruta del archivo.
        filepath: ruta al archivo que se desea importar
        type: tipo de archivo ('csv', 'xlsx', 'json')
        """
        self.filepath = filepath
        self.type = type.lower()
        if self.type == "csv":
            self.data = read_csv(f"{self.filepath}.{self.type}")
        elif self.type == "xlsx":
            self.data = read_excel(f"{self.filepath}.{self.type}")
        elif self.type == "json":
            self.data = read_json(f"{self.filepath}.{self.type}")
        else:
            raise ValueError("Tipo de archivo no soportado. Tipos permitidos: csv, xlsx, json.")
        
    def show(self):
        """
        Muestra los datos importados.
        """
        print(self.data)

    mostrar= show

    def toVec(self, col: 'int|str' = "a", row: int = 1, stop: int = None) -> vector:
        """
        Devuelve una columna de los datos como un vector.
        col: índice de columna a extraer (índice entero o etiqueta de columna / letras estilo Excel)
        row: índice de fila inicial (comenzando en 1)
        stop: índice de fila final opcional (comenzando en 1, inclusivo). Si se proporciona,
              la iteración se detiene cuando el índice de la fila actual excede `stop`.
        """
        vals = []
        i = row - 1

        # Validate stop parameter when provided
        if stop is not None:
            try:
                stop = int(stop)
            except Exception:
                raise ValueError("stop debe ser un entero o None")
            if stop < row:
                raise ValueError("stop debe ser mayor o igual que row")

        # Helper: convert Excel-style letters (A, B, ..., Z, AA, AB, ...) to zero-based index
        def letters_to_index(s: str) -> int | None:
            if not s:
                return None
            s = s.upper()
            total = 0
            for ch in s:
                if not ('A' <= ch <= 'Z'):
                    return None
                total = total * 26 + (ord(ch) - ord('A') + 1)
            return total - 1

        # Accept either a column index (int) or a column label (str).
        # Stop when we hit the end of the dataframe or exceed the stop row (if set).
        while i < len(self.data) and (stop is None or (i + 1) <= stop):
            try:
                if isinstance(col, int):
                    val = self.data.iloc[i, col]
                else:
                    # Prefer exact header match first (preserves existing behavior when headers are 'A','B', etc.)
                    if col in self.data.columns:
                        col_idx = self.data.columns.get_loc(col)
                    else:
                        # Try case-insensitive header match
                        col_upper = str(col).upper()
                        matches = [c for c in self.data.columns if str(c).upper() == col_upper]
                        if matches:
                            col_idx = self.data.columns.get_loc(matches[0])
                        else:
                            # Try Excel-style letter(s) -> index
                            letter_idx = letters_to_index(str(col))
                            if letter_idx is None:
                                raise KeyError(f"Columna '{col}' no encontrada")
                            col_idx = letter_idx
                    val = self.data.iloc[i, col_idx]
            except IndexError:
                # row/col out of range -> stop iteration
                break
            if pd.isna(val):
                break
            vals.append(val)
            i += 1
        return vector(data=vals)
        
    aVector= toVec
