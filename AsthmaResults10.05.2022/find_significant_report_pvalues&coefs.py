import pandas as pd
import os
from functools import reduce

external_effects = ["const", "MIN", "Age_BMI", "Birth_year", "dapar_3gr", "Educ_GE11YN", "Israeli", "Eshkol_3gr"]
def homozygote_union(files_list, save_file_name):
    dataframes_list = []
    for file in files_list:
        columns_dict = {}
        print(file)
        type = "ashkenazim" if "ashkenazim" in file else "all_soldiers"
        coef_or_pvalue = "coef" if "coef" in file else "pvalue"
        if "overweight" in file:
            fat_type = "overweight"
        elif "normal" in file:
            fat_type = "normal"
        else:
            fat_type = ""
        if fat_type != "":
            type = type + "_" + fat_type

        cur_df = pd.read_excel(file, index_col=0)
        cur_df.rename(index={"has_allele": 'Homozygous'}, inplace=True)
        for col in list(cur_df.columns):
            columns_dict[col] = col + "_" + type + "_" + coef_or_pvalue
        cur_df.rename(columns=columns_dict, inplace=True)
        dataframes_list.append(cur_df)
    df_merged = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='inner'),
                       dataframes_list)
    df_merged.to_csv(save_file_name + ".csv")

def heterozygote_union(files_list, save_file_name):
    dataframes_list = []
    for file in files_list:
        print(file)
        cur_df = pd.read_excel(file, index_col=0)
        type = "ashkenazim" if "ashkenazim" in file else "all_soldiers"
        if "overweight" in file:
            fat_type = "overweight"
        elif "normal" in file:
            fat_type = "normal"
        else:
            fat_type = ""
        if fat_type != "":
            type = type + "_" + fat_type
        coef_or_pvalue = "coef" if "coef" in file else "pvalue"
        if set(list(cur_df.columns)) == {0, 1}:
            cur_df.rename(columns={0: f"1_{type}_{coef_or_pvalue}", 1: f"2_{type}_{coef_or_pvalue}"}, inplace=True)
        if set(list(cur_df.columns)) == {0}:
            cur_df.rename(columns={0: f"{type}_{coef_or_pvalue}"}, inplace=True)
        dataframes_list.append(cur_df)
    df_merged = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='inner'),
                       dataframes_list)
    df_external = df_merged.loc[external_effects]
    df_merged.drop(external_effects, inplace=True)
    df_merged.sort_index(inplace=True)
    df_merged = pd.concat([df_merged, df_external])
    df_merged.to_csv(save_file_name + ".csv")


def find_significant(df, col_name, alpha=0.05):
    print(col_name)
    df_no_external_effects = df.drop(external_effects)
    significant_alleles = df_no_external_effects[df_no_external_effects[col_name] <= alpha].index
    print(f"Number of significant alleles {len(significant_alleles)}")
    return significant_alleles


def union_all_columns_according_to_significant_alleles(coefs_file, pvalues_file, alpha=0.05):
    result_df_name = "significant_" + pvalues_file.split("/")[-1].replace("_pvalues", "")
    pvalues_df = pd.read_excel(pvalues_file, index_col=0)
    coefs_df = pd.read_excel(coefs_file, index_col=0)
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


