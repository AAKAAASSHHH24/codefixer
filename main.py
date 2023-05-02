from flask import Flask, request, render_template
from dotenv import load_dotenv
import openai
import os

app = Flask(__name__)
load_dotenv()

# API Token
openai.api_key = os.getenv('openai_api_key')
#stripe.api_key = os.getenv('stripe_api_key')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if usage_counter > 3:
            return render_template("payment.html")
        # Code Errr
        code = request.form["code"]
        error = request.form["error"]

        prompt = (f"Explain the error in this code without fixing it:"
                  f"\n\n{code}\n\nError:\n\n{error}")
        model_engine = "text-davinci-003"
        explanation_completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.9,
        )

        explanation = explanation_completions.choices[0].text
        print(explanation)
        fixed_code_prompt = (f"Fix this code: \n\n{code}\n\nError:\n\n{error}."
                             f" \n Respond only with the fixed code.")
        fixed_code_completions = openai.Completion.create(
            engine=model_engine,
            prompt=fixed_code_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.9,
        )
        fixed_code = fixed_code_completions.choices[0].text
        usage_counter += 1
        update_usage_counter(fingerprint, usage_counter)

        return render_template("index.html",
                               explanation=explanation,
                               fixed_code=fixed_code)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
