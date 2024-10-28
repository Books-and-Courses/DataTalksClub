import pickle
import pandas as pd

model_file = "../models/model1.bin"
dv_file = "../models/dv.bin"

# Load the DictVectorizer
with open(dv_file, 'rb') as f_in:
    dv = pickle.load(f_in)

# Load the model
with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)

# Verify everything is loaded
print(dv)
print(model)

# Test data
test = {"job": "management", "duration": 400, "poutcome": "success"}
X = dv.transform([test])

# Predict probability
print(model.predict_proba(X))

