import click
from os import getcwd
from database import import_data


@click.command()
@click.option(
    '--filepath',
    prompt='Укажите путь до json для импорта',
    default=getcwd() + '/test.json',
    type=click.STRING
)
def main(filepath):
    """
    Функция для приема данных из консоли для импорта
    :param filepath:
    :return:
    """
    click.echo(f'\nУказанный путь: {filepath}')
    if click.confirm('Проверьте введенные данные. Начать импорт?', abort=True, default=True):
        import_data(filepath)


if __name__ == '__main__':
    main()

