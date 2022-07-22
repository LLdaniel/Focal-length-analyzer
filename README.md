# Focal-length-analyzer
Creates a histogram to visualize the distribution of used focal lengths on a set of pictures containing exif data

## Idea
A discussion about photography and focal length lead to the idea creating a small data analysis tool for how often a specific focal length is used in a set of pictures. The resulting analysis is presented as a histogram with the possibility to compare two distinct sets of pictures. E.g. a comparision between to photographers` habits on focal length.

## Usage
Feed the tool with data happens on the CLI and will bring up the final result as an histogram:
1. Start CLI tool with ```python3 focal-length-analyzer.py dir1``` where ```dir1``` is a picture containing directory
2. Get the final result as a histogram
3. Additional options:
 - Compare Mode of two directories: `python3 focal-length-analyzer.py dir1 dir2`
 - common sensor reference, choose between full frame, aps-c sensor with a specific crop factor or none. Default is full frame. Can be combined with the compare mode.
   - `python3 focal-length-analyzer.py dir1 -s ff`
   
   - `python3 focal-length-analyzer.py dir1 -s aps-c1.6`
   
   - `python3 focal-length-analyzer.py dir1 -s none`
 

## Requirements
- Python 3.9.2

## Binary Build Procedure
Will come soon.

## Licence
MIT License
Copyright (c) 2022 LLdaniel
