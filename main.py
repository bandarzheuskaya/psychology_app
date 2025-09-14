import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ===== НАСТРОЙКА СТРАНИЦЫ =====
st.set_page_config(
    page_title="PsychoTest Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== СТИЛИ ДЛЯ КРАСОТЫ =====
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #6a5acd;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .theme-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1.5rem 0;
        transition: transform 0.3s ease;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .theme-card:hover {
        transform: translateY(-8px);
    }
.test-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    margin: 1rem 0;
    transition: transform 0.3s ease;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    height: 220px; /* 👈 ФИКСИРОВАННАЯ ВЫСОТА */
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* Кнопка внизу, заголовок и описание сверху */
    overflow: hidden; /* Чтобы ничего не вылезало */
}

.test-card h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    font-weight: bold;
    line-height: 1.3;
}

.test-card p {
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.5;
    flex-grow: 1; /* Занимает всё свободное пространство между заголовком и кнопкой */
    overflow-y: auto; /* 👈 ВКЛЮЧАЕМ СКРОЛЛ ПРИ ПЕРЕПОЛНЕНИИ */
    padding-right: 5px; /* Чтобы скролл не мешал тексту */
    scrollbar-width: thin; /* Для Firefox */
    scrollbar-color: rgba(255,255,255,0.5) transparent; /* Цвет скролла */
}

.test-card p::-webkit-scrollbar {
    width: 6px;
}

.test-card p::-webkit-scrollbar-track {
    background: transparent;
}

.test-card p::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.4);
    border-radius: 3px;
}

.test-card button {
    margin-top: 1rem;
    width: 100%;
}
    .stButton>button {
        background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 12px 25px;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .result-box {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ===== ДАННЫЕ: 7 ТЕМ ПО 3 ТЕСТА КАЖДАЯ =====
THEMES = {
    "delegation": {
        "name": "🔹 Делегирование задач",
        "description": "Оцените, насколько эффективно вы распределяете обязанности",
        "tests": {
            "delegation_test": {
                "title": "📊 Тест на делегирование",
                "description": "16 вопросов о том, как вы распределяете работу",
                "questions": [
                    {"text": "Продолжаете ли вы работать после окончания рабочего дня?", "options": ["Да", "Нет"],
                     "scores": [1, 0]},
                    {"text": "Трудитесь ли вы дольше, чем ваши сотрудники?", "options": ["Да", "Нет"],
                     "scores": [1, 0]},
                    {"text": "Часто ли вы выполняете за других работу, с которой те вполне могли бы справиться сами?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Удается ли вам найти в случае нужды подчиненного или коллегу, который помог бы вам?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {
                        "text": "Знают ли ваш коллега, подчиненный (или ваш шеф) ваши задачи и сферу деятельности достаточно хорошо, чтобы заменить вас, если вы оставите свою работу?",
                        "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Хватает ли вам времени на планирование своих задач и деятельности?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Бывает ли «завален» ваш письменный стол, когда вы возвращаетесь из командировки?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {
                        "text": "Занимаетесь ли вы другими делами и проблемами из той сферы ответственности, которая была закреплена за вами до последнего повышения по службе?",
                        "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Часто ли вы бываете вынуждены откладывать важную задачу, чтобы выполнить другие?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Часто ли вам приходится спешить, чтобы соблюсти важные сроки?", "options": ["Да", "Нет"],
                     "scores": [1, 0]},
                    {"text": "Расходуете ли вы время на рутинную работу, которую могут сделать другие?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Сами ли вы диктуете большую часть своих памятных записок, корреспонденции и отчетов?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Часто ли к вам обращаются по поводу задач, не выполненных вашими подчиненными?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Хватает ли вам времени на общественную и представительскую деятельность?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Стремитесь ли вы к тому, чтобы всюду быть в курсе дел и иметь информацию обо всем?",
                     "options": ["Да", "Нет"], "scores": [1, 0]},
                    {"text": "Стоит ли вам больших усилий придерживаться списка приоритетных дел?",
                     "options": ["Да", "Нет"], "scores": [1, 0]}
                ],
                "interpretation": {
                    (0, 3): {"level": "Отлично!", "emoji": "🏆", "advice": "Вы отлично делегируете полномочия!"},
                    (4, 7): {"level": "Есть резервы", "emoji": "📈",
                             "advice": "У вас еще есть резервы для улучшения и делегирования."},
                    (8, 16): {"level": "Проблема", "emoji": "⚠️",
                              "advice": "Делегирование представляет для вас серьезную проблему — решению которой вы должны уделить первостепенное внимание."}
                }
            },
            "decision_style_test": {  # 👈 НОВЫЙ ТЕСТ — ВТОРОЙ В РАЗДЕЛЕ
                "title": "🎯 Стили принятия решений",
                "description": "25 вопросов. Оцените, насколько вы согласны с утверждениями: от 1 (полностью не согласен) до 5 (полностью согласен).",
                "questions": [
                    {"text": "Принимая решения, я обычно полагаюсь на свою интуицию.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "I"},
                    {"text": "Я редко принимаю важные решения, не посоветовавшись с другими людьми.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "D"},
                    {
                        "text": "Для меня важнее почувствовать, что решение правильное, чем иметь для него рациональное обоснование.",
                        "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                        "scores": [1, 2, 3, 4, 5], "style": "I"},
                    {
                        "text": "Я перепроверяю источники информации, чтобы убедиться в их достоверности, прежде чем принять решение.",
                        "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                        "scores": [1, 2, 3, 4, 5], "style": "R"},
                    {"text": "Я использую советы других людей при принятии своих важных решений.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "D"},
                    {
                        "text": "Я откладываю принятие решений, потому что размышления о них вызывают у меня беспокойство.",
                        "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                        "scores": [1, 2, 3, 4, 5], "style": "A"},
                    {"text": "Я принимаю решения логично и систематично.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "R"},
                    {"text": "При принятии решений я делаю то, что первое приходит в голову.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "S"},
                    {"text": "Я обычно принимаю мгновенные решения.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "S"},
                    {
                        "text": "Мне нравится, когда кто-то направляет меня в нужную сторону, когда я сталкиваюсь с важными решениями.",
                        "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                        "scores": [1, 2, 3, 4, 5], "style": "D"},
                    {"text": "Мой процесс принятия решений требует тщательного обдумывания.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "R"},
                    {"text": "Принимая решение, я доверяю своим внутренним чувствам и реакциям.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "I"},
                    {
                        "text": "Принимая решение, я рассматриваю различные варианты с точки зрения конкретной цели.",
                        "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                        "scores": [1, 2, 3, 4, 5], "style": "R"},
                    {"text": "Я избегаю принятия важных решений, пока не начнутся серьезные давления.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "A"},
                    {"text": "Я часто принимаю импульсивные решения.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "S"},
                    {"text": "При принятии решений я полагаюсь на свои инстинкты.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "I"},
                    {"text": "Я обычно принимаю решения, которые кажутся мне правильными.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "I"},
                    {"text": "Мне часто требуется помощь других людей при принятии важных решений.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "D"},
                    {"text": "Я откладываю принятие решений whenever possible.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "A"},
                    {"text": "Я часто принимаю решения спонтанно, под влиянием момента.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "S"},
                    {"text": "Я часто откладываю принятие важных решений.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "A"},
                    {"text": "Если у меня есть поддержка других, мне легче принимать важные решения.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "D"},
                    {"text": "Я обычно принимаю важные решения, только если я обязан это сделать.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "A"},
                    {"text": "Я быстро принимаю решения.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "S"},
                    {"text": "Обычно у меня есть рациональное обоснование для принятия решений.",
                     "options": ["1 — полностью не согласен", "2", "3 — нейтрально", "4", "5 — полностью согласен"],
                     "scores": [1, 2, 3, 4, 5], "style": "R"}
                ],
                "interpretation": {},
                "style_labels": {
                    "R": "Рациональный",
                    "I": "Интуитивный",
                    "A": "Избегающий",
                    "D": "Зависимый",
                    "S": "Спонтанный"
                },
                "style_descriptions": {
                    "R": "Я принимаю решения логично и систематически.",
                    "A": "Я избегаю принятия важных решений, пока не возникнет давление.",
                    "D": "Я редко принимаю важные решения, не посоветовавшись с другими людьми.",
                    "I": "Принимая решения, я склонен полагаться на свою интуицию.",
                    "S": "Я обычно принимаю мгновенные решения."
                }
            },
            "delegation_team": {
                "title": "👥 Командное делегирование",
                "description": "Как ваша команда воспринимает ваш стиль делегирования?",
                "questions": [
                    {"text": "Подчинённые чувствуют, что им дают возможность расти?",
                     "options": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Команда знает, какие задачи можно выполнять самостоятельно?",
                     "options": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Вы регулярно проверяете прогресс, но не вмешиваетесь в процесс?",
                     "options": ["Никогда", "Редко", "Иногда", "Часто", "Всегда"], "scores": [0, 1, 2, 3, 4]}
                ],
                "interpretation": {
                    (0, 3): {"level": "Низкий уровень", "emoji": "📉",
                             "advice": "Команда не чувствует автономии — нужно менять подход."},
                    (4, 8): {"level": "Средний уровень", "emoji": "⚖️",
                             "advice": "Есть прогресс, но ещё есть место для улучшений."},
                    (9, 12): {"level": "Высокий уровень", "emoji": "🚀",
                              "advice": "Отличная практика делегирования! Команда растёт и развивается."}
                }
            }
        }
    },

    "burnout": {
        "name": "🔥 Выгорание",
        "description": "Оцените уровень эмоционального и физического истощения",
        "tests": {
            "burnout_1": {
                "title": "🩺 Тест на выгорание (Maslach)",
                "description": "15 вопросов по трём шкалам: эмоциональное истощение, цинизм, снижение профессиональной эффективности",
                "questions": [
                    {"text": "Я чувствую себя эмоционально опустошённым.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я стал более циничным по отношению к своей работе.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я чувствую, что моя работа не приносит смысла.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я испытываю усталость даже после отдыха.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я избегаю контактов с коллегами.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я стал менее продуктивным.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]}
                ],
                "interpretation": {
                    (0, 6): {"level": "Норма", "emoji": "😊", "advice": "Вы в хорошей форме!"},
                    (7, 15): {"level": "Риск выгорания", "emoji": "⚠️", "advice": "Обратите внимание на баланс работы и отдыха."},
                    (16, 24): {"level": "Выгорание", "emoji": "🆘", "advice": "Срочно обратитесь к психологу или возьмите отпуск."}
                }
            },
            "burnout_2": {
                "title": "⏳ Тест на хроническую усталость",
                "description": "Оцените, насколько утомляет вас ежедневная рутина",
                "questions": [
                    {"text": "Я просыпаюсь утром без сил.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Мне сложно начать день.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я избегаю социальных встреч из-за усталости.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]}
                ],
                "interpretation": {
                    (0, 3): {"level": "Норма", "emoji": "😊", "advice": "Энергия на месте!"},
                    (4, 8): {"level": "Предвыгорание", "emoji": "🟡", "advice": "Пора пересмотреть режим дня и отдых."},
                    (9, 12): {"level": "Выгорание", "emoji": "🆘", "advice": "Не откладывайте заботу о себе — нужна помощь."}
                }
            },
            "burnout_3": {
                "title": "💡 Мотивация и смысл",
                "description": "На сколько ваша работа имеет для вас смысл?",
                "questions": [
                    {"text": "Я верю, что моя работа имеет значение.", "options": ["Совершенно не согласен", "Не согласен", "Нейтрально", "Согласен", "Полностью согласен"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я горжусь тем, что делаю.", "options": ["Совершенно не согласен", "Не согласен", "Нейтрально", "Согласен", "Полностью согласен"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я чувствую, что мои усилия замечают и ценят.", "options": ["Совершенно не согласен", "Не согласен", "Нейтрально", "Согласен", "Полностью согласен"], "scores": [0, 1, 2, 3, 4]}
                ],
                "interpretation": {
                    (0, 3): {"level": "Потеря смысла", "emoji": "🌑", "advice": "Возможно, пора переосмыслить карьеру или найти новые мотиваторы."},
                    (4, 8): {"level": "Снижение мотивации", "emoji": "⛅", "advice": "Попробуйте изменить задачи или найти новое применение своим навыкам."},
                    (9, 12): {"level": "Глубокий смысл", "emoji": "🌟", "advice": "Вы на правильном пути — сохраняйте баланс!"}
                }
            }
        }
    },

    "leadership": {
        "name": "👑 Лидерство",
        "description": "Оцените свой стиль лидерства и влияние на команду",
        "tests": {
            "leadership_1": {
                "title": "🎯 Стиль лидерства (Goleman)",
                "description": "Какой стиль лидерства вы используете чаще всего?",
                "questions": [
                    {"text": "Я часто даю указания и контролирую детали.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я вдохновляю команду видением и энтузиазмом.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я стараюсь понять потребности каждого члена команды.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я позволяю команде принимать решения.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]}
                ],
                "interpretation": {
                    (0, 4): {"level": "Авторитарный", "emoji": "⚔️", "advice": "Вы эффективны в кризисах, но подавляете инициативу."},
                    (5, 9): {"level": "Вдохновляющий", "emoji": "✨", "advice": "Отличный стиль для роста команды!"},
                    (10, 16): {"level": "Партнёрский", "emoji": "🤝", "advice": "Вы строите доверие и развитие — идеальный баланс."}
                }
            },
            "leadership_2": {
                "title": "🗣️ Коммуникация лидера",
                "description": "Насколько эффективно вы общаетесь с командой?",
                "questions": [
                    {"text": "Я чётко объясняю цели и ожидания.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я слушаю мнение команды, прежде чем принимать решение.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я регулярно даю обратную связь.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]}
                ],
                "interpretation": {
                    (0, 3): {"level": "Низкая эффективность", "emoji": "🔇", "advice": "Команда теряется — улучшите коммуникацию."},
                    (4, 7): {"level": "Средняя", "emoji": "💬", "advice": "Есть основы — работайте над регулярностью и глубиной."},
                    (8, 12): {"level": "Высокая", "emoji": "📣", "advice": "Отличная практика! Это ключ к устойчивому лидерству."}
                }
            },
            "leadership_3": {
                "title": "🌱 Развитие команды",
                "description": "Насколько вы инвестируете в рост своих подчинённых?",
                "questions": [
                    {"text": "Я помогаю сотрудникам ставить личные цели развития.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я предоставляю возможности для обучения и новых проектов.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]},
                    {"text": "Я отмечаю успехи команды и благодарю их.", "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"], "scores": [0, 1, 2, 3, 4]}
                ],
                "interpretation": {
                    (0, 3): {"level": "Недостаточно", "emoji": "🌱", "advice": "Команда не растёт — инвестируйте в людей."},
                    (4, 7): {"level": "Умеренно", "emoji": "🌿", "advice": "Вы делаете немного — увеличьте частоту поддержки."},
                    (8, 12): {"level": "Отлично", "emoji": "🌳", "advice": "Вы формируете будущих лидеров — продолжайте!"}
                }
            }
        }
    },

    "stress": {
        "name": "🌪️ Стресс",
        "description": "Оцените уровень стресса и его источники",
        "tests": {}
    },
    "communication": {
        "name": "💬 Коммуникация",
        "description": "Как вы взаимодействуете с коллегами и клиентами?",
        "tests": {}
    },
    "empathy": {
        "name": "❤️ Эмпатия",
        "description": "Насколько вы способны понимать чувства других?",
        "tests": {}
    },
    "time_management": {
        "name": "⏱️ Управление временем",
        "description": "Насколько эффективно вы планируете и используете своё время?",
        "tests": {}
    }
}

# ===== ФУНКЦИИ =====
def show_main_menu():
    st.markdown('<h1 class="main-header">🧠 PsychoTest Pro</h1>', unsafe_allow_html=True)
    st.write("Выберите тему для прохождения теста:")

    for theme_key, theme_data in THEMES.items():
        with st.container():
            st.markdown(f"""
                <div class="theme-card">
                    <h3>{theme_data['name']}</h3>
                    <p>{theme_data['description']}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Выбрать тему", key=f"btn_theme_{theme_key}"):
                # 👇 ВАЖНО: ОЧИЩАЕМ ВСЁ, ЧТО СВЯЗАНО С ТЕСТАМИ!
                st.session_state.current_theme = theme_key
                if 'current_test' in st.session_state:
                    del st.session_state.current_test
                if 'current_question' in st.session_state:
                    del st.session_state.current_question
                if 'answers' in st.session_state:
                    del st.session_state.answers
                if 'scores' in st.session_state:
                    del st.session_state.scores
                st.rerun()


def show_theme_tests():
    theme_key = st.session_state.current_theme
    theme = THEMES[theme_key]

    st.title(theme["name"])
    st.subheader(theme["description"])
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    tests_list = list(theme["tests"].items())

    for idx, (test_key, test_data) in enumerate(tests_list):
        with [col1, col2, col3][idx % 3]:
            st.markdown(f"""
                <div class="test-card">
                    <h4>{test_data['title']}</h4>
                    <p>{test_data['description']}</p>
                </div>
            """, unsafe_allow_html=True)

            # 👇 КНОПКА — ВНЕ HTML-КАРТОЧКИ, НО ПОД НЕЙ — ЭТО НОРМАЛЬНО!
            if st.button("👉 Пройти тест", key=f"btn_test_{theme_key}_{test_key}"):
                st.session_state.current_test = test_key
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.scores = []
                st.rerun()

    if st.button("← Вернуться к темам"):
        del st.session_state.current_theme
        st.rerun()


def run_test():
    theme_key = st.session_state.current_theme
    test_key = st.session_state.current_test
    test = THEMES[theme_key]["tests"][test_key]
    total_questions = len(test["questions"])
    current_q = st.session_state.current_question

    # Защита от выхода за границы
    if current_q < 0:
        st.session_state.current_question = 0
        st.rerun()
    elif current_q >= total_questions:
        st.session_state.current_question = total_questions - 1
        st.rerun()

    st.title(test["title"])
    st.progress(current_q / total_questions)

    question = test["questions"][current_q]

    st.markdown(f"### Вопрос {current_q + 1} из {total_questions}")
    st.markdown(f"**{question['text']}**")

    # Восстанавливаем предыдущий ответ
    if len(st.session_state.answers) > current_q:
        prev_answer = st.session_state.answers[current_q]
        selected_index = question["options"].index(prev_answer)
    else:
        selected_index = 0

    answer = st.radio(
        "Выберите ответ:",
        question["options"],
        index=selected_index,
        key=f"q{current_q}"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # Кнопка "Назад"
    if current_q > 0:
        with col1:
            if st.button("← Назад", key=f"btn_back_{current_q}", use_container_width=True):
                st.session_state.answers.pop()
                st.session_state.scores.pop()
                st.session_state.current_question -= 1
                st.rerun()

    # Кнопка "Далее" или "Завершить"
    with col2:
        if current_q == total_questions - 1:
            btn_text = "✅ Завершить тест"
        else:
            btn_text = "→ Следующий вопрос"

        if st.button(btn_text, key=f"btn_next_{current_q}", use_container_width=True):
            score_index = question["options"].index(answer)
            if len(st.session_state.answers) > current_q:
                st.session_state.answers[current_q] = answer
                st.session_state.scores[current_q] = question["scores"][score_index]
            else:
                st.session_state.answers.append(answer)
                st.session_state.scores.append(question["scores"][score_index])

            # ⚠️ Не увеличиваем current_question, если это последний вопрос
            if current_q == total_questions - 1:
                # Переходим к результатам — не реран, а изменяем состояние
                st.session_state.current_question = total_questions  # Условно "завершено"
                st.rerun()
            else:
                st.session_state.current_question += 1
                st.rerun()

def show_results(theme_key, test_key):
    test = THEMES[theme_key]["tests"][test_key]
    total_score = sum(st.session_state.scores)
    max_possible = len(test["questions"]) * max(test["questions"][0]["scores"])  # Максимальный балл

    # Находим интерпретацию
    result = None
    for score_range, interpretation in test["interpretation"].items():
        if score_range[0] <= total_score <= score_range[1]:
            result = interpretation
            break

    # Показываем красивые результаты
    st.balloons()
    st.markdown(f"""
        <div class="result-box">
            <h2>{result['emoji']} Ваш результат: {total_score} из {max_possible} баллов</h2>
            <h3>{result['level']}</h3>
            <p>{result['advice']}</p>
        </div>
    """, unsafe_allow_html=True)

    # ===== НОВАЯ ШКАЛА =====
    st.markdown("### 📊 Визуализация результата")

    # Определяем цвета по диапазонам
    if max_possible == 16:  # Для теста на делегирование
        low_end = 3
        medium_end = 7
    else:
        # Автоматически определяем границы на основе интерпретаций
        ranges = list(test["interpretation"].keys())
        low_end = ranges[0][1]  # Верхняя граница первого диапазона
        medium_end = ranges[1][1]  # Верхняя граница второго

    # Рассчитываем процент
    percentage = min(100, (total_score / max_possible) * 100)

    # Цветовая шкала: зелёный → жёлтый → красный
    if percentage <= (low_end / max_possible) * 100:
        color = "#4CAF50"  # Зелёный
    elif percentage <= (medium_end / max_possible) * 100:
        color = "#FFC107"  # Жёлтый
    else:
        color = "#F44336"  # Красный

    # Создаём HTML-шкалу
    st.markdown(f"""
        <div style="
            background-color: #e0e0e0;
            height: 30px;
            border-radius: 15px;
            position: relative;
            margin: 20px 0;
            overflow: hidden;
            width: 100%;
        ">
            <div style="
                background: linear-gradient(90deg, #4CAF50, #FFC107, #F44336);
                height: 100%;
                width: {percentage}%;
                border-radius: 15px;
                transition: width 1s ease-in-out;
            "></div>
            <div style="
                position: absolute;
                top: 50%;
                left: {percentage}%;
                transform: translateX(-50%) translateY(-50%);
                color: white;
                font-weight: bold;
                font-size: 14px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
                padding: 0 8px;
                background: rgba(0,0,0,0.3);
                border-radius: 15px;
            ">{total_score}/{max_possible}</div>
        </div>
    """, unsafe_allow_html=True)

    # Подпись под шкалой
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div style='text-align: center; color: #4CAF50;'>🔹 Низкий<br>({0}-{low_end})</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: center; color: #FFC107;'>🟡 Средний<br>({low_end+1}-{medium_end})</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align: center; color: #F44336;'>🔴 Высокий<br>({medium_end+1}-{max_possible})</div>", unsafe_allow_html=True)

    # ===== Таблица ответов =====
    st.write("### 📝 Ваши ответы:")
    results_df = pd.DataFrame({
        'Вопрос': [q['text'] for q in test['questions']],
        'Ответ': st.session_state.answers,
        'Баллы': st.session_state.scores
    })
    st.dataframe(results_df, use_container_width=True)

    if st.button("🔄 Выбрать другой тест"):
        for key in ['current_theme', 'current_test', 'current_question', 'answers', 'scores']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def show_results1(theme_key, test_key):
    test = THEMES[theme_key]["tests"][test_key]
    total_questions = len(test["questions"])

    # Считаем баллы по стилям — только если есть поле "style"
    style_scores = {"R": 0, "I": 0, "A": 0, "D": 0, "S": 0}
    has_style = False

    for i in range(total_questions):
        score = st.session_state.scores[i]
        question = test["questions"][i]
        if "style" in question:
            style = question["style"]
            if style in style_scores:
                style_scores[style] += score
            else:
                print(f"Неизвестный стиль: {style}")
        has_style = True  # Если хотя бы один вопрос имеет style — значит, это тест со стилями

    # Находим доминирующий стиль
    if has_style:
        dominant_style = max(style_scores, key=style_scores.get)
        max_score = style_scores[dominant_style]
        total_possible = 25  # Фиксировано: 25 вопросов × 1 балл максимум
        avg_score = sum(style_scores.values()) / len(style_scores)

        # Получаем описание доминирующего стиля
        style_name = test.get("style_labels", {}).get(dominant_style, "Неизвестный стиль")
        style_desc = test.get("style_descriptions", {}).get(dominant_style, "Описание отсутствует")

        # Показываем результаты
        st.balloons()
        st.markdown(f"""
            <div class="result-box">
                <h2>🎯 Ваш доминирующий стиль принятия решений</h2>
                <h3>{style_name} ({max_score}/{total_possible})</h3>
                <p><em>"{style_desc}"</em></p>
            </div>
        """, unsafe_allow_html=True)

        # ===== ВИЗУАЛИЗАЦИЯ: ГОРИЗОНТАЛЬНЫЕ ШКАЛЫ ПО КАЖДОМУ СТИЛЮ =====
        st.markdown("### 📊 Распределение стилей (баллы из 25)")

        for style_code, score in style_scores.items():
            label = test.get("style_labels", {}).get(style_code, style_code)
            percentage = min(100, (score / total_possible) * 100)

            # Цветовая шкала: 0–8 = красный, 9–16 = жёлтый, 17–25 = зелёный
            if percentage <= 32:   # ≤ 8 баллов
                color = "#F44336"  # Красный
            elif percentage <= 64: # ≤ 16 баллов
                color = "#FFC107"  # Жёлтый
            else:                  # >16 баллов
                color = "#4CAF50"  # Зелёный

            # Создаём HTML-шкалу
            st.markdown(f"""
                <div style="
                    background-color: #e0e0e0;
                    height: 20px;
                    border-radius: 10px;
                    margin: 10px 0;
                    position: relative;
                    width: 100%;
                ">
                    <div style="
                        background: {color};
                        height: 100%;
                        width: {percentage}%;
                        border-radius: 10px;
                        transition: width 1s ease-in-out;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 50%;
                        left: {percentage}%;
                        transform: translateX(-50%) translateY(-50%);
                        color: white;
                        font-weight: bold;
                        font-size: 14px;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
                        padding: 0 8px;
                        background: rgba(0,0,0,0.3);
                        border-radius: 15px;
                    ">{score}/{total_possible}</div>
                </div>
                <p style="margin: 5px 0; font-weight: 500; color: white;">{label}</p>
            """, unsafe_allow_html=True)

        # ===== ПОДРОБНАЯ ИНТЕРПРЕТАЦИЯ =====
        st.markdown("### 🔍 Подробная интерпретация")

        for style_code, score in style_scores.items():
            label = test.get("style_labels", {}).get(style_code, style_code)
            description = test.get("style_descriptions", {}).get(style_code, "Описание отсутствует")
            is_dominant = "✅ **ДОМИНИРУЮЩИЙ**" if style_code == dominant_style else ""
            st.markdown(f"""
                **{label}** — {score}/25<br>
                _"{description}"_ {is_dominant}
                """, unsafe_allow_html=True)

    else:
        # Если нет стилей — показываем простой результат
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0

        # Найди интерпретацию
        result = None
        for score_range, interpretation in test["interpretation"].items():
            if score_range[0] <= total_score <= score_range[1]:
                result = interpretation
                break

        if not result:
            result = {"level": "Не определено", "emoji": "❓", "advice": "Результат не интерпретируется."}

        st.balloons()
        st.markdown(f"""
            <div class="result-box">
                <h2>{result['emoji']} Ваш результат: {total_score} из {max_possible} баллов</h2>
                <h3>{result['level']}</h3>
                <p>{result['advice']}</p>
            </div>
        """, unsafe_allow_html=True)

        # ===== ШКАЛА =====
        percentage = min(100, (total_score / max_possible) * 100)
        st.markdown(f"""
            <div style="
                background-color: #e0e0e0;
                height: 30px;
                border-radius: 15px;
                position: relative;
                margin: 20px 0;
                overflow: hidden;
                width: 100%;
            ">
                <div style="
                    background: linear-gradient(90deg, #4CAF50, #FFC107, #F44336);
                    height: 100%;
                    width: {percentage}%;
                    border-radius: 15px;
                    transition: width 1s ease-in-out;
                "></div>
                <div style="
                    position: absolute;
                    top: 50%;
                    left: {percentage}%;
                    transform: translateX(-50%) translateY(-50%);
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
                    padding: 0 8px;
                    background: rgba(0,0,0,0.3);
                    border-radius: 15px;
                ">{total_score}/{max_possible}</div>
            </div>
        """, unsafe_allow_html=True)

    # ===== ТАБЛИЦА ОТВЕТОВ =====
    st.markdown("### 📝 Ваши ответы:")
    results_df = pd.DataFrame({
        'Вопрос': [q['text'] for q in test['questions']],
        'Ответ': st.session_state.answers,
        'Баллы': st.session_state.scores,
        'Стиль': [q.get('style', '—') for q in test['questions']]  # Безопасно получаем style
    })
    st.dataframe(results_df, use_container_width=True)

    if st.button("🔄 Выбрать другой тест"):
        for key in ['current_theme', 'current_test', 'current_question', 'answers', 'scores']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# ===== ЗАПУСК ПРИЛОЖЕНИЯ =====
def main():
    if 'current_theme' not in st.session_state:
        show_main_menu()
    elif 'current_test' not in st.session_state:
        show_theme_tests()
    else:
        # Получаем текущий тест
        theme_key = st.session_state.current_theme
        test_key = st.session_state.current_test
        test = THEMES[theme_key]["tests"][test_key]
        total_questions = len(test["questions"])

        # Проверяем, завершен ли тест
        if 'current_question' not in st.session_state or st.session_state.current_question >= total_questions:
            # ✅ ВЫБОР ФУНКЦИИ РЕЗУЛЬТАТОВ В ЗАВИСИМОСТИ ОТ ТЕСТА
            if test_key == "decision_style_test":
                show_results1(theme_key, test_key)
            else:
                show_results(theme_key, test_key)
        else:
            run_test()


if __name__ == "__main__":
    main()
