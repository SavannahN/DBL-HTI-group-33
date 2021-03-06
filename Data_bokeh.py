# import libraries
import pandas as pd
from bokeh.plotting import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.embed import components

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_data_user, get_data_user_all_maps


def draw_dataframe(user_name: str, name_map: str, data_set: pd.DataFrame, multiple=False):
    if name_map == 'ALL':
        df = get_data_user_all_maps(user_name, data_set)
    else:
        df = get_data_user(user_name, name_map, data_set)

    df.sort_values(by=['StimuliName'], inplace=True)

    source = ColumnDataSource(df)
    columns = [
        TableColumn(field="Timestamp", title="Time Stamp"),
        TableColumn(field="StimuliName", title="Map"),
        TableColumn(field="FixationIndex", title="Fixation Index"),
        TableColumn(field="FixationDuration", title="Fixation Duration"),
        TableColumn(field="MappedFixationPointX", title="X Coordinate Fixation"),
        TableColumn(field="MappedFixationPointY", title="Y Coordinate Fixation"),
        TableColumn(field="user", title="Participant"),
        TableColumn(field="description", title="description"),
    ]

    data_table = DataTable(source=source, columns=columns)

    if not multiple:
        script, div = components(data_table)
        return [script, div]
    else:
        return data_table
