import pandas as pd
import json
from pathlib import Path
from typing import List, Optional

def convert_excel_to_json(
    excel_path: Path, 
    sheet_names: Optional[List[str]] = None, 
    columns: Optional[List[str]] = None, 
    output_path: Optional[Path] = None
    ) -> None:
    """
    Преобразует файл Excel в файл JSON. Файл Excel может иметь несколько листов, и файл JSON будет содержать все данные из всех листов.
    
    args:
        excel_file: Путь к файлу Excel.
        sheet_names: Имена листов, которые необходимо преобразовать. Если None, будут преобразованы все листы.
        columns: Имена столбцов, которые необходимо включить в файл JSON. Если None, будут включены все столбцы.
        output_file: Путь к файлу вывода JSON. Если None, файл JSON будет сохранен в том же каталоге, что и файл Excel.
    """
    if not sheet_names:
        xl = pd.ExcelFile(excel_path)
        sheet_names = xl.sheet_names
        
    result = {}
    
    for sheet in sheet_names:
        df = pd.read_excel(excel_path, sheet_name=sheet)
        
        if columns:
            df = df[columns]
            
        result[sheet] = json.loads(
            df.to_json(orient='records', force_ascii=False)
        )
        
    if not output_path:
        output_path = Path(excel_path).with_suffix('.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
if  __name__ == '__main__':
    excel_path = Path('app/docs/store.xlsx')
    # sheet_names = ['all']
    # columns = ['Цех', 'Группа', 'Помещение', 'Шкаф/Привод', 'Агрегат', 'Преобразователь', 'Тип преобразователя']
    sheet_names = ['Хранение']
    columns = ['Наименование группы', 'Наименование', 'Параметры', 'Ном.н.', 'Кол.', 'Место хранения', 'Размещение', 'Размещение Б/У', 'Размещение новое', 'Установка', 'Примечание']
    convert_excel_to_json(excel_path, sheet_names, columns)
        