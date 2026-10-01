from flask import Flask, render_template, jsonify, request
import sqlite3
import requests
from datetime import date

app = Flask(__name__)

DATABASE = "yatb.db"

WORDS = [
    {
        "word": "profound",
        "meaning": "Very deep or having a strong effect.",
        "example": "The experience had a profound impact on her."
    },
    {
        "word": "compelling",
        "meaning": "Very convincing or interesting.",
        "example": "He presented a compelling argument."
    },
    {
        "word": "inevitable",
        "meaning": "Certain to happen and impossible to avoid.",
        "example": "Change is inevitable."
    },
    {
        "word": "significant",
        "meaning": "Important or noticeable.",
        "example": "Education plays a significant role in society."
    },
    {
        "word": "substantial",
        "meaning": "Large in amount, size or importance.",
        "example": "She made substantial progress."
    },
    {
        "word": "detrimental",
        "meaning": "Causing harm or damage.",
        "example": "Too much stress can be detrimental."
    },
    {
        "word": "beneficial",
        "meaning": "Helpful or useful.",
        "example": "Reading is beneficial for your vocabulary."
    },
    {
        "word": "widespread",
        "meaning": "Existing or happening in many places.",
        "example": "The technology is now widespread."
    },
    {
        "word": "controversial",
        "meaning": "Causing disagreement or argument.",
        "example": "The decision was controversial."
    },
    {
        "word": "remarkable",
        "meaning": "Unusual or impressive.",
        "example": "She made remarkable progress."
    },
    {
        "word": "vulnerable",
        "meaning": "Easily hurt, influenced or damaged.",
        "example": "Young systems can be vulnerable."
    },
    {
        "word": "persistent",
        "meaning": "Continuing despite difficulty.",
        "example": "Persistent practice improves skills."
    },
    {
        "word": "ambiguous",
        "meaning": "Having more than one possible meaning.",
        "example": "The question was ambiguous."
    },
    {
        "word": "unprecedented",
        "meaning": "Never having happened before.",
        "example": "The team achieved unprecedented results."
    },
    {
        "word": "sophisticated",
        "meaning": "Advanced and complex.",
        "example": "The software uses a sophisticated system."
    },
    {
        "word": "overwhelming",
        "meaning": "Very strong or difficult to deal with.",
        "example": "The amount of information was overwhelming."
    },
    {
        "word": "reluctant",
        "meaning": "Not willing or eager to do something.",
        "example": "He was reluctant to speak."
    },
    {
        "word": "determined",
        "meaning": "Having a strong decision to achieve something.",
        "example": "She was determined to succeed."
    },
    {
        "word": "efficient",
        "meaning": "Working well without wasting time or resources.",
        "example": "This method is more efficient."
    },
    {
        "word": "innovative",
        "meaning": "Using new ideas or methods.",
        "example": "The school created an innovative project."
    },
    {
        "word": "diverse",
        "meaning": "Including many different types.",
        "example": "The class has diverse interests."
    },
    {
        "word": "accurate",
        "meaning": "Correct and free from mistakes.",
        "example": "Make sure your answer is accurate."
    },
    {
        "word": "relevant",
        "meaning": "Connected with the subject being discussed.",
        "example": "Use relevant evidence."
    },
    {
        "word": "adaptable",
        "meaning": "Able to change according to circumstances.",
        "example": "Good learners are adaptable."
    },
    {
        "word": "credible",
        "meaning": "Able to be trusted or believed.",
        "example": "Use credible sources."
    },
    {
        "word": "considerable",
        "meaning": "Large or important enough to be noticed.",
        "example": "The project requires considerable effort."
    },
    {
        "word": "crucial",
        "meaning": "Extremely important.",
        "example": "Practice is crucial for improvement."
    },
    {
        "word": "complex",
        "meaning": "Containing many connected parts; not simple.",
        "example": "The problem is complex."
    },
    {
        "word": "enhance",
        "meaning": "To improve the quality or value of something.",
        "example": "Reading can enhance your vocabulary."
    },
    {
        "word": "emphasize",
        "meaning": "To give special importance to something.",
        "example": "The teacher emphasized the key idea."
    },
    {
        "word": "facilitate",
        "meaning": "To make something easier.",
        "example": "Technology can facilitate learning."
    },
    {
        "word": "maintain",
        "meaning": "To keep something at the same level or condition.",
        "example": "Maintain a regular study routine."
    },
    {
        "word": "obtain",
        "meaning": "To get or acquire something.",
        "example": "Students can obtain useful information."
    },
    {
        "word": "perspective",
        "meaning": "A particular way of viewing something.",
        "example": "Try another perspective."
    },
    {
        "word": "phenomenon",
        "meaning": "Something that exists or happens and can be observed.",
        "example": "Social media is a global phenomenon."
    },
    {
        "word": "predict",
        "meaning": "To say what you think will happen.",
        "example": "Scientists can predict some changes."
    },
    {
        "word": "allocate",
        "meaning": "To give something for a particular purpose.",
        "example": "Allocate enough time for revision."
    },
    {
        "word": "consequence",
        "meaning": "A result of an action or event.",
        "example": "Every decision has a consequence."
    },
    {
        "word": "assess",
        "meaning": "To judge or evaluate something.",
        "example": "Teachers assess students' progress."
    },
    {
        "word": "justify",
        "meaning": "To give a good reason for something.",
        "example": "You must justify your answer."
    },
    {
        "word": "retain",
        "meaning": "To keep or remember something.",
        "example": "Practice helps you retain vocabulary."
    },
    {
        "word": "transform",
        "meaning": "To change something significantly.",
        "example": "Education can transform lives."
    },
    {
        "word": "capacity",
        "meaning": "The ability or amount something can contain or handle.",
        "example": "The brain has a remarkable capacity to learn."
    },
    {
        "word": "coherent",
        "meaning": "Clear, logical and well organized.",
        "example": "Write a coherent paragraph."
    },
    {
        "word": "feasible",
        "meaning": "Possible and practical to do.",
        "example": "The plan is feasible."
    }
]

