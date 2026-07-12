# Django Project Blogicum
Blogicum is a home for creative individuals, where the boundaries between blogging and social media communication are erased. Here you will find not only a friendly atmosphere, but also fascinating stories about new, previously unknown experiences.
## Part of the work on the Blogicum project:
- [Blogicum part 1](https://github.com/kostoyanskaya/blogicum_first_part)
- [Blogicum part 2](https://github.com/kostoyanskaya/blogicum_second_part)
- [Blogicum part 3 - final version.](https://github.com/kostoyanskaya/blogicum_django)
### Main features:
- Setting up the admin panel;
- New user registration;
- Writing, editing, deleting publications;
- Viewing other people's publications;
- Ability to add images;
- Ability to write and edit comments;
- Reading publications in the category of interest;
- Editing your own profile.
## What we use:
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
## Installation (Windows):
1. Cloning the repository
```
git clone git@github.com:kostoyanskaya/sprint4.git
```
1. Navigate to the blogicum_django directory
```
cd blogicum_django
```
3. Creating a virtual environment
```
python -m venv venv
```
4. Activating the virtual environment
```
source venv/Scripts/activate
```
5. Update pip
```
python -m pip install --upgrade pip
```
6. Installing dependencies
```
pip install -r requirements.txt
```
7. Navigate to the blogicum directory
```
cd blogicum
```
8. Applying migrations
```
python manage.py migrate
```
9. Load fixtures into the database
```
python manage.py loaddata db.json
```
10. Create a superuser
```
python manage.py createsuperuser
```
11. To run the project, enter the command
```
python manage.py runserver
```
## Author
#### [_Viktoriia_](https://github.com/kostoyanskaya/)
