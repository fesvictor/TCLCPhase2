# Scrapping election results
## What will we be doing?
We will be scrapping the data from https://election.thestar.com.my/selangor.html


## What is it for?
It is to find out whether the analysis result based on social media truly reflects the result of election.

## Technology
We will be using Node.js and Cheerio.js, look at [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-node-js-request-and-cheerio-to-set-up-simple-web-scraping) to learn more.

## Language
Typescript.

## How to run the code?
First, install the required packages
```
cd scrapping-election-results
npm install 
```
Secondly, install Typescript
```
npm install -g ts-node
npm install -g typescript
```
Then, run 
```
ts-node scrape.js
```

## Suggested editor
Visual Studio Code.

## Output format
Look at the `outputInterfaces.ts`.
I will describe the format using Typescript's `interfaces`.