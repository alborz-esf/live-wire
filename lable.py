import plotly
import plotly.express as px
import plotly.graph_objects as go
from skimage import measure
from PIL import Image
import os
import numpy as np
import pandas as pd
from tkinter import filedialog
import sys
from skimage.measure import regionprops_table


class make_feature:
    def __init__(self) -> None:
        self.labels =None
        self.img = None
        self.mask = None
        self.current_directory = os.getcwd()
        self.properties = ['area', 'eccentricity', 'perimeter', 'intensity_mean',
                                                            'orientation',
                                                            'axis_major_length',
                                                            'axis_minor_length']

    def read_images(self):

        first_image_filename = None
        second_image_filename = None

        first_image_filename = filedialog.askopenfilename(
                                            title="Select the first image file (the image)",
                                            initialdir=self.current_directory)
        if first_image_filename == "":
            sys.exit()
            
        second_image_filename = filedialog.askopenfilename(
                                            title="Select the second image file (the mask)",
                                            initialdir=self.current_directory)
        if second_image_filename == "":
            sys.exit()

        self.img = None
        self.mask = None

        self.img = Image.open(first_image_filename)
        self.img = self.img.convert('L')
        w, h = self.img.size
        resize_factor = max(w,h)/480
        self.img = self.img.resize((int(w//resize_factor),int(h//resize_factor)))
        self.img = np.array(self.img)

        self.mask = Image.open(second_image_filename)
        self.mask = self.mask.convert('L')
        self.mask = self.mask.resize((int(w//resize_factor),int(h//resize_factor)))
        self.mask = np.array(self.mask)
        self.mask = self.mask > 150
        print(f'=============> images loaded')

    def make_prop(self):
        
        self.labels = measure.label(self.mask)
        self.props = measure.regionprops(self.labels, self.img)
        print(f'=============> props created')

    def draw_plot(self):

        fig = px.imshow(self.mask, binary_string=True)
        fig.update_traces(hoverinfo='skip')
        # fig = go.Figure()
        # fig.add_trace(go.Image(z=self.mask))

        for index in range(0, self.labels.max()):
            label_i = self.props[index].label
            contour = measure.find_contours(self.labels == label_i, 0.5)[0]
            y, x = contour.T
            hoverinfo = ''
            for prop_name in self.properties:
                hoverinfo += f'<b>{prop_name}: {getattr(self.props[index], prop_name):.2f}</b><br>'
            fig.add_trace(go.Scatter(
                x=x, y=y, name=label_i,
                mode='lines', fill='toself', showlegend=False,
                hovertemplate=hoverinfo, hoveron='points+fills'))

        plotly.io.show(fig)
        self.draw_plot_2()
        # pyo.plot(fig, filename='C:/Users/albor/Downloads/output.html', auto_open=False)
        print(f'=============> plot drawn')

    def make_table_of_features(self):

        props_pd = regionprops_table(self.labels, properties=('label','centroid',
                                                 'orientation',
                                                 'axis_major_length',
                                                 'axis_minor_length', 'eccentricity', 'perimeter', 'area'))
                                                
        print(props_pd)
        res_df = pd.DataFrame(props_pd)
        res_df.to_csv('C:/Users/albor/Downloads/output.csv', index=False)
        print(f'=============> table created')


if __name__ == "__main__": 
    obj = make_feature()
    obj.read_images()
    obj.make_prop()
    obj.draw_plot()
    obj.make_table_of_features()