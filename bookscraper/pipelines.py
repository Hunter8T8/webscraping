# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # --- Strip whitespaces from all string fields except description ---
        for field_name in adapter.field_names():
            if field_name != 'description':
                value = adapter.get(field_name)

                # Handle None values
                if not value:
                    adapter[field_name] = ""
                    continue

                # If list/tuple, take first element
                if isinstance(value, (list, tuple)):
                    value = value[0] if len(value) > 0 else ""

                # Ensure string before strip
                adapter[field_name] = str(value).strip()

        # --- category & product_type to lowercase ---
        for lowercase_key in ['category', 'product_type']:
            value = adapter.get(lowercase_key)

            if not value:
                adapter[lowercase_key] = ""
                continue

            if isinstance(value, (list, tuple)):
                value = value[0] if len(value) > 0 else ""

            adapter[lowercase_key] = str(value).lower()

        # --- availability (extract number) ---
        availability_string = adapter.get('availability')
        if availability_string and '(' in availability_string:
            try:
                availability_array = availability_string.split('(')[1].split(' ')
                adapter['availability'] = int(availability_array[0])
            except (IndexError, ValueError):
                adapter['availability'] = 0
        else:
            adapter['availability'] = 0

        # --- num_reviews to int ---
        num_reviews_string = adapter.get('num_reviews', "0")
        if isinstance(num_reviews_string, (list, tuple)):
            num_reviews_string = num_reviews_string[0] if len(num_reviews_string) > 0 else "0"

        try:
            adapter['num_reviews'] = int(num_reviews_string)
        except (ValueError, TypeError):
            adapter['num_reviews'] = 0

        # --- stars to int ---
        stars_string = adapter.get('stars')
        if stars_string:
            split_stars_array = str(stars_string).split()
            if len(split_stars_array) > 1:
                stars_text_value = split_stars_array[1].lower()
                stars_map = {
                    "zero": 0, "one": 1, "two": 2,
                    "three": 3, "four": 4, "five": 5
                }
                adapter['stars'] = stars_map.get(stars_text_value, 0)
            else:
                adapter['stars'] = 0
        else:
            adapter['stars'] = 0

        return item


class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='abhi8289',
            database='books'
        )
        self.cur = self.conn.cursor()

        # Create table if not exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id INT NOT NULL AUTO_INCREMENT,
            url VARCHAR(255),
            title TEXT,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL(10,2),
            price_incl_tax DECIMAL(10,2),
            tax DECIMAL(10,2),
            price DECIMAL(10,2),
            availability INT,
            num_reviews INT,
            stars INT,
            category VARCHAR(255),
            description TEXT,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO books (
            url, title, upc, product_type,
            price_excl_tax, price_incl_tax, tax, price,
            availability, num_reviews, stars, category, description
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            item.get("url", ""),
            item.get("title", ""),
            item.get("upc", ""),
            item.get("product_type", ""),
            self._safe_number(item.get("price_excl_tax")),
            self._safe_number(item.get("price_incl_tax")),
            self._safe_number(item.get("tax")),
            self._safe_number(item.get("price")),
            self._safe_int(item.get("availability")),
            self._safe_int(item.get("num_reviews")),
            self._safe_int(item.get("stars")),
            item.get("category", ""),
            str(item.get("description", "")) if item.get("description") else None
        ))

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    # --- Helper functions ---
    def _safe_number(self, value):
        if isinstance(value, (list, tuple)):
            value = value[0] if len(value) > 0 else 0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _safe_int(self, value):
        if isinstance(value, (list, tuple)):
            value = value[0] if len(value) > 0 else 0
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

                         




    





                         
                         

