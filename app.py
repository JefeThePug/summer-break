import os
from flask import Flask, request, jsonify
from data_handler import DataHandler

app = Flask(__name__)
DATABASE = DataHandler()

# Constants
EXPENSE_TYPE = " Expense"
INCOME_TYPE = " Income"


@app.route('/')
def home() -> tuple:
    """
    Root endpoint to display available requests.
    """
    return (
        jsonify(
            {
                "root":{
                    "requests": {
                        "POST": "/transactions -f data=@<csv file>",
                        "GET": "/report",
                    }
                }
            }
        ), 
        200,
    )


@app.route('/transactions', methods=["POST"])
def transactions() -> tuple:
    """
    Endpoint to handle data upload
    Data should be a csv file passed into the request as a variable named "data"
    """
    try:
        data = request.files["data"]
        if data:
            DATABASE.update_data(data.stream)
            return (jsonify({"message":"successfully uploaded data"}), 200)
        else:
            return (
                jsonify(
                    {"error": "no 'data' file provided in the transactions request"}
                ), 
                400,
            )
    except FileNotFoundError:
        return (jsonify({"error": "File Not Found"}), 400)
    except Exception as e:
        return (jsonify({"error": f"Internal server error: {str(e)}"}), 500)


@app.route('/report')
def report() -> tuple:
    """
    Endpoint to generate a financial report based on the data uploaded to the database.
    """
    try:
        data = DATABASE.get_data()
        summary = data.groupby(by=["Type"])["Amount($)"].sum()
        expenses = summary.get(EXPENSE_TYPE, 0.0)
        income = summary.get(INCOME_TYPE, 0.0)
        net_revenue = income - expenses
        return (
            jsonify(
                {
                    "gross-revenue": income, 
                    "expenses": expenses, 
                    "net-revenue": net_revenue,
                }
            ),
            200,
        )
    except Exception as e:
        return (jsonify({"error": f"Internal server error: {str(e)}"}), 500)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
