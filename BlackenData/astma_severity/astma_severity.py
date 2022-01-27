import os
from BlackenData.utils import *

def union_blacken_data():
    coef_or_pvalue = "coefs"
    heterzygots_files_list = [os.path.join("all_soldiers", "heterzygots", f"all_soldiers_astma_severity_alleles_easy_vs_hard_{coef_or_pvalue}_together.xls"),
                  os.path.join("ashkenazim", "heterzygots", f"ashkenazim_astma_severity_alleles_easy_vs_hard_{coef_or_pvalue}_together.xls")]
    save_file_name = "heterzygots_astma_severity_alleles_easy_vs_hard"
    heterozygote_union(heterzygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "pvalues"
    heterzygots_files_list = [os.path.join("all_soldiers", "heterzygots", f"all_soldiers_astma_severity_alleles_easy_vs_hard_{coef_or_pvalue}_together.xls"),
                  os.path.join("ashkenazim", "heterzygots", f"ashkenazim_astma_severity_alleles_easy_vs_hard_{coef_or_pvalue}_together.xls")]
    save_file_name = "heterzygots_astma_severity_alleles_easy_vs_hard"
    heterozygote_union(heterzygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "coefs"
    homozygots_files_list = [os.path.join("all_soldiers", "homozygots",
                                          f"homozygot_all_soldiers_astma_severity_easy_vs_hard_{coef_or_pvalue}_seperate.xls"),
                  os.path.join("ashkenazim", "homozygots",
                               f"homozygot_ashkenazim_astma_severity_easy_vs_hard_{coef_or_pvalue}_seperate.xls")]
    save_file_name = "homozygots_astma_severity_alleles_easy_vs_hard"
    homozygote_union(homozygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "pvalues"
    homozygots_files_list = [os.path.join("all_soldiers", "homozygots",
                                          f"homozygot_all_soldiers_astma_severity_easy_vs_hard_{coef_or_pvalue}_seperate.xls"),
                  os.path.join("ashkenazim", "homozygots",
                               f"homozygot_ashkenazim_astma_severity_easy_vs_hard_{coef_or_pvalue}_seperate.xls")]
    save_file_name = "homozygots_astma_severity_alleles_easy_vs_hard"
    homozygote_union(homozygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

union_blacken_data()