# ECHO-based IfA-Smeargle Masks
#### Documentation for Echo Filter/Masking Codes and Methods

This document describes the different ECHO filter classes, and each of the filters
within the classes. Describing their functionality, rational, limitations, and applicability, 
the documentation below is expected to be comprehensive. The Python doc-strings
are considered to be more up-to-date (but not necessarily accurate). When in doubt, do not
hesitate to contact project maintainers. 

If a filter or mask fails to apply (or does not catch any pixels), A warning will normally be 
displayed.


-----


## ECHO-000 Class

The ECHO-000 class of filters are reserved mostly for masks/masking methods that are 
fundamental in origin. That is, the reasons why they are being masked is more about critical 
short-falls in hardware/software, or even about nature itself, than something about array 
performance. 

Being the first and most fundamental class, this is always applied first. 


------

## ECHO-100 Class

The ECHO-100 class of filters are reserved mostly for masks/masking methods that are based
not on hard problems, but on problems stemming from unusual output. The outputs that
would trigger a ECHO-100 class filter either do not make too much physical sense, or
data that does not provide any useful data. 

The source of ECHO-100 flags may be from hard (ECHO-000 like) problems. However, it is not
exactly determined to be an ECHO-000 reason, and thus cannot be marked as so.


#### ECHO-120 Subarray Mask

The sub-array mask applies a mask to the entire array excluding a specific subarray provided by
given x-range and y-range bounds. The sub-array is inclusive of the bounds provided. 

No more than a single sub-array may be provided. It does not make sence to have more than one
sub-array. A sub-array mask is strictly meant for trimming the edge pixels or a priori trims based
on detector configuration.


## ECHO-200 Class

The ECHO-200 class of filters are reserved for masks and masking techniques that do not have
a known hard problem source. The problems that may arise that may require an ECHO-200 class
filter are far softer. These filters may be used for masking pixels such that downstream lines and
software behave nicer (assuming that there is no ECHO-000 or ECHO-100 class source for said
filters).

As the source of these filters are mostly for downstream efforts, not all of them are
expected to be used. However, it is usually suggested that ECHO-200 class filters not be
skipped unless there is a very good, well-understood reason.


#### ECHO-270 Minimum Cut

This mask filters out all pixels that have a value strictly less than a specific limiting 
minimum; that is, values equal to the minimum are kept.

The limiting minimum is hard-coded as a parameter provided by the user.

#### ECHO-271 Maximum Cut

This mask filters out all pixels that have a value strictly more than a specific limiting 
maximum; that is, values equal to the maximum are kept.

The limiting maximum is hard-coded as a parameter provided by the user.


------


## ECHO-300 Class

The ECHO-300 class is reserved for filters of an arbitrary nature. Nevertheless important,
the source and rational for these filters do not fit the above criteria set by higher classes.
More freedom may be exercised when applying or not these filters. However, it is assumed that one
knows what they are doing when ignoring or applying filters. 

The source of these filters, being arbitrary, are always applied last and are always overruled 
by the higher class filters.  

#### ECHO-380 Single Pixels

This mask applies itself to a given list of single pixels. Each pixel included in the function's
pixel list is considered to be flagged. The list of pixels provided must be in the
following form:

[ (x1,y1) , (x2,y2) , (x3,y3) , ... (xn,yn) ]

Each single pixel at those pixel coordinates (zero-indexed) will be flagged for masking.

#### ECHO-381 Rectangle Mask

This mask applies itself to rectangles defined by parallel lists of x-ranges and y-ranges. 
It is acceptable if these rectangles overlap. 

If only one rectangle is being made, the xy-ranges should be embedded as if to resemble parallel
arrays. The program may be able to do it automatically, but it is best not to rely on such
adaptation. Moreover, the xy-ranges should be referencing their values based on a 0-indexed 
data array. The rectangle masking is inclusive of the values provided. 

#### ECHO-382 Column Mask

This mask applies itself to columns of pixels specified by a 0-indexed list. The list
must contain all of the columns to mask; if it not contained, it is not masked. 

The specifications of the columns are given by its x-axis coordinate (again, 0-indexed).

#### ECHO-383 Row Mask

This mask applies itself to rows of pixels specified by a 0-indexed list. The list
must contain all of the rows to mask; if it not contained, it is not masked. 

The specifications of the rows are given by its y-axis coordinate (again, 0-indexed).


#### ECHO-398 Nothing

This is an arbitrary mask stipulating that nothing should be flagged. This does not have
much to do with pure science, but it is handy for obtaining a blank blanket mask. Basically 
the direct opposite of ECHO-399.

It works just as all other masks. 

#### ECHO-399 Everything

This is an arbitrary mask stipulating that everything should be flagged. This does not have
much to do with pure science, but it is handy for obtaining a full blanket mask. Basically 
the direct opposite of ECHO-398.

It works just as all other masks. 