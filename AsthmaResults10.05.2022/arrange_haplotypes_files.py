import pandas as pd

if __name__ == "__main__":
    file = "asthma_haplotypes_obese_and_not.csv"
    df = pd.read_csv(file, index_col=0)
    columns = list(df.columns)
    new_columns = []
    for column in columns:
        print(column)
        split_column = column.split("~")
        del split_column[3]
        column_with_no_dp = "~".join(split_column)
        print(column_with_no_dp)
        new_columns.append(column_with_no_dp)
    df.columns = new_columns
    df.to_csv("new_asthma_haplotypes_obese_and_not.csv")
