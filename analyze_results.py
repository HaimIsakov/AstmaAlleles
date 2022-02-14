import os

import numpy as np
import pandas as pd

external_effects = ["const", "MIN", "Age_BMI", "Birth_year", "Year_BMI", "dapar_3gr", "Educ_GE11YN", "Israeli",
                    "Eshkol_3gr"]


def find_significant(df, col_name, alpha=0.05):
    print(col_name)
    df_no_external_effects = df.drop(external_effects)
    significant_alleles = df_no_external_effects[df_no_external_effects[col_name] <= alpha].index
    print(f"Number of significant alleles {len(significant_alleles)}")
    return significant_alleles


def find_significant2(df, col_name, alpha=0.05, drop=True):
    print(col_name)
    if drop:
        df = df.drop(external_effects)
    bool_significant_alleles = df[col_name] <= alpha
    return bool_significant_alleles


def all_ashkenazim_comparison(file_name, col_name1, col_name2):
    df = pd.read_csv(file_name, index_col=0)
    all_significant_alleles = find_significant(df, col_name1, alpha=0.05)
    ashkenazim_significant_alleles = find_significant(df, col_name2, alpha=0.05)
    intersec_alleles = set(all_significant_alleles) & set(ashkenazim_significant_alleles)
    print("Number of intersection of alleles ", len(intersec_alleles))
    return intersec_alleles


def union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05):
    result_df_name = "significant_" + pvalues_file.split("/")[-1].replace("_pvalues", "")
    pvalues_df = pd.read_csv(pvalues_file, index_col=0)
    coefs_df = pd.read_csv(coefs_file, index_col=0)
    columns = list(pvalues_df.columns)
    all_dict = {}
    for col in columns:
        type = col.replace("_pvalues", "")
        coefs_col = col.replace("pvalues", "coefs")
        significant_alleles = find_significant(pvalues_df, col, alpha=alpha)
        significant_coefs = coefs_df[coefs_col].loc[significant_alleles]
        significant_pvalues = pvalues_df[col].loc[significant_alleles]
        for allele in significant_alleles:
            col_name1 = type + "_pvalues"
            col_name2 = type + "_coefs"
            if allele not in all_dict:
                all_dict[allele] = {}
            all_dict[allele][col_name1] = significant_pvalues.loc[allele]
            all_dict[allele][col_name2] = significant_coefs.loc[allele]
    result_df = pd.DataFrame.from_dict(all_dict, orient='index')
    result_df.sort_index(inplace=True)
    sum_cols = result_df.count(axis=0)
    sum_cols = [int(sum_cols.loc[col]) for col in list(result_df.columns)]
    result_df.loc["count"] = sum_cols
    result_df.to_csv(result_df_name)
    return result_df


if __name__ == "__main__":
    # file_name = "BlackenData/astma_alleles/heterzygots_astma_alleles_pvalues.csv"
    # col_name1 = "all_pvalues"
    # col_name2 = "ashkenazim_pvalues"
    # intersec_alleles = all_ashkenazim_comparison(file_name, col_name1, col_name2)

    coefs_file = os.path.join("BlackenData", "astma_alleles", "heterzygots_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("BlackenData", "astma_alleles", "heterzygots_astma_alleles_pvalues.csv")
    result_df = union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05)
    coefs_file = os.path.join("BlackenData", "astma_alleles", "homozygots_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("BlackenData", "astma_alleles", "homozygots_astma_alleles_pvalues.csv")
    result_df = union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05)

    coefs_file = os.path.join("BlackenData", "allergic_astma", "heterzygots_allergic_astma_coefs.csv")
    pvalues_file = os.path.join("BlackenData", "allergic_astma", "heterzygots_allergic_astma_pvalues.csv")
    result_df = union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05)
    coefs_file = os.path.join("BlackenData", "allergic_astma", "homozygots_allergic_astma_coefs.csv")
    pvalues_file = os.path.join("BlackenData", "allergic_astma", "homozygots_allergic_astma_pvalues.csv")
    result_df = union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05)

    coefs_file = os.path.join("BlackenData", "astma_fat_skinny", "heterzygots_fat_skinny_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("BlackenData", "astma_fat_skinny", "heterzygots_fat_skinny_astma_alleles_pvalues.csv")
    result_df = union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05)
    coefs_file = os.path.join("BlackenData", "astma_fat_skinny", "homozygots_fat_skinny_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("BlackenData", "astma_fat_skinny", "homozygots_fat_skinny_astma_alleles_pvalues.csv")
    result_df = union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05)

    coefs_file = os.path.join("BlackenData", "astma_severity", "heterzygots_astma_severity_alleles_easy_vs_hard_coefs.csv")
    pvalues_file = os.path.join("BlackenData", "astma_severity", "heterzygots_astma_severity_alleles_easy_vs_hard_pvalues.csv")
    result_df = union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05)
    coefs_file = os.path.join("BlackenData", "astma_severity", "homozygots_astma_severity_alleles_easy_vs_hard_coefs.csv")
    pvalues_file = os.path.join("BlackenData", "astma_severity", "homozygots_astma_severity_alleles_easy_vs_hard_pvalues.csv")
    result_df = union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05)
