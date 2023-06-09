# Pipeline sub_churn_train

## Overview

A pipeline for creating a trained model for predicting whether or not a character will churn from their subscription.

## Pipeline inputs


- sub_churn_standard_features: A data set with all common features used for predicting whether a character will churn from their subscription.
- character_currency: Currency data for characters by month.

## Pipeline outputs

- sub_churn_fitted_pipeline: The newly trained model for subscription churn predictions.
- in_sample_score_report: A text file with the report of the score on the characters that we trained the model on (in-sample score).
