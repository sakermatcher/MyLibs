import matplotlib.pyplot as plt
import seaborn as sb
from .vector import vector

onColor= 0
colors = [
    "#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#A833FF",
    "#33FFF6", "#FF8F33", "#8FFF33", "#338FFF", "#FF3333",
    "#33FF8F", "#8F33FF", "#33A8FF", "#FFA833", "#A8FF33",
    "#33FFA8", "#A833A8", "#F633FF", "#33F6FF", "#FF3366",
    "#66FF33", "#3366FF", "#FF6633", "#33FF66", "#6633FF",
    "#33CCFF", "#CC33FF", "#FF33CC", "#33FFCC", "#FFCC33",
    "#33CC66", "#66CC33", "#CC6633", "#3366CC", "#6633CC",
    "#CC3366", "#66FFCC", "#CCFF66", "#FF66CC", "#66CCFF",
    "#CC66FF", "#FFCC66", "#66CC99", "#99CC66", "#CC9966",
    "#6699CC", "#9966CC", "#CC6699", "#99FF66", "#6699FF"
]

def getNextColor():
    global onColor
    color = colors[onColor]
    onColor += 1
    if onColor >= len(colors):
        onColor = 0
    return color

class fig:
    def __init__(self, subPlots:list[list]):
        """
        Inicializa una figura con los subgráficos indicados.
        subPlots: Lista 2D de objetos de gráfico para organizar en la figura.
        """
        if type(subPlots[0]) is not list:
            subPlots= [subPlots]
        self.subPlots= subPlots
        self.sizeY= len(subPlots)
        self.sizeX= 0
        for row in subPlots:
            if len(row) > self.sizeX:
                self.sizeX= len(row)

    def show(self, block= True):
        """Muestra la figura con sus subgráficos."""
        plt.figure()
        plotIndex= 1
        for y, row in enumerate(self.subPlots):
            for p in row:
                plt.subplot(self.sizeY, self.sizeX, plotIndex)
                p.show(block= False, show= False)
                plotIndex+= 1
            plotIndex= (y+1)*self.sizeX + 1
        plt.show(block= block)
        plt.close()

    mostrar= show

figure= fig

class plotHeatMap:
    def __init__(self, values:list[list[float]], x_labels:list[str]=None, y_labels:list[str]=None, title:str="Heat Map", showVals:bool=True, cmap:str="viridis", showGrid:bool=True):
        """
        Inicializa un mapa de calor con los datos y opciones de estilo indicados.
        values: Lista 2D de valores para el mapa de calor.
        x_labels: Etiquetas del eje X.
        y_labels: Etiquetas del eje Y.
        title: Título del mapa de calor.
        showVals: Si se deben mostrar los valores en cada celda.
        cmap: Mapa de colores a usar.
        showGrid: Indica si se muestran las líneas de la cuadrícula.
        """
        self.values= values
        self.x_labels= x_labels
        self.y_labels= y_labels
        self.cmap= cmap
        self.title= title
        self.showGrid= showGrid
        self.showVals= showVals
    
    def show(self, block= True, show=True):
        """Muestra el mapa de calor."""
        if show:
            plt.figure()
        sb.heatmap(self.values, xticklabels=self.x_labels, yticklabels=self.y_labels, cmap=self.cmap, annot=self.showVals)
        plt.title(self.title)
        plt.grid(self.showGrid)

        if show:
            plt.show(block= block)
            plt.close()
    
    mostrar= show

class plotBox:
    def __init__(self, values:vector, x_label:str="X-axis", y_label:str="Y-axis", title:str="Box Plot", color:str=None, showGrid:bool=True):
        """
        Inicializa un diagrama de caja (boxplot) con los datos y opciones de estilo indicados.
        values: Vector con los valores (eje Y).
        x_label: Etiqueta del eje X.
        y_label: Etiqueta del eje Y.
        title: Título del gráfico.
        color: Color de la caja.
        showGrid: Indica si se muestran las líneas de la cuadrícula.
        """
        self.y_data= values
        if color is None:
            color= getNextColor()
        self.color= color
        self.title= title
        self.showGrid= showGrid
        self.x_label= x_label
        self.y_label= y_label

    def show(self, block= True, show=True):
        """Muestra el diagrama de caja (boxplot)."""
        if show:
            plt.figure()
        plt.boxplot(self.y_data.toFloats(), patch_artist= True, boxprops=dict(facecolor=self.color))
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(self.showGrid)

        if show:
            plt.show(block= block)
            plt.close()
        
    mostrar= show

