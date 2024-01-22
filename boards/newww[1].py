import shap
import matplotlib.pyplot as plt

# load JS visualization code to notebook
shap.initjs()

# Create the explainer
explainer = shap.TreeExplainer(rf)

shap_values = explainer.shap_values(X_test)

shap_values_list = [s.tolist() if isinstance(s, np.ndarray) else s for s in shap_values]

shap_summary_values = {
    "expected_value": explainer.expected_value.tolist(),
    "shap_values": shap_values_list,
    "feature_names": X_features
}

json_summary_plot = json.dumps(shap_summary_values)

import json
file_path = "/content/file1.json"
with open(file_path, 'w') as json_file:
    json.dump(json_summary_plot, json_file)


import numpy as np
X_test_dict = X_test.to_dict(orient='records')

json_X_test = json.dumps(X_test_dict)

file_path = "/content/file2.json"
with open(file_path, 'w') as json_file:
    json.dump(json_X_test, json_file)


print("Variable Importance Plot - Global Interpretation")
figure = plt.figure()
shap.summary_plot(shap_values, X_test)
