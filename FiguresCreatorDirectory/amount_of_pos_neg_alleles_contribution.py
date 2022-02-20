import os.path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def create_amount_of_pos_neg_alleles_table(files_list):
    for file in files_list:
        print(file)
        cur_df = pd.read_csv(file, index_col=0)
        cur_df.drop(["count"], inplace=True, axis=0)
        cur_df_coefs_cols = [col for col in list(cur_df.columns) if col.split("_")[-1] == "coefs"]
        prefixes = ["A", "B", "C", "DRB1", "DQB1"] # For each locus
        grouper = [next(p for p in prefixes if p == c.split("*")[0]) for c in cur_df.index]
        for coef_col in cur_df_coefs_cols:
            print(coef_col)
            counts_grouped_df = cur_df.groupby(grouper, axis=0)[coef_col]
            locus_pos_neg_count_table = counts_grouped_df.agg(pos_count=lambda s: s.gt(0).sum(),
                                                              neg_count=lambda s: s.lt(0).sum()).astype(int)
            print(locus_pos_neg_count_table)


if __name__ == "__main__":
    # df = pd.DataFrame(np.random.rand(6, 4),
    #                   index=['one', 'two', 'three', 'four', 'five', 'six'],
    #                   columns=pd.Index(['A', 'B', 'C', 'D'],
    #                                    name='Genus')).round(2)
    #
    # df.plot(kind='bar', figsize=(10, 4))
    #
    # ax = plt.gca()
    # pos = []
    # for bar in ax.patches:
    #     pos.append(bar.get_x() + bar.get_width() / 2.)
    #
    # ax.set_xticks(pos, minor=True)
    # lab = []
    # for i in range(len(pos)):
    #     l = df.columns.values[i // len(df.index.values)]
    #     lab.append(l)
    #
    # ax.set_xticklabels(lab, minor=True)
    # ax.tick_params(axis='x', which='major', pad=15, size=0)
    # plt.setp(ax.get_xticklabels(), rotation=0)
    #
    # plt.show()

    # https://stackoverflow.com/questions/25386870/pandas-plotting-with-multi-index

    files_list = [os.path.join("..", "AstmaResults31.01.21", "astma_alleles", "significant",
                               "significant_heterzygots_astma_alleles.csv"),
                  os.path.join("..", "AstmaResults31.01.21", "astma_allergic", "significant",
                               "significant_heterzygots_allergic_astma.csv"),
                  os.path.join("..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "significant",
                               "significant_heterzygots_normal_vs_overweight_astma_alleles.csv")]
    create_amount_of_pos_neg_alleles_table(files_list)
