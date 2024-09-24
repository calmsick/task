import sys
import os
import pandas as pd
from datetime import datetime, timedelta


def load_data_for_date_range(start_date, end_date):
    """Загружает данные за указанный диапазон дат."""
    data = pd.DataFrame()
    current_date = start_date
    while current_date <= end_date:
        file_name = current_date.strftime('%Y-%m-%d') + '.csv'
        file_path = os.path.join('input', file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            data = pd.concat([data, df])
        current_date += timedelta(days=1)
    return data


def aggregate_data(data):
    """Агрегирует данные по пользователям и типам действий."""
    # Создаем сводную таблицу для подсчета количества действий
    pivot_table = pd.pivot_table(data, index='email', columns='action', aggfunc='size', fill_value=0)

    # Преобразуем MultiIndex в обычные колонки
    pivot_table = pivot_table.reset_index()
    pivot_table.columns.name = None

    # Переименовываем колонки для соответствия требуемому формату
    pivot_table.columns = ['email', 'create_count', 'read_count', 'update_count', 'delete_count']

    return pivot_table


def save_output(aggregated_data, output_date):
    """Сохраняет агрегированные данные в файл."""
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, output_date.strftime('%Y-%m-%d') + '.csv')
    aggregated_data.to_csv(output_file, index=False)


def main(target_date_str):
    """Основная функция для выполнения скрипта."""
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
    start_date = target_date - timedelta(days=7)
    end_date = target_date - timedelta(days=1)

    data = load_data_for_date_range(start_date, end_date)
    aggregated_data = aggregate_data(data)
    save_output(aggregated_data, target_date)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <YYYY-mm-dd>")
        sys.exit(1)

    target_date_str = sys.argv[1]
    main(target_date_str)