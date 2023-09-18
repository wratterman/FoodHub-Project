import pandas as pd


def export_tables(cur):
    tables_to_export = [
        "restaurants",
        "logo_photos",
        "restaurant_cuisines",
        "cuisines",
        "menus",
        "items",
        "restaurant_menu_items",
        "restaurant_menus",
        "restaurant_logos",
    ]
    for table_name in tables_to_export:
        cur.execute(f"SELECT * FROM {table_name} ORDER BY id;")
        rows = cur.fetchall()

        if rows:
            column_names = [desc[0] for desc in cur.description]
            data = pd.DataFrame(rows, columns=column_names)

            csv_file_path = f"output_csvs/{table_name}.csv"
            data.to_csv(csv_file_path, index=False)

            print(f"Exported data from '{table_name}' to '{table_name}.csv'")


def export_cuisine_search_results(cur):
    cuisines_to_search = [
        "French",
        "Italian",
        "Chinese",
        "Mexican",
        "Thai",
        "American",
        "Mediterranean",
        "Japanese",
        "Spanish",
        "Indian",
        "Vietnamese",
        "Greek",
    ]
    for cuisine in cuisines_to_search:
        cur.execute(f"SELECT * FROM menu_items_by_cuisine_and_price('{cuisine}', 15);")
        rows = cur.fetchall()

        if rows:
            column_names = [desc[0] for desc in cur.description]
            data = pd.DataFrame(rows, columns=column_names)

            csv_file_path = (
                f"output_csvs/query_results/{cuisine}_items_below_15_dollars.csv"
            )
            data.to_csv(csv_file_path, index=False)

            print(
                f"Exported data from '{cuisine} Search' to '{cuisine}_items_below_15_dollars.csv'"
            )