def union_interaction_files():
    files_list = [os.path.join("interaction", "alleles", f"equation4_coefs_together.xlsx"),
                  os.path.join("interaction", "alleles", f"equation4_pvalues_together.xlsx"),
                  os.path.join("interaction", "alleles", f"equation4_ashkenazim_coefs_together.xlsx"),
                  os.path.join("interaction", "alleles", f"equation4_ashkenazim_pvalues_together.xlsx")]
    save_file_name = "interaction_asthma_alleles"
    heterozygote_union(files_list, save_file_name)

    files_list = [os.path.join("interaction", "homozygous", f"equation4_all_soldiers_homozygous_coefs_seperate.xlsx"),
                  os.path.join("interaction", "homozygous", f"equation4_all_soldiers_homozygous_pvalues_seperate.xlsx"),
                  os.path.join("interaction", "homozygous", f"equation4_ashkenazim_homozygous_coefs_seperate.xlsx"),
                  os.path.join("interaction", "homozygous", f"equation4_ashkenazim_homozygous_pvalues_seperate.xlsx")]
    save_file_name = "interaction_asthma_homozygots"
    homozygote_union(files_list, save_file_name)

    files_list = [os.path.join("interaction", "kirs", f"equation4_all_soldiers_kirs_coefs_seperate.xlsx"),
                  os.path.join("interaction", "kirs", f"equation4_all_soldiers_kirs_pvalues_seperate.xlsx"),
                  os.path.join("interaction", "kirs", f"equation4_ashkenazim_kirs_coefs_seperate.xlsx"),
                  os.path.join("interaction", "kirs", f"equation4_ashkenazim_kirs_pvalues_seperate.xlsx")]
    save_file_name = "interaction_asthma_kirs"
    homozygote_union(files_list, save_file_name)

def union_seperate_obese_and_not_files():
    files_list = [os.path.join("seperate_obese_and_normal", "allergic_asthma", f"all_soldiers_binary_asthma_allergic_normal_coefs_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "allergic_asthma", f"all_soldiers_binary_asthma_allergic_normal_pvalues_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "allergic_asthma", f"all_soldiers_binary_asthma_allergic_overweight_coefs_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "allergic_asthma", f"all_soldiers_binary_asthma_allergic_overweight_pvalues_together.xlsx")]
    save_file_name = "allergic_asthma_obese_and_not"
    heterozygote_union(files_list, save_file_name)

    files_list = [os.path.join("seperate_obese_and_normal", "asthma_severity", f"all_soldiers_binary_asthma_severity_normal_coefs_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma_severity", f"all_soldiers_binary_asthma_severity_normal_pvalues_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma_severity", f"all_soldiers_binary_asthma_severity_overweight_coefs_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma_severity", f"all_soldiers_binary_asthma_severity_overweight_pvalues_together.xlsx")]
    save_file_name = "asthma_severity_obese_and_not"
    heterozygote_union(files_list, save_file_name)

    files_list = [os.path.join("seperate_obese_and_normal", "asthma", "alleles", f"all_soldiers_asthma_alleles_normal_coefs_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "alleles", f"all_soldiers_asthma_alleles_normal_pvalues_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "alleles", f"all_soldiers_asthma_alleles_overweight_coefs_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "alleles", f"all_soldiers_asthma_alleles_overweight_pvalues_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "alleles", f"ashkenazim_asthma_alleles_normal_coefs_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "alleles", f"ashkenazim_asthma_alleles_normal_pvalues_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "alleles", f"ashkenazim_asthma_alleles_overweight_coefs_together.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "alleles", f"ashkenazim_asthma_alleles_overweight_pvalues_together.xlsx")]
    save_file_name = "asthma_alleles_obese_and_not"
    heterozygote_union(files_list, save_file_name)

    files_list = [os.path.join("seperate_obese_and_normal", "asthma", "haplotypes", f"all_soldiers_asthma_haplotypes_normal_coefs_seperate.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "haplotypes", f"all_soldiers_asthma_haplotypes_normal_pvalues_seperate.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "haplotypes", f"all_soldiers_asthma_haplotypes_overweight_coefs_seperate.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "haplotypes", f"all_soldiers_asthma_haplotypes_overweight_pvalues_seperate.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "haplotypes", f"ashkenazim_asthma_haplotypes_normal_coefs_seperate.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "haplotypes", f"ashkenazim_asthma_haplotypes_normal_pvalues_seperate.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "haplotypes", f"ashkenazim_asthma_haplotypes_overweight_coefs_seperate.xlsx"),
                  os.path.join("seperate_obese_and_normal", "asthma", "haplotypes", f"ashkenazim_asthma_haplotypes_overweight_pvalues_seperate.xlsx")]
    save_file_name = "asthma_haplotypes_obese_and_not"
    homozygote_union(files_list, save_file_name)


if __name__ == "__main__":
    # union_interaction_files()
    union_seperate_obese_and_not_files()
