sak.math (Documentación en Español)
===================================

Resumen
-------
`sak.math` es una librería ligera de apoyo numérico y de gráficos construida sobre `decimal`, `pandas`, `matplotlib` y `seaborn`. Proporciona:

* Una clase `vector` precisa (almacena internamente valores `Decimal`) con operaciones aritméticas, slicing y utilidades.
* Importación de datos mediante `load` (alias: `imp`, `cargar`) para CSV / XLSX / JSON con conversión directa de columnas a vectores.
* Funciones basadas en expresiones (`fx`) y regresión polinómica (`polyfit`).
* Primitivas de graficación rápidas: línea, dispersión (scatter), barras, caja (box), pastel (pie), mapa de calor (heat map) y figuras con múltiples sub–gráficos.
* Aliases en español expuestos en `esp` y algunos sinónimos bilingües dentro de `eng` (por ejemplo `mostrar`).

Instalación
-----------

```powershell
pip install matplotlib seaborn pandas
```

----------------------
Usar la API en inglés:

```python
import sak.math.eng as sak
```

O la API en español:

```python
import sak.math.esp as sak
```

Inicio Rápido
-------------
```python
import sak.math.esp as sak  # o eng

# Importar hoja de cálculo y extraer columnas B y C (filas 6..83 inclusive)
data = sak.imp("tests", type="xlsx")
t = data.toVec("B", 6, 83)
x = data.toVec("C", 6, 83)

# Ajuste polinómico (grado 2) y evaluación
pol = sak.polyfit(t, x, 2)
y = pol.calc(t)

# Graficar original vs curva ajustada
p = sak.plotLine(t, x, title="Gráfica de Prueba", x_label="Valores T", y_label="Valores X", color="green")
p.addData(t, y, label="Ajuste")
p.show()
```

Conceptos Clave
---------------
### Precisión y Decimal
Todos los valores numéricos dentro de `vector` y los generados por `fx` / `polyfit` se almacenan como `Decimal` para reducir la deriva de coma flotante. Al graficar, los valores se convierten a floats de Python.

### Vectores
Crear rangos o desde datos crudos:
```python
v1 = sak.vec(10)            # 0..10 inclusivo, paso 1
v2 = sak.vec(2, 5)          # 2..5 inclusivo, paso 1
v3 = sak.vec(0, 11, 0.1)    # 0..11 inclusivo, paso 0.1
v4 = sak.vec(data=[3, 6, 9]) # elementos explícitos
```
La aritmética es elemento a elemento (las longitudes deben coincidir):
```python
v_sum = v1 + 2
v_mix = v2 + v4            # lanza excepción si las longitudes difieren
diffs = v3.diff()
total = v4.sum()
idx = v4.find(6)           # devuelve índice o None
```
El slicing devuelve un nuevo vector: `v_part = v3[10:20]`.

### Importación de Datos (`load` / `imp` / `cargar`)
```python
dataset = sak.cargar("mydata", type="xlsx")
```
```python
colA = dataset.toVec("A", 2, 40)        # Letras de columnas estilo Excel
colPorIdx = dataset.toVec(1, 2, 40)      # índice de columna base cero
```
Las letras de columna se traducen (A, B, ..., Z, AA, AB...). También puedes usar nombres de encabezado exactos (no distinguen mayúsculas/minúsculas). Se detiene al encontrar un valor en blanco/NaN o al exceder la fila `stop`.

### Funciones (`fx`)
Construye desde una expresión en cadena. Operadores soportados: `+ - * / ^` y trigonometría (`sin`, `cos`, `tan`), `log`, `sqrt`, constantes `e`, `pi`. La trigonometría puede estar en grados (por defecto) o radianes.
```python
f = sak.fx("-0.2x^2 + 2.4x + 22.8")
g = sak.fx("sin(x) + 3", degRad="rad")
val = f.calc(4)
y_vals = f.calc(v3)          # devuelve vector
```
Puedes pasar constantes nombradas: `f.calc(v3, A=2, B=5)` si tu ecuación usa `A`, `B`.

### Ajuste Polinómico (`polyfit`)
Regresión polinómica de mínimos cuadrados que retorna una instancia `fx`.
```python
poly = sak.polyfit(t, x, 2)
pred = poly.calc(t)
```
Lanza excepción si las longitudes difieren, si el grado < 0, o si el sistema es singular (raro: puntos x idénticos con restricciones conflictivas).

Graficación
-----------
Los colores rotan automáticamente. Cada objeto de gráfica tiene `.show(block=True)` y alias en español `.mostrar`.

### Línea / Dispersión (`plotLine`)
```python
p = sak.plotLine(t, x, title="Ejemplo", x_label="Tiempo", y_label="Valor", type='l')
p.addData(t, y, label="Ajuste", type='l')
p.show()
```
Parámetros:
* `x`, `y`: vectores
* `type`: 'l' (línea) o 's' (dispersión)
* `pointTypes`: marcador cuando es dispersión
* `addData(...)` añade series adicionales

### Mapa de Calor (`plotHeatMap`)
```python
hm = sak.plotHeatMap(values=[[1,2],[3,4]], x_labels=["A","B"], y_labels=["F1","F2"], title="Calor")
hm.show()
```
`showVals=True` anota las celdas; `cmap` cualquier cadena de colormap de matplotlib.

