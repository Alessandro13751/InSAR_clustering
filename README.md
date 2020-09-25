# InSAR_clustering

InSAR_clustering is an open-source code written in Python that support users in analysing time series of ground deformation.
I have developed this tool for an easier analysis of InSAR time series and better geological interpretation of the geophysical source of ground deformation.
Usually InSAR results consist in matrix of millions of different targets (namely the radar target/pixel) by hundreds of different time intervals so the manual interpretation of this matrix is unfeasbile if not time consuming.

The underlying approach of the InSAR_clustering toolkit is described in detail in the following British Geological Survey (BGS) Open Report:
Novellino, A.; Terrington, R.; Christodoulou, V.; Smith, H.; Bateson, L.. 2019 Ground motion and stratum thickness comparison in Tower Hamlets, London. Nottingham, UK, British Geological Survey, 31pp. (OR/19/043)

The report is available at http://nora.nerc.ac.uk/id/eprint/525619/ 

The script is currently used for the interpretation of the Automatic InSAR Processor developed by the Earth Observation team in BGS. For more information on this, do please ask E.Hussain (ekhuss@bgs.ac.uk) or myself (alessn@bgs.ac.uk) for more details.

# Description
The python script can be divided in three main parts:
1) loading the data, which is (as usual!) the most time consuming part considering that datatsets produced with different software will inevitably have different format.
