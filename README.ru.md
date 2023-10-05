# Визуализация истории местоположения
Проект для визуализации вашей истории местоположения из google аккаунта
# Загрузка данных
Переходим на сайт https://takeout.google.com/settings/takeout/custom/all и экспортируем историю своего местоположения в JSON формате.

![Экспорт данных](imgs/ru_export.png?raw=true "Экспорт данных")

Копируем путь до файла и указываем его в файле main.py переменной path_to_data

![Данные местоположений](imgs/ru_records.png?raw=true "Данные местоположений")

Если карта открывается долго, то значит на карте ставится много меток и стоит использовать данные рассортированые по годам

![Местоположения по годам](imgs/ru_years.png?raw=true "Местоположения по годам")