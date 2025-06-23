# IoT Telemetry WebSocket Service

##  Описание

**Тема:** Мониторинг метрик IoT-устройств в реальном времени  
**Назначение:**  
Данный сервис позволяет IoT-устройствам отправлять телеметрию (температуру, влажность, заряд батареи) через WebSocket-соединение.  
Веб-клиент администратора подписывается на потоки устройств и отображает данные в реальном времени.

---

## Стек технологий

- Python 3.9+
- Библиотека `websockets` Python (серверная часть)
- HTML + JavaScript (клиентская часть)
- JSON-протокол обмена сообщениями

---

## Установка и запуск

### 1. Клонировать или загрузить проект

```bash
git clone https://github.com/Kirasect/WebsocketIotTelemetry
cd WebsocketIotTelemetry
```

### 2. Установить зависимости

В терминале pycharm:
```
pip install websockets
```
### 3. Запуск

Запуск сервера
```
python server.py
```
Запуск симулятора устройств
```
python device_sim.py
```
Открыть файл client.html в браузере (двойной клик или через Live Server в VS Code).

## Протокол сообщений JSON

### 1. Аутентификация клиента (устройство или админ):
```
{
  "type": "AUTH",
  "payload": {
    "token": "abc123"
  }
}
```
Ответ сервера (успешно):
```
{
  "type": "AUTH_OK"
}
```
Ответ сервера (ошибка)
```
{
  "type": "AUTH_ERROR",
  "payload": {
    "error": "Invalid token"
  }
}
```

### 2. Отправка метрик устройством:
```
{
  "type": "TELEMETRY",
  "payload": {
    "device_id": "device001",
    "temperature": 22.5,
    "humidity": 45.0,
    "battery": 98
  }
}
```
Ответ администраторам:
```
{
  "type": "TELEMETRY",
  "payload": {
    "device_id": "device001",
    "temperature": 22.5,
    "humidity": 45.0,
    "battery": 98
  }
}
```

### 3. Клиент (админ) может подписаться на конкретные устройства:
Если не отправлять SUBSCRIBE, клиент получит метрики всех устройств по умолчанию.
```
{
  "type": "SUBSCRIBE",
  "payload": {
    "device_id": "device001"
  }
}
```


## Интерфейс администратора
В файле client.html реализован простой веб-интерфейс, отображающий поступающие метрики:
- Метрики группируются по device_id
- Новые данные отображаются сверху

  ![image](https://github.com/user-attachments/assets/a414725d-6519-4b65-b013-61a29c4054f1)


## Структура проекта

![image](https://github.com/user-attachments/assets/a76c8ee0-1ceb-4edb-8903-138f07521dda)

