import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys

vsc_results_path = '/home/daan/Documents/Masterproef/masterproef/VSC results/'
basis_path = "0-basis/"
standard_path = "1-standard/"
ii_path = "2-iterative_intervals/"
swi_path = "3-sampling_with_iteration/"
fs_path = "4-full_sampling/"
its_path = "inf-to-sus/"

section_colors= ["#eda189", "#bfacd6", "#c7b526", "#25c9ae"]
threads_colors = ["#542e71", "#fb3640", "#fdca40", "#a799b7"]
comparison_section_colors= ["#ef476f", "#06d6a0", "#118ab2", "#ffd166"]
approach_colors = ["#FDAA10","#14B37D","#64afff","#1f4397", "#FF9999", "#C20000"]


#---------- BASIS ----------

def basis_all():
    df = pd.read_csv(vsc_results_path + "/0-basis/all_1.csv")
    df.index += 1
    df = df.div(1000000)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_all_runtime_sections',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=section_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def basis_opt():
    df = pd.read_csv(vsc_results_path + "/0-basis/opt_1.csv")
    df.index += 1
    df = df.div(1000000)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_opt_runtime_sections',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=section_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def basis_infected():
    df = pd.read_csv(vsc_results_path + "0-basis/basis_all_1/Successful runs/1/2021-04-22-20:15:41/infected.csv", header=None)
    df.index += 1
    df = df.T # Transpose dataframe
    df.columns = ["all-to-all"]

    '''
    df2 = pd.read_csv(vsc_results_path + "0-basis/basis_opt_1/Successful runs/1/2021-04-22-17:52:43/infected.csv", header=None)
    df2.index += 1
    df2 = df2.T # Transpose dataframe
    df2.columns = ["inf-to-sus"]
    df["inf-to-sus"] = df2["inf-to-sus"]
    '''
    print(df)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_infected',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Infected people",
        font_size=40,
        legend_title=None,
        showlegend=False,
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis_range=[0,800000]
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def basis_all_parallel_infector():
    all1 = pd.read_csv(vsc_results_path + "/0-basis/all_1.csv")
    all1.index += 1
    all1 = all1.div(1000000)

    all2 = pd.read_csv(vsc_results_path + "/0-basis/all_2.csv")
    all2.index += 1
    all2 = all2.div(1000000)

    all4 = pd.read_csv(vsc_results_path + "/0-basis/all_4.csv")
    all4.index += 1
    all4 = all4.div(1000000)

    all8 = pd.read_csv(vsc_results_path + "/0-basis/all_8.csv")
    all8.index += 1
    all8 = all8.div(1000000)

    df = pd.DataFrame()
    df['1'] = all1['Infector']
    df['2'] = all2['Infector']
    df['4'] = all4['Infector']
    df['8'] = all8['Infector']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_all_parallel_infector',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=threads_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title="Threads",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis_range=[0,240],
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def basis_opt_parallel_infector():
    opt1 = pd.read_csv(vsc_results_path + "/0-basis/opt_1.csv")
    opt1.index += 1
    opt1 = opt1.div(1000000)

    opt2 = pd.read_csv(vsc_results_path + "/0-basis/opt_2.csv")
    opt2.index += 1
    opt2 = opt2.div(1000000)

    opt4 = pd.read_csv(vsc_results_path + "/0-basis/opt_4.csv")
    opt4.index += 1
    opt4 = opt4.div(1000000)

    opt8 = pd.read_csv(vsc_results_path + "/0-basis/opt_8.csv")
    opt8.index += 1
    opt8 = opt8.div(1000000)

    df = pd.DataFrame()
    df['1'] = opt1['Infector']
    df['2'] = opt2['Infector']
    df['4'] = opt4['Infector']
    df['8'] = opt8['Infector']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_opt_parallel_infector',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=threads_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title="Threads",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis_range=[0,2],
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def basis_all_parallel_updating():
    all1 = pd.read_csv(vsc_results_path + "/0-basis/all_1.csv")
    all1.index += 1
    all1 = all1.div(1000000)

    all2 = pd.read_csv(vsc_results_path + "/0-basis/all_2.csv")
    all2.index += 1
    all2 = all2.div(1000000)

    all4 = pd.read_csv(vsc_results_path + "/0-basis/all_4.csv")
    all4.index += 1
    all4 = all4.div(1000000)

    all8 = pd.read_csv(vsc_results_path + "/0-basis/all_8.csv")
    all8.index += 1
    all8 = all8.div(1000000)

    df = pd.DataFrame()
    df['1'] = all1['Updating']
    df['2'] = all2['Updating']
    df['4'] = all4['Updating']
    df['8'] = all8['Updating']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_parallel_updating',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=threads_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title="Threads",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def basis_opt_parallel_updating():
    opt1 = pd.read_csv(vsc_results_path + "/0-basis/opt_1.csv")
    opt1.index += 1
    opt1 = opt1.div(1000000)

    opt2 = pd.read_csv(vsc_results_path + "/0-basis/opt_2.csv")
    opt2.index += 1
    opt2 = opt2.div(1000000)

    opt4 = pd.read_csv(vsc_results_path + "/0-basis/opt_4.csv")
    opt4.index += 1
    opt4 = opt4.div(1000000)

    opt8 = pd.read_csv(vsc_results_path + "/0-basis/opt_8.csv")
    opt8.index += 1
    opt8 = opt8.div(1000000)

    df = pd.DataFrame()
    df['1'] = opt1['Updating']
    df['2'] = opt2['Updating']
    df['4'] = opt4['Updating']
    df['8'] = opt8['Updating']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_parallel_updating',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=threads_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title="Threads",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def basis():
    basis_all()
    basis_opt()
    basis_all_parallel_infector()
    basis_opt_parallel_infector()
    basis_all_parallel_updating()
    basis_opt_parallel_updating()

