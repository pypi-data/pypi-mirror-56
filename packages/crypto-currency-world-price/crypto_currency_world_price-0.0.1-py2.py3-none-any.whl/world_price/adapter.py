from world_price.base import WorldPriceSource


class WorldPriceAdapter(WorldPriceSource):

    def __init__(self, adaptee):
        self.adaptee = adaptee()

    async def get_price(self, symbol):

        return await self.adaptee.get_price(symbol)
