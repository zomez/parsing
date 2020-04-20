from writer import Writer2


class Sort:
    def __init__(self):
        self.shop = []
        self.sort_shop = []
        self.mass = []

    def sort(self, mass):
        for item in mass:
            # print('Shop: {}'.format(item['shop']))
            if not item['shop'] in self.shop:
                self.shop.append(item['shop'])

        for item in self.shop:
            self.sort_shop.append([item])

        for item in mass:
            for el in self.sort_shop:
                if item['shop'] == el[0]:
                    el.append([item])

        print(len(self.sort_shop))

        Writer2().run(self.sort_shop)

    def print(self):
        for i in self.sort_shop:
            print(i)

    def run(self):
        self.sort(self.mass)
        print(len(self.sort_shop))
        for i in self.sort_shop:
            print(i)


if __name__ == '__main__':
    Sort().run()
