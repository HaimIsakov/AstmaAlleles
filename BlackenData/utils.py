import pandas as pd
from functools import reduce

external_effects = ["const", "MIN", "Age_BMI", "Birth_year", "Year_BMI", "dapar_3gr", "Educ_GE11YN", "Israeli",
                    "Eshkol_3gr"]


def heterozygote_union(files_list, save_file_name, coef_or_pvalue="coefs"):
    dataframes_list = []
    for file in files_list:
        print(file)
        cur_df = pd.read_excel(file, index_col=0)
        type = file.split("/")[-1].split("_")[0]
        if "fat" in file or "skin" in file or "skinny" in file:
            if set(list(cur_df.columns)) == {0}:
                if "fat" in file:
                    print("fat")
                    cur_df.rename(columns={0: f"{type}_fat_{coef_or_pvalue}"}, inplace=True)
                if "skin" in file or "skinny" in file:
                    print("skinny")
                    cur_df.rename(columns={0: f"{type}_skinny_{coef_or_pvalue}"}, inplace=True)
        else:
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
    df_merged.to_csv(save_file_name + "_" + coef_or_pvalue + ".csv")


def homozygote_union(files_list, save_file_name, coef_or_pvalue="coefs"):
    dataframes_list = []
    for file in files_list:
        columns_dict = {}
        print(file)
        type = file.split("/")[-1].split("_")[0]
        cur_df = pd.read_excel(file, index_col=0)
        cur_df.rename(index={"has_allele": 'Homozygous'}, inplace=True)
        if "fat" in file or "skin" in file or "skinny" in file:
            for col in list(cur_df.columns):
                columns_dict[col] = col + "_" + type
                if "fat" in file:
                    print("fat")
                    columns_dict[col] = columns_dict[col] + "_" + "fat" + "_" + coef_or_pvalue
                if "skin" in file or "skinny" in file:
                    print("skinny")
                    columns_dict[col] = columns_dict[col] + "_" + "skinny" + "_" + coef_or_pvalue
        else:
            for col in list(cur_df.columns):
                columns_dict[col] = col + "_" + type + "_" + coef_or_pvalue
        cur_df.rename(columns=columns_dict, inplace=True)
        dataframes_list.append(cur_df)
    df_merged = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='inner'),
                       dataframes_list)
    df_merged.to_csv(save_file_name + "_" + coef_or_pvalue + ".csv")
