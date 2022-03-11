# Hairdresser API

## Описание

Данный python-проект написан для упрощения разработки собственных приложений
парикмахерских или тренировки в написании и поддержки API серверов.

За основу взяты пакеты aiohttp (для асинхронной обработки запросов) и gino (для
асинхронной работы с базой данных)

По умолчанию имеются такие объекты как Пользователь, Организация, Администратор,
Парикмахер, Услуга, Смена, Отделение, Сессия и методы для работы с ними.

Проект подойдет как заготовка для собственного решения. Дописав новые и
отредактировав имеющиеся методы, можно получить приложение, отвечающее вашим
собственным требованиям и предпочтениям.

---

## Термины и определения

Организация (Organization) - Владелец сервиса, имеющий права на редактирование
любых данных сервиса.

Отделение (Department) - Одна из имеющихся парикмахерских организации.

Услуга (Service) - Стрижка, укладка или любое другое действие, осуществляемое
парикмахером в отношении клиента.

Смена (Shift) - Временной период работы группы парикмахеров.

Клиент (Customer) - Пользователь, зарегистрировавшийся и желающий получить
какие-либо услуги сервиса.

Парикмахер (Hairdresser) - Пользователь, зарегистрированный организацией для 
оказания услуг клиентам.

Администратор (Administrator) - Пользователь, зарегистрированный организацией для
контроля работы парикмахеров и отделений парикмахерской. И имеющий права на
редактирование некоторых данных сервиса.

Сессия (Session) - Временной промежуток, разрешающий пользователю доступ к 
серверу. Также, сессия - строка ссылающаяся на какую-либо сессию. 

---

## Список запросов

### Customer

#### Customer: GET

