import pandas as pd
from matplotlib import pyplot as plt

external_effects = ["MIN", "Age_BMI", "Birth_year", "dapar_3gr", "Educ_GE11YN", "Israeli", "Eshkol_3gr"]

def split_df_to_all_and_ashkenazim_two_cols(coefs_df, row):
    columns = coefs_df.columns
    type_dict_coefs = {"all_soldiers": {}, "ashkenazim":{}}
    for col in columns:
        if "all_soldiers" in col:
            type = "all_soldiers"
        else:
            type = "ashkenazim"
        xlabel = col.replace(type, "").replace("_", "").replace("coefs", "")
        type_dict_coefs[type][xlabel] = coefs_df.loc[row][col]
    print(type_dict_coefs)
    return type_dict_coefs

def coefs_external_effects(file, alpha=0.05):

    df = pd.read_csv(file, index_col=0)
    df = df.loc[external_effects]

    columns = list(df.columns)
    pvalue_columns = [column for column in columns if "pvalue" in column]
    # zero the coefficients that their pvalue is greater than 0.05
    for col in pvalue_columns:
        coefs_col = col.replace("pvalue", "coef")
        # bool_significant_alleles = find_significant2(pvalues_df, col, alpha=alpha)
        df[coefs_col] = df[coefs_col].where(df[col] <= alpha, 0)
    # drop the pvalues columns
    df.drop(pvalue_columns, inplace=True, axis=1)
    # remvoe the coef suffix
    df.columns = df.columns.str.replace("_coef", '')
    return df

def plot_external_effect(coefs_df, row, ax, **kwargs):
    type_dict_coefs = split_df_to_all_and_ashkenazim_two_cols(coefs_df, row)
    result_df = pd.DataFrame.from_dict(type_dict_coefs, orient='index').T
    result_df.sort_index(inplace=True)
    b = result_df.plot.bar(rot=kwargs["rot"], color=kwargs["colors"], ax=ax, legend=None)
    # plt.ylabel("Coefficient = log(OR)")
    ax.tick_params(axis='both', which='major', labelsize=15)
    ax.tick_params(axis='both', which='minor', labelsize=15)

    ax.set_title(row, size=16)
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
    ax.set_title(row, size=16)
    ax.tick_params(axis='both', which='major', labelsize=15)
    ax.tick_params(axis='both', which='minor', labelsize=15)
    b.set_axisbelow(True)
    b.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)

def get_external_effects_coef_df(file, heterzygot=True, **kwargs):
    coefs_df = coefs_external_effects(file, alpha=0.05)
    fig, axs = plt.subplots(2, 4, figsize=(20,15))
    ind = [(i, j) for i in range(2) for j in range(4)]
    for p, row in enumerate(coefs_df.index):
        # if "homozygots" in file:
        #     plot_external_effect_homozygot(coefs_df, row, axs[ind[p]], **kwargs)
        # if "heterzygots" in coefs_file:
        if heterzygot:
            plot_external_effect(coefs_df, row, axs[ind[p]], **kwargs)
        else:
            plot_external_effect_homozygot(coefs_df, row, axs[ind[p]], **kwargs)

    handles, labels = axs[ind[0]].get_legend_handles_labels()
    # if len(labels) > 1:
    fig.legend(handles, labels, fontsize=17)
    plt.setp(axs, ylim=[-0.5, 0.5])

    fig.suptitle(kwargs["fig_title"], size=18)
    fig.tight_layout(pad=2)
    plt.savefig(kwargs["save_file_name"] + ".jpeg", bbox_inches="tight", pad_inches=0.5)
    plt.show()


if __name__ == "__main__":
    # file = "asthma_alleles_obese_and_not.csv"
    # df = coefs_external_effects(file, alpha=0.05)
    # kwargs = {"colors": ['purple', 'red'], "rot": 90, "fig_title": "Asthma&Alleles",
    #           "save_file_name": "other_astma_alleles"}
    # get_external_effects_coef_df(file, **kwargs)
    #
    # file = "allergic_asthma_obese_and_not.csv"
    # df = coefs_external_effects(file, alpha=0.05)
    # kwargs = {"colors": ['darkgreen', 'lime'], "rot": 90, "fig_title": "Allergic Asthma - Alleles",
    #           "save_file_name": "other_allergic_asthma"}
    # get_external_effects_coef_df(file, **kwargs)
    #
    # file = "asthma_severity_obese_and_not.csv"
    # df = coefs_external_effects(file, alpha=0.05)
    # kwargs = {"colors": ['blue', 'cyan'], "rot": 90, "fig_title": "Asthma Severity - Alleles",
    #           "save_file_name": "other_asthma_severity"}
    # get_external_effects_coef_df(file, **kwargs)

    # file = "interaction_asthma_alleles.csv"
    # df = coefs_external_effects(file, alpha=0.05)
    # kwargs = {"colors": ['purple', 'red'], "rot": 90, "fig_title": "Interaction Model Asthma&Alleles",
    #           "save_file_name": "other_interaction_asthma_alleles"}
    # get_external_effects_coef_df(file, **kwargs)

    # file = "interaction_asthma_homozygots.csv"
    # df = coefs_external_effects(file, alpha=0.05)
    # kwargs = {"colors": ['purple', 'red'], "rot": 90, "fig_title": "Interaction Model Asthma&Homozygous",
    #           "save_file_name": "other_interaction_asthma_homozygous"}
    # get_external_effects_coef_df(file, heterzygot=False, **kwargs)

    file = "interaction_asthma_kirs.csv"
    df = coefs_external_effects(file, alpha=0.05)
    kwargs = {"colors": ['purple', 'red'], "rot": 90, "fig_title": "Interaction Model Asthma&Kir",
              "save_file_name": "other_interaction_asthma_kirs"}
    get_external_effects_coef_df(file, heterzygot=True, **kwargs)
