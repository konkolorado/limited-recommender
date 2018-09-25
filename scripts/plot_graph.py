"""
Helped function to plot data using matplotlib
"""

import matplotlib.pyplot as plt


def plot_top_n(data_counts, title, xlabel, top=10):
    """
    Produces a matplotlib plot with the given title and xlabel
    displaying the top results in data_counts
    Params:
        data_counts: a Counter object
        title, xlabel: strings
        top: optional integer arg
    """
    most_numerous = data_counts.most_common(top)
    items, counts = zip(*most_numerous)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(fontsize=10, rotation=90)
    plt.scatter(items, counts)
    plt.show()
