import time

from pyo3_example import fibonacci_number  # Rust实现

from fib_calcs.enums import CalculationMethod
from fib_calcs.fib_calculation import FibCalculation


def _time_process(processor, input_number):
    """统计函数执行执行"""
    start = time.time()
    result = processor(input_number)
    end = time.time()
    return result, end - start


def _process_method(input_method):
    """根据输入的方法字符串返回对应的枚举"""
    calc_enum = CalculationMethod._value2member_map_.get(input_method)
    if calc_enum is None:
        raise ValueError("Invalid calculation method: {}".format(input_method))
    return calc_enum


def calc_fib_number(input_number, method):
    """根据输入的方法计算斐波那契数列，选择Python或Rust实现"""
    if isinstance(method, str):
        method = _process_method(input_method=method)
    if method == CalculationMethod.PYTHON:
        calc, time_taken = _time_process(processor=FibCalculation, input_number=input_number)
        return calc.fib_number, time_taken
    elif method == CalculationMethod.RUST:
        calc, time_taken = _time_process(processor=fibonacci_number, input_number=input_number)
        return calc, time_taken
