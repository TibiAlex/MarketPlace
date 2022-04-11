"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import threading
import logging
import logging.handlers

# se creaza fisierul de log si se configureaza la nivelul info si in modul de write
logging.basicConfig(filename='marketplace.log', level=logging.INFO)
LOG = logging.handlers.RotatingFileHandler(filename='marketplace.log', mode='w',
                                           maxBytes=1000, backupCount=0)


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
        logging.info("enter constructor")

        self.queue_size_per_producer = queue_size_per_producer
        self.lock_p = threading.Lock()  # lock pentru producator
        self.lock_c = threading.Lock()  # lock pentru consumator

        self.cart_number = -1  # numarul de carturi
        self.cart_dex = {}  # dictionar de liste pentru a retine toate carturile
        self.producer_number = -1   # numarul de producatori
        self.producer_dex = {}  # dex de liste pentru a retine toti producatorii cu produsele lor

        logging.info("leave constructor")

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        Generate the id of the producer from the number of registrations until now
        And add an empty list in the dex on the place where the key is the producer id
        """
        with self.lock_p:
            logging.info("register producer")
            self.producer_number += 1
            self.producer_dex[self.producer_number] = []
            logging.info("finished registering producer")
        return self.producer_number

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.

        we verify if the queue is not full and add a product on the list in the dex
        """
        with self.lock_p:
            logging.info('try publishing %s on producer with id %s',
                         product, producer_id)
            if self.queue_size_per_producer < len(self.producer_dex[producer_id]):
                logging.error('could not publish %s on producer with id %s',
                              product, producer_id)
                return False
            self.producer_dex[producer_id].append([product, 1])
            logging.info('finished publishing %s on producer with id %s',
                         product, producer_id)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id

        Generate the id of the cart out of the number sof carts
        Add an empty list in the dex
        """

        with self.lock_c:
            logging.info("register new cart")
            self.cart_number += 1
            self.cart_dex[self.cart_number] = []
            logging.info("finished registering new cart")
        return self.cart_number

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again

        We verify if there is the product on the shelf, if it is we put it in the cart
        and change the value of the product on the shelf from 1 to 0
        """
        with self.lock_p:
            logging.info('try adding %s to cart with id %s', product, cart_id)
            for producer, _ in self.producer_dex.items():
                for i, pair in enumerate(self.producer_dex[producer]):
                    if product == pair[0] and pair[1] == 1:
                        self.cart_dex[cart_id].append((producer, product))
                        self.producer_dex[producer][i][1] = 0
                        logging.info('finished adding %s to cart with id %s', product, cart_id)
                        return True
            logging.error('could not add %s to cart with id %s', product, cart_id)
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart

        We remove the product from the cart and change the value of the product on the
        shelf from 0 to 1
        """
        with self.lock_c:
            logging.info('try removing %s from cart with id %s', product, cart_id)
            for pair in self.cart_dex[cart_id]:
                if pair[1] == product:
                    producer_id = pair[0]
                    if pair in self.cart_dex[cart_id]:
                        self.cart_dex[cart_id].remove(pair)
                    for i in range(len(self.producer_dex[producer_id])):
                        if self.producer_dex[producer_id][i][0] == product and \
                                self.producer_dex[producer_id][i][1] == 0:
                            self.producer_dex[producer_id][i][1] = 1
                            break
                    break
            logging.info('finished removing %s from cart with id %s', product, cart_id)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart

        we return a list of the items in the cart
        we remove all the items in the cart and all the items on the shelf
        that have the value of 0
        """
        with self.lock_c:
            logging.info('placing order for cart id %s', cart_id)
            order = []
            for pair in self.cart_dex[cart_id]:
                order.append(pair[1])
                for i in range(len(self.producer_dex[pair[0]])):
                    if self.producer_dex[pair[0]][i][0] == pair[1] and \
                            self.producer_dex[pair[0]][i][1] == 0:
                        del self.producer_dex[pair[0]][i]
                        break
            logging.info('finished placing order for cart id %s', cart_id)
        return order
