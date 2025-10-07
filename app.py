from flask import Flask, render_template, request

app = Flask(__name__)

# conversion helpers
def lbs_to_kg(lbs): return lbs * 0.45359237
def cm_to_m(cm): return cm / 100
def feet_inch_to_m(feet, inches): return feet * 0.3048 + inches * 0.0254

# bmi calculator
def calc_bmi_summary(age, gender, unit_system, weight, height_m):
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category, color = "Underweight", "#ff9800"
    elif bmi < 25:
        category, color = "Normal", "#4caf50"
    elif bmi < 30:
        category, color = "Overweight", "#2196f3"
    else:
        category, color = "Obesity", "#f44336"

    healthy_min_w = 18.5 * (height_m ** 2)
    healthy_max_w = 24.9 * (height_m ** 2)
    bmi_prime = bmi / 25
    ponderal_index = weight / (height_m ** 3)

    return {
        "age": age,
        "gender": gender,
        "unit_system": unit_system,
        "bmi": round(bmi, 1),
        "category": category,
        "color": color,
        "healthy_weight_min": round(healthy_min_w, 1),
        "healthy_weight_max": round(healthy_max_w, 1),
        "bmi_prime": round(bmi_prime, 2),
        "ponderal_index": round(ponderal_index, 2),
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result, error = None, None
    if request.method == "POST":
        try:
            unit = request.form.get("unit", "us")
            age = int(request.form.get("age") or 0)
            gender = request.form.get("gender", "Male")

            if unit == "us":
                feet = float(request.form.get("feet") or 0)
                inches = float(request.form.get("inches") or 0)
                pounds = float(request.form.get("pounds") or 0)

                height_m = feet_inch_to_m(feet, inches)
                weight_kg = lbs_to_kg(pounds)

            else:  # metric
                cm = float(request.form.get("cm") or 0)
                kg = float(request.form.get("kg") or 0)

                height_m = cm_to_m(cm)
                weight_kg = kg

            # ✅ strict validation
            if age < 2 or age > 120:
                raise ValueError("⚠ Age must be between 2 and 120 years.")
            if height_m <= 0:
                raise ValueError("⚠ Height must be greater than zero.")
            if weight_kg <= 0:
                raise ValueError("⚠ Weight must be greater than zero.")

            result = calc_bmi_summary(age, gender, unit, weight_kg, height_m)

        except ValueError as ex:
            error = str(ex)
        except Exception:
            error = "⚠ Invalid input. Please enter valid numbers."

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
