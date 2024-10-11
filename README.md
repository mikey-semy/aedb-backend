# Проект AEDB

Проект AEDB (Automated Electric Drive Base) представляет собой вспомогательный инструментарий для службы автоматизированного электропривода. 

## Возможности

- Инструкции по эксплуатации для обслуживаемого оборудования
- Электробезопасность
  
## В разработке
- Калькулятор для настройки скоростей моталок
- Формирование и печать наряд-допусков
- Расположение и перечень оборудования
- Перечень хранения на складах

## API Manuals:
### All
- GET /api/v1/manuals
- DELETE /api/v1/manuals
- POST /api/v1/manuals
- POST /api/v1/manuals/add_all
- POST /api/v1/manuals/upload
### Manuals
- GET /api/v1/manuals/nested
- GET /api/v1/manuals/search
- PUT /api/v1/manuals/{manual_id}
- DELETE /api/v1/manuals/{manual_id}
### Groups
- GET /api/v1/manuals/groups
- GET /api/v1/manuals/search_groups
- PUT /api/v1/manuals/group/{group_id}
- DELETE /api/v1/manuals/group/{group_id}
- POST /api/v1/manuals/group
- POST /api/v1/manuals/add_groups
### Categories
- GET /api/v1/manuals/categories
- GET /api/v1/manuals/search_categories
- PUT /api/v1/manuals/category/{category_id}
- DELETE /api/v1/manuals/category/{category_id}
- POST /api/v1/manuals/category
- POST /api/v1/manuals/add_categories



