"""
Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT

@author: Marshall Farrier
@contact: marshalldfarrier@gmail.com
@since: 2014-11-07
@summary: Chart financial data

Since detailed charts are readily available online, these charts
serve 2 purposes:
1. Verify data integrity
2. Visualize events as defined by custom algorithms.
The functions in this submodule wrap pandas and matplotlib
for ease of use in serving these 2 purposes.

Resources:
http://matplotlib.org/api/pyplot_api.html
http://matplotlib.org/api/finance_api.html
http://stackoverflow.com/questions/22027415/
http://sentdex.com/sentiment-analysisbig-data-and-python-tutorials-algorithmic-trading/how-to-chart-stocks-and-forex-doing-your-own-financial-charting/
http://stackoverflow.com/questions/19580116/plotting-candlestick-data-from-a-dataframe-in-python
http://sentdex.com/sentiment-analysisbig-data-and-python-tutorials-algorithmic-trading/how-to-chart-stocks-and-forex-doing-your-own-financial-charting/
http://pandas.pydata.org/pandas-docs/version/0.15.0/visualization.html
"""

import datetime as dt

import matplotlib.dates as mdates
import matplotlib.finance as fplt
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def candlestick(df, **kwargs):
    """
    candlestick(df, title='GE', fname='foo.png', events=evdf, eventcolors=['r', 'g'], 
            bollinger=bolldf, sma=smadf)

    Show and optionally save candlestick chart of a DataFrame as retrieved using data.get().

    Parameters
    ---
    df : DataFrame containing columns 'Open', 'High', 'Low', 'Close' and 'Volume'
        source data
    title : str, optional
        title to be used for the chart
    fname : str, optional
        If provided, the chart will be saved to a file named `fname`. `fname`
        should also include the extension '.png' or '.pdf'
    events : DataFrame, optional
        must have the same index as df.
        Up to 4 columns of events will be mapped. The order of the columns will
        determine the marker to be assigned to the event. The color order is:
        ['g^', 'ro', 'bs', 'k^']
        Non-events in this DataFrame should have a value like np.NAN,
        which matplotlib will not plot.
        The events DataFrame should use dtype='float'. If not, a bug in numpy (or matplotlib)
        can lead to a TypeError:
        http://matplotlib.1069221.n5.nabble.com/type-error-with-python-3-2-and-version-1-1-1-of-matplotlib-numpy-error-td38784.html
    bollinger : DataFrame, optional
        if present Bollinger bands will be overlaid
        must have same index as df
        must contain columns 'Upper' and 'Lower'
    sma : DataFrame, optional
        if present, first data column will be overlaid as simple moving average
        must have same index as df
    """
    _make_chart(df, 'candlestick', **kwargs)

def adj_close(df, **kwargs):
    """
    adj_close(df, title='GE', fname='foo.png', events=evdf, eventcolors=['r', 'g'], 
            bollinger=bolldf, sma=smadf)

    Show and optionally save adj_close chart of a DataFrame as retrieved using data.get().

    Parameters
    ---
    df : DataFrame containing columns 'Open', 'High', 'Low', 'Close' and 'Volume'
        source data
    title : str, optional
        title to be used for the chart
    fname : str, optional
        If provided, the chart will be saved to a file named `fname`. `fname`
        should also include the extension '.png' or '.pdf'
    events : DataFrame, optional
        must have the same index as df.
        Up to 4 columns of events will be mapped. The order of the columns will
        determine the marker to be assigned to the event. The color order is:
        ['g^', 'ro', 'bs', 'k^']
        Non-events in this DataFrame should have a value like np.NAN,
        which matplotlib will not plot.
        The events DataFrame should use dtype='float'. If not, a bug in numpy (or matplotlib)
        can lead to a TypeError:
        http://matplotlib.1069221.n5.nabble.com/type-error-with-python-3-2-and-version-1-1-1-of-matplotlib-numpy-error-td38784.html
    bollinger : DataFrame, optional
        if present Bollinger bands will be overlaid
        must have same index as df
        must contain columns 'Upper' and 'Lower'
    sma : DataFrame, optional
        if present, first data column will be overlaid as simple moving average
        must have same index as df
    """
    _make_chart(df, 'adj_close', **kwargs)