class plotLine:
    def __init__(self, x:vector, y:vector, x_label:str="X-axis", y_label:str="Y-axis", title:str="Plot", label:str="", color:str=None, type:str='l', pointTypes:str="", showGrid:bool=True):
        """
        Inicializa una gráfica con línea y/o puntos con los datos y opciones de estilo indicados.
        x: Vector de coordenadas X.
        y: Vector de coordenadas Y.
        label: Etiqueta de la serie.
        color: Color de la serie.
        type: Tipo de gráfico ('l' para línea, 's' para dispersión, etc.).
        pointTypes: Estilo del marcador para los puntos (si aplica).
        """
        self.x_data= [x]
        self.y_data= [y]
        if label== "":
            label= y.name
        self.labels= [label]
        self.types= [type]
        if color is None:
            color= getNextColor()
        self.colors= [color]
        self.pointTypes= [pointTypes]
        self.title= title
        self.showGrid= showGrid
        self.x_label= x_label
        self.y_label= y_label

    def addData(self, x:vector, y:vector, label:str="", color:str=None, type:str='l', pointTypes:str=""):
        """
        Agrega otro conjunto de datos a la gráfica.
        x: Vector de coordenadas X.
        y: Vector de coordenadas Y.
        label: Etiqueta de la nueva serie.
        color: Color de la nueva serie.
        type: Tipo de gráfico ('l' para línea, 's' para dispersión, etc.).
        pointTypes: Estilo del marcador para los puntos (si aplica).
        """
        self.x_data.append(x)
        self.y_data.append(y)
        if label== "":
            label= y.name
        self.labels.append(label)
        self.types.append(type)
        if color is None:
            color= getNextColor()
        self.colors.append(color)
        self.pointTypes.append(pointTypes)
    
    agregarDatos= addData

    def show(self, block= True, show=True):
        """Muestra la gráfica con línea y/o puntos."""
        if show:
            plt.figure()
        for i in range(len(self.x_data)):
            if self.types[i] == 'l':
                plt.plot(self.x_data[i], self.y_data[i], label=self.labels[i], color=self.colors[i])
            elif self.types[i] == 's':
                plt.scatter(self.x_data[i], self.y_data[i], label=self.labels[i], color=self.colors[i], marker=self.pointTypes[i] if self.pointTypes[i] != "" else 'o')
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.legend(self.labels)
        plt.grid(self.showGrid)

        if show:
            plt.show(block= block)
            plt.close()

    mostrar= show

class plotBar:
    def __init__(self, names:list[str], y:vector, x_label:str="", y_label:str="", title:str="Bar Plot", color:str=None, showGrid:bool=True):
        """
        Inicializa un gráfico de barras con los datos y opciones de estilo indicados.
        names: Nombres/etiquetas para cada barra.
        y: Vector de valores (altura de cada barra).
        x_label: Etiqueta del eje X.
        y_label: Etiqueta del eje Y.
        title: Título del gráfico.
        color: Color de las barras.
        showGrid: Indica si se muestran las líneas de la cuadrícula.
        """
        self.names= names
        self.y_data= y
        if color is None:
            color= getNextColor()
        self.color= color
        self.title= title
        self.showGrid= showGrid
        self.x_label= x_label
        self.y_label= y_label

    def show(self, block= True, show=True):
        """Muestra el gráfico de barras."""
        if show:
            plt.figure()
        plt.bar(self.names, self.y_data, color=self.color)
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(self.showGrid)

        if show:
            plt.show(block= block)
            plt.close()
    
    mostrar= show

class plotPie:
    def __init__(self, names:list[str], values:vector, title:str="Pie Chart", colors:list[str]=None):
        """
        Inicializa un gráfico de pastel con los datos y opciones de estilo indicados.
        names: Nombres/etiquetas para cada porción.
        values: Vector de valores para cada porción.
        title: Título del gráfico de pastel.
        colors: Lista de colores para las porciones.
        """
        self.names= names
        self.values= values
        if colors is None:
            colors= [getNextColor() for _ in range(len(names))]
        self.colors= colors
        self.title= title

    def show(self, block= True, show=True):
        """Muestra el gráfico de pastel."""
        if show:
            plt.figure()
        plt.pie(self.values, labels=self.names, colors=self.colors, autopct='%1.1f%%')
        plt.title(self.title)

        if show:
            plt.show(block= block)
            plt.close()

    mostrar= show