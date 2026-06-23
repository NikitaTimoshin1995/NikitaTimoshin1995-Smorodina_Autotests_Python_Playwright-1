import allure
from fixtures.all import db_connection  
import psycopg2


class UserAPI:


    @allure.step("Обновить email и login пользователя по телефону")
    def update_user_email_by_phone(self, db_connection, phone: str, email: str):
        try:
            cursor = db_connection.cursor()
            update_query = """
            UPDATE users 
            SET email = %s, 
                login = %s
            WHERE phone = %s
            """
            cursor.execute(update_query, (email, email, phone))
            db_connection.commit()
            updated_rows = cursor.rowcount
            cursor.close()
            allure.attach(f"SQL запрос: {update_query}\nПараметры: phone='{phone}', email='{email}'\nОбновлено строк: {updated_rows}", name="Детали обновления пользователя")
            if updated_rows == 0:
                allure.attach(f"Пользователь с телефоном {phone} не найден", name="Предупреждение")
                return False
            elif updated_rows == 1:
                allure.attach(f"Успешно обновлен пользователь с телефоном {phone}", name="Успех")
                return True
            else:
                allure.attach(f"Обновлено {updated_rows} пользователей с телефоном {phone}", name="Информация")
                return updated_rows
        except psycopg2.Error as e:
            db_connection.rollback()
            error_message = f"Ошибка при обновлении пользователя: {e}"
            allure.attach(error_message, name="Ошибка БД")
            raise Exception(error_message)
        finally:
            if 'cursor' in locals():
                cursor.close()

    @allure.step("Удалить пользователя по номеру телефона и связанные данные из базы данных")
    def delete_user_by_phone(self, conn, phone_number: str):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM users WHERE phone = %s",
                (phone_number,)
            )
            result = cursor.fetchone()
            if not result:
                print(f"Пользователь с телефоном {phone_number} не найден. Переход к следующему шагу.")
                allure.attach(f"Пользователь с телефоном {phone_number} не найден", name="Информация")
                return False
            user_id = result[0]
            print(f"Найден пользователь с id: {user_id}")
            cursor.execute(
                "DELETE FROM sys_user_logs WHERE user_id = %s",
                (user_id,)
            )
            deleted_sys_user_logs = cursor.rowcount
            print(f"Удалено записей из sys_user_logs: {deleted_sys_user_logs}")
            cursor.execute(
                "DELETE FROM order_status_history WHERE user_id = %s",
                (user_id,)
            )
            deleted_order_status_history = cursor.rowcount
            print(f"Удалено записей из order_status_history: {deleted_order_status_history}")
            cursor.execute(
                "DELETE FROM operation_status_history WHERE user_id = %s",
                (user_id,)
            )
            deleted_operation_status_history = cursor.rowcount
            print(f"Удалено записей из operation_status_history: {deleted_operation_status_history}")
            cursor.execute(
                "DELETE FROM operations WHERE user_id = %s",
                (user_id,)
            )
            deleted_operations = cursor.rowcount
            print(f"Удалено записей из operations: {deleted_operations}")
            cursor.execute(
                "DELETE FROM orders WHERE user_id = %s",
                (user_id,)
            )
            deleted_orders = cursor.rowcount
            print(f"Удалено записей из orders: {deleted_orders}")
            cursor.execute(
                "DELETE FROM clients WHERE user_id = %s",
                (user_id,)
            )
            deleted_clients = cursor.rowcount
            print(f"Удалено записей из clients: {deleted_clients}")
            cursor.execute(
                "DELETE FROM users WHERE phone = %s",
                (phone_number,)
            )
            conn.commit()
            success_msg = (f"Удален пользователь с телефоном '{phone_number}' (id: {user_id}). "
                        f"Удалено записей: sys_user_logs={deleted_sys_user_logs}, order_status_history={deleted_order_status_history}, operation_status_history={deleted_operation_status_history}, operations={deleted_operations}, orders={deleted_orders}, clients={deleted_clients}")
            allure.attach(success_msg, name="Успешное удаление")
            print(success_msg)
            return True
        except Exception as e:
            conn.rollback()
            error_msg = f"Ошибка при удалении пользователя с телефоном {phone_number}: {str(e)}"
            allure.attach(error_msg, name="Ошибка")
            raise Exception(error_msg)
        finally:
            cursor.close()