from pandas import read_csv, read_excel, read_json
import pandas as pd
from sak.math.eng.vector import vector

class load:
    def __init__(self, filepath: str, type: str = "xlsx"):
        """
        Initializes the import class with the given file path.
        filepath: path to the file to be imported
        type: type of the file ('csv', 'xlsx', 'json')
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
            raise ValueError("Unsupported file type. Supported types are: csv, xlsx, json.")
        
    def show(self):
        """
        Displays the imported data.
        """
        print(self.data)

    mostrar= show

    def toVec(self, col: 'int|str' = "a", row: int = 1, stop: int = None) -> vector:
        """
        Returns a column of the data as a vector.
        col: column index to extract (int index or column label / Excel-style letter(s))
        row: starting row index (1-based)
        stop: optional ending row index (1-based, inclusive). If provided, iteration
              stops when the current row index would exceed `stop`.
        """
        vals = []
        i = row - 1

        # Validate stop parameter when provided
        if stop is not None:
            try:
                stop = int(stop)
            except Exception:
                raise ValueError("stop must be an integer or None")
            if stop < row:
                raise ValueError("stop must be greater than or equal to row")

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
                                raise KeyError(f"Column '{col}' not found")
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