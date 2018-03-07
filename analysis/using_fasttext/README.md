# Using Facebook's FastText to do semantic classification
The model is trained with amazon reviews data:
   - __label__1 means bad
   - __label__2 means good

## How to run the scripts?
First you need to configure `config.sh`:
- `fasttext_home` refer to the home directory of `fasttext` executable binary.
- `trained_model` refer to the trained fasttext model

After the configuration:
```
# Assume that you are in the directory of TCLCPhase2
cd ./analysis/using_fasttext
./run
```
## Reference
- https://fasttext.cc/docs/en/supervised-tutorial.html
- https://www.kaggle.com/bittlingmayer/amazonreviews