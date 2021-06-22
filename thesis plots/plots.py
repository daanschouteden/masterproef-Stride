import plotly.express as px
import plotly.graph_objects as go
from numpy.core.numeric import NaN

import pandas as pd
import sys

vsc_results_path = '/home/daan/Documents/Masterproef/masterproef/VSC results/'
standard_path = "1-standard/"
fs_path = "4-full_sampling/"

contact_vector_path = "/home/daan/opt/stride-302/data/contact_matrix_flanders_conditional_teachers.xml"
contact_matrix_path = "/home/daan/Documents/Masterproef/matrices/"
contact_rates_csv = 'contact_rates_original.csv'
reverse_contact_matrix = 'reverse_contacts_standard.csv'

approach_colors = ["#FDAA10","#14B37D","#64afff","#1f4397", "#FF9999", "#C20000"]

COLOR_HEATMAP = 'Hot'
# age,  household_id,  school_id,   work_id,  primary_community,  secondary_community
#df = pd.read_csv('/home/daan/opt/stride-302/data/pop_belgium11M_c500_teachers_censushh.csv')
#df = pd.read_csv('/home/daan/opt/stride-302/data/pop_belgium600k_c500_teachers_censushh.csv')
#df = df.astype(int)

#print(df.head(1))

xtitle_standoff = 25
ytitle_standoff = 40

#---------- POPULATION ----------
def population_age_distribution():
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'population_age_distribution'
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(df, x="age",
    ).update_layout(
        xaxis_title="Age",
        yaxis_title="Number of people",
        font_size=40,
        showlegend=False
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
        ticks="outside",
        title_standoff=80,
    ).update_traces(marker=dict(color='red'))
    #.update_traces(marker=dict(color='rgba(15, 214, 30, 1)'))
    fig.show(config=conf)

#---------- HOUSEHOLD ----------
def household_size_distribution():
    sizes = df['household_id'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'household_poolsizes',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    
    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
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
        ticks="outside",
        title_standoff=80,
    )
    fig.show(config=conf)

#---------- SCHOOL ----------
def school_size_distribution():
    sizes = df[df.school_id > 0]['school_id'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'school_poolsizes'
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
        xaxis_range=[1,50]
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
        ticks="outside",
        title_standoff=80,
    )
    fig.show(config=conf)

def school_ages_per_size():
    sizes = df[df.school_id > 0]['school_id'].value_counts()
    print(sizes.index)
    print(sizes.values)

    counter = 0
    for i in range(len(sizes)):
        if sizes.values[i] < 14 or sizes.values[i] > 23:
            continue
        counter += 1
        if counter % 100 == 0:
            print(counter)
        if ((df['age']<18) & (df['school_id'] == sizes.index[i])).any():
            print("nou")
            return

def school_age_distribution():
    ages = df[df.school_id > 0]['age']
    print(ages)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'school_age_distribution',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(ages
    ).update_layout(
        xaxis_title="Age",
        yaxis_title="Number of people",
        font_size=40,
        showlegend=False,
        xaxis_range=[1,100]
    ).update_xaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=100,
    ).update_traces(marker=dict(color='red'))
    fig.show(config=conf)

#---------- WORKPLACE ----------
def workplace_size_distribution():
    sizes = df[df.work_id > 0]['work_id'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'workplace_all_poolsizes',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=80,
    )
    fig.show(config=conf)

def workplace_size_1_10_distribution():
    sizes = df[df.work_id > 0]['work_id'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'workplace_1-10_poolsizes',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
        xaxis_range=[1,10],
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
        ticks="outside",
        title_standoff=60,
    )
    fig.show(config=conf)

def workplace_size_10_50_distribution():
    sizes = df[df.work_id > 0]['work_id'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'workplace_10-50_poolsizes',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
        xaxis_range=[10,50],
        yaxis_range=[0,2500],
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
        ticks="outside",
        title_standoff=60,
    )
    fig.show(config=conf)

def workplace_size_50_250_distribution():
    sizes = df[df.work_id > 0]['work_id'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'workplace_50-250_poolsizes',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
        xaxis_range=[50,250],
        yaxis_range=[0,50],
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
        ticks="outside",
        title_standoff=60,
    )
    fig.show(config=conf)

def workplace_size_250_1000_distribution():
    sizes = df[df.work_id > 0]['work_id'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'workplace_250-1000_poolsizes',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
        xaxis_range=[250,1000],
        yaxis_range=[0,10],
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
        title_standoff=60,
        ticks="outside",
    )
    fig.show(config=conf)

def workplace_age_distribution():
    ages = df[df.work_id > 0]['age']
    print(ages)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'workplace_age_distribution',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(ages
    ).update_layout(
        xaxis_title="Age",
        yaxis_title="Number of people",
        font_size=40,
        showlegend=False,
        xaxis_range=[1,100]
    ).update_xaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=50,
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=100,
    ).update_traces(marker=dict(color='red'))
    fig.show(config=conf)

