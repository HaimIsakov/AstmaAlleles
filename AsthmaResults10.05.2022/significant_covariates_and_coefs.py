from cluster_maps_creator import *

if __name__ == "__main__":
    # file = "interaction_asthma_alleles.csv"
    # file = "interaction_asthma_homozygots.csv"
    # file = "interaction_asthma_kirs.csv"

    file = "new_asthma_haplotypes_obese_and_not.csv"

    df = zero_unsignificant_coefs(file, alpha=0.05)
    save_file_name = f"only_sig_{file}"
    df.to_csv(save_file_name)
