import pandas as pd

city_names = pd.Series(['San Francisco', 'San Jose', 'Sacramento'])
population = pd.Series([852469, 1015785, 485199])

if __name__ == '__main__':
    print(pd.__version__)

    city_population = pd.DataFrame({'City name': city_names, 'Population': population})
    print(city_population)

    california_housing_dataframe = \
        pd.read_csv("https://download.mlcc.google.com/mledu-datasets/california_housing_train.csv",
                    sep=",")
    # print(california_housing_dataframe)
    description = california_housing_dataframe.describe()
    print(description)

    print(california_housing_dataframe.head())