def close(df, **kwargs):
    """
    close(df, title='GE', fname='foo.png', events=evdf, eventcolors=['r', 'g'], 
            bollinger=bolldf, sma=smadf)

    Show and optionally save close chart of a DataFrame as retrieved using data.get().

    Parameters
    ---
    df : DataFrame containing columns 'Open', 'High', 'Low', 'Close' and 'Volume'
        source data
    title : str, optional
        title to be used for the chart
    fname : str, optional
        If provided, the chart will be saved to a file named `fname`. `fname`
        should also include the extension '.png' or '.pdf'
    events : DataFrame, optional
        must have the same index as df.
        Up to 4 columns of events will be mapped. The order of the columns will
        determine the marker to be assigned to the event. The color order is:
        ['g^', 'ro', 'bs', 'k^']
        Non-events in this DataFrame should have a value like np.NAN,
        which matplotlib will not plot.
        The events DataFrame should use dtype='float'. If not, a bug in numpy (or matplotlib)
        can lead to a TypeError:
        http://matplotlib.1069221.n5.nabble.com/type-error-with-python-3-2-and-version-1-1-1-of-matplotlib-numpy-error-td38784.html
    bollinger : DataFrame, optional
        if present Bollinger bands will be overlaid
        must have same index as df
        must contain columns 'Upper' and 'Lower'
    sma : DataFrame, optional
        if present, first data column will be overlaid as simple moving average
        must have same index as df
    """
    _make_chart(df, 'close', **kwargs)

def _make_chart(df, chart_type, **kwargs):
    fig = plt.figure()
    ax1 = plt.subplot2grid((5, 4), (0, 0), rowspan=4, colspan=4)
    ax1.grid(True)
    plt.ylabel('Price')
    plt.setp(plt.gca().get_xticklabels(), visible=False)
    if chart_type == 'candlestick':
        _candlestick_ax(df, ax1)
    elif chart_type == 'adj_close':
        _adj_close_ax(df, ax1)
    elif chart_type == 'close':
        _close_ax(df, ax1)

    if 'sma' in kwargs:
        _plot_sma(kwargs['sma'])
    if 'bollinger' in kwargs:
        _plot_bollinger(kwargs['bollinger'])
    if 'events' in kwargs:
        _plot_events(kwargs['events'])

    ax2 = plt.subplot2grid((5, 4), (4, 0), sharex=ax1, rowspan=1, colspan=4)
    ax2.bar(df.index, df.loc[:, 'Volume'])
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(12))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_minor_locator(mdates.DayLocator())
    ax2.yaxis.set_ticklabels([])
    ax2.grid(True)
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.subplots_adjust(left=.09, bottom=.18, right=.94, top=0.94, wspace=.20, hspace=0)
    if 'title' in kwargs:
        plt.suptitle(kwargs['title'])
    if 'fname' in kwargs:
        plt.savefig(kwargs['fname'], bbox_inches='tight')
    plt.show()
    plt.close()

def _candlestick_ax(df, ax):
    """
    # Alternatively: (but hard to get dates set up properly)
    plt.xticks(range(len(df.index)), df.index, rotation=45)
    fplt.candlestick2_ohlc(ax, df.loc[:, 'Open'].values, df.loc[:, 'High'].values, 
            df.loc[:, 'Low'].values, df.loc[:, 'Close'].values, width=0.2)
    """
    quotes = df.reset_index()
    quotes.loc[:, 'Date'] = mdates.date2num(quotes.loc[:, 'Date'].astype(dt.date))
    fplt.candlestick_ohlc(ax, quotes.values)

def _adj_close_ax(df, ax):
    ax.plot(df.index, df.loc[:, 'Adj Close'])

def _close_ax(df, ax):
    ax.plot(df.index, df.loc[:, 'Close'])

def _plot_bollinger(bolldf):
    plt.fill_between(bolldf.index, bolldf.loc[:, 'Upper'].values, 
            bolldf.loc[:, 'Lower'].values, facecolor='gray', alpha=0.5)

def _plot_sma(smadf):
    lines = plt.plot(smadf.index, smadf.iloc[:, 0].values)
    lines[0].set_color('g')

def _plot_events(events):
    colors = ['gd', 'rv', 'b*', 'k^']
    n_events = min({len(events.columns), len(colors)})
    for i in range(n_events):
        plt.plot(events.index, events.iloc[:, i].values, colors[i], alpha=0.5, ms=12.0)