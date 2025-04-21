import os
import app # Assuming your main script is app.py
import json # Import the json library

# Test if the model file is created after running the main script
def test_model_file_created():
    # Ensure data exists before running app.main()
    if not os.path.exists('data/credit_card_records.csv'):
        print("Data file not found. Generating data...")
        # You might need to adjust how generate.py is called if it's not directly runnable
        # This assumes generate.py is in a 'util' subdirectory relative to tests.py
        # Or more robustly, find the absolute path if needed.
        # For simplicity now, let's assume it's runnable if needed,
        # but ideally the data should exist from a previous step.
        # If running generate locally first is the norm, we might skip generation here.
        # Let's rely on data being present from Step 0 for local tests.
        if os.path.exists('util/generate.py'):
             os.system('python util/generate.py') # Simple way, might need refinement

    app.main()  # Assuming the main function encapsulates the training logic
    assert os.path.exists('models/model.pkl')

# Test the model score: check type, range, and compare with historical scores
def test_model_score():
    # Ensure data exists if model needs retraining during test
    if not os.path.exists('data/credit_card_records.csv'):
         if os.path.exists('util/generate.py'):
             os.system('python util/generate.py')

    score = app.main()  # Assuming the main function returns the score
    print(f"Current model score: {score}") # Add print statement for clarity

    # Basic score checks
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

    # --- Start of new logic for Step 3 ---
    scores_file = 'model_scores.json'

    # Check if the scores file exists
    if not os.path.exists(scores_file):
         raise FileNotFoundError(f"Error: {scores_file} not found. Cannot compare scores.")

    # Load the model scores history
    try:
         with open(scores_file, 'r') as f:
             model_scores = json.load(f)
    except json.JSONDecodeError:
         raise ValueError(f"Error: Could not decode JSON from {scores_file}.")
    except Exception as e:
         raise IOError(f"Error reading {scores_file}: {e}")


    # Ensure the list is not empty and contains dictionaries
    if not model_scores or not isinstance(model_scores, list) or not all(isinstance(item, dict) for item in model_scores):
         raise ValueError(f"Error: {scores_file} should contain a non-empty list of score dictionaries.")

    # Get the latest score from the history file
    try:
        # Sort by version if needed, or assume last entry is latest
        # Assuming the last entry is the latest for simplicity
        latest_entry = model_scores[-1]
        if 'score' not in latest_entry:
             raise KeyError(f"Error: Latest entry in {scores_file} is missing the 'score' key.")
        latest_score = latest_entry['score']
        print(f"Latest historical score from {scores_file}: {latest_score}")

    except IndexError:
        raise ValueError(f"Error: {scores_file} is empty or has incorrect structure.")
    except KeyError as e:
         raise KeyError(f"Error accessing score data in {scores_file}: {e}")

