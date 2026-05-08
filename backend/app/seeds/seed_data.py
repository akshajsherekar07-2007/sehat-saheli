"""
Seed data for Phase 2 features — quiz, learn, flashcards.
Run: python -m app.seeds.seed_data
"""

import asyncio
import uuid

from sqlalchemy import select

from app.core.database import async_session_factory
from app.models.quiz import Quiz, QuizCategory
from app.models.learn import LearnCategory, LearnArticle
from app.models.flashcard import FlashcardDeck, Flashcard


def uid():
    return str(uuid.uuid4())


QUIZ_DATA = [
    {
        "name": "Menstrual Health",
        "slug": "menstrual-health",
        "description": "Test your knowledge about periods and menstrual cycle",
        "questions": [
            {
                "question": {"en": "What is the average length of a menstrual cycle?", "hi": "मासिक धर्म चक्र की औसत लंबाई क्या है?"},
                "options": {"en": ["14 days", "21 days", "28 days", "35 days"], "hi": ["14 दिन", "21 दिन", "28 दिन", "35 दिन"]},
                "correct_option": 2,
                "difficulty": "easy",
            },
            {
                "question": {"en": "Which hormone triggers ovulation?", "hi": "कौन सा हार्मोन ओव्यूलेशन को ट्रिगर करता है?"},
                "options": {"en": ["Estrogen", "Luteinizing Hormone (LH)", "Progesterone", "Testosterone"], "hi": ["एस्ट्रोजन", "ल्यूटिनाइजिंग हार्मोन (LH)", "प्रोजेस्टेरोन", "टेस्टोस्टेरोन"]},
                "correct_option": 1,
                "difficulty": "medium",
            },
            {
                "question": {"en": "How long does a typical period last?", "hi": "एक सामान्य माहवारी कितने दिन तक चलती है?"},
                "options": {"en": ["1-2 days", "3-7 days", "10-14 days", "15-20 days"], "hi": ["1-2 दिन", "3-7 दिन", "10-14 दिन", "15-20 दिन"]},
                "correct_option": 1,
                "difficulty": "easy",
            },
        ],
    },
    {
        "name": "Nutrition & Diet",
        "slug": "nutrition",
        "description": "Learn about healthy eating habits for growing bodies",
        "questions": [
            {
                "question": {"en": "Which nutrient is essential for strong bones?", "hi": "मजबूत हड्डियों के लिए कौन सा पोषक तत्व आवश्यक है?"},
                "options": {"en": ["Vitamin C", "Iron", "Calcium", "Vitamin B12"], "hi": ["विटामिन C", "आयरन", "कैल्शियम", "विटामिन B12"]},
                "correct_option": 2,
                "difficulty": "easy",
            },
            {
                "question": {"en": "Which food is the richest source of iron?", "hi": "किस भोजन में सबसे ज्यादा आयरन होता है?"},
                "options": {"en": ["Rice", "Spinach", "Bread", "Milk"], "hi": ["चावल", "पालक", "रोटी", "दूध"]},
                "correct_option": 1,
                "difficulty": "easy",
            },
            {
                "question": {"en": "How many glasses of water should you drink daily?", "hi": "आपको रोजाना कितने गिलास पानी पीना चाहिए?"},
                "options": {"en": ["2-3 glasses", "4-5 glasses", "8-10 glasses", "15+ glasses"], "hi": ["2-3 गिलास", "4-5 गिलास", "8-10 गिलास", "15+ गिलास"]},
                "correct_option": 2,
                "difficulty": "easy",
            },
        ],
    },
    {
        "name": "Personal Hygiene",
        "slug": "hygiene",
        "description": "Quiz on cleanliness and personal care practices",
        "questions": [
            {
                "question": {"en": "How often should you change a sanitary pad?", "hi": "सैनिटरी पैड कितनी बार बदलना चाहिए?"},
                "options": {"en": ["Every 12 hours", "Every 4-6 hours", "Once a day", "Every 2 days"], "hi": ["हर 12 घंटे", "हर 4-6 घंटे", "दिन में एक बार", "हर 2 दिन"]},
                "correct_option": 1,
                "difficulty": "easy",
            },
            {
                "question": {"en": "What is the best way to wash your hands?", "hi": "हाथ धोने का सबसे अच्छा तरीका क्या है?"},
                "options": {"en": ["Quick rinse", "Soap and water for 20 seconds", "Just sanitizer", "Wipe on clothes"], "hi": ["जल्दी से धोना", "20 सेकंड तक साबुन और पानी", "सिर्फ सैनिटाइज़र", "कपड़ों पर पोंछना"]},
                "correct_option": 1,
                "difficulty": "easy",
            },
        ],
    },
]

