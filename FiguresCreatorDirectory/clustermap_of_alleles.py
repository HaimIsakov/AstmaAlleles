import os
from functools import reduce

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from FiguresCreatorDirectory.analyze_results_with_zero_unsignificant_coefs import zero_unsignificant_coefs


def create_alleles_coefs_df_all_models(tuple_coefs_pvalues):
    dataframes_list = []
    for coefs_file, pvalues_file, model_name in tuple_coefs_pvalues:
        coef_df = zero_unsignificant_coefs(coefs_file, pvalues_file, alpha=0.05)
        coef_df.rename(columns=lambda x: x.replace('_coefs', ''), inplace=True)
        coef_df.rename(columns=lambda x: model_name + "_" + x, inplace=True)

        dataframes_list.append(coef_df)
    df_merged = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='inner'),
                       dataframes_list)
    df_merged = df_merged.loc[~(df_merged == 0).all(axis=1)]
    df_merged.to_csv("df_all_allleles_all_models.csv")
    return df_merged


def plot_cluster_map(df):
    print(df.shape)
    np_mat = df.values
    for i in range(np_mat.shape[0]):
        for j in range(np_mat.shape[1]):
            if np_mat[i, j] < 0:
                np_mat[i, j] = np_mat[i, j] - 2
            if np_mat[i, j] > 0:
                np_mat[i, j] = np_mat[i, j] + 2
    df = pd.DataFrame(np_mat,
                      index=df.index,
                      columns=df.columns)
    cg = sns.clustermap(df, cmap=sns.color_palette("vlag", as_cmap=True), linewidths=0.1, linecolor='gray',
                        xticklabels=df.columns, yticklabels=df.index, mask=(df==0), vmin=-3, vmax=3)
    cg.ax_heatmap.set_yticklabels(cg.ax_heatmap.get_ymajorticklabels(), fontsize=6)
    plt.tight_layout()
    plt.savefig("clustermap_alleles_models.pdf")
    plt.show()


if __name__ == "__main__":

    coefs_file1 = os.path.join("..","AstmaResults31.01.21", "astma_alleles", "blacken_data",
                              "heterzygots_astma_alleles_coefs.csv")
    pvalues_file1 = os.path.join("..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
                                "heterzygots_astma_alleles_pvalues.csv")
    # kwargs = {"colors": ['purple', 'red'],
    #           "save_file_name": "heterzygots_astma_alleles"}

    coefs_file2 = os.path.join("..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
                              "heterzygots_allergic_astma_coefs.csv")
    pvalues_file2 = os.path.join("..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
                                "heterzygots_allergic_astma_pvalues.csv")
    # kwargs = {"colors": ['darkgreen', 'lime'],
    #           "save_file_name": "heterzygots_allergic_asthma"}

    coefs_file3 = os.path.join("..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
                              "heterzygots_astma_severity_alleles_mild_vs_severe_coefs.csv")
    pvalues_file3 = os.path.join("..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
                                "heterzygots_astma_severity_alleles_mild_vs_severe_pvalues.csv")
    # kwargs = {"colors": ['blue', 'cyan'],
    #           "save_file_name": "heterzygots_asthma_severity"}

    coefs_file4 = os.path.join("..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "blacken_data",
                              "heterzygots_normal_vs_overweight_astma_alleles_coefs.csv")
    pvalues_file4 = os.path.join("..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "blacken_data",
                                "heterzygots_normal_vs_overweight_astma_alleles_pvalues.csv")
    # kwargs = {"colors": ['darkorange', 'gold'],
    #           "save_file_name": "heterzygots_astma_normal_vs_overweight"}

    coefs_files = [coefs_file1, coefs_file2, coefs_file3, coefs_file4]
    pvalues_files = [pvalues_file1, pvalues_file2, pvalues_file3, pvalues_file4]
    model_names = ["alleles", "allergic", "severity", "bmi"]

    tuple_coefs_pvalues = [(coef_file, pvalues_file, model_name) for coef_file, pvalues_file, model_name in
                           zip(coefs_files, pvalues_files, model_names)]
    df_merged = create_alleles_coefs_df_all_models(tuple_coefs_pvalues)
    plot_cluster_map(df_merged)