#---------- STANDARD ----------

def standard_all():
    df = pd.read_csv(vsc_results_path + standard_path + "all_1.csv")
    df.index += 1
    df = df.div(1000000)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_all_runtime_sections',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=section_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def standard_opt():
    df = pd.read_csv(vsc_results_path + standard_path + "opt_1.csv")
    df.index += 1
    df = df.div(1000000)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_opt_runtime_sections',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=section_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def standard_all_parallel_infector():
    t1 = pd.read_csv(vsc_results_path + standard_path + "all_1.csv")
    t1.index += 1
    t1 = t1.div(1000000)

    t2 = pd.read_csv(vsc_results_path + standard_path + "all_2.csv")
    t2.index += 1
    t2 = t2.div(1000000)

    t4 = pd.read_csv(vsc_results_path + standard_path + "all_4.csv")
    t4.index += 1
    t4 = t4.div(1000000)

    t8 = pd.read_csv(vsc_results_path + standard_path + "all_8.csv")
    t8.index += 1
    t8 = t8.div(1000000)

    df = pd.DataFrame()
    df['1'] = t1['Infector']
    df['2'] = t2['Infector']
    df['4'] = t4['Infector']
    df['8'] = t8['Infector']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_all_parallel_infector',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=threads_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title="Threads",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis_range=[0,80],
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def standard_opt_parallel_infector():
    t1 = pd.read_csv(vsc_results_path + standard_path + "opt_1.csv")
    t1.index += 1
    t1 = t1.div(1000000)

    t2 = pd.read_csv(vsc_results_path + standard_path +"opt_2.csv")
    t2.index += 1
    t2 = t2.div(1000000)

    t4 = pd.read_csv(vsc_results_path + standard_path + "opt_4.csv")
    t4.index += 1
    t4 = t4.div(1000000)

    t8 = pd.read_csv(vsc_results_path + standard_path + "opt_8.csv")
    t8.index += 1
    t8 = t8.div(1000000)

    df = pd.DataFrame()
    df['1'] = t1['Infector']
    df['2'] = t2['Infector']
    df['4'] = t4['Infector']
    df['8'] = t8['Infector']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_opt_parallel_infector',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=threads_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title="Threads",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis_range=[0,1.5],
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

