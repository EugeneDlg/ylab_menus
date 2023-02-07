import os

from celery import Celery
from dotenv import load_dotenv
from datetime import datetime
from xlsxwriter import Workbook

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "password")

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:5672"

celery_app = Celery("tasks", broker=RABBITMQ_URL, backend="rpc://")


@celery_app.task
def generate_xlsx_file(menu_data: list) -> None:
    id_ = celery_app.current_task.request.id
    file_name = f"{datetime.now().strftime('%Y%m%d_%H-%M-%S')}.xlsx"
    file_path = os.path.join("data", file_name)
    workbook = Workbook(file_path)
    worksheet = workbook.add_worksheet()
    worksheet.set_column("A:A", 5)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 20)
    worksheet.set_column("D:D", 20)
    worksheet.set_column("E:E", 80)
    worksheet.set_column("F:F", 15)
    bold = workbook.add_format({"bold": True})
    row_number = 0
    for menu_index, menu in enumerate(menu_data):
        worksheet.write(row_number, 0, menu_index + 1, bold)
        worksheet.write(row_number, 1, menu["title"], bold)
        worksheet.write(row_number, 2, menu["description"], bold)
        row_number += 1
        for submenu_index, submenu in enumerate(menu["submenus"]):
            worksheet.write(row_number, 1, submenu_index + 1, bold)
            worksheet.write(row_number, 2, submenu["title"], bold)
            worksheet.write(row_number, 3, submenu["description"], bold)
            row_number += 1
            for dish_index, dish in enumerate(submenu["dishes"]):
                worksheet.write(row_number, 2, dish_index + 1)
                worksheet.write(row_number, 3, dish["title"], bold)
                worksheet.write(row_number, 4, dish["description"], bold)
                worksheet.write(row_number, 5, dish["price"], bold)
                row_number += 1
    workbook.close()
    return {"file_name": file_name}
