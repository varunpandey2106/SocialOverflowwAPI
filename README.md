# SocialOverflowwAPI

## Introduction

SocialOverfloww is a blog/thought-post oriented Social Media API that is built using Django and Django Rest Framework

## Features

- **User Management and Authentication, Social Login**
- **Post/Artcile Management**
- **Feed**
- **Notifications**
- **Discussions**
- **Messaging**
- **Third party Integrations**

## DB DIAGRAM
![Screenshot 2023-10-08 210900](https://github.com/varunpandey2106/BaazaarAPI/assets/77747699/8c888954-a6ea-4c36-b3a0-cdd550bb239b)


## Swagger

![Screenshot 2023-10-08 210208](https://github.com/varunpandey2106/BaazaarAPI/assets/77747699/b673047d-db70-43ec-84cb-b6cdc2aba2ef)

![Screenshot 2023-10-08 210252](https://github.com/varunpandey2106/BaazaarAPI/assets/77747699/7265edcf-f447-425c-99c3-9996544dbdfd)

![Screenshot 2023-10-08 210528](https://github.com/varunpandey2106/BaazaarAPI/assets/77747699/77a88056-3790-4043-bd41-aa8b1e3d2ad9)

![Screenshot 2023-10-08 210625](https://github.com/varunpandey2106/BaazaarAPI/assets/77747699/01e7a176-19a5-4155-bc25-b85f5d264936)




## Future Work

- **search and discovery using elasticsearch**
- **popular articles/posts using a recommendation engine**

## Tech Stack

- **Django**
- **Django REST framework**
- **Celery** 
- **PostgreSQL**
- **DrawSQL**
- **OAuth2**
- **Twillio API**
- **Gmail API**
- **Postman**
- **Docker**


## Installation

Clone the repository and navigate to the project directory:
```bash

git clone https://github.com/varunpandey2106/SocialOverFlowwAPIAPI.git
cd BazaarAPI

```

- Setup Virtual Environment and install dependencies 
```bash
virtualenv SocialOverFlowwAPI
pip install -r requirements.txt
```

- Run Migrations and Run Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

- Access Project at: 
```bash
 http://localhost:8000/
```


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License
