# ECHO-based IfA-Smeargle Masks
#### Documentation for Echo Filter/Masking Codes and Methods

This document describes the different ECHO filter classes, and each of the filters
within the classes. Describing their functionality, rational, limitations, and applicability, 
the documentation below is expected to be comprehensive. The Python doc-strings
are considered to be more up-to-date (but not necessarily accurate). When in doubt, do not
hesitate to contact project maintainers. 


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


------

## ECHO-200 Class

The ECHO-200 class of filters are reserved for masks and masking techniques that do not have
a known hard problem source. The problems that may arise that may require an ECHO-200 class
filter are far softer. These filters may be used for masking pixels such that downstream lines and
software behave nicer (assuming that there is no ECHO-000 or ECHO-100 class source for said
filters).

As the source of these filters are mostly for downstream efforts, not all of them are
expected to be used. However, it is usually suggested that ECHO-200 class filters not be
skipped unless there is a very good, well-understood reason.


------


## ECHO-300 Class

The ECHO-300 class is reserved for filters of an arbitrary nature. Nevertheless important,
the source and rational for these filters do not fit the above criteria set by higher classes.
More freedom may be exercised when applying or not these filters. However, it is assumed that one
knows what they are doing when ignoring or applying filters. 

The source of these filters, being arbitrary, are always applied last and are always overruled 
by the higher class filters.  