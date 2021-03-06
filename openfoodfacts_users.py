import mysql.connector
import logging
import records

from mysql.connector import errorcode
from logging.handlers import RotatingFileHandler

class DataBaseUsers:
    """
        Class which handle any users
    """
    def __init__(self, connection):
        """
            constructor
        """
        self.conn_user = connection
        self.logger = logging.getLogger()

    def get_all_products_per_category(self, category):
        """
            method which get all products of different categories
        """
        cat = self.conn_user.query(""" SELECT product.barcode, product.name_product, product.grade, product.web_site
                                       FROM products as product
                                       JOIN products_categories as pc
                                            ON pc.product_id = product.barcode
                                       JOIN categories as cat
                                            ON pc.category_id = cat.id
                                       WHERE cat.category= :user_cat
                                       ORDER BY product.barcode;

                             """, user_cat=category, fetchall=True).as_dict()
        return cat

    def get_all_favorites_product(self):
        """
            Method which get all favorite product from user
        """

        all_favorites_products = self.conn_user.query("""
                                                       Select product.barcode, product.name_product, product.grade, product.web_site
                                                       FROM Products as product
                                                       JOIN favorites as fav
                                                            ON fav.id_substitute = product.barcode
                                                        ORDER BY product.barcode
                                                      """).as_dict()

        return all_favorites_products

    def choose_product_from_category(self, category, product):
        """
            Method which is check product with another product
        """
        product_grade = self.conn_user.query("""
                                                SELECT product.barcode, product.name_product, MIN(product.grade), product.web_site, cat.category
                                                FROM products as product
                                                JOIN products_categories as pc
                                                    ON pc.product_id = product.barcode
                                                JOIN categories as cat
                                                    ON pc.category_id = cat.id
                                                WHERE product.grade < :grade AND cat.category= :user_cat
                                                ORDER BY product.grade
                                             """, grade='c' ,user_cat=category, fetchall=True).as_dict()
        return product_grade



    def add_product_into_favorites(self, product, substitute):
        """
            method which is add a product into favorites table

        """
        product_favorite = self.conn_user.query("""
                                INSERT into favorites
                                (id_product, id_substitute)
                                VALUES
                                (:id_product, :id_substitute)

                             """, id_product=product, id_substitute=substitute)
        return product_favorite
