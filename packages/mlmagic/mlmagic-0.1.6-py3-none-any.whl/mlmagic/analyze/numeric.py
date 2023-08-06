import numpy as np
import matplotlib.pyplot as plt


def find_numeric_vars(df):
    """
    Finds all the numeric variables in the dataset
    :param df: Pandas dataframe
    :return: List of all the numeric variable names
    """
    return [var for var in df.columns if df[var].dtypes != 'O']


def find_discrete_vars(df, threshold=20, excluded_vars=''):
    """
    Find all the discrete variables in the dataset.
    :param df: Pandas dataframe
    :param threshold: Cut off to decide when a value is considered discrete
    :param excluded_vars: List of column names to exclude
    :return: List of all the discrete variable names
    """
    num_vars = find_numeric_vars(df)
    return [var for var in num_vars if len(df[var].unique()) < threshold and var not in excluded_vars]


def bar_plot_discrete_vars(df, discrete_vars, target):
    """
    Create bar plots for the discrete variables, in relation to the target variable
    :param df: Pandas dataframe
    :param discrete_vars: List of all the discrete variables
    :param target: The target variable
    :return: Plots of all the discrete variables in relation to the target variable
    """
    for var in discrete_vars:
        df.groupby(var)[target].median().plot.bar()
        plt.title(var)
        plt.show()


def find_continuous_vars(df, threshold=20, excluded_vars=''):
    """
    Find all the discrete continuous in the dataset.
    :param df: Pandas dataframe
    :param threshold: Cut off to decide when a value is considered continuous
    :param excluded_vars: List of column names to exclude
    :return: List of all the continuous variable names
    """
    num_vars = find_numeric_vars(df)
    return [var for var in num_vars if len(df[var].unique()) > threshold and var not in excluded_vars]


def hist_plot_continuous_vars(df, continuous_vars, target, bins=20):
    """
    Create histogram plots for the continuous variables, in relation to the target variable
    :param df: Pandas dataframe
    :param continuous_vars: List of all the continuous variables
    :param target: The target variable
    :param bins: Number of bins te create for the histograms
    :return: Plots of all the continuous variables in relation to the target variable
    """
    for var in continuous_vars:
        df[var].hist(bins=bins)
        plt.ylabel(target)
        plt.xlabel(var)
        plt.title(var + 'vs. ' + target)
        plt.show()


def normalize_continuous_vars(df, continuous_vars):
    """
    Normalize the continuous variables
    :param df: Pandas dataframe
    :param continuous_vars: List of continuous variable names
    :return: Pandas dataframe with normalized continuous variables
    """
    for var in continuous_vars:
        if 0 in df[var].unique():
            pass
        else:
            df[var] = np.log(df[var])
    return df


def scatter_plot_continuous_vars(df, continuous_vars, target, normalize=False):
    """
    Create a scatter plot of the continuous variables on the target
    :param df: Pandas dataframe
    :param continuous_vars: List of continuous variables
    :param target: The dependent variable
    :param normalize: Whether the variables should be normalized
    :return: Scatter plot for all the continuous variables related to the target
    """
    skipped = []

    if normalize:
        for var in continuous_vars:
            if 0 in df[var]:
                skipped.append(var)
                pass
        df[target] = np.log(df[target])
        print('Could not normalize the following variables: ', skipped)

    for var in continuous_vars:
        plt.scatter(df[var], df[target])
        plt.ylabel(target)
        plt.ylabel(var)
        plt.show()


def box_plot_continuous_vars(df, continuous_vars, normalize=False):
    """
    Show boxplot per continuous variable to expose outliers
    :param df: Pandas dataframe
    :param continuous_vars: List of continuous variables
    :param normalize: Whether data should be normalized
    :return: Box plot of all the continuous variables
    """

    skipped = []

    if normalize:
        for var in continuous_vars:
            if 0 in df[var].unique():
                skipped.append(var)
                pass
        print('Could not normalize the following variables: ', skipped)
    for var in continuous_vars:
        plt.boxplot(column=var)
        plt.title(var)
        plt.ylabel(var)
        plt.show()