def basis_standard_comparison_all():
    bsis = pd.read_csv(vsc_results_path + basis_path + "all_1.csv")
    bsis.index += 1
    bsis = bsis.div(1000000)

    standard = pd.read_csv(vsc_results_path + standard_path + "all_1.csv")
    standard.index += 1
    standard = standard.div(1000000)

    df = pd.DataFrame()
    df['value (infector)'] = bsis['Infector']
    df['value (total)'] = bsis['Total']
    df['reference (infector)'] = standard['Infector']
    df['reference (total)'] = standard['Total']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_standard_comparison_all',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=comparison_section_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title="Pass by:",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis_range=[0,80],
        legend={'itemsizing': 'constant'},
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=3)
        )
    fig.show(config=conf)

def basis_standard_comparison_opt():
    bsis = pd.read_csv(vsc_results_path + basis_path + "opt_1.csv")
    bsis.index += 1
    bsis = bsis.div(1000000)

    standard = pd.read_csv(vsc_results_path + standard_path + "opt_1.csv")
    standard.index += 1
    standard = standard.div(1000000)

    df = pd.DataFrame()
    df['value (infector)'] = bsis['Infector']
    df['value (total)'] = bsis['Total']
    df['reference (infector)'] = standard['Infector']
    df['reference (total)'] = standard['Total']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'basis_standard_comparison_opt',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.line(df, color_discrete_sequence=comparison_section_colors
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title="Pass by:",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis_range=[0,3],
        legend={'itemsizing': 'constant'},
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=3)
        )
    fig.show(config=conf)

def standard():
    standard_all()
    standard_opt()
    standard_all_parallel_infector()
    standard_opt_parallel_infector()

def stats(path, filename):
    df = pd.read_csv(vsc_results_path + path + filename + ".csv")
    df.index += 1
    df = df.div(1000000)
    print(path + ": " + filename)
    print(df.mean())

#---------- ITERATIVE INTERVALS ----------

