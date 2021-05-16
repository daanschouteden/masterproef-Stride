from numpy.core.numeric import NaN
from pandas.core.frame import DataFrame
import plotly.express as px
import plotly.graph_objects as go
import plotly
import pandas as pd
import sys

vsc_results_path = '/home/daan/Documents/Masterproef/masterproef/VSC results/'
basis_path = "0-basis/"
standard_path = "1-standard/"
iterative_intervals_path = "2-iterative_intervals/"

filename = "all_1_times_counts.csv"

section_colors= ["#eda189", "#bfacd6", "#c7b526", "#25c9ae"]
threads_colors = ["#542e71", "#fb3640", "#fdca40", "#a799b7"]
comparison_section_colors= ["#FFF700", "#2BD8E7", "#B3AD00", "#2F8F97"]
approach_colors = ["#FDAA10","#14B37D","#64afff","#1f4397"]


#---------- 1-Standard ----------

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
            color=approach_colors[0],
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
            color=approach_colors[0],
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
            color=approach_colors[0],
            size=10,
        ),
    )
    fig.show(config=conf)

def standard_type_totals_weekly():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_times_type_totals',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    df2 = pd.DataFrame(columns=['pooltype', 'times'])
    secondary = df['times_secondary'].mul(5).sum()
    primary = df['times_primary'].mul(2).sum()
    work = df['times_workplace'].mul(5).sum()
    k12school = df['times_k12school'].mul(5).sum()
    college = df['times_college'].mul(5).sum()
    household = df['times_household'].mul(7).sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['secondary', 'primary', 'workplace', 'K-12 school', 'college', 'household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df2.loc[i] = [pooltype[i]] + [times[i]]

    df2['times'] = df2['times'].div(1000000).div(7)
    df2['times'] = df2['times'].astype(float).round(2)
    

    # Don't show zero values
    df2.replace(0, NaN, inplace=True)

    print(df2)

    df2 = df2.sort_values('times')

    fig = px.bar(df2, y='pooltype', x='times', text='times', orientation='h'
    ).update_layout(
        xaxis_title="Time (in seconds)",
        yaxis_title=None,
        font_size=40,
        legend_title=None,
        showlegend=False,
        xaxis = dict(
            #tickmode = 'linear',
            tick0 = 0,
            #dtick = 10,
        ),
        xaxis_range=[0,23]
    ).update_xaxes(
        title_standoff=40,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=50,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
        marker_color='orange'
    )
    fig.show(config=conf)

def standard_type_totals_overhead_weekly():
    df = pd.read_csv(vsc_results_path + standard_path + "all_1_pools.csv")
    df.index += 1
    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_times_type_totals_overhead',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    df = df.head(7)
    df = df.sum().to_frame('times')
    df = df.div(1000000).div(7)
    df = df.astype(float).round(2)
    df = df.head(6) # remove cluster
    df = df.sort_values('times')
    print(df)

    fig = px.bar(df, x='times', text='times', orientation='h'
    ).update_layout(
        xaxis_title="Time (in seconds)",
        yaxis_title=None,
        font_size=40,
        legend_title=None,
        showlegend=False,
        xaxis = dict(
            #tickmode = 'linear',
            tick0 = 0,
            #dtick = 10,
        ),
        xaxis_range=[0,23]
    ).update_xaxes(
        title_standoff=40,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=50,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)

def standard_type_totals_both():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1

    df2 = pd.DataFrame(columns=['pooltype', 'algorithm only'])
    secondary = df['times_secondary'].mul(5).sum()
    primary = df['times_primary'].mul(2).sum()
    work = df['times_workplace'].mul(5).sum()
    k12school = df['times_k12school'].mul(5).sum()
    college = df['times_college'].mul(5).sum()
    household = df['times_household'].mul(7).sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df2.loc[i] = [pooltype[i]] + [times[i]]

    df2['algorithm only'] = df2['algorithm only'].div(1000000).div(7)
    df2['algorithm only'] = df2['algorithm only'].astype(float).round(2)

    # Don't show zero values
    df2.replace(0, NaN, inplace=True)

    df2['pooltype'] = df2['pooltype'].astype(str)
    print(df2)

    df = pd.read_csv(vsc_results_path + standard_path + "all_1_pools.csv")
    df.index += 1

    df = df.head(7)
    df = df.sum().to_frame('total time')
    df = df.div(1000000).div(7)
    df = df.astype(float).round(2)
    df = df.head(6) # remove cluster
    df['pooltype'] = df.index
    df['pooltype'] = df['pooltype'].astype(str)
    print(df)

    df_both = df.merge(df2, how='inner', on='pooltype')
    print(df_both)
    df_both = df_both.sort_values('total time', ascending=True)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_times_type_totals',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(name="algorithm only", y=df_both['pooltype'], x=df_both['algorithm only'], text=df_both['algorithm only'], orientation='h', marker=dict(color=approach_colors[0])),
            go.Bar(name="total time", y=df_both['pooltype'], x=df_both['total time'], text=df_both['total time'], orientation='h', marker=dict(color='red')),
        ],
    ).update_layout(
        xaxis_title="Time (in seconds)",
        yaxis_title=None,
        font_size=40,
        legend_title=None,
        barmode='group',
        xaxis = dict(
            #tickmode = 'linear',
            tick0 = 0,
            #dtick = 10,
        ),
        xaxis_range=[0,24],
        legend=dict(
            yanchor="bottom",
            y=0.05,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=40,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=50,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

#---------- 2-Iterative intervals ----------

def iterative_intervals_type_averages_primary():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_primary']
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_primary']
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_primary']
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_primary']
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    print(df_ii)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'times_avg_ii_primary',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode='markers', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode='markers', marker=dict(color=approach_colors[1])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,1450],
        yaxis_range=[-0.05,9],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=40,
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=6,
        ),
    )
    fig.show(config=conf)

