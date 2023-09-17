import json

from db import establish_connection
from data_loader import (
    load_restaurant_data,
    export_tables,
    export_cuisine_search_results,
)


def load_data(
    load_restaurant_data, export_tables, export_cuisine_search_results, data, cur
):
    load_restaurant_data(data, cur)
    export_tables(cur)
    export_cuisine_search_results(cur)


with open("input_data/FoodHub_data.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

if __name__ == "__main__":
    conn = establish_connection()
    cur = conn.cursor()
    load_data(
        load_restaurant_data, export_tables, export_cuisine_search_results, data, cur
    )
    conn.commit()
    conn.close()
