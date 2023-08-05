import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def vars_with_na(df):
    """
    Create a list of all the variables (columns) that have null values
    :param df: Pandas data frame
    :return: list of column names with missing values
    """
    return [var for var in df.columns if df[var].isnull().sum() > 1]


def vars_with_na_percentage(df):
    """
    Print out the list of all variables that have missing values, with their respective percentages
    :param df: pandas data frame
    :return: printed list of variables and pecentage of missing values
    """
    for var in vars_with_na(df):
        print(var, np.round(df[var].isnull().sum(), 3), '% missing values')


def analyse_na_value(df, target):
    """
    Print the difference in effect of missing values vs. non missing values on the target variable
    :param df: pandas dataframe
    :param target: the target variable to analyse
    :return: bar charts of all the variables with missing values, and their median salesprice
    """
    for var in vars_with_na(df):
        df[var] = np.where(df[var].isnull(), 1, 0)
        df.groupby(var)['SalePrice'].median().plot.bar()
        plt.title(var)
        plt.show()






