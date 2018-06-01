# What is analysis process doing?
## The analysis process is doing 4 things:
1. Process raw data
2. Remove unrelated data
3. Label semantic
4. Classification

Note that each of the process belongs to one folder.  
Each process is further explained below.

---

## 1. Process raw data
### Why do we need this step?
Because all of the scraped data have different format. If we do not unify the data into a single format, it will be hard to analyze it.

So, in this step, we will transform all the scraped results from various sources into a list of `Post` objects.  


Example of a `Post` object is as follows:
```json
{ 
	"date": "20170306",
	"value": "who will be pakatan's answer to najib?",
	"origin": "scrape-results/blog/rockybru_20170801_160034.csv",
	"source": "blog",
	"related_to": null,
	"semantic_value": {
		"positive": false,
		"negative": false
	}
}
```

|Property|Meaning|  
|--|--| 
|`date`|When is this post written|  
|`value`|What is written by the author|  
|`origin`|This post is belonging to which file|  
|`source`|Type of source|
|`related_to`|This post is related to which political figure/party (example Najib)|  
|`semantic_value`|Does this post carries a negative or positive value?|  


### How it works?
- First, load the scrape results from the following folder:
	- `scrape-results`
- Then, load the transformer (which will be called as parsers in the actual code) to transform the data from various sources.
	- For example, to transform the scraped data from `lowyat.net`, we will use the function `parse_lowyat`
- After the transformation is done, save the list of `Post` objects to the following files:
	- `analysis/_1_process_raw_data/output/english.json`
	- `analysis/_1_process_raw_data/output/chinese.json`

---

## 2. Remove unrelated data
In this step, we will remove all the data that is not related to this project.  

### How is a post consider related?
When a post contains the name of a political leader/party.  
For example, the following sentences is consider *related*.
```
Najib receive donation.

Pakatan harapan is my hope.
```
And the following sentence is consider *unrelated*.
```
I think we need to ban GST.

Why is roti canai so expensive?
```
### How this step works?
- First, we will load the names of party and leaders from the following files:  
 	- `keywords/target/leader.json` 
	- `keywords/target/party.json`
- Then, we will load all the `Post` object produced by the previous process (which Process Raw Data) from the following files:
	- `analysis/_1_process_raw_data/output/english.json`
	- `analysis/_1_process_raw_data/output/chinese.json`
- After that, we will check the `value` of each `Post` object to see if they contains any keywords, if they did, we will assign the value to the `related_to` property.
- Then, remove all the `Post` object which its `related_to` property is still null from the original list of `Post` object.
- Lastly, save the modified list of `Post` objects into the following folder:
	- `analysis/_2_remove_unrelated_data/`
- The output shall be named:
	- `english.json`
	- `chinese.json`

### Example
Suppose we have the following `Post` object.
```json
{ 
	"date": "20170306",
	"value": "Najib vs mahathir",
	"origin": "scrape-results/blog/rockybru_20170801_160034.csv",
	"source": "blog",
	"related_to": null,
	"semantic_value": {
		"positive": false,
		"negative": false
	}
}
```
Then, after this process, it will look like the following:
```json
{ 
	"date": "20170306",
	"value": "Najib vs mahathir",
	"origin": "scrape-results/blog/rockybru_20170801_160034.csv",
	"source": "blog",
	"related_to": [ "najib", "mahathir" ],
	"semantic_value": {
		"positive": false,
		"negative": false
	}
}
```
---

## 3. Label semantic
During this step, we will label the semantic value of each `Post` object.  

Wait, what is **semantic value**?  It means the **meaning** of the sentence.

For example, 
```js
"Najib sucks" // Negative 

"I love Najib" // Positive 

"Najib giving speech" // Neutral 

"I love Najib but he sucks" // Both positive and negative
```

### How this step works?
Actually, every step works the same way, which are:
- First, load the output from the previous process
- Process the data (in this step is to label the semantic value)
	- Load the semantic keywords from the following files:
		- `keywords/polarity/english_positive.txt`
		- `keywords/polarity/english_negative.txt`
		- `keywords/polarity/chinese_positive.txt`
		- `keywords/polarity/chinese_negative.txt`
	- Check the occurence of those semantic keywords for each `Post` object
- Save it as `english.json` and ` chinese.json`

### Actual example
Suppose we have the following `Post` object.
```json
{ 
	"date": "20170306",
	"value": "Najib is corrupted",
	"origin": "scrape-results/blog/rockybru_20170801_160034.csv",
	"source": "blog",
	"related_to": [ "najib" ],
	"semantic_value": {
		"positive": false,
		"negative": false
	}
}
```
After this process, it shall looks like:
```json
{ 
	"date": "20170306",
	"value": "Najib is corrupted",
	"origin": "scrape-results/blog/rockybru_20170801_160034.csv",
	"source": "blog",
	"related_to": [ "najib" ],
	"semantic_value": {
		"positive": false,
		"negative": true 
	}
}
```
The only difference is the `semantic_value.negative` property which is changed from `false` to `true`.

---

## 4. Classification
This is the last step of the analysis process, which is to produce output that will be used for **generating graphs**. 

During this step, we will:
```
Count the number of negative/positive/neutral post for each leader/party across a specified time period.
```
Ok, I know it's hard to understand, but no worries, let's look at an example output:
```json
{
	"start_date": "20180101", 
	"end_date": "20180105", 
	"language": "english", 
	"data": {
		"najib": {
			"positive": [0,0,0,0,0], 
			"negative": [9,9,9,9,9], 
			"neutral": [0,0,0,0,0]
		}, 
		"mahathir": {
			"positive": [9,9,9,9,9], 
			"negative": [0,0,0,0,0], 
			"neutral": [0,0,0,0,0]
		}, 
	}
}
```
What does the data means?
- `start_date`, `end_date` 
	- This value is specified by the clients, in this example, we can think that the client want the analysis from `1st of January 2018` to `5th of January 2018`.
- `language`
	- To identified the data is analyzed from `chinese` sources or `english` sources
- `data`
	- The data related to each political leader/party

Now, let's look at what the numbers mean.   

If you notice carefully, you can see that the `negative` property of `najib` is `[9,9,9,9,9]`, it means that there are **9** negative posts talking about Najib every day during the 5 days from `2018-01-01` to `2018-01-05`.

Then, using those data, we will generated graphs for each policitcal leader/party.

### Where are the output saved?
- `analysis/results/english_extracted.json`
- `analysis/results/chinese_extracted.json`

---

# How to run the code?
## Disclaimer
I will **only explain** things that **CANNOT** be found on Google. For example,
- How to generate the output for the first process?


That is to say, I will **not explain** that **CAN** be found on Google. For example,
- How to clone a project?
- How to run a Python file?

So, please do take your time to do some research about the terms that you don't understand.


Furthermore, whenever you see something as the following: 
```
python main.py
```
It means to open up your **terminal** and type in the code written in the grey box.

P/S: If you are using Windows, **terminal** means Git Bash, not Command Prompt or PowerShell.

## Recommended IDE
Visual Studio Code (not Visual Studio!)
- Please note that we will not use **button** to run the code, we will use **command** instead
- If you are using Windows, please use Git Bash to run the code which I will be mention later

### Why Visual Studio Code?
- Because it has built-in Integrated Terminal, which will be easy for us to run the code (as I mentioned we will not use *buttons*).
- Moreover, you can install the Python extension, which will provide you Intellisense support


## Prerequisite
- Install `Anaconda`. The instructions can be found at https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-16-04.
- Git clone this project 

## Steps
Please follow it carefully, missing any step may result in failure.
### 1. Create the `scrape-results` folder at the project root
(If you don't understand what is *project root* please Google it)
```
mkdir scrape-results
```

### 2. Download the scrape results 
You need to download them from the Google Drive folder (you need to ask from Dr. Victor to give you the access).  

Then, paste the files into the `scrape-results` folder.  

Note that the structure in the Google Drive will be a little different from the structure we need.   

So, make sure the folder structure is same as the following:
```.
scrape-results
├── blog
├── facebook
│   ├── chinese
│   └── english
├── forum
│   ├── carinet
│   ├── jbtalks
│   └── lowyat
├── news
│   └── malaysiakini
└── twitter
```
Within each directory (AKA folder) will be the respective scrape data, which is usually in the `.json` or `.csv` format.

### 3. Run the code
This step will be relatively simple as I had already written scripts for it.

#### To run every process at once
```
cd analysis
./run 
```

#### To run every process for english data only
```
cd analysis
./run --english
```

#### To run every process for chinese data only
```
cd analysis
./run --chinese
```

#### How to run only a specific process
For example, if I only wants to run `Process Raw Data` step:

```shell
cd analysis/_1_process_raw_data
./run
```

You can specify `--english` or `--chinese` if you want to run it for specific language.

## How to run test for each process?

Make sure you are in the directory of `analysis`.

```shell
./test
```

## How is the code structured?
Within each process (which is a folder), there will be 2 primary files:
- `main.py`
	- The python code for the process
- `run`
	- The shell script to run the `main.py`
```
analysis
├── run
├── _1_process_raw_data
│   ├── main.py
│   └── run
├── _2_remove_unrelated_data
│   ├── main.py
│   └── run
├── _3_label_semantic
│   ├── main.py
│   └── run
└── _4_classification
    ├── main.py
    └── run
```
Of course there are a lot more files than that, but the skeleton is basically as above.

## What is process 5 and process 6?
If you notice carefully, I did not mention the following process:
- `_5_analyze_source`
- `_6_analyze_keyword`

Both of this process is not the main job of the `analysis` process, they are just for:
- Analayze where the post comes from across a period of time 
- Analyze which keyword is the most popular 

If you want to understand more, just go into those folders and look at the `.png` files.


## Misc
### What is `using_fasttext` for?
Basically, it is to do supervised machine learning on those post objects using `fasttext`, so that in the future, we can use the model to predict the future scrape-results, because currently, we are using simple keyword matching only, which might not be very <del>efficient</del> effective.

By the way, `fasttext` is a machine learning library made my Facebook. (Google it for more infomation)

### What is `transform_format_for_mongodb` for?
This process is to transform the output data from `_2_remove_unrelated_data` to a format which will be used for another project, which is to 
- Let human to manually label the semantic value of each post

After that, we will obtain the labelled results and use it for machine learning as mentioned above.
