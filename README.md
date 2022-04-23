# Тестовые задания для компании AliTair
### Задание №1 — Обработка изображений
Наложить .png плашку поверх картинки

#### Решение:
Использование модуля Pillow, OS и Sys. Код решения данной задачи находиться по пути: *sources/image_processing*

**Использование:**
```shell
  (venv)../image_processing$: python main.py data/source.jpg data/shape.png result.jpg
```

### Задание №2 — Aliexpress API
Написать скрипты для обновления остатков и цен. Одновременно должно обновляться не более 50 товаров. Для api рекомендуется написать две функции: обработчик, отправитель запросов. Скрипты реализовать на python 3, для api на python  2.

Шаги обновления:
выгрузить файл поставщика
используя данные из предыдущего шага обновить фид (или наш фид, фид интим4)
реализовать скрипты для обновления остатков и цен на маркетплейсе

#### Решение:
Использование модуля **requests** для скачивания файлов по url совместно с модулем **xml** для парсигна этих файлов

> Конфигурация в файле main.py
> ``` python
> import ...
>
> REMOTE_FEED_URL = 'https://stripmag.ru/datafeed/p5s_full_stock.xml'
> OUR_FEED_URL = 'http://alitair.1gb.ru/Intim_Ali_allfids_2.xml'
> SAVING_PATH = ''
> ```

**Запуск скрипта:**
```shell
(venv)../aliexpress_api$: python main.py
[23.04.2022 14:21:50]: Got data from source file
[23.04.2022 14:21:52]: Got data from destination file
[23.04.2022 14:22:30]: All tree processed successfuly
[23.04.2022 14:22:32]: File saved: Intim_Ali_allfids_2.xml
(venv)../aliexpress_api$:
```
