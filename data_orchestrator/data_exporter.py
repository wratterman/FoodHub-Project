import csv

def export_tables(cur):
    tables_to_export = [
        "restaurants",
        "logo_photos",
        "restaurant_cuisines",
        "cuisines",
        "menus",
        "items",
        "menu_items",
    ]
    for table_name in tables_to_export:
        cur.execute(f"SELECT * FROM {table_name};")
        rows = cur.fetchall()

        if rows:
            column_names = [desc[0] for desc in cur.description]

            # Create a CSV file for Created tables
            with open(f"output_csvs/{table_name}.csv", "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(column_names)
                csv_writer.writerows(rows)

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

            # Create a CSV file for Created tables
            with open(
                f"output_csvs/query_results/{cuisine}_items_below_15_dollars.csv",
                "w",
                newline="",
            ) as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(column_names)
                csv_writer.writerows(rows)

            print(
                f"Exported data from '{cuisine} Search' to '{cuisine}_items_below_15_dollars.csv'"
            )