def iterative_intervals_type_averages_secondary():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_secondary']
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_secondary']
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_secondary']
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_secondary']
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    print(df_ii)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'times_avg_ii_secondary',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode='markers', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode='markers', marker=dict(color=approach_colors[1])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,1450],
        yaxis_range=[-0.05,9],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=40,
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=6,
        ),
    )
    fig.show(config=conf)

def iterative_intervals_type_averages_workplace():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_workplace']
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_workplace']
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_workplace']
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_workplace']
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    print(df_ii)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'times_avg_ii_workplace',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode='markers', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode='markers', marker=dict(color=approach_colors[1])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,1020],
        yaxis_range=[-0.05,6],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=40,
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=6,
        ),
    )
    fig.show(config=conf)

def iterative_intervals_type_averages_k12school():
    pooltype = "k12school"
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pooltype]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pooltype]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pooltype]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pooltype]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    print(df_ii)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'times_avg_ii_k12school',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode='markers', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode='markers', marker=dict(color=approach_colors[1])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[-0.05,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=40,
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=6,
        ),
    )
    fig.show(config=conf)

def iterative_intervals_type_averages_college():
    pooltype = "college"
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pooltype]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pooltype]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pooltype]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pooltype]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    print(df_ii)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'times_avg_ii_college',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode='markers', marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode='markers', marker=dict(color=approach_colors[1])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[-0.05,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=40,
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=2,
        gridcolor='white',
        title_standoff=50,
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=6,
        ),
    )
    fig.show(config=conf)

