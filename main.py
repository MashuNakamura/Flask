from flask import Flask, render_template, request, redirect, url_for, session
from app import BayesianMBTIApp

# Inisialisasi Flask
app = Flask(__name__)
app.secret_key = '123'  # untuk session

# Load app dan pertanyaan saat pertama
mbti_app = BayesianMBTIApp()
questions = mbti_app.questions

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        idx = int(request.form["idx"])
        answer = int(request.form["answer"])
        
        if "probabilities" not in session:
            session["probabilities"] = {k: v for k, v in mbti_app.type_probabilities.items()}

        # Reconstruct object
        mbti_app.type_probabilities = session["probabilities"]

        # Update probabilitas
        question, answer_likelihoods = questions[idx]
        if answer in answer_likelihoods:
            mbti_app.update_probabilities(answer_likelihoods[answer])
            session["probabilities"] = mbti_app.type_probabilities
        else:
            pass  # bisa ditambahkan handling

        # Redirect ke pertanyaan selanjutnya atau ke hasil
        if idx + 1 < len(questions):
            return redirect(url_for("question", idx=idx+1))
        else:
            return redirect(url_for("result"))

    return redirect(url_for("question", idx=0))


@app.route("/question/<int:idx>")
def question(idx):
    if idx >= len(questions):
        return redirect(url_for("result"))
    question, _ = questions[idx]
    return render_template("index.html", idx=idx, question=question)


@app.route("/result")
def result():
    mbti_app.type_probabilities = session.get("probabilities", mbti_app.type_probabilities)
    mbti_type = mbti_app.get_most_probable_type()
    description = mbti_app.mbti_descriptions.get(mbti_type, "Deskripsi tidak tersedia.")
    session.clear()
    return render_template("result.html", mbti_type=mbti_type, description=description)

if __name__ == "__main__":
    app.run(debug=True)