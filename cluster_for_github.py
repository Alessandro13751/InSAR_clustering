#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execute a cluster analysis of the data generated from mintpy_ts2df.py

@authors: alessn @British Geological Survey

***Updates***
27 July 2020: Cluster analysis on the time series extracted with mintpy_ts2df.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tslearn.clustering import TimeSeriesKMeans
from sklearn.preprocessing import StandardScaler
from sklearn import decomposition
from collections import Counter
np.set_printoptions(precision=4)
np.set_printoptions(suppress=True)

proj_dir = "/localb/data/insar/Hanoi/Descending_insar/mintpy/geo" #to be changed every time
os.chdir(proj_dir)

#Import the input files
df_coords = pd.read_csv (r'coords.csv'); lats=df_coords['lat']; lons=df_coords['lon'];
df = pd.read_csv (r'df_array.csv')
df_array=df.iloc[:,:].to_numpy() #df_array=df_nan.iloc[:,0:-1].to_numpy() #to extract all the not nan values from the dataframe

##--------------------------------------PCA analysis----------------------------------------
#PCA to constrain the number of clusters to use with the unsupervised clustering,
#see https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

#standardize/normalise the dataset’s features onto unit scale (mean = 0 and variance = 1),
df_array_std = StandardScaler().fit_transform(df_array)
print (df_array_std[~np.isnan(df_array_std)].mean()) #must be very close to 0

pca = decomposition.PCA()
pca.fit(df_array_std)
print(pca.explained_variance_)

#check the three main components
plt.plot(pca.components_[0,:], linewidth=1, color='blue', label='PC1')
plt.plot(pca.components_[1,:], linewidth=1, color='red', label='PC2')
plt.plot(pca.components_[2,:], linewidth=1, color='green', label='PC3')
plt.legend()
plt.title('PCA eigenvectors')
plt.xlabel('satellite acquisitions')
plt.ylabel('LOS displacement [m]')
plt.savefig('PCA_eigenvectors.png')

#take only components which explain up to 95% of the variance
variance_perc = (pca.explained_variance_/sum(pca.explained_variance_))*100

##two ways of selecting the number of components: everything >1% or cumulative <95% of the variance
#relevant_components = len([i for i in variance_perc if i >=1])
#print ("Components accounting for =>1% of variance : " + str(relevant_components))
for i in range(0,len(variance_perc)):
    sum(variance_perc[0:i])
    if sum(variance_perc[0:i])>=90:
        break
print ("Components accounting for <=90% of variance : " + str(i))
components=i

##--------------------------------------Cluster analysis----------------------------------------
##for theory, see https://scikit-learn.org/stable/modules/clustering.html
##for parameters setting, https://tslearn.readthedocs.io/en/stable/gen_modules/clustering/tslearn.clustering.TimeSeriesKMeans.html
# Euclidean k-means
print("Euclidean k-means")
km = TimeSeriesKMeans(n_clusters=components, max_iter=5,metric='euclidean',random_state=0).fit(df_array)
cluster_centre=km.cluster_centers_.shape
#time_series_class=km.predict(df_array_std)
time_series_class=km.predict(df_array)
labels = km.labels_
count_labels=list(Counter(labels).values())
inertia=km.inertia_


##plot the % of the clusters
labels_for_plot=list(Counter(labels).keys())
fig1, ax1 = plt.subplots()
ax1.pie(count_labels,labels=labels_for_plot, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("% of points distribution per clusters"); props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.75,-1,'no_of_samples='+str(len(labels)),verticalalignment='top',bbox=props)
plt.show()
plt.savefig('Clusters_%_distribution.png')

##Plotting the clusters centre
##for plotting, https://tslearn.readthedocs.io/en/stable/auto_examples/clustering/plot_kmeans.html#sphx-glr-auto-examples-clustering-plot-kmeans-py
##taking the 5th and 95th percentile to display along with the clusters centre
cluster_10th_percentile=[] 
cluster_90th_percentile=[]
cluster_50th_percentile=[]

for yi in range(components):
    for time in range(df_array.shape[1]):
        class_temporary=df_array[time_series_class==yi]
        number_1=np.percentile(class_temporary[:,time],10);number_2=np.percentile(class_temporary[:,time],90);number_3=np.percentile(class_temporary[:,time],50);
        cluster_10th_percentile.append(number_1)
        cluster_90th_percentile.append(number_2)
        cluster_50th_percentile.append(number_3)
cluster_10th_percentile=np.reshape(cluster_10th_percentile,(components,df_array.shape[1]))
cluster_90th_percentile=np.reshape(cluster_90th_percentile,(components,df_array.shape[1]))
cluster_50th_percentile=np.reshape(cluster_50th_percentile,(components,df_array.shape[1]))

plt.figure()
for yi in range(components):
    plt.subplot(1, components,yi+1)
    for xx in range(3):       
        plt.plot(cluster_10th_percentile[yi,:],"k-", alpha=.2)
        plt.plot(cluster_90th_percentile[yi,:],"k-", alpha=.2)
        plt.plot(km.cluster_centers_[yi].ravel(),"r-")
        plt.text(0.55,0.85,'Cluster %d' % (yi+1),
                 transform=plt.gca().transAxes)
        if yi==1:
            plt.title("Euclidean $k$-means")
plt.savefig('Clusters_centre.png')

#export cluster location and the cluster time series as .csv
labels=labels+1
labels_dataframe=pd.DataFrame(labels,columns=['cluster']); labels_dataframe.index=lats.index
df_coords_clusters = pd.concat([df_coords['lat'],df_coords['lon'],labels_dataframe],axis=1)
df_coords_clusters.to_csv(os.path.join(proj_dir,'df_coords_clusters_buttare.csv')) #to save the displ+coords data as csv
np.savetxt("df_clusters_displ.csv", cluster_50th_percentile, delimiter=",")