import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import MetaTrader5 as mt5
from data_collector import stream_data

def connect_mt5():
    if not mt5.initialize():
        print('Error connecting mt5')
        return False
    else:
        return True

timef = [mt5.TIMEFRAME_D1, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_M15]
long, mid, short = stream_data('AMD',timef, 250)

def visualize(long, mid, short):
    # Create figure and subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
    
    # Function to plot a single timeframe
    def plot_timeframe(ax, df, title):
        # Plot price line
        ax.plot(df['time'], df['close'], label='Price', color='blue')
        
        # Plot SMAs if available
        if 'SMA_50' in df.columns:
            ax.plot(df['time'], df['SMA_50'], label='SMA 50', color='orange', linestyle='--')
        if 'SMA_200' in df.columns:
            ax.plot(df['time'], df['SMA_200'], label='SMA 200', color='red', linestyle='--')
        
        # Plot Bollinger Bands if available
        if 'BB_upper' in df.columns and 'BB_lower' in df.columns:
            ax.fill_between(df['time'], df['BB_upper'], df['BB_lower'], color='gray', alpha=0.3, label='Bollinger Bands')
            ax.plot(df['time'], df['BB_middle'], color='black', linestyle=':', label='BB Middle')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.set_title(title)
        ax.grid(True)
        ax.legend()
    
    # Plot each timeframe
    plot_timeframe(ax1, long, 'Daily Timeframe (D1)')
    plot_timeframe(ax2, mid, 'Hourly Timeframe (H1)')
    plot_timeframe(ax3, short, '15-Minute Timeframe (M15)')
    
    plt.tight_layout()
    plt.show()

visualize(long, mid, short)
