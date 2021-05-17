import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import sys
import xml.etree.ElementTree as ET

contact_vector_path = "/home/daan/opt/stride-302/data/contact_matrix_flanders_conditional_teachers.xml"
contact_matrix_path = "/home/daan/Documents/Masterproef/matrices/"
contact_rates_csv = 'contact_rates_original.csv'
reverse_cr_standard = 'reverse_contacts_standard.csv'
reverse_cr_ii = 'reverse_contacts_iterative_intervals.csv'
reverse_cr_swi = 'reverse_contacts_sampling_with_iteration.csv'

approach_colors = ["#c20000","#FDAA10","#14B37D","#64afff","#1f4397"]

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

# The original xml to csv
def contact_matrix_to_csv():    
    df = pd.DataFrame()

    ages, rates = age_and_rates('household')
    df['age'] = ages[:100]
    df['household'] = rates[:100]

    _, rates = age_and_rates('school')
    df['school'] = rates[:100]

    _, rates = age_and_rates('work')
    df['workplace'] = rates[:100]

    _, rates = age_and_rates('primary_community')
    df['primary'] = rates[:100]

    _, rates = age_and_rates('secondary_community')
    df['secondary'] = rates[:100]

    df.to_csv('contact_rates_original.csv', index=False)


#---------- Reverse contact matrices ----------

def contact_matrix_plot():
    df_standard = pd.read_csv(reverse_cr_standard)
    df = pd.read_csv(reverse_cr_swi)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'swi_vs_standard_reverse_cr_workplace',
            #'height': 500,
            #'width': 700,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    print(df.head(1))

    fig = go.Figure()
    # Standard
    fig.add_trace(go.Scatter(x=df_standard['age'], y=df_standard['Workplace'],
                    mode='markers',
                    name='Original',
                    marker=dict(
                        size=18,
                        color=approach_colors[1],
                        opacity=1,
                    ),
    ))

    # Sampling with iteration
    fig.add_trace(go.Scatter(x=df['age'], y=df['Workplace'],
                    mode='markers',
                    name='Iterative intervals',
                    marker=dict(
                        size=14,
                        color=approach_colors[3],
                        opacity=1,
                    ),
    ))

    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Contact rate",
        font_size=40,
        showlegend=True,
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
        xaxis_range=[-1,101],
        yaxis_range=[-0.5,21],
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            traceorder='normal',
        ),
    ).update_xaxes(
        title_standoff=40,
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
    )
    fig.show(config=conf)

if __name__=="__main__":
    contact_matrix_plot()