### Gráfico de Caja (`plotBox` / `graficaCaja`)
```python
bp = sak.graficaCaja(sak.vec(data=[5,7,8,6,9]), title="Distribución")
bp.mostrar()
```

### Barras (`plotBar` / `graficaBarras`)
```python
bars = sak.graficaBarras(["A","B","C"], sak.vec(data=[10,5,7]), title="Conteos")
bars.mostrar()
```

### Pastel (`plotPie` / `graficaPastel`)
```python
pie = sak.graficaPastel(["Cat A","Cat B"], sak.vec(data=[60, 40]), title="Participación")
pie.mostrar()
```

### Figuras con Múltiples Sub–gráficos (`fig` / `figure` / `figura`)
Organiza objetos de gráfica en una cuadrícula 2D:
```python
fig = sak.figura([
	[hm, p],
	[bp, pie]
])
fig.mostrar()
```

Referencia de la API
--------------------
### vector
Formas del constructor:
* `vec(stop)` → rango 0..stop
* `vec(start, stop)` → paso 1
* `vec(start, stop, step)`
* `vec(data=[...])` provee elementos explícitos

Métodos clave: `suma()`, `diff()`, `encontrar(value)`, `agregarDatos(list)`, `append(val)`, `combinar(other)`, `toFloats()`, slicing `v[a:b]`.
Operadores: `+ - * /` con escalar o vector de igual longitud.

### load / imp / cargar
`cargar(filepath: str, type: 'csv'|'xlsx'|'json')` – lee `filepath.<type>`.
`toVec(col, row=1, stop=None)` – extracción de columna; `col` puede ser int, nombre de encabezado, o letras.

### fx
`fx(equation: str, degRad='deg')` – construye expresión. Usa `calc(x)` o alias `eval(x)` donde `x` es escalar o vector.
Constantes/trig se envuelven automáticamente en `radians()` cuando `degRad='deg'`.

### polyfit
`polyfit(x: vector, y: vector, degree: int) -> fx` – polinomio de mínimos cuadrados (retorna un `fx`).

### plotLine / graficaLinea
`plotLine(x: vector, y: vector, x_label='X-axis', y_label='Y-axis', title='Plot', label='', color=None, type='l', pointTypes='', showGrid=True)`
Añadir series: `addData(x, y, label='', color=None, type='l', pointTypes='')`.

### plotHeatMap / graficaMapaCalor
`plotHeatMap(values, x_labels=None, y_labels=None, title='Heat Map', showVals=True, cmap='viridis', showGrid=True)`.

### plotBox / graficaCaja
`plotBox(values: vector, x_label='X-axis', y_label='Y-axis', title='Box Plot', color=None, showGrid=True)`.

### plotBar / graficaBarras
`plotBar(names: list[str], y: vector, x_label='', y_label='', title='Bar Plot', color=None, showGrid=True)`.

### plotPie / graficaPastel
`plotPie(names: list[str], values: vector, title='Pie Chart', colors=None)`.

### fig / figure / figura
`fig(subPlots: list[list])` – disposición 2D; cualquier lista interna es una fila. `.show()` renderiza todo.

Aliases e Internacionalización
------------------------------
Equivalentes en español disponibles (ejemplos): `imp`/`cargar`, `mostrar`, `graficaLinea`, `graficaMapaCalor`, `graficaCaja`, `graficaBarras`, `graficaPastel`, `figura`.

Manejo de Errores y Casos Especiales
------------------------------------
* `vector(step=0)` lanza `ValueError`.
* Desajuste de longitud en aritmética de vectores o `polyfit` lanza `ValueError`.
* Matriz singular durante `polyfit` lanza `ValueError("Matrix is singular...")`.
* `load` con `type` no soportado lanza `ValueError`.
* `toVec` se detiene en el primer NaN o cuando se supera `stop`.
* `fx.calc` lanza excepción si `x` no es escalar ni `vector`.

Notas de Rendimiento
--------------------
`polyfit` usa eliminación Gaussiana ingenua (O(n^3) en el grado). Adecuado para grados pequeños (típico <= 6). Para conjuntos de datos grandes o grados altos considera integrar NumPy.

Ideas de Extensibilidad
-----------------------
* Añadir resúmenes estadísticos (media, mediana, desviación estándar) a `vector`.
* Proveer backend opcional con NumPy para velocidad.
* Añadir utilidades de guardar/exportar para gráficas.

Ejemplo Completo (Combinado)
----------------------------
```python
import sak.math.esp as sak

data = sak.imp("tests", type="xlsx")
t = data.toVec("B", 6, 83)
x = data.toVec("C", 6, 83)
pol = sak.polyfit(t, x, 2)
y = pol.calc(t)

p_line = sak.plotLine(t, x, title="Datos vs Ajuste", x_label="t", y_label="x")
p_line.addData(t, y, label="Ajuste Cuadrático")

hm = sak.plotHeatMap(values=[[1,2,3],[3,2,1],[2,3,4]], x_labels=["A","B","C"], y_labels=["F1","F2","F3"], title="Patrón")
box = sak.plotBox(sak.vec(data=[5,7,8,6,9,5]), title="Dispersión")
pie = sak.plotPie(["Cat A","Cat B","Cat C"], sak.vec(data=[15,30,55]))

fig = sak.figure([
	[hm, p_line],
	[box, pie]
])
fig.show()
```
