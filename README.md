# Pusle-heating_ML_MOS
Dataset and data process for Pulse Heating Combined with Machine Learning for Enhanced Gas Identification and Concentration Detection with MOS Gas Sensors

- The original test data is stored in the "data" folder.

- The file "get_csv_fortrain.py" in the "data" folder processes the original data to obtain data from different gas concentrations for the same type of sensor.

  The file "pdconcat.py" combines different CSV files into a single CSV file, resulting in a dataset with different types of gases and their concentrations.

  The file "std_calculate.py" performs standard deviation normalization on the dataset files.

- The processed data is stored in two separate folders, namely "0304" and "0401".
- The final dataset file is named "sensor_HCHO_ETH_C3H6O_std.csv".
