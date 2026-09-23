# ==============================================================================
# FILE: train_model.py
# PURPOSE: This is the "Teacher" script. It reads network traffic data,
#          learns what is normal vs. an attack, and saves that knowledge
#          as a file (the "trained model") so the website can use it later.
# ==============================================================================

# --- TOOLS WE NEED ---
# Think of these like importing tools from a toolbox before starting a project.
import pandas as pd      # pandas: reads and organises data like Excel spreadsheets
import numpy as np       # numpy: does fast math on large lists of numbers
import joblib            # joblib: saves and loads Python objects (like our trained model) to/from disk
import os                # os: lets Python talk to Windows (check files, create folders, etc.)
from sklearn.preprocessing import StandardScaler, LabelEncoder  # Tools that "clean" and normalise data
from sklearn.model_selection import train_test_split             # Splits data into teaching vs. testing portions
from sklearn.ensemble import RandomForestClassifier              # The actual AI brain (a "forest" of decision trees)


def run_training(dataset_path=None):
    """
    This is the main training function.
    Call this to teach the AI. It reads a CSV dataset, learns from it,
    and saves the trained model to the /model folder.
    """

    # --- STEP 1: FIGURE OUT WHERE WE ARE ---
    # Find the folder where this script lives on the computer.
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # The model folder is inside the same folder as this script.
    model_dir = os.path.join(base_dir, "model")

    # If no specific dataset was given, use the default training file.
    if not dataset_path:
        dataset_path = os.path.join(base_dir, "Dataset", "kdd_train.csv")

    # This is the full path where the finished model file will be saved.
    model_output_path = os.path.join(model_dir, "trained_rf_model.pkl")

    # --- SAFETY CHECK 1: Make sure the model folder exists and is writable ---
    # Create the folder if it doesn't exist yet (like creating a new drawer).
    if not os.path.exists(model_dir):
        try:
            os.makedirs(model_dir)
        except Exception as e:
            # If we can't create the folder, stop and report the error.
            return {"status": "error", "message": f"Could not create model directory: {str(e)}"}

    # Check that we actually have permission to save files in that folder.
    if not os.access(model_dir, os.W_OK):
        return {"status": "error", "message": "Model directory is not writable. Please check permissions."}

    print(f"Training model using data from: {dataset_path}")

    # --- SAFETY CHECK 2: Make sure the dataset file actually exists ---
    if not os.path.exists(dataset_path):
        return {"status": "error", "message": f"Dataset file not found: {os.path.basename(dataset_path)}"}

    try:
        # --- STEP 2: LOAD THE DATASET ---
        # Read the CSV file (like opening an Excel sheet).
        # We only take the first 20,000 rows to keep training fast.
        dataset = pd.read_csv(dataset_path, nrows=20000)

        # If the file was totally empty, stop and report.
        if dataset.empty:
            return {"status": "error", "message": "The provided dataset is empty."}

        # --- STEP 3: FIND THE "ANSWER" COLUMN ---
        # The dataset has many columns. One column holds the "answer" (is this traffic
        # normal or an attack?). We need to find which column that is.
        expected_labels = ['labels', 'Label', 'class3', 'class', 'target', 'Outcome', 'attack_type']
        target_col = None

        # Check the dataset columns against our known list of label names.
        for col in expected_labels:
            if col in dataset.columns:
                target_col = col
                break

        # If we didn't find it by exact name, try a broader search (case-insensitive).
        if not target_col:
            for col in dataset.columns:
                if any(kw in col.lower() for kw in ['label', 'class', 'target']):
                    target_col = col
                    break

        # If we still can't find the answer column, the dataset format is wrong — stop.
        if not target_col:
            return {"status": "error", "message": f"Invalid Dataset: No attack signature column found. Expected one of {expected_labels}"}

        # Rename it to 'labels' internally so the rest of the code is consistent.
        if target_col != 'labels':
            dataset.rename(columns={target_col: 'labels'}, inplace=True)

        # Save the unique list of attack types (e.g. "normal", "neptune", "smurf").
        labels_list = np.unique(dataset['labels']).ravel()

        # --- STEP 4: CONVERT TEXT TO NUMBERS ---
        # Computers can only do math on numbers, not words.
        # This step converts any text column (like "tcp", "udp") into numbers.
        label_encoder = []
        for col in dataset.columns:
            try:
                # If the column has words (not numbers), convert them.
                if not pd.api.types.is_numeric_dtype(dataset[col]):
                    le = LabelEncoder()
                    dataset[col] = le.fit_transform(dataset[col].astype(str))
                    # Save the encoder so we can use it again during prediction.
                    label_encoder.append([col, le])
            except Exception as e:
                return {"status": "error", "message": f"Character encoding failed on column '{col}': {str(e)}"}

        # --- STEP 5: CLEAN UP BAD NUMBERS ---
        # Replace infinity values and empty cells with 0.
        # Infinity values would break the math, so we swap them out.
        dataset.replace([np.inf, -np.inf], np.nan, inplace=True)
        dataset.fillna(0, inplace=True)

        # Pull out the "answer" column (Y) and make sure it's an integer.
        Y = dataset['labels'].values.ravel().astype('int')

        # We need at least 2 different attack classes to teach the AI.
        # If everything in the data is "normal", there's nothing to learn.
        if len(np.unique(Y)) < 2:
            return {"status": "error", "message": "Insufficient data: Model requires at least 2 distinct classes to train."}

        # Remove the "answer" column from the input data.
        # The AI should learn FROM the other columns, not by peeking at the answer.
        dataset.drop(['labels'], axis=1, inplace=True)

        # --- STEP 6: NORMALISE THE DATA (MAKE ALL NUMBERS COMPARABLE) ---
        # Some columns may have values like 0-1, while others go up to 1,000,000.
        # Scaling (StandardScaler) brings everything to a similar range so one big
        # number doesn't unfairly dominate the AI's learning.
        scaler = StandardScaler()
        try:
            X = scaler.fit_transform(dataset.values)
        except Exception as e:
            return {"status": "error", "message": f"Data normalization failed: {str(e)}. Ensure your dataset contains numeric features."}

        # --- STEP 7: SPLIT DATA INTO "TEACHING" AND "TESTING" PORTIONS ---
        # We set aside 20% of the data for testing (like a surprise exam).
        # The AI trains on the other 80%, then we test it on the 20% it never saw.
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # --- STEP 8: TRAIN THE AI ---
        # Random Forest = a collection of 100 "decision trees" that vote together.
        # Like asking 100 experts and going with the majority opinion.
        rf_cls = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_cls.fit(X_train, y_train)  # This is the actual "teaching" step.

        # --- STEP 9: TEST THE AI ---
        # Score the model on the 20% test data it has never seen.
        # Returns a number between 0.0 (terrible) and 1.0 (perfect).
        accuracy = rf_cls.score(X_test, y_test)

        # --- STEP 10: SAVE EVERYTHING TO DISK ---
        # Pack all the trained pieces into one dictionary and save as a .pkl file.
        # The website will load this file every time it starts up so it doesn't
        # have to re-train from scratch each time.
        model_data = {
            'rf_model': rf_cls,             # The trained AI brain
            'scaler': scaler,               # The normaliser (needed for prediction)
            'labels': labels_list,          # List of all attack types
            'label_encoder': label_encoder, # Text-to-number converters
            'feature_columns': dataset.columns.tolist()  # Column names used during training
        }

        joblib.dump(model_data, model_output_path)  # Save to the /model folder

        # Return a success message with stats.
        return {
            "status": "success",
            "accuracy": round(accuracy * 100, 2),  # e.g. 98.5 means 98.5% correct
            "model_path": model_output_path,
            "classes": labels_list.tolist(),
            "dataset_used": os.path.basename(dataset_path)
        }

    except Exception as e:
        # Catch-all: if something unexpected goes wrong, return the error message.
        return {"status": "error", "message": str(e)}


# --- THIS BLOCK ONLY RUNS WHEN YOU RUN THIS FILE DIRECTLY ---
# (Not when the website imports it as a module)
if __name__ == '__main__':
    result = run_training()

    # Print a formatted training report to the terminal.
    print("\n" + "="*60)
    print("🛡️  CYBERSHIELD AI: MODEL TRAINING REPORT")
    print("="*60)

    if result.get('status') == 'success':
        print(f"✅ STATUS:    SUCCESS")
        print(f"🎯 ACCURACY:  {result.get('accuracy')}%")
        print(f"💾 SAVED TO:  {result.get('model_path')}")

        classes = result.get('classes', [])
        print(f"\n🚀 DETECTABLE ATTACK CLASSES ({len(classes)}):")
        print("-" * 60)

        # Print the attack classes neatly in rows of 3.
        for i in range(0, len(classes), 3):
            row = classes[i:i+3]
            formatted_row = "  ".join(f"• {c:<18}" for c in row)
            print(formatted_row)
    else:
        print(f"❌ STATUS:    FAILED")
        print(f"⚠️  ERROR:     {result.get('message')}")

    print("="*60 + "\n")
