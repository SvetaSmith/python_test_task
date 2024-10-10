# Проект решения тестового задания.

Проект написан на Питон 3.12, для запуска приложения необходимо запустить файл main.py.
Для корректной работы приложения до запуска необходимо настроить переменные окружения:
1. TABLE_ID_MY переменная для идентификатора гугл таблицы
2. SERVICE_ACCOUNT b64decode закодированная строка файла json для использования сервисного аккаунта гугл при подключении к апи
3. API_KEY - ApiKey который предоставляет gridly для аутентификации в апи.

В модуле main реализован метод, который последовательно обращается к гугл таблице для получения из нее данных источника, затем получает данные из gridly для сравнения и формирования списков записей требующих добавления и\или обновления содержимого.
Проверка на добавление реализована по появлению новых Record ID, проверка на изменение содержимого строки реализована через изменение hash от данных строки, кроме Record ID.
В модуле gtask содержатся методы для подключения к гугл таблице и получения ее данных в “сыром” виде.
Модуль gridly содержит методы для получения и отправки данных в gridly.


Допущения:
гриды, с именованными колонками в gridly для каждой из таблиц уже существуют, так же, если объем данных станет более существенным, то необходимо рассмотреть вариант помещение данных в табличные структуры внутри кода, например, SQLite

Предварительное заполнение гридов данными не требуется, при первой синхронизации все данные будет перенесены из гугл таблицы.

Альтернативными вариантами для организации данной синхронизации можно назвать:
- использование скрипта Google Apps Script. В таком случае можно реализовать кнопку в главном меню и непосредственно из таблицы осуществлять запуск синхронизации
    
  ```javascript
function onOpen() {
let ui = SpreadsheetApp.getUi();
ui.createMenu("Отправка в gridly")
    .addItem("Отправить данные", "updateData")
   .addToUi();
}
    ```
  пример создания меню.

далее в функции  updateData можно использовать  UrlFetchApp для отправки запроса в  gridly, а SpreadsheetApp для доступа к данным листа 

- так же можно использовать встроенные механизмы  gridly., которые доступны в расширенной версии (от €29 seat / month), Gridly connector доступны в бесплатной версии с ограничениями.
- возможным вариантом видится использование выгрузки из гугл таблиц в виде csv файла и импорт в gridly интерфейсным методом  
- для этой задачи можно использовать airbyte, однако его функционал кажется избыточным
