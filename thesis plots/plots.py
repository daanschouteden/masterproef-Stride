import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import sys
import xml.etree.ElementTree as ET

contact_vector_path = "/home/daan/opt/stride-302/data/contact_matrix_flanders_conditional_teachers.xml"
contact_matrix_path = "/home/daan/Documents/Masterproef/matrices/"

COLOR_HEATMAP = 'Hot'
# age,  household_id,  school_id,   work_id,  primary_community,  secondary_community
#df = pd.read_csv('/home/daan/opt/stride-302/data/pop_belgium11M_c500_teachers_censushh.csv')
#df = pd.read_csv('/home/daan/opt/stride-302/data/pop_belgium600k_c500_teachers_censushh.csv')
#df = df.astype(int)

#print(df.head(1))
print("\n")

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
#---------- Contact matrices ----------

def age_and_rates(pool):
    tree = ET.parse(contact_vector_path)
    root = tree.getroot()

    ages = list()
    rates = list()
    for typ in root:
        if typ.tag == pool:
            for part in typ:
                for cntcs in part:
                    if cntcs.tag == "age":
                        ages.append(int(cntcs.text))
                    if cntcs.tag == "contacts":
                        for cntc in cntcs:
                            for rt in cntc:
                                if rt.tag == "rate":
                                    rates.append(float(rt.text))
    return (ages, rates)

def contact_matrix_school():
    ages, rates = age_and_rates('school')
    
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'school_contact_rates',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    fig = px.scatter(x=ages, y=rates
    ).update_layout(
        xaxis_title="Age",
        yaxis_title="Contact rate",
        font_size=40,
        showlegend=False,
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0.0,
            dtick = 2,
        ),
        xaxis_range=[0,112],
        yaxis_range=[0,21],
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
        title_standoff=80,
        ticks="outside",
    ).update_traces(
        marker=dict(
            size=16,
            color="blue"),
        selector=dict(mode='markers')
    )
    fig.show(config=conf)

def contact_matrix_work():
    ages, rates = age_and_rates('work')
    
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'work_contact_rates',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    fig = px.scatter(x=ages, y=rates
    ).update_layout(
        xaxis_title="Age",
        yaxis_title="Contact rate",
        font_size=40,
        showlegend=False,
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0.0,
            dtick = 2,
        ),
        xaxis_range=[0,112],
        yaxis_range=[0,21],
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
        title_standoff=80,
        ticks="outside",
    ).update_traces(
        marker=dict(
            size=16,
            color="blue"),
        selector=dict(mode='markers')
    )
    fig.show(config=conf)

def contact_matrix_primary():
    ages, rates = age_and_rates('primary_community')
    
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'primary_contact_rates',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    fig = px.scatter(x=ages, y=rates
    ).update_layout(
        xaxis_title="Age",
        yaxis_title="Contact rate",
        font_size=40,
        showlegend=False,
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0.0,
            dtick = 2,
        ),
        xaxis_range=[0,112],
        yaxis_range=[0,21],
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
        title_standoff=80,
        ticks="outside",
    ).update_traces(
        marker=dict(
            size=16,
            color="blue"),
        selector=dict(mode='markers')
    )
    fig.show(config=conf)

def contact_matrix_secondary():
    ages, rates = age_and_rates('secondary_community')
    
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'secondary_contact_rates',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    fig = px.scatter(x=ages, y=rates
    ).update_layout(
        xaxis_title="Age",
        yaxis_title="Contact rate",
        font_size=40,
        showlegend=False,
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0.0,
            dtick = 2,
        ),
        xaxis_range=[0,112],
        yaxis_range=[0,21],
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
        title_standoff=80,
        ticks="outside",
    ).update_traces(
        marker=dict(
            size=16,
            color="blue"),
        selector=dict(mode='markers')
    )
    fig.show(config=conf)


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
        coloraxis=dict(colorbar_x=0.75, colorbar_thickness=25),
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
        coloraxis=dict(colorbar_x=0.75, colorbar_thickness=25),
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
        coloraxis=dict(colorbar_x=0.75, colorbar_thickness=25),
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
        coloraxis=dict(colorbar_x=0.75, colorbar_thickness=25),
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


if __name__=="__main__":
    contact_heatmap_school()