[GET /customer](#get-customer)

[GET /customer.recover_password](#get-customerrecover_password)

[GET /customer.administrator](#get-customeradministrator)

[GET /customer.reception](#get-customerreception)

[GET /customer.department](#get-customerdepartment)

[GET /customer.hairdresser](#get-customerhairdresser)

#### Customer: POST

[POST /customer.edit](#post-customerrecover_password)

[POST /customer.recover_password](#post-customerrecover_password)

[POST /customer.registration](#post-customerregistration)

[POST /customer.authorization](#post-customerauthorization)

[POST /customer.reception](#post-customerreception)

#### Customer: PUT

[PUT /customer.reception](#post-customerreception)

#### Customer: DELETE

[DELETE /customer.reception](#post-customerreception)

### Administrator

#### Administrator: GET

[GET /administrator](#get-administrator)

[GET /administrator.customer](#get-administratorcustomer)

[GET /administrator.hairdresser](#get-administratorhairdresser)

[GET /administrator.department](#get-administratordepartment)

[GET /administrator.administrator](#get-administratoradministrator)

[GET /administrator.service](#get-administratorservice)

[GET /administrator.reception](#get-administratorreception)

[GET /administrator.shift](#get-administratorshift)

[GET /administrator.session](#get-administratorsession)

#### Administrator: POST

[POST /administrator.authorization](#post-administratorauthorization)

[POST /administrator.department](#post-administratordepartment)

[POST /administrator.shift](#post-administratorshift)

#### Administrator: PUT

[PUT /administrator.shift](#put-administratorshift)

#### Administrator: DELETE

[DELETE /administrator.reception](#delete-administratorreception)

[DELETE /administrator.shift](#delete-administratorshift)

[DELETE /administrator.session](#delete-administratorsession)

### Hairdresser

#### Hairdresser: GET

[GET /hairdresser](#get-hairdresser)

[GET /hairdresser.administrator](#get-hairdresseradministrator)

[GET /hairdresser.hairdresser](#get-hairdresserhairdresser)

[GET /hairdresser.customer](#get-hairdressercustomer)

[GET /hairdresser.department](#get-hairdresserdepartment)

[GET /hairdresser.reception](#get-hairdresserreception)

[GET /hairdresser.shift](#get-hairdressershift)

#### Hairdresser: POST

[POST /hairdresser.authorization](#post-hairdresserauthorization)

#### Hairdresser: DELETE

[DELETE /hairdresser.reception](#delete-hairdresserreception)

### Organization

#### Organization: GET

[GET /organization](#get-organization)

[GET /organization.customer](#get-organizationcustomer)

[GET /organization.hairdresser](#get-organizationhairdresser)

[GET /organization.department](#get-organizationdepartment)

[GET /organization.administrator](#get-organizationadministrator)

[GET /organization.service](#get-organizationservice)

[GET /organization.reception](#get-organizationreception)

[GET /organization.shift](#get-organizationshift)

[GET /organization.session](#get-organizationsession)

#### Organization: POST

[POST /organization.authorization](#post-organizationauthorization)

[POST /organization.hairdresser](#post-organizationhairdresser)

[POST /organization.department](#post-organizationdepartment)

[POST /organization.administrator](#post-organizationadministrator)

[POST /organization.service](#post-organizationservice)

[POST /organization.shift](#post-organizationshift)

#### Organization: PUT

[PUT /organization.hairdresser](#put-organizationhairdresser)

[PUT /organization.department](#put-organizationdepartment)

[PUT /organization.administrator](#put-organizationadministrator)

[PUT /organization.service](#put-organizationservice)

[PUT /organization.shift](#put-organizationshift)

#### Organization: DELETE

[DELETE /organization.hairdresser](#delete-organizationhairdresser)

[DELETE /organization.department](#delete-organizationdepartment)

[DELETE /organization.administrator](#delete-organizationadministrator)

[DELETE /organization.service](#delete-organizationservice)

[DELETE /organization.reception](#delete-organizationreception)

[DELETE /organization.shift](#delete-organizationshift)

[DELETE /organization.session](#delete-organizationsession)

---

## Запросы

### GET /customer

Возвращает пользователю его информацию.

_Параметры запроса_

```text
Не принимает параметры
```

_Пример запроса_

```text
*domain*/customer
```

_Структура ответа_

```text
id - ID пользователя
email - Электронная почта пользователя
name - Фамилия Имя пользователя
phone - Номер мобильного телефона пользователя
```

_Пример ответа_

```json
{
  "id": 1,
  "email": "customer_email@gmail.com",
  "name": "Марочкин Даниил",
  "phone": "+1 (222) 333-44-55"
}
```

### POST /customer.edit

Редактирует данные пользователя. И возвращает актуальную информацию.

_Параметры запроса_

```text
new_name - Новые Фамилия и Имя
new_email - Новая электронная почта
new_password - Новый пароль 
new_phone - Новый номер мобильного телефона
```

`Запрос может включать не все параметры`

_Примеры запроса_

```json
{
  "new_name": "Марочкин Данил",
  "new_email": "other_email@gmail.com",
  "new_password": "A2qKfoSd3XCsx7QK",
  "new_phone": "+3 (222) 333-44-55"
}
```

```json
{
  "new_password": "A2qKfoSd3XCsx7QK"
}
```

_Структура ответа_

```text
id - ID пользователя
email - Электронная почта пользователя
name - Фамилия Имя пользователя
phone - Номер мобильного телефона пользователя
```

_Пример ответа_

```json
{
  "id": 1,
  "email": "other_email@gmail.com",
  "name": "Марочкин Данил",
  "phone": "+3 (222) 333-44-55"
}
```

### GET /customer.recover_password

Создает запрос на восстановление пароля.

_Параметры запроса_

```text
email - Электронная почта пользователя
```

_Пример запроса_

```text
*domain*/customer.recover_password?email=customer_email@gmail.com
```

_Пример ответа_

```text
Не возвращает данные
```

### POST /customer.recover_password

Восстанавливает пароль.

_Параметры запроса_

```text
key - Код подтверждения почты
new_password - Новый пароль 
```

_Пример запроса_

```json
{
  "key": "37a40385-8242-40de-b703-ce57f0a05ea0",
  "new_password": "bMkdULeSWhuJyMzU"
}
```

_Пример ответа_

```text
Не возвращает данные
```

### POST /customer.registration

Регистрирует нового пользователя. Сразу создает сессию и передает ее в cookies.

_Параметры запроса_

```text
name - Фамилия Имя
email - Электронная почта
password - Пароль
phone - Номер мобильного телефона для связи при возникновении вопросов
```

_Пример запроса_

```json
{
  "name": "Марочкин Даниил",
  "email": "customer_email@gmail.com",
  "password": "zUWhuLbJdUMkyMeS",
  "phone": "+1 (222) 333-44-55"
}
```

_Пример ответа_

```text
Не возвращает данные
```

### POST /customer.authorization

Авторизует пользователя. Создает сессию и передает ее в cookies.

_Параметры запроса_

```text
email - Адрес электронной почты
password - Пароль
```

_Пример запроса_

```json
{
  "email": "customer_email@gmail.com",
  "password": "zUWhuLbJdUMkyMeS"
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /customer.reception

Возвращает список записей пользователя.

_Параметры запроса_

```text
id - ID записи
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/customer.reception
```

```text
*domain*/customer.reception?id=1
```

_Структура ответа_

```text
reception - запись(или receptions - список записей)
    id - ID записи
    day - День записи
    month - Месяц записи
    year - Год записи
    day_time - время записи в минутах с начала дня
    services - список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время предоставления услуги
    customer - Пользователь
        id - ID пользователя
        email - Электронная почта пользователя
        name - Фамилия Имя пользователя
        phone - Номер мобильного телефона пользователя
    hairdresser - Парикмахер
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    department - Отделение
        id - ID отделения
        address - Адрес отделения
        name - Название отделения    
```

_Примеры ответа_

`Если id передан данные находятся в поле reception`

`Если id не передан данные находятся в поле receptions`

```json
{
  "receptions": []
}
```

```json
{
  "receptions": [
    {
      "id": 31,
      "day": 1,
      "month": 3,
      "year": 2022,
      "day_time": 720,
      "services": [
        {
          "id": 1,
          "name": "Модельная стрижка",
          "price": 750,
          "duration": 45
        }
      ],
      "customer": {
        "id": 1,
        "email": "customer_email@gmail.com",
        "name": "Марочкин Даниил",
        "phone": "+1 (222) 333-44-55"
      },
      "hairdresser": {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      },
      "department": {
        "id": 1,
        "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
        "name": "СПбГУПТД на БМ"
      }
    }
  ]
}
```

```json
{
  "reception": {
    "id": 31,
    "day": 1,
    "month": 3,
    "year": 2022,
    "day_time": 720,
    "services": [
      {
        "id": 1,
        "name": "Модельная стрижка",
        "price": 750,
        "duration": 45
      }
    ],
    "customer": {
      "id": 1,
      "email": "customer_email@gmail.com",
      "name": "Марочкин Даниил",
      "phone": "+1 (222) 333-44-55"
    },
    "hairdresser": {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    },
    "department": {
      "id": 1,
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
      "name": "СПбГУПТД на БМ"
    }
  }
}
```

### POST /customer.reception

Возвращает доступные для создания записи данные. Время, парикмахер, услуги.
Используется до отправки запроса на создание записи для определения доступных
услуг на выбранный год, месяц, день.

_Параметры запроса_

```text
department - ID отделения парикмахерской
services - список ID услуг
hairdresser - ID парикмахера
year - год проверки 
month - месяц проверки
day - день проверки
day_time - время записи в минутах от начала дня
```

`services не является обязательным параметром`

`hairdresser не является обязательным параметром`

`day_time не является обязательным параметром`

_Примеры запроса_

```json
{
  "department": 1,
  "services": [
    1,
    2,
    3,
    4
  ],
  "hairdresser": 1,
  "year": 2022,
  "month": 3,
  "day": 2,
  "day_time": 183
}
```

```json
{
  "department": 1,
  "year": 2022,
  "month": 3,
  "day": 1
}
```

_Структура ответа_

```text
available_time - Список доступного для записи времени (по заданным параметрам)
    1 значение элемента - начало отрезка с доступным для записи временем
    2 значение элемента - конец отрезка с доступным для записи временем
available_services - Список доступных услуги услуг (по заданным параметрам)
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
available_hairdressers - Список доступных парикмахеров (по заданным параметрам)
        id - ID парикмахера
        name - Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Примеры ответа_

```json
{
  "available_time": [
    [
      700,
      1200
    ],
    [
      1250,
      1400
    ]
  ],
  "available_services": [
    {
      "id": 1,
      "name": "Модельная стрижка",
      "price": 750,
      "duration": 45
    },
    {
      "id": 2,
      "name": "Укладка",
      "price": 500,
      "duration": 30
    }
  ],
  "available_hairdressers": [
    {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    }
  ]
}
```

```json
{
  "available_time": [],
  "available_services": [],
  "available_hairdressers": []
}
```

### PUT /customer.reception

Записывает пользователя на прием.

_Параметры запроса_

```text
department - ID отделения парикмахерской
services - список ID услуг
hairdresser - ID парикмахера
year - год записи 
month - месяц записи
day - день записи
day_time - время записи в минутах от начала дня
```

_Пример запроса_

```json
{
  "department": 1,
  "services": [
    1
  ],
  "hairdresser": 1,
  "year": 2022,
  "month": 3,
  "day": 2,
  "day_time": 1200
}
```

_Структура ответа_

```text
reception - запись 
    id - ID записи
    year - Год записи
    month - Месяц записи
    day - День записи
    day_time - Время записи в минутах от начала дня
    services - список услуг в записи
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
    customer - Пользователь
        id - ID пользователя
        email - Электронная почта пользователя
        name - Имя пользователя
        phone - Номер мобильного телефона пользователя
    hairdresser
        id - ID парикмахера
        name - Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    department
        id - ID отделения
        address - Адрес отделения
        name - Название отделения
```

_Пример ответа_

```json
{
  "reception": {
    "id": 1,
    "year": 2022,
    "month": 3,
    "day": 2,
    "day_time": 1200,
    "services": [
      {
        "id": 5,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "customer": {
      "id": 1,
      "email": "customer_email@gmail.com",
      "name": "Марочкин Даниил",
      "phone": "+1 (222) 333-44-55"
    },
    "hairdresser": {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    },
    "department": {
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
      "id": 1,
      "name": "Hair HaHair"
    }
  }
}
```

### DELETE /customer.reception

Удаляет запись на прием.

_Параметры запроса_

```text
id - ID записи
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /customer.administrator

Возвращает информацию об администраторе.

_Параметры запроса_

```text
id - ID администратора
```

`id не является обязательным параметром`

_Пример запроса_

```text
*domain*/customer.administrator
```

```text
*domain*/customer.administrator?id=1
```

_Структура ответа_

```text
administrator - Администратор (или administrators - список администраторов)
    id - ID администратора
    name - Фамилия Имя администратора
    phone - Номер мобильного телефона администратора
```

_Примеры ответа_

`Если id передан данные находятся в поле administrator`

`Если id не передан данные находятся в поле administrators`

```json
{
  "administrator": {
    "id": 1,
    "name": "Сманцырева Вероника",
    "phone": "+1 (222) 333-44-77"
  }
}
```

```json
{
  "administrators": [
    {
      "id": 1,
      "name": "Сманцырева Вероника",
      "phone": "+1 (222) 333-44-77"
    }
  ]
}
```

### GET /customer.hairdresser

Возвращает информацию о парикмахере.

_Параметры запроса_

```text
id - ID парикмахера
```

`id не является обязательным параметром`

_Пример запроса_

```text
*domain*/customer.hairdresser
```

```text
*domain*/customer.hairdresser?id=1
```

_Структура ответа_

```text
hairdresser - Парикмахер(или hairdressers - список парикмахеров)
    id - ID парикмахера
    name - Фамилия Имя парикмахера
    phone - Номер мобильного телефона парикмахера
```

_Пример ответа_

`Если id передан данные находятся в поле hairdresser`

`Если id не передан данные находятся в поле hairdressers`

```json
{
  "hairdresser": {
    "id": 1,
    "name": "Икоева Лаура",
    "phone": "+1 (222) 333-44-66"
  }
}
```

```json
{
  "hairdressers": [
    {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    }
  ]
}
```

### GET /customer.department

Возвращает информацию об отделении.

_Параметры запроса_

```text
id - ID отделения
day - День работы
```

`Запрос может включать не все параметры`

`Day передается только совместно с id`

_Пример запроса_

```text
*domain*/customer.department
```

```text
*domain*/customer.department?id=1
```

```text
*domain*/customer.department?id=1&day=1
```

_Структура ответа_

```text
department - Отделение(или departments - список отделений)
    id - ID отделения
    address - Адрес отделения
    name - Название отделения
```

_Примеры ответа_

`Если id передан данные находятся в поле department`

`Если id не передан данные находятся в поле departments`

```json
{
  "departments": [
    {
      "id": 1,
      "name": "Hair Styler",
      "services": [
        {
          "id": 1,
          "name": "Обрезание концов",
          "price": 1000,
          "duration": 15
        }
      ],
      "hairdressers": [
        {
          "id": 1,
          "name": "Икоева Лаура",
          "phone": "+1 (222) 333-44-66"
        }
      ],
      "administrators": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ],
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186"
    }
  ]
}
```

`Следующий ответ не имеет в запросе day`

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186"
  },
  "schedule": [
    {
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400
    },
    {
      "day": 2,
      "start_day_time": 750,
      "end_day_time": 1200
    }
  ],
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    },
    {
      "id": 2,
      "day": 2,
      "start_day_time": 750,
      "end_day_time": 1200,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

`Следующий ответ имеет в запросе day`

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186"
  },
  "schedule": [
    {
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400
    }
  ],
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

### GET /administrator

Возвращает администратору его информацию.

_Параметры запроса_

```text
Не принимает параметры
```

_Пример запроса_

```text
*domain*/administrator
```

_Структура ответа_

```text
id - ID администратора
name - Фамилия Имя администратора
phone - Номер мобильного телефона администратора
```

_Пример ответа_

```json
{
  "id": 1,
  "name": "Сманцырева Вероника",
  "phone": "+1 (222) 333-44-77"
}
```

### POST /administrator.authorization

Авторизует администратора. Создает сессию и передает ее в cookies.

_Параметры запроса_

```text
phone - Номер мобильного телефона
password - Пароль
```

_Пример запроса_

```json
{
  "phone": "+1 (222) 333-44-77",
  "password": "zUWhuLbJdUMkyMeS"
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /administrator.customer

Возвращает информацию о пользователе.

_Параметры запроса_

```text
id - ID пользователя
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/administrator.customer
```

```text
*domain*/administrator.customer?id=1
```

_Структура ответа_

```text
customer - Пользователь(или hairdressers - Список пользователей)
        id - ID пользователя
        email - Электронная почта пользователя
        name - Фамилия Имя пользователя
        phone - Номер мобильного телефона пользователя
````

_Примеры ответа_

`Если id передан данные находятся в поле customer`

`Если id не передан данные находятся в поле customers`

```json
{
  "customer": {
    "id": 1,
    "email": "customer_email@gmail.com",
    "name": "Марочкин Даниил",
    "phone": "+1 (222) 333-44-55"
  }
}
```

```json
{
  "customers": [
    {
      "id": 1,
      "email": "customer_email@gmail.com",
      "name": "Марочкин Даниил",
      "phone": "+1 (222) 333-44-55"
    }
  ]
}
```

### GET /administrator.hairdresser

Возвращает информацию о парикмахере.

_Параметры запроса_

```text
id - ID парикмахера
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/administrator.hairdresser
```

```text
*domain*/administrator.hairdresser?id=1
```

_Структура ответа_

```text
hairdresser - Парикмахер(или hairdressers - Список парикмахеров)
    id - ID парикмахера
    name - Фамилия Имя парикмахера
    phone - Номер мобильного телефона парикмахера
````

_Примеры ответа_

`Если id передан данные находятся в поле hairdresser`

`Если id не передан данные находятся в поле hairdressers`

```json
{
  "hairdresser": {
    "id": 1,
    "name": "Икоева Лаура",
    "phone": "+1 (222) 333-44-66"
  }
}
```

```json
{
  "hairdressers": [
    {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    }
  ]
}
```

### GET /administrator.department

Возвращает информацию об отделении.

_Параметры запроса_

```text
id - ID отделения
day - День работы
```

`Запрос может включать не все параметры`

`Day передается только совместно с id`

_Пример запроса_

```text
*domain*/administrator.department
```

```text
*domain*/administrator.department?id=1
```

```text
*domain*/administrator.department?id=1&day=1
```

_Структура ответа_

```text
department - Отделение(или departments - список отделений)
    id - ID отделения
    address - Адрес отделения
    name - Название отделения
    services - Список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    administrators- Список администраторов
        id - ID администратора
        name - Фамилия Имя администратора
        phone - Номер мобильного телефона администратора

(При указании id)
schedule - Расписание работы
    start_day_time - Время начала в минутах с начала дня
    end_day_time - Время завершения в минутах с начала дня
    day - День к которому относится данный отрезок
shifts
    id - ID смены
    start_day_time - Время начала в минутах с начала дня
    end_day_time - Время завершения в минутах с начала дня
    day - День смены
    hairdressers - Список парикмахеров смены
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Примеры ответа_

`Если id передан данные находятся в поле department`

`Если id не передан данные находятся в поле departments`

```json
{
  "departments": [
    {
      "id": 1,
      "name": "Hair Styler",
      "services": [
        {
          "id": 1,
          "name": "Обрезание концов",
          "price": 1000,
          "duration": 15
        }
      ],
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
      "hairdressers": [
        {
          "id": 1,
          "name": "Икоева Лаура",
          "phone": "+1 (222) 333-44-66"
        }
      ],
      "administrators": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

`Следующий ответ не имеет в запросе day`

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ]
  },
  "schedule": [
    {
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400
    },
    {
      "day": 2,
      "start_day_time": 750,
      "end_day_time": 1200
    }
  ],
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    },
    {
      "id": 2,
      "day": 2,
      "start_day_time": 750,
      "end_day_time": 1200,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

`Следующий ответ имеет в запросе day`

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ]
  },
  "schedule": [
    {
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400
    }
  ],
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

### POST /administrator.department

Редактирует некоторые данные отделения

_Параметры запроса_

```text
id - ID отделения
new_hairdressers - Новый список парикмахеров
new_services - Новый список оказываемых услуг
```

`new_hairdressers не является обязательным параметром`

`new_services не является обязательным параметром`

_Примеры запроса_

```json
{
  "id": 1,
  "new_hairdressers": [
    1,
    2,
    3
  ],
  "new_services": [
    1,
    2
  ]
}
```

```json
{
  "id": 1,
  "new_hairdressers": [
    1,
    2,
    3
  ]
}
```

```json
{
  "id": 1,
  "new_services": [
    1,
    2
  ]
}
```

_Структура ответа_

```text
department - Отделение
    id - ID отделения
    address - Адрес отделения
    name - Название отделения
    services - Список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    administrators- Список администраторов
        id - ID администратора
        name - Фамилия Имя администратора
        phone - Номер мобильного телефона администратора
```

_Пример ответа_

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ]
  }
}
```

### GET /administrator.administrator

Возвращает информацию об администраторе.

_Параметры запроса_

```text
id - ID администратора
```

`id не является обязательным параметром`

_Пример запроса_

```text
*domain*/administrator.administrator
```

```text
*domain*/administrator.administrator?id=1
```

_Структура ответа_

```text
administrator - Администратор (или administrators - список администраторов)
    id - ID администратора
    name - Фамилия Имя администратора
    phone - Номер мобильного телефона администратора
```

_Примеры ответа_

`Если id передан данные находятся в поле administrator`

`Если id не передан данные находятся в поле administrators`

```json
{
  "administrator": {
    "id": 1,
    "name": "Сманцырева Вероника",
    "phone": "+1 (222) 333-44-77"
  }
}
```

```json
{
  "administrators": [
    {
      "id": 1,
      "name": "Сманцырева Вероника",
      "phone": "+1 (222) 333-44-77"
    }
  ]
}
```

### GET /administrator.service

Возвращает информацию об услуге.

_Параметры запроса_

```text
id - ID услуги
```

`id не является обязательным параметром`

_Пример запроса_

```text
*domain*/administrator.service
```

```text
*domain*/administrator.service?id=1
```

_Структура ответа_

```text
service - Услуга (или services - список услуг)
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
```

_Примеры ответа_

`Если id передан данные находятся в поле service`

`Если id не передан данные находятся в поле services`

```json
{
  "services": [
    {
      "id": 1,
      "name": "Обрезание концов",
      "price": 1000,
      "duration": 15
    }
  ]
}
```

```json
{
  "service": {
    "id": 1,
    "name": "Обрезание концов",
    "price": 1000,
    "duration": 15
  }
}
```

### GET /administrator.reception

Возвращает список записей пользователей.

_Параметры запроса_

```text
id - ID записи
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/administrator.reception
```

```text
*domain*/administrator.reception?id=1
```

_Структура ответа_

```text
reception - запись(или receptions - список записей)
    id - ID записи
    day - День записи
    month - Месяц записи
    year - Год записи
    day_time - время записи в минутах с начала дня
    services - список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время предоставления услуги
    customer - Пользователь
        id - ID пользователя
        email - Электронная почта пользователя
        name - Фамилия Имя пользователя
        phone - Номер мобильного телефона пользователя
    hairdresser - Парикмахер
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    department - Отделение
        id - ID отделения
        address - Адрес отделения
        name - Название отделения    
```

_Примеры ответа_

`Если id передан данные находятся в поле reception`

`Если id не передан данные находятся в поле receptions`

```json
{
  "receptions": []
}
```

```json
{
  "receptions": [
    {
      "id": 31,
      "day": 1,
      "month": 3,
      "year": 2022,
      "day_time": 720,
      "services": [
        {
          "id": 1,
          "name": "Модельная стрижка",
          "price": 750,
          "duration": 45
        }
      ],
      "customer": {
        "id": 1,
        "email": "customer_email@gmail.com",
        "name": "Марочкин Даниил",
        "phone": "+1 (222) 333-44-55"
      },
      "hairdresser": {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      },
      "department": {
        "id": 1,
        "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
        "name": "СПбГУПТД на БМ"
      }
    }
  ]
}
```

```json
{
  "reception": {
    "id": 31,
    "day": 1,
    "month": 3,
    "year": 2022,
    "day_time": 720,
    "services": [
      {
        "id": 1,
        "name": "Модельная стрижка",
        "price": 750,
        "duration": 45
      }
    ],
    "customer": {
      "id": 1,
      "email": "customer_email@gmail.com",
      "name": "Марочкин Даниил",
      "phone": "+1 (222) 333-44-55"
    },
    "hairdresser": {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    },
    "department": {
      "id": 1,
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
      "name": "СПбГУПТД на БМ"
    }
  }
}
```

### DELETE /administrator.reception

Удаляет запись на прием.

_Параметры запроса_

```text
id - ID записи
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /administrator.shift

Возвращает список смен.

_Параметры запроса_

```text
id - ID смены
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/administrator.shift
```

```text
*domain*/administrator.shift?id=1
```

_Структура ответа_

```text
shift - запись(или shifts - список записей)
    id - ID записи
    day - День записи
    start_day_time - время начала смены в минутах от начала дня
    end_day_time - время конца смены в минутах от начала дня
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Примеры ответа_

`Если id передан данные находятся в поле shift`

`Если id не передан данные находятся в поле shifts`

```json
{
  "shifts": []
}
```

```json
{
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 720,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Икоева Лаура",
          "phone": "+1 (222) 333-44-66"
        }
      ]
    }
  ]
}
```

```json
{
  "shift": {
    "id": 1,
    "day": 1,
    "start_day_time": 720,
    "end_day_time": 1400,
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ]
  }
}
```

### POST /administrator.shift

Изменяет смену.

_Параметры запроса_

```text
id - ID смены
new_start_day_time - Новое время начала смены в минутах с начала дня
new_end_day_time - Новое время конца смены в минутах с начала дня
new_day - Новый день недели смены
new_hairdressers - Новый список парикмахеров
```

`new_start_day_time не является обязательным параметром`

`new_end_day_time не является обязательным параметром`

`new_day не является обязательным параметром`

`new_hairdressers не является обязательным параметром`

_Примеры запроса_

```json
{
  "id": 1,
  "new_start_day_time": 1,
  "new_end_day_time": 1000,
  "new_day": 1,
  "new_hairdressers": [
    1,
    2
  ]
}
```

```json
{
  "id": 1,
  "new_hairdressers": [
    1,
    2
  ]
}
```

_Структура ответа_

```text
shift - запись
    id - ID записи
    day - День записи
    start_day_time - время начала смены в минутах от начала дня
    end_day_time - время конца смены в минутах от начала дня
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Пример ответа_

```json
{
  "shift": {
    "id": 1,
    "day": 1,
    "start_day_time": 720,
    "end_day_time": 1400,
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ]
  }
}
```

### PUT /administrator.shift

Создает новую смену.

_Параметры запроса_

```text
department - ID отделения парикмахерской
hairdressers - Список ID парикмахеров
day - день записи
start_day_time - время начала смены в минутах от начала дня
end_day_time - время конца смены в минутах от начала дня
```

_Пример запроса_

```json
{
  "department": 1,
  "start_day_time": 700,
  "end_day_time": 1400,
  "day": 1,
  "hairdressers": [
    1,
    2
  ]
}
```

_Структура ответа_

```text
shift - запись
    id - ID записи
    day - День записи
    start_day_time - время начала смены в минутах от начала дня
    end_day_time - время конца смены в минутах от начала дня
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Пример ответа_

```json
{
  "shift": {
    "id": 1,
    "day": 1,
    "start_day_time": 720,
    "end_day_time": 1400,
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ]
  }
}
```

### DELETE /administrator.shift

Удаляет смену.

_Параметры запроса_

```text
id - ID смены
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /administrator.session

Возвращает список сессий.

_Параметры запроса_

```text
Не принимает параметры
```

_Пример запроса_

```text
*domain*/administrator.session
```

_Структура ответа_

```text
sessions - Список сессий 
    id - ID сессии
    user_type - Тип пользователя
    user_id - ID пользователя
    die_time - Время жизни сессии
```

_Пример ответа_

```json
{
  "sessions": [
    {
      "id": 1,
      "user_type": "Customer",
      "user_id": 1,
      "die_time": 1646769892
    },
    {
      "id": 2,
      "user_type": "Hairdresser",
      "user_id": 0,
      "die_time": 1647163748
    }
  ]
}
```

### DELETE /administrator.session

Удаляет сессию.

_Параметры запроса_

```text
id - ID сессии
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /organization

Возвращает организации ее информацию.

_Параметры запроса_

```text
Не принимает параметры
```

_Пример запроса_

```text
*domain*/organization
```

_Структура ответа_

```text
name - Название организации
email - Электронная почта организации
```

_Пример ответа_

```json
{
  "name": "Hair Super Style",
  "email": "organization_mail@example.com"
}
```

### GET /organization.customer

Возвращает информацию о пользователе.

_Параметры запроса_

```text
id - ID пользователя
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/organization.customer
```

```text
*domain*/organization.customer?id=1
```

_Структура ответа_

```text
customer - Пользователь(или hairdressers - Список пользователей)
        id - ID пользователя
        email - Электронная почта пользователя
        name - Фамилия Имя пользователя
        phone - Номер мобильного телефона пользователя
````

_Примеры ответа_

`Если id передан данные находятся в поле customer`

`Если id не передан данные находятся в поле customers`

```json
{
  "customer": {
    "id": 1,
    "email": "customer_email@gmail.com",
    "name": "Марочкин Даниил",
    "phone": "+1 (222) 333-44-55"
  }
}
```

```json
{
  "customers": [
    {
      "id": 1,
      "email": "customer_email@gmail.com",
      "name": "Марочкин Даниил",
      "phone": "+1 (222) 333-44-55"
    }
  ]
}
```

### POST /organization.authorization

Авторизует организацию. Создает сессию и передает ее в cookies.

_Параметры запроса_

```text
email - Адрес электронной почты
password - Пароль
```

_Пример запроса_

```json
{
  "email": "organization_mail@example.com",
  "password": "heSzUbJdLyMuWUMk"
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /organization.hairdresser

Возвращает информацию о парикмахере.

_Параметры запроса_

```text
id - ID парикмахера
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/organization.hairdresser
```

```text
*domain*/organization.hairdresser?id=1
```

_Структура ответа_

```text
hairdresser - Парикмахер(или hairdressers - Список парикмахеров)
    id - ID парикмахера
    name - Фамилия Имя парикмахера
    phone - Номер мобильного телефона парикмахера
````

_Примеры ответа_

`Если id передан данные находятся в поле hairdresser`

`Если id не передан данные находятся в поле hairdressers`

```json
{
  "hairdresser": {
    "id": 1,
    "name": "Икоева Лаура",
    "phone": "+1 (222) 333-44-66"
  }
}
```

```json
{
  "hairdressers": [
    {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    }
  ]
}
```

### POST /organization.hairdresser

Изменяет данные парикмахера.

_Параметры запроса_

```text
id - ID смены
new_name - Новые Фамилия и Имя парикмахера
new_phone - Новый номер мобильного телефона парикмахера
new_password - Новый пароль парикмахера
```

`new_name не является обязательным параметром`

`new_phone не является обязательным параметром`

`new_password не является обязательным параметром`

_Примеры запроса_

```json
{
  "id": 1,
  "new_name": "Насир Махмуд",
  "new_phone": "+1 (222) 333-44-88",
  "new_password": "yMbJkeSzUdhMuUWL"
}
```

```json
{
  "id": 1,
  "new_name": "Насир Махмуд"
}
```

_Структура ответа_

```text
hairdresser - Парикмахер
    id - ID парикмахера
    name - Фамилия Имя парикмахера
    phone - Номер мобильного телефона парикмахера
```

_Пример ответа_

```json
{
  "hairdresser": {
    "id": 1,
    "name": "Насир Махмуд",
    "phone": "+1 (222) 333-44-88"
  }
}
```

### PUT /organization.hairdresser

Создает аккаунт нового парикмахера.
_Параметры запроса_

```text
name - Фамилия Имя парикмахера
phone - Номер мобильного телефона парикмахера
password - Пароль парикмахера
```

_Примеры запроса_

```json
{
  "name": "Насир Махмуд",
  "phone": "+1 (222) 333-44-88",
  "password": "yMbJkeSzUdhMuUWL"
}
```

_Структура ответа_

```text
hairdresser - Парикмахер
    id - ID парикмахера
    name - Фамилия Имя парикмахера
    phone - Номер мобильного телефона парикмахера
```

_Пример ответа_

```json
{
  "hairdresser": {
    "id": 1,
    "name": "Насир Махмуд",
    "phone": "+1 (222) 333-44-88"
  }
}
```

### DELETE /organization.hairdresser

Удаляет аккаунт парикмахера.

_Параметры запроса_

```text
id - ID парикмахера
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /organization.administrator

Возвращает информацию об администраторе.

_Параметры запроса_

```text
id - ID администратора
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/organization.administrator
```

```text
*domain*/organization.administrator?id=1
```

_Структура ответа_

```text
administrator - Администратор(или administrators - Список администраторов)
    id - ID администратора
    name - Фамилия Имя администратора
    phone - Номер мобильного телефона администратора
````

_Примеры ответа_

`Если id передан данные находятся в поле administrator`

`Если id не передан данные находятся в поле administrators`

```json
{
  "administrator": {
    "id": 1,
    "name": "Сманцырева Вероника",
    "phone": "+1 (222) 333-44-77"
  }
}
```

```json
{
  "hairdressers": [
    {
      "id": 1,
      "name": "Сманцырева Вероника",
      "phone": "+1 (222) 333-44-77"
    }
  ]
}
```

### POST /organization.administrator

Изменяет данные администратора.

_Параметры запроса_

```text
id - ID смены
new_name - Новые Фамилия и Имя администратора
new_phone - Новый номер мобильного телефона администратора
new_password - Новый пароль администратора
```

`new_name не является обязательным параметром`

`new_phone не является обязательным параметром`

`new_password не является обязательным параметром`

_Примеры запроса_

```json
{
  "id": 1,
  "new_name": "Шестаков Семен",
  "new_phone": "+1 (222) 333-44-99",
  "new_password": "eSzyMbUdLJhMuUWk"
}
```

```json
{
  "id": 1,
  "new_name": "Шестаков Семен"
}
```

_Структура ответа_

```text
administrator - Администратор
    id - ID администратора
    name - Фамилия Имя администратора
    phone - Номер мобильного телефона администратора
```

_Пример ответа_

```json
{
  "administrator": {
    "id": 1,
    "name": "Шестаков Семен",
    "phone": "+1 (222) 333-44-99"
  }
}
```

### PUT /organization.administrator

Создает аккаунт нового администратора.

_Параметры запроса_

```text
name - Фамилия Имя администратора
phone - Номер мобильного телефона администратора
password - Пароль администратора
```

_Примеры запроса_

```json
{
  "name": "Сманцырева Вероника",
  "phone": "+1 (222) 333-44-77",
  "password": "yMbJkeSzUdhMuUWL"
}

```

_Структура ответа_

```text
administrator - Администратор
    id - ID администратора
    name - Фамилия Имя администратора
    phone - Номер мобильного телефона администратора
```

_Пример ответа_

```json
{
  "administrator": {
    "id": 1,
    "name": "Сманцырева Вероника",
    "phone": "+1 (222) 333-44-77"
  }
}
```

### DELETE /organization.administrator

Удаляет аккаунт администратора.

_Параметры запроса_

```text
id - ID администратора
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /organization.department

Возвращает информацию об отделении.

_Параметры запроса_

```text
id - ID отделения
day - День работы
```

`Запрос может включать не все параметры`

`Day передается только совместно с id`

_Пример запроса_

```text
*domain*/organization.department
```

```text
*domain*/organization.department?id=1
```

```text
*domain*/organization.department?id=1&day=1
```

_Структура ответа_

```text
department - Отделение(или departments - список отделений)
    id - ID отделения
    address - Адрес отделения
    name - Название отделения
    services - Список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    administrators- Список администраторов
        id - ID администратора
        name - Фамилия Имя администратора
        phone - Номер мобильного телефона администратора

(При указании id)
schedule - Расписание работы
    start_day_time - Время начала в минутах с начала дня
    end_day_time - Время завершения в минутах с начала дня
    day - День к которому относится данный отрезок
shifts
    id - ID смены
    start_day_time - Время начала в минутах с начала дня
    end_day_time - Время завершения в минутах с начала дня
    day - День смены
    hairdressers - Список парикмахеров смены
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Примеры ответа_

`Если id передан данные находятся в поле department`

`Если id не передан данные находятся в поле departments`

```json
{
  "departments": [
    {
      "id": 1,
      "name": "Hair Styler",
      "services": [
        {
          "id": 1,
          "name": "Обрезание концов",
          "price": 1000,
          "duration": 15
        }
      ],
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
      "hairdressers": [
        {
          "id": 1,
          "name": "Икоева Лаура",
          "phone": "+1 (222) 333-44-66"
        }
      ],
      "administrators": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

`Следующий ответ не имеет в запросе day`

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ]
  },
  "schedule": [
    {
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400
    },
    {
      "day": 2,
      "start_day_time": 750,
      "end_day_time": 1200
    }
  ],
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    },
    {
      "id": 2,
      "day": 2,
      "start_day_time": 750,
      "end_day_time": 1200,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

`Следующий ответ имеет в запросе day`

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ]
  },
  "schedule": [
    {
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400
    }
  ],
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

### POST /organization.department

Редактирует данные отделения.

_Параметры запроса_

```text
id - ID отделения
new_name - Новое название
new_address - Новый адрес
new_administrators - Новый список администраторов
new_hairdressers - Новый список парикмахеров
new_services - Новый список оказываемых услуг
```

`new_name не является обязательным параметром`

`new_address не является обязательным параметром`

`new_administrators не является обязательным параметром`

`new_hairdressers не является обязательным параметром`

`new_services не является обязательным параметром`

_Примеры запроса_

```json
{
  "id": 1,
  "new_name": "Быстро-резка",
  "new_address": "Вознесенский пр., 46, Санкт-Петербург, 190068",
  "new_administrators": [
    1,
    2,
    3
  ],
  "new_hairdressers": [
    1,
    2,
    3
  ],
  "new_services": [
    1,
    2
  ]
}
```

```json
{
  "id": 1,
  "new_services": [
    1,
    2
  ]
}
```

_Структура ответа_

```text
department - Отделение
    id - ID отделения
    address - Адрес отделения
    name - Название отделения
    services - Список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    administrators- Список администраторов
        id - ID администратора
        name - Фамилия Имя администратора
        phone - Номер мобильного телефона администратора
```

_Пример ответа_

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "address": "Вознесенский пр., 46, Санкт-Петербург, 190068",
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ]
  }
}
```

### PUT /organization.department

Создает новое отделение.

_Параметры запроса_

```text
name - Новое название
address - Новый адрес
administrators - Новый список администраторов
hairdressers - Новый список парикмахеров
services - Новый список оказываемых услуг
```

_Пример запроса_

```json
{
  "name": "Быстро-резка",
  "address": "Вознесенский пр., 46, Санкт-Петербург, 190068",
  "administrators": [
    1,
    2,
    3
  ],
  "hairdressers": [
    1,
    2,
    3
  ],
  "services": [
    1,
    2
  ]
}
```

_Структура ответа_

```text
department - Отделение
    id - ID отделения
    address - Адрес отделения
    name - Название отделения
    services - Список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    administrators- Список администраторов
        id - ID администратора
        name - Фамилия Имя администратора
        phone - Номер мобильного телефона администратора
```

_Пример ответа_

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "address": "Вознесенский пр., 46, Санкт-Петербург, 190068",
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ]
  }
}
```

### DELETE /organization.department

Удаляет отделение.

_Параметры запроса_

```text
id - ID отделения
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /organization.service

Возвращает информацию об услуге.

_Параметры запроса_

```text
id - ID услуги
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/organization.service
```

```text
*domain*/organization.service?id=1
```

_Структура ответа_

```text
service - Услуга (или services - список услуг)
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
````

_Примеры ответа_

`Если id передан данные находятся в поле service`

`Если id не передан данные находятся в поле services`

```json
{
  "services": [
    {
      "id": 1,
      "name": "Обрезание концов",
      "price": 1000,
      "duration": 15
    }
  ]
}
```

```json
{
  "service": {
    "id": 1,
    "name": "Обрезание концов",
    "price": 1000,
    "duration": 15
  }
}
```

### POST /organization.service

Изменяет данные услуги.

_Параметры запроса_

```text
id - ID услуги
new_name - Новое название услуги
new_price - Новая цена услуги
new_duration - Новое время на оказание услуги
```

`new_name не является обязательным параметром`

`new_price не является обязательным параметром`

`new_duration не является обязательным параметром`

_Примеры запроса_

```json
{
  "id": 1,
  "new_name": "Мелирование",
  "new_price": 1200,
  "new_duration": 75
}
```

```json
{
  "id": 1,
  "new_duration": 10
}
```

_Структура ответа_

```text
service - Услуга
    id - ID услуги
    name - Название услуги
    price - Цена услуги
    duration - Время на оказание услуги
```

_Пример ответа_

```json
{
  "service": {
    "id": 1,
    "name": "Мелирование",
    "price": 1200,
    "duration": 75
  }
}
```

### PUT /organization.service

Создает новую услугу.

_Параметры запроса_

```text
name - Фамилия Имя администратора
phone - Номер мобильного телефона администратора
password - Пароль администратора
```

_Примеры запроса_

```json
{
  "name": "Мелирование",
  "price": 1200,
  "duration": 75
}

```

_Структура ответа_

```text
service - Услуга
    id - ID услуги
    name - Название услуги
    price - Цена услуги
    duration - Время на оказание услуги
```

_Пример ответа_

```json
{
  "service": {
    "id": 1,
    "name": "Мелирование",
    "price": 1200,
    "duration": 75
  }
}
```

### DELETE /organization.service

Удаляет услугу.

_Параметры запроса_

```text
id - ID услуги
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /organization.reception

Возвращает список записей пользователей.

_Параметры запроса_

```text
id - ID записи
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/organization.reception
```

```text
*domain*/organization.reception?id=1
```

_Структура ответа_

```text
reception - запись(или receptions - список записей)
    id - ID записи
    day - День записи
    month - Месяц записи
    year - Год записи
    day_time - время записи в минутах с начала дня
    services - список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время предоставления услуги
    customer - Пользователь
        id - ID пользователя
        email - Электронная почта пользователя
        name - Фамилия Имя пользователя
        phone - Номер мобильного телефона пользователя
    hairdresser - Парикмахер
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    department - Отделение
        id - ID отделения
        address - Адрес отделения
        name - Название отделения    
```

_Примеры ответа_

`Если id передан данные находятся в поле reception`

`Если id не передан данные находятся в поле receptions`

```json
{
  "receptions": []
}
```

```json
{
  "receptions": [
    {
      "id": 31,
      "day": 1,
      "month": 3,
      "year": 2022,
      "day_time": 720,
      "services": [
        {
          "id": 1,
          "name": "Модельная стрижка",
          "price": 750,
          "duration": 45
        }
      ],
      "customer": {
        "id": 1,
        "email": "customer_email@gmail.com",
        "name": "Марочкин Даниил",
        "phone": "+1 (222) 333-44-55"
      },
      "hairdresser": {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      },
      "department": {
        "id": 1,
        "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
        "name": "СПбГУПТД на БМ"
      }
    }
  ]
}
```

```json
{
  "reception": {
    "id": 31,
    "day": 1,
    "month": 3,
    "year": 2022,
    "day_time": 720,
    "services": [
      {
        "id": 1,
        "name": "Модельная стрижка",
        "price": 750,
        "duration": 45
      }
    ],
    "customer": {
      "id": 1,
      "email": "customer_email@gmail.com",
      "name": "Марочкин Даниил",
      "phone": "+1 (222) 333-44-55"
    },
    "hairdresser": {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    },
    "department": {
      "id": 1,
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
      "name": "СПбГУПТД на БМ"
    }
  }
}
```

### DELETE /organization.reception

Удаляет запись на прием.

_Параметры запроса_

```text
id - ID записи
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /organization.shift

Возвращает список смен.

_Параметры запроса_

```text
id - ID смены
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/organization.shift
```

```text
*domain*/organization.shift?id=1
```

_Структура ответа_

```text
shift - запись(или shifts - список записей)
    id - ID записи
    day - День записи
    start_day_time - время начала смены в минутах от начала дня
    end_day_time - время конца смены в минутах от начала дня
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Примеры ответа_

`Если id передан данные находятся в поле shift`

`Если id не передан данные находятся в поле shifts`

```json
{
  "shifts": []
}
```

```json
{
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 720,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Икоева Лаура",
          "phone": "+1 (222) 333-44-66"
        }
      ]
    }
  ]
}
```

```json
{
  "shift": {
    "id": 1,
    "day": 1,
    "start_day_time": 720,
    "end_day_time": 1400,
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ]
  }
}
```

### POST /organization.shift

Изменяет смену.

_Параметры запроса_

```text
id - ID смены
new_start_day_time - Новое время начала смены в минутах с начала дня
new_end_day_time - Новое время конца смены в минутах с начала дня
new_day - Новый день недели смены
new_hairdressers - Новый список парикмахеров
```

`new_start_day_time не является обязательным параметром`

`new_end_day_time не является обязательным параметром`

`new_day не является обязательным параметром`

`new_hairdressers не является обязательным параметром`

_Примеры запроса_

```json
{
  "id": 1,
  "new_start_day_time": 1,
  "new_end_day_time": 1000,
  "new_day": 1,
  "new_hairdressers": [
    1,
    2
  ]
}
```

```json
{
  "id": 1,
  "new_hairdressers": [
    1,
    2
  ]
}
```

_Структура ответа_

```text
shift - запись
    id - ID записи
    day - День записи
    start_day_time - время начала смены в минутах от начала дня
    end_day_time - время конца смены в минутах от начала дня
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Пример ответа_

```json
{
  "shift": {
    "id": 1,
    "day": 1,
    "start_day_time": 720,
    "end_day_time": 1400,
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ]
  }
}
```

### PUT /organization.shift

Создает новую смену.

_Параметры запроса_

```text
department - ID отделения парикмахерской
hairdressers - Список ID парикмахеров
day - день записи
start_day_time - время начала смены в минутах от начала дня
end_day_time - время конца смены в минутах от начала дня
```

_Пример запроса_

```json
{
  "department": 1,
  "start_day_time": 700,
  "end_day_time": 1400,
  "day": 1,
  "hairdressers": [
    1,
    2
  ]
}
```

_Структура ответа_

```text
shift - запись
    id - ID записи
    day - День записи
    start_day_time - время начала смены в минутах от начала дня
    end_day_time - время конца смены в минутах от начала дня
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Пример ответа_

```json
{
  "shift": {
    "id": 1,
    "day": 1,
    "start_day_time": 720,
    "end_day_time": 1400,
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ]
  }
}
```

### DELETE /organization.shift

Удаляет смену.

_Параметры запроса_

```text
id - ID смены
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /organization.session

Возвращает список сессий.

_Параметры запроса_

```text
Не принимает параметры
```

_Пример запроса_

```text
*domain*/administrator.session
```

_Структура ответа_

```text
sessions - Список сессий 
    id - ID сессии
    user_type - Тип пользователя
    user_id - ID пользователя
    die_time - Время жизни сессии
```

_Пример ответа_

```json
{
  "sessions": [
    {
      "id": 1,
      "user_type": "Customer",
      "user_id": 1,
      "die_time": 1646769892
    },
    {
      "id": 2,
      "user_type": "Hairdresser",
      "user_id": 0,
      "die_time": 1647163748
    }
  ]
}
```

### DELETE /organization.session

Удаляет сессию.

_Параметры запроса_

```text
id - ID сессии
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /hairdresser

Возвращает парикмахеру его информацию.

_Параметры запроса_

```text
Не принимает параметры
```

_Пример запроса_

```text
*domain*/hairdresser
```

_Структура ответа_

```text
id - ID парикмахера
name - Фамилия Имя парикмахера
phone - Номер мобильного телефона парикмахера
```

_Пример ответа_

```json
{
  "id": 1,
  "name": "Икоева Лаура",
  "phone": "+1 (222) 333-44-66"
}
```

### POST /hairdresser.authorization

Авторизует парикмахера. Создает сессию и передает ее в cookies.

_Параметры запроса_

```text
phone - Номер мобильного телефона
password - Пароль
```

_Пример запроса_

```json
{
  "phone": "+1 (222) 333-44-66",
  "password": "LbJdUzUWMkyMeShu"
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /hairdresser.administrator

Возвращает информацию об администраторе.

_Параметры запроса_

```text
id - ID администратора
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/hairdresser.administrator
```

```text
*domain*/hairdresser.administrator?id=1
```

_Структура ответа_

```text
administrator - Администратор(или administrators - Список администраторов)
    id - ID администратора
    name - Фамилия Имя администратора
    phone - Номер мобильного телефона администратора
````

_Примеры ответа_

`Если id передан данные находятся в поле administrator`

`Если id не передан данные находятся в поле administrators`

```json
{
  "administrator": {
    "id": 1,
    "name": "Сманцырева Вероника",
    "phone": "+1 (222) 333-44-77"
  }
}
```

```json
{
  "hairdressers": [
    {
      "id": 1,
      "name": "Сманцырева Вероника",
      "phone": "+1 (222) 333-44-77"
    }
  ]
}
```

### GET /hairdresser.hairdresser

Возвращает информацию о парикмахере.

_Параметры запроса_

```text
id - ID парикмахера
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/hairdresser.hairdresser
```

```text
*domain*/hairdresser.hairdresser?id=1
```

_Структура ответа_

```text
hairdresser - Парикмахер(или hairdressers - Список парикмахеров)
    id - ID парикмахера
    name - Фамилия Имя парикмахера
    phone - Номер мобильного телефона парикмахера
````

_Примеры ответа_

`Если id передан данные находятся в поле hairdresser`

`Если id не передан данные находятся в поле hairdressers`

```json
{
  "hairdresser": {
    "id": 1,
    "name": "Икоева Лаура",
    "phone": "+1 (222) 333-44-66"
  }
}
```

```json
{
  "hairdressers": [
    {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    }
  ]
}
```

### GET /hairdresser.customer

Возвращает информацию о пользователе.

_Параметры запроса_

```text
id - ID пользователя
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/hairdresser.customer
```

```text
*domain*/hairdresser.customer?id=1
```

_Структура ответа_

```text
customer - Пользователь(или hairdressers - Список пользователей)
        id - ID пользователя
        email - Электронная почта пользователя
        name - Фамилия Имя пользователя
        phone - Номер мобильного телефона пользователя
````

_Примеры ответа_

`Если id передан данные находятся в поле customer`

`Если id не передан данные находятся в поле customers`

```json
{
  "customer": {
    "id": 1,
    "email": "customer_email@gmail.com",
    "name": "Марочкин Даниил",
    "phone": "+1 (222) 333-44-55"
  }
}
```

```json
{
  "customers": [
    {
      "id": 1,
      "email": "customer_email@gmail.com",
      "name": "Марочкин Даниил",
      "phone": "+1 (222) 333-44-55"
    }
  ]
}
```

### GET /hairdresser.department

Возвращает информацию об отделении.

_Параметры запроса_

```text
id - ID отделения
day - День работы
```

`Запрос может включать не все параметры`

`Day передается только совместно с id`

_Пример запроса_

```text
*domain*/hairdresser.department
```

```text
*domain*/hairdresser.department?id=1
```

```text
*domain*/hairdresser.department?id=1&day=1
```

_Структура ответа_

```text

department - Отделение(или departments - список отделений)
    id - ID отделения
    address - Адрес отделения
    name - Название отделения
    services - Список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время на оказание услуги
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    administrators- Список администраторов
        id - ID администратора
        name - Фамилия Имя администратора
        phone - Номер мобильного телефона администратора

(При указании id)
schedule - Расписание работы
    start_day_time - Время начала в минутах с начала дня
    end_day_time - Время завершения в минутах с начала дня
    day - День к которому относится данный отрезок
shifts
    id - ID смены
    start_day_time - Время начала в минутах с начала дня
    end_day_time - Время завершения в минутах с начала дня
    day - День смены
    hairdressers - Список парикмахеров смены
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера       
```

_Примеры ответа_

`Если id передан данные находятся в поле department`

`Если id не передан данные находятся в поле departments`

```json
{
  "departments": [
    {
      "id": 1,
      "name": "Hair Styler",
      "hairdressers": [
        {
          "id": 1,
          "name": "Икоева Лаура",
          "phone": "+1 (222) 333-44-66"
        }
      ],
      "administrators": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ],
      "services": [
        {
          "id": 1,
          "name": "Обрезание концов",
          "price": 1000,
          "duration": 15
        }
      ],
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186"
    }
  ]
}
```

`Следующий ответ не имеет в запросе day`

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ],
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186"
  },
  "schedule": [
    {
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400
    },
    {
      "day": 2,
      "start_day_time": 750,
      "end_day_time": 1200
    }
  ],
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    },
    {
      "id": 2,
      "day": 2,
      "start_day_time": 750,
      "end_day_time": 1200,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

`Следующий ответ имеет в запросе day`

```json
{
  "department": {
    "id": 1,
    "name": "Hair Styler",
    "services": [
      {
        "id": 1,
        "name": "Обрезание концов",
        "price": 1000,
        "duration": 15
      }
    ],
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ],
    "administrators": [
      {
        "id": 1,
        "name": "Сманцырева Вероника",
        "phone": "+1 (222) 333-44-77"
      }
    ],
    "address": "Большая Морская ул., 18, Санкт-Петербург, 191186"
  },
  "schedule": [
    {
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400
    }
  ],
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 600,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Сманцырева Вероника",
          "phone": "+1 (222) 333-44-77"
        }
      ]
    }
  ]
}
```

### GET /hairdresser.reception

Возвращает список записей пользователей.

_Параметры запроса_

```text
id - ID записи
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/hairdresser.reception
```

```text
*domain*/hairdresser.reception?id=1
```

_Структура ответа_

```text
reception - запись(или receptions - список записей)
    id - ID записи
    day - День записи
    month - Месяц записи
    year - Год записи
    day_time - время записи в минутах с начала дня
    services - список услуг
        id - ID услуги
        name - Название услуги
        price - Цена услуги
        duration - Время предоставления услуги
    customer - Пользователь
        id - ID пользователя
        email - Электронная почта пользователя
        name - Фамилия Имя пользователя
        phone - Номер мобильного телефона пользователя
    hairdresser - Парикмахер
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
    department - Отделение
        id - ID отделения
        address - Адрес отделения
        name - Название отделения    
```

_Примеры ответа_

`Если id передан данные находятся в поле reception`

`Если id не передан данные находятся в поле receptions`

```json
{
  "receptions": []
}
```

```json
{
  "receptions": [
    {
      "id": 31,
      "day": 1,
      "month": 3,
      "year": 2022,
      "day_time": 720,
      "services": [
        {
          "id": 1,
          "name": "Модельная стрижка",
          "price": 750,
          "duration": 45
        }
      ],
      "customer": {
        "id": 1,
        "email": "customer_email@gmail.com",
        "name": "Марочкин Даниил",
        "phone": "+1 (222) 333-44-55"
      },
      "hairdresser": {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      },
      "department": {
        "id": 1,
        "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
        "name": "СПбГУПТД на БМ"
      }
    }
  ]
}
```

```json
{
  "reception": {
    "id": 31,
    "day": 1,
    "month": 3,
    "year": 2022,
    "day_time": 720,
    "services": [
      {
        "id": 1,
        "name": "Модельная стрижка",
        "price": 750,
        "duration": 45
      }
    ],
    "customer": {
      "id": 1,
      "email": "customer_email@gmail.com",
      "name": "Марочкин Даниил",
      "phone": "+1 (222) 333-44-55"
    },
    "hairdresser": {
      "id": 1,
      "name": "Икоева Лаура",
      "phone": "+1 (222) 333-44-66"
    },
    "department": {
      "id": 1,
      "address": "Большая Морская ул., 18, Санкт-Петербург, 191186",
      "name": "СПбГУПТД на БМ"
    }
  }
}
```

### DELETE /hairdresser.reception

Удаляет запись на прием.

_Параметры запроса_

```text
id - ID записи
```

_Пример запроса_

```json
{
  "id": 1
}
```

_Пример ответа_

```text
Не возвращает данные
```

### GET /hairdresser.shift

Возвращает список смен парикмахера.

_Параметры запроса_

```text
id - ID смены
```

`id не является обязательным параметром`

_Примеры запроса_

```text
*domain*/hairdresser.shift
```

```text
*domain*/hairdresser.shift?id=1
```

_Структура ответа_

```text
shift - запись(или shifts - список записей)
    id - ID записи
    day - День записи
    start_day_time - время начала смены в минутах от начала дня
    end_day_time - время конца смены в минутах от начала дня
    hairdressers - Список парикмахеров
        id - ID парикмахера
        name - Фамилия Имя парикмахера
        phone - Номер мобильного телефона парикмахера
```

_Примеры ответа_

`Если id передан данные находятся в поле shift`

`Если id не передан данные находятся в поле shifts`

```json
{
  "shifts": []
}
```

```json
{
  "shifts": [
    {
      "id": 1,
      "day": 1,
      "start_day_time": 720,
      "end_day_time": 1400,
      "hairdressers": [
        {
          "id": 1,
          "name": "Икоева Лаура",
          "phone": "+1 (222) 333-44-66"
        }
      ]
    }
  ]
}
```

```json
{
  "shift": {
    "id": 1,
    "day": 1,
    "start_day_time": 720,
    "end_day_time": 1400,
    "hairdressers": [
      {
        "id": 1,
        "name": "Икоева Лаура",
        "phone": "+1 (222) 333-44-66"
      }
    ]
  }
}
```
