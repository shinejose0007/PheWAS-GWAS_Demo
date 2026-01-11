nextflow.enable.dsl=2

workflow {

    Channel
        .fromPath(params.genotypes)
        .set { geno_ch }

    Channel
        .fromPath(params.phenotypes)
        .set { pheno_ch }

    GWAS_PYTHON(
        geno_ch,
        pheno_ch
    )
}
