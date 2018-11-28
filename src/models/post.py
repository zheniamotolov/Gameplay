class Post:
    def __init__(self, idx, name, type_code):
        self.idx = idx
        self.name = name
        self.type_code = type_code


class Town(Post):
    def __init__(self, idx, name, armor, armor_capacity, events, level,
                 next_level_price, player_idx, point_idx, population,
                 population_capacity, product, product_capacity,
                 train_cooldown):
        super().__init__(idx, name, 1)

        self.armor = armor
        self.armor_capacity = armor_capacity
        self.events = events
        self.level = level
        self.next_level_price = next_level_price
        self.player_idx = player_idx
        self.point_idx = point_idx
        self.population = population
        self.population_capacity = population_capacity
        self.product = product
        self.product_capacity = product_capacity
        self.train_cooldown = train_cooldown


class Market(Post):
    def __init__(self, idx, name):
        super().__init__(idx, name, 2)
        pass


class Storage(Post):
    def __init__(self, idx, name):
        super().__init__(idx, name, 3)
        pass
