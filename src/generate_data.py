import numpy as np, pandas as pd, os

def generate_demo_data(n=500, m=100, phenotype_type='binary', outdir="data"):
    os.makedirs(outdir, exist_ok=True)
    # genotype-like matrix: 0/1/2
    rng = np.random.default_rng(42)
    genotypes = rng.integers(0,3,size=(n,m))
    samples = [f"S{str(i).zfill(5)}" for i in range(n)]
    variants = [f"var_{i}" for i in range(m)]
    gdf = pd.DataFrame(genotypes, index=samples, columns=variants)
    # simple covariates
    age = rng.integers(20,80,size=n)
    sex = rng.integers(0,2,size=n)
    # phenotype influenced by first variant for demo
    if phenotype_type == 'binary':
        logits = -2 + 0.8 * gdf['var_0'].values + 0.01*age + 0.3*sex
        probs = 1 / (1 + np.exp(-logits))
        pheno = (rng.random(n) < probs).astype(int)
    else:
        pheno = 50 + 2.5 * gdf['var_0'].values + 0.1*age + 0.5*sex + rng.normal(0,5,size=n)
    pdf = pd.DataFrame({'phenotype': pheno, 'age': age, 'sex': sex}, index=samples)
    gpath = os.path.join(outdir, "genotypes_demo.csv")
    ppath = os.path.join(outdir, "phenotypes_demo.csv")
    gdf.to_csv(gpath)
    pdf.to_csv(ppath)
    return gpath, ppath

if __name__ == "__main__":
    generate_demo_data()
