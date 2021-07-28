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
sampling_with_iteration_path = "3-sampling_with_iteration/"
full_sampling_path = "4-full_sampling/"
adjusted_full_sampling_path = "5-adjusted_full_sampling/"
good_full_sampling_path = "6-good_full_sampling/"
old_full_sampling = "full_sampling initially/"

filename = "all_1_times_counts.csv"
filename_ptype = "all_1_times_counts_pType.csv"
filename_psize = "all_1_times_counts_pSize.csv"

section_colors= ["#eda189", "#bfacd6", "#c7b526", "#25c9ae"]
threads_colors = ["#542e71", "#fb3640", "#fdca40", "#a799b7"]
comparison_section_colors= ["#FFF700", "#2BD8E7", "#B3AD00", "#2F8F97"]
approach_colors = ["#FDAA10","#14B37D","#64afff","#1f4397", "#FF9999", "#C20000", "#722D8E", "#E153E6"]

gridwidth = 2
linewidth = 5
xtitle_standoff = 25
ytitle_standoff = 40

###########################################
def get_basis_df():
    df = pd.read_csv(vsc_results_path + basis_path + filename)
    df.index += 1

    df_og = pd.DataFrame(columns=['pooltype', 'basis'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_og.loc[i] = [pooltype[i]] + [times[i]]

    df_og['basis'] = df_og['basis'].div(1000000)
    df_og['basis'] = df_og['basis'].astype(float).round(2)

    # Don't show zero values
    df_og.replace(0, NaN, inplace=True)

    df_og['pooltype'] = df_og['pooltype'].astype(str)

    return df_og

def get_standard_df():
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1

    df_og = pd.DataFrame(columns=['pooltype', 'original'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_og.loc[i] = [pooltype[i]] + [times[i]]

    df_og['original'] = df_og['original'].div(1000000)
    df_og['original'] = df_og['original'].astype(float).round(2)

    # Don't show zero values
    df_og.replace(0, NaN, inplace=True)

    df_og['pooltype'] = df_og['pooltype'].astype(str)

    return df_og

def get_ii_df():
    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1

    df_ii = pd.DataFrame(columns=['pooltype', 'iterative intervals'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_ii.loc[i] = [pooltype[i]] + [times[i]]

    df_ii['iterative intervals'] = df_ii['iterative intervals'].div(1000000)
    df_ii['iterative intervals'] = df_ii['iterative intervals'].astype(float).round(2)

    # Don't show zero values
    df_ii.replace(0, NaN, inplace=True)

    df_ii['pooltype'] = df_ii['pooltype'].astype(str)

    return df_ii

def get_swi_df():
    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1

    df_swi = pd.DataFrame(columns=['pooltype', 'sampling with iteration'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_swi.loc[i] = [pooltype[i]] + [times[i]]

    df_swi['sampling with iteration'] = df_swi['sampling with iteration'].div(1000000)
    df_swi['sampling with iteration'] = df_swi['sampling with iteration'].astype(float).round(2)

    # Don't show zero values
    df_swi.replace(0, NaN, inplace=True)

    df_swi['pooltype'] = df_swi['pooltype'].astype(str)

    return df_swi

def get_old_fs_pType_df():
    df = pd.read_csv(vsc_results_path + old_full_sampling + filename_ptype)
    df.index += 1

    df_fs = pd.DataFrame(columns=['pooltype', 'full sampling'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_fs.loc[i] = [pooltype[i]] + [times[i]]

    df_fs['full sampling'] = df_fs['full sampling'].div(1000000)
    df_fs['full sampling'] = df_fs['full sampling'].astype(float).round(2)

    # Don't show zero values
    df_fs.replace(0, NaN, inplace=True)

    df_fs['pooltype'] = df_fs['pooltype'].astype(str)

    return df_fs

def get_old_fs_pSize_df():
    df = pd.read_csv(vsc_results_path + old_full_sampling + filename_psize)
    df.index += 1

    df_fs2 = pd.DataFrame(columns=['pooltype', 'full sampling (>150)'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_fs2.loc[i] = [pooltype[i]] + [times[i]]

    df_fs2['full sampling (>150)'] = df_fs2['full sampling (>150)'].div(1000000)
    df_fs2['full sampling (>150)'] = df_fs2['full sampling (>150)'].astype(float).round(2)

    # Don't show zero values
    df_fs2.replace(0, NaN, inplace=True)

    df_fs2['pooltype'] = df_fs2['pooltype'].astype(str)

    return df_fs2

def get_new_fs_pType_df():
    df = pd.read_csv(vsc_results_path + full_sampling_path + filename)
    df.index += 1

    df_fs = pd.DataFrame(columns=['pooltype', 'new full sampling'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_fs.loc[i] = [pooltype[i]] + [times[i]]

    df_fs['new full sampling'] = df_fs['new full sampling'].div(1000000)
    df_fs['new full sampling'] = df_fs['new full sampling'].astype(float).round(2)

    # Don't show zero values
    df_fs.replace(0, NaN, inplace=True)

    df_fs['pooltype'] = df_fs['pooltype'].astype(str)

    return df_fs

def get_new_fs_pSize_df():
    df = pd.read_csv(vsc_results_path + adjusted_full_sampling_path + filename)
    df.index += 1

    df_fs = pd.DataFrame(columns=['pooltype', 'new full sampling (>150)'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_fs.loc[i] = [pooltype[i]] + [times[i]]

    df_fs['new full sampling (>150)'] = df_fs['new full sampling (>150)'].div(1000000)
    df_fs['new full sampling (>150)'] = df_fs['new full sampling (>150)'].astype(float).round(2)

    # Don't show zero values
    df_fs.replace(0, NaN, inplace=True)

    df_fs['pooltype'] = df_fs['pooltype'].astype(str)

    return df_fs

def get_fsuc_pType_df():
    df = pd.read_csv(vsc_results_path + good_full_sampling_path + filename)
    df.index += 1

    df_fs = pd.DataFrame(columns=['pooltype', 'full sampling unique contacts'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_fs.loc[i] = [pooltype[i]] + [times[i]]

    df_fs['full sampling unique contacts'] = df_fs['full sampling unique contacts'].div(1000000)
    df_fs['full sampling unique contacts'] = df_fs['full sampling unique contacts'].astype(float).round(2)

    # Don't show zero values
    df_fs.replace(0, NaN, inplace=True)

    df_fs['pooltype'] = df_fs['pooltype'].astype(str)

    return df_fs

def get_fsuc_pSize_df():
    df = pd.read_csv(vsc_results_path + good_full_sampling_path + "all_1_times_counts_pSize150.csv")
    df.index += 1

    df_fs = pd.DataFrame(columns=['pooltype', 'full sampling unique contacts (>150)'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_fs.loc[i] = [pooltype[i]] + [times[i]]

    df_fs['full sampling unique contacts (>150)'] = df_fs['full sampling unique contacts (>150)'].div(1000000)
    df_fs['full sampling unique contacts (>150)'] = df_fs['full sampling unique contacts (>150)'].astype(float).round(2)

    # Don't show zero values
    df_fs.replace(0, NaN, inplace=True)

    df_fs['pooltype'] = df_fs['pooltype'].astype(str)

    return df_fs

def get_basis_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + basis_path + filename)
    df.index += 1
    df_basis = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_basis['totals'] = df['times_' + pooltype]
    df_basis['totals'] = df_basis['totals'].div(1000)
    df_basis['counts'] = df['counts_' + pooltype]
    df_basis['averages'] = df_basis['totals'] / df_basis['counts']
    return df_basis

def get_standard_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pooltype]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pooltype]
    df_or['averages'] = df_or['totals'] / df_or['counts']
    return df_or

def get_ii_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pooltype]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pooltype]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']
    return df_ii

def get_swi_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pooltype]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pooltype]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']
    return df_swi

def get_old_fs_pType_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + old_full_sampling + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pooltype]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pooltype]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']
    return df_fs

def get_old_fs_pSize_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + old_full_sampling + filename_psize)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pooltype]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pooltype]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']
    return df_fs

def get_new_fs_pType_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + full_sampling_path + filename)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pooltype]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pooltype]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']
    return df_fs

def get_new_fs_pSize_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + adjusted_full_sampling_path + filename)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pooltype]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pooltype]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']
    return df_fs

def get_gfs_pType_averages_df(pooltype):
    df = pd.read_csv(vsc_results_path + good_full_sampling_path + filename)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pooltype]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pooltype]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']
    return df_fs

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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        title_standoff=ytitle_standoff,
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        title_standoff=ytitle_standoff,
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        title_standoff=ytitle_standoff,
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
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
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
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
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
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        title_standoff=ytitle_standoff,
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        title_standoff=ytitle_standoff,
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        title_standoff=ytitle_standoff,
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        title_standoff=ytitle_standoff,
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        title_standoff=ytitle_standoff,
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
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

