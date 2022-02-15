import os

import numpy as np
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


def plot_external_effect(coefs_df, row, ax, **kwargs):
    type_dict_coefs = split_df_to_all_and_ashkenazim_two_cols(coefs_df, row)
    result_df = pd.DataFrame.from_dict(type_dict_coefs, orient='index').T
    result_df.sort_index(inplace=True)
    b = result_df.plot.bar(rot=kwargs["rot"], color=kwargs["colors"], ax=ax, legend=None)
    # plt.ylabel("Coefficient = log(OR)")
    ax.set_title(row, size=9)
    b.set_axisbelow(True)
    b.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)


def plot_external_effect_homozygot(coefs_df, row, ax, **kwargs):
    type_dict_coefs = split_df_to_all_and_ashkenazim_two_cols(coefs_df, row)
    result_df = pd.DataFrame.from_dict(type_dict_coefs, orient='index').T
    result_df.sort_index(inplace=True)
    if "prefixes" in kwargs:
        prefixes = kwargs["prefixes"]
        grouper = [next(p for p in prefixes if p == c[0]) for c in result_df.index]
        means_df = result_df.groupby(grouper, axis=0).mean()
        std_df = result_df.groupby(grouper, axis=0).std()
    else:
        means_df = result_df.mean(axis=0)
        std_df = result_df.std(axis=0)
    b = means_df.plot.bar(yerr=std_df, rot=kwargs["rot"], color=kwargs["colors"], ax=ax, legend=None)
    # plt.ylabel("Coefficient = log(OR)")
    # ax.set_ylim([-0.4, 0.4])
    ax.set_title(row, size=9)
    b.set_axisbelow(True)
    b.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)


def get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs):
    coefs_df = coefs_external_effects(coefs_file, pvalues_file, alpha=0.05)
    fig, axs = plt.subplots(2, 4, figsize=(20,15))
    ind = [(i, j) for i in range(2) for j in range(4)]
    for p, row in enumerate(coefs_df.index):
        if "homozygots" in coefs_file:
            plot_external_effect_homozygot(coefs_df, row, axs[ind[p]], **kwargs)
        if "heterzygots" in coefs_file:
            plot_external_effect(coefs_df, row, axs[ind[p]], **kwargs)
    handles, labels = axs[ind[0]].get_legend_handles_labels()
    if len(labels) > 1:
        fig.legend(handles, labels)

    plt.setp(axs, ylim=[-0.5,0.5])
    fig.suptitle(kwargs["fig_title"])
    fig.tight_layout(pad=1)
    plt.savefig(kwargs["save_file_name"] + ".jpeg", bbox_inches="tight", pad_inches=0.1)
    plt.show()


if __name__ == "__main__":
    coefs_file = os.path.join("..", "..","AstmaResults31.01.21", "astma_alleles", "blacken_data",
                              "homozygots_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
                                "homozygots_astma_alleles_pvalues.csv")
    kwargs = {"colors": ['purple', 'red'], "rot" : 45, "fig_title": "Asthma&Alleles - Homozygous",
              "save_file_name": "other_homozygous_astma_alleles"}
    get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
    #
    coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
                              "homozygots_allergic_astma_coefs.csv")
    pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
                                "homozygots_allergic_astma_pvalues.csv")
    kwargs = {"colors": ['darkgreen', 'lime'], "rot" : 0, "fig_title": "Allergic Asthma - Homozygous",
              "prefixes": ["1", "2"],
              "save_file_name": "other_homozygous_allergic_asthma"}
    get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)

    # coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                           "homozygots_astma_severity_alleles_mild_vs_severe_coefs.csv")
    # pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                             "homozygots_astma_severity_alleles_mild_vs_severe_pvalues.csv")
    # kwargs = {"colors": ['blue', 'cyan'], "rot" : 0, "fig_title": "Asthma Severity - Homozygous",
    #           "prefixes": ["1", "2"],
    #           "save_file_name": "other_homozygous_asthma_severity"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
    #
    #
    # coefs_file = os.path.join("..", "..","AstmaResults31.01.21", "astma_alleles", "blacken_data",
    #                           "heterzygots_astma_alleles_coefs.csv")
    # pvalues_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
    #                             "heterzygots_astma_alleles_pvalues.csv")
    # kwargs = {"colors": ['purple', 'red'], "rot" : 45, "fig_title": "Asthma&Alleles - Heterozygous",
    #           "save_file_name": "other_heterzygots_astma_alleles"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
    #
    # coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
    #                           "heterzygots_allergic_astma_coefs.csv")
    # pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
    #                             "heterzygots_allergic_astma_pvalues.csv")
    # kwargs = {"colors": ['darkgreen', 'lime'],"rot" : 0,"fig_title": "Allergic Asthma - Heterozygous",
    #           "save_file_name": "other_heterzygots_allergic_asthma"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
    # #
    # coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                           "heterzygots_astma_severity_alleles_mild_vs_severe_coefs.csv")
    # pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                             "heterzygots_astma_severity_alleles_mild_vs_severe_pvalues.csv")
    # kwargs = {"colors": ['blue', 'cyan'],"rot" : 0,"fig_title": "Asthma Severity- Heterozygous",
    #           "save_file_name": "other_heterzygots_asthma_severity"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
    #
    # coefs_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "blacken_data",
    #                           "heterzygots_normal_vs_overweight_astma_alleles_coefs.csv")
    # pvalues_file = os.path.join("..", "..", "AstmaResults31.01.21", "astma_normal_vs_overweight", "blacken_data",
    #                             "heterzygots_normal_vs_overweight_astma_alleles_pvalues.csv")
    # kwargs = {"colors": ['darkorange', 'gold'],"rot" : 45, "fig_title": "Asthma BMI- Heterozygous",
    #           "save_file_name": "other_heterzygots_astma_normal_vs_overweight"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
