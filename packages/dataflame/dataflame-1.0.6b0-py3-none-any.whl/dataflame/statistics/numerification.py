__title__ = 'Project DataFlame'
__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credit__ = 'erLab - University of California, Los Angeles'

"""
    DataFlame: Utilities for Statistical Analysis
    ==========
    This module includes the main utilities that are to be used for statistical analysis of dataframes.
"""
# libraries
from typing import List
import pandas


def get_dataframe_column_layout(dataframe: pandas.DataFrame, column_name: str) -> List[str]:
    """
    The :func:`get_dataframe_column_layout` is responsible for getting a column name and a dataframe.
    What it does then, is that it first builds the list of unique elements that are present in the column,
    and also converts them to string so that the overall list becomes sortable. We do this because it would
    be a redundant operation to try to keep the layouts as well. Therefore, we are going to use
    a deterministic approach that is well-defined so that it is reusable in generating the layouts.
    The output of this function will also be used for the final numerification of the column by
    :func:`numerify_dataframe_column`.

    Parameters
    ----------
    dataframe: `pandas.DataFrame`, required
        The main dataframe to work with.
    column_name: `str`, required
        The name of the column for which the labels are required

    Returns
    ----------
    The output of this method, as expected, is of `List[str]` type.
    """
    return sorted([str(e) for e in dataframe[column_name].astype('str').unique().tolist()])


def numerify_dataframe_column(dataframe: pandas.DataFrame, column_name: str) -> None:
    """
    The :func:`numerify_dataframe_column` assists us in numerifying a column in a dataframe. Using
    this function, the system automatically generates and computes the layout for the column and
    then uses it to convert types into str. Note that this function does not return anything
    and the numerification is performed in-place on the dataframe.

    Parameters
    ----------
    dataframe: `pandas.DataFrame`, required
        This parameter is used to deal with the dataframe that is passed to the function. That
        dataframe is going to undergo changes and the changes will be performed in place meaning
        that there is nothing retunred by this function but the dataframe is changed itself.
    column_name: `str`, required
        This is the name of the column to be numerified.

    """
    # getting the layout
    dataframe[column_name] = dataframe[column_name].astype('str')
    layout = get_dataframe_column_layout(dataframe, column_name)

    # categorizer function
    def internal_numerifier(x):
        return float(layout.index(str(x)))

    # apply it
    dataframe[column_name] = dataframe[column_name].apply(internal_numerifier)


def numerify_dataframe(dataframe: pandas.DataFrame, verbose: bool = False) -> None:
    """
    The :func:`numerify_dataframe` is provided to take a dataframe, and without considerations of
    types and values in each column, it converts and tries to numerify everything.

    Parameters
    ----------
    dataframe: `pandas.DataFrame`, required
        This parameter is used to deal with the dataframe that is passed to the function. That
        dataframe is going to undergo changes and the changes will be performed in place meaning
        that there is nothing retunred by this function but the dataframe is changed itself.
    verbose: `bool`, optional (default=False)
        If true, messages regarding the activity of the function are printed to the function.

    """

    for column in dataframe.columns.tolist():
        if verbose:
            print("numerifying column: {}       \n".format(column))
        numerify_dataframe_column(dataframe, column)
