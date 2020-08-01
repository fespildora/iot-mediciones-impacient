# Getting Started with Python on IBM Cloud

To get started, we'll take you through a sample Python Flask app, help you set up a development environment, deploy to IBM Cloud and add a Cloudant database.

## Prerequisites

You'll need the following:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)

## 1. Clone the sample app

Now you're ready to start working with the app. Clone the repo and change to the directory where the sample app is located.
  ```
git clone https://github.com/fespildora/iot-mediciones-impacient
cd iot-mediciones-impacient
  ```

  Peruse the files in the *iot-mediciones-impacient* directory to familiarize yourself with the contents.

## 2. Run the app locally

Install the dependencies listed in the [requirements.txt](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) file to be able to run the app locally.

You can optionally use a [virtual environment](https://packaging.python.org/installing/#creating-and-using-virtual-environments) to avoid having these dependencies clash with those of other Python projects or your operating system.
  ```
pip install -r requirements.txt
  ```

Run the app.
  ```
python app.py
  ```

 View your app at: http://localhost:8000

## 4. Create IoT Divice

1. Log in to IBM Cloud in your Browser. Browse to the `Dashboard`. Select your application by clicking on its name in the `Name` column.
2. Launch Service
3. Device Type > Add Device 
4. Browse > Add Device with reference Device Type
5. Simulations running > Import/Export simulation > simulator.json in the *iot-mediciones-impacient* directory
6. APP > Generate API Key > Select "Standart Application" > Generate Key
7. Copy API Key and Token.
8. Add API KEY in simulator.json

"APIKey": ""

9. Create file "application.yaml"

identity:
    appId: 
auth:
    key: 
    token:

10. Settings > Activate Last Event Cache 

## 4. Add a database

Next, we'll add a NoSQL database to this application and set up the application so that it can run locally and on IBM Cloud.

1. Log in to IBM Cloud in your Browser. Browse to the `Dashboard`. Select your application by clicking on its name in the `Name` column.
2. Click on `Connections` then `Connect new`.
2. In the `Data & Analytics` section, select `Cloudant NoSQL DB` and `Create` the service.
3. Select `Restage` when prompted. IBM Cloud will restart your application and provide the database credentials to your application using the `VCAP_SERVICES` environment variable. This environment variable is only available to the application when it is running on IBM Cloud.

Environment variables enable you to separate deployment settings from your source code. For example, instead of hardcoding a database password, you can store this in an environment variable which you reference in your source code. [Learn more...](/docs/manageapps/depapps.html#app_env)

## 5. Use the database

We're now going to update your local code to point to this database. We'll create a json file that will store the credentials for the services the application will use. This file will get used ONLY when the application is running locally. When running in IBM Cloud, the credentials will be read from the VCAP_SERVICES environment variable.

1. Create a file called `vcap-local.json` in the `iot-mediciones-impacient` directory with the following content:
  ```
  {
    "services": {
      "cloudantNoSQLDB": [
        {
          "credentials": {
            "username":"CLOUDANT_DATABASE_USERNAME",
            "password":"CLOUDANT_DATABASE_PASSWORD",
            "host":"CLOUDANT_DATABASE_HOST"
          },
          "label": "cloudantNoSQLDB"
        }
      ]
    }
  }
  ```

2. Back in the IBM Cloud UI, select your App -> Connections -> Cloudant -> View Credentials

3. Copy and paste the `username`, `password`, and `host` from the credentials to the same fields of the `vcap-local.json` file replacing **CLOUDANT_DATABASE_USERNAME**, **CLOUDANT_DATABASE_PASSWORD**, and **CLOUDANT_DATABASE_URL**.

4. Run your application locally.
  ```
python app.py
  ```

  View your app at: http://localhost:8000. Any names you enter into the app will now get added to the database.

