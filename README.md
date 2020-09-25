# InSAR_clustering
InSAR_clustering is an open-source code written in Python that support users in analysing time series of ground deformation.
I have developed this tool for an easier analysis of InSAR time series and better geological interpretation of the geophysical source of ground deformation.
Usually InSAR results consist in matrix of millions of different targets (namely the radar target/pixel) by hundreds of different time intervals so the manual interpretation of this matrix is unfeasbile if not time consuming.

![](images/cluster_result.png)

The underlying approach of the InSAR_clustering script is described in detail in the following British Geological Survey (BGS) Open Report:
Novellino, A.; Terrington, R.; Christodoulou, V.; Smith, H.; Bateson, L.. 2019 Ground motion and stratum thickness comparison in Tower Hamlets, London. Nottingham, UK, British Geological Survey, 31pp. (OR/19/043)

The report is available at http://nora.nerc.ac.uk/id/eprint/525619/ 

The script is currently used for the interpretation of the Automatic InSAR Processor developed by the Earth Observation team in BGS. For more information on this, do please ask E.Hussain (ekhuss@bgs.ac.uk) or myself (alessn@bgs.ac.uk) for more details.


# Description
The python script can be divided in three main parts:
1) loading the data, which is (as usual!) the most time consuming part considering that datatsets produced with different software will inevitably have different format.
2) Performing a Principal Component Analysis (PCA) of the time series. More details on the application of PCA on InSAR time series are here: https://doi.org/10.3390/rs10040607
3) Performing a Cluster analysis where the number of clusters is based on the number of components retrieved in (2) with the PCA.

For (3) it is necessary to import the sklearn module. In particular, the 'TimeSeriesKMeans' clustering method has been used.


# Installation
No installation is required and all the used packages are uploaded at the beginning of the code (lines 12-27).
