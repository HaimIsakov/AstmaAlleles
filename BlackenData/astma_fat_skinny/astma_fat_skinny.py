import os
from BlackenData.utils import *

def union_blacken_data():
    coef_or_pvalue = "coefs"
    heterzygots_files_list = [os.path.join("all_soldiers", "fat", "heterzygots",
                                           f"all_soldiers_astma_alleles_fat_population_{coef_or_pvalue}_together.xls"),
                              # os.path.join("ashkenazim", "fat", "heterzygots",
                              #              f"ashkenazim_astma_{coef_or_pvalue}_together.xls"),
                              os.path.join("all_soldiers", "skinny", "heterzygots",
                                           f"all_soldiers_astma_alleles_skinny_population_{coef_or_pvalue}_together.xls"),
                              os.path.join("ashkenazim", "skinny", "heterzygots",
                                           f"ashkenazim_astma_skin_population_{coef_or_pvalue}_together.xls")]
    save_file_name = "heterzygots_fat_skinny_astma_alleles"
    heterozygote_union(heterzygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "pvalues"
    heterzygots_files_list = [os.path.join("all_soldiers", "fat", "heterzygots",
                                           f"all_soldiers_astma_alleles_fat_population_{coef_or_pvalue}_together.xls"),
                              # os.path.join("ashkenazim", "fat", "heterzygots",
                              #              f"ashkenazim_astma_{coef_or_pvalue}_together.xls"),
                              os.path.join("all_soldiers", "skinny", "heterzygots",
                                           f"all_soldiers_astma_alleles_skinny_population_{coef_or_pvalue}_together.xls"),
                              os.path.join("ashkenazim", "skinny", "heterzygots",
                                           f"ashkenazim_astma_skin_population_{coef_or_pvalue}_together.xls")]
    save_file_name = "heterzygots_fat_skinny_astma_alleles"
    heterozygote_union(heterzygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "coefs"
    homozygots_files_list = [os.path.join("all_soldiers", "fat", "homozygots",
                                          f"all_soldiers_astma_fat_population_homozygot_{coef_or_pvalue}_seperate.xls"),
                             os.path.join("ashkenazim", "fat", "homozygots",
                                          f"ashkenazim_astma_fat_population_homozygot_{coef_or_pvalue}_seperate.xls"),
                             os.path.join("all_soldiers", "skinny", "homozygots",
                                          f"all_soldiers_astma_skin_population_homozygot_{coef_or_pvalue}_seperate.xls"),
                             os.path.join("ashkenazim", "skinny", "homozygots",
                                          f"ashkenazim_astma_skin_population_homozygot_{coef_or_pvalue}_seperate.xls")]
    save_file_name = "homozygots_fat_skinny_astma_alleles"
    homozygote_union(homozygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

    coef_or_pvalue = "pvalues"
    homozygots_files_list = [os.path.join("all_soldiers", "fat", "homozygots",
                                          f"all_soldiers_astma_fat_population_homozygot_{coef_or_pvalue}_seperate.xls"),
                             os.path.join("ashkenazim", "fat", "homozygots",
                                          f"ashkenazim_astma_fat_population_homozygot_{coef_or_pvalue}_seperate.xls"),
                             os.path.join("all_soldiers", "skinny", "homozygots",
                                          f"all_soldiers_astma_skin_population_homozygot_{coef_or_pvalue}_seperate.xls"),
                             os.path.join("ashkenazim", "skinny", "homozygots",
                                          f"ashkenazim_astma_skin_population_homozygot_{coef_or_pvalue}_seperate.xls")]
    save_file_name = "homozygots_fat_skinny_astma_alleles"
    homozygote_union(homozygots_files_list, save_file_name, coef_or_pvalue=coef_or_pvalue)

union_blacken_data()