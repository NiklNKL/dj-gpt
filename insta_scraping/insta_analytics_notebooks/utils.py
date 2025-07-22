import sys
import os
import json
import joblib
import shap
import pandas as pd

def load_results(load_dir):
    """
    Load a saved LGBM model along with its data, hyperparameters, and MAE from a directory.
    """
    if not os.path.isdir(load_dir):
        raise FileNotFoundError(f"Could not find directory '{load_dir}'.")

    model_path = os.path.join(load_dir, "final_model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Could not find model file '{model_path}'.")
    final_model = joblib.load(model_path)

    X_train = pd.read_parquet(os.path.join(load_dir, "X_train.parquet"))
    X_test = pd.read_parquet(os.path.join(load_dir, "X_test.parquet"))
    y_train = pd.read_parquet(os.path.join(load_dir, "y_train.parquet")).squeeze()
    y_test = pd.read_parquet(os.path.join(load_dir, "y_test.parquet")).squeeze()

    metadata_path = os.path.join(load_dir, "metadata.json")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Could not find metadata file '{metadata_path}'.")
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    return {
        "final_model": final_model,
        "X_test": X_test,
        "y_test": y_test,
        "X_train": X_train,
        "y_train": y_train,
        "best_hyperparams": metadata.get("best_hyperparams"),
        "best_error": metadata.get("best_mean_absolute_error")
    }

def save_results(output_dict, save_dir="lgbm_results"):
    """
    Save the model, training/test data, hyperparameters, and best error value in a directory.
    """
    os.makedirs(save_dir, exist_ok=True)

    model_path = os.path.join(save_dir, "final_model.pkl")
    joblib.dump(output_dict["final_model"], model_path)

    output_dict["X_train"].to_parquet(os.path.join(save_dir, "X_train.parquet"))
    output_dict["X_test"].to_parquet(os.path.join(save_dir, "X_test.parquet"))
    output_dict["y_train"].to_frame().to_parquet(os.path.join(save_dir, "y_train.parquet"))
    output_dict["y_test"].to_frame().to_parquet(os.path.join(save_dir, "y_test.parquet"))

    metadata = {
        "best_hyperparams": output_dict["best_hyperparams"],
        "best_mean_absolute_error": output_dict["best_error"]
    }
    with open(os.path.join(save_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"Results have been saved to '{save_dir}'.")

_path_added = False

def add_project_root_to_path():
    """
    Check if the project root directory is in the Python path.
    If not, add it to sys.path and change the working directory to the project root.
    """
    global _path_added

    if _path_added:
        return
    
    root_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))

    if root_dir not in sys.path:
        sys.path.append(root_dir)
        # print(f"Added {root_dir} to Python path.")
    
    if os.getcwd() != root_dir:
        os.chdir(root_dir)
        # print(f"Changed working directory to {root_dir}.")
    _path_added = True


def basic_shap_explainer(results):
    """
    Erstellt einen SHAP-Explainer und berechnet die SHAP-Werte für das gegebene Modell.
    """
    data_set = pd.concat([results["X_train"], results["X_test"]])
    final_model = results["final_model"]

    explainer = shap.TreeExplainer(model=final_model)
    shap_values = explainer(data_set)

    return shap_values


def explain_prediction(model, instance, explainer=None):
    """
    Erklärt eine einzelne Vorhersage mit SHAP.

    Parameter:
    - model: Das trainierte Modell (z. B. LightGBM)
    - instance: Eine Zeile als pd.Series oder pd.DataFrame (mit Feature-Namen!)
    - explainer: Optionaler SHAP Explainer (wird sonst neu erstellt)

    Rückgabe:
    - Dictionary mit Vorhersage, SHAP-Werten, Base-Value, Input-Features usw.
    """
    if not isinstance(instance, (pd.Series, pd.DataFrame)):
        raise ValueError("instance muss eine pd.Series oder pd.DataFrame mit einer Zeile sein.")

    instance_df = instance.to_frame().T if isinstance(instance, pd.Series) else instance

    # Explainer initialisieren, falls nicht mitgegeben
    if explainer is None:
        explainer = shap.Explainer(model)

    # SHAP-Werte berechnen
    shap_values = explainer(instance_df)

    return shap_values
