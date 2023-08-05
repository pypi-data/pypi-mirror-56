import matplotlib.pyplot as plt
import rawpy
import numpy as np
import pandas
from skimage.color import rgb2grey
from skimage.morphology import disk
from skimage.filters.rank import mean

indexAlpha = np.array(["a","b",'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
             'aa','bb','cc','dd','ee','ff','gg','hh','ii','jj','kk','ll','mm','nn','oo'])


class Image(object):
    def __init__(self, image, name=None):
        self.image = image
        self.processed_image = None
        self.brightness= None
        self.name = name
        self.sections = {}

    def __str__(self):
        return "<Image: " + self.name + ">"

    def process_image(self, color=rawpy.ColorSpace(0)):
        self.processed_image = rgb2grey(self.image.postprocess(output_color=color))

    def select_points(self, name, shape="rectangle", rows=None, columns=None, column_start=0, row_start=0, points = []):
        """ Creates a section object and appends it to the sections list
         Parameters
         ------------
         name: str
            The name of the section
        shape: str
            The shape of the section
        rows: int
            The number of rows in the selection
        columns: int
            The number of columns in the selction
        """

        if self.processed_image is None:
            self.process_image()
        if points == []:
            fig, ax = plt.subplots()
            ax.imshow(self.processed_image)

            def onclick(event):
                if event.button == 3:
                    if points == []:
                        points.append([event.xdata, event.ydata])
                        print(points)
                    else:
                        coords = [event.xdata, event.ydata]
                        close_points = np.sum(np.power(np.subtract(points, coords), 2), axis=-1) < 500
                        print(close_points)
                        if close_points.any():
                            print(np.where(close_points)[0][0])
                            del points[np.where(close_points)[0][0]]
                        else:
                            points.append([event.xdata, event.ydata])
                            print(points)
                    plt.clf()
                    plt.imshow(self.processed_image)
                    plt.scatter(np.array(points)[:, 0],  np.array(points)[:, 1])
                    fig.canvas.draw()

            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            plt.show()
        if not rows:
            rows = input("How many rows are there in the selection")
        if not columns:
            columns = input("How many columns are there in the selection")
        print(points)

        self.sections[name] = Section(vertexes=points,
                                      rows=rows,
                                      columns=columns,
                                      name=name,
                                      shape=shape,
                                      row_start=row_start,
                                      column_start=column_start)
        print(self.sections[name])

    def get_all_positions(self):
        positions = {}
        for key in self.sections.keys():
            positions[key] = self.sections[key].get_indexes()
        return positions

    def show(self):
        plt.imshow(self.processed_image)
        xy = self.get_all_positions()
        d = np.array([data_dict for sect in xy.values() for data_dict in sect.values.flatten()])
        plt.scatter(d[:, 0], d[:, 1])
        print((d[0, 0], d[1, 0]))

    def get_segmented(self, pixels=20):
        positions = self.get_all_positions()
        segmented_images = {}
        for section in positions.keys():
            segmented_images[section] = positions[section]
            for row_name, row in positions[section].iterrows():
                for col_name, index in row.items():
                    segmented_images[section].loc[row_name][col_name] = self.processed_image[
                                                                        int(index[1])-pixels:int(index[1])+pixels,
                                                                        int(index[0])-pixels:int(index[0])+pixels]
        return segmented_images

    def plot_intensities(self,pixels=20, type="smooth_max"):
        xy = self.get_all_positions()
        d = np.array([data_dict for sect in xy.values() for data_dict in sect.values.flatten()])
        c = self.get_values(pixels=pixels, type=type)
        c = np.array([data_dict for sect in c.values() for data_dict in sect.values.flatten()])
        print(d)
        plt.scatter(d[:, 0], d[:, 1], c=c)
        plt.imshow(self.processed_image, cmap="gray")
        plt.show()

    def get_values(self, pixels=20, type="max", output="Intensities.txt"):
        """Analyze the segments and return some value for the segements.

        Parameters:
        --------------
        pixels: int
            The number of pixels to search from the zero point to get the value from
        type: str
            Either max,
        :param type:
        :param output:
        :return:
        """

        seg = self.get_segmented(pixels=pixels)
        values = {}

        if type is "max":
            for key in seg.keys():
                values[key] = seg[key]
                for row_name, row in seg[key].iterrows():
                    for col_name, image in row.items():
                        values[key].loc[row_name][col_name] = np.max(image)
        if type is "smooth_max":
            selem = disk(2)
            for key in seg.keys():
                values[key] = seg[key]
                for row_name, row in seg[key].iterrows():
                    for col_name, image in row.items():
                        values[key].loc[row_name][col_name] = np.max(mean(image, selem))
        if output is not None:
            with open(self.name+output, "w") as f:
                for key in values.keys():
                    f.write("\n"+key+"\n")
                    f.write(values[key].to_string())
        return values

    def set_references(self):
        """ Set a reference to be saved with the image and applied when certain methods are preformed.
        """
        return


class Section(object):
    def __init__(self, vertexes, rows, columns, name, shape, row_start=0, column_start=0):
        self.vertexes = vertexes
        self.row_start = row_start
        self.col_start = column_start
        self.rows = rows
        self.columns = columns
        self.name = name
        self.shape = shape

    def __str__(self):
        return "<Sections: " + str(self.name) + "| (" + str(self.rows)+"," + str(self.columns) + ">"

    def get_indexes(self):
        if self.shape == "rectangle":
            points = np.array(self.vertexes)
            v1 = (points[1] - points[0]) / (self.rows - 1)
            v2 = (points[2] - points[0]) / (self.columns - 1)
            print(v1)
            print(v2)
            positions =pandas.DataFrame(data=None,
                                        index = indexAlpha[range(self.row_start,self.row_start+self.rows)],
                                        columns=range(self.col_start,self.col_start+self.columns))
            for i in range(self.rows):
                for j in range(self.columns):
                    positions.iloc[i, j] = (j * v2 + i * v1 + points[0])

        if self.shape == "triangle":
            points = np.array(self.vertexes)
            v1 = (points[1] - points[0]) / (self.rows - 1)
            v2 = (points[2] - points[0]) / (self.columns - 1)
            positions =pandas.DataFrame(data=None,
                                        index = indexAlpha[range(self.row_start,self.row_start+self.rows)],
                                        columns=range(self.col_start,self.col_start+self.cols))
            for i in range(self.rows):
                for j in range(self.columns- i):
                    positions.iloc[i, j] = (j * v2 + i * v1 + points[0])

        return positions


