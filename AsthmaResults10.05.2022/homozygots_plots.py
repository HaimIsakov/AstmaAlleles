import os

import pandas as pd
from matplotlib import pyplot as plt

external_effects = ["const", "MIN", "Age_BMI", "Birth_year", "dapar_3gr", "Educ_GE11YN", "Israeli", "Eshkol_3gr"]

def split_df_to_normal_and_ashkenazim_two_cols(coefs_df, row):
    columns = coefs_df.columns
    type_dict_coefs = {"all": {}, "ashkenazim":{}}
    for col in columns:
        if "all" in col:
            type = "all"
        else:
            type = "ashkenazim"
        xlabel = col.replace(type, "").replace("_", "").replace("coef", "")
        type_dict_coefs[type][xlabel] = coefs_df.loc[row][col]
    print(type_dict_coefs)
    return type_dict_coefs

def split_df_to_normal_and_obese_two_cols(coefs_df, row):
    columns = coefs_df.columns
    type_dict_coefs = {"normal": {}, "overweight":{}}
    for col in columns:
        if "normal" in col:
            type = "normal"
        else:
            type = "overweight"
        xlabel = col.replace(type, "").replace("coef", "")[:-2]
        type_dict_coefs[type][xlabel] = coefs_df.loc[row][col]
    print(type_dict_coefs)
    return type_dict_coefs

def plot_homozygous(coefs_df, row, **kwargs):
    type_dict_coefs = split_df_to_normal_and_ashkenazim_two_cols(coefs_df, row)
    result_df = pd.DataFrame.from_dict(type_dict_coefs, orient='index').T
    result_df.sort_index(inplace=True)
    ax = result_df.plot.bar(rot=0, color=kwargs["colors"])
    plt.ylabel("Coefficient = log(OR)")
    plt.title(row)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
    # plt.savefig(row + "_" + kwargs["save_file_name"] + ".jpeg")
    plt.show()

def bar_plot(df):
    # df["am"] = [0] * df.shape[0]
    # df = df.reindex(sorted(df.columns), axis=1)

    df.plot(kind='bar', figsize=(10, 4), legend=None, edgecolor='black', width=0.5)
    ax = plt.gca()
    pos = []
    for bar in ax.patches:
        pos.append(bar.get_x()+bar.get_width()/2.)

    ax.set_xticks(pos, minor=True)
    lab = []
    for i in range(len(pos)):
        l = df.columns.values[i//len(df.index.values)]
        lab.append(l)

    ax.set_xticklabels(lab, minor=True, size=7)
    ax.tick_params(axis='x', which='major', pad=95, size=0)
    plt.setp(ax.get_xticklabels(), rotation=0)
    plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)
    plt.ylabel("log(OR)")
    # remove label from legend
    label_to_remove = ''
    h, l = ax.get_legend_handles_labels()
    idx_keep = [k[0] for k in enumerate(l) if l[k[0]] != label_to_remove]
    handles = []
    labels = []
    for i in idx_keep:
        handles.append(h[i])
        labels.append(l[i])
    ax.legend(handles, labels, loc='upper left')

def prepare_homozygot_file_to_plot(file, alpha=0.05):
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
    return df

def plot_external_effect(coefs_df, row, **kwargs):
    type_dict_coefs = split_df_to_normal_and_obese_two_cols(coefs_df, row)
    result_df = pd.DataFrame.from_dict(type_dict_coefs, orient='index').T
    result_df.sort_index(inplace=True)
    ax = result_df.plot.bar(rot=0, color=kwargs["colors"])
    plt.xticks(rotation=45)
    plt.ylabel("Coefficient = log(OR)")
    plt.title(row)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
    plt.tight_layout()

    plt.savefig(row + "_" + kwargs["save_file_name"] + ".jpeg")
    plt.show()

if __name__ == "__main__":
    # Never been run

    # file = "interaction_asthma_homozygots.csv"
    # save_file = "bar_plot_homozygots_interaction_model.pdf"
    # df = pd.read_csv(file, index_col=0)
    # non_inter_cols = [column for column in list(df.index) if "inter" not in column]
    # # df = df.loc[non_inter_cols]
    # df.drop(external_effects, inplace=True)
    # possible_cols = list(set([col.replace("A_", "").replace("B_", "").replace("C_", "").replace("DRB1_", "").replace("DQB1_", "") for col in list(df.columns) ]))
    #
    # # possible_cols = list(set([col.replace("BW4_", "").replace("BW6_", "").replace("C1_", "") for col in list(df.columns) ]))
    #
    # dict = {}
    # feature_list = ["A", "B", "C", "DRB1", "DQB1"]
    # # feature_list = ["BW4", "BW6", "C1"]
    # for x in feature_list:
    #     for col in possible_cols:
    #         if x not in dict:
    #             dict[x] = {}
    #         cur_col = x + "_" + col
    #         dict[x][col] = df.loc[x][cur_col]
    # for x in feature_list:
    #     for col in possible_cols:
    #         y = x + "_inter_BMI"
    #         if y not in dict:
    #             dict[y] = {}
    #         cur_col = x + "_" + col
    #         dict[y][col] = df.loc[y][cur_col]
    #
    # final_df = pd.DataFrame.from_dict(dict, orient="index")
    # pvalue_columns = [column for column in list(final_df.columns) if "pvalue" in column]
    # # zero the coefficients that their pvalue is greater than 0.05
    # for col in pvalue_columns:
    #     coefs_col = col.replace("pvalue", "coef")
    #     # bool_significant_alleles = find_significant2(pvalues_df, col, alpha=alpha)
    #     final_df[coefs_col] = final_df[coefs_col].where(final_df[col] <= 0.05, 0)
    # # drop the pvalues columns
    # final_df.drop(pvalue_columns, inplace=True, axis=1)
    # final_df.columns = final_df.columns.str.replace("_coef", '')
    # final_df.sort_index(inplace=True)
    # bar_plot(final_df)
    # plt.tight_layout()
    # plt.savefig(save_file)
    # plt.show()



    # file = "asthma_homozygots_obese_and_not.csv"
    # df = prepare_homozygot_file_to_plot(file, alpha=0.05)
    # kwargs = {"colors": ['purple', 'red'], "save_file_name": "new_homozygous_asthma_alleles"}
    #
    # plot_external_effect(df, "Homozygous", **kwargs)


    file = "asthma_homozygots_obese_and_not.csv"
    df = prepare_homozygot_file_to_plot(file, alpha=0.05)
    kwargs = {"colors": ['purple', 'red'], "save_file_name": "new_homozygous_asthma_alleles"}

    plot_external_effect(df, "Homozygous", **kwargs)

