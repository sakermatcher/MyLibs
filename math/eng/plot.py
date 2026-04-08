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

def pause(time:int|float):
    """Pauses the execution for a given time in seconds."""
    plt.pause(time)

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
        initializes a figure with given subplots.
        
        Args:
            ots: 2D list of plot objects to arrange in the figure.
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
        """Displays the figure with its subplots."""
        plt.figure()
        plotIndex= 1
        for y, row in enumerate(self.subPlots):
            for p in row:
                plt.subplot(self.sizeY, self.sizeX, plotIndex)
                p.show(block= False, show= False)
                plotIndex+= 1
            plotIndex= (y+1)*self.sizeX + 1
        plt.show(block= block)

    mostrar= show

class figure(fig):
    pass

class plotHeatMap:
    def __init__(self, values:list[list[float]], x_labels:list[str]=None, y_labels:list[str]=None, title:str="Heat Map", showVals:bool=True, cmap:str="viridis", showGrid:bool=True):
        """
        initializes a heat map with given data and styling options.

        Args:
            values: 2D list of values for the heat map
            x_labels: labels for the x-axis
            y_labels: labels for the y-axis
            title: title of the heat map
            cmap: color map to use
            showGrid: whether to show grid lines
        """
        self.values= values
        self.x_labels= x_labels
        self.y_labels= y_labels
        self.cmap= cmap
        self.title= title
        self.showGrid= showGrid
        self.showVals= showVals
    
    def show(self, block= True, show=True):
        """Displays the heat map."""
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
        initializes a box plot with given data and styling options.

        Args:
            values: vector of y-coordinates
            x_label: label for the x-axis
            y_label: label for the y-axis
            title: title of the box plot
            color: color of the box
            showGrid: whether to show grid lines
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
        """Displays the box plot."""
        if show:
            plt.figure()
        if type(self.y_data) is vector:
            yData= self.y_data._toFloats()
        else:
            yData= self.y_data
        plt.boxplot(yData, patch_artist= True, boxprops=dict(facecolor=self.color))
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
        initializes a plot line with given data and styling options.

        Args:
            x: vector of x-coordinates
            y: vector of y-coordinates
            x_label: label for the x-axis
            y_label: label for the y-axis
            title: title of the plot
            label: label for the plot line
            color: color of the plot line
            type: type of plot ('l' for line, 's' for scatter, etc.)
            pointTypes: marker style for points (if applicable)
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
        self.plot= None

    def addData(self, x:vector, y:vector, label:str="", color:str=None, type:str='l', pointTypes:str=""):
        """
        adds another data set to the plot line.

        Args:
            x: vector of x-coordinates
            y: vector of y-coordinates
            label: label for the new data set
            color: color of the new data set
            type: type of plot ('l' for line, 's' for scatter, etc.)
            pointTypes: marker style for points (if applicable)
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

    aggregarDatos= addData

    def changeData(self, index:int, x:vector, y:vector, label:str="", color:str=None, type:str='', pointTypes:str=""):
        """
        changes an existing data set in the plot line.

        Args:
            index: index of the data set to change
            x: new vector of x-coordinates
            y: new vector of y-coordinates
        """
        if label != "":
            self.labels[index]= label
        if color is not None:
            self.colors[index]= color
        if type != '':
            self.types[index]= type
        if pointTypes != "":
            self.pointTypes[index]= pointTypes
        
        self.x_data[index]= x
        self.y_data[index]= y

    def show(self, block= True, show=True, figure:int=0):
        """Displays the plot line."""
        if show:
            plt.figure(figure)
            # clear previous contents so repeated calls redraw a fresh frame
            plt.clf()
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
            if block:
                plt.close()

    mostrar= show

class plotQuiver:
    def __init__(self, x:vector, y:vector, u:vector, v:vector, x_label:str="X-axis", y_label:str="Y-axis", title:str="Quiver Plot", color:str=None, scale:float=None, angles:str="xy", scale_units:str="xy", width:float=None, showGrid:bool=True):
        """
        initializes a quiver plot with given vector field data and styling options.

        Args:
            x: vector of x-coordinates for arrow origins
            y: vector of y-coordinates for arrow origins
            u: vector of x-components for arrows
            v: vector of y-components for arrows
            x_label: label for the x-axis
            y_label: label for the y-axis
            title: title of the plot
            color: color for arrows
            scale: scaling factor for arrow length
            angles: angle mode for arrows
            scale_units: unit mode used with scale
            width: shaft width of arrows
            showGrid: whether to show grid lines
        """
        self.x_data= x
        self.y_data= y
        self.u_data= u
        self.v_data= v
        if color is None:
            color= getNextColor()
        self.color= color
        self.scale= scale
        self.angles= angles
        self.scale_units= scale_units
        self.width= width
        self.title= title
        self.showGrid= showGrid
        self.x_label= x_label
        self.y_label= y_label

    def show(self, block= True, show=True):
        """Displays the quiver plot."""
        if show:
            plt.figure()

        if type(self.x_data) is vector:
            xData= self.x_data._toFloats()
        else:
            xData= self.x_data
        if type(self.y_data) is vector:
            yData= self.y_data._toFloats()
        else:
            yData= self.y_data
        if type(self.u_data) is vector:
            uData= self.u_data._toFloats()
        else:
            uData= self.u_data
        if type(self.v_data) is vector:
            vData= self.v_data._toFloats()
        else:
            vData= self.v_data

        kwargs= {
            "angles": self.angles,
            "scale_units": self.scale_units,
            "color": self.color
        }
        if self.scale is not None:
            kwargs["scale"]= self.scale
        if self.width is not None:
            kwargs["width"]= self.width

        plt.quiver(xData, yData, uData, vData, **kwargs)
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(self.showGrid)

        if show:
            plt.show(block= block)
            plt.close()

    mostrar= show

class plotBar:
    def __init__(self, names:list[str], y:vector, x_label:str="", y_label:str="", title:str="Bar Plot", color:str=None, showGrid:bool=True):
        """
        initializes a bar plot with given data and styling options.
        
        Args:
            names: names for each bar
            y: vector of y-coordinates
            label: label for the bar plot
            color: color of the bars
            showGrid: whether to show grid lines
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
        """Displays the bar plot."""
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
        initializes a pie chart with given data and styling options.

        Args:
            names: names for each slice
            values: vector of values for each slice
            title: title of the pie chart
            colors: list of colors for the slices
        """
        self.names= names
        self.values= values
        if colors is None:
            colors= [getNextColor() for _ in range(len(names))]
        self.colors= colors
        self.title= title

    def show(self, block= True, show=True):
        """Displays the pie chart."""
        if show:
            plt.figure()
        
        plt.pie(self.values, labels=self.names, colors=self.colors, autopct='%1.1f%%')
        plt.title(self.title)

        if show:
            plt.show(block= block)
            plt.close()
            
    mostrar= show