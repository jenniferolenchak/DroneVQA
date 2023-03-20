## Running notebooks from the Model Testing Folder
    
### 1. Create a new virtual environment for testing

```
python -m venv Testing_Venv
```

This folder was environement was created with python v3.10 and pip v22.3, but newer versions may also be functional.

### 2. Install Pytorch

Follow the Pytorch installation (https://pytorch.org/) 

Example command with Cuda:
```
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```

Example installation command without Cuda:
```
pip3 install torch torchvision torchaudio
```

### 3. Install all other dependencies

```
pip install -r requirements.txt
```

### 4. Now run any of the notebooks for testing