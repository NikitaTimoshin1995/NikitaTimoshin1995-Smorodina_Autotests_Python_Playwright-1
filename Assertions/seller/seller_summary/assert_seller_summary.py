import allure
from Assertions.assertions import Assertions
import time



class AssertionsSellerSummary(Assertions): 

    @allure.step("Проверка операций заказа в базе данных")
    def check_order_operations_in_db(self, db_connection, order_id: int, expected_summa: int = None, 
                                    expected_status_id: int = None, expected_info: str = None,
                                    expected_operation_type_id: int = None, expected_operator_id: int = None):
        timeout = 30
        interval = 2
        elapsed = 0
        operations_data = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            cursor.execute("SELECT summa, status_id, info, operation_type_id, operator_id FROM operations WHERE order_id = %s and operation_type_id=5 order by created_at desc", (order_id,))
            operations_data = cursor.fetchone()
            cursor.close()
            if operations_data is not None:
                break
            else:
                time.sleep(interval)
                elapsed += interval
        if operations_data is None:
            raise AssertionError(f"Операции для заказа с ID {order_id} не найдены в базе данных за отведенное время.")
        summa, status_id, info, operation_type_id, operator_id = operations_data
        if expected_summa is not None:
            expected_summa_float = float(expected_summa)  
            summa_float = float(summa)  
            assert summa_float == expected_summa_float, f"summa не совпадает. Ожидалось: {expected_summa:.2f}, но получено: {summa:.2f}"  
        if expected_status_id is not None:
            assert status_id == expected_status_id, f"status_id не совпадает. Ожидалось: {expected_status_id}, но получено: {status_id}"
        if expected_info is not None:
            assert info == expected_info, f"info не совпадает. Ожидалось: {expected_info}, но получено: {info}"
        if expected_operation_type_id is not None:
            assert operation_type_id == expected_operation_type_id, f"operation_type_id не совпадает. Ожидалось: {expected_operation_type_id}, но получено: {operation_type_id}"
        if expected_operator_id is not None:
            assert operator_id == expected_operator_id, f"operator_id не совпадает. Ожидалось: {expected_operator_id}, но получено: {operator_id}"