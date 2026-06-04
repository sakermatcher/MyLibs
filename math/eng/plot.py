import matplotlib.pyplot as plt
import seaborn as sb
from .vector import vector
from .vector import vector2D

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
    def __init__(self, x:vector, y:vector, u:vector, v:vector, x_label:str="X-axis", y_label:str="Y-axis", title:str="Quiver Plot", color:str=None, scale:float=None, angles:str="xy", scale_units:str="xy", width:float=None, showGrid:bool=True, heatmap:bool=False, heatmap_cmap:str="magma", heatmap_alpha:float=0.35, heatmap_levels:int=20):
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
            heatmap: whether to draw a magnitude heatmap behind the arrows and normalize arrow lengths
            heatmap_cmap: color map used for the magnitude heatmap ["viridis", "magma", "inferno", "plasma"]
            heatmap_alpha: transparency of the heatmap background
            heatmap_levels: number of contour levels used for the heatmap
        """
        self.x_data= x
        self.y_data= y
        self.u_data= u
        self.v_data= v

        # Normalize vector inputs early to validate dimensions with a clear error.
        self._x_values = x._toFloats() if isinstance(x, vector) else list(x)
        self._y_values = y._toFloats() if isinstance(y, vector) else list(y)
        self._u_values = u._toFloats() if isinstance(u, vector) else list(u)
        self._v_values = v._toFloats() if isinstance(v, vector) else list(v)

        lengths = {len(self._x_values), len(self._y_values), len(self._u_values), len(self._v_values)}
        if len(lengths) != 1:
            raise ValueError("x, y, u and v must have the same length")

        if color is None:
            color= getNextColor()
        self.color= color
        self.scale= scale
        self.angles= angles
        self.scale_units= scale_units
        self.width= width
        self.title= title
        self.showGrid= showGrid
        self.heatmap= heatmap
        self.heatmap_cmap= heatmap_cmap
        self.heatmap_alpha= heatmap_alpha
        self.heatmap_levels= heatmap_levels
        self.x_label= x_label
        self.y_label= y_label
        self._points= []
        self._level_curves= []

    def _to_float_list(self, values):
        if isinstance(values, vector):
            return values._toFloats()
        return [float(v) for v in values]

    def _field_magnitudes(self):
        return [(u ** 2 + v ** 2) ** 0.5 for u, v in zip(self._u_values, self._v_values)]

    def _heatmap_arrow_length(self):
        unique_x= sorted(set(self._x_values))
        unique_y= sorted(set(self._y_values))
        spacings= []

        if len(unique_x) > 1:
            x_steps= [right - left for left, right in zip(unique_x, unique_x[1:]) if right > left]
            if x_steps:
                spacings.append(min(x_steps))

        if len(unique_y) > 1:
            y_steps= [top - bottom for bottom, top in zip(unique_y, unique_y[1:]) if top > bottom]
            if y_steps:
                spacings.append(min(y_steps))

        if spacings:
            return min(spacings) * 0.8

        return 1.0

    def _normalized_field(self):
        magnitudes= self._field_magnitudes()
        arrow_length= self._heatmap_arrow_length()
        normalized_u= []
        normalized_v= []

        for u_value, v_value, magnitude in zip(self._u_values, self._v_values, magnitudes):
            if magnitude == 0:
                normalized_u.append(0)
                normalized_v.append(0)
            else:
                normalized_u.append((u_value / magnitude) * arrow_length)
                normalized_v.append((v_value / magnitude) * arrow_length)

        return magnitudes, normalized_u, normalized_v

    def addPoints(self, x:vector|list|vector2D, y:vector|list=None, label:str="", color:str=None, marker:str="o", size:float=30):
        """Adds scatter points to be displayed on top of the quiver field."""
        if isinstance(x, vector2D):
            x_values, y_values = x._toFloats()
        else:
            if y is None:
                raise ValueError("y values are required when x is not vector2D")
            x_values= self._to_float_list(x)
            y_values= self._to_float_list(y)
        if len(x_values) != len(y_values):
            raise ValueError("Points x and y must have the same length")
        if color is None:
            color= getNextColor()

        self._points.append({
            "x": x_values,
            "y": y_values,
            "label": label,
            "color": color,
            "marker": marker,
            "size": size
        })

    agregarPuntos= addPoints

    def addLevelCurves(self, x_grid, y_grid, z_values, levels=10, colors=None, linewidths:float=1.0, alpha:float=1.0, showLabels:bool=False):
        """Adds contour (level) curves to be displayed on top of the quiver field."""
        if colors is None:
            colors= getNextColor()

        self._level_curves.append({
            "x": x_grid,
            "y": y_grid,
            "z": z_values,
            "levels": levels,
            "colors": colors,
            "linewidths": linewidths,
            "alpha": alpha,
            "showLabels": showLabels
        })

    agregarCurvasDeNivel= addLevelCurves

    def show(self, block= True, show=True):
        """Displays the quiver plot."""
        if show:
            plt.figure()

        magnitudes= None
        u_values= self._u_values
        v_values= self._v_values

        if self.heatmap:
            magnitudes, u_values, v_values= self._normalized_field()
            if len(self._x_values) >= 3:
                heatmap= plt.tripcolor(
                    self._x_values,
                    self._y_values,
                    magnitudes,
                    shading="gouraud",
                    cmap=self.heatmap_cmap,
                    alpha=self.heatmap_alpha
                )
                plt.colorbar(heatmap, label="Magnitude")
            else:
                heatmap= plt.scatter(
                    self._x_values,
                    self._y_values,
                    c=magnitudes,
                    cmap=self.heatmap_cmap,
                    alpha=self.heatmap_alpha
                )
                plt.colorbar(heatmap, label="Magnitude")
            
            # Filter out zero magnitude arrows
            filtered_data = [(x, y, u, v) for x, y, u, v, m in zip(self._x_values, self._y_values, u_values, v_values, magnitudes) if m != 0]
            if filtered_data:
                filtered_x, filtered_y, filtered_u, filtered_v = zip(*filtered_data)
            else:
                filtered_x, filtered_y, filtered_u, filtered_v = [], [], [], []
        else:
            filtered_x, filtered_y, filtered_u, filtered_v = self._x_values, self._y_values, u_values, v_values

        kwargs= {
            "angles": self.angles,
            "scale_units": self.scale_units,
            "color": self.color
        }
        if self.scale is not None and not self.heatmap:
            kwargs["scale"]= self.scale
        elif self.heatmap:
            kwargs["scale"]= 1
            kwargs["scale_units"]= "xy"
        if self.width is not None:
            kwargs["width"]= self.width

        plt.quiver(filtered_x, filtered_y, filtered_u, filtered_v, **kwargs)

        has_labelled_points= False
        for points in self._points:
            plt.scatter(
                points["x"],
                points["y"],
                s=points["size"],
                c=points["color"],
                marker=points["marker"],
                label=points["label"] if points["label"] != "" else None
            )
            if points["label"] != "":
                has_labelled_points= True

        for curve in self._level_curves:
            contour = plt.contour(
                curve["x"],
                curve["y"],
                curve["z"],
                levels=curve["levels"],
                colors=curve["colors"],
                linewidths=curve["linewidths"],
                alpha=curve["alpha"]
            )
            if curve["showLabels"]:
                plt.clabel(contour, inline=True, fontsize=8)

        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(self.showGrid)
        if has_labelled_points:
            plt.legend()

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