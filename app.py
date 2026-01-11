import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import hashlib
from pathlib import Path

from src.assoc import per_variant_logistic, per_variant_linear
from src.generate_data import generate_demo_data

# ==================================================
# Page configuration
# ==================================================
st.set_page_config(
    page_title="PheWAS / GWAS Demo",
    layout="wide"
)

st.title("PheWAS / GWAS Demo – Reproduzierbare Analysepipeline")

# ==================================================
# Authentication helpers
# ==================================================
USERS_FILE = Path("users.json")

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def authenticate_user(username, password):
    users = load_users()
    if username not in users:
        return False
    return users[username] == hash_password(password)

# ==================================================
# Session state initialization (CRITICAL)
# ==================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "genotypes_df" not in st.session_state:
    st.session_state.genotypes_df = None

if "phenotype_series" not in st.session_state:
    st.session_state.phenotype_series = None

if "covariates_df" not in st.session_state:
    st.session_state.covariates_df = None

if "results_df" not in st.session_state:
    st.session_state.results_df = None

# ==================================================
# Login / Registration page
# ==================================================
if not st.session_state.authenticated:
    st.subheader("🔐 Login / Registrierung")

    tabs = st.tabs(["Login", "Registrieren"])

    with tabs[0]:
        login_user = st.text_input("Benutzername", key="login_user")
        login_pw = st.text_input("Passwort", type="password", key="login_pw")

        if st.button("Login"):
            if authenticate_user(login_user, login_pw):
                st.session_state.authenticated = True
                st.session_state.username = login_user
                st.success(f"Eingeloggt als {login_user}")
                st.rerun()
            else:
                st.error("Ungültiger Benutzername oder Passwort")

    with tabs[1]:
        reg_user = st.text_input("Neuer Benutzername", key="reg_user")
        reg_pw = st.text_input("Neues Passwort", type="password", key="reg_pw")

        if st.button("Registrieren"):
            if register_user(reg_user, reg_pw):
                st.success("Registrierung erfolgreich. Bitte einloggen.")
            else:
                st.error("Benutzername existiert bereits.")

    st.stop()

# ==================================================
# Sidebar — ALWAYS visible widgets
# ==================================================
with st.sidebar:
    st.markdown(f"👤 **User:** {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

    st.markdown("---")

    st.header("Datenquelle")

    data_mode = st.radio(
        "Auswahl",
        ["Demo-Daten generieren", "CSV-Dateien hochladen"],
        key="data_mode"
    )

    st.markdown("---")

    genotypes_file = st.file_uploader(
        "Genotypen (CSV)",
        type=["csv"],
        key="geno_upload"
    )

    phenotype_file = st.file_uploader(
        "Phenotype (CSV)",
        type=["csv"],
        key="pheno_upload"
    )

    st.markdown("---")

    n_samples = st.number_input(
        "Anzahl Samples (Demo)",
        min_value=100,
        max_value=5000,
        value=500,
        step=100
    )

    n_variants = st.number_input(
        "Anzahl Varianten (Demo)",
        min_value=10,
        max_value=2000,
        value=100,
        step=10
    )

    phenotype_type = st.selectbox(
        "Phänotyp-Typ",
        ["binary", "continuous"]
    )

    covariates_enabled = st.checkbox(
        "Kovariaten (Alter, Geschlecht)",
        value=True
    )

    st.markdown("---")

    generate_button = st.button("Demo-Daten generieren")
    run_button = st.button("Analyse durchführen")

# ==================================================
# Data loading / generation
# ==================================================
if generate_button and data_mode == "Demo-Daten generieren":
    g_path, p_path = generate_demo_data(
        n=int(n_samples),
        m=int(n_variants),
        phenotype_type=phenotype_type,
        outdir="data"
    )

    st.session_state.genotypes_df = pd.read_csv(g_path, index_col=0)
    pheno_df = pd.read_csv(p_path, index_col=0)

    st.session_state.phenotype_series = pheno_df.iloc[:, 0]

    if covariates_enabled and pheno_df.shape[1] >= 3:
        st.session_state.covariates_df = pheno_df.iloc[:, 1:3]
    else:
        st.session_state.covariates_df = None

    st.session_state.results_df = None
    st.success("Demo-Daten erfolgreich generiert.")

if (
    data_mode == "CSV-Dateien hochladen"
    and genotypes_file is not None
    and phenotype_file is not None
):
    st.session_state.genotypes_df = pd.read_csv(genotypes_file, index_col=0)
    pheno_df = pd.read_csv(phenotype_file, index_col=0)

    st.session_state.phenotype_series = pheno_df.iloc[:, 0]

    if covariates_enabled and pheno_df.shape[1] >= 3:
        st.session_state.covariates_df = pheno_df.iloc[:, 1:3]
    else:
        st.session_state.covariates_df = None

    st.session_state.results_df = None
    st.success("CSV-Dateien erfolgreich geladen.")

# ==================================================
# Analysis
# ==================================================
if run_button:
    if st.session_state.genotypes_df is None:
        st.error("Bitte zuerst Daten laden oder generieren.")
    else:
        with st.spinner("Assoziationsanalyse läuft..."):
            if phenotype_type == "binary":
                res = per_variant_logistic(
                    st.session_state.genotypes_df,
                    st.session_state.phenotype_series,
                    st.session_state.covariates_df
                )
            else:
                res = per_variant_linear(
                    st.session_state.genotypes_df,
                    st.session_state.phenotype_series,
                    st.session_state.covariates_df
                )

            st.session_state.results_df = res

        st.success("Analyse abgeschlossen.")

# ==================================================
# Results
# ==================================================
if st.session_state.results_df is not None:
    res = st.session_state.results_df.dropna(subset=["pval"])

    st.subheader("Top Assoziationen")
    st.dataframe(res.sort_values("pval").head(20), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(range(len(res)), -np.log10(res["pval"]), s=10)
        ax.set_xlabel("Variante")
        ax.set_ylabel("-log10(p)")
        ax.set_title("Manhattan-like Plot")
        st.pyplot(fig)

    with col2:
        pvals = res["pval"].values
        obs = -np.log10(np.sort(pvals))
        exp = -np.log10(np.linspace(1 / len(pvals), 1, len(pvals)))

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(exp, obs, s=8)
        ax.plot([exp.min(), exp.max()], [exp.min(), exp.max()], linestyle="--")
        ax.set_xlabel("Expected -log10(p)")
        ax.set_ylabel("Observed -log10(p)")
        ax.set_title("QQ-Plot")
        st.pyplot(fig)

    csv = res.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Ergebnisse als CSV herunterladen",
        data=csv,
        file_name="phewas_results.csv",
        mime="text/csv"
    )

# ==================================================
# Footer
# ==================================================
st.markdown("---")
st.caption(
    "Proof-of-Concept für statistische Genetik / PheWAS-GWAS. "
    "Synthetische Daten, Python-basierte Analyse. "
    "Skalierung auf PLINK/Hail und HPC vorgesehen (siehe stubs/)."
    "Hinweis: Für biobank-skalige Analysen ist eine PLINK/Hail-Integration vorgesehen "
    "(siehe stubs/plink_stub.py)."
)






