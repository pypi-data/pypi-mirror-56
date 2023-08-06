## This package allows you to:
1. Create a scatterplot 
2. Plot the distribution of your data
3. Group or cluster samples in your data

### 1. Creating a scatterplot:

To create a scatterplot, you have to run the **scattergraph** function from the **plotting.py** file, which takes the following arguments:
1.  x: this is the column that you want to plot on your x-axis. This should be a numpy array.
2.  y: this is the column that you want to plot on your y-axis. This should be a numpy array.
3.  xtitle: this will be the title of your x-axis. This should be a string.
4.  ytitle: this will be the title of your y-axis. This should be a string.
5.  graphtitle: this will be the title of your graph. This should be a string.
6.  outlier_treatment: this tells the graph how to visually differentiate outliers on your plot. You can choose one of the below options. This should be a string.
-  "color": plots the outliers in a different color
-  "shape": plots the outliers with a different marker
-  "size": plots the outliers with a different size
-  _Note: this argument will default to size if any other string is passed_
7. outlier_sensitivity: this is a multiplier in a customized IQR calculation, which ultiamately generates a sub-array of outliers. This should be a float (recommended between 0 and 2). If outlier_sensitivity is zero, then your outliers are in the 1st and 4th quartile of your data. The higher the outlier_sensitivity, the fewer the outliers.

### 2. Plotting your distributions:
To plot your distribution, you have to run the **plotdistribution** function from the **plotting.py** file, which takes the following arguments:
1. y: this is the column that has your target data. This should be a numpy array.
2. numberofbins: choose the number of bins for the histogram. The larger the data set, the more likely you�ll want a large number of bins. This should be an int.
3. plottitle: this will be the title of your graph. This should be a string.

### 3. Grouping/creating clusters:
To create clusters, you have to run the **create_clusters** function from the **clustering.py** file, which takes the following arguments:
1. x: the columns that you want to use as a basis for clustering. This should be a numpy array.
2. y: this is the column that has your target data. This should be a numpy array.
3. numberofclusters: the number of clusters to form as well as the number of centroids to generate. This should be an int.