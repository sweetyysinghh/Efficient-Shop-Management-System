from flask import Flask, request, render_template
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load the sales prediction models and crowd model
model_a = pickle.load(open('best_model_a.pkl', 'rb'))
model_b = pickle.load(open('best_model_b.pkl', 'rb'))
model_c = pickle.load(open('best_model_c.pkl', 'rb'))
model_crowd = pickle.load(open('crowd.pkl', 'rb'))
encoder = pickle.load(open('encoder.pkl', 'rb'))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        day = request.form["day"]
        staff_per_5_customers = int(request.form["staff_per_5_customers"])
        inventory_a = int(request.form["inventory_a"])
        inventory_b = int(request.form["inventory_b"])
        inventory_c = int(request.form["inventory_c"])
        selling_price_a = float(request.form["selling_price_a"])
        cost_price_a = float(request.form["cost_price_a"])
        selling_price_b = float(request.form["selling_price_b"])
        cost_price_b = float(request.form["cost_price_b"])
        selling_price_c = float(request.form["selling_price_c"])
        cost_price_c = float(request.form["cost_price_c"])

        # Encoding the day
        encoded_day = encoder.transform(np.array([[day]]))
        # Predicting the crowd
        predicted_customer_count = model_crowd.predict(encoded_day)[0]
        customer_count = int(predicted_customer_count)
        staff_needed = (customer_count // 5) * staff_per_5_customers

        # Prepare the input data for the sales prediction models
        data = {f'Day_{x}': 0 for x in ['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']}
        data.update({'Customer Count': customer_count})

        # Set the correct day in data
        if f'Day_{day}' in data:
            data[f'Day_{day}'] = 1

        # Convert data to DataFrame
        input_df = pd.DataFrame([data])

        # Predict sales using the loaded models
        sales_a = int(model_a.predict(input_df)[0])
        sales_b = int(model_b.predict(input_df)[0])
        sales_c = int(model_c.predict(input_df)[0])

        # Calculate stock status and profits
        stock_status_a = "Enough" if inventory_a >= sales_a else "Restock"
        stock_status_b = "Enough" if inventory_b >= sales_b else "Restock"
        stock_status_c = "Enough" if inventory_c >= sales_c else "Restock"
        profit_a = (selling_price_a - cost_price_a) * sales_a
        profit_b = (selling_price_b - cost_price_b) * sales_b
        profit_c = (selling_price_c - cost_price_c) * sales_c

        return render_template("result.html", day=day, customer_count=customer_count, staff_needed=staff_needed,
                               sales_a=sales_a, stock_status_a=stock_status_a, profit_a=f'{profit_a:.2f}',
                               sales_b=sales_b, stock_status_b=stock_status_b, profit_b=f'{profit_b:.2f}',
                               sales_c=sales_c, stock_status_c=stock_status_c, profit_c=f'{profit_c:.2f}')

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
