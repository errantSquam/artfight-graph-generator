
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import matplotlib.image as mpimg
import mplcyberpunk
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


# Edit as appropriate with your own colors, files and characters
endpoint_day = 31
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
    'Valen': mpimg.imread('markers/valenmarker.png'),
    'Orca': mpimg.imread('markers/orcamarker.png'),
    'Arelis': mpimg.imread('markers/arelismarker.png'),
    'Ashaya': mpimg.imread('markers/ashayamarker.png'),
    'Ordell': mpimg.imread('markers/ordellmarker.png'),
}


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

    df_cumsum = df_filtered.set_index('Day').cumsum().reset_index() # heh heh . . . cum

    df_melted = df_cumsum.melt(id_vars=['Day'], var_name='Character', value_name='Defences')

    sns.set_theme(rc={'figure.figsize':(10,5)})

    plt.style.use("cyberpunk")

    fig, ax = plt.subplots()
    
    if endpoint_day < 7:
        ax.set_ylim(0.0, 7)
        ax.set_xlim(0.0, 7.0)
    
    ax.xaxis.grid(True, which='minor')

    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))

    ax.xaxis.set_minor_locator(MultipleLocator(1)) # not sure why this doesn't work lol >_>
    

    
    ax.tick_params(which='both')

    for chara in df_melted['Character'].unique(): #write data normally
        data = df_melted[df_melted['Character'] == chara]
        
        color = color_palette.get(chara, '#000000')  
        marker_img = markers.get(chara)


        
        if marker_img is not None:
            x = data['Day']
            y = data['Defences']
            plt.plot(x, y, label=chara, color=color, marker = ".", clip_on = False)

        else:
            sns.lineplot(data=data, x='Day', y='Defences', label=chara, color=color, marker = ".")

    for chara in np.flip(df_melted['Character'].unique()): # now for images 
        data = df_melted[df_melted['Character'] == chara]
        marker_img = markers.get(chara)
        
        
        if marker_img is not None:
            x = data['Day']
            y = data['Defences']
            marker_size = 0.7
            for xi, yi in zip(x, y):
                if xi == 0 or xi == endpoint_day or \
                (xi > 0 and data['Defences'].iloc[xi] - data['Defences'].iloc[xi-1] != data['Defences'].iloc[xi] - data['Defences'].iloc[xi+1]):
                    plt.imshow(marker_img, extent=(xi-marker_size/2, xi+marker_size/2, yi-marker_size/2, yi+marker_size/2), aspect='equal', zorder=10, clip_on = False)

    plt.title('Artfight 2023 Defences')
    plt.xlabel('Day')
    plt.ylabel('# Defences')
    
    
    plt.legend(title='Character', loc='center left', bbox_to_anchor=(1, 0.5), fontsize = 8)
    plt.subplots_adjust(right=0.90)
    mplcyberpunk.make_lines_glow()

    writeBytes() 

    plt.show()



createGraph(endpoint_day, color_palette, markers)