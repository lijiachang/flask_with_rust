from flask import Flask

from fib_calcs.fib_calculation import FibCalculation
from data_access import dal
from models.databases.fib_entry import FibEntry

app = Flask(__name__)


@app.route('/')
def home():
    return 'home for the fib calculator'


@app.route('/calculate/<int:number>')
def calculate(number):
    calc = FibCalculation(input_number=number)
    return "your entered number is: {0}, and the fibonacci number is: {1}".format(number, calc.fib_number)


@app.route('/calculate_v2/<int:number>')
def calculate_v2(number):
    """
    检查数据库中是否有已经计算过的斐波那契数列的值
    如果没有，则计算并存储到数据库中
    如果有，则直接返回数据库中的值
    """
    fib_calc = dal.session.query(FibEntry).filter(FibEntry.input_number == number).one_or_none()
    if fib_calc is None:
        calc = FibCalculation(input_number=number)
        new_calc = FibEntry(input_number=number, calculated_number=calc.fib_number)
        dal.session.add(new_calc)
        dal.session.commit()
        return f"your entered number is: {number}, which has a fibonacci number of: {calc.fib_number}"
    return f"your entered number is: {number}, which has an existing fibonacci number of: {fib_calc.calculated_number}"


@app.teardown_request
def teardown_request(exception):
    """确保当请求完成时，数据库会话已经过期、关闭和删除。"""
    dal.session.expire_all()
    dal.session.remove()
    dal.session.close()


if __name__ == '__main__':
    app.run(use_reloader=True, port=5002, threaded=True)
