import os

import pandas as pd
from matplotlib import pyplot as plt

from FiguresCreatorDirectory.analyze_results_with_zero_unsignificant_coefs import zero_unsignificant_coefs, \
    coefs_external_effects


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
    # plt.savefig(row + "_" + kwargs["save_file_name"] + ".jpeg")
    plt.show()


def get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs):
    coefs_df = zero_unsignificant_coefs(coefs_file, pvalues_file, alpha=0.05)
    for row in coefs_df.index:
        plot_external_effect(coefs_df, row, **kwargs)

# def get_coefs_df(coefs_file, pvalues_file, **kwargs):
#     coefs_df = zero_unsignificant_coefs(coefs_file, pvalues_file, alpha=0.05)
#     plot_bar_plot(coefs_df, **kwargs)
#
#
# def plot_bar_plot(coefs_df, **kwargs):
#     coefs_df = coefs_df.reindex(sorted(coefs_df.columns), axis=1)
#     coefs_df_cols = coefs_df.columns
#     fig, ax = plt.subplots(1, figsize=(16, 8))
#     xlabels = [label.replace("_coefs", "") for label in coefs_df_cols]
#     x_pos = xlabels
#     y = coefs_df.values[0]
#     bar_plot = plt.bar(x_pos, y, width=0.5)
#     for i in range(len(x_pos)):
#         type = xlabels[i].split("_")[-1]
#         if type == "all":
#             bar_plot[i].set_color(kwargs["color1"])
#         else:
#             bar_plot[i].set_color(kwargs["color2"])
#     rects = bar_plot
#     for rect in rects:
#         height = rect.get_height()
#         if height <= 0:
#             ax.text(rect.get_x() + rect.get_width() / 2., height - kwargs["height_minus"],
#                     f"{height : .5f}",
#                     ha='center', va='bottom')
#         else:
#             ax.text(rect.get_x() + rect.get_width() / 2., height + kwargs["height_minus"],
#                     f"{height : .5f}",
#                     ha='center', va='bottom')
#     ax.set_xticklabels(xlabels, rotation=30)
#
#     plt.ylim(kwargs["bottom_ylim"], kwargs["upper_ylim"])
#     plt.tight_layout()
#     #grid
#     ax.set_axisbelow(True)
#     ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
#     plt.savefig(kwargs["save_file_name"] + ".jpeg")
#     plt.show()


if __name__ == "__main__":
    coefs_file = os.path.join("..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
                              "homozygots_astma_alleles_coefs.csv")
    pvalues_file = os.path.join("..", "AstmaResults31.01.21", "astma_alleles", "blacken_data",
                                "homozygots_astma_alleles_pvalues.csv")
    kwargs = {"colors": ['purple', 'red'], "save_file_name": "homozygous_asthma_alleles"}
    get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)

    # coefs_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
    #                           "homozygots_allergic_astma_coefs.csv")
    # pvalues_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_allergic", "blacken_data",
    #                             "homozygots_allergic_astma_pvalues.csv")
    # kwargs = {"colors": ['darkgreen', 'lime'],
    #           "save_file_name": "homozygous_allergic_asthma"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)
    #
    # coefs_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                           "homozygots_astma_severity_alleles_mild_vs_severe_coefs.csv")
    # pvalues_file = os.path.join("..","..", "AstmaResults31.01.21", "astma_severity", "blacken_data",
    #                             "homozygots_astma_severity_alleles_mild_vs_severe_pvalues.csv")
    # kwargs = {"colors": ['blue', 'cyan'],
    #           "save_file_name": "homozygous_asthma_severity"}
    # get_external_effects_coef_df(coefs_file, pvalues_file, **kwargs)

#
# file = os.path.join("..", "AstmaResults31.01.21", "astma_alleles", "significant",
#                     "significant_homozygots_astma_alleles.csv")
# cur_df = pd.read_csv(file, index_col=0)
# cur_df.drop(["count"], inplace=True, axis=0)
# cur_df = cur_df.reindex(sorted(cur_df.columns), axis=1)
# cur_df_coefs_cols = [col for col in list(cur_df.columns) if col.split("_")[-1] == "coefs"]
# coef_cur_df = cur_df[cur_df_coefs_cols]
#
# fig, ax = plt.subplots(1, figsize=(16, 8))
# xlabels = [label.replace("_coefs", "") for label in coef_cur_df.columns]
# x_pos = xlabels
# y = coef_cur_df.values[0]
# bar_plot = plt.bar(x_pos, y, width =0.5)
# for i in range(len(x_pos)):
#     if i % 2 == 0:
#         bar_plot[i].set_color('purple')
#     else:
#         bar_plot[i].set_color('pink')
# rects = bar_plot
# for rect in rects:
#     height = rect.get_height()
#     ax.text(rect.get_x() + rect.get_width() / 2., - 0.005 + height,
#             f"{height : .3f}",
#             ha='center', va='bottom')
#
# plt.ylim(-0.12, 0)
#
# #grid
# ax.set_axisbelow(True)
# ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
# # plt.title('My Company - 2020\n', loc='left')
# plt.savefig("homozygous_asthma_alleles.jpeg")
# plt.show()
#

