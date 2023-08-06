import webbrowser
import os
import numpy as np
import pandas as pd
from collections import OrderedDict
# flask libraries
from flask import Flask, request, render_template, url_for, redirect, send_from_directory
import flask
# from flask_bootstrap import Bootstrap
import json
from stats_tools import tools
from stats_tools import table
import seaborn as sns
from scipy.cluster.vq import kmeans, vq
import uuid
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from plotting.altarian import altair_monovariate_bar, altair_monovariate_hist, altair_bivariate
import pandas_profiling
import re
from io import BytesIO
import base64

class Output():
    """output operation"""
    def __init__(self):
        pass

    monovariate_plot_session = {}
    script = ""
    crosstab_session = {}

    def monovariate_plot(self, request, dataset):
        r = request
        g = r.form.getlist('monovariate')
        options_tipo_var = r.form["var_type"]
        #options_ordinal_list = r.form["ordinal_list"]
        options_drop = r.form["drop_missing"]

        self.monovariate_plot_session = {
            "g": g,
            "options_tipo_var": options_tipo_var,
            #'options_categorical_list': options_ordinal_list
        }

        if options_drop == "drop":
            dataset.dropna(subset=[g[0]], inplace=True)
        elif options_drop == "no_drop":
            pass

        unique_values = dataset[g[0]].unique()
        series = dataset[g[0]]

        data = table.dist_frequenza(dataset,
                                    g[0],
                                    save=False,
                                    tipo=options_tipo_var)

        if options_tipo_var == "cardinale":
            dataset_cardinale = dataset.round(2)
            data = table.dist_frequenza(dataset_cardinale,
                                        g[0],
                                        save=False,
                                        tipo=options_tipo_var)



        data_non_tot = data.drop("Totale")
        datatest = pd.DataFrame({"X": data_non_tot.index.values,
                                 "Frequency": data_non_tot["Frequenze"].values})

        if options_tipo_var == "likert":
            options_categorical_list = ["1", "2", "3", "4", "5"]
            data = table.dist_frequenza(dataset,
                                    g[0],
                                    save=False,
                                    tipo="ordinale",
                                    lista_ordinale=[1,2,3,4,5])


            data_non_tot = data.drop("Totale")

            dataset_dist_plot = pd.DataFrame({"X": data_non_tot.index.values,
                                              "Frequency": data_non_tot["Frequenze"].values})
            dataset_dist_plot.dropna(inplace=True)
            dataset_dist_plot.set_index(dataset_dist_plot["X"], inplace=True)
            dataset_dist_plot.index = dataset_dist_plot.index.map(str)
            dataset_dist_plot = dataset_dist_plot.loc[options_categorical_list]
            dataset_dist_plot.fillna(0, inplace = True)
            dataset_dist_plot.X = dataset_dist_plot.index
            print(dataset_dist_plot)

        try:
            gini = tools.gini(series)
        except:
            gini = np.nan

        equilibrium_values = tools.Sq_output(datatest["Frequency"])
        if options_tipo_var == "cardinale":
            characteristic_values = {
                "mean": series.mean(),
                "standard deviation": series.std(),
                "gini index": str(gini)

            }

        elif options_tipo_var == "categoriale":
            characteristic_values = {
                "mode": datatest[datatest["Frequency"] == datatest["Frequency"].max()]["X"].values[0],
                "total equilibrium": datatest["Frequency"].sum() / len(datatest["Frequency"].unique()),
                "Sq": equilibrium_values["Sq"],
                "Sq_norm": equilibrium_values["Sq_Norm"],
                "Eq": equilibrium_values["Eq"]

            }

        elif options_tipo_var == "likert":
            characteristic_values = {
                "mean": series.mean(),
                "standard deviation": series.std(),
                "gini index": str(gini),
                "mode": datatest[datatest["Frequency"] == datatest["Frequency"].max()]["X"].values[0],
                "total equilibrium": datatest["Frequency"].sum() / len(datatest["Frequency"].unique()),
                "Sq": equilibrium_values["Sq"],
                "Sq_norm": equilibrium_values["Sq_Norm"],
                "Eq": equilibrium_values["Eq"]

            }

        print(options_tipo_var)
        if options_tipo_var == "categoriale" or options_tipo_var == "ordinale":
            chart = altair_monovariate_bar(data=datatest, options_tipo_var=options_tipo_var, lista_ordinale=False)
            print(chart.to_json())
        elif options_tipo_var == "likert":
            chart = altair_monovariate_bar(data=dataset_dist_plot, options_tipo_var=options_tipo_var,
                                           lista_ordinale=options_categorical_list)

            print(chart.to_json())
        elif options_tipo_var == "cardinale":
            print(dataset[g[0]])
            dataset_hist = dataset.round(2)
            chart = altair_monovariate_hist(dataset_hist, g[0])
            print(chart.to_json())

        return render_template("monovariate/monovariate_plot.html",
                               operation_form=g,
                               chart_json=chart.to_json(),
                               data=data.to_html(classes="table table-striped"),
                               unique_values=unique_values,
                               options_tipo_var=options_tipo_var,
                               characteristic_values=characteristic_values
                               )

    def monovariate_plot_sorted(self, dataset):
        g = self.monovariate_plot_session["g"]
        options_tipo_var = self.monovariate_plot_session["options_tipo_var"]
        options_categorical_list = self.monovariate_plot_session["option_categorical_list"]
        dataset = dataset
        unique_values = dataset[g[0]].unique()

        data = table.dist_frequenza(dataset,
                                    g[0],
                                    save=False,
                                    tipo="categoriale",
                                    lista_ordinale=options_categorical_list)

        data_non_tot = data.drop("Totale")

        dataset_dist_plot = pd.DataFrame({"X": data_non_tot.index.values,
                                 "Frequency": data_non_tot["Frequenze"].values})
        dataset_dist_plot.dropna(inplace=True)
        dataset_dist_plot.set_index(dataset_dist_plot["X"], inplace=True)
        dataset_dist_plot.index = dataset_dist_plot.index.map(str)
        dataset_dist_plot = dataset_dist_plot.loc[options_categorical_list]

        equilibrium_values = tools.Sq_output(dataset_dist_plot["Frequency"])
        if options_tipo_var == "cardinale":
            characteristic_values = {
                "mean": dataset_dist_plot["Frequency"].mean(),
                "standard deviation": dataset_dist_plot["Frequency"].std(),
                "gini index": tools.gini(dataset_dist_plot["Frequency"].values)

            }

        if options_tipo_var == "categoriale":
            characteristic_values = {
                "mode": dataset_dist_plot[dataset_dist_plot["Frequency"] == dataset_dist_plot["Frequency"].max()]["X"].values[0],
                "total equilibrium": dataset_dist_plot["Frequency"].sum() / len(dataset_dist_plot["Frequency"].unique()),
                "Sq": equilibrium_values["Sq"],
                "Sq_norm": equilibrium_values["Sq_Norm"],
                "Eq": equilibrium_values["Eq"]

            }
        print(options_categorical_list)
        chart = altair_monovariate_bar(data=dataset_dist_plot, options_tipo_var=options_tipo_var,
                                       lista_ordinale=options_categorical_list)



        return render_template("monovariate/monovariate_plot.html",
                               operation_form=g,
                               chart_json=chart.to_json(),
                               data=data.to_html(classes="table table-striped"),
                               unique_values=unique_values, options_tipo_var=options_tipo_var,
                               characteristic_values=characteristic_values)

    def bivariate_plot(self, request, dataset):
        g = request
        g_x = g.form.getlist('bivariate_x')[0]
        g_y = g.form.getlist('bivariate_y')[0]
        g_hue = "empty"

        print(g_x, g_y)
        data = dataset


        correlation = data[[g_x, g_y]].corr()

        chart = altair_bivariate(dataset, g_x, g_y)

        script = g.form["textarea_script"]
        print(script)
        plt.figure()

        x_result = script.split('x="')[1].split('"')[0]
        y_result = script.split('y="')[1].split('"')[0]
        print(len(x_result))
        print(len(y_result))

        if len(x_result) > 35 or len(y_result) > 35:
            try:
                hue_result = script.split('hue="')[1].split('"')[0]
                data_reduced = data[[x_result,y_result, hue_result]]
                data_reduced.columns = ["x", "y", "hue"]
                result = sns.lmplot(x="x",y="y",data=data_reduced,hue="hue")
                g_hue = g.form.getlist('bivariate_hue')[0]

                #chart = altair_bivariate_hue(data_reduced, "x", "y", "hue")
            except:
                data_reduced = data[[x_result, y_result]]
                data_reduced.columns = ["x", "y"]
                result = sns.jointplot(x="x", y="y", data=data_reduced, kind="reg")

        else:
            result = eval(script, {'data': data, "pd": pd, "sns": sns})



        figfile = BytesIO()
        plt.savefig(figfile, format="png")
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = base64.b64encode(figfile.getvalue())
        plt.figure()

        return render_template("bivariate/bivariate_plot.html",
                               operation_form=[g_x, g_y, g_hue],
                               chart_json=chart.to_json(),
                               correlation=correlation.to_html(classes="table table-striped"),
                               #img_link=img_link,
                               img=figdata_png.decode('utf8'))

    def cluster_output(self, request, dataset, selected_file_link):
        data = dataset

        nome_var = request.form["new_var_name"]
        script = request.form["textarea_script"]
        self.script = script
        result = eval(script, {'data': data, "pd": pd, "vq": vq, "kmeans": kmeans})
        data_select = data[result[0]]
        data_select.dropna(inplace=True)
        data_select = data_select.applymap(float)

        data_values = data_select.values

        centroids, _ = kmeans(data_values, result[1])
        # assign each sample to a cluster
        idx, _ = vq(data_values, centroids)
        data_select[nome_var] = idx
        output = pd.concat([data_select[nome_var], data], axis=1)
        plt.figure()
        variabile = eval(script)[0]
        if len(variabile) == 2:

            c = output[nome_var]

            for classes in c.unique():
                output_temp = output[output[nome_var] == classes]
                x = output_temp[variabile[0]]
                y = output_temp[variabile[1]]

                result = sns.scatterplot(x=x, y=y, data=output_temp, cmap="tab20c", label=classes)
                result.legend()


            figfile = BytesIO()
            plt.savefig(figfile, format="png")
            figfile.seek(0)  # rewind to beginning of file
            figdata_png = base64.b64encode(figfile.getvalue())

        elif len(variabile) == 3:


            c = output[nome_var]


            result = plt.axes(projection='3d')
            for classes in c.unique():
                output_temp = output[output[nome_var] == classes]
                x = output_temp[variabile[0]]
                y = output_temp[variabile[1]]
                z = output_temp[variabile[2]]

                result.scatter3D(x, y, z, cmap="tab20c", label=classes)
                result.legend()

            figfile = BytesIO()
            plt.savefig(figfile, format="png")
            figfile.seek(0)  # rewind to beginning of file
            figdata_png = base64.b64encode(figfile.getvalue())
        else:
            img_link = ""
        output.to_excel(selected_file_link, index=False)
        output = output.to_html(table_id="result_data")
        plt.figure()


        return render_template("cluster/cluster_output.html", data=output, img=figdata_png.decode('utf8'))

    def ncrosstab_output(self, request, dataset):
        try:
            script = request.form["textarea_script"]
            index_series = request.form["textarea_script_index"]
            columns_series = request.form["textarea_script_columns"]
            self.script = script
            self.index_series = index_series
            self.columns_series = columns_series
        except:
            script = self.script
        data = dataset
        result = eval(script, {'data': data, "pd": pd})


        '''
        index = script.split("index=[")[1].split("]],")[0]
        columns = script.split("columns=[")[1].split("]],")[0]
        print(index, columns)
        '''
        try:
            print(result.index.nlevels)
            self.crosstab_session["ncrosstab_classification_index"] = result.index.nlevels
        except:
            pass
        try:
            print(result.columns.nlevels)
            self.crosstab_session["ncrosstab_classification_columns"] = result.columns.nlevels

        except:
            pass

        if result.index.nlevels == 1 & result.columns.nlevels == 1:
            abilitate_tipology = "abilitate"
            stacked = result.stack().reset_index().rename(columns={0: 'value'})
            print(stacked)
            result_img = sns.barplot(x=stacked.columns[0], y=stacked.columns[2], hue=stacked.columns[1], data=stacked)

            figfile = BytesIO()
            plt.savefig(figfile, format="png")
            figfile.seek(0)  # rewind to beginning of file
            figdata_png = base64.b64encode(figfile.getvalue())
        else:
            abilitate_tipology = "disabilitate"
            img_link = ""

        self.crosstab_session["ncrosstab_output"] = result.to_html(classes="draggable", table_id="corr_tab")
        self.crosstab_session["ncrosstab_output_margin"] = "pass"
        self.crosstab_session["crosstab_output_descriptive"] = "pass"

        return render_template("crosstab/crosstab_output.html",
                               table=result.to_html(classes="draggable",
                                                    table_id="corr_tab"),
                               abilitate_tipology=abilitate_tipology,
                               img=figdata_png.decode('utf8'))

    def ncrosstab_classification(self):
        result = self.crosstab_session["ncrosstab_output"]
        ncrosstab_classification_index = self.crosstab_session["ncrosstab_classification_index"]
        ncrosstab_classification_columns = self.crosstab_session["ncrosstab_classification_columns"]
        return render_template("crosstab/crosstab_classification.html",
                               table=result,
                               classification_index=ncrosstab_classification_index,
                               classification_columns=ncrosstab_classification_columns
                               )

    def ncrosstab_classification_ouput(self, dataset, selected_file_link):
        dataset.to_excel(selected_file_link, index=False)
        return render_template("crosstab/crosstab_classification_output.html",
                               table= dataset.to_html(table_id = "result_data"))

    def recode_output(self, request, obj_elab):
        g = request.values.to_dict()
        new_var_name = g["new_variabile_name"]
        print(g)
        recode_var = obj_elab.recode_var

        print(recode_var[0])
        dataset = obj_elab.dataset
        def recode(dictionary, x):
            try:
                return dictionary[x]
            except:
                return x

        dataset[new_var_name] = dataset[recode_var[0]].apply(lambda x: recode(g, str(x)))
        dataset.to_excel(obj_elab.selected_file_link, index=False)
        output = dataset.to_html(table_id="result_data")
        return render_template("cluster/cluster_output.html", data=output)

    def calc_output(self, request, dataset):
        g = request
        print(g.form)
        dataset = g.form["dataset"]
        data = pd.read_excel("./static/uploads/" + dataset)
        result = eval(g.form["formula"], {'data': data})

        if g.form["new_variabile"] == "":
            if isinstance(result, pd.Series):
                return eval(g.form["formula"], {'data': data}).to_frame().to_html(classes="table table-striped")
            elif not isinstance(result, pd.Series):
                return eval(g.form["formula"], {'data': data})
        else:
            data[g.form["new_variabile"]] = eval(g.form["formula"], {'data': data})
            dataset = g.form["dataset"]
            data.to_excel("./static/uploads/" + dataset)
            # return "<h> nuova variabile </h>" + data[g.form["new_variabile"]].to_frame().to_html()
            output = pd.concat([data[g.form["new_variabile"]], data], axis=1)

            output = output.to_html(table_id="result_data")
            return render_template("calc_output.html", data=output)

    def profiling_output(self, obj_elab):
        data = obj_elab.dataset
        # profile = data.profile_report(title=flask.session["selected_file"])
        profile = pandas_profiling.ProfileReport(data)
        print(dir(profile))
        profile.title = obj_elab.selected_file
        profile.to_file(output_file="./templates/profiling.html")
        return render_template("profiling.html")


