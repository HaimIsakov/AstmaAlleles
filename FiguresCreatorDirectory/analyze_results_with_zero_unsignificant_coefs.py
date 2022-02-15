import os

import pandas as pd

from analyze_results import find_significant2
external_effects = ["const", "MIN", "Age_BMI", "Birth_year", "Year_BMI", "dapar_3gr", "Educ_GE11YN", "Israeli",
                    "Eshkol_3gr"]


def zero_unsignificant_coefs(coefs_file, pvalues_file, alpha=0.05):
    pvalues_df = pd.read_csv(pvalues_file, index_col=0)
    coefs_df = pd.read_csv(coefs_file, index_col=0)
    coefs_df.drop(external_effects, inplace=True)

    columns = list(pvalues_df.columns)
    for col in columns:
        coefs_col = col.replace("pvalues", "coefs")
        bool_significant_alleles = find_significant2(pvalues_df, col, alpha=alpha)
        coefs_df[coefs_col] = coefs_df[coefs_col].where(bool_significant_alleles, 0)
    return coefs_df


def coefs_external_effects(coefs_file, pvalues_file, alpha=0.05):
    pvalues_df = pd.read_csv(pvalues_file, index_col=0)
    coefs_df = pd.read_csv(coefs_file, index_col=0)

    pvalues_df = pvalues_df.loc[external_effects]
    pvalues_df.drop(["const"], inplace=True)
    coefs_df = coefs_df.loc[external_effects]
    coefs_df.drop(["const"], inplace=True)

    columns = list(pvalues_df.columns)
    for col in columns:
        coefs_col = col.replace("pvalues", "coefs")
        bool_significant_alleles = find_significant2(pvalues_df, col, alpha=alpha, drop=False)
        coefs_df[coefs_col] = coefs_df[coefs_col].where(bool_significant_alleles, 0)
    return coefs_df


# if __name__ == "__main__":
#     coefs_file = os.path.join("..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
#                               "homozygots_astma_alleles_coefs.csv")
#     pvalues_file = os.path.join("..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
#                                 "homozygots_astma_alleles_pvalues.csv")
#     coefs_df = zero_unsignificant_coefs(coefs_file, pvalues_file, alpha=0.05)
