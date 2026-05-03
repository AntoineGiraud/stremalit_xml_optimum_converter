import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

# Import de notre logique métier modularisée (la même que Streamlit !)
from src.xml_parser import extract_darva_data
from src.pdf_gen import create_professional_pdf

# Initialisation de l'application Typer et de la console Rich
app = typer.Typer(
    help="Générateur de PDF d'Ordre de Mission depuis un XML Optimum/DARVA."
)
console = Console()


@app.command()
def process(
    xml_path: Annotated[
        Path, typer.Argument(help="Chemin vers le fichier XML source à traiter.")
    ],
    output_dir: Annotated[
        Path,
        typer.Option("--out", "-o", help="Dossier de destination pour le PDF généré."),
    ] = Path("output"),
):
    """
    Extrait les données d'un fichier XML et génère un Ordre de Mission PDF.
    """
    # Vérification de l'existence du fichier
    if not xml_path.exists():
        console.print(
            f"[bold red]❌ Erreur :[/bold red] Le fichier '{xml_path}' est introuvable."
        )
        raise typer.Exit(code=1)

    # Vérification/Création du dossier de destination
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[cyan]⚙️  Analyse du fichier XML :[/cyan] {xml_path}")

    try:
        # 1. Traitement Métier : Extraction
        data = extract_darva_data(str(xml_path))

        # Affichage d'un beau tableau récapitulatif dans le terminal avec Rich
        table = Table(show_header=True, header_style="bold magenta", border_style="dim")
        table.add_column("Champ métier", width=25)
        table.add_column("Valeur extraite")

        for key, value in data.items():
            table.add_row(key, str(value))

        console.print(table)
        console.print()

        # 2. Traitement Métier : Génération du PDF
        with console.status(
            "[bold green]Génération du fichier PDF en cours...[/bold green]",
            spinner="dots",
        ):
            pdf_bytes = create_professional_pdf(data)

            # Définition du nom du fichier
            immatriculation = data.get("Immatriculation", "INCONNU").replace("-", "")
            output_file = output_dir / f"OM_{immatriculation}.pdf"

            # Écriture du fichier binaire
            with open(output_file, "wb") as f:
                f.write(pdf_bytes)

        console.print(
            f"[bold green]✅ Succès ![/bold green] Fichier sauvegardé sous : [bold]{output_file}[/bold]\n"
        )

    except Exception as e:
        console.print(
            f"[bold red]❌ Une erreur est survenue lors du traitement :[/bold red] {e}"
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
