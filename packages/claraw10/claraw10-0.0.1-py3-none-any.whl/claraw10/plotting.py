import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def outlier(y,outlier_sensitivity):
    q75, q25 = np.percentile(y, [75 ,25])
    iqr = q75 - q25
    max_suspected = outlier_sensitivity*iqr + q75
    min_suspected = q25 - outlier_sensitivity*iqr
    outliers = []
    for i in y:
        if (i < min_suspected) or (i > max_suspected):
            outliers.append(i)
    return np.array(outliers)
       
    
def scattergraph(x,y,xtitle,ytitle,graphtitle,outlier_treatment,outlier_sensitivity):
    o = outlier(y,outlier_sensitivity)
    for i,point in enumerate(x):
        if y[i] in o:
            if outlier_treatment == 'color':
                plt.scatter(point,y[i],color="#f7cac9")
            elif outlier_treatment == 'shape':
                plt.scatter(point,y[i],color="#92a8d1",marker="^")
            else: #default to size
                plt.scatter(point,y[i],s=50,color="#92a8d1")
        else:
            plt.scatter(point,y[i],color="#92a8d1",marker='.')
    plt.xlabel(xtitle,size='small', weight='bold',color='#034f84')
    plt.ylabel(ytitle,size='small',weight='bold',color='#034f84')
    plt.title(graphtitle, weight='bold',color='#034f84')
    plt.xticks(size="small",color='#034f84')
    plt.yticks(size="small",color='#034f84')
    coefs = np.polyfit(x, y, 2)
    stepsize = np.abs((np.max(x) - np.min(x)) / 100)
    new_xs = np.arange(np.min(x), np.max(x), stepsize)
    ffit = np.polyval(coefs, new_xs)
    plt.plot(new_xs,ffit,color="#f7786b")
    plt.show()   

def plotdistribution(y,numberofbins,plottitle):

    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.set_color_codes()
    sns.distplot(y, bins=numberofbins, color='#9999ff')
    plt.xticks(size="small",color='#00004d')
    plt.yticks(size="small",color='#00004d')
    plt.title(plottitle, weight='bold', color='#00004d')
    plt.show()

