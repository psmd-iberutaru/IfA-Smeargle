
"""
The reduction of the arrays should not generally call the upper lines. 
Each line should be called within a Zulu function, allowing for the 
consistency and ease of usage of the IfA Smeargle module. Changes should
only be applied to the configuration classes.

Slight, required modifications to the default lines are their own separate 
functions, contained within the file of the detector that they apply to.
"""

# Adding the pipelines.
from IfA_Smeargle.zulu.detector_pipelines.saphria_pipeline import *
