"""
The ZULU line is the final cumulation of all other lines, in a way, it is
the script that dictates how the data should be manipulated. Each array
type has its own functional line, while each subset of these arrays should
contain their own configuration file (from Yankee). 

Each functional line is contained within their own file.

The reduction of the arrays should not generally call the upper lines. 
Each line should be called within a Zulu function, allowing for the 
consistency and ease of usage of the IfA Smeargle module. Changes should
only be applied to the configuration classes.
"""