def ii_vs_standard_type_totals():
    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

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
        xaxis_range=[0,32],
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
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
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

#---------- 3-Sampling with iteration ----------

#----- pType
def swi_pType_averages_primary_full():
    pType = 'primary'
    mode = 'markers'
    fn = "times_avg_swi_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pType_averages_secondary_full():
    pType = 'secondary'
    mode = 'markers'
    fn = "times_avg_swi_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pType_averages_workplace_full():
    pType = 'workplace'
    mode = 'markers'
    fn = "times_avg_swi_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pType_averages_primary():
    pType = 'primary'
    mode = 'lines'
    fn = "times_avg_swi_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pType_averages_secondary():
    pType = 'secondary'
    mode = 'lines'
    fn = "times_avg_swi_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pType_averages_workplace():
    pType = 'workplace'
    mode = 'lines'
    fn = "times_avg_swi_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pType_averages_k12school():
    pType = 'k12school'
    mode='lines'
    fn = "times_avg_swi_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals']
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals']
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals']
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in microseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,10],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=4,
        ),
    )
    fig.show(config=conf)

def swi_pType_averages_college():
    pType = 'college'
    mode='lines'
    fn = "times_avg_swi_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals']
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals']
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals']
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in microseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,20],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=4,
        ),
    )
    fig.show(config=conf)

