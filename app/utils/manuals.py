"""
Модуль утилит для manuals

Этот модуль предоставляет класс PDFCoverExtractor, который позволяет
извлекать первую страницу PDF-файла и сохранять ее как изображение.
"""
import os
import requests
from urllib.parse import urlparse
from pdf2image import convert_from_bytes
from PyPDF2 import PdfWriter, PdfReader
import io

from app.const import media_path, media_folder_name

class PDFCoverExtractor:
    """
    Класс для извлечения обложки из PDF-файлов.
    """
    def __init__(self):
        """
        Инициализирует экземпляр PDFCoverExtractor.
        """
        pass

    @staticmethod
    def create_url(input_url):
        """
        Извлекает обложку из PDF-файла и сохраняет ее как изображение.

        Args:
            input_file (str): Путь к входному PDF-файлу.

        Returns:
            None
        """
        # Получаем PDF-файл
        response = requests.get(input_url, stream=True)

        # Извлекаем имя файла из URL
        parsed_url = urlparse(input_url)
        file_name = os.path.basename(parsed_url.path)

        # Указываем путь для сохранения PDF-файла
        local_pdf_path = os.path.join(media_path, "manuals", "covers", file_name)

        # Сохраняем PDF-файл
        with open(local_pdf_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        # Извлекаем обложку из загруженного PDF-файла
        print(f"Извлечение обложки из {local_pdf_path}...")

        # Открываем входной PDF-файл и извлекаем первую страницу
        with open(local_pdf_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            first_page = pdf_reader.pages[0]

            # Создаем выходной PDF-writer и добавляем первую страницу
            pdf_writer = PdfWriter()
            pdf_writer.add_page(first_page)

            # Записываем данные выходного PDF в буфер памяти
            buffer = io.BytesIO()
            pdf_writer.write(buffer)

            # Конвертируем данные выходного PDF в изображение и сохраняем как PNG-файл
            images = convert_from_bytes(buffer.getvalue())

            output_filename = f"{os.path.basename(local_pdf_path)[:-4]}.png"

            output_path = media_path / "manuals" / "covers" / output_filename

            images[0].save(output_path)

            relative_path = media_folder_name / "manuals" / "covers" /  output_filename

            # Выводим сообщение о подтверждении
            print(f"Готово, обложка сохранена по адресу: {relative_path}")

            # Удаляем файл PDF после использования
            if os.path.exists(local_pdf_path):
                os.remove(local_pdf_path)
                print(f"Файл удален: {local_pdf_path}")
            else:
                print(f"Файл не найден для удаления: {local_pdf_path}")
                
            # Закрываем буфер памяти
            buffer.close()

        return f"{relative_path}"
