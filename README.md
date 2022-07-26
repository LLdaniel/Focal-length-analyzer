# Focal-length-analyzer
Creates a histogram to visualize the distribution of used focal lengths on a set of pictures containing exif data

## Idea
A discussion about photography and focal length lead to the idea creating a small data analysis tool for how often a specific focal length is used in a set of pictures. The resulting analysis is presented as a histogram with the possibility to compare two distinct sets of pictures. E.g. a comparision between to photographers` habits on focal length.

## Usage
![Focal-length-analyer Screenshot](/img/exampleHisto.png "Focal-length-analyer Screenshot")
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
Currently binaries are available for *Linux* and *Windows*.
They are created separately on each plattform with [pyinstaller](https://pypi.org/project/pyinstaller/ "pyinstaller").
<table>
     <tr>
          <th columnspan="3">File</th>
          <th>Sum sha256</th>
          <th>Plattform</th>
     </tr>
     <tr>
          <td>Focal-length-analyzer-1.0-win.zip</td>
          <td>7e4c946bd3204f5d11442dd2ac8b0c64b444548d218c7770c93bd26cb7b96867</td>
          <td>Windows</td>
     </tr>
     <tr>
          <td>Focal-length-analyzer-1.0-linux.tar.gz</td>
          <td>2c60d3d5b57f7c6fd94a187c80d6943906629248098f5dd9ea260ccc1107ea81</td>
          <td>Linux</td>
     </tr>
</table>

## Licence
MIT License
Copyright (c) 2022 LLdaniel