def swi_pType_averages():
    swi_pType_averages_primary_full()
    swi_pType_averages_secondary_full()
    swi_pType_averages_workplace_full()

    swi_pType_averages_primary()
    swi_pType_averages_secondary()
    swi_pType_averages_workplace()
    swi_pType_averages_k12school()
    swi_pType_averages_college()

def swi_pType_vs_rest_type_totals():
    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

    #------ SWI pType
    df_swi = get_swi_df()

    df_both = df_ii.merge(df_og, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi, how='inner', on='pooltype')
    print(df_both)
    df_both = df_both.sort_values('original', ascending=True)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'swi_vs_rest_type_totals',
            'height': 1350,
            'width': 1832,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(
                name="sampling with iteration",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration'],
                text=df_both['sampling with iteration'],
                orientation='h',
                marker=dict(color=approach_colors[2]),
                texttemplate="%{x:.2f}",
            ),
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
        xaxis_range=[0,32],
        legend=dict(
            yanchor="bottom",
            y=0.03,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

#----- pSize
def swi_pSize_averages_primary():
    pType = 'primary'
    mode = 'lines'
    fn = "times_avg_swi_pSize_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_psize)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pSize_averages_secondary():
    pType = 'secondary'
    mode = 'lines'
    fn = "times_avg_swi_pSize_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_psize)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pSize_averages_workplace():
    pType = 'workplace'
    mode = 'lines'
    fn = "times_avg_swi_pSize_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_psize)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def swi_pSize_averages_k12school():
    pType = 'k12school'
    mode='lines'
    fn = "times_avg_swi_pSize_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_psize)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in microseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,0.02],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=4,
        ),
    )
    fig.show(config=conf)

def swi_pSize_averages_college():
    pType = 'college'
    mode='lines'
    fn = "times_avg_swi_pSize_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_psize)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in microseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,0.02],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=4,
        ),
    )
    fig.show(config=conf)

def swi_pSize_averages():
    swi_pSize_averages_primary()
    swi_pSize_averages_secondary()
    swi_pSize_averages_workplace()
    swi_pSize_averages_k12school()
    swi_pSize_averages_college()

def swi_pSize_vs_rest_type_totals():
    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

    #------ SWI pType
    df_swi = get_swi_df()

    #------ SWI pSize
    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_psize)
    df.index += 1

    df_swi2 = pd.DataFrame(columns=['pooltype', 'sampling with iteration (>150)'])
    secondary = df['times_secondary'].sum()
    primary = df['times_primary'].sum()
    work = df['times_workplace'].sum()
    k12school = df['times_k12school'].sum()
    college = df['times_college'].sum()
    household = df['times_household'].sum()
    
    #results = {'secondary': secondary, 'primary': primary, 'work': work, 'k12-school': k12school, 'college': college, 'household': household}
    pooltype =  ['Secondary', 'Primary', 'Workplace', 'K-12 school', 'College', 'Household']
    times = [secondary, primary, work, k12school, college, household]

    for i in range(len(pooltype)):
        df_swi2.loc[i] = [pooltype[i]] + [times[i]]

    df_swi2['sampling with iteration (>150)'] = df_swi2['sampling with iteration (>150)'].div(1000000)
    df_swi2['sampling with iteration (>150)'] = df_swi2['sampling with iteration (>150)'].astype(float).round(2)

    # Don't show zero values
    df_swi2.replace(0, NaN, inplace=True)

    df_swi2['pooltype'] = df_swi2['pooltype'].astype(str)

    df_both = df_ii.merge(df_og, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi2, how='inner', on='pooltype')
    df_both = df_both.sort_values('original', ascending=True)
    print(df_both)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'swi_pSize_vs_rest_type_totals',
            'height': 1350,
            'width': 1832,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(
                name="sampling with iteration (>150)",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration (>150)'],
                text=df_both['sampling with iteration (>150)'],
                orientation='h',
                marker=dict(color=approach_colors[3]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="sampling with iteration",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration'],
                text=df_both['sampling with iteration'],
                orientation='h',
                marker=dict(color=approach_colors[2]),
                texttemplate="%{x:.2f}",
            ),
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
        xaxis_range=[0,32],
        legend=dict(
            yanchor="bottom",
            y=0.03,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)


#---------- 4-Full sampling ----------

#----- pType
def fs_pType_averages_primary_full():
    pooltype = 'primary'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_fs = get_old_fs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pType_averages_secondary_full():
    pType = 'secondary'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pType_averages_workplace_full():
    pType = 'workplace'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pType_averages_primary():
    pType = 'primary'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pType_averages_secondary():
    pType = 'secondary'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pType_averages_workplace():
    pType = 'workplace'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pType_averages_k12school():
    pType = 'k12school'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals']
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals']
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals']
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals']
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in microseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,40],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="right",
            x=0.90,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pType_averages_college():
    pType = 'college'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals']
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals']
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals']
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals']
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in microseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,30],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pType_averages():
    fs_pType_averages_primary_full()
    fs_pType_averages_secondary_full()
    fs_pType_averages_workplace_full()
    fs_pType_averages_primary()
    fs_pType_averages_secondary()
    fs_pType_averages_workplace()
    fs_pType_averages_k12school()
    fs_pType_averages_college()

