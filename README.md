# **SN_AI – Predicting Serie A Match Results Using RNNs**

---

## Introduction / Context

The **SN_AI** project aims to predict Serie A match results from the 2015/2016 season to the ongoing 2025/2026 season.  
We will use **Recurrent Neural Networks (RNNs)** to capture temporal dependencies in historical team data and generate probabilistic match outcome predictions.

**Note:** Match results depend on more than historical results. Real-life factors such as player fitness, absences, strategies, and transfer market dynamics cannot currently be modeled due to insufficient data.

---

## Dataset and Split

- **Dataset:** each match is represented as a JSON object containing date, teams, score, and match number.

```json
{
  "MatchNumber": 1,
  "RoundNumber": 1,
  "DateUtc": "2017-08-19 16:00:00Z",
  "Location": "Juventus Stadium",
  "HomeTeam": "Juventus",
  "AwayTeam": "Cagliari",
  "Group": null,
  "HomeTeamScore": 3,
  "AwayTeamScore": 0
}
```

**The dataset is divided in this way:**

- 70% for training
- 15% for validation
- 15% for testing

## Features

Main features used for the RNN:

- **Teams:** `home_team_name`, `away_team_name`
- **Recent performance (last 5 matches):**  
  `home_last5_points`, `away_last5_points`  
  `home_last5_goals`, `away_last5_goals`
- **Season averages:**  
  `home_avg_goals_scored`, `away_avg_goals_scored`  
  `home_avg_goals_conceded`, `away_avg_goals_conceded`
- **Elo ratings:**  
  `elo_home_team`, `elo_away_team`, `elo_diff`
- **Recent performance differences:**  
  `goal_diff_last5`, `points_diff_last5`
- **Match history last 2 seasons:**  
  `last2yrs_match_history`

---

## RNN Output

The network should output a Python object:

```python
result_predicted = {
    "home_win_prob": ...,
    "away_win_prob": ...,
    "draw_prob": ...,
    "home_goal_prediction": ...,
    "away_goal_prediction": ...,
    "over_2_5_prob": ...,
    "under_2_5_prob": ...
}
```

## Architecture and Method

- Network type: **RNN** (to capture temporal dependencies)
- Activation function: **ReLU**
- Loss function: **cross-entropy** (for result probabilities) and **MSE** (for goals)
- Backpropagation: **BPTT (Backpropagation Through Time)**
- Optimizer: **Adam**
- Regularization: **dropout and L2 weight decay**
- Validation: train/validation/test as indicated

---

## Evaluation

- Metrics:
  - Accuracy / F1-score / Precision / Recall (for win/draw/loss probabilities)
  - MAE / MSE (for predicted goals)
  - Confusion matrix
- Feature importance analysis to understand which features most influence predictions

---
