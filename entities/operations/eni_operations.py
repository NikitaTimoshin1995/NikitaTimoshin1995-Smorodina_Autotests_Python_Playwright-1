import allure
from fixtures.all import db_connection  


class OperationsAPI:


    @allure.step('Удаление операций по order_id и operation_type_id')
    def delete_operations_by_order_and_type(self, db_connection, order_id, operation_type_id):
        cursor = db_connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM operations WHERE order_id = %s AND operation_type_id = %s",
                (order_id, operation_type_id)
            )    
            db_connection.commit()
            deleted_count = cursor.rowcount
            allure.attach(
                f"Удалено {deleted_count} операций для order_id={order_id}, operation_type_id={operation_type_id}",
                name="Delete Operations Result",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"Удалено {deleted_count} операций для order_id={order_id}, operation_type_id={operation_type_id}")
            return deleted_count
        except Exception as e:
            db_connection.rollback()
            error_msg = f"Ошибка при удалении операций: {str(e)}"
            allure.attach(error_msg, name="Delete Operations Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(error_msg)    
        finally:
            cursor.close()