import json

from django.core.cache import cache

from product.models import Price


class Cart:

    CARD_CACHE_ID = 'card_'

    def __init__(self, request):
        self.user = request.user

        cart = cache.get(self.CARD_CACHE_ID + self.user.id)

        if not cart:
            cart = {}
        else:
            cart = json.loads(cart)

        self.cart = cart

    @classmethod
    def unique_name_generator(cls, product, price):
        return f'{product.id}-{price.id}'

    @property
    def show_cart(self):
        return self.cart.values()

    def total_price(self):

        chosen_product = [product['price'] for product in self.show_cart]

        return sum(Price.objects.filter(pk__in=chosen_product).values_list('price', flat=True))

    def add(self, product, quantity, price):

        key = self.unique_name_generator(product, price)

        if key not in self.cart.keys():
            self.cart.update({key: {
                'product': product.id,
                'quantity': quantity,
                'price': price.id,
            }})
        else:
            self.cart[key]['quantity'] += 1

        self.save()

    def remove(self, product, price):
        key = self.unique_name_generator(product, price)

        if self.cart[key]['quantity'] == 1:
            self.cart.pop(key)
        else:
            self.cart[key]['quantity'] -= 1

        self.save()

    @property
    def clear(self):
        cache.delete(self.CARD_CACHE_ID + self.user.id)
        return 0

    def save(self):

        self.cart = json.dumps(self.cart)
        cache.set(self.CARD_CACHE_ID + self.user.id, self.cart, 60 * 60 * 24 * 4)

