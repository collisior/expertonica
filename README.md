## Uploading and processing the Excel file that contains list of websites using Django

- Clone this repo to your system.

- Create a virtual environment and activate it.

- Install the dependencies using `pip install -r requirement.txt`.

- Start the python server, `python manage.py runserver`.

- Go to `localhost:8080` (or any other host:port you are using) and upload the `som_file_name.xls` file.

- Upload file (.xls, .xlsx, .csv). Wait until all websites gone through checking process.

- Waiting can take some time...

- To view already checked list of websites and their results, go to `localhost:8080/api/checked`

- To view JSON format of detailed result of a partivular website, go to `localhost:8080/api/site_check/example.com`


