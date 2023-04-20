# Votally
An open polling system based on Python Django framework.

# Requirements
This project runs on [Python 3.10](https://www.python.org/) using the [Django 4.1.7](https://www.djangoproject.com/) Web Framework The following requirements are listed in the requirements.txt file which can be used to install the required packages using pip.

- asgiref==3.6.0
- defusedxml==0.7.1
- diff-match-patch==20200713
- Django==4.1.7
- django-bootstrap5==22.2
- django-import-export==3.1.0
- et-xmlfile==1.1.0
- MarkupPy==1.14
- odfpy==1.4.1
- openpyxl==3.1.2
- Pillow==9.4.0
- PyYAML==6.0
- sqlparse==0.4.3
- tablib==3.3.0
- tzdata==2022.7
- xlrd==2.0.1
- xlwt==1.3.0

# Development Setup
Clone the repository
```bash
git clone https://github.com/advation/votally.git
```

Create a virtual environment and install the requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the development server to create the DB file.
```bash
python manage.py runserver 0.0.0.0:8000
``` 

Create a superuser
```bash
python manage.py createsuperuser
```

Make migrations & migrate to create the DB schema
```bash
python manage.py makemigrations
python manage.py migrate
```

Populate DB with initial data (zip codes, age groups, etc.)
 