# import libraries
import matplotlib.pyplot as plt
import gc
import numpy as np
from PIL import Image
from bokeh.layouts import gridplot
from bokeh.embed import components

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_x_fixation
from Data_bokeh import draw_dataframe
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph
from Gazestripes_bokeh import draw_gaze_stripes
from AOI_rivers_bokeh import draw_AOI_rivers
from Heat_Gaze_comb_bokeh import draw_heat_gaze_comb
from AOI_stimulus_bokeh import draw_AOI_stimulus


def draw_all_plots(user_name: str, name_map: str, check_vis, num_AOIs, data_set, string_folder):
    vis = []
    gc.collect()
    x_dat = get_x_fixation(user_name, name_map, data_set)

    image_source = string_folder + name_map
    img = plt.imread(image_source)
    im = Image.fromarray((img * 255).astype(np.uint8))
    x_dim, y_dim = im.size

    try:
        if x_dat:
            if "Data Table" in check_vis:
                datatable = draw_dataframe(user_name, name_map, data_set, True)
                script, div = components(datatable)
                return [script, div]
            if "Gaze Plot" in check_vis:
                gazeplot = draw_gazeplot(user_name, name_map, data_set, image_source, True)
                vis.append(gazeplot)
            if "Heatmap" in check_vis:
                heatmap = draw_heatmap(user_name, name_map, data_set, image_source, True)
                vis.append(heatmap)
            if "Heatmap + Gaze Plot" in check_vis:
                heat_gaze = draw_heat_gaze_comb(user_name, name_map, data_set, image_source, True)
                vis.append(heat_gaze)     
            if "Transition Graph" in check_vis:
                transition = draw_transition_graph(user_name, name_map, data_set, image_source,num_AOIs, True)
                vis.append(transition)
            if "Gaze Stripes" in check_vis:
                gazestripes = draw_gaze_stripes(user_name, name_map, data_set, image_source, True)
                vis.append(gazestripes)
            if "AOI Rivers" in check_vis:
                if user_name != "ALL":
                    return ["AOI rivers only displays data for all users", ""]
                else:
                    aoiriv = draw_AOI_rivers(user_name, name_map, num_AOIs, data_set, True)
                    vis.append(aoiriv)
            if "AOI Stimulus" in check_vis:
                AOI_stimulus = draw_AOI_stimulus(user_name, name_map, num_AOIs, data_set, image_source, True)
                vis.append(AOI_stimulus)               
            grid = gridplot(vis, ncols=1, plot_width=int(x_dim / 2.5), plot_height=int(y_dim / 2.5))

            script, div = components(grid)
            return [script, div]
        else:
            return ["No user data found", ""]
    except MemoryError as error:
        return ["A memory error occured, do not select to many data and plots at the same time", ""]
