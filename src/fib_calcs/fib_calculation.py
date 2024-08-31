class FibCalculation:
    def __init__(self, input_number: int):
        self.input_number = input_number
        self.fib_number: int = self.recur_fib(n=self.input_number)

    @staticmethod
    def recur_fib(n: int):
        if n <= 1:
            return n
        else:
            return FibCalculation.recur_fib(n - 1) + FibCalculation.recur_fib(n - 2)
