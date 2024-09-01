from flask import Flask

from fib_calcs.fib_calculation import FibCalculation
from data_access import dal
from models.databases.fib_entry import FibEntry

from task_queue.engine import make_celery
from task_queue.fib_calc_task import create_calculate_fib

app = Flask(__name__)
celery = make_celery(app)

calculate_fib = create_calculate_fib(input_celery=celery)


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


@app.route('/calculate_v3/<int:number>')
def calculate_v3(number):
    """
    检查输入的数字是否小于31并且不在数据库，
    如果数字太大 则会将计算发送到Celery并返回一条消息，告诉用于已被发送到队列
    """
    fib_calc = dal.session.query(FibEntry).filter(FibEntry.input_number == number).one_or_none()
    if fib_calc is None:
        if number < 31:  # 立即计算，并将结果存储到数据库
            calc = FibCalculation(input_number=number)
            new_calc = FibEntry(input_number=number, calculated_number=calc.fib_number)
            dal.session.add(new_calc)
            dal.session.commit()
            return f"your entered number is: {number}, which has a fibonacci number of: {calc.fib_number}"
        else:
            calculate_fib.delay(number)
            return (f"your entered number is: {number}, which is too large to calculate immediately, "
                    f"and has been sent to the queue")

    return f"your entered number is: {number}, which has an existing fibonacci number of: {fib_calc.calculated_number}"


@app.teardown_request
def teardown_request(exception):
    """确保当请求完成时，数据库会话已经过期、关闭和删除。"""
    dal.session.expire_all()
    dal.session.remove()
    dal.session.close()


if __name__ == '__main__':
    app.run(use_reloader=True, port=5002, threaded=True)
