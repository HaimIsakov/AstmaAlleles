import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

external_effects = ["const", "MIN", "Age_BMI", "Birth_year", "dapar_3gr", "Educ_GE11YN", "Israeli", "Eshkol_3gr"]

def find_significant2(df, col_name, alpha=0.05, drop=True):
    print(col_name)
    if drop:
        df = df.drop(external_effects)
    bool_significant_alleles = df[col_name] <= alpha
    return bool_significant_alleles

def zero_unsignificant_coefs(file, alpha=0.05):
    df = pd.read_csv(file, index_col=0)
    df.drop(external_effects, inplace=True)

    columns = list(df.columns)
    pvalue_columns = [column for column in columns if "pvalue" in column]
    # zero the coefficients that their pvalue is greater than 0.05
    for col in pvalue_columns:
        coefs_col = col.replace("pvalue", "coef")
        # bool_significant_alleles = find_significant2(pvalues_df, col, alpha=alpha)
        df[coefs_col] = df[coefs_col].where(df[col] <= alpha, 0)
    # drop the pvalues columns
    df.drop(pvalue_columns, inplace=True, axis=1)
    # remove alleles that have never been significat (in pvalues term)
    df = df.loc[~(df == 0).all(axis=1)]
    # remvoe the coef suffix
    df.columns = df.columns.str.replace("_coef", '')
    return df

def plot_cluster_map(df, save_file_name="clustermap_alleles_models"):
    print(df.shape)
    np_mat = df.values
    # just to make the colors look more clear
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
    plt.savefig(f"{save_file_name}.pdf")
    plt.show()


if __name__ == "__main__":
    file = "asthma_alleles_obese_and_not.csv"
    df = zero_unsignificant_coefs(file, alpha=0.05)
    save_file_name = "cluster_map_asthma_alleles"
    plot_cluster_map(df, save_file_name=save_file_name)

    file = "allergic_asthma_obese_and_not.csv"
    df = zero_unsignificant_coefs(file, alpha=0.05)
    save_file_name = "cluster_map_allergic_asthma"
    plot_cluster_map(df, save_file_name=save_file_name)

    file = "asthma_severity_obese_and_not.csv"
    df = zero_unsignificant_coefs(file, alpha=0.05)
    save_file_name = "cluster_map_asthma_severity"
    plot_cluster_map(df, save_file_name=save_file_name)
