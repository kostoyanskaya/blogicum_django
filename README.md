#  Django-проект Блогикум
Блогикум — это дом для креативных личностей, где границы между ведением блога и общением в социальных сетях стираются. Здесь вы найдете не только дружескую атмосферу, но и увлекательные истории о новых, ранее неизвестных впечатлениях.

## Часть работы над проектом Блогикум:

- [Блогикум часть 1](https://github.com/kostoyanskaya/blogicum_first_part)
- [Блогикум часть 2](https://github.com/kostoyanskaya/blogicum_second_part)
- [Блогикум часть 3 - финальная версия.](https://github.com/kostoyanskaya/blogicum_django)

### Основные возможности:

- Настройка панели администратора;
- Регистрация нового пользователя;
- Написание публикаций, редактирование, удаление;
- Просмотр чужих публикаций;
- Возможность добавлять картинки;
- Возможность написать и редактировать комментарии;
- Чтение публикаций в интересующей категории;
- Редактирование собственного профиля.
## Что применяем:
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white)
![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?logo=pytest&logoColor=white)
![Git](https://img.shields.io/badge/-Git-F05032?logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/-GitHub-181717?logo=github&logoColor=white)
* SQLite
* Django templates
* Django routes
* Django ORM
* Django forms

## Установка (Windows):

1. Клонирование репозитория

```
git clone git@github.com:kostoyanskaya/sprint4.git
```

1. Переход в директорию blogicum_django

```
cd blogicum_django
```

3. Создание виртуального окружения

```
python -m venv venv
```

4. Активация виртуального окружения

```
source venv/Scripts/activate
```

5. Обновите pip

```
python -m pip install --upgrade pip
```

6. Установка зависимостей

```
pip install -r requirements.txt
```

7. Переход в директорию blogicum

```
cd blogicum
```

8. Применение миграций

```
python manage.py migrate
```

9. Загрузить фикстуры в БД

```
python manage.py loaddata db.json
```

10. Создать суперпользователя

```
python manage.py createsuperuser
```

11. Запуск проекта, введите команду

```
python manage.py runserver
```

## Автор
#### [_Анастасия Ресницкая_](https://github.com/kostoyanskaya/)
