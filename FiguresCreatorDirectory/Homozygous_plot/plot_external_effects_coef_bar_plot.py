import os

import pandas as pd
from matplotlib import pyplot as plt

from FiguresCreatorDirectory.analyze_results_with_zero_unsignificant_coefs import coefs_external_effects, \
    zero_unsignificant_coefs


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


def plot_external_effect(coefs_df, row, **kwargs):
    type_dict_coefs = split_df_to_all_and_ashkenazim_two_cols(coefs_df, row)
    result_df = pd.DataFrame.from_dict(type_dict_coefs, orient='index').T
    result_df.sort_index(inplace=True)
    ax = result_df.plot.bar(rot=0, color=kwargs["colors"])
    plt.ylabel("Coefficient = log(OR)")
    plt.title(row)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
    plt.savefig(row + "_" + kwargs["save_file_name"] + ".jpeg")
    plt.show()


def get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs):
    coefs_df = coefs_external_effects(coefs_file, pvalues_file, alpha=0.05)
    for row in coefs_df.index:
        plot_external_effect(coefs_df, row, **kwargs)


if __name__ == "__main__":
    # coefs_file = os.path.join("..", "..","AstmaResults31.01.21", "astma_alleles", "blacken_data",
    #                           "homozygots_astma_alleles_coefs.csv")
    # pvalues_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
    #                             "homozygots_astma_alleles_pvalues.csv")
    # kwargs = {"colors": ['purple', 'red'],
    #           "save_file_name": "homozygous_astma_alleles"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
    #
    # coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
    #                           "homozygots_allergic_astma_coefs.csv")
    # pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
    #                             "homozygots_allergic_astma_pvalues.csv")
    # kwargs = {"colors": ['darkgreen', 'lime'],
    #           "save_file_name": "homozygous_allergic_asthma"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
    #
    # coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                           "homozygots_astma_severity_alleles_mild_vs_severe_coefs.csv")
    # pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                             "homozygots_astma_severity_alleles_mild_vs_severe_pvalues.csv")
    # kwargs = {"colors": ['blue', 'cyan'],
    #           "save_file_name": "homozygous_asthma_severity"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)



    coefs_file = os.path.join("..", "..","AstmaResults31.01.21", "astma_alleles", "blacken_data",
                              "heterzygots_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
                                "heterzygots_astma_alleles_pvalues.csv")
    kwargs = {"colors": ['purple', 'red'],
              "save_file_name": "heterzygots_astma_alleles"}
    get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)

    coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
                              "heterzygots_allergic_astma_coefs.csv")
    pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
                                "heterzygots_allergic_astma_pvalues.csv")
    kwargs = {"colors": ['darkgreen', 'lime'],
              "save_file_name": "heterzygots_allergic_asthma"}
    get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)

    coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
                              "heterzygots_astma_severity_alleles_mild_vs_severe_coefs.csv")
    pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
                                "heterzygots_astma_severity_alleles_mild_vs_severe_pvalues.csv")
    kwargs = {"colors": ['blue', 'cyan'],
              "save_file_name": "heterzygots_asthma_severity"}
    get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)

    coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "blacken_data",
                              "heterzygots_normal_vs_overweight_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "blacken_data",
                                "heterzygots_normal_vs_overweight_astma_alleles_pvalues.csv")
    kwargs = {"colors": ['darkorange', 'gold'],
              "save_file_name": "heterzygots_astma_normal_vs_overweight"}
    get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
