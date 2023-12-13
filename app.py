import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import SymLogNorm

pd.set_option('mode.use_inf_as_na', True)
with np.errstate(invalid='ignore'):


    st.set_page_config(
        page_title="Shot Data Analysis",
        layout="wide"
    )

    # Read the data
    combined_shot_data = pd.read_csv('CombinedShotData.csv')
    league_stats = pd.read_csv('LeagueStats.csv')
    season_2002_shot_data = pd.read_csv('2002ShotData.csv')
    season_2022_shot_data = pd.read_csv('2022ShotData.csv')

    def calculate_percentage(df):
        total_shots = len(df)
        two_pointers = len(df[df['ShotType'] == '2-pointer'])
        three_pointers = len(df[df['ShotType'] == '3-pointer'])
        return (two_pointers / total_shots) * 100, (three_pointers / total_shots) * 100

    def plot_distance_histogram(data_list, colors, title, show_3point_line=True):
        sns.set(style="whitegrid")
        bin_edges = range(0, 36, 2)
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for i, data in enumerate(data_list):
            data['Distance (ft)'] = pd.to_numeric(data['Distance (ft)'], errors='coerce')
            with np.errstate(invalid='ignore'):  # Add this line
                sns.histplot(data['Distance (ft)'], bins=bin_edges, kde=False, alpha=0.6, ax=ax, color=colors[i], label=seasons[i])
        if show_3point_line:
            ax.axvline(x=24, color='red', linestyle='--', label='3-point Line')


        ax.set_xlabel('Distance (ft)')
        ax.set_ylabel('Frequency')
        ax.legend()
        return fig

    def plot_3pt_attempted_per_game(data):
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(data['Season'], data['3PA'], marker='o', linestyle='-', color='b', label='3PA', linewidth=2, markersize=8)
        ax.plot(data['Season'], data['3P'], marker='o', linestyle='-', color='r', label='3PM', linewidth=2, markersize=8)

        max_value = 40
        ax.set_ylim(0, max_value)
        ax.set_xlabel('Season')
        ax.set_ylabel('3-Pointers Attempted (3PA)')
        ax.set_xticks(data['Season'])  # Set ticks based on available seasons
        ax.set_xticklabels(data['Season'], rotation=45)  # Rotate tick labels
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.invert_xaxis()
        ax.legend()

        # Add a horizontal line at y=0 for better clarity
        ax.axhline(y=0, color='black', linewidth=0.5)

        return fig

    def plot_fg_attempted_per_game(data):
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(data['Season'], data['FGA'], marker='o', linestyle='-', color='b', label='FGA', linewidth=2, markersize=8)
        ax.plot(data['Season'], data['FG'], marker='o', linestyle='-', color='r', label='FGM', linewidth=2, markersize=8)

        max_value = 100
        ax.set_ylim(0, max_value)
        ax.set_xlabel('Season')
        ax.set_ylabel('Field Goals Attempted (FGA)')
        ax.set_xticks(data['Season'])  # Set ticks based on available seasons
        ax.set_xticklabels(data['Season'], rotation=45)  # Rotate tick labels
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.invert_xaxis()
        ax.legend()

        # Add a horizontal line at y=0 for better clarity
        ax.axhline(y=0, color='black', linewidth=0.5)

        return fig


    def plot_shot_heatmap(shot_data):
        heatmap, _, _ = np.histogram2d(shot_data['Top'], shot_data['Left'], bins=(70, 70))
        cmap = 'plasma'
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap, cmap=cmap, norm=SymLogNorm(linthresh=0.1),
                    xticklabels=False,
                    yticklabels=False, ax=ax)
        return fig

    def plot_shot_type_percentage(percentage, title, ax):
        labels = ['2-pointer', '3-pointer']
        colors = ['#ff9999', '#66b3ff']
        explode = (0.1, 0)

        ax.pie(percentage, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, explode=explode)

    def plot_shooting_percentage(data, selected_distance=None, st=None):
        # Assuming 'Distance' is a column in your dataset, and 'Result' indicates make or miss
        grouped_data = data.groupby(['Distance (ft)', 'Result']).size().unstack(fill_value=0)

        # Calculate percentage of makes and misses at each distance
        total_shots = grouped_data.sum(axis=1)
        make_percentage = (grouped_data['make'] / total_shots) * 100
        miss_percentage = (grouped_data['miss'] / total_shots) * 100

        # Sort the index for both make_percentage and miss_percentage
        make_percentage = make_percentage.sort_index()
        miss_percentage = miss_percentage.sort_index()

        # Define lighter shades of red and green
        light_green = '#8FED92'
        light_red = '#FF726E'

        # Plotting the data with lighter shades
        fig, ax = plt.subplots(figsize=(10, .5))
        ax.barh(make_percentage.index, make_percentage, height=0.05, color=light_green, label='Make')
        ax.barh(miss_percentage.index, miss_percentage, left=make_percentage, height=0.05, color=light_red, label='Miss')

        ax.set_xlabel('Percentage')



        # Remove y-axis
        ax.get_yaxis().set_visible(False)

        # Show plot only if a specific distance is not selected
        if selected_distance is None:
            return fig, ax
        else:
            st.pyplot(fig)



    # Streamlit App
    st.title('NBA Shot Data Analytics Dashboard')

    # Sidebar for user input (if any)



    # Display Plots
    st.markdown("<h3 style='text-align: center;'>NBA Shot Distance Histograms: 2002-03 and 2022-23 Seasons</h3>", unsafe_allow_html=True)

    data_list = [season_2002_shot_data, season_2022_shot_data]
    colors = ['blue', 'red']
    seasons = ['2002-2003 Season', '2022-2023 Season']

    show_3point_line = st.checkbox('Show 3-Point Line', value=True)

    fig_distance_histogram = plot_distance_histogram(data_list, colors, 'NBA Shot Distance Distribution - 2002-03 and 2022-23 Seasons', show_3point_line)
    st.pyplot(fig_distance_histogram)
    st.markdown("<medium style='text-align: center;'>This histogram illustrates the distribution of shot distances for the selected NBA seasons. Use the check box to add or remove the red dashed line that represents the 3-point line. The darker color shows the overlap between the two seasons.</small>", unsafe_allow_html=True)


    st.header('League Averages Over Seasons')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center;'>3-Pointers Attempted and Made Per Game</h3>", unsafe_allow_html=True)
        fig_3pt = plot_3pt_attempted_per_game(league_stats)
        st.pyplot(fig_3pt)
        st.markdown("<small style='text-align: center;'>This line graph shows the change in 3-pointers attempted and made per game over the last 20 years, notice the increase, especially in recent years.</small>", unsafe_allow_html=True)


    with col2:
        st.markdown("<h3 style='text-align: center;'>Field Goals Attempted and Made Per Game</h3>", unsafe_allow_html=True)
        fig_fg = plot_fg_attempted_per_game(league_stats)
        st.pyplot(fig_fg)
        st.markdown("<small style='text-align: center;'>This line graph shows the change in field goals attempted and made per game over the last 20 years, there is little change in the total number of shots taken per game.</small>", unsafe_allow_html=True)

    # Heatmaps


    st.header('Season Shooting Data')
    selected_season = st.selectbox('Select Season', ['2002-2003 Season', '2022-2023 Season'])

    # Create columns for heatmaps
    col3, col4 = st.columns(2)

    if selected_season == '2002-2003 Season':
        with col3:
            st.markdown("<h3 style='text-align: center;'>Shot Heat Map: 2002-2003 Season</h3>", unsafe_allow_html=True)

            fig_heatmap_2002 = plot_shot_heatmap(season_2002_shot_data)
            st.pyplot(fig_heatmap_2002)
            st.markdown("<small style='text-align: center;'>This heat map shows the location of shots on the court of the top 5 shooters, most shots are taken near basket with a fairly even distribution everywhere else.</small>", unsafe_allow_html=True)

        with col4:
            st.markdown("<h3 style='text-align: center;'>Shot Type Distribution: 2022-2023 Season</h3>", unsafe_allow_html=True)
            fig_pie_2002, ax_pie_2002 = plt.subplots(figsize=(5, 5))
            percentage_2002 = calculate_percentage(season_2002_shot_data)
            plot_shot_type_percentage(percentage_2002, 'Shot Type Percentage - 2002-03 Season', ax_pie_2002)
            st.pyplot(fig_pie_2002)
            st.markdown("<small style='text-align: center;'>This pie chart illustrates the distribution of shot type, about 1/5 of shots are beyond the 3-point line.</small>", unsafe_allow_html=True)

        
        st.markdown("<h3 style='text-align: center;'>Shooting Percentage by Distance: 2002-2003 Season</h3>", unsafe_allow_html=True)

        selected_distance = st.selectbox('Select a Distance:', sorted(season_2002_shot_data['Distance (ft)'].unique()[season_2002_shot_data['Distance (ft)'].unique() <= 29]))
        filtered_data = season_2002_shot_data[season_2002_shot_data['Distance (ft)'] == selected_distance]

        fig = plot_shooting_percentage(filtered_data, selected_distance, st)
        st.markdown("<medium style='text-align: center;'>Use the box above to select a distance and see the percentage of makes and misses. The green represents makes, the red represents misses.</small>", unsafe_allow_html=True)



    else:
        with col3:
            st.markdown("<h3 style='text-align: center;'>Shot Heat Map: 2002-2003 Season</h3>", unsafe_allow_html=True)

            fig_heatmap_2022 = plot_shot_heatmap(season_2022_shot_data)
            st.pyplot(fig_heatmap_2022)
            st.markdown("<small style='text-align: center;'>This heat map shows the location of shots on the court of the top 5 shooters, very few shots are taken right in front of the 3-point line, and there is a larger distribution of shots around the basket.</small>", unsafe_allow_html=True)


        with col4:
            st.markdown("<h3 style='text-align: center;'>Shot Type Distribution: 2022-2023 Season</h3>", unsafe_allow_html=True)
            fig_pie_2022, ax_pie_2022 = plt.subplots(figsize=(5, 5))
            percentage_2022 = calculate_percentage(season_2022_shot_data)
            plot_shot_type_percentage(percentage_2022, 'Shot Type Percentage - 2002-03 Season', ax_pie_2022)
            st.pyplot(fig_pie_2022)
            st.markdown("<small style='text-align: center;'>This pie chart illustrates the distribution of shot type, about 1/4 of shots are beyond the 3-point line.</small>", unsafe_allow_html=True)

        
        st.markdown("<h3 style='text-align: center;'>Shooting Percentage by Distance: 2022-2023 Season</h3>", unsafe_allow_html=True)

        selected_distance = st.selectbox('Select a Distance:', sorted(season_2022_shot_data['Distance (ft)'].unique()[season_2022_shot_data['Distance (ft)'].unique() <= 29]))


        filtered_data = season_2022_shot_data[season_2022_shot_data['Distance (ft)'] == selected_distance]

        fig = plot_shooting_percentage(filtered_data, selected_distance, st)
        st.markdown("<medium style='text-align: center;'>Use the box above to select a distance and see the percentage of makes and misses. The green represents makes, the red represents misses.</small>", unsafe_allow_html=True)


    st.header('Useful Links')
    st.markdown("- [GitHub Repository](https://github.com/Andrew601/Stat-386-Project)", unsafe_allow_html=True)
    st.markdown("- [Blog Post](https://andrew601.github.io/ShotAnalysis.html)", unsafe_allow_html=True)