LEARN_DATA = [
    {
        "name": "Understanding Your Body",
        "slug": "body",
        "icon": "Heart",
        "articles": [
            {
                "title": {"en": "What is Puberty?", "hi": "यौवन क्या है?"},
                "content": {"en": "Puberty is the time in life when your body begins to change and develop from a child into an adult. For girls, this usually starts between ages 8-13. During puberty, you may notice your body growing taller, developing breasts, growing body hair, and eventually starting your menstrual period.\n\nThese changes are completely normal and happen to every girl! Your body is preparing for adulthood, and it's important to understand these changes so you can take care of yourself.\n\n**Key changes during puberty:**\n- Growth spurts (getting taller)\n- Breast development\n- Body hair growth\n- Skin changes (sometimes acne)\n- Menstruation begins\n- Emotional changes", "hi": "यौवन जीवन का वह समय है जब आपका शरीर बच्चे से वयस्क में बदलने लगता है..."},
                "content_type": "article",
            },
            {
                "title": {"en": "The Menstrual Cycle Explained", "hi": "मासिक धर्म चक्र की व्याख्या"},
                "content": {"en": "The menstrual cycle is a monthly process that your body goes through to prepare for pregnancy. The average cycle lasts about 28 days, but it can range from 21-35 days.\n\n**Phase 1: Menstruation (Day 1-5)**\nThis is your period — the uterine lining sheds through the vagina.\n\n**Phase 2: Follicular Phase (Day 1-13)**\nYour body prepares an egg for release. Estrogen levels rise.\n\n**Phase 3: Ovulation (Day 14)**\nAn egg is released from the ovary.\n\n**Phase 4: Luteal Phase (Day 15-28)**\nThe body prepares for possible pregnancy. If the egg isn't fertilized, hormone levels drop and the cycle restarts.", "hi": "मासिक धर्म चक्र एक मासिक प्रक्रिया है..."},
                "content_type": "article",
            },
        ],
    },
    {
        "name": "Nutrition & Health",
        "slug": "nutrition",
        "icon": "Apple",
        "articles": [
            {
                "title": {"en": "Iron-Rich Foods for Girls", "hi": "लड़कियों के लिए आयरन युक्त भोजन"},
                "content": {"en": "Iron is especially important for girls because you lose iron during your period. Not having enough iron can make you feel tired, dizzy, and weak — this is called anemia.\n\n**Iron-rich foods to eat daily:**\n- 🥬 Green leafy vegetables (spinach, fenugreek)\n- 🫘 Lentils and beans (dal, rajma)\n- 🥜 Nuts and seeds (almonds, sesame)\n- 🍎 Fruits (pomegranate, dates, figs)\n- 🥚 Eggs\n- 🍖 Lean meat (if non-vegetarian)\n\n**Tips to absorb more iron:**\n- Eat Vitamin C foods (lemon, orange) with iron-rich meals\n- Avoid tea/coffee during meals\n- Cook in iron utensils", "hi": "लड़कियों के लिए आयरन बहुत महत्वपूर्ण है..."},
                "content_type": "article",
            },
        ],
    },
    {
        "name": "Hygiene & Self-Care",
        "slug": "hygiene",
        "icon": "Sparkles",
        "articles": [
            {
                "title": {"en": "Menstrual Hygiene: A Complete Guide", "hi": "मासिक धर्म स्वच्छता: एक संपूर्ण गाइड"},
                "content": {"en": "Good menstrual hygiene is essential for your health and comfort during periods.\n\n**Choosing the right product:**\n- Sanitary pads (most common in India)\n- Menstrual cups (reusable, eco-friendly)\n- Cloth pads (reusable, budget-friendly)\n\n**Important hygiene practices:**\n- Change pads every 4-6 hours\n- Wash hands before and after changing pads\n- Clean the genital area with water (front to back)\n- Dispose of used pads properly (wrap in paper)\n- Bath/shower daily during periods\n- Wear clean, cotton underwear", "hi": "अच्छी मासिक धर्म स्वच्छता आपके स्वास्थ्य के लिए जरूरी है..."},
                "content_type": "article",
            },
        ],
    },
]

