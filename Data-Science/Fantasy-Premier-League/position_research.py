import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def add_top_k_target(data, k, points_column="total_points"):
    data = data.copy()
    data["y"] = np.nan
    labeled = data[points_column].notna()
    rank = (
        data.loc[labeled]
        .groupby(["season", "GW"])[points_column]
        .rank(method="min", ascending=False)
    )
    data.loc[labeled, "y"] = rank.le(k).astype(float)
    return data


def top_ids_with_ties(group, column, k, id_column="element"):
    ranked = group[column].dropna().sort_values(ascending=False)
    if ranked.empty:
        return set()
    cutoff = ranked.iloc[min(k, len(ranked)) - 1]
    return set(group.loc[group[column].ge(cutoff), id_column])


def week_weight(data, id_column="element"):
    week_size = data.groupby(["season", "GW"])[id_column].transform("size")
    return (1 / week_size).to_numpy()


def rows_before(data, season, gw):
    season_order = data["season_order"]
    target_order = data.loc[data["season"].eq(season), "season_order"].iloc[0]
    return season_order.lt(target_order) | (
        data["season"].eq(season) & data["GW"].lt(gw)
    )


def score_origin(
    data,
    feature_columns,
    model_name,
    season,
    gw,
    k,
    id_column="element",
):
    train = data.loc[rows_before(data, season, gw) & data["y"].notna()].copy()
    valid = data.loc[
        data["season"].eq(season)
        & data["GW"].eq(gw)
        & data["total_points"].notna()
    ].copy()
    if train.empty or valid.empty:
        return None

    if model_name == "minutes_sort":
        scores = valid["minutes_ewm"].fillna(-np.inf).to_numpy()
    else:
        imputer = SimpleImputer(strategy="median", keep_empty_features=True)
        train_values = imputer.fit_transform(train[feature_columns])
        valid_values = imputer.transform(valid[feature_columns])
        if model_name == "logistic_regression":
            scaler = StandardScaler()
            train_values = scaler.fit_transform(train_values)
            valid_values = scaler.transform(valid_values)
            model = LogisticRegression(max_iter=1000, random_state=42)
        elif model_name == "gradient_boosting":
            model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=3,
                random_state=42,
            )
        else:
            raise ValueError(f"Unknown model: {model_name}")
        model.fit(train_values, train["y"], sample_weight=week_weight(train))
        scores = model.predict_proba(valid_values)[:, 1]

    scored = valid[[id_column, "name", "total_points"]].copy()
    scored["score"] = scores
    predicted = top_ids_with_ties(scored, "score", k, id_column)
    actual = top_ids_with_ties(scored, "total_points", k, id_column)
    overlap = len(predicted & actual)
    return {
        "season": season,
        "GW": gw,
        "model": model_name,
        "hit_rate": overlap / len(predicted) if predicted else np.nan,
        "correct": overlap,
        "n_predicted": len(predicted),
        "n_actual": len(actual),
    }


def compare_models(
    data,
    feature_columns,
    k,
    season="2025-26",
    development_weeks=range(1, 20),
    check_weeks=range(20, 39),
):
    data = add_top_k_target(data, k)
    rows = []
    for block, weeks in [
        ("development_gw1_19", development_weeks),
        ("historical_check_gw20_38", check_weeks),
    ]:
        for model_name in [
            "minutes_sort",
            "logistic_regression",
            "gradient_boosting",
        ]:
            for gw in weeks:
                result = score_origin(
                    data,
                    feature_columns,
                    model_name,
                    season,
                    gw,
                    k,
                )
                if result is not None:
                    result["block"] = block
                    rows.append(result)
    detail = pd.DataFrame(rows)
    summary = (
        detail.groupby(["block", "model"], as_index=False)
        .agg(
            mean_hit_rate=("hit_rate", "mean"),
            correct=("correct", "sum"),
            predictions=("n_predicted", "sum"),
            weeks=("GW", "nunique"),
        )
        .sort_values(["block", "mean_hit_rate"], ascending=[True, False])
    )
    return summary, detail
