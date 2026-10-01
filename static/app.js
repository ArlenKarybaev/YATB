let words = [];
let questions = [];

let currentWord = 0;
let currentQuestion = 0;

let quizLocked = false;

let lastTranslation = "";


/* ================= API ================= */

async function api(url, options = {}) {

    const response = await fetch(url, options);

    if (!response.ok) {
        throw new Error("API error");
    }

    return response.json();
}


/* ================= NAVIGATION ================= */

function navigate(page) {

    document
        .querySelectorAll(".page")
        .forEach(element => {

            element.classList.remove("active");

        });


    const selectedPage =
        document.getElementById("page-" + page);


    if (!selectedPage) {
        return;
    }


    selectedPage.classList.add("active");


    document
        .querySelectorAll(".bottom-nav button")
        .forEach(button => {

            button.classList.remove("active");

            if (
                button.dataset.page === page
            ) {

                button.classList.add("active");

            }

        });


    if (page === "quiz") {
        renderQuestion();
    }


    if (page === "vocabulary") {
        loadVocabulary();
    }


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


/* ================= STATS ================= */

async function updateStats() {

    const stats =
        await api("/api/stats");


    document.getElementById("xp")
        .textContent = stats.xp;


    document.getElementById("streak")
        .textContent = stats.streak;


    document.getElementById("level")
        .textContent = stats.level;


    document.getElementById("level-xp")
        .textContent = stats.level_xp;


    document.getElementById("progress")
        .style.width = stats.level_xp + "%";
}


/* ================= LEARN ================= */

async function loadWords() {

    words =
        await api("/api/words");

    renderWord();
}


function renderWord() {

    if (!words.length) {
        return;
    }


    const word =
        words[currentWord];


    document.getElementById("word-counter")
        .textContent =
        `${currentWord + 1} / ${words.length}`;


    document.getElementById("word")
        .textContent =
        word.word;


    document.getElementById("meaning")
        .textContent =
        word.meaning;


    document.getElementById("example")
        .textContent =
        `"${word.example}"`;
}


function nextWord() {

    currentWord++;

    if (currentWord >= words.length) {
        currentWord = 0;
    }

    renderWord();
}


async function learnCurrentWord() {

    await api(
        "/api/xp",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                amount: 5
            })
        }
    );


    await updateStats();

    nextWord();
}


async function saveCurrentWord() {

    const word =
        words[currentWord];


    await api(
        "/api/saved",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(word)
        }
    );


    alert("Saved to My Vocabulary ⭐");
}


/* ================= QUIZ ================= */

async function loadQuestions() {

    questions =
        await api("/api/questions");

    renderQuestion();
}


function renderQuestion() {

    if (!questions.length) {
        return;
    }


    quizLocked = false;


    const question =
        questions[currentQuestion];


    document.getElementById("question-number")
        .textContent =
        `Question ${currentQuestion + 1} / ${questions.length}`;


    document.getElementById("question")
        .textContent =
        question.question;


    document.getElementById("feedback")
        .textContent = "";


    document.getElementById("next-question")
        .style.display = "none";


    const container =
        document.getElementById("answers");


    container.innerHTML = "";


    question.answers.forEach(
        (answer, index) => {

            const button =
                document.createElement("button");


            button.className = "answer";

            button.textContent = answer;


            button.onclick = function () {

                answerQuestion(
                    index,
                    button
                );

            };


            container.appendChild(button);

        }
    );
}


async function answerQuestion(
    selected,
    selectedButton
) {

    if (quizLocked) {
        return;
    }


    quizLocked = true;


    const question =
        questions[currentQuestion];


    const buttons =
        document.querySelectorAll(".answer");


    buttons.forEach(
        (button, index) => {

            if (
                index === question.correct
            ) {

                button.classList.add(
                    "correct"
                );

            }

        }
    );


    const feedback =
        document.getElementById("feedback");


    if (
        selected === question.correct
    ) {

        feedback.textContent =
            "Correct! +10 XP 🔥";


        await api(
            "/api/xp",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    amount: 10
                })
            }
        );


        await updateStats();

    } else {

        selectedButton.classList.add(
            "wrong"
        );


        feedback.textContent =
            "Not quite. Keep learning!";

    }


    document.getElementById("next-question")
        .style.display = "block";
}


function nextQuestion() {

    currentQuestion++;

    if (
        currentQuestion >= questions.length
    ) {

        currentQuestion = 0;

    }


    renderQuestion();
}


/* ================= TRANSLATOR ================= */

async function translateText() {

    const input =
        document.getElementById(
            "translate-input"
        ).value.trim();


    if (!input) {
        return;
    }


    const translation =
        document.getElementById(
            "translation"
        );


    translation.textContent =
        "Translating...";


    const source =
        document.getElementById(
            "source-language"
        ).value;


    const target =
        document.getElementById(
            "target-language"
        ).value;


    try {

        const result =
            await api(
                "/api/translate",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: input,
                        source: source,
                        target: target
                    })
                }
            );


        if (result.translation) {

            lastTranslation =
                result.translation;


            translation.textContent =
                result.translation;

        } else {

            translation.textContent =
                "Translation unavailable.";

        }

    } catch {

        translation.textContent =
            "Could not connect to translator.";

    }
}


function swapLanguages() {

    const source =
        document.getElementById(
            "source-language"
        );


    const target =
        document.getElementById(
            "target-language"
        );


    if (source.value === "auto") {
        source.value = "en";
    }


    const old =
        source.value;


    source.value =
        target.value;


    target.value =
        old;
}


async function saveTranslation() {

    const input =
        document.getElementById(
            "translate-input"
        ).value.trim();


    if (
        !input ||
        !lastTranslation
    ) {

        return;

    }


    await api(
        "/api/saved",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                word: input,

                meaning: lastTranslation,

                example:
                    "Saved from Translator"

            })
        }
    );


    alert("Saved to My Vocabulary ⭐");
}


/* ================= VOCABULARY ================= */

async function loadVocabulary() {

    const words =
        await api("/api/saved");


    const container =
        document.getElementById(
            "saved-list"
        );


    container.innerHTML = "";


    if (!words.length) {

        container.innerHTML = `

            <div class="learning-card">

                <div class="big-word">
                    🦅
                </div>

                <p style="
                    text-align:center;
                    color:#8995a5;
                ">
                    Your vocabulary is empty.
                    <br><br>
                    Save words from Learn
                    or Translator.
                </p>

            </div>

        `;

        return;
    }


    words.forEach(word => {

        const item =
            document.createElement("div");


        item.className =
            "saved-word";


        const content =
            document.createElement("div");


        const title =
            document.createElement("strong");


        title.textContent =
            word.word;


        const meaning =
            document.createElement("p");


        meaning.textContent =
            word.meaning;


        content.appendChild(title);

        content.appendChild(meaning);


        const remove =
            document.createElement("button");


        remove.className =
            "remove-btn";


        remove.textContent =
            "Remove";


        remove.onclick = async function () {

            await fetch(
                "/api/saved/" +
                encodeURIComponent(word.word),
                {
                    method: "DELETE"
                }
            );


            loadVocabulary();

        };


        item.appendChild(content);

        item.appendChild(remove);


        container.appendChild(item);

    });
}


/* ================= START ================= */

async function startApp() {

    try {

        await loadWords();

        await loadQuestions();

        await updateStats();

        await loadVocabulary();


        navigate("home");

    } catch (error) {

        console.error(error);

        alert(
            "YATB could not start. " +
            "Make sure Flask is running."
        );

    }
}


startApp();