FLASHCARD_DATA = [
    {
        "name": "Body Basics",
        "slug": "body-basics",
        "description": "Learn key facts about your body",
        "category": "health",
        "cards": [
            {"front": {"en": "What is menstruation?", "hi": "मासिक धर्म क्या है?"}, "back": {"en": "The monthly shedding of the uterine lining through the vagina. It's a normal, healthy process that happens to all girls.", "hi": "गर्भाशय की परत का मासिक रूप से योनि के माध्यम से बहना।"}},
            {"front": {"en": "What is ovulation?", "hi": "ओव्यूलेशन क्या है?"}, "back": {"en": "The release of a mature egg from the ovary, usually around day 14 of the menstrual cycle.", "hi": "अंडाशय से एक परिपक्व अंडे का निकलना, आमतौर पर मासिक चक्र के 14वें दिन।"}},
            {"front": {"en": "What causes period cramps?", "hi": "पीरियड क्रैम्प्स का कारण क्या है?"}, "back": {"en": "Prostaglandins — chemicals that cause the uterus to contract and shed its lining. Gentle exercise and warm compresses can help!", "hi": "प्रोस्टाग्लैंडिंस — रसायन जो गर्भाशय को सिकुड़ने और अपनी परत को बहाने का कारण बनते हैं।"}},
            {"front": {"en": "How much blood is lost during a period?", "hi": "पीरियड के दौरान कितना खून बहता है?"}, "back": {"en": "About 2-3 tablespoons (30-40 ml) on average. It may seem like more, but it's mostly tissue and fluids.", "hi": "औसतन लगभग 2-3 बड़े चम्मच (30-40 मिलीलीटर)।"}},
        ],
    },
    {
        "name": "Nutrition Facts",
        "slug": "nutrition-facts",
        "description": "Key nutrition knowledge for growing girls",
        "category": "nutrition",
        "cards": [
            {"front": {"en": "Why is iron important for girls?", "hi": "लड़कियों के लिए आयरन क्यों जरूरी है?"}, "back": {"en": "Girls lose iron during menstruation. Iron helps carry oxygen in the blood. Low iron causes anemia — tiredness, weakness, dizziness.", "hi": "लड़कियां मासिक धर्म के दौरान आयरन खोती हैं। कम आयरन एनीमिया का कारण बनता है।"}},
            {"front": {"en": "What is calcium needed for?", "hi": "कैल्शियम किसके लिए जरूरी है?"}, "back": {"en": "Strong bones and teeth! During your teens, you build most of your bone mass. Eat dairy, leafy greens, and fortified foods.", "hi": "मजबूत हड्डियां और दांत! अपनी किशोरावस्था में आप अपनी हड्डियों का अधिकतर भाग बनाते हैं।"}},
            {"front": {"en": "Name 3 iron-rich Indian foods", "hi": "3 आयरन युक्त भारतीय खाद्य पदार्थों के नाम बताइए"}, "back": {"en": "1. Spinach (palak)\n2. Lentils (dal)\n3. Jaggery (gur)\n\nBonus: Pomegranate, dates, sesame seeds!", "hi": "1. पालक\n2. दाल\n3. गुड़\n\nबोनस: अनार, खजूर, तिल!"}},
        ],
    },
]


async def seed():
    """Insert seed data into the database."""
    async with async_session_factory() as db:
        # Check if already seeded
        existing = await db.execute(select(QuizCategory).limit(1))
        if existing.scalar_one_or_none():
            print("⚠️  Data already seeded, skipping.")
            return

        print("🌱 Seeding quiz data...")
        for cat_data in QUIZ_DATA:
            cat_id = uid()
            cat = QuizCategory(id=cat_id, name=cat_data["name"], slug=cat_data["slug"], description=cat_data["description"])
            db.add(cat)
            for q in cat_data["questions"]:
                db.add(Quiz(id=uid(), category_id=cat_id, **q))

        print("📚 Seeding learn data...")
        for cat_data in LEARN_DATA:
            cat_id = uid()
            cat = LearnCategory(id=cat_id, name=cat_data["name"], slug=cat_data["slug"], icon=cat_data["icon"])
            db.add(cat)
            for i, a in enumerate(cat_data["articles"]):
                db.add(LearnArticle(id=uid(), category_id=cat_id, order_index=i, **a))

        print("🃏 Seeding flashcard data...")
        for deck_data in FLASHCARD_DATA:
            deck_id = uid()
            db.add(FlashcardDeck(id=deck_id, name=deck_data["name"], slug=deck_data["slug"], description=deck_data["description"], category=deck_data["category"]))
            for i, card in enumerate(deck_data["cards"]):
                db.add(Flashcard(id=uid(), deck_id=deck_id, order_index=i, front=card["front"], back=card["back"]))

        await db.commit()
        print("✅ Seed data inserted successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
