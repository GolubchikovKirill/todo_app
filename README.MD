# 📋 Task API

### FastAPI сервис для управления списком задач (ToDo). Поддерживает создание, получение, обновление и удаление задач.

### Стэк:
- **FastAPI**
- **uvicorn**
- **SQL**
- **uv**
- **Docker**

### 📌 Эндпоинты

#### 🔹 Создать задачу

*POST* `/tasks/`

Создает новую задачу.

*Request Body (JSON)*
```json
{
  "title": "Название задачи",
  "description": "Описание задачи",
  "status": "pending"
}
```
*Response*
```json
{
  "id": 1,
  "title": "Название задачи",
  "description": "Описание задачи",
  "status": "pending"
}
```
#### 🔹 Получить задачу по ID

*GET* `/tasks/{task_id}`

Возвращает задачу по её ID.

*Response*
```json
{
  "id": 1,
  "title": "Название задачи",
  "description": "Описание задачи",
  "status": "pending"
}
```
*Возможные ошибки*
    `404 Not Found — если задача не найдена`

#### 🔹 Получить список задач

*GET* `/tasks/

*Query Params*
	`status — (опционально) фильтрация по статусу (pending, completed)`

*Response*
```json
[
  {
    "id": 1,
    "title": "Task 1",
    "description": "Desc 1",
    "status": "pending"
  },
  {
    "id": 2,
    "title": "Task 2",
    "description": "Desc 2",
    "status": "completed"
  }
]
```
#### 🔹 Обновить задачу

*PUT* `/tasks/{task_id}

Обновляет существующую задачу.

*Request Body*
```json
{
  "title": "Новое название",
  "description": "Новое описание",
  "status": "completed"
}
```
*Response*
```json
{
  "id": 1,
  "title": "Новое название",
  "description": "Новое описание",
  "status": "completed"
}
```
*Возможные ошибки*
	`404 Not Found — если задача не найдена`

#### 🔹 Удалить задачу

*DELETE* `/tasks/{task_id}`

Удаляет задачу по ID.

*Response*
```json
{
  "message": "Task deleted"
}
```
*Возможные ошибки*
	`404 Not Found — если задача не найдена`