def fs_pType_vs_rest_type_totals():
    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

    #------ SWI pType
    df_swi = get_swi_df()

    #------ FS pType
    df_fs = get_old_fs_pType_df()

    df_both = df_ii.merge(df_og, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs, how='inner', on='pooltype')
    df_both = df_both.sort_values('original', ascending=True)
    print(df_both)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'fs_pType_vs_rest_type_totals',
            'height': 1350,
            'width': 1832,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(
                name="full sampling",
                y=df_both['pooltype'],
                x=df_both['full sampling'],
                text=df_both['full sampling'],
                orientation='h',
                marker=dict(color=approach_colors[4]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="sampling with iteration",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration'],
                text=df_both['sampling with iteration'],
                orientation='h',
                marker=dict(color=approach_colors[2]),
                texttemplate="%{x:.2f}",
            ),
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
        xaxis_range=[0,32],
        legend=dict(
            yanchor="bottom",
            y=0.03,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

#----- pSize
def fs_pSize_averages_primary_full():
    pooltype = 'primary'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_fs = get_old_fs_pType_averages_df(pooltype)

    df_fs2 = get_old_fs_pSize_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pSize_averages_secondary_full():
    pType = 'secondary'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pSize_averages_workplace_full():
    pType = 'workplace'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pSize_averages_primary():
    pType = 'primary'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pSize_averages_secondary():
    pType = 'secondary'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pSize_averages_workplace():
    pType = 'workplace'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,300],
        yaxis_range=[0,0.5],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pSize_averages_k12school():
    pType = 'k12school'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,0.04],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="right",
            x=0.90,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pSize_averages_college():
    pType = 'college'
    mode = 'lines'
    fn = "times_avg_fs_pType_"

    df = pd.read_csv(vsc_results_path + standard_path + filename)
    df.index += 1
    df_or = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_or['totals'] = df['times_' + pType]
    df_or['totals'] = df_or['totals'].div(1000)
    df_or['counts'] = df['counts_' + pType]
    df_or['averages'] = df_or['totals'] / df_or['counts']

    df = pd.read_csv(vsc_results_path + iterative_intervals_path + filename)
    df.index += 1
    df_ii = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_ii['totals'] = df['times_' + pType]
    df_ii['totals'] = df_ii['totals'].div(1000)
    df_ii['counts'] = df['counts_' + pType]
    df_ii['averages'] = df_ii['totals'] / df_ii['counts']

    df = pd.read_csv(vsc_results_path + sampling_with_iteration_path + filename_ptype)
    df.index += 1
    df_swi = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_swi['totals'] = df['times_' + pType]
    df_swi['totals'] = df_swi['totals'].div(1000)
    df_swi['counts'] = df['counts_' + pType]
    df_swi['averages'] = df_swi['totals'] / df_swi['counts']

    df = pd.read_csv(vsc_results_path + full_sampling_path + filename_ptype)
    df.index += 1
    df_fs = pd.DataFrame(columns=['totals', 'counts', 'averages'])
    df_fs['totals'] = df['times_' + pType]
    df_fs['totals'] = df_fs['totals'].div(1000)
    df_fs['counts'] = df['counts_' + pType]
    df_fs['averages'] = df_fs['totals'] / df_fs['counts']

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pType,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,0.03],
        legend=dict(
            yanchor="top",
            y=0.91,
            xanchor="left",
            x=0.10,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fs_pSize_averages():
    fs_pSize_averages_primary_full()
    fs_pSize_averages_secondary_full()
    fs_pSize_averages_workplace_full()
    fs_pSize_averages_primary()
    fs_pSize_averages_secondary()
    fs_pSize_averages_workplace()
    fs_pSize_averages_k12school()
    fs_pSize_averages_college()

def fs_pSize_vs_rest_type_totals():
    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

    #------ SWI pType
    df_swi = get_swi_df()

    #------ FS pType
    df_fs = get_old_fs_pType_df()

    #------ FS pSize
    df_fs2 = get_old_fs_pSize_df()

    df_both = df_ii.merge(df_og, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs2, how='inner', on='pooltype')
    df_both = df_both.sort_values('original', ascending=True)
    print(df_both)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'fs_pSize_vs_rest_type_totals',
            'height': 1800,
            'width': 1832,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(
                name="full sampling (>150)",
                y=df_both['pooltype'],
                x=df_both['full sampling (>150)'],
                text=df_both['full sampling (>150)'],
                orientation='h',
                marker=dict(color=approach_colors[5]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="full sampling",
                y=df_both['pooltype'],
                x=df_both['full sampling'],
                text=df_both['full sampling'],
                orientation='h',
                marker=dict(color=approach_colors[4]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="sampling with iteration",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration'],
                text=df_both['sampling with iteration'],
                orientation='h',
                marker=dict(color=approach_colors[2]),
                texttemplate="%{x:.2f}",
            ),
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
        xaxis_range=[0,32],
        legend=dict(
            yanchor="bottom",
            y=0.02,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

####################################

def differents_fs():
    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

    #------ SWI pType
    df_swi = get_swi_df()

    #------ FS pType
    df_fs = get_old_fs_pType_df()

    #------ FS pSize
    df_fs2 = get_old_fs_pSize_df()

    #------ NEW FS pType
    df_new_fs = get_new_fs_pType_df()

    #------ NEW FS pType
    df_new_fs2 = get_new_fs_pSize_df()

    df_both = df_ii.merge(df_og, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs2, how='inner', on='pooltype')
    df_both = df_both.merge(df_new_fs, how='inner', on='pooltype')
    df_both = df_both.merge(df_new_fs2, how='inner', on='pooltype')
    df_both = df_both.sort_values('original', ascending=True)
    print(df_both)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'different_fs',
            'height': 1350,
            'width': 1832,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(
                name="new full sampling (>150)",
                y=df_both['pooltype'],
                x=df_both['new full sampling (>150)'],
                text=df_both['new full sampling (>150)'],
                orientation='h',
                marker=dict(color='grey'),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="new full sampling",
                y=df_both['pooltype'],
                x=df_both['new full sampling'],
                text=df_both['new full sampling'],
                orientation='h',
                marker=dict(color='black'),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="full sampling (>150)",
                y=df_both['pooltype'],
                x=df_both['full sampling (>150)'],
                text=df_both['full sampling (>150)'],
                orientation='h',
                marker=dict(color=approach_colors[5]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="full sampling",
                y=df_both['pooltype'],
                x=df_both['full sampling'],
                text=df_both['full sampling'],
                orientation='h',
                marker=dict(color=approach_colors[4]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="sampling with iteration",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration'],
                text=df_both['sampling with iteration'],
                orientation='h',
                marker=dict(color=approach_colors[2]),
                texttemplate="%{x:.2f}",
            ),
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
        xaxis_range=[0,32],
        legend=dict(
            yanchor="bottom",
            y=0.03,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

def afs_averages_primary_full():
    pooltype = 'primary'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def afs_averages_secondary_full():
    pooltype = 'secondary'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def afs_averages_workplace_full():
    pooltype = 'workplace'
    mode = 'markers'
    fn = "times_avg_fs_pType_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
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
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

######################""

def fsuc_averages_primary_full():
    pooltype = 'primary'
    mode = 'markers'
    fn = "times_avg_fsuc_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    df_fsuc = get_gfs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            #go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
            go.Scatter(name="Full sampling unique contacts", y=df_fsuc['averages'], mode=mode, marker=dict(color=approach_colors[6])),
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
            y=0.96,
            xanchor="left",
            x=0.02,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fsuc_averages_secondary_full():
    pooltype = 'secondary'
    mode = 'markers'
    fn = "times_avg_fsuc_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    df_fsuc = get_gfs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            #go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
            go.Scatter(name="Full sampling unique contacts", y=df_fsuc['averages'], mode=mode, marker=dict(color=approach_colors[6])),
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
            y=0.96,
            xanchor="left",
            x=0.02,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fsuc_averages_workplace_full():
    pooltype = 'workplace'
    mode = 'markers'
    fn = "times_avg_fsuc_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    df_fsuc = get_gfs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype + "_full",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            #go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
            go.Scatter(name="Full sampling unique contacts", y=df_fsuc['averages'], mode=mode, marker=dict(color=approach_colors[6])),
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
            y=0.96,
            xanchor="left",
            x=0.02,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fsuc_averages_primary():
    pooltype = 'primary'
    mode = 'lines'
    fn = "times_avg_fsuc_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    df_fsuc = get_gfs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            #go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
            go.Scatter(name="Full sampling unique contacts", y=df_fsuc['averages'], mode=mode, marker=dict(color=approach_colors[6])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,400],
        yaxis_range=[0,.5],
        legend=dict(
            yanchor="top",
            y=0.96,
            xanchor="left",
            x=0.02,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fsuc_averages_secondary():
    pooltype = 'secondary'
    mode = 'lines'
    fn = "times_avg_fsuc_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    df_fsuc = get_gfs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            #go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
            go.Scatter(name="Full sampling unique contacts", y=df_fsuc['averages'], mode=mode, marker=dict(color=approach_colors[6])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,400],
        yaxis_range=[0,.5],
        legend=dict(
            yanchor="top",
            y=0.96,
            xanchor="left",
            x=0.02,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fsuc_averages_workplace():
    pooltype = 'workplace'
    mode = 'lines'
    fn = "times_avg_fsuc_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    df_fsuc = get_gfs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            #go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
            go.Scatter(name="Full sampling unique contacts", y=df_fsuc['averages'], mode=mode, marker=dict(color=approach_colors[6])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,400],
        yaxis_range=[0,.5],
        legend=dict(
            yanchor="top",
            y=0.96,
            xanchor="left",
            x=0.02,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fsuc_averages_k12school():
    pooltype = 'k12school'
    mode = 'lines'
    fn = "times_avg_fsuc_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    df_fsuc = get_gfs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            #go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
            go.Scatter(name="Full sampling unique contacts", y=df_fsuc['averages'], mode=mode, marker=dict(color=approach_colors[6])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,30],
        yaxis_range=[0,0.05],
        legend=dict(
            yanchor="top",
            y=0.96,
            xanchor="left",
            x=0.02,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fsuc_averages_college():
    pooltype = 'college'
    mode = 'lines'
    fn = "times_avg_fsuc_"

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_old_fs = get_old_fs_pType_averages_df(pooltype)

    df_new_fs = get_new_fs_pType_averages_df(pooltype)

    df_fsuc = get_gfs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': fn + pooltype,
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original all-to-all", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Full sampling", y=df_old_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
            #go.Scatter(name="New full sampling", y=df_new_fs['averages'], mode=mode, marker=dict(color='black')),
            go.Scatter(name="Full sampling unique contacts", y=df_fsuc['averages'], mode=mode, marker=dict(color=approach_colors[6])),
        ],
    ).update_layout(
        xaxis_title="Pool size",
        yaxis_title="Time (in milliseconds)",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,51],
        yaxis_range=[0,0.05],
        legend=dict(
            yanchor="top",
            y=0.96,
            xanchor="left",
            x=0.02,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def fsuc():
    fsuc_averages_primary_full()
    fsuc_averages_secondary_full()
    fsuc_averages_workplace_full()
    fsuc_averages_primary()
    fsuc_averages_secondary()
    fsuc_averages_workplace()
    fsuc_averages_k12school()
    fsuc_averages_college()

def fsuc_pType_vs_rest_type_totals():
    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

    #------ SWI pType
    df_swi = get_swi_df()

    #------ FS pType
    df_fs = get_old_fs_pType_df()

    #------ FS pSize
    df_fs2 = get_old_fs_pSize_df()

    df_fsuc_pType = get_fsuc_pType_df()

    df_both = df_ii.merge(df_og, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs2, how='inner', on='pooltype')
    df_both = df_both.merge(df_fsuc_pType, how='inner', on='pooltype')
    df_both = df_both.sort_values('original', ascending=True)
    print(df_both)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'fsuc_pType_vs_rest_type_totals',
            'height': 2100,
            'width': 1832,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
                go.Bar(
                name="full sampling unique contacts",
                y=df_both['pooltype'],
                x=df_both['full sampling unique contacts'],
                text=df_both['full sampling unique contacts'],
                orientation='h',
                marker=dict(color=approach_colors[6]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="full sampling (>150)",
                y=df_both['pooltype'],
                x=df_both['full sampling (>150)'],
                text=df_both['full sampling (>150)'],
                orientation='h',
                marker=dict(color=approach_colors[5]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="full sampling",
                y=df_both['pooltype'],
                x=df_both['full sampling'],
                text=df_both['full sampling'],
                orientation='h',
                marker=dict(color=approach_colors[4]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="sampling with iteration",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration'],
                text=df_both['sampling with iteration'],
                orientation='h',
                marker=dict(color=approach_colors[2]),
                texttemplate="%{x:.2f}",
            ),
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
        xaxis_range=[0,32],
        legend=dict(
            yanchor="bottom",
            y=0.02,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)

def fsuc_pSize_vs_rest_type_totals():
    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

    #------ SWI pType
    df_swi = get_swi_df()

    #------ FS pType
    df_fs = get_old_fs_pType_df()

    #------ FS pSize
    df_fs2 = get_old_fs_pSize_df()

    #------ FSUC pType
    df_fsuc_pType = get_fsuc_pType_df()

    #------ FSUC pType
    df_fsuc_pSize = get_fsuc_pSize_df()

    df_both = df_ii.merge(df_og, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs2, how='inner', on='pooltype')
    df_both = df_both.merge(df_fsuc_pType, how='inner', on='pooltype')
    df_both = df_both.merge(df_fsuc_pSize, how='inner', on='pooltype')
    df_both = df_both.sort_values('original', ascending=True)
    print(df_both)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'fsuc_pSize_vs_rest_type_totals',
            'height': 2400,
            'width': 1832,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(
                name="full sampling unique contacts (>150)",
                y=df_both['pooltype'],
                x=df_both['full sampling unique contacts (>150)'],
                text=df_both['full sampling unique contacts (>150)'],
                orientation='h',
                marker=dict(color=approach_colors[7]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="full sampling unique contacts",
                y=df_both['pooltype'],
                x=df_both['full sampling unique contacts'],
                text=df_both['full sampling unique contacts'],
                orientation='h',
                marker=dict(color=approach_colors[6]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="full sampling (>150)",
                y=df_both['pooltype'],
                x=df_both['full sampling (>150)'],
                text=df_both['full sampling (>150)'],
                orientation='h',
                marker=dict(color=approach_colors[5]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="full sampling",
                y=df_both['pooltype'],
                x=df_both['full sampling'],
                text=df_both['full sampling'],
                orientation='h',
                marker=dict(color=approach_colors[4]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="sampling with iteration",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration'],
                text=df_both['sampling with iteration'],
                orientation='h',
                marker=dict(color=approach_colors[2]),
                texttemplate="%{x:.2f}",
            ),
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
        xaxis_range=[0,32],
        legend=dict(
            yanchor="bottom",
            y=0.02,
            xanchor="right",
            x=0.98,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)


def vulgariserend_artikel():
    pooltype = 'primary'
    mode = 'markers'

    df_basis = get_basis_averages_df(pooltype)

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_fs = get_old_fs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': "simulatietijd",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Origineel", y=df_basis['averages'], mode=mode, marker=dict(color='darkblue')),
            go.Scatter(name="Één ampersand toevoegen", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            go.Scatter(name="Indelen in leeftijdsgroepen", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            go.Scatter(name="Contact staaltje nemen", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            go.Scatter(name="Extra verbetering", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        title={
        'text': "Simulatie-tijd per aanpassing",
        'y':0.96,
        'x':0.50,
        'xanchor': 'center',
        'yanchor': 'top'
        },
        xaxis_title="Bubbel grootte",
        yaxis_title="Milliseconden",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,1450],
        yaxis_range=[-0.05,20],
        legend=dict(
            yanchor="top",
            y=0.892,
            xanchor="left",
            x=0.138,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=25,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)

def vulgariserend_artikel_typetotals():
    df_basis = get_basis_df()
    df_basis = df_basis.head(1)
    print(df_basis)

    df_og = get_standard_df()

    #------ II
    df_ii = get_ii_df()

    #------ SWI pType
    df_swi = get_swi_df()

    #------ FS pSize
    df_fs = get_old_fs_pSize_df()


    df_both = df_basis.merge(df_og, how='inner', on='pooltype')
    df_both = df_both.merge(df_ii, how='inner', on='pooltype')
    df_both = df_both.merge(df_swi, how='inner', on='pooltype')
    df_both = df_both.merge(df_fs, how='inner', on='pooltype')
    df_both = df_both.sort_values('original', ascending=True)
    print(df_both)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'snelheidswinst',
            'height': 700,
            #'width': 1832,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Bar(
                name="Extra verbetering",
                y=df_both['pooltype'],
                x=df_both['full sampling (>150)'],
                orientation='h',
                marker=dict(color=approach_colors[4]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="Contact staaltje nemen",
                y=df_both['pooltype'],
                x=df_both['sampling with iteration'],
                orientation='h',
                marker=dict(color=approach_colors[2]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="Indelen in leeftijdsgroepen",
                y=df_both['pooltype'],
                x=df_both['iterative intervals'],
                orientation='h',
                marker=dict(color=approach_colors[1]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="Één ampersand toevoegen",
                y=df_both['pooltype'],
                x=df_both['original'],
                orientation='h',
                marker=dict(color=approach_colors[0]),
                texttemplate="%{x:.2f}",
            ),
            go.Bar(
                name="Origineel",
                y=df_both['pooltype'],
                x=df_both['basis'],
                orientation='h',
                marker=dict(color='darkblue'),
                texttemplate="%{x:.2f}",
            ),
        ],
    ).update_layout(
        title={
            'text': "Tijd per dag voor vrije tijd bubbels",
            'y':0.96,
            'x':0.54,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Seconden per dag",
        yaxis_title=None,
        font_size=40,
        legend_title=None,
        barmode='group',
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
        xaxis_range=[0,60],
        legend=dict(
            yanchor="bottom",
            y=0.02,
            xanchor="right",
            x=0.99,
            traceorder='normal',
        ),
        legend_traceorder='reversed',
        #yaxis={'categoryorder':'total descending'}
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        visible=False,
        title_standoff=ytitle_standoff,
        showgrid=False,
        #gridwidth=gridwidth,
        #gridcolor='white',
        ticks="outside",
        tickformat='',
    ). update_traces(
        textposition='outside',
        width=0.15,
    )
    fig.show(config=conf)
    #plotly.offline.plot(fig)


def presentation():
    pooltype = 'primary'
    mode = 'markers'

    df_basis = get_basis_averages_df(pooltype)

    df_or = get_standard_averages_df(pooltype)

    df_ii = get_ii_averages_df(pooltype)

    df_swi = get_swi_averages_df(pooltype)

    df_fs = get_old_fs_pType_averages_df(pooltype)

    conf = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': "presentation_times_counts",
            #'height': 600,
            #'width': 800,
            #'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    fig = go.Figure(
        data=[
            go.Scatter(name="Original (by value)", y=df_basis['averages'], mode=mode, marker=dict(color='darkblue')),
            go.Scatter(name="Original (by reference)", y=df_or['averages'], mode=mode, marker=dict(color=approach_colors[0])),
            #go.Scatter(name="Iterative intervals", y=df_ii['averages'], mode=mode, marker=dict(color=approach_colors[1])),
            #go.Scatter(name="Sampling with iteration", y=df_swi['averages'], mode=mode, marker=dict(color=approach_colors[2])),
            #go.Scatter(name="Full sampling (>150)", y=df_fs['averages'], mode=mode, marker=dict(color=approach_colors[4])),
        ],
    ).update_layout(
        title={
        'text': "Primary community infector",
        'y':0.96,
        'x':0.52,
        'xanchor': 'center',
        'yanchor': 'top'
        },
        xaxis_title="Pool size",
        yaxis_title="Milliseconds",
        font_size=40,
        legend_title=None,
        showlegend=True,
        xaxis_range=[0,1450],
        yaxis_range=[-0.05,20],
        legend=dict(
            yanchor="top",
            y=0.892,
            xanchor="left",
            x=0.138,
            traceorder='normal',
            itemsizing='constant'
        ),
    ).update_xaxes(
        title_standoff=xtitle_standoff,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
    ).update_yaxes(
        title_standoff=25,
        showgrid=True,
        gridwidth=gridwidth,
        gridcolor='white',
        ticks="outside",
        tickformat='',
    ).update_traces(
        line=dict(
            width=5
        ),
        marker=dict(
            size=5,
        ),
    )
    fig.show(config=conf)


if __name__=="__main__":
    #standard_all_averages()
    #standard_all_totals()
    #standard_all_totals_weekly()
    #standard_type_totals_weekly()
    #standard_type_totals_overhead_weekly()
    #standard_type_totals_both()
    #ii_type_averages()
    #ii_vs_standard_type_totals()
    #swi_pType_averages()
    #swi_pSize_averages()
    #swi_pType_vs_rest_type_totals()
    #fs_pType_averages()
    #fs_pType_vs_rest_type_totals()
    #fs_pSize_vs_rest_type_totals()
    #differents_fs()

    #---------- wrongnode adjustments
    #differents_fs()
    #afs_averages_primary_full()
    #afs_averages_workplace_full()
    #gfs_averages_workplace_full()
    #fsuc()
    #fsuc_pType_vs_rest_type_totals()
    #fsuc_pSize_vs_rest_type_totals()
    #fsuc_averages_secondary_full()
    #vulgariserend_artikel()
    #vulgariserend_artikel_typetotals()
    presentation()