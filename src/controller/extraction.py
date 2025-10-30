import csv
import os
from dotenv import load_dotenv

load_dotenv()

load_dotenv()
mysql_user: str | None = os.getenv('MYSQL_USER')
mysql_password: str | None = os.getenv('MYSQL_PASSWORD')


def find_csv_files():
    """Trouve automatiquement le dossier contenant les fichiers CSV."""

    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Répertoire actuel : {current_dir}")

    # Tous les chemins potentiels où chercher
    base_paths = [
        os.path.join(current_dir, "../data/10. Hackathon_Leuven_2025"),
        os.path.join(current_dir, "../../data/10. Hackathon_Leuven_2025"),
        "/mnt/c/Users/momo9/Downloads/hackathon-ia/data/10. Hackathon_Leuven_2025",
        "C:/Users/momo9/Downloads/hackathon-ia/data/10. Hackathon_Leuven_2025"
    ]

    # On cherche un dossier qui contient le mot "synthetic"
    for base in base_paths:
        base = os.path.abspath(base)
        if not os.path.exists(base):
            continue

        for item in os.listdir(base):
            full_path = os.path.join(base, item)
            if os.path.isdir(full_path) and "synthetic" in item.lower():
                print(f"✅ Dossier trouvé automatiquement : {full_path}")
                return full_path

    print("❌ Aucun dossier 'Synthetic' trouvé automatiquement.")
    print("Vérifie la structure du dossier. Dossiers explorés :")
    for base in base_paths:
        print(f"  - {os.path.abspath(base)}")
    return None


def generate_sql_inserts():
    data_dir = find_csv_files()
    if not data_dir:
        print("Impossible de trouver les fichiers CSV"); return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "../sql_inserts")
    os.makedirs(output_dir, exist_ok=True)

    file_mapping = {
        'customers.csv': 'customers',
        'products.csv': 'products_active',
        'products_closed.csv': 'products_closed',
        'transactions.csv': 'transactions'
    }

    for csv_file, table_name in file_mapping.items():
        csv_path = os.path.join(data_dir, csv_file)
        print(f"\nRecherche de: {csv_path}")
        if not os.path.exists(csv_path):
            print(f"✗ Fichier introuvable: {csv_file}"); continue

        output_path = os.path.join(output_dir, f"insert_{table_name}.sql")
        print(f"✓ Fichier trouvé: {csv_file}")
        print(f"Génération: {output_path}")

        with open(csv_path, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames or []
            cols_backticked = [f"`{h.replace('`','``')}`" for h in headers]

            with open(output_path, 'w', encoding='utf-8') as sqlfile:
                # 1) Sélectionne la DB
                sqlfile.write("USE ing;\n\n")
                # 2) Crée la table si elle n'existe pas (tout en TEXT pour aller vite)
                ddl_cols = ", ".join([f"{c} TEXT" for c in cols_backticked])
                sqlfile.write(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({ddl_cols});\n\n")

                # 3) INSERTs
                count = 0
                for row in reader:
                    values = []
                    for v in (row.get(h, '') for h in headers):
                        if v == '' or v is None:
                            values.append('NULL')
                        else:
                            values.append("'" + str(v).replace("'", "''") + "'")
                    sql = f"INSERT INTO `{table_name}` ({', '.join(cols_backticked)}) VALUES ({', '.join(values)});\n"
                    sqlfile.write(sql)
                    count += 1

        print(f"✓ {count} lignes générées dans {output_path}")




generate_sql_inserts()