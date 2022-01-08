## PROJECT SUMMARY:
REST APIs are built utilizing Python Django framework and Mysql DB.

It contains the below mentioned endpoints:
- a GET '/math'
- a GET '/funclogs-summary'

The `math` service handles n number of mathematical functions. It calculates the results of the mathematical algorithms and save the computation time in the database. This program includes only Fibonacci, Ackermann and Factorial algorithms. 

The `funclogs-summary` service displays the summary of the function logs. It helps manage the paginated data using page numbers in the request query parameters. It is also capable of filtering the data based on some filters.

## PROJECT STRUCTURE:
```
codingtask/
├── README.md
├── .gitignore
└── codingtask/
    ├── Makefile
    ├── apps
    │   ├── __init__.py
    │   ├── api
    │   │   ├── __init__.py
    │   │   ├── apps.py
    │   │   ├── exceptions.py
    │   │   ├── filters.py
    │   │   ├── migrations
    │   │   │   ├── 0001_initial.py
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── serializers.py
    │   │   ├── tests
    │   │   │   ├── __init__.py
    │   │   │   └── test_views.py
    │   │   ├── urls.py
    │   │   ├── utils.py
    │   │   └── views.py
    │   ├── pagination.py
    │   └── utils.py
    ├── conf
    │   └── init.sql
    ├── codingtask/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    └── requirements.txt
```

### PYTHON LIBRARIES & FRAMEWORKS USED:
- django - This is a Python-based open-source web framework that follows the model-template-view
architectural pattern.
- djangorestframework: This is a powerful and flexible toolkit built on top of the Django web framework
for building REST APIs.
- django-filter:- This is a reusable Django application for allowing users to filter querysets
dynamically from URL parameters.
- mysqlclient:- MySQL DB connector for Python.
- drf-yasg:- This is a Swagger generation tool provided by Django Rest Framework that allow you
to build API documentation.
- ddt: Data-driven testing (DDT) is a parameterized testing that allow you to multiply one test case
by running it with different test data, and make it appear as multiple test cases.

### PREREQUISITES:
- Please make sure you have Python and Mysql installed in your system
- Python 3.6.0 is used for this task.

### HOW TO START APPLICATION USING VIRTUAL ENVIRONMENT:
Please follow the below steps to start the application(Following commands are appliable for Windows OS):

```
- Setup mysql database:
mysql -u root -p (login into mysql server)
Enter root user password
create databases and database user. You can execute the sql script under codingtask\conf\init.sql.

NOTE: I have used MYSQL WorkBench to execute the SQL queries.

```
- Navigate to the project directory: ```cd codingtask```
- Create the virtual environment: ```python3 -m venv env```  or ```python -m venv env```
- Activate the virtual environment: ```env/Scripts/activate```. [For MacOS/Linux use ```source env/bin/activate```]

- Go into the directory:  ```cd codingtask```
- Install project requirements:  ```make install-requirements```
- Create database tables:  ```make migrate```
- Run the application by the following command:  ```make start-server```
- Show database migrations (if you want to see):  ```make showmigrations```

NOTE: "make" utility will be mostly available by default in *nix and MacOS. On Windows, you need to install manually.
"make" will be very useful for automating tasks.
If you are unable to install "make", then you can execute the commands that are present inside Makefile.

### HOW TO RUN APPLICATION UNITTESTS
- Run the command to run the all unittests of the application: ```make tests```
  
### HOW TO TEST THE API
- How to test using Swagger UI:
    - Hit the url in the browser:
        ```
        localhost:8080/api-docs/
        ```

- How to test using CURL:
    - Math API
        ```
        curl -X GET "http://localhost:8080/api/math/?function=fibonacci&n=5" -H  "accept: application/json"
        ```
    - Function Logs API
        ```
        curl -X GET "http://localhost:8080/api/funclogs-summary/?function=factorial" -H  "accept: application/json"
        ```

#### HOW TO SETUP THE PROJECT ON AWS ELASTIC BEAN STALK
Following are the steps that need to be executed to connect to Django application on AWS.

High-Level Steps:
- Install EBCLI:
    Command to execute is : ```python -m pip install awsebcli``` or ```pip install awsebcli```
    Set the ENVIRONMENT VARIABLE for eb.
- Environment Preparation:
   - Activate your virtual Environment - C:\Users\USERNAME\ebdjango>%HOMEPATH%\eb-virt\Scripts\activate
   - Run pip freeze, and then save the output to a file named requirements.txt.
       Create a directory named ```.ebextensions```
       In the ```.ebextensions``` directory, add a configuration file named ```django.config``` with the following text. This setting, WSGIPath, specifies the location of the WSGI script that Elastic Beanstalk uses to start your application
                option_settings:
            aws:elasticbeanstalk:container:python:
                WSGIPath: codingtask/wsgi.py
   - Deactivate your virtual environment with the ```deactivate``` command.

- Configure ElasticBeanStalk
    - Initialize the App : Command is - ```eb init -p python-3.6 codingtask```
    - Create an Environment: Commaind is - ```eb create codingtask-env```
    - When the environment creation process completes, find the domain name of your new environment by running ```eb status``` and note down the ```CNAME``` value
    - Open the ```settings.py``` file in the application directory. Add ```ALLOWED_HOSTS = [CNAME value]``` setting in a new line. Save the file

- Deployment Process
    - Installing packages – ```eb deploy```. This command needs to be run whenever you perform any change in the code.
    
- Configuring a Database
    - Database setup & Perform database migrations:
        Execute ```eb console``` to open the BeanStalk Configuration page. Create a new RDS database with username/password.
        Modify settings.py to point to the newly created RDS instance.
        ```python manage.py makemigrations``` and ```python manage.py migrate``` to be  executed in your virtual environment to create table structure.
    - Execute ```eb deploy``` to deploy the changes made above.

- Accessing the Application
  - ```eb open``` - To open the application in the browser.

NOTE: Elastic Beanstalk is a Platform-As-A-Service[PAAS] offering from Amazon that can setup, deploy, and maintain the application on Amazon AWS. It’s a managed service. You can quickly deploy your application without thinking of setting up underlying infrastructure to run your program.

