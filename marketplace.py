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
        self.lock_p = threading.Lock()  # lock :P
        self.lock_c = threading.Lock()
        self.lock = threading.Lock()

        self.cart_number = -1
        self.cart_dex = {}
        self.producer_number = -1
        self.producer_dex = {}

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.lock_p.acquire()
        self.producer_number += 1
        self.producer_dex[self.producer_number] = []
        self.lock_p.release()
        return self.producer_number

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.queue_size_per_producer < len(self.producer_dex[producer_id]):
            return False
        self.producer_dex[producer_id].append([product, 1])
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.lock_c.acquire()
        self.cart_number += 1
        self.cart_dex[self.cart_number] = []
        self.lock_c.release()

        return self.cart_number

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.lock_c.acquire()
        for producer in self.producer_dex:
            for i, pair in enumerate(self.producer_dex[producer]):
                if product == pair[0] and pair[1] == 1:
                    self.cart_dex[cart_id].append((producer, product))
                    self.producer_dex[producer][i][1] = 0
                    self.lock_c.release()
                    return True
        self.lock_c.release()

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.lock_c.acquire()

        for pair in self.cart_dex[cart_id]:
            if pair[1] == product:
                producer_id = pair[0]
                if pair in  self.cart_dex[cart_id]:
                    self.cart_dex[cart_id].remove(pair)
                for i in range(len(self.producer_dex[producer_id])):
                    if self.producer_dex[producer_id][i][0] == product and \
                            self.producer_dex[producer_id][i][1] == 0:
                        self.producer_dex[producer_id][i][1] = 1
                        break
                break
        self.lock_c.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.lock.acquire()
        order = []
        for pair in self.cart_dex[cart_id]:
            order.append(pair[1])
            for i in range(len(self.producer_dex[pair[0]])):
                if self.producer_dex[pair[0]][i][0] == pair[1] and \
                        self.producer_dex[pair[0]][i][1] == 0:
                    del self.producer_dex[pair[0]][i]
                    break
        self.lock.release()
        return order
