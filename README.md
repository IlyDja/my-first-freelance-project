##technical assignment:




+ автоматизировать загрузку отчетов из кабинета Seller.ozozn.ru
+ Получить вход в аккаунт с вводом отп кода
+ Получение отчетов:
+ Отчет продвижение товаров - переходим в Продвижение > Трафареты > Аналитика > Скачать отчет > Жмем кнопку на "вчера"
+ Стоимость хранения - FBO > Стоимость размещения > Скачать отчет > По товарам > выбрать период (только вчерашний день)
+ Закрепленные отзывы - Товары > Закрепление отзыва > Дополнительно Скачать аналитику в excel
+ Отзывы за баллы - Товары > Отзывы за баллы > Аналитика (перейти к отчетам) > За период (только вчерашний день) > Сформировать > Перезайти в "Перейти к отчетам"
+ Выгрузка отчетов на POST /v1/uploadReport
