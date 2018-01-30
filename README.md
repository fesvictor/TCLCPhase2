# TCLC Phase 2
This is the repo for the second phase for TCLC project
involving basic parsing and visualization of scraping results

## Proccess (3 steps)
### 1. Scrapping
### 2. Analysis
The results generated at this phase will be located at :
```
analysis/results
```
The output file is name as `<language>_extracted.json`, for example: `english_extracted.json`

### 3. Visualization


## How to get started
### First, clone the project
```
git clone https://github.com/fesvictor/TCLCPhase1
```
### Secondly, install all the necessary packages 
```
pip install -r requirements.txt
```
### Thirdly, download the scrape-results from Google Drive
Now you can run anyfile by running, for example :
```
py Analysis.py
```

### How to regenerate `requirements.txt` ?
```
pipreqs ./ --force
```
Basically, `pipreqs` will scan through all `*.py` files to see what import is required. For more information, read [here](http://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/).


### Why Travis CI is not running `.travis.yml`?
There are 2 reasons:
- You misspelled `.travis.yml`
- The file contains error, you can those errors using [Travis Lint](https://lint.travis-ci.org/)