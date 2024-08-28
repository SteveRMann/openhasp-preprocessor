<h3 align="center">OpenHASP Preprocessor</h3>

---

<p align="center"> Making pages.jsonl manageable.
    <br> 
</p>

<p align="center"> I am not an expert. Mistake me for one at your own risk.
    <br> 
</p>


## 📝 Table of Contents
- [Description](#description)
- [Usage](#usage)
  - [Preparation](#preparation)
  - [Execution](#execution)
- [Errors](#errors) 
- [Utilities](#utilities)


## 🎈 Description <a name = "description"></a>

- This Python script allows you to manage each page of an OpenHASP display in separate .src files.
- The script also looks for possible errors that would prevent your page from loading into the panel.
- Managing page files is enhanced with comments and variables substitutions.

## 🚀 Usage <a name = "usage"></a>

### Preparation <a name = "preparation"></a>

1. Create a .src file in a pages folder for each page.  
For example **page2.src** is the **jsonl** code for everything that will appear on page 2.  
  
```
{
  "comment":" ------------------------- Page 2 - Temperatures -------------------------"
}

# ********** Page title **********
{
  "comment":"----- PageTitle",
  "page":2,"id":1,
  "obj":"btn",
  "x":120,"y":0,"w":240,"h":40,
  "text":"Temperatures","align":2,"value_font":22,
  "bg_opa":0,"text_color":"gray","radius":0,"border_side":0
}

# *************** Horizontal Line ***************
# 
{
  "comment":"----- Green Horizontal Line",
  "page": 2,"id": 12,
  "obj": "btn",
  "x": 10,"y": 45,"w": 470,"h": 2,
  "bg_color": "green",
  "bg_opa": 255,
  "border_width": 0
}

# ********** Attic label and temperature **********
{
  "comment":"----- Attic label",
  "page":2,"id":2,
  "obj":"label",
  "x":@p2-labels,"y":@p2-row1,"h":50,"w":200,"text":"Attic:","align":0,
  "bg_color":"#2C3E50","text_color":"#FFFFFF"
}

{
  "comment":"----- Attic Temperature data",
  "page":2,"id":3,
  "obj":"label",
  "x":@p2-values,"y":@p2-row1,"h":50,"w":200,"text":"p2b3","align":0,
  "text_color":"#FFFFFF"
}
```
**Notes**  
```
1. The x: and y: positions are populated with variables named @p2-labels, @p2-values and @p2-row1.  
The file: pages.ini (below) is where the variables are defined. (You can use any variable names).

Note- Variable names are case-insensitive.

Sounds like a lot of work, but it makes moving whole columns or rows of objects easy.
For example if I want all of my object labels to start on a different X position, I only have to
make a single change in the pages.ini file.  

2. Comments starting with a # are ignored in the processing  
```

2. Create a variables key:value file named **pages.ini**  
Example:  
```
# Page 1
@p1-labels:10
@p1-values:160
@p1-row1:180
@p1-row2:220
@p1-row3:260
@p1-row4:300

#Page 2
@p2-labels:10
@p2-values:180
@p2-row1:80
@p2-row2:120
@p2-row3:160
@p2-row4:200
@p2-row5:240
```

**Notes**  
```
1. Comments starting with a # are ignored in the processing  
```


**Execution**<a name = "execution"></a>
1. In a cmd window, CD to the folder that contains **pages.py** and **pages.ini**.  
2. Run: python pages.py sample-pages  

The script pages.py will wrap all this up.  First it merges all of your page.src files into a single intermediate file, then makes the variable substitutions and outputs to the **pages.jsonl** file that you send to the panel.  

### 💡 Errors <a name = "errors"></a>

Duplicate page:id values

Duplicate pages.ini variable names

Last line inside block does not have an even number of quotes

Last line inside block ends with a comma

Line inside block does not end with a comma

Line inside block does not have an even number of quotes

Line is not inside a data block

The source directory does not exist

Unmatched closing brace (no opening brace)

Unmatched opening brace (no closing brace)


---
## 🚀 Utilities <a name = "utilities"></a>

### compress.py
Compress the input file by removing unnecessary whitespace.
```Useage:
Usage: python compress.py inputfile outputfile
```

### expand.py
Expands the pages.jsonl input file by placing every element on its own line.
```Useage:
usage: expand.py [-h] [-o OUTPUT] input_file
If the output is not specified, the input file is overwritten.
```

### page-index.py
Makes an index of all page, ID and comment values in the pages.src files.
```Useage:
python page-index.py [-h] [-o OUTPUT] pagesfolder
```

### Plate screenshot overlay.psd
A photoshop tool for designing pages
