
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import matplotlib.image as mpimg
import mplcyberpunk
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


def writeBytes():
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    image_base64 = f"data:image/png;base64,{image_base64}"


    with open('output.txt', 'w') as f:
        f.write(image_base64)
        
    plt.savefig('output.png', bbox_inches='tight', dpi=300)


def createGraph(endpoint_day, palette, markers):
    df = pd.read_csv('artfight 2024 data.csv')
    
    

    df.fillna(0, inplace=True)

    df_filtered = df[df['Day'] <= endpoint_day]

    df_cumsum = df_filtered.set_index('Day').cumsum().reset_index()

    df_melted = df_cumsum.melt(id_vars=['Day'], var_name='Character', value_name='Defences')

    #print(df_melted)

    
    #plt.figure(figsize=(10, 6))
    #sns.set(style="ticks", context="talk")
    sns.set_theme(rc={'figure.figsize':(10,5)})

    plt.style.use("cyberpunk")

    fig, ax = plt.subplots()
    #fig = plt.figure(figsize=(20, 2))
    
    if endpoint_day < 7:
        ax.set_ylim(0.0, 7)
        ax.set_xlim(1.0, 7.0)
    
    ax.xaxis.grid(True, which='minor')

    ax.xaxis.set_major_locator(MultipleLocator(7))
    ax.yaxis.set_major_locator(MultipleLocator(1))

    ax.xaxis.set_minor_locator(MultipleLocator(1))
    

    
    ax.tick_params(which='both')

    for chara in df_melted['Character'].unique():
        data = df_melted[df_melted['Character'] == chara]
        
        color = color_palette.get(chara, '#000000')  
        marker_img = markers.get(chara)
        

        
        if marker_img is not None:
            x = data['Day']
            y = data['Defences']
            plt.plot(x, y, label=chara, color=color, clip_on = False)

            marker_size = 0.7
            for xi, yi in zip(x, y):
                plt.imshow(marker_img, extent=(xi-marker_size/2, xi+marker_size/2, yi-marker_size/2, yi+marker_size/2), aspect='equal', zorder=10, clip_on = False)

        else:
            sns.lineplot(data=data, x='Day', y='Defences', label=chara, color=color)

    plt.title('Artfight 2024 Defences')
    plt.xlabel('Day')
    plt.ylabel('# Defences')
    
    
    plt.legend(title='Character', loc='center left', bbox_to_anchor=(1, 0.5), fontsize = 8)
    plt.subplots_adjust(right=0.90)
    mplcyberpunk.make_lines_glow()

    writeBytes() 

    plt.show()


# Edit as appropriate
endpoint_day = 1
color_palette = {
    'Ekaitz': '#FF6347',  
    'Valen': '#ffcb66',
    'Orca': "#8da2ff",
    'Arelis': '#dcc5f3',
    'Ashaya': '#54ff80',
    'Ordell': '#9b78ff'
}
markers = {
    'Ekaitz': mpimg.imread('markers/ekaitzmarker.png'),
}

createGraph(endpoint_day, color_palette, markers)