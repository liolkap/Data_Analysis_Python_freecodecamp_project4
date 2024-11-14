import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv').set_index('date')

# Clean data
df = df[(df['value'] > df['value'].quantile(0.025)) &
        (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df, color='red')
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ticks = ['2016-07-01', '2017-01-01', '2017-07-01', '2018-01-01',
             '2018-07-01', '2019-01-01', '2019-07-01', '2019-12-01']
    ax.set_xticks(ticks)
    ax.set_xticklabels(['2016-07', '2017-01', '2017-07', '2018-01',
                        '2018-07', '2019-01', '2019-07', '2019-12'])

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy().reset_index()

    ## Splitting the date column into three columns
    df_bar_dates = df_bar['date'].str.split('-', expand=True)
    df_bar['year'], df_bar['month'], df_bar['day'] = df_bar_dates[0], df_bar_dates[1], df_bar_dates[2]
    df_bar = df_bar.drop('date', axis=1)

    ## Preparing data for the bar plot
    data = df_bar.groupby(['year', 'month'])['value'].mean().apply(round, ndigits=2)

    d2016 = pd.DataFrame(data['2016']).T.rename({'value': '2016'}, axis=0)
    d2017 = pd.DataFrame(data['2017']).T.rename({'value': '2017'}, axis=0)
    d2018 = pd.DataFrame(data['2018']).T.rename({'value': '2018'}, axis=0)
    d2019 = pd.DataFrame(data['2019']).T.rename({'value': '2019'}, axis=0)
    bar_data = pd.concat([d2017, d2016, d2018, d2019], axis=0).iloc[[1, 0, 2, 3]].fillna(0)
    bar_data = bar_data.rename({'01': 'January', '02': 'February', '03': 'March',
                                '04': 'April', '05': 'May', '06': 'June',
                                '07': 'July', '08': 'August', '09': 'September',
                                '10': 'October', '11': 'November', '12': 'December'}, axis=1)

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 10))
    bar_data.plot(kind='bar', ax=ax)
    ax.legend(title='Months')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box_dates = df_box['date'].str.split('-', expand=True)
    df_box['year'], df_box['month'], df_box['day'] = df_box_dates[0], df_box_dates[1], df_box_dates[2]
    df_box = df_box.drop('date', axis=1)

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(28, 10))
    sns.boxplot(data=df_box, x='year', y='value', ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')

    df_box = df_box.sort_values(by=['month', 'year'])
    df_box['month'] = df_box['month'].replace({'01': 'Jan', '02': 'Feb', '03': 'Mar',
                                               '04': 'Apr', '05': 'May', '06': 'Jun',
                                               '07': 'Jul', '08': 'Aug', '09': 'Sep',
                                               '10': 'Oct', '11': 'Nov', '12': 'Dec'})

    sns.boxplot(data=df_box, x='month', y='value', ax=ax[1])
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
