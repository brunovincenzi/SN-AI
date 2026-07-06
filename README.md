# SN_AI

SN_AI predicts Serie A match outcomes from historical match data using engineered numerical features and a PyTorch Multi-Layer Perceptron (MLP) classifier.

The current model predicts one of three classes:

- Home win
- Draw
- Away win

## Project Structure

- `SN_AI.ipynb`: main notebook for loading data, building features, training the model, evaluating results, and printing readable predictions.
- `json_files/`: normalized Serie A season JSON files used by the notebook.
- `json_files_generator/`: source/generated JSON files plus a conversion utility.
- `script_changeformatdate.py`: utility for normalizing `DateUtc` values in JSON files.
- `requirements.txt`: pinned direct dependencies from the local project environment.

## Data

Each JSON file contains one Serie A season. A match record includes fields such as:

```json
{
  "DateUtc": "2017-08-19 16:00:00Z",
  "HomeTeam": "Juventus",
  "AwayTeam": "Cagliari",
  "HomeTeamScore": 3,
  "AwayTeamScore": 0
}
```

Some files include extra metadata such as location, group, match number, or round number. The notebook keeps only the fields needed for modeling.

## Notebook Workflow

The notebook runs top to bottom through these stages:

1. Load all season JSON files from `json_files/`.
2. Parse matches and build chronological match histories for teams.
3. Split seasons into train, evaluation, and test sets.
4. Build pre-match engineered features.
5. Scale features using a `StandardScaler` fitted only on the training set.
6. Train a PyTorch MLP classifier.
7. Evaluate test accuracy, classification metrics, and confusion matrix.
8. Print readable match-by-match predictions.

## Temporal Split

The split is season-based:

- Training: `9495` through `1516`
- Evaluation: `1617` through `2021`
- Test: `2122` through `2526`

This keeps later seasons as future data instead of randomly mixing matches across time.

## Active Features

The active feature vector contains six numerical values:

- Elo rating difference
- Recent win-rate difference
- Recent draw-rate difference
- Current-season goal-difference variance difference
- Difference in each team's most recent encoded result
- Difference in each team's second-most recent encoded result

The target labels are:

```python
0 = Home win
1 = Draw
2 = Away win
```

## Model

The model is an MLP with:

- Two hidden linear layers
- Batch normalization
- ReLU activations
- Dropout
- Cross-entropy loss with balanced class weights and label smoothing
- Adam optimizer
- Reduce-on-plateau learning-rate scheduling
- Early stopping based on evaluation loss

## Reproducibility Notes

The notebook sets random seeds for Python, NumPy, and PyTorch. Exact neural-network metrics may still vary across hardware, PyTorch builds, and CPU/GPU execution details.

The JSON file iteration order is intentionally left unchanged in the notebook so the current behavior is preserved.

## Setup

Install the pinned dependencies:

```bash
pip install -r requirements.txt
```

Then open and run:

```bash
jupyter notebook SN_AI.ipynb
```

## Utilities

The conversion scripts can overwrite JSON files. Use them only when you intentionally want to regenerate or normalize dataset files.
