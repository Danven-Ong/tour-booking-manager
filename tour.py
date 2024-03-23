class Tour:
    def __init__(self, code: str, name: str, days: int, nights: int, cost: float):
        self._code = code
        self._name = name
        self._days = days
        self._nights = nights
        self._cost = cost

    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def days(self) -> int:
        return self._days

    @property
    def nights(self) -> int:
        return self._nights

    @property
    def cost(self) -> float:
        return self._cost

    @cost.setter
    def cost(self, newCost: float) -> float:
        self._cost = newCost

    @property
    def daysNight(self) -> str:
        return f"({self.days}D/{self.nights}N)"

    def __str__(self) -> str:
        return f"Tour Code: {self.code:10}Name: {self.name:<20} {self.daysNight:<10}Base Cost: ${self.cost}"


tour1 = Tour("JPHA08", "Best of Hokkaido", 8, 7, 2699.08)

tour2 = Tour("KMBK08", "Mukbang Korea ", 8, 6, 1699.36)

tour3 = Tour("VNDA06", "Discover Vietnam ", 6, 5, 999.00)

if __name__ == "__main__":
    print(tour1)
    print(tour2)
    print(tour3)
