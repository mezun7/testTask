import database
import click


@click.command()
@click.option('--employee_id', prompt='Укажите идентификатор сотрудника', type=click.INT)
def get_employees(employee_id: int):
    """
    Функция для получения сотрудников в офисе по идентификатору сотрудника
    :param employee_id:
    :return:
    """
    connection = next(database.session_maker)
    employee = database.get_employee_by_id(connection, employee_id)
    if not employee:
        print("Не найден сотрудник с указанным идентификатором")
        return
    office = database.get_office_by_employee_id(connection, employee_id)
    if not office:
        print("Не найден офис для указанного сотрудника")
        return

    employees = database.get_employees_by_office_id(connection, office['id'])
    print(f'{office["Name"]}:', ", ".join([item["Name"] for item in employees]))


if __name__ == "__main__":
    get_employees()
