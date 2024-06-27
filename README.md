<h3 align="center">Pre-processor and Utilities for OpenHASP</h3>

----

# python.py - an openhasp-preprocessor.
A preprocessor for the pages.jsonl file.  This allows you to make the page definitions in separate files and use variables to define variables for x: and y: positions or colors.  Really anything can be substituted globally.

## Useage:
**Preparation**
1. Create a .src file in a pages folder for each page.  
For example **page2.src** is the **jsonl** code for everything that will appear on page 2.  
Example:  
```
{
  "comment":" ------------------------- Page 2 - Temperatures -------------------------"
}

{
  "comment":"----- PageTitle",
  "page":2,"id":1,
  "obj":"btn",
  "x":120,"y":0,"w":240,"h":40,
  "text":"Temperatures","align":2,"value_font":22,
  "bg_opa":0,"text_color":"gray","radius":0,"border_side":0
}

{
  "comment":"----- Green Horizontal Line",
  "page": 2,"id": 12,
  "obj": "btn",
  "x": 10,"y": 45,"w": 470,"h": 2,
  "bg_color": "green",
  "bg_opa": 255,
  "border_width": 0
}

{
  "comment":"----- Attic label",
  "page":2,"id":2,
  "obj":"label",
  "x":@p2-labels,"y":@p2r1,"h":50,"w":200,"text":"Attic:","align":0,
  "bg_color":"#2C3E50","text_color":"#FFFFFF"
}

{
  "comment":"----- Attic Temperature data",
  "page":2,"id":3,
  "obj":"label",
  "x":@p2-values,"y":@p2r1,"h":50,"w":200,"text":"p2b3","align":0,
  "text_color":"#FFFFFF"
}
```
Notice that the x: and y: positions are populated with variables named @p2-labels, @p2-values and @p2r1.  
The file: pages.ini (below) is where the variables are defined. (You can use any name for your variables). Sounds like a lot of work, but it makes moving whole columns or rows of objects easy. For example if I want all of my object labels to start on a different X position, I only have to make a single change in the pages.ini file.  

2. Create a variables key:value file named **pages.ini**  
Example:  
```
@p1-labels:10
@p1-values:160
@p1r1:180
@p1r2:220
@p1r3:260
@p1r4:300

@p2-labels:10
@p2-values:180
@p2r1:80
@p2r2:120
@p2r3:160
@p2r4:200
@p2r5:240
```
**Execution**
1. In a cmd window, CD to the folder that contains **pages.py** and **pages.ini**.  
2. Run: python pages.py sample-pages  

The script pages.py will wrap all this up.  First it merges all of your page.src files into a single intermediate file, then makes the variable substitutions and outputs to the **pages.jsonl** file that you send to the panel.  

<h3 align="center">Utilities</h3>

# compress.py - Compress the pages.jsonl input file by removing unnecessary whitespace.
## Useage:
python compress.py sample-pages/page0.src page0-compressed.src  


# expand.py - Exoands the pages.jsonl input file by placing every element on its own line.
## Useage:
python expand.py sample-pages/page0-compressed.src page0-expanded.src  

# Plate screenshot overlay.psd - A photoshop tool for designing pages