from typing import Dict
import numpy as np
from typing import Generator, List
import os

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class Stats:
    def __init__(self) -> None:
        self._vals = []
        self._min = None
        self._max = None
        self._mean = None
        self._median = None
        self._std = None
        self._25 = None
        self._50 = None
        self._75 = None

    @staticmethod
    def to_float(val):
        try:
            return float(val)
        except:
            return None

    def get_stats(self) -> Dict:
        # calculate mean, std and percentiles only when required
        self.calculate_mean()
        self.calculate_std()
        self.calculate_25()
        self.calculate_50()
        self.calculate_75()

        return {
            'min': self._min,
            'max': self._max,
            'mean': self._mean,
            'median': self._median,
            'std': self._std,
            '25': self._25,
            '50': self._50,
            '75': self._75
        }

    def update_min(self, val: float) -> None:
        if self._min is None:
            self._min = val

        if val < self._min:
            self._min = val

    def update_max(self, val: float) -> None:
        if self._max is None:
            self._max = val

        if val > self._max:
            self._max = val

    def calculate_mean(self) -> None:
        self._mean = sum(self._vals) / len(self._vals)

    def calculate_std(self) -> None:
        self._std = np.std(self._vals)

    def calculate_25(self) -> None:
        self._25 = np.percentile(self._vals, 25)

    def calculate_50(self) -> None:
        self._50 = np.percentile(self._vals, 50)

    def calculate_75(self) -> None:
        self._75 = np.percentile(self._vals, 75)

    def update_stats(self, val) -> None:
        val = self.to_float(val)
        if val is None:
            return

        self._vals.append(val)
        self.update_min(val=val)
        self.update_max(val=val)


# Takes a few arguments: file path, separator, list of columns
class DataReader:
    def __init__(self, fp: str, sep: str, col_names: List) -> None:
        self._fp = fp
        self._sep = sep
        self._col_names = col_names

    # iter method which returns a generator
    def __iter__(self) -> Generator:
        """
        Input : None
        Output : Generator

        This method should return an iterable generator. Upon iteration the data should be of type Dict
        For example if the file format is as below:

        StockCode    , Description    , UnitPrice  , Quantity, TotalPrice , Country
        22180        , RETROSPOT LAMP , 19.96      , 4       , 79.84      , Russia
        23017        , APOTHECARY JAR , 24.96      , 1       , 24.96      , Germany

        The generator function should return the rows in the below format (dictionary):
        - keys are a list of columns
        - values will be values of each row from the file
        {
            'StockCode': '22180',
            'Description': 'RETROSPOT LAMP',
            'UnitPrice': 19.96,
            'Quantity': 4,
            'TotalPrice': 79.84,
            'Country': 'Russia',
        }
        """
    ######################################## YOUR CODE HERE ##################################################
    
    # output generator -- use 'yield' keyword 
    # generate each row: dictionary comprehension
    # Steps:
    # 1. read the file
    # 2. iterate over each row
    # 3. split each row based on the separator
    # 4. return the dictionary of each row
    # 5. yield
    # 6. return the generator as a dictionary in this format

        # for loop iteration iterates over filepath
        for n_row, row in enumerate(open(self._fp, "r")):
            # for each row, split it based on iterator
            row_vals = row.strip('\n').split(self._sep)

            # create a dictionary of each 
            # define the row_vals dictionary  
            # Dictionary comprehension to create a dictionary out of something
            # row_vals = [row_vals[i] for i in self._col_names]
                # zip these 2 lists together and access them as key-value pairs
            row_vals = { key: value for key, value in zip(self._col_names, row_vals) }
            # Append the row number to each dictionary object
            # row_vals['n_row'] = n_row

            # return results
            yield row_vals


    ######################################## YOUR CODE HERE ##################################################

    def get_file_path(self):
        return self._fp

    def get_column_names(self):
        return self._col_names

if __name__ == "__main__":
    # Define the path to the sample data, the separator, and the columns
    filepath = "../data/tst/2021.csv"
    separator = ","
    columns = ['StockCode', 'Description', 'UnitPrice', 'Quantity', 'TotalPrice', 'Country']

    # Create an instance of the DataReader
    reader = DataReader(filepath, separator, columns)

    # Loop through the generator and print each row
    for row in reader:
        print(row)