# Dayton Ohio Power Consumption

Our aim is to create a model that predicts hourly household power consumption for the next 24 hours from the current time.

There is one big issue here: First is that I haven't found any dataset for this that also has data going back more than a year or two. I did however find a dataset that gives us total power consumption per hour for Dayton Ohio from 2004 to 2018. The first section of this README shows how to get (roughly) an average household from this dataset.

## Setup

Dataset can be downloaded from [here](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)

Once downloaded, unzip the contents into the `data/00_preraw` folder.

We use specifically the Dayton hourly dataset. Since the consumption here is for the whole of dayton, we renormalise it down to a household level example by renormalising the dataset so that it's yearly power consumption for the last year is the same as the average power consumption for a Dayton OH household. According to energysage.com, [this is 13,092 kWh](https://www.energysage.com/local-data/electricity-cost/oh/montgomery-county/dayton/). 

Note: This was last updated in 2023, so this figure likely doesn't match up well with the average during our dataset. It would however bring the data to roughly the right order of magnitude, which can easily be adjusted later when we have better information.

This renormalisation is done by running the `00_data_prep` notebook in this folder and it produces the `01_raw/DAYTON_power_consumption.csv`, which is the data set the rest of the work is done on. In addition, this data is also split into train/CV/test datasets using this notebook and the data is saved to `02_intermediate/` under `{dataset name}_power.csv`.

## Assumptions of the renormalisation:

1. As noted above, that the average kWh number for Dayton in 2023 is the same as from 2017-08-04 to 2018-08-03. Probably only accurate up to an order of magnitude
2. That the total consumption time series is proportional to the consumption for a household. This is a poor assumption: It's very likely that industry makes up a large portion of the power consumption (or possibly even the majority) and the industry side of things likely has a very different pattern from household consumption.
3. That we can just sum up the MW values from the dataset to get MWh over a year. I'm not well versed in this context so I can't be 100% sure this is correct.