class Operation():
    def __init__(self):
        pass

    recode_session = {}
    def load(self, request, obj_elab):
        g = request
        dataset = obj_elab.load(g)
        html_data = dataset.head(500).to_html(table_id="head_data",
                                              classes="table table-striped table-bordered display nowrap")
        return render_template("select_action.html",
                               selected_file=obj_elab.selected_file,
                               html_data=html_data)

    def recode_operation(self, request, obj_elab):
        g = request.form.getlist('recode_var')
        self.recode_session["recode_var"] = g
        obj_elab.recode_var = g

        dataset = obj_elab.dataset
        unique_values = dataset[g[0]].unique()

        data = table.dist_frequenza(dataset,
                                    g[0],
                                    save=False,
                                    tipo="categoriale")

        return render_template("recode/recode_operation.html",
                               operation_form=g,
                               data=data.to_html(classes="table table-striped"),
                               unique_values=unique_values,

                               )

    def post_arrive(request, obj_elab):
        posted = request.get_json()['category_order']
        recode = posted
        try:
            data = obj_elab.dataframe
            import numpy as np
            data["type_" + recode['vary'] + "_" + recode['varx']] = np.nan

            def set_typo(row, recode):
                for item in recode['dataframe']:
                    if (row[recode['varx']] == item['categoryx']) & (row[recode['vary']] == item['categoryy']):
                        print(row[recode['varx']] == item['categoryx'], row[recode['varx']], item['categoryx'],
                              row[recode['vary']], item['categoryy'], item["value"])
                        return item["value"]
                    else:
                        pass

            data["type_" + recode['vary'] + "_" + recode['varx']] = data.apply(lambda row: set_typo(row, recode),
                                                                               axis=1)
            obj_elab.dataset = data
            data.to_excel(obj_elab.selected_file)
            return "executed: you can find the new variabile in the last columns of dataframe"
        except:
            return "error.. somethings wrong"

    def create_subset(self, dataset):
        selection = request.values.to_dict()
        new_filename = selection['new_filename']
        del selection['new_filename']
        new_filename = str(new_filename) + ".xlsx"
        columns = selection.keys()
        dataset_subset = dataset[columns]
        dataset_subset.to_excel("./static/uploads/" + new_filename, index = False)
        files = os.listdir("./static/uploads/")
        return render_template("index.html", files=files, upload="true")


