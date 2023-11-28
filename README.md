# Summer Break
## A Solution to Canonical's Technical Take Home Assessment


### Assignment Summary

>You are contacted by a friend in desperate need of help - they have just spent the summer mowing lawns and, while they made good money, they forgot that they need to declare their income and expenses for tax purposes! You have been asked to use your programming prowess to help them out. The good news is that they kept all their invoices and receipts and have already performed the data-entry task. They merely need you to process the data and yield a tax-friendly report. You ask them why they don't just use [a spreadsheet, Turbo Tax, etc] but they scoff at your lack of DIY enthusiasm, alas.
>Indulging your friend, you agree to develop a web service API that allows submission of data files and the ability to query the resulting aggregate data for the summer.
>Their data entry exercise has resulted in a file tracking revenue and expenses, formatted as follows:
>  `Date, Type, Amount($), Memo`
>Where `Type` is one of "Income" or "Expense" and `Memo` is either an expense category or job address (both just strings)
>Your web service must have the following API endpoints:
>  `POST /transactions`
>Take as input the CSV formatted data as above, parse, and store the data.
>  `GET /report`
>Return a JSON document with the tally of gross revenue, expenses, and net revenue (gross - expenses) as follows:
>  {
>      "gross-revenue": <amount>,
>      "expenses": <amount>,
>      "net-revenue": <amount>
>  }


### Instructions

To setup the environment and run the code, you need to run a few things in your terminal. The first is setting up the environment and running the flask app:

1. cd to the directory where app.py, data_handler.py, data.csv, and test.sh are located
2. setup and run flask with the following command
  `export FLASK_APP=app.py && export FLASK_ENV=development && flask run`

To run a test of this API, simply run the contents of the test.sh file provided:

1. open a new terminal (since your flask app is running in the first)
2. cd to the directory where app.py, data_handler.py, data.csv, and test.sh are located using either `bash test.sh` or `sh test.sh` in a new terminal window

The test will perform a POST request to the `/transactions` endpoint using the `data.csv` file and then perform a GET request to the `/report` endpoint, returning JSON data to summarize the finances.

You can perform any additional tests using other CSV files provided they have the same structure as `data.csv` with columns for `Date, Type, Amount($), Memo`. This can be done in a number of ways 
- a similar way as the `test.sh` file
- using software such as Thunder Client or Postman to perform requests
- inputting curl commands into your terminal directly
  - `curl -X POST http://127.0.0.1:5000/transactions  -F "data=@<CSV_FILE>"` for POST
  - `curl http://127.0.0.1:5000/report` for GET


### Context and Assumptions

I approached this challenge trying to keep it as simple as possible with basic Flask endpoints and a temporary database for storage instead of a persistent one like a SQL or MongoDB database.

To keep the temporary database modular, in the event it requires being replaced with a persistent database, I have included it as a class in its own Python module, utelizing the  `pandas`library. Within the class we have access to methods which retrieve or update the database as required by the main code.

I decided to go with `pandas` to handle the database because it performs well with the data provided in the assignment and can also manipulate the data quite easily, similar to how an SQL query would. 

I have begun this assignment with the assumption that the user would potentially be making multiple POST requests to the API to continually update their financial records over time, and as such have decided to handle duplicate entries so they are not considered in the financial summary. 

I have also considered that there will be potentially circumstances where the user makes a request with a CSV file path that does not exist, so I have decided to incorporate some error handling for this circumstance. 


### Shortcomings

If this were something intended for production, the most obvious shortcoming would be 

* Volatile data storage. 
  A persistent database would be preferred. 
* Heavy `pandas` import.
  Switching to a persistent database would also relieve the code of this.
* Lack of logging.
  There should be more logging using Python's `logging` module, which I forwent in the interest of time. 
* More advanced functionality.
  As the challene outlined and as the code currently is, there is no way to remove data from the database in the event of a mistake or when starting a report for a new year. Obviously more features added for functionality like this would greatly improve the code. 


### Future Improvements

Given more time with this project, I would love to do the following:
* Incorporate logging to better handle errors and information for the user
* Switch to a SQL database for persistent storage
* Add more endpoints, namely ones to
  - remove data from the database
  - organise the database to handle numerous tax periods
* Incorporate different Types into the data such as `Refunds`
* Containerize this API using Docker to improve its distribution and more cleanly handle dependencies 
* Employ a cloud-based infrastructure such as AWS to enhance scalability and availability, while delegating the responsibilities of security and infrastructure management to a trusted service provider. 