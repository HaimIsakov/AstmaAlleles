import os

import pandas as pd
from matplotlib import pyplot as plt

file = os.path.join("..", "AstmaResults31.01.21", "astma_Alleles", "significant",
                    "significant_homozygots_astma_alleles.csv")
cur_df = pd.read_csv(file, index_col=0)
cur_df.drop(["count"], inplace=True, axis=0)
cur_df_coefs_cols = [col for col in list(cur_df.columns) if col.split("_")[-1] == "coefs"]
coef_cur_df = cur_df[cur_df_coefs_cols]

result_df = coef_cur_df
fig, ax = plt.subplots(1, figsize=(16, 8))
xlabels = [label.replace("_coefs", "") for label in coef_cur_df.columns]
plt.bar(xlabels, coef_cur_df.values[0], color = '#337AE3', width =0.5)
plt.ylim(-0.12, 0)

#grid
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
# plt.title('My Company - 2020\n', loc='left')
plt.show()
