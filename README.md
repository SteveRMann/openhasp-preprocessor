# openhasp-preprocessor
A preprocessor for the pages.jsonl file.  This allows you to make the page definitions in separate files and use variables to define things like x: and y: positions or colors.

#Useage:
It's probably easier to just look at the example.  

1. Create a src file in a pages folder for each page.  
For example page2.src is the openHasp jsonl code for everything that will appear on page 2.
(Example below)

2. Create a substitutions key:value file named pages.sub  
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

Now, lets look at the example file: page2.src
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

Notice that the x: and y: positions are populated with @p2-labels, @p2-values and @p2r1. Look back at the file: pages.sub.  This is where the variable substitutions are defined. Sounds like a lot of work, but it makes moving whole columns or rows of objects easy. For example if I want all of my object labels to start on a different X position, I only have to make a single change in the pages.sub file.  

The Python script, pages.py will wrap all this up.  First it merges all of your page.src files into a single intermediate file, pages.src, then makes the variable substitutions and outputs to the pages.jsonl file that you send to the panel.  


