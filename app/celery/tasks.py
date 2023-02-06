import json
import os

from celery import Celery
from dotenv import load_dotenv
from xlsxwriter import Workbook

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "password")

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:5672"

app = Celery("tasks", broker=RABBITMQ_URL, backend="rpc://")


@app.task(track_started=True)
def generate_xlsx_file(data: list) -> None:

    menu_data = json.loads(data)
    id_ = app.current_task.request.id
    file_path = os.path.join("data", f"{id_}.xlsx")
    workbook = Workbook(file_path)
    worksheet = workbook.add_worksheet()
    worksheet.set_column("A:A", 5)
    worksheet.set_column("B:B", 10)
    worksheet.set_column("C:D", 20)
    worksheet.set_column("E:E", 70)
    worksheet.set_column("F:F", 15)
    bold = workbook.add_format({"bold": True})
    row = 0
    for menu_index, menu in enumerate(menu_data):
        worksheet.write(row, 0, menu_index + 1, bold)
        worksheet.write(row, 1, menu["title"], bold)
        worksheet.write(row, 2, menu["description"], bold)
        row += 1
        for submenu_index, submenu in enumerate(menu["submenus"].values()):
            worksheet.write(row, 1, submenu_index + 1, bold)
            worksheet.write(row, 2, submenu["title"], bold)
            worksheet.write(row, 3, submenu["description"], bold)
            row += 1
            for dish_index, dish in enumerate(submenu["dishes"].values()):
                worksheet.write(row, 2, dish_index + 1)
                worksheet.write(row, 3, dish["title"], bold)
                worksheet.write(row, 4, dish["description"], bold)
                worksheet.write(row, 5, dish["price"], bold)
                row += 1
        workbook.close()
