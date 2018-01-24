# TCLC Phase 2
This is the repo for the second phase for TCLC project
involving basic parsing and visualization of scraping results

### There are three folders in the master branch.   
 
1.  **data** - contains the output from the scraping component (currently in csv and json format) as well as phrases for categorizing this  output  
 
2. **temp** - contains  the output from the analysis component that will subsequently be used by the visualization component.  
 
3. **results** - contains the output from the visualization component

 **parameter-file.txt** specifies the parameters and values to be used by the different analysis, scraping and visualization components.
 
There are 3 text files (instructions for xxxx.txt), where xxxx is 
* analysis
* scraping 
* visualization.  

This should provide instructions for running these 3 components; for e.g. what Python libraries to import, any setup required, etc. It should be completed by the developers responsible for each of these components.
 
 There are 3 branches in addition to the master branch which correspond to each of these 3 components 
 * analysis 
 * scraping 
 * visualization. 
 
 All code development should be confined to these branches until it has been tested to be working for a specific features. Then issue a pull-request and I will merge the required branch into the master branch. 

## How to get started
First, clone the project 
```
git clone https://github.com/fesvictor/TCLCPhase1
```
Secondly, install all the necessary packages 
```
pip install -r requirements.txt
```
Now you can run anyfile by running, for example :
```
py Analysis.py
```

### How to regenerate `requirements.txt` ?
```
pipreqs ./ --force
```
Basically, `pipreqs` will scan through all `*.py` files to see what import is required. For more information, read [here](http://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/).

