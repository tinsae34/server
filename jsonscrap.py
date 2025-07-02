from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
MESSAGES_FILE = "messages.json"
DRIVERS_FILE = "drivers.json"

def load_deliveries():
    try:
        with open(MESSAGES_FILE, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except Exception as e:
        print("Error reading messages.json:", e)
        return []

def save_deliveries(deliveries):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(deliveries, f, indent=2)

def load_drivers():
    try:
        with open(DRIVERS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error reading drivers.json:", e)
        return []

@app.route("/")
def index():
    deliveries = load_deliveries()
    drivers = load_drivers()
    return render_template("index.html", deliveries=deliveries, drivers=drivers)

@app.route("/assign_driver", methods=["POST"])
def assign_driver():
    try:
        delivery_index = int(request.form.get("delivery_index", -1))
        driver_id = request.form.get("driver_id", "").strip()

        if delivery_index < 0 or not driver_id:
            raise ValueError("Invalid form data")

        deliveries = load_deliveries()
        if 0 <= delivery_index < len(deliveries):
            deliveries[delivery_index]["assigned_driver_id"] = driver_id
            print(f"Assigning driver {driver_id} to delivery {delivery_index}")

            save_deliveries(deliveries)

    except Exception as e:
        print("Error in assigning driver:", e)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=3000)
