Folder with training code used for fine-tuning ViLT Transformer Model

First, ensure that you have a folder with images used for training in the "root" (line 26) location specified in the code.

Secondly, gather your labels and answer files, and input their locations in the appropriate spaces in the code. (Line 13 for questions, Line 38 for answers)

Finally, grab your base VilT model and input its location to the save line (Line 169)

Then simply execute the code, it does all the rest for you.

Afterwards the model you inputed in line 169 will be updated with the training executed by the code.