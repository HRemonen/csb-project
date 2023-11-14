# Cyber Security Base 2023 – Project I

This repository contains a vulnerable web application for the first project of the [Cyber Security Base 2023](https://cybersecuritybase.mooc.fi/module-3.1) course.

## Disclaimer

This project intentionally contains security vulnerabilities. 

## Installation

1. Install the needed packages with 
    ```bash
    python3 -m pip install django "selenium<4" "urllib3<2" beautifulsoup4 requests
    ```

2. Set up a local database

    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

3. Start the development server

    ```bash
    python3 manage.py runserver
    ```