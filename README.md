# kedro-ml

## Overview

An simple example DS framework that enables experimentation and allows for collaboration between DSs and MLEs while also providing an easy way to produce production ready pipelines.

The example data and pipelines are used for training, predicting and scoring a model for predicting subscription churn from a synthesised dataset. Further details later on.

## How to install dependencies for developing

Brief version:

1. Ensure you have python version 3.10 installed directly on your machine (it may not be the standard python version). You'll either need the command (possibly python3.10) or you'll need the path to the 
   1. Note that installing python 3.10 in some virtual environment and then going from there can cause issues when using poetry.
2. Ensure you have poetry installed and on your path.
3. While in the root of this directory run the command `poetry env use $(which <python 3.10 command>)`, where `<python 3.10 command>` is the command you type to use python 3.10 on your system.
4. Next run `poetry install`


## Contents

There are 5 base pipelines:

1. `sub_churn_standard_features`: This pipeline produces a dataset for all non-currency features. Basically a small feature store. 
2. `sub_churn_train`: This is the pipeline that trains the model. 
3. `sub_churn_score`: This pipeline uses the model produced in `sub_churn_train` and gives a score, both in the logs and as an output (found in `data/08_reporting/score_report.txt`). This pipeline gets the predictions and compares against the actuals in one go. This pipeline is more for back-testing a model rather than for production use
4. `sub_churn_batch_predict`: This pipeline makes predictions for characters using the model created by `sub_churn_train` and saves them. This pipeline runs without any subscription miss data (which would be the case in a production setting).
5. `sub_churn_batch_score`: This creates a score for the predictions made in `sub_churn_batch_predict`. The idea being that we can run this pipeline after the churn data for the characters predictions produced by `sub_churn_batch_predict` is ready and get the score.

In addition to these 5 we also have 3 composite pipelines:
- `sub_churn_train_from_raw` which is just `sub_churn_standard_features` composed with `sub_churn_train`
- `sub_churn_score_from_raw` which is just `sub_churn_standard_features` composed with `sub_churn_score`
- `sub_churn_batch_score_from_raw` which is just `sub_churn_standard_features` composed with `sub_churn_batch_score`

You can run any of these using the command `poetry run kedro run -p <pipeline name>`, or if you're inside the poetry shell just `kedro run -p <pipeline name>`. You can also see any of the pipelines above mapped out by running `poetry run kedro viz` (or just `kedro viz` inside the shell).

### Other game example

One of the things we can do with Kedro is to set up separate environments with different parameters. One way this can be used is by having different params for different games. We have a set of pipelines that were created as an example of how we can produce different versions of a model for different games very easily: Each of the 8 pipelines mentioned above have game2 counterparts that are only available in the `game2_env`. They have their own separate configuration to produce the different models and keep the data separate.

You can run them by using `poetry run kedro run --env=game2_env -p <pipeline name>_game2`. Note the two differences with this command: 
1. We've added a `--env=game2_env` to switch to the other environment. The `_game2` pipelines aren't currently available through the default env.
2. We've added a `_game2` to the name. That way, when we're in the `game2_env` we still have access to the original pipeline (provided we don't overwrite the standard configuration in that environment).

### Additional content/features

1. Preprocessing steps for training are configurable: Many changes to the model - including the addition of some features and changing the preprocessing pipeline steps and even the prediction algorithm - can be done through the config files without any need to change the code itself.
2. Working library: Pipelines have been created using functions that can be easily reused in notebooks or other scripts. This can be done by either creating the notebook/script in this repository or by running `poetry build` and installing the resulting wheel in another repository. This new wheel won't be able to run Kedro commands and it won't have any of the configuration but all the pipeline definitions and functions will be available to import through `kedro_ml`.
3. Dockerfile: Builds the current repo into a new Docker image. There's also an accompanying script (`get_model.sh`) that can build and run the image, run the training pipeline and copy the result into the root directory of this repo (outside of the docker image).  
4. Decorator for logging seeds: For reproducibility and debugging purposes, if a node has a random element, we can add `@log_seed` to get a log of the random seed at the beginning of the node execution.

## Data

The sample synthesised data can be found in `data/01_raw` and it consists of 4 files. These files have been produced synthetically and randomly without any real underlying model, so training and predicting from them will not produce any meaningful results.

The data example is a sham dataset that is meant to look like it comes from game data. In particular, it's meant to describe player characters and subscriptions for the player characters. 

- `character_data.csv`: has some basic character information
- `character_currency.csv`: contains currency information for the character in question at the beginning of each month. The `hard` and `soft` prefixes refer to hard currency and soft currency that can be either bought or otherwise earned in game and spent on in-game items.
- `sub_data`: Players can sign up for a subscription to get hard and soft currency each month. There is no penalty for cancelling or otherwise not paying for subscriptions, they just stop getting the currencies for any month where they don't pay for the subscription. This is known as "missing" a subscription.
- `sub_miss`: Gives details on subscriptions that have missed. Any character that misses 3 months in a row is said to have churned, and the subscription will be cancelled entirely.

The example models attempt to predict if a character will soon churn.