def iterative_intervals_type_totals_vs_standard():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1

    df2 = pd.DataFrame(columns=['pooltype', 'algorithm only'])
    secondary = df['times_secondary'].mul(5).sum()
    primary = df['times_primary'].mul(2).sum()
    work = df['times_workplace'].mul(5).sum()
    k12school = df['times_k12school'].mul(5).sum()
    college = df['times_college'].mul(5).sum()
    household = df['times_household'].mul(7).sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df2.loc[i] = [pooltype[i]] + [times[i]]

    df2['algorithm only'] = df2['algorithm only'].div(1000000).div(7)
    df2['algorithm only'] = df2['algorithm only'].astype(float).round(2)

    # Don't show zero values
    df2.replace(0, NaN, inplace=True)

    df2['pooltype'] = df2['pooltype'].astype(str)
    print(df2)

    df = pd.read_csv(vsc_results_path + standard_path + "all_1_pools.csv")
    df.index += 1

    df = df.head(7)
    df = df.sum().to_frame('total time')
    df = df.div(1000000).div(7)
    df = df.astype(float).round(2)
    df = df.head(6) # remove cluster
    df['pooltype'] = df.index
    df['pooltype'] = df['pooltype'].astype(str)
    print(df)

    df_both = df.merge(df2, how='inner', on='pooltype')
    print(df_both)
    df_both = df_both.sort_values('total time', ascending=True)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'standard_times_type_totals',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(name="algorithm only", y=df_both['pooltype'], x=df_both['algorithm only'], text=df_both['algorithm only'], orientation='h', marker=dict(color=approach_colors[0])),
            go.Bar(name="total time", y=df_both['pooltype'], x=df_both['total time'], text=df_both['total time'], orientation='h', marker=dict(color='blue')),
        ],
    ).update_layout(
        xaxis_title="Time (in seconds)",
        yaxis_title=None,
        font_size=40,
        legend_title=None,
        barmode='group',
        xaxis = dict(
            #tickmode = 'linear',
            tick0 = 0,
            #dtick = 10,
        ),
        xaxis_range=[0,24],
        legend=dict(
            yanchor="bottom",
            y=0.05,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=40,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=50,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

def ii_vs_standard_type_totals():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1

    df_og = pd.DataFrame(columns=['pooltype', 'original'])
    secondary = df['times_secondary'].mul(5).sum()
    primary = df['times_primary'].mul(2).sum()
    work = df['times_workplace'].mul(5).sum()
    k12school = df['times_k12school'].mul(5).sum()
    college = df['times_college'].mul(5).sum()
    household = df['times_household'].mul(7).sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_og.loc[i] = [pooltype[i]] + [times[i]]

    df_og['original'] = df_og['original'].div(1000000).div(7)
    df_og['original'] = df_og['original'].astype(float).round(2)

    # Don't show zero values
    df_og.replace(0, NaN, inplace=True)

    df_og['pooltype'] = df_og['pooltype'].astype(str)
    print(df_og)

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1

    df_ii = pd.DataFrame(columns=['pooltype', 'iterative intervals'])
    secondary = df['times_secondary'].mul(5).sum()
    primary = df['times_primary'].mul(2).sum()
    work = df['times_workplace'].mul(5).sum()
    k12school = df['times_k12school'].mul(5).sum()
    college = df['times_college'].mul(5).sum()
    household = df['times_household'].mul(7).sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_ii.loc[i] = [pooltype[i]] + [times[i]]

    df_ii['iterative intervals'] = df_ii['iterative intervals'].div(1000000).div(7)
    df_ii['iterative intervals'] = df_ii['iterative intervals'].astype(float).round(2)

    # Don't show zero values
    df_ii.replace(0, NaN, inplace=True)

    df_ii['pooltype'] = df_ii['pooltype'].astype(str)
    print(df_ii)

    df_both = df_ii.merge(df_og, how='inner', on='pooltype')
    print(df_both)
    df_both = df_both.sort_values('original', ascending=True)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'ii_vs_standard_type_totals',
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(
                name="iterative intervals",
                y=df_both['pooltype'],
                x=df_both['iterative intervals'],
                text=df_both['iterative intervals'],
                orientation='h',
                marker=dict(color=approach_colors[1]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="original",
                y=df_both['pooltype'],
                x=df_both['original'],
                text=df_both['original'],
                orientation='h',
                marker=dict(color=approach_colors[0]),
                texttemplate="%{x:.2f}",
            ),
        ],
    ).update_layout(
        xaxis_title="Time (in seconds)",
        yaxis_title=None,
        font_size=40,
        legend_title=None,
        barmode='group',
        xaxis = dict(
            #tickmode = 'linear',
            tick0 = 0,
            #dtick = 10,
        ),
        xaxis_range=[0,24],
        legend=dict(
            yanchor="bottom",
            y=0.05,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        #legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=35,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=50,
        showgrid=False,
        #gridwidth=5,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

def ii_type_averages():
    iterative_intervals_type_averages_primary()
    iterative_intervals_type_averages_secondary()
    iterative_intervals_type_averages_workplace()
    iterative_intervals_type_averages_k12school()
    iterative_intervals_type_averages_college()

if __name__=="__main__":
    #standard_all_averages()
    #standard_all_totals()
    #standard_all_totals_weekly()
    #standard_type_totals_weekly()
    #standard_type_totals_overhead_weekly()
    #standard_type_totals_both()
    #ii_type_averages()
    ii_vs_standard_type_totals()