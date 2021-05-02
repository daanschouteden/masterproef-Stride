from numpy.core.numeric import NaN
from pandas.core.frame import DataFrame
import plotly.express as px
import pandas as pd
import sys

vsc_results_path = '/home/daan/Documents/Masterproef/masterproef/VSC results/'
basis_path = "0-basis/"
standard_path = "1-standard/"
filename = "all_1_times_counts.csv"

section_colors= ["#eda189", "#bfacd6", "#c7b526", "#25c9ae"]
threads_colors = ["#542e71", "#fb3640", "#fdca40", "#a799b7"]
comparison_section_colors= ["#FFF700", "#2BD8E7", "#B3AD00", "#2F8F97"]


def standard_all_averages():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_times_all_averages',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    df_combined = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_combined['totals'] = df['times_household'] + df['times_k12school'] + df['times_college'] +\
        df['times_workplace'] + df['times_primary'] + df['times_secondary']
    df_combined['totals'] = df_combined['totals'].div(1000)

    df_combined['counts'] = df['counts_household'] + df['counts_k12school'] + df['counts_college'] +\
        df['counts_workplace'] + df['counts_primary'] + df['counts_secondary']

    df_combined['averages'] = df_combined['totals'] / df_combined['counts']


    print(df_combined)

    fig = px.scatter(df_combined['averages']
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=False,
        xaxis_range=[0,1450],
        yaxis_range=[0,9],
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
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            color='orange',
            size=10,
        ),
    )
    fig.show(config=conf)

def standard_all_totals():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_times_all_totals',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    df_combined = pd.DataFrame(columns=['totals'])
    df_combined['totals'] = df['times_household'] + df['times_k12school'] + df['times_college'] +\
        df['times_workplace'] + df['times_primary'] + df['times_secondary']
    df_combined['totals'] = df_combined['totals'].div(1000)

    # Don't show zero values
    df_combined.replace(0, NaN, inplace=True)

    print(df_combined)

    fig = px.scatter(df_combined
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=False,
        xaxis = dict(
            #tickmode = 'linear',
            tick0 = 0,
            #dtick = 10,
        ),
        yaxis = dict(
            #tickmode = 'linear',
            tick0 = 0,
            #dtick = 10,
        ),
        xaxis_range=[0,1450]
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
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            color='orange',
            size=10,
        ),
    )
    fig.show(config=conf)

def standard_all_totals_weekly():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_times_all_totals_weekly',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    df_combined = pd.DataFrame(columns=['totals'])
    df_combined['totals'] = df['times_household'].mul(7) + df['times_k12school'].mul(5) + df['times_college'].mul(5) +\
        df['times_workplace'].mul(5) + df['times_primary'].mul(2) + df['times_secondary'].mul(5)
    df_combined['totals'] = df_combined['totals'].div(1000).div(7)

    # Don't show zero values
    df_combined.replace(0, NaN, inplace=True)

    print(df_combined)

    fig = px.scatter(df_combined
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=False,
        xaxis_range=[0,1450],
        yaxis = dict(
            #tickmode = 'linear',
            tick0 = 0,
            #dtick = 10,
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
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            color='orange',
            size=10,
        ),
    )
    fig.show(config=conf)


if __name__=="__main__":
    #standard_all_averages()
    #standard_all_totals()
    standard_all_totals_weekly()
