import pandas as pd
external_effects = ["const", "MIN", "Age_BMI", "Birth_year", "dapar_3gr", "Educ_GE11YN", "Israeli", "Eshkol_3gr"]


def parse_summary_file(file):
    dict = {}
    for line in file:
        split_line = line.split()
        feature = split_line[0]

        dict[feature] = {"coef": float(split_line[1]), "pvalue": float(split_line[4]),
                         "low_CI": float(split_line[5]), "high_CI": float(split_line[6])}
    df = pd.DataFrame.from_dict(dict, orient="index")
    df.drop(external_effects, axis=0, inplace=True)
    df.sort_index(inplace=True)
    return df


if __name__ == "__main__":
    normal_file = open("logistic_regression_model_all_soldiers_asthma_alleles_normal_summary_together", "r")
    normal_df = parse_summary_file(normal_file)
    normal_df.to_csv("logistic_regression_model_all_soldiers_asthma_alleles_normal_summary_together.csv")
    normal_file.close()
    fat_file = open("logistic_regression_model_all_soldiers_asthma_alleles_overweight_summary_together", "r")
    fat_df = parse_summary_file(fat_file)
    fat_df.to_csv("logistic_regression_model_all_soldiers_asthma_alleles_overweight_summary_together.csv")
    fat_file.close()

    normal_df.set_index(normal_df.index.astype(str) + '_normal', inplace=True)
    fat_df.set_index(fat_df.index.astype(str) + '_overweight', inplace=True)
    united_df = pd.concat([normal_df, fat_df], axis=0)
    united_df.sort_index(inplace=True)
    united_df.to_csv("logistic_regression_model_all_soldiers_asthma_alleles.csv")
    x=1