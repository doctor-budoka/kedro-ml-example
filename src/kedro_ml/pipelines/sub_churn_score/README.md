# Pipeline sub_churn_score

## Overview

A pipeline for scoring characters who have been around long enough for us to have the full details. Useful for back-testing models.

## Pipeline inputs

- sub_churn_standard_features: A data set with all common features used for predicting whether a character will churn from their subscription.
- character_currency: Character currency data by month
- sub_churn_fitted_pipeline: The current model for subscription churn predictions

## Pipeline outputs

- score_report: A text file with the report. It contains separate scores for both general characters and newly subscribed characters (those who haven't had a subscription before)