class Elab():
    """
    Main class

    """

    def __init__(self):
        pass
    #variabile
    selected_file = "no_file"
    action_to_file = "no_action"
    variable_name_type = OrderedDict()
    variable_name_type_obj = OrderedDict()
    dataset = ""
    option_categorical_list = ""
    monovariate_plot_session = ""
    selected_file_link = ""
    #inner classes
    output = Output()
    operation = Operation()

    def load(self, request, descriptions):
        g = request
        self.selected_file = g.form["load"]
        self.action_to_file = g.form["file_config"]
        self.selected_file_link = "./static/uploads/" + self.selected_file
        self.variable_name_type = {}
        self.variable_name_type_obj = {}
        self.variable_name_type_only_obj = {}

        if g.form["file_config"] == "remove":
            os.remove("./static/uploads/" + g.form["load"])
            files = os.listdir("./static/uploads/")
            return render_template("index.html", files=files, upload="removed")
        else:
            if g.form["file_config"] == "standard_excel":
                #flask.session["selected_file"] = g.form["load"]
                dataset = pd.read_excel("./static/uploads/" + g.form["load"])
            elif g.form["file_config"] == "excel_google_form":
                dataset = pd.read_excel("./static/uploads/" + g.form["load"])
                dataset = dataset.applymap(lambda x: tools.google_form_likert(x))
                dataset.to_excel("./static/uploads/" + "__gform__" + g.form["load"])
                #flask.session["selected_file"] = "__gform__" + g.form["load"]
            elif g.form["file_config"] == "csv1":
                dataset = pd.read_csv("./static/uploads/" + g.form["load"], sep=";")
                dataset.to_excel("./static/uploads/" + g.form["load"] + ".xlsx")
                #flask.session["selected_file"] = g.form["load"] + ".xlsx"
            elif g.form["file_config"] == "csv2":
                dataset = pd.read_csv("./static/uploads/" + g.form["load"], sep=",")
                dataset.to_excel("./static/uploads/" + g.form["load"] + ".xlsx")
                #flask.session["selected_file"] = g.form["load"] + ".xlsx"
            elif g.form["file_config"] == "create_subset":
                #flask.session["selected_file"] = g.form["load"]
                dataset = pd.read_excel("./static/uploads/" + g.form["load"])
                self.variable_name_type.update(dataset.dtypes.to_dict(into=OrderedDict))
                self.dataset = dataset
                return render_template("create_subset.html", columns=self.variable_name_type)
            elif g.form["file_config"] == "join_dataset":
                pass
            else:
                pass

            self.variable_name_type.update(dataset.dtypes.to_dict(into=OrderedDict))
            self.variable_name_type_obj.update(dataset.loc[:, (dataset.dtypes != "object").values].dtypes.to_dict(into=OrderedDict))
            self.variable_name_type_only_obj.update(dataset.loc[:, (dataset.dtypes == "object").values].dtypes.to_dict(into=OrderedDict))
            self.dataset = dataset
            html_data = dataset.head(500).to_html(table_id="head_data",
                                                  classes="table table-striped table-bordered display nowrap")
            self.html_data = html_data
            return render_template("select_action.html",
                                   selected_file=self.selected_file,
                                   html_data=html_data,
                                   descriptions = descriptions)





