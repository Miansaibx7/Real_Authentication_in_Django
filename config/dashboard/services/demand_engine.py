class DemandEngine:

    @staticmethod
    def calculate(trend_score, price, rating):

        price_score = max(0, 100 - float(price or 50))

        return round(
            trend_score * 0.5 +
            price_score * 0.3 +
            rating * 10 * 0.2,
            2
        )