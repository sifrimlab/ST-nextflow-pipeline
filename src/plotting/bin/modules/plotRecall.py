import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


df = pd.read_csv("stats/prec_recall.csv")
x =list(set(df ['special']))
y1 =list(df[df['pixel_distance']==1]['ratio'])
y2 =list(df[df['pixel_distance']==2]['ratio'])
y3 =list(df[df['pixel_distance']==3]['ratio'])
y0 =list(df[df['pixel_distance']==0]['ratio'])
width = 0.20       # the width of the bars

N = 3
ind = np.arange(N)

plt.rcParams.update({'font.size': 18})
_, ax = plt.subplots(1,1)
rects3 = ax.bar(ind,y3, width, color='orange')
rects2 = ax.bar(ind+width, y2, width, color='cornflowerblue')
rects1 = ax.bar(ind+width*2, y1, width, color='maroon')
rects0 = ax.bar(ind+width*3, y0, width, color='slategrey')


ax.set_ylabel('Complete Barcode Ratio')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Normal', 'No global registration', 'No registration') )
ax.legend( (rects3[0], rects2[0],rects1[0], rects0[0]), ('3 pixels', '2 pixels', '1 pixel', 'exact match') )

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.005*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects3)
autolabel(rects2)
autolabel(rects1)
autolabel(rects0)
plt.show()

