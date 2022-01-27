import os
from BlackenData.utils import *


def union_blacken_data():
    coef_or_pvalue = "coefs"
    heterzygots_files_list = [os.path.join("all_soldiers", "heterzygots", f"all_soldiers_astma_alleles_{coef_or_pvalue}_together.xls"),
                  os.path.join("ashkenazim", "heterzygots", f"ashkenazim_astma_{coef_or_pvalue}_together.xls")]
    save_file_name = "heterzygots_astma_alleles"
    heterozygote_union(heterzygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "pvalues"
    heterzygots_files_list = [os.path.join("all_soldiers", "heterzygots", f"all_soldiers_astma_alleles_{coef_or_pvalue}_together.xls"),
                  os.path.join("ashkenazim", "heterzygots", f"ashkenazim_astma_{coef_or_pvalue}_together.xls")]
    save_file_name = "heterzygots_astma_alleles"
    heterozygote_union(heterzygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "coefs"
    homozygots_files_list = [os.path.join("all_soldiers", "homozygots",
                                          f"all_soldiers_astma_homozygots_{coef_or_pvalue}_seperate.xls"),
                  os.path.join("ashkenazim", "homozygots",
                               f"ashkenazim_astma_homozygots_{coef_or_pvalue}_seperate.xls")]
    save_file_name = "homozygots_astma_alleles"
    homozygote_union(homozygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "pvalues"
    homozygots_files_list = [os.path.join("all_soldiers", "homozygots",
                                          f"all_soldiers_astma_homozygots_{coef_or_pvalue}_seperate.xls"),
                  os.path.join("ashkenazim", "homozygots",
                               f"ashkenazim_astma_homozygots_{coef_or_pvalue}_seperate.xls")]
    save_file_name = "homozygots_astma_alleles"
    homozygote_union(homozygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

union_blacken_data()