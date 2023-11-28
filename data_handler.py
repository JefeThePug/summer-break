import pandas as pd
from tempfile import SpooledTemporaryFile


class DataHandler:
    """
    A class for handling data storage in a temporary database.

    Attributes:
        database (pandas.DataFrame): The main data stored.

    Methods:
        update_data(data):
            Update the database with new data from a CSV file.
        get_data() -> pd.DataFrame:
            Retrieve the current data stored in the DataFrame.

    Dunder Methods:
        __init__():
            Initializes an instance of the DataHandler class containing an empty pd.DataFrame.
        __repr__() -> str:
            Return a string representation of the pd.DataFrame
    """

    def __init__(self):
        """
        Initializes an empty pandas dataframe with columns ["Date", "Type", "Amount($)", "Memo"]
        """
        self.database = pd.DataFrame(columns=["Date", "Type", "Amount($)", "Memo"])

    def update_data(self, data: SpooledTemporaryFile):
        """
        Updates dataframe with new data

        Args:
            data: the .stream contents of the CSV file passed in an API POST request
        """
        try:
            new_df = pd.read_csv(data, names=["Date", "Type", "Amount($)", "Memo"])
            self.database = pd.concat(
                [self.database, new_df], ignore_index=True
            ).drop_duplicates()
        except Exception as e:
            raise ValueError(f"Error updating data: {str(e)}")

    def get_data(self) -> pd.DataFrame:
        """
        Return the current data

        Returns:
            pd.DataFrame: The dataframe containing the data
        """
        return self.database
    
    def __repr__(self) -> str:
        """
        Get a string representation of the DataFrame for debugging or visualization purposes

        Returns:
            str: The dataframe represented as a string
        """
        return str(self.database)
