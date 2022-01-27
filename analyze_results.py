import pandas as pd

external_effects = ["const", "MIN", "Age_BMI", "Birth_year", "Year_BMI", "dapar_3gr", "Educ_GE11YN", "Israeli",
                    "Eshkol_3gr"]


def find_significant(df, col_name, alpha=0.05):
    print(col_name)
    df_no_external_effects = df.drop(external_effects)
    significant_alleles = df_no_external_effects[df_no_external_effects[col_name] <= alpha].index
    print(f"Number of significant alleles {len(significant_alleles)}")
    return significant_alleles


def all_ashkenazim_comparison(file_name, col_name1, col_name2):
    df = pd.read_csv(file_name, index_col=0)
    all_significant_alleles = find_significant(df, col_name1, alpha=0.05)
    ashkenazim_significant_alleles = find_significant(df, col_name2, alpha=0.05)
    intersec_alleles = set(all_significant_alleles) & set(ashkenazim_significant_alleles)
    print("Number of intersection of alleles ", len(intersec_alleles))
    return intersec_alleles

def all():
    columns_to_compare = []
    for number in [1,2]:
        for loci in ['A', 'B', 'C', 'DRB1', 'DQB1']:
            columns_to_compare.append((f"{number}_{loci}_all" , f"{number}_{loci}_ashkenazim"))

if __name__ == "__main__":
    file_name = "BlackenData/astma_alleles/heterzygots_astma_alleles_pvalues.csv"
    col_name1 = "all_pvalues"
    col_name2 = "ashkenazim_pvalues"
    intersec_alleles = all_ashkenazim_comparison(file_name, col_name1, col_name2)
