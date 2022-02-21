import os.path
from functools import reduce

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from FiguresCreatorDirectory.analyze_results_with_zero_unsignificant_coefs import coefs_external_effects, \
    zero_unsignificant_coefs


def create_amount_of_pos_neg_alleles_table(coefs_file, pvalues_file):
    coefs_df = zero_unsignificant_coefs(coefs_file, pvalues_file, alpha=0.05)
    cur_df_coefs_cols = [col for col in list(coefs_df.columns) if col.split("_")[-1] == "coefs"]
    prefixes = ["A", "B", "C", "DRB1", "DQB1"]  # For each locus
    grouper = [next(p for p in prefixes if p == c.split("*")[0]) for c in coefs_df.index]
    dataframes_list = []
    for coef_col in cur_df_coefs_cols:
        print(coef_col)
        new_coef_col = coef_col.replace("_coefs", "")
        counts_grouped_df = coefs_df.groupby(grouper, axis=0)[coef_col]  # group the coefs_df according to each locus
        locus_pos_neg_count_table = counts_grouped_df.agg(pos_count=lambda s: s.gt(0).mean(),
                                                          neg_count=lambda s: s.lt(0).mean()).astype(float)
        locus_pos_neg_count_table = locus_pos_neg_count_table.rename(columns={"pos_count": "pos_" + new_coef_col,
                                                                              "neg_count": "neg_" + new_coef_col})
        dataframes_list.append(locus_pos_neg_count_table)
        print(locus_pos_neg_count_table)
    # merge all dataframes
    df_merged = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='inner'),
                       dataframes_list)
    # sort the columns order
    df_merged = df_merged.reindex(sorted(df_merged.columns), axis=1)
    return df_merged

def bar_plot(df):
    df["o"] = [0] * df.shape[0]
    df = df.reindex(sorted(df.columns), axis=1)

    df.plot(kind='bar', figsize=(10, 4), legend=None)
    ax = plt.gca()
    pos = []
    for bar in ax.patches:
        pos.append(bar.get_x()+bar.get_width()/2.)

    ax.set_xticks(pos, minor=True)
    lab = []
    for i in range(len(pos)):
        l = df.columns.values[i//len(df.index.values)]
        lab.append(l)

    ax.set_xticklabels(lab, minor=True, size=7)
    ax.tick_params(axis='x', which='major', pad=95, size=0)
    plt.setp(ax.get_xticklabels(), rotation=0)
    plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)

    # remove label from legend
    label_to_remove = 'o'
    h, l = ax.get_legend_handles_labels()
    idx_keep = [k[0] for k in enumerate(l) if l[k[0]] != label_to_remove]
    handles = []
    labels = []
    for i in idx_keep:
        handles.append(h[i])
        labels.append(l[i])
    ax.legend(handles, labels, loc='upper left')


if __name__ == "__main__":
    # https://stackoverflow.com/questions/25386870/pandas-plotting-with-multi-index


    # coefs_file = os.path.join("..","AstmaResults31.01.21", "astma_alleles", "blacken_data",
    #                           "heterzygots_astma_alleles_coefs.csv")
    # pvalues_file = os.path.join("..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
    #                             "heterzygots_astma_alleles_pvalues.csv")
    # save_file_name = "mean_of_associations_asthma_alleles"

    # coefs_file = os.path.join("..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
    #                           "heterzygots_allergic_astma_coefs.csv")
    # pvalues_file = os.path.join( "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
    #                             "heterzygots_allergic_astma_pvalues.csv")
    # save_file_name = "mean_of_associations_allergic_asthma"


    # coefs_file = os.path.join("..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                           "heterzygots_astma_severity_alleles_mild_vs_severe_coefs.csv")
    # pvalues_file = os.path.join("..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                             "heterzygots_astma_severity_alleles_mild_vs_severe_pvalues.csv")
    # save_file_name = "mean_of_associations_asthma_severity"


    coefs_file = os.path.join("..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "blacken_data",
                              "heterzygots_normal_vs_overweight_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "blacken_data",
                                "heterzygots_normal_vs_overweight_astma_alleles_pvalues.csv")
    save_file_name = "mean_of_associations_asthma_bmi"

    df = create_amount_of_pos_neg_alleles_table(coefs_file, pvalues_file)
    bar_plot(df)
    plt.tight_layout()
    plt.savefig(f"{save_file_name}.pdf")
    plt.show()
