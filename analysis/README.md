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
./run
```

## How to run test for each process?
Make sure you are in the dir of `analysis`.
```
./test
```

## How to install missing packages?
```
$ python -m pip install <package_name>
```
That's all, enjoy!