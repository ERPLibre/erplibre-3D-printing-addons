# Slicing Profile Script

---

Basic Python script to generate the model for the *web_slicing_profile* module from the configuration file of the actual
***SuperSlicer*** instance installed for usage.

## Usage
In a terminal, in the directory with all the files (the script and the config files) :
```{r}
    python generate_model_skeleton.py
```
Or
```{r}
    py generate_model_skeleton.py
```

When successful, the file *slicing_profile.py* is generated. After some manuals editing, the final result would be like
[slicing_profile.py](slicing_profile.py)