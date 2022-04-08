"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import threading
import logging


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.cart_count = -1  # numarul de cosuri de cumparaturi
        self.cart_list = []  # lista cu id-ul fiecarui cos de cumparaturi
        self.producer_count = -1  # numarul de producatori
        self.producer_list = []  # lista cu id-ul fiecarui producator
        self.lock = threading.Lock()  # lock :P
        self.all_carts_list = []  # lista de liste ce contine toate obiectele din cosuri
        self.all_producers_id_list = []  # lista de liste cu id-ul producatorilor pt fiecare produs
        self.product_count = 0  # numarul total de produse
        self.all_producers_list = []  # lista de liste cu toate produsele producatorilor

        print("market")

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.lock.acquire()
        self.producer_count += 1
        self.lock.release()

        self.producer_list.append(self.producer_count)
        self.all_producers_list.insert(self.producer_count, [])
        return self.producer_count

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.queue_size_per_producer < self.product_count:
            return False
        self.all_producers_list[producer_id].append(product)
        self.lock.acquire()
        self.product_count += 1
        self.lock.release()
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.lock.acquire()
        self.cart_count += 1
        self.lock.release()

        self.all_carts_list.append([])
        self.all_producers_id_list.insert(self.cart_count, [])
        self.cart_list.append(self.cart_count)
        return self.cart_count

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for i in range(self.producer_count + 1):
            for j in range(len(self.all_producers_list[i])):
                if product == self.all_producers_list[i][j]:
                    self.all_carts_list[cart_id].append(product)
                    self.all_producers_id_list[cart_id].append(i)
                    self.lock.acquire()
                    self.product_count -= 1
                    self.lock.release()
                    self.all_producers_list[i].remove(product)
                    return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        producer_id = 0
        for i in range(len(self.all_carts_list[cart_id])):
            if self.all_carts_list[cart_id][i] == product:
                producer_id = i
                break
        del self.all_carts_list[cart_id][producer_id]
        del self.all_producers_id_list[cart_id][producer_id]
        self.lock.acquire()
        self.product_count += 1
        self.lock.release()

        self.all_producers_list.insert(producer_id, product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.all_carts_list[cart_id]
