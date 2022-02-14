import os

import pandas as pd
from matplotlib import pyplot as plt
file = os.path.join("..","AstmaResults31.01.21", "astma_severity", "significant",
                    "significant_homozygots_astma_severity_alleles_mild_vs_severe.csv")
cur_df = pd.read_csv(file, index_col=0)
cur_df.drop(["count"], inplace=True, axis=0)
cur_df = cur_df.reindex(sorted(cur_df.columns), axis=1)
cur_df_coefs_cols = [col for col in list(cur_df.columns) if col.split("_")[-1] == "coefs"]
coef_cur_df = cur_df[cur_df_coefs_cols]

fig, ax = plt.subplots(1, figsize=(16, 8))
xlabels = [label.replace("_coefs", "") for label in coef_cur_df.columns]
x_pos = xlabels
y = coef_cur_df.values[0]
bar_plot = plt.bar(x_pos, y, width =0.5)
for i in range(len(x_pos)):
    type = xlabels[i].split("_")[-1]
    if type == "all":
        bar_plot[i].set_color('blue')
    else:
        bar_plot[i].set_color('cyan')
rects = bar_plot
for rect in rects:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2., - 0.005 + height,
            f"{height : .3f}",
            ha='center', va='bottom')

plt.ylim(-0.15, 0)

#grid
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)
# plt.title('My Company - 2020\n', loc='left')
plt.savefig("homozygous_asthma_severity.jpeg")
plt.show()
