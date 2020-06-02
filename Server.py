from flask import Flask, render_template, request, session, redirect
import pandas as pd

# visualization methods.
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph
from Gazestripes_bokeh import draw_gaze_stripes
from AOI_rivers_bokeh import draw_AOI_rivers
from AllPlots_bokeh import draw_all_plots
from Data_bokeh import draw_dataframe

# 'library' created by the team to help with he processing of the data
from HelperFunctions import drop_down_info

# Initialize the flask server and the encryption key for session data.
app = Flask(__name__)
app.secret_key = "pPAQaAI4lte5d8Hwci1i"

# Read the Fixation data, This should become a non static part of the code.
FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)
dict = {'KÃ¶ln':'Köln', 'BrÃ¼ssel':'Brüssel', 'DÃ¼sseldorf': 'Düsseldorf', 'GÃ¶teborg' : 'Göteborg', 'ZÃ¼rich': 'Zürich' }
df_data.replace(dict, regex=True, inplace=True)

# The visualization methods we support in this app.
LIST_VIS_ID = ["Data table", "Gazeplot", "Heatmap", "Transition graph", "Gaze Stripes", "AOI Rivers", "All tools"]

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["filename"]
            app.logger.info('testing info log')

            print(image)

            return redirect(request.url)


    return render_template("home.html")

@app.route("/", methods=["POST", "GET"])
def home():
    """

    :return: The web page to be renderd.
    """
    lists = drop_down_info(LIST_VIS_ID, df_data)
    if request.method == "POST":
        for ID in ["MapID", "UserID", "VisID"]:
            if request.form[ID]:
                session[ID] = request.form[ID]
            else:
                return render_template("home.html", session=[], LISTS=lists)

        if session["VisID"] == "Gazeplot":
            Graph = draw_gazeplot(session["UserID"], session["MapID"])

        elif session["VisID"] == "Data table":
            Graph = draw_dataframe(session["UserID"], session["MapID"])

        elif session["VisID"] == "Heatmap":
            Graph = draw_heatmap(session["UserID"], session["MapID"])

        elif session["VisID"] == "Transition graph":
            Graph = draw_transition_graph(session["UserID"], session["MapID"])

        elif session["VisID"] == "Gaze Stripes":
            Graph = draw_gaze_stripes(session["UserID"], session["MapID"])
        
        elif session["VisID"] == "AOI Rivers":
            Graph = draw_AOI_rivers(session["UserID"], session["MapID"], 7)    

        elif session["VisID"] == "All tools":
            Graph = draw_all_plots(session["UserID"], session["MapID"])

        return render_template("home.html", session=session, LISTS=lists, Graph=Graph)
    else:
        return render_template("home.html", session=[], LISTS=lists)


@app.route("/help/")
def help():
    """

    :return: The web page to be renderd.
    """
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=False)