def ii_vs_standard_all_infector():
    df_og = pd.read_csv(vsc_results_path + standard_path + "all_1.csv")
    df_og.index += 1
    df_og = df_og.div(1000000)

    df_ii = pd.read_csv(vsc_results_path + ii_path + "all_1.csv")
    df_ii.index += 1
    df_ii = df_ii.div(1000000)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'ii_vs_standard_infector',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    print(df_og.head())
    fig = go.Figure(
        data=[
            go.Scatter(name="Original", x=df_og.index, y=df_og['Infector'], mode='lines', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", x=df_ii.index, y=df_ii['Infector'], mode='lines', marker=dict(color=approach_colors[1])),
        ],
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
        xaxis_range=[1,100],
        yaxis_range=[0,40],
    ).update_xaxes(
        title_standoff=20,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=40,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

#---------- SAMPLING WITH ITERATION ----------

def swi_all_infector():
    df_og = pd.read_csv(vsc_results_path + standard_path + "all_1.csv")
    df_og.index += 1
    df_og = df_og.div(1000000)

    df_ii = pd.read_csv(vsc_results_path + ii_path + "all_1.csv")
    df_ii.index += 1
    df_ii = df_ii.div(1000000)

    df_swi = pd.read_csv(vsc_results_path + swi_path + "all_1_pType.csv")
    df_swi.index += 1
    df_swi = df_swi.div(1000000)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'swi_vs_rest_infector',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    print(df_og.head())
    fig = go.Figure(
        data=[
            go.Scatter(name="Original", x=df_og.index, y=df_og['Infector'], mode='lines', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", x=df_ii.index, y=df_ii['Infector'], mode='lines', marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", x=df_swi.index, y=df_swi['Infector'], mode='lines', marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
        xaxis_range=[1,100],
        yaxis_range=[0,40],
    ).update_xaxes(
        title_standoff=20,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=40,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

#---------- FULL SAMPLING pType ----------

def fs_pType_all_infector():
    df_og = pd.read_csv(vsc_results_path + standard_path + "all_1.csv")
    df_og.index += 1
    df_og = df_og.div(1000000)

    df_ii = pd.read_csv(vsc_results_path + ii_path + "all_1.csv")
    df_ii.index += 1
    df_ii = df_ii.div(1000000)

    df_swi = pd.read_csv(vsc_results_path + swi_path + "all_1_pType.csv")
    df_swi.index += 1
    df_swi = df_swi.div(1000000)

    df_fs = pd.read_csv(vsc_results_path + fs_path + "all_1_pType.csv")
    df_fs.index += 1
    df_fs = df_fs.div(1000000)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'fs_pType_vs_rest_infector',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    print(df_og.head())
    fig = go.Figure(
        data=[
            go.Scatter(name="Original", x=df_og.index, y=df_og['Infector'], mode='lines', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", x=df_ii.index, y=df_ii['Infector'], mode='lines', marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", x=df_swi.index, y=df_swi['Infector'], mode='lines', marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", x=df_fs.index, y=df_fs['Infector'], mode='lines', marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
        xaxis_range=[1,100],
        yaxis_range=[0,40],
    ).update_xaxes(
        title_standoff=20,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=40,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

#---------- FULL SAMPLING pSize ----------

def fs_pSize_all_infector():
    df_og = pd.read_csv(vsc_results_path + standard_path + "all_1.csv")
    df_og.index += 1
    df_og = df_og.div(1000000)

    df_ii = pd.read_csv(vsc_results_path + ii_path + "all_1.csv")
    df_ii.index += 1
    df_ii = df_ii.div(1000000)

    df_swi = pd.read_csv(vsc_results_path + swi_path + "all_1_pType.csv")
    df_swi.index += 1
    df_swi = df_swi.div(1000000)

    df_fs = pd.read_csv(vsc_results_path + fs_path + "all_1_pType.csv")
    df_fs.index += 1
    df_fs = df_fs.div(1000000)

    df_fs2 = pd.read_csv(vsc_results_path + fs_path + "all_1_pSize.csv")
    df_fs2.index += 1
    df_fs2 = df_fs2.div(1000000)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'fs_pSize_vs_rest_infector',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    print(df_og.head())
    fig = go.Figure(
        data=[
            go.Scatter(name="Original", x=df_og.index, y=df_og['Infector'], mode='lines', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", x=df_ii.index, y=df_ii['Infector'], mode='lines', marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", x=df_swi.index, y=df_swi['Infector'], mode='lines', marker=dict(color=approach_colors[2])),
            #go.Scatter(name="Full sampling", x=df_fs.index, y=df_fs['Infector'], mode='lines', marker=dict(color=approach_colors[4])),
            go.Scatter(name="Full sampling (>150)", x=df_fs2.index, y=df_fs2['Infector'], mode='lines', marker=dict(color=approach_colors[5])),
        ],
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
        xaxis_range=[1,100],
        yaxis_range=[0,40],
    ).update_xaxes(
        title_standoff=20,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=40,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)


#---------- INF-TO-SUS ----------

def inf_to_sus_infectors():
    df_og = pd.read_csv(vsc_results_path + standard_path + "opt_1.csv")
    df_og.index += 1
    df_og = df_og.div(1000000)

    df_ii_both = pd.read_csv(vsc_results_path + its_path + "ii_sort_both.csv")
    df_ii_both.index += 1
    df_ii_both = df_ii_both.div(1000000)

    df_ii_sus = pd.read_csv(vsc_results_path + its_path + "ii_sort_sus.csv")
    df_ii_sus.index += 1
    df_ii_sus = df_ii_sus.div(1000000)

    df_sample_contacts_both = pd.read_csv(vsc_results_path + its_path + "sample_contacts_sort_both.csv")
    df_sample_contacts_both.index += 1
    df_sample_contacts_both = df_sample_contacts_both.div(1000000)

    df_sample_contacts_sus = pd.read_csv(vsc_results_path + its_path + "sample_contacts_sort_sus.csv")
    df_sample_contacts_sus.index += 1
    df_sample_contacts_sus = df_sample_contacts_sus.div(1000000)

    df_sample_both = pd.read_csv(vsc_results_path + its_path + "sample_sort_both.csv")
    df_sample_both.index += 1
    df_sample_both = df_sample_both.div(1000000)

    df_sample_sus = pd.read_csv(vsc_results_path + its_path + "sample_sort_sus.csv")
    df_sample_sus.index += 1
    df_sample_sus = df_sample_sus.div(1000000)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'inf_to_sus_infectors',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    print(df_ii_sus.head())

    fig = go.Figure(
        data=[
            go.Scatter(name="Original", x=df_og.index, y=df_og['Infector'], mode='lines', marker=dict(color=approach_colors[0])),
            #go.Scatter(name="Iterative intervals (sort both)", x=df_ii_both.index, y=df_ii_both['Infector'], mode='lines', marker=dict(color=approach_colors[1])),
            #go.Scatter(name="Iterative intervals (sort susceptibles)", x=df_ii_sus.index, y=df_ii_sus['Infector'], mode='lines', marker=dict(color=approach_colors[2])),
            go.Scatter(name="Sampling contacts (sort both)", x=df_sample_contacts_both.index, y=df_sample_contacts_both['Infector'], mode='lines', marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling contacts (sort susceptibles)", x=df_sample_contacts_sus.index, y=df_sample_contacts_sus['Infector'], mode='lines', marker=dict(color=approach_colors[2])),
            #go.Scatter(name="Sampling (sort both)", x=df_sample_both.index, y=df_sample_both['Infector'], mode='lines', marker=dict(color=approach_colors[1])),
            #go.Scatter(name="Sampling (sort susceptibles)", x=df_sample_sus.index, y=df_sample_sus['Infector'], mode='lines', marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
        xaxis_range=[1,100],
        yaxis_range=[0,2.5],
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.03,
            traceorder='normal',
        ),
    ).update_xaxes(
        title_standoff=20,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=40,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=3)
        )
    fig.show(config=conf)


def its_infections():
    df_og = pd.read_csv(vsc_results_path + standard_path + "standard_opt_1/Successful runs/1/infected.csv", header=None).T
    df_og.index += 1

    df_ii_both = pd.read_csv(vsc_results_path + its_path + "ii_sort_both/Successful runs/1/infected.csv", header=None).T
    df_ii_both.index += 1
    print(df_ii_both)

    df_ii_sus = pd.read_csv(vsc_results_path + its_path + "ii_sort_sus/Successful runs/1/infected.csv", header=None).T
    df_ii_sus.index += 1

    df_sample_contacts_both = pd.read_csv(vsc_results_path + its_path + "sample_contacts_sort_both/Successful runs/1/infected.csv", header=None).T
    df_sample_contacts_both.index += 1

    df_sample_contacts_sus = pd.read_csv(vsc_results_path + its_path + "sample_contacts_sort_sus/Successful runs/1/infected.csv", header=None).T
    df_sample_contacts_sus.index += 1

    df_sample_both = pd.read_csv(vsc_results_path + its_path + "sample_sort_both/Successful runs/1/infected.csv", header=None).T
    df_sample_both.index += 1

    df_sample_sus = pd.read_csv(vsc_results_path + its_path + "sample_sort_sus/Successful runs/1/infected.csv", header=None).T
    df_sample_sus.index += 1

    conf = {    
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'its_infections',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original", x=df_og.index, y=df_og[0], mode='lines', marker=dict(color=approach_colors[0])),
            #go.Scatter(name="ii both", x=df_ii_both.index, y=df_ii_both[0], mode='lines', marker=dict(color=approach_colors[1])),
            #go.Scatter(name="ii sus", x=df_ii_sus.index, y=df_ii_sus[0], mode='lines', marker=dict(color=approach_colors[2])),
            #go.Scatter(name="sampling (sort both)", x=df_sample_both.index, y=df_sample_both[0], mode='lines', marker=dict(color=approach_colors[1])),
            go.Scatter(name="sampling (sort susceptibles)", x=df_sample_sus.index, y=df_sample_sus[0], mode='lines', marker=dict(color=approach_colors[2])),
            #go.Scatter(name="sampling contacts (sort both)", x=df_sample_contacts_both.index, y=df_sample_contacts_both[0], mode='lines', marker=dict(color=approach_colors[1])),
            go.Scatter(name="sampling contacts (sort susceptibles)", x=df_sample_contacts_sus.index, y=df_sample_contacts_sus[0], mode='lines', marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Infected people",
        font_size=40,
        legend_title=None,
        xaxis_range=[1,100],
        yaxis_range=[0,840000],
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.01,
            traceorder='normal',
        ),
    ).update_xaxes(
        title_standoff=20,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=40,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)

#---------- ALL-TO-ALL SUMMARY ----------

def infector_summary():
    df = pd.read_csv(vsc_results_path + basis_path + "all_1.csv")
    df.index += 1
    df = df.div(1000000)

    df_og = pd.read_csv(vsc_results_path + standard_path + "all_1.csv")
    df_og.index += 1
    df_og = df_og.div(1000000)

    df_ii = pd.read_csv(vsc_results_path + ii_path + "all_1.csv")
    df_ii.index += 1
    df_ii = df_ii.div(1000000)

    df_swi = pd.read_csv(vsc_results_path + swi_path + "all_1_pType.csv")
    df_swi.index += 1
    df_swi = df_swi.div(1000000)

    df_fs = pd.read_csv(vsc_results_path + fs_path + "all_1_pType.csv")
    df_fs.index += 1
    df_fs = df_fs.div(1000000)

    df_fs2 = pd.read_csv(vsc_results_path + fs_path + "all_1_pSize.csv")
    df_fs2.index += 1
    df_fs2 = df_fs2.div(1000000)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'infector_runtimes_summary',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    print(df_og.head())
    fig = go.Figure(
        data=[
            go.Scatter(name="Original (by value)", x=df.index, y=df['Infector'], mode='lines', marker=dict(color='black')),
            go.Scatter(name="Original (by reference)", x=df_og.index, y=df_og['Infector'], mode='lines', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", x=df_ii.index, y=df_ii['Infector'], mode='lines', marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", x=df_swi.index, y=df_swi['Infector'], mode='lines', marker=dict(color=approach_colors[2])),
            #go.Scatter(name="Full sampling", x=df_fs.index, y=df_fs['Infector'], mode='lines', marker=dict(color=approach_colors[4])),
            go.Scatter(name="Full sampling (>150)", x=df_fs2.index, y=df_fs2['Infector'], mode='lines', marker=dict(color=approach_colors[5])),
        ],
    ).update_layout(
        xaxis_title="Day",
        yaxis_title="Time (in seconds)",
        font_size=40,
        legend_title=None,
        xaxis_range=[1,100],
        yaxis_range=[0,70],
    ).update_xaxes(
        title_standoff=20,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=40,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5)
        )
    fig.show(config=conf)


if __name__=="__main__":
    #stats(ii_path, 'all_1')
    #ii_vs_standard_all_infector()
    #stats(swi_path, 'all_1_pType')
    #swi_all_infector()
    #stats(fs_path, 'all_1_pType')
    #fs_pType_all_infector()
    #stats(fs_path, 'all_1_pSize')
    #fs_pSize_all_infector()

    '''
    stats(standard_path, 'opt_1')
    stats(its_path, 'ii_sort_both')
    stats(its_path, 'ii_sort_sus')
    stats(its_path, 'sample_contacts_sort_both')
    stats(its_path, 'sample_contacts_sort_sus')
    stats(its_path, 'sample_sort_both')
    stats(its_path, 'sample_sort_sus')
    '''

    #inf_to_sus_infectors()
    #its_infections()

    #infector_summary()

    basis_standard_comparison_all()
    basis_standard_comparison_opt()
