
# PheWAS/GWAS Demo – Streamlit Proof-of-Concept

Kurzbeschreibung
----------------
Dieses Projekt ist ein kompaktes, reproduzierbares Proof-of-Concept, das Fähigkeiten demonstriert, die in der Stellenausschreibung *Statistical Genetics / Machine Learning* (IKMB, Kiel University) gefordert werden. Die App zeigt: Datenaufbereitung, einfache Assoziationsanalysen (per-variant logistic/linear regression), Visualisierungen (Manhattan-like, QQ-Plot), reproduzierbare Workflows (Docker + Skript), und Dokumentation.

Inhalte
-------
- `app.py` – Streamlit-Anwendung (Deutsch), interaktive Demo.
- `src/assoc.py` – Implementierung von per-variant logistic/linear Regression.
- `src/generate_data.py` – Erzeugt synthetische Demo-Daten (Genotypen & Phenotype).
- `data/` – Ort der generierten Demo-Daten.
- `workflow/run_demo.sh` – Einfaches Workflow-Skript (Demo-Daten erzeugen).
- `Dockerfile` – Container-Image für reproduzierbaren Betrieb.
- `requirements.txt` – Python-Abhängigkeiten.
- `README.md` – Diese Datei.

Mapping zu den Anforderungen (Kurz)
----------------------------------
- **Statistische Genetik / PheWAS/GWAS-Relevanz:** Per-variant Tests (logistic/linear) zeigen Grundprinzipien von Assoziationsstudien. In einer Produktionsumgebung würden PLINK/Hail verwendet werden; hier ist das Prinzip in Python reproduziert.
- **Pipeline & Reproduzierbarkeit:** Dockerfile + `workflow/run_demo.sh` zeigen Containerisierung und einen einfachen Workflow. Die Struktur ist bereit für Nextflow/Snakemake Integration.
- **Skalierbarkeit & HPC:** Das Projekt demonstriert die richtige Architektur (modulare Skripte, separate Datengeneratoren, und Konfigurationspunkte) — Nextflow/Snakemake + SLURM-Konfigurationen lassen sich leicht ergänzen.
- **Software-Engineering:** modularer `src/`-Code, Requirements, und klare README-Dokumentation.

GitHub-Projekte (Erklärung & Link)
---------------------------------
- `Timeseries_Forecasting_PowerBI` – Zeitreihenaufbereitung, Modelltraining, Evaluation und PowerBI-Integration. Link: https://github.com/shinejose0007/Timeseries_Forecasting_PowerBI
- `SalesPowerBI` – End-to-end Reporting, Datenmodellierung und DAX-Kennzahlen. Link: https://github.com/shinejose0007/SalesPowerBI
- `Transaction_analysis` – Explorative Analysen, Aggregationen und ETL-Skripte. Link: https://github.com/shinejose0007/Transaction_analysis

Wie ausführen (lokal)
---------------------
1. Klonen / Entpacken des Repositories.
2. (Optional) Container bauen: `docker build -t phewas_demo .`
3. Container laufen lassen: `docker run --rm -p 8501:8501 phewas_demo`
4. Oder lokal: `pip install -r requirements.txt` und `streamlit run app.py`

Hinweis
-----
Dieses Projekt verwendet synthetische Daten zu Demonstrationszwecken. Für echte biobank-skalige Analysen sind spezialisierte Formate (BGEN/PLINK/Hail) und zusätzliches QC/Privacy-Handling erforderlich.

Kontakt
-------
Shine Jose – shine.jose3@gmail.com
