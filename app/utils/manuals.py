"""
Модуль утилит для manuals

Этот модуль предоставляет класс PDFCoverExtractor, который позволяет
извлекать первую страницу PDF-файла и сохранять ее как изображение.
"""
import os
import requests

from pdf2image import convert_from_bytes
from PyPDF2 import PdfWriter, PdfReader
import io

from app.const import media_path

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
        local_pdf_path = os.path.join(media_path, file_name)
        print(f"local_pdf_path: {local_pdf_path}")

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
            output_path = media_path / output_filename
            print(output_path)
            images[0].save(output_path)

            # Выводим сообщение о подтверждении
            print(f"Готово, ваша обложка сохранена по адресу: {output_path}")

            # Закрываем буфер памяти
            buffer.close()

        return f"{output_path}"
