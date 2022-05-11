import os

import pandas as pd
from matplotlib import pyplot as plt

def split_df_to_all_and_ashkenazim_two_cols(coefs_df, row):
    columns = coefs_df.columns
    type_dict_coefs = {"all": {}, "ashkenazim":{}}
    for col in columns:
        if "all" in col:
            type = "all"
        else:
            type = "ashkenazim"
        xlabel = col.replace("_", "").replace("coefs", "").replace(type, "")
        type_dict_coefs[type][xlabel] = coefs_df.loc[row][col]
    print(type_dict_coefs)
    return type_dict_coefs

def plot_homozygous(coefs_df, row, **kwargs):
    type_dict_coefs = split_df_to_all_and_ashkenazim_two_cols(coefs_df, row)
    result_df = pd.DataFrame.from_dict(type_dict_coefs, orient='index').T
    result_df.sort_index(inplace=True)
    ax = result_df.plot.bar(rot=0, color=kwargs["colors"])
    plt.ylabel("Coefficient = log(OR)")
    plt.title(row)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
    # plt.savefig(row + "_" + kwargs["save_file_name"] + ".jpeg")
    plt.show()


if __name__ == "__main__":
    # Never been run
    coefs_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
                              "homozygots_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
                                "homozygots_astma_alleles_pvalues.csv")
    kwargs = {"colors": ['purple', 'red'], "save_file_name": "homozygous_asthma_alleles"}
    get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