def workplace_percentages():
    sizes = df[df.work_id > 0]['work_id'].value_counts()
    total = len(sizes.values)

    counter = 0
    for value in sizes.values:
        if value <= 9:
            counter += 1
    print(str(counter) + " / " + str(total) + " = " + str(counter/total))

def workplace_people():
    sizes = df[df.work_id > 0]['work_id'].value_counts()
    total = 0

    people = 0
    for i in range(len(sizes.values)):
        total += sizes.values[i]
        if sizes.values[i] >= 250:
            people += sizes.values[i]
    print(str(people) + " / " + str(total) + " = " + str(people/total))

def workplace_min_max_ranges():
    sizes = df[df.work_id > 0]['work_id'].value_counts().value_counts()

    bottom = 250
    top = 10000

    minimum = sys.maxsize
    maximum = 0
    for i in range(len(sizes.values)):
        if sizes.index[i] >= bottom and sizes.index[i] <= top:
            minimum = min(minimum, sizes.values[i])
            maximum = max(maximum, sizes.values[i])
    print("Min: " + str(minimum) + "\nMax: " + str(maximum))

#---------- PRIMARY COMMUNITY ----------
def primary_size_distribution():
    sizes = df['primary_community'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'primary_community_poolsizes',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
        xaxis_range=[1,1450],
        yaxis_range=[0,1000],
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=80,
    )
    fig.show(config=conf)

#---------- SECONDARY COMMUNITY ----------

def secondary_size_distribution():
    sizes = df['secondary_community'].value_counts()
    print(sizes)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'secondary_community_poolsizes',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(sizes
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of pools",
        font_size=40,
        showlegend=False,
        xaxis_range=[1,1450],
        yaxis_range=[0,1000],
    ).update_xaxes(
        title_standoff=50,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        title_standoff=80,
    )
    fig.show(config=conf)

##########################################


##########################################
#---------- Contact heatmaps ----------
def contact_heatmap_school():
    matrix = pd.read_csv(contact_matrix_path + "ref_fl2010_regular_weekday_school_conditional_age23_teachers_gam_mij_rec_median.csv", delimiter=";", decimal=",")

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'school_contact_heatmap',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    lst = []
    lst.extend(range(0,81))
    matrix.columns=lst
    print(matrix)
    fig = px.imshow(matrix, color_continuous_scale=COLOR_HEATMAP
    ).update_layout(
        xaxis_title="Age (initiator)",
        yaxis_title="Age (recipient)",
        font_size=40,
        coloraxis=dict(
            colorbar_x=0.75,
            colorbar_thickness=25,
            cmin=0,
            cmax=3.5,
        ),
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 20,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 20,
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        #showgrid=True,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        #showgrid=True,
        #gridwidth=5,
        #gridcolor='white',
        title_standoff=0,
        ticks="outside",
        autorange=True
    )

    fig.show(config=conf)

def contact_heatmap_work():
    matrix = pd.read_csv(contact_matrix_path + "ref_fl2010_regular_weekday_workplace_conditional_gam_mij_rec_median.csv", delimiter=";", decimal=",")

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'work_contact_heatmap',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    lst = []
    lst.extend(range(0,81))
    matrix.columns=lst
    print(matrix)
    fig = px.imshow(matrix, color_continuous_scale=COLOR_HEATMAP
    ).update_layout(
        xaxis_title="Age (initiator)",
        yaxis_title="Age (recipient)",
        font_size=40,
        coloraxis=dict(
            colorbar_x=0.75,
            colorbar_thickness=25,
            cmin=0,
            cmax=0.3,
        ),
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 20,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 20,
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        #showgrid=True,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        #showgrid=True,
        #gridwidth=5,
        #gridcolor='white',
        title_standoff=0,
        ticks="outside",
        autorange=True
    )

    fig.show(config=conf)

def contact_heatmap_primary():
    matrix = pd.read_csv(contact_matrix_path + "ref_fl2010_weekend_community_gam_mij_rec.csv", delimiter=";", decimal=",")

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'primary_contact_heatmap',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    lst = []
    lst.extend(range(0,81))
    matrix.columns=lst
    print(matrix)
    fig = px.imshow(matrix, color_continuous_scale=COLOR_HEATMAP
    ).update_layout(
        xaxis_title="Age (initiator)",
        yaxis_title="Age (recipient)",
        font_size=40,
        coloraxis=dict(
            colorbar_x=0.75,
            colorbar_thickness=25,
            cmin=0,
            cmax=0.8,
            #colorbar_tickformat=".2f",
        ),
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 20,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 20,
        ),
        #margin = {'l':0,'r':0,'t':0,'b':0},
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        #showgrid=True,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        #showgrid=True,
        #gridwidth=5,
        #gridcolor='white',
        title_standoff=0,
        ticks="outside",
        autorange=True
    )

    fig.show(config=conf)

