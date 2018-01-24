import matplotlib.font_manager as mfm
import matplotlib.pyplot as plt
#Chinese
font_path = "yahei.ttf"
prop = mfm.FontProperties(fname=font_path)

import pandas as pd
import datetime
import re
import os

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)
pd.options.display.chop_threshold = None
pd.options.display.expand_frame_repr = False

def date_converter(filename, _source, _type):
    search = "temp/%s/%s/(.*)_%s__%s.csv" % (_source, _type, _source, _type)
    date_regex = re.compile(search)
    date = date_regex.search(filename)
    date = str(date.group(1))
    date = datetime.datetime.strptime(date, '%Y_%m') #Converts string to date object
    return datetime.datetime.strftime(date, '%B %Y')

def get_single_scale(df, scale):
    if scale == -1:
        _df = df.groupby('name', sort=False).sum().reset_index()
        _df = _df.set_index('name').reset_index()
    else:
        _df = df.loc[df['scale'] == scale]
        _df = _df.set_index('name').reset_index()
    return _df

def get_names(df):
    return list(df.iloc[:,0])

def process_single_name(df, name):
    _df = df.loc[df['name'] == name].set_index('name').reset_index()
    return _df

def subplot_week(df, name, ax, c):
    week1 = 7*1
    week2 = 7*2
    week3 = 7*3
    week4 = 7*4
    week5 = 7*5
    _df = df.transpose().iloc[2:].reset_index()
    _df.columns = ['day','values']
    w1_sum = _df.iloc[:week1]['values'].sum() #Week1 Sum
    w2_sum = _df.iloc[week1:week2]['values'].sum() #Week2 Sum
    w3_sum = _df.iloc[week2:week3]['values'].sum() #Week3 Sum
    w4_sum = _df.iloc[week3:week4]['values'].sum() #Week4 Sum
    w5_sum = _df.iloc[week4:week5]['values'].sum() #Week5 Sum
    df_sum = pd.DataFrame(columns=['sum'], index=['W1','W2','W3','W4','W5'])
    df_sum.loc['W1'] = [w1_sum]
    df_sum.loc['W2'] = [w2_sum]
    df_sum.loc['W3'] = [w3_sum]
    df_sum.loc['W4'] = [w4_sum]
    df_sum.loc['W5'] = [w5_sum]
#    print(df_sum)
    df_sum.plot(ax=ax, kind='bar', color=c)
    ax.legend().remove()
    ax.set_title(name.strip().upper().replace(' ', '\n'), fontproperties=prop) #Chinese
    ax.set_axisbelow(True)
    ax.grid(b=True, which='major', axis='y', color='0.85', linestyle='-')
    
def plot_weekly(filename, _source, _type):
    
    df = pd.read_csv(filename)
    date_str = date_converter(filename, _source, _type)
    
    plt.ioff()
    
    scales = [1,2, -1]
    for _scale in scales:
        
        my_dpi = 150#96
    
        fig, axes = plt.subplots(nrows=2, ncols=7, figsize=(3840/my_dpi, 2160/my_dpi), dpi=my_dpi, sharey=True, sharex=True)
        fig.suptitle("Source: %s, Type: %s (Weekly) - %s" % (_source.capitalize(), _type.capitalize(), date_str), y=0.94, fontsize=25)
        plt.rc('axes', titlesize=8)     # fontsize of the axes title
        
        if _type == 'party':
            fig.delaxes(axes[1,3])
            fig.delaxes(axes[1,4])
            fig.delaxes(axes[1,5])
            fig.delaxes(axes[1,6])
    
        _df = get_single_scale(df, _scale) #Process single scale
        names = get_names(_df) #Get all names
        
        #Iterate Negative Scale (scale=1)  
        if _scale == 1:
            _s = 'Negative'
            color = 'C1'
        if _scale == 2:
            _s = 'Positive'
            color = 'C0'
        if _scale == -1:
            _s = 'Overall'
            color = 'C2'
            
        for _name, _axes in zip(names, axes.reshape(-1)):
            _df2 = process_single_name(_df, _name) #Process single name
            _df2 = subplot_week(_df2, _name, _axes, color) #Process subplot for single name
            
        filename_datestamp = datetime.datetime.strptime(date_str, '%B %Y')
        filename_datestamp = datetime.datetime.strftime(filename_datestamp, '%Y%m')
        
        lines, labels = axes[0,0].get_legend_handles_labels()
        
        fig.legend(lines, [_s], bbox_to_anchor=(0.95, 0.885), bbox_transform=plt.gcf().transFigure)
        
        plt.savefig('results/polarity_output/weekly/%s/%s/%s_%s_%s_%s.png' % (_source, _type, filename_datestamp, _source, _type, _s.lower()), bbox_inches='tight', dpi=300)
        
        plt.clf() #Clear figure after saving to avoid memory issues
        plt.close('all') #Disable console print

#sources = ['facebook', 'others', 'twitter']
sources = ['chinese']
types = ['leader', 'party']

for _s in sources:
    for _t in types:
        directory = os.path.join("temp",_s,_t)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith("20") and filename.endswith(".csv"): 
                 path = os.path.join(directory, filename)
                 print("Plotting file: " + path)
                 plot_weekly(path, _s, _t)
                 
print("Plotting completed")
