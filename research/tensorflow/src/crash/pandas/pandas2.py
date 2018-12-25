import numpy as np
import pandas as pd
import pandas1

cities = pd.DataFrame({'City name': pandas1.city_names, 'Population': pandas1.population})

if __name__ == '__main__':
    print(type(cities['City name']))
    print(cities['City name'])
    print(type(cities['City name'][1]))
    print(cities['City name'][1])
    print(type(cities[0:2]))
    print(cities[0:2])

    print(np.log(pandas1.population))

    populationMillions = pandas1.population.apply(lambda val: val > 1000000)
    print(populationMillions)

    cities['Area square miles'] = pd.Series([46.87, 176.53, 97.92])
    cities['Population density'] = cities['Population'] / cities['Area square miles']
    print(cities)

    # TODO
    '''
    Modify the cities table by adding a new boolean column that is True if and only if both of the following are True:
    - The city is named after a saint.
    - The city has an area greater than 50 square miles.
    Note: Boolean Series are combined using the bitwise, rather than the traditional boolean, operators.
          For example, when performing logical and, use & instead of and.
    Hint: "San" in Spanish means "saint."
    '''
