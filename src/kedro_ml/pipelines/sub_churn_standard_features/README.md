# Pipeline sub_chjrn_standard_features

## Overview

This pipeline is used to create a dataset of standard features for use in predicting whether a character/player will churn from their subscription

## Pipeline inputs

- sub_data: Data about individual subscription schedules
- characters: Data about characters who have gotten a subscription
- sub_miss: Data about subscription misses. A miss is a month where the subscription was not fulfilled (whether by cancellation or payment decline)


## Pipeline outputs

- sub_churn_standard_features: A data set with all common features used for predicting whether a character/player will churn from their subscription
