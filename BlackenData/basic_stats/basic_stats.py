import pandas as pd


def union_stats_files(file_all, file2_ashkenazim, col_name):
    df1 = pd.read_excel(file_all, index_col=0)
    df1.rename(columns={0: f"all_{col_name}"}, inplace=True)

    df2 = pd.read_excel(file2_ashkenazim, index_col=0)
    df2.rename(columns={0: f"ashkenazim_{col_name}"}, inplace=True)

    merged_df = df1.merge(df2, how='inner', left_index=True, right_index=True)
    merged_df.sort_values(by=[f"ashkenazim_{col_name}", f"all_{col_name}"], inplace=True, ascending=False)
    merged_df.to_excel("all&ashkenazim_" + file_all)


if __name__ == "__main__":
    file_all = "alleles_hist.xls"
    file2_ashkenazim = "ashkenazim_alleles_hist.xls"
    col_name = "frequency"
    union_stats_files(file_all, file2_ashkenazim, col_name)

    file_all = "code_diseases_hist.xls"
    file2_ashkenazim = "ashkenazim_code_diseases_hist.xls"
    col_name = "frequency"
    union_stats_files(file_all, file2_ashkenazim, col_name)

    file_all = "homozygots_hist.xls"
    file2_ashkenazim = "ashkenazim_homozygots_hist.xls"
    col_name = "frequency"
    union_stats_files(file_all, file2_ashkenazim, col_name)

