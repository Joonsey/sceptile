# Disease & Plant Convolution

### Quick start

#### Requirements

- poetry
- git lfs


To download training data there is a utility script
```sh
./scripts/download_data.sh
```
This will download the training data that is used
> NOTE: This is a *little* large, might take some time to download

The training should be primarily done within the `main.py` file and can be executed normaly with 
```sh
poetry run python main.py
```

### Dev rules

The interface is what we expect to export to other applications, nothing except for the interface class should be public at any time
