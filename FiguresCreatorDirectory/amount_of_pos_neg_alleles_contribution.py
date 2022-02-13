import os.path

import pandas as pd


def create_amount_of_pos_neg_alleles_table(files_list):
    for file in files_list:
        print(file)
        cur_df = pd.read_csv(file, index_col=0)
        cur_df.drop(["count"], inplace=True, axis=0)
        cur_df_coefs_cols = [col for col in list(cur_df.columns) if col.split("_")[-1] == "coefs"]
        for coef_col in cur_df_coefs_cols:
            print(coef_col)
            pos_sum_cols = cur_df[cur_df[coef_col] > 0].shape[0]
            print("Number of positive alleles contribution", pos_sum_cols)
            neg_sum_cols = cur_df[cur_df[coef_col] < 0].shape[0]
            print("Number of negative alleles contribution", neg_sum_cols)


if __name__ == "__main__":
    files_list = [os.path.join("..", "AstmaResults31.01.21", "astma_Alleles", "significant",
                               "significant_heterzygots_astma_alleles.csv"),
                  os.path.join("..", "AstmaResults31.01.21", "astma_allergic", "significant",
                               "significant_heterzygots_allergic_astma.csv"),
                  os.path.join("..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "significant",
                               "significant_heterzygots_normal_vs_overweight_astma_alleles.csv")]
    create_amount_of_pos_neg_alleles_table(files_list)