QUESTIONS = [
    {
        "question": "If a result is 'inevitable', it is...",
        "answers": [
            "certain to happen",
            "easy to forget",
            "very small",
            "completely unclear"
        ],
        "correct": 0
    },
    {
        "question": "Something 'detrimental' is...",
        "answers": [
            "helpful",
            "harmful",
            "traditional",
            "accurate"
        ],
        "correct": 1
    },
    {
        "question": "A 'compelling' argument is...",
        "answers": [
            "convincing",
            "ambiguous",
            "weak",
            "irrelevant"
        ],
        "correct": 0
    },
    {
        "question": "If something is 'widespread', it is...",
        "answers": [
            "rare",
            "found in many places",
            "secret",
            "unfinished"
        ],
        "correct": 1
    },
    {
        "question": "To 'allocate' time means to...",
        "answers": [
            "waste it",
            "give it for a purpose",
            "forget it",
            "measure it"
        ],
        "correct": 1
    },
    {
        "question": "A 'credible' source is...",
        "answers": [
            "trustworthy",
            "confusing",
            "ancient",
            "random"
        ],
        "correct": 0
    },
    {
        "question": "To 'enhance' something means to...",
        "answers": [
            "improve it",
            "remove it",
            "hide it",
            "predict it"
        ],
        "correct": 0
    },
    {
        "question": "A 'coherent' answer is...",
        "answers": [
            "logical and clear",
            "very short",
            "unrelated",
            "incorrect"
        ],
        "correct": 0
    }
]


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 1,
            last_day TEXT,
            words_learned INTEGER DEFAULT 0
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS saved_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            meaning TEXT,
            example TEXT
        )
    """)

    user = connection.execute(
        "SELECT * FROM user WHERE id = 1"
    ).fetchone()

    if not user:
        connection.execute(
            """
            INSERT INTO user
            (id, xp, streak, last_day, words_learned)
            VALUES (1, 0, 1, ?, 0)
            """,
            (str(date.today()),)
        )

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/api/stats")
def stats():
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM user WHERE id = 1"
    ).fetchone()

    connection.close()

    xp = user["xp"]

    return jsonify({
        "xp": xp,
        "level": xp // 100 + 1,
        "level_xp": xp % 100,
        "streak": user["streak"],
        "words_learned": user["words_learned"]
    })


@app.get("/api/words")
def get_words():
    return jsonify(WORDS)


@app.post("/api/xp")
def add_xp():
    data = request.json
    amount = int(data.get("amount", 0))

    amount = max(0, min(amount, 100))

    connection = get_connection()

    connection.execute(
        """
        UPDATE user
        SET xp = xp + ?,
            words_learned = words_learned + ?
        WHERE id = 1
        """,
        (
            amount,
            1 if amount >= 5 else 0
        )
    )

    connection.commit()
    connection.close()

    return jsonify({"success": True})


@app.get("/api/questions")
def get_questions():
    return jsonify(QUESTIONS)


@app.get("/api/saved")
def get_saved_words():
    connection = get_connection()

    words = connection.execute(
        """
        SELECT word, meaning, example
        FROM saved_words
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return jsonify([dict(word) for word in words])


@app.post("/api/saved")
def save_word():
    data = request.json

    word = data.get("word", "").strip()

    if not word:
        return jsonify({"success": False}), 400

    connection = get_connection()

    connection.execute(
        """
        INSERT OR REPLACE INTO saved_words
        (word, meaning, example)
        VALUES (?, ?, ?)
        """,
        (
            word,
            data.get("meaning", ""),
            data.get("example", "")
        )
    )

    connection.commit()
    connection.close()

    return jsonify({"success": True})


@app.delete("/api/saved/<path:word>")
def delete_saved_word(word):
    connection = get_connection()

    connection.execute(
        "DELETE FROM saved_words WHERE word = ?",
        (word,)
    )

    connection.commit()
    connection.close()

    return jsonify({"success": True})


@app.post("/api/translate")
def translate():
    data = request.json

    text = data.get("text", "").strip()
    source = data.get("source", "auto")
    target = data.get("target", "en")

    if not text:
        return jsonify({
            "translation": ""
        })

    try:
        response = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": source,
                "tl": target,
                "dt": "t",
                "q": text
            },
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        translation = ""

        for part in result[0]:
            if part[0]:
                translation += part[0]

        return jsonify({
            "translation": translation
        })

    except Exception:
        return jsonify({
            "translation": "",
            "error": "Translation is temporarily unavailable."
        }), 503


if __name__ == "__main__":
    create_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )