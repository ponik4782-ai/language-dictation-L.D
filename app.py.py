from flask import Flask, render_template, request, jsonify
import difflib

app = Flask(__name__)

# Расширенная база фраз для диктанта
DATA = {
    "it": [
        {
            "phrase": "Buongiorno, vorrei un caffè per favore.",
            "translation": "Доброе утро, я бы хотел кофе, пожалуйста."
        },
        {
            "phrase": "Mi piacerebbe viaggiare in Italia quest'estate.",
            "translation": "Мне бы хотелось попутешествовать по Италии этим летом."
        },
        {
            "phrase": "Dove si trova la stazione dei treni?",
            "translation": "Где находится железнодорожная станция?"
        },
        {
            "phrase": "Quanto costa questo biglietto?",
            "translation": "Сколько стоит этот билет?"
        },
        {
            "phrase": "Parla inglese?",
            "translation": "Вы говорите по-английски?"
        },
        {
            "phrase": "La cucina italiana è la migliore del mondo.",
            "translation": "Итальянская кухня — лучшая в мире."
        }
    ],
    "ko": [
        {
            "phrase": "안녕하세요, 저는 한국어를 공부하고 있어요.",
            "translation": "Здравствуйте, я изучаю корейский язык."
        },
        {
            "phrase": "오늘 날씨가 정말 좋습니다.",
            "translation": "Сегодня погода действительно отличная."
        },
        {
            "phrase": "내일 영화 보러 갈까요?",
            "translation": "Пойдем завтра в кино?"
        },
        {
            "phrase": "이것은 얼마예요?",
            "translation": "Сколько это стоит?"
        },
        {
            "phrase": "저는 김치를 아주 좋아합니다.",
            "translation": "Я очень люблю кимчи."
        },
        {
            "phrase": "한국 음식은 정말 맛있어요.",
            "translation": "Корейская еда очень вкусная."
        }
    ]
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_phrase', methods=['POST'])
def get_phrase():
    data = request.json
    lang = data.get('lang', 'it')
    index = data.get('index', 0)

    phrases = DATA.get(lang, DATA['it'])
    if index >= len(phrases):
        index = 0  # Зацикливаем фразы, когда они кончаются

    item = phrases[index]

    return jsonify({
        "phrase": item["phrase"],
        "translation": item["translation"],
        "index": index,
        "total": len(phrases)
    })


@app.route('/check', methods=['POST'])
def check():
    data = request.json
    lang = data.get('lang', 'it')
    index = data.get('index', 0)
    user_input = data.get('text', '')

    phrases = DATA.get(lang, DATA['it'])
    item = phrases[index]
    original = item["phrase"]
    translation = item["translation"]

    orig_clean = original.strip()
    user_clean = user_input.strip()

    diff = list(difflib.ndiff(user_clean, orig_clean))

    comparison_result = []
    for char in diff:
        code = char[0]
        value = char[2]
        if code == ' ':
            comparison_result.append({"char": value, "status": "correct"})
        elif code == '-':
            comparison_result.append({"char": value, "status": "extra"})
        elif code == '+':
            comparison_result.append({"char": value, "status": "missing"})

    is_perfect = orig_clean.lower() == user_clean.lower()

    return jsonify({
        "is_perfect": is_perfect,
        "original": original,
        "translation": translation,
        "user_input": user_input,
        "comparison": comparison_result
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)