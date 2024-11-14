# Sales Data Airflow Pipeline

## 1. Objectives

### 1.1 Process the sales data from excel format into SQL table in MYSQL

### 1.2 Turn the data into reports in excel and send them to Google Drive

### 1.3 Send notification to Gmail about the reports

### Create DAGs for each of the steps above in Airflow

## 2. Architecture

<img src="./images/Sales Data Airflow Pipeline.png" width="500">

## 3. Prerequisites

### 3.1 MySQL DB Setup

Run below docker command:

```bash
docker run --name mysql-diy --network diy_network -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=diy -e MYSQL_USER=myuser -e MYSQL_PASSWORD=mypassword mysql:8.0.40-debian
```

### 3.1.1 Run the SQL Queries

Connect to the MYSql DB using any clients and run the sql scripts in `sql_queries` folder.

### 3.2 Install Airflow in Docker

Follow the official instruction: [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

#### 3.2.1 Modifications to the official Airflow Docker Compose Yaml

##### 3.2.1.1 Use Dockerfile image rather than Official Docker Image

Line 52 is commented and line 53 is uncommented

```yaml
  # image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.10.2}
  build: .
```

##### 3.2.1.2 Include all needed Python packages

Include the packages in Line 71. If not, it is equivalent of the pakcages not installed in the Airflow container.

```yaml
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- openpyxl pandas pymysql sqlalchemy cryptography google-api-python-client google-auth}
```

##### 3.2.1.3 Mount local folder into the Airflow container’s folders

Look at line 75 to 83

```yaml
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - ${AIRFLOW_PROJ_DIR:-.}/operation:/opt/airflow/operation
    - ${AIRFLOW_PROJ_DIR:-.}/file_output:/opt/airflow/file_output
    - ${AIRFLOW_PROJ_DIR:-.}/credentials:/opt/airflow/credentials
    - ${AIRFLOW_PROJ_DIR:-.}/airflow.cfg:/opt/airflow/airflow.cfg
```

Some explanation

1. operation: to store the local python scripts, these will be imported as module in the dag scripts.
2. file_output: to store the excel files
3. credentials: to store the Service Account JSON.
4. airflow.cfg: to directly modify the Airflow Configuration.

##### 3.1.1.4 Add networks for each containers

Look into each container configs, they all have this line so they have same network with MySql DB.

```yaml
networks:
- diy_network
```

### 3.3 Setup for Sharepoint Upload

### 3.3.1 Google Service Account

1. Follow the official Instruction to setup Google Service Account: [List and get service account keys](https://cloud.google.com/iam/docs/keys-list-get)

2. Once you get the JSON file, copy it to the `credentials` folder

### 3.3.2 Copy the Sharepoint Directory to Python Code

<img src="./images/Sharepoint folder.png" width="500">

Your Shareppoint folder then needs to be stored in the Python code: `operation/upload_file_to_drive_product_category.py` and `operation/upload_file_to_drive_store_region.py`

### 3.4 Setup SMTP server for email

#### 3.4.1 Create a Google App Password

Get the App Apssword from this instructions: [App Password](https://myaccount.google.com/apppasswords)

#### 3.4.2 Setup airflow.cfg

Follow below template:

```cfg
[smtp]
smtp_host = smtp.gmail.com
smtp_port = 587
smtp_user = your.email@gmail.com
smtp_password = your_app_password  # Use App Password, not your regular Gmail password
smtp_mail_from = your.email@gmail.com
smtp_starttls = True
smtp_ssl = False

```

## 4. Tasks Explanations

Look into the Python scripts in `dags/` folder. There are 2 of them for different reports:

1. Product Category
2. Store Region

Their codes pretty much the same.

There are 3 Tasks being created, they will be explained by chapter below.

### 4.1.1 generate_report

This task uses Python modules to generate the Excel file from the MySQL DB. The modules is from `operation/read_mysql_product_category.py` and `operation/read_mysql_store_region.py`

### 4.1.2 upload_file

This task uses Python modules to upload the Excel to the Drive folder. The modules is from `operation/upload_file_to_drive_product_category.py` and `operation/upload_file_to_drive_store_region.py`

### 4.1.3 send_success_email

This task uses Email operator to send email of tasks completion. Thoretically, it will only send the email if the previous tasks completed/ successful.

## 5. Monitor the Airflow Webserver

1. Go to localhost:8081
2. Use default Airflow Credentials:

    ```txt
    Username: airflow
    Password: airflow
    ```
