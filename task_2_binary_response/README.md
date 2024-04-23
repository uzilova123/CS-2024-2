# Домашнее задание

Для запуска:

1. Установить библиотеки: `pip install -r requirements.txt`
2. Перейти в директорию файла app.py
3. Выполнить команду: `flask --app app run`

Задание:

1. Сделать генерацию самоподобных фигур с помощью L-System (https://github.com/maruschin/l-system)
2. Добавить uri, который будет обрабатывать подобные запросы: `/l_system/iter=3,angle=90,axiom="F-F-F-F",prod="{'F': 'F-F+F+F'}"`

Источники:

1. Документация html, css: https://www.w3schools.com/html/default.asp
2. Фреймворк: https://flask.palletsprojects.com/en/3.0.x/
3. L-System: https://github.com/maruschin/l-system/tree/master
4. http://algorithmicbotany.org/papers/abop/abop.pdf
5. https://inconvergent.net/generative/
6. https://github.com/inconvergent?tab=repositories
