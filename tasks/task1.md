# Задача 1. Инициализация рабочего окружения

* **Мягкий дедлайн**: --
* **Жёсткий дедлайн**: 26.02.2023, 23:59
* Полный балл: 5

## Задача

- [X] Сделать `fork` данного репозитория.
- [X] Добавить ссылку на ваш `fork` в [таблицу](https://docs.google.com/spreadsheets/d/1-vx82auNr0PQDQ3SwA7IYewZyOC9iHIaoX1w1qRUZ3I/edit?usp=sharing).
- [ ] Добавить в совладельцы форка одного из ассистентов (чтобы узнать, кого именно, нужно посмотреть в [таблицу](https://docs.google.com/spreadsheets/d/1-vx82auNr0PQDQ3SwA7IYewZyOC9iHIaoX1w1qRUZ3I/edit?usp=sharing))
- [X] Реализовать модуль, предоставляющий перечисленные ниже возможности. Для работы с графами использовать [cfpq-data](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#graphs). Данный модуль в дальнейшем будет расширяться. Функции, которые необходимо реализовать:
  - [X] По имени графа вернуть количество вершин, рёбер и перечислить различные метки, встречающиеся на рёбрах. Для получения графа по имени использовать [эту функцию](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#get-a-real-graph).
  - [X] По количеству вершин в циклах и именам меток строить [граф из двух циклов](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.generators.labeled_two_cycles_graph.html#cfpq_data.graphs.generators.labeled_two_cycles_graph) и сохранять его в указанный файл в формате DOT (использовать pydot).
- [ ] Добавить необходимые тесты.
- [X] Добавить запуск тестов с помощью `pytest` в `.github/workflows/`.
