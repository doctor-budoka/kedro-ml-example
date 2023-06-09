# Pipeline sub_churn_batch_predict

## Overview

This pipeline applies a previously fitted subscription churn model to a batch of characters and outputs the probabilities.

## Pipeline inputs

- sub_data: Data about individual subscriptions
- characters: Data about characters who have gotten a subscription
- character_currency: Currency balance data for characters by month
- sub_churn_fitted_pipeline: The current model for subscription churn predictions

## Pipeline outputs

- sub_churn_predict_batch_predictions: The predictions for the current batch
