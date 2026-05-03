# 🚗 Connecteur XML DARVA/Optimum vers PDF

Ce projet est un prototype interactif développé avec **Streamlit**. Il permet de simuler la réception d'un flux XML d'assurance automobile (type Norme DARVA / Optimum), d'en extraire les informations métier clés via XPath, et de générer un Ordre de Mission structuré au format PDF.

## ✨ Fonctionnalités

- **Upload de fichier XML** : Interface drag & drop pour charger le flux.
- **Parsing ciblé** : Extraction robuste des données du client, du véhicule et du sinistre via XPath.
- **Visualisation métier** : Affichage synthétique des informations critiques (Immatriculation, Franchise, etc.) directement dans l'UI.
- **Génération PDF** : Création à la volée d'une fiche d'intervention téléchargeable (grâce à `fpdf2`).

## 📸 Aperçus

### Interface Streamlit

![Interface utilisateur](./docs/screen_ui_streamlit.png)

### PDF Généré

![Aperçu du PDF](./docs/screen_pdf_genere.png)

## 🛠️ Utilisation

Assurez-vous d'avoir uv installé sur votre machine pour gérer votre environnement python.

1. Clonez ce repository.
2. `uv sync` Installez les dépendances python requises
3. `uv run streamlit run main.py` lancer l'app streamlit (ui)
4. Charger le fichier `input\demo_optimum.xml` pour la démo

### Option terminal `cli.py` avec typer

- `uv run cli.py --help`
- `uv run cli.py input\demo_optimum.xml`
- `uv run cli.py input\demo_optimum.xml -o autre/chemin/de/sortie`

![screen_cli_typer](./docs/screen_cli_typer.png)