def contact_heatmap_secondary():
    matrix = pd.read_csv(contact_matrix_path + "ref_fl2010_regular_weekday_community_gam_mij_rec.csv", delimiter=";", decimal=",")

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'secondary_contact_heatmap',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    lst = []
    lst.extend(range(0,81))
    matrix.columns=lst
    print(matrix)
    fig = px.imshow(matrix, color_continuous_scale=COLOR_HEATMAP
    ).update_layout(
        xaxis_title="Age (initiator)",
        yaxis_title="Age (recipient)",
        font_size=40,
        coloraxis=dict(
            colorbar_x=0.75,
            colorbar_thickness=25,
            cmin=0,
            cmax=0.8,
        ),
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 20,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 20,
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        #showgrid=True,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        #showgrid=True,
        #gridwidth=5,
        #gridcolor='white',
        title_standoff=0,
        ticks="outside",
        autorange=True
    )

    fig.show(config=conf)

##########################################

def distributions():
    pass
    #print(df[df.work_id > 0]['age'].max())

    #population_age_distribution()
    #household_size_distribution()

    #school_size_distribution()
    #school_ages_per_size()
    #school_age_distribution()

    #workplace_size_distribution()
    #workplace_age_distribution()
    #workplace_size_1_10_distribution()
    #workplace_size_10_50_distribution()
    #workplace_size_50_250_distribution()
    #workplace_size_250_1000_distribution()
    #workplace_percentages()
    #workplace_people()
    #workplace_min_max_ranges()

    #primary_size_distribution()
    #secondary_size_distribution()

def contact_matrices():
    contact_matrix_school()
    contact_matrix_work()
    contact_matrix_primary()
    contact_matrix_secondary()

def contact_heatmaps():
    contact_heatmap_school()
    contact_heatmap_work()
    contact_heatmap_primary()
    contact_heatmap_secondary()

def susceptibles():
    df = pd.read_csv('susceptibles.csv')
    print(df.head())

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'susceptibles_distribution'
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.histogram(df, x="Pool size", y="Susceptibles"
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Number of susceptibles",
        font_size=40,
        showlegend=False
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
        ticks="outside",
        title_standoff=80,
    ).update_traces(marker=dict(color='blue'))
    #.update_traces(marker=dict(color='rgba(15, 214, 30, 1)'))
    fig.show(config=conf)

def infectious():
    df = pd.read_csv('infectious.csv')
    df.index += 1
    print(df.head())
    # Don't show zero values
    df.replace(0, NaN, inplace=True)
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'infectious_distribution'
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = px.scatter(df, x=df.index, y="Infectious", 
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Average infectious persons",
        font_size=40,
        showlegend=False,
        xaxis_range=[0,1450],
        yaxis_range=[0,160],
    ).update_xaxes(
        title_standoff=30,
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=5,
        gridcolor='white',
        ticks="outside",
        title_standoff=40,
    ).update_traces(marker=dict(color='blue', size=10))
    #.update_traces(marker=dict(color='rgba(15, 214, 30, 1)'))
    fig.show(config=conf)

def infected():
    df_og = pd.read_csv(vsc_results_path + standard_path + "standard_all_1/Successful runs/1/infected.csv", header=None).T
    df_og.index += 1

    df_fs = pd.read_csv(vsc_results_path + fs_path + "full_sampling_all_1_pType/Successful runs/1/infected.csv", header=None).T
    df_fs.index += 1

    conf = {    
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'infections',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original", x=df_og.index, y=df_og[0], mode='lines', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Full sampling", x=df_fs.index, y=df_fs[0], mode='lines', marker=dict(color=approach_colors[4])),
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

#########################################

def countMatches():
    vsc_results_path = '/home/daan/Documents/Masterproef/masterproef/VSC results/'
    standard_path = "1-standard/"
    filename = "all_1_times_counts.csv"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1

    poolsizes = {}
    for index, row in df.iterrows():
        poolsizes[index] = row["counts_household"]
        poolsizes[index] += row["counts_k12school"]
        poolsizes[index] += row["counts_college"]
        poolsizes[index] += row["counts_workplace"]
        poolsizes[index] += row["counts_primary"]
        poolsizes[index] += row["counts_secondary"]
    
    totalMatches = 0
    for key, value in poolsizes.items():
        if value == 0:
            continue
        sizeMatches = get_triangular_number(key) * value
        totalMatches += sizeMatches

    print(totalMatches)

def get_triangular_number(number):
    outcome = 0
    for i in range(number):
        outcome += i
    return outcome

if __name__=="__main__":
    #contact_heatmap_school()
    #contact_heatmap_work()
    #contact_heatmap_primary()
    #contact_heatmap_secondary()
    countMatches()
