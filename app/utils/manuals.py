"""
Модуль утилит для manuals

Этот модуль предоставляет класс PDFCoverExtractor, который позволяет
извлекать первую страницу PDF-файла и сохранять ее как изображение.
"""
import os
import requests
import tempfile
from tempfile import NamedTemporaryFile
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
        response = requests.get(input_url, stream=True)
        with NamedTemporaryFile(suffix='.pdf', dir='/tmp') as tmp:
            for chunk in response.iter_content(1024):
                tmp.write(chunk)
            tmp.seek(0)
            os.chmod(tmp.name, 0o666)
            print(f"Извлечение обложки из {tmp.name}...")
        
            # Открываем входной PDF-файл и извлекаем первую страницу
            pdf_reader = PdfReader(tmp.name)
            first_page = pdf_reader.pages[0]

        # Создаем выходной PDF-writer и добавляем первую страницу
        pdf_writer = PdfWriter()
        pdf_writer.add_page(first_page)

        # Записываем данные выходного PDF в буфер памяти
        buffer = io.BytesIO()
        pdf_writer.write(buffer)

        # Конвертируем данные выходного PDF в изображение и сохраняем как PNG-файл
        images = convert_from_bytes(buffer.getvalue())

        output_filename = f"{os.path.basename(tmp.name)[:-4]}.png"
        output_path = media_path / output_filename
        print(output_path)
        images[0].save(output_path)

        # Выводим сообщение о подтверждении
        print(f"Готово, ваша обложка сохранена по адресу: {output_filename}")

        # Закрываем буфер памяти
        buffer.close()

        return f"{output_filename}"
