import numpy as np
import pandas1
import pandas2

if __name__ == '__main__':
    print(pandas1.city_names.index)

    print(pandas2.cities)
    print(pandas2.cities.index)

    cities = pandas2.cities.reindex([2, 0, 1])
    print(cities)
    print(cities.index)

    random_cities = cities.reindex(np.random.permutation(cities.index))
    print(random_cities)

    # TODO
    '''
    The reindex method allows index values that are not in the original DataFrame's index values.
    Try it and see what happens if you use such values! Why do you think this is allowed?
    '''
