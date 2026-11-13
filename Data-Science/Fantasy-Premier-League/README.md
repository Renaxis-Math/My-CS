# Fantasy Premier League Player Shortlisting

This project builds leak-safe, position-specific shortlists for Fantasy Premier
League. It predicts tie-aware top-K membership by gameweek rather than exact
player order:

- Goalkeeper: top 5
- Defender: top 10
- Midfielder: top 10
- Forward: top 10

## Project structure

- `fantasy_premier_league.ipynb` — root data pipeline, shared feature
  engineering, frozen benchmarks, and current-gameweek predictions.
- `goalkeeper.ipynb` — goalkeeper-specific research.
- `defender.ipynb` — defender-specific research.
- `midfielder.ipynb` — midfielder-specific research, including matchup and
  opponent-style experiments.
- `forward.ipynb` — forward-specific research.
- `position_research.py` — shared tie-aware walk-forward evaluation utilities
  for the position notebooks.

The root notebook owns common data construction and definitions. Position
notebooks are research branches: a feature should only return to the root after
it survives the agreed validation process.

## Methodology

- One modeling row per player-gameweek after double-gameweek collapse.
- Stable FPL player codes connect a player's history across seasons.
- Every evaluated gameweek trains only on earlier rows.
- The target is tie-aware top-K membership.
- Hit rate is set overlap divided by predicted-list size; ordering within the
  shortlist does not matter.
- Each historical gameweek receives equal total training weight.
- Logistic regression, gradient boosting, and recent-minutes sorting are
  compared where applicable.
- Development and historical-check periods are kept separate. Historical
  checks discussed during feature design are not treated as untouched tests.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

The notebooks require internet access for the public Fantasy Premier League API
and the historical dataset maintained by
[vaastav/Fantasy-Premier-League](https://github.com/vaastav/Fantasy-Premier-League).

## Run order

1. Run `fantasy_premier_league.ipynb` from top to bottom.
2. The final root cell writes `fpl_feature_panel.pkl`.
3. Run `goalkeeper.ipynb`, `defender.ipynb`, and `forward.ipynb` in any order.
4. `midfielder.ipynb` currently performs its own historical loading and can run
   independently.

Rerun the root whenever source data or shared feature engineering changes.
`fpl_feature_panel.pkl` is generated locally and intentionally excluded from
Git, so a fresh clone must run the root before the dependent branches.

## Important limitations

- Exact player-versus-opponent history is usually too sparse to be reliable.
- Historical deadline injury and availability snapshots are unavailable.
- Goals and assists are rare events, so extreme weekly returns remain noisy.
- A historical improvement is only a shadow result until it is confirmed on a
  genuinely prospective block.
