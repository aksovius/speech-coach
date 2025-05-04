import time
from functools import wraps
from typing import Callable

from bytewax import operators as op
from bytewax.dataflow import Dataflow

from stream.metrics import ERRORS, PROCESSED_MESSAGES, PROCESSING_LATENCY


def with_metrics(workflow_name: str):
    """Декоратор для добавления метрик к операторам Bytewax"""

    def decorator(operator_func: Callable):
        @wraps(operator_func)
        def wrapper(flow: Dataflow, *args, **kwargs):
            # Получаем оригинальный оператор
            original_operator = operator_func(flow, *args, **kwargs)

            # Создаем новый оператор с метриками
            def measure_step(step_name: str, func: Callable):
                def wrapper(*args, **kwargs):
                    start_time = time.time()
                    try:
                        result = func(*args, **kwargs)
                        PROCESSED_MESSAGES.labels(
                            workflow=workflow_name, status="success"
                        ).inc()
                        return result
                    except Exception as e:
                        ERRORS.labels(
                            workflow=workflow_name, error_type=type(e).__name__
                        ).inc()
                        PROCESSED_MESSAGES.labels(
                            workflow=workflow_name, status="error"
                        ).inc()
                        raise
                    finally:
                        PROCESSING_LATENCY.labels(
                            workflow=workflow_name, step=step_name
                        ).observe(time.time() - start_time)

                return wrapper

            # Добавляем метрики к каждому шагу
            if hasattr(original_operator, "oks"):
                original_operator.oks = measure_step("oks", original_operator.oks)
            if hasattr(original_operator, "errs"):
                original_operator.errs = measure_step("errs", original_operator.errs)

            return original_operator

        return wrapper

    return decorator


# Декорируем основные операторы
map_with_metrics = with_metrics("cleanup")(op.map)
filter_with_metrics = with_metrics("cleanup")(op.filter)
input_with_metrics = with_metrics("cleanup")(op.input)
output_with_metrics = with_metrics("cleanup")(op.output)
