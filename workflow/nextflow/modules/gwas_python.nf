process GWAS_PYTHON {

    tag "python-gwas"

    publishDir "${params.outdir}", mode: 'copy'

    input:
    path genotypes
    path phenotypes

    output:
    path "gwas_results.csv"

    script:
    """
    python - << 'EOF'
    import pandas as pd
    from src.assoc import per_variant_logistic

    geno = pd.read_csv("${genotypes}", index_col=0)
    pheno = pd.read_csv("${phenotypes}", index_col=0)

    res = per_variant_logistic(
        geno,
        pheno.iloc[:, 0],
        None
    )

    res.to_csv("gwas_results.csv", index=False)
    EOF
    """
}
