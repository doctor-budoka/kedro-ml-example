# Pipeline sub_churn_batch_score

## Overview

Once a predicted batch has been around long enough for us to know whether or not they churned, we can run this pipeline to find out how the model did.

## Pipeline inputs

- sub_churn_standard_features: A data set with all common features used for predicting whether a character will churn from their subscription.
- sub_churn_predict_batch_predictions: The predictions for a set of characters/subscriptions.

## Pipeline outputs

- predict_batch_score_report: A text file with the report. It contains separate scores for both general characters and new characters (those who haven't had a subscription before)
