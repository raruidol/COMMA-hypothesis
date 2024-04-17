Setting up conda environment as follows should get it running on godel:

```
conda create -n hyp-env python=3.8.5

conda activate hyp-env

pip install -r custom_reqs.txt
pip install pydantic==1.9
pip install -r custom_reqs.txt
pip install accelerate -U
pip install torch==2.0.1
```
(actually I assume that first install of the *custom_reqs* before pydantic is redundant, this just appears to be the command history I recorded, so including it in case something odd happens that this would somehow resolve)


To prep data:
```
python preprocess_eimear_streamline.py
python data_split_eimear.py
```

To run transformers:
```
python fine_tune_LM.py --data [key]
```
where key is as described in the email. When creating new jsons of data, use the naming convention *[key]_hypothesis.json* to keep this flag usable.

I suggest that any new variants of extracted data are created by updating *preprocess_eimear_streamline.py* as that's the shortest version of the code. Likewise splitting by using data_split_eimear.py, where the new data can be split by adding its name to the list at the top of the file.


Additional notes:
- Please note that fine_tune_LM has been edited to use RoBERTa, not RoBERTa-Large as in the original reported results.
- Sorry for the silly extra filenames, this is the magic of research code assumed for personal only use... To prep data from the folder containing AIF (data_raw), first run *preprocess_eimear_streamline.py*. preprocess.py is the original (I think still vanilla?), then edited to *preprocess_eimear.py*, which I've ALSO kept for reference and then edited down to the _streamline version to make it easier to add more variants.