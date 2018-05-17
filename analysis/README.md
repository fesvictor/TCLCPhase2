# What is analysis process doing?
## Prerequisite
Make sure you install `Anaconda`. The instructions can be found at https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-16-04.
## 1. Output files in the following format 
```json
{
	startDate: "2017-08-01",
	endDate: "2017-12-31",
	language: "EN", // EN or CN or BM
	data:{
		candidate / party : {
			neutral: [], //List of numbers where length == endDate - startDate
			positive: [0, 1,2 ],
			negative: [],			
		}
	}
}

//for jh
{
	semantic_value:{
		positive: true,
		negative: false
	}
}
```
Note that `startDate` and `endDate` is given by client.

## 2. For every scrapped result, output a file for error checking in the future
### But how the file should be formatted?
This question remains unknown. Will need to ask Dr. Victor in the future again.

## How to run the whole process?
Make sure you are in the dir of `analysis`.
```
# To process only english data
./run --english

# To process only chiense data
./run --chinese

# To run the process for both language
./run
```

## How to run only a specific process

```shell
# For example, if I only want to run step 1
cd ./_1_process_raw_data
./run
```

You can specify `--english` or `--chinese` if you want to run it for specific language.

## How to run test for each process?

Make sure you are in the dir of `analysis`.

```shell
./test
```

## How to install missing packages?

```shell
python -m pip install <package_name>
```

That's all, enjoy!

## Algorithm benchmark

The benchmarker is named `benchmark_labelling_algo.py`.
```

regex = 5.67s
dic_and_tokens = 1.89s
```
So, `dic_and_tokens` is faster. 