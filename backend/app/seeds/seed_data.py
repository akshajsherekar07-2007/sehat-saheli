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


# ── QUIZ DATA ────────────────────────────────────────────────────

QUIZ_DATA = [
    {
        "name": "Menstrual Health", "slug": "menstrual-health",
        "description": "Test your knowledge about periods and menstrual cycle",
        "questions": [
            {"question": {"en": "What is the average length of a menstrual cycle?"}, "options": {"en": ["14 days", "21 days", "28 days", "35 days"]}, "correct_option": 2, "difficulty": "easy"},
            {"question": {"en": "Which hormone triggers ovulation?"}, "options": {"en": ["Estrogen", "Luteinizing Hormone (LH)", "Progesterone", "Testosterone"]}, "correct_option": 1, "difficulty": "medium"},
            {"question": {"en": "How long does a typical period last?"}, "options": {"en": ["1-2 days", "3-7 days", "10-14 days", "15-20 days"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "What is the uterine lining called?"}, "options": {"en": ["Cervix", "Endometrium", "Fallopian tube", "Ovary"]}, "correct_option": 1, "difficulty": "medium"},
            {"question": {"en": "At what age do most girls get their first period?"}, "options": {"en": ["6-8 years", "9-14 years", "16-18 years", "19-21 years"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "What is menarche?"}, "options": {"en": ["End of periods", "First period ever", "Heaviest day", "Ovulation day"]}, "correct_option": 1, "difficulty": "medium"},
            {"question": {"en": "Which phase comes after ovulation?"}, "options": {"en": ["Menstruation", "Follicular phase", "Luteal phase", "Puberty"]}, "correct_option": 2, "difficulty": "hard"},
            {"question": {"en": "Period pain is caused by which chemical?"}, "options": {"en": ["Insulin", "Adrenaline", "Prostaglandins", "Serotonin"]}, "correct_option": 2, "difficulty": "hard"},
        ],
    },
    {
        "name": "Nutrition & Diet", "slug": "nutrition",
        "description": "Learn about healthy eating habits for growing bodies",
        "questions": [
            {"question": {"en": "Which nutrient is essential for strong bones?"}, "options": {"en": ["Vitamin C", "Iron", "Calcium", "Vitamin B12"]}, "correct_option": 2, "difficulty": "easy"},
            {"question": {"en": "Which food is the richest source of iron?"}, "options": {"en": ["Rice", "Spinach", "Bread", "Milk"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "How many glasses of water should you drink daily?"}, "options": {"en": ["2-3 glasses", "4-5 glasses", "8-10 glasses", "15+ glasses"]}, "correct_option": 2, "difficulty": "easy"},
            {"question": {"en": "Which vitamin helps absorb iron better?"}, "options": {"en": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"]}, "correct_option": 2, "difficulty": "medium"},
            {"question": {"en": "What condition is caused by low iron?"}, "options": {"en": ["Diabetes", "Anemia", "Asthma", "Arthritis"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "Which is a good source of protein for vegetarians?"}, "options": {"en": ["White rice", "Dal (lentils)", "Tea", "Sugar"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "Vitamin D is best obtained from?"}, "options": {"en": ["Moonlight", "Sunlight", "Tubelight", "Candlelight"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "Jaggery (gur) is rich in which mineral?"}, "options": {"en": ["Zinc", "Calcium", "Iron", "Sodium"]}, "correct_option": 2, "difficulty": "medium"},
        ],
    },
    {
        "name": "Personal Hygiene", "slug": "hygiene",
        "description": "Quiz on cleanliness and personal care practices",
        "questions": [
            {"question": {"en": "How often should you change a sanitary pad?"}, "options": {"en": ["Every 12 hours", "Every 4-6 hours", "Once a day", "Every 2 days"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "What is the best way to wash your hands?"}, "options": {"en": ["Quick rinse", "Soap and water for 20 seconds", "Just sanitizer", "Wipe on clothes"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "Which direction should you clean the genital area?"}, "options": {"en": ["Back to front", "Front to back", "Side to side", "Any direction"]}, "correct_option": 1, "difficulty": "medium"},
            {"question": {"en": "How often should you shower during periods?"}, "options": {"en": ["Not at all", "Once a week", "Daily", "Every other day"]}, "correct_option": 2, "difficulty": "easy"},
            {"question": {"en": "What type of underwear is best during periods?"}, "options": {"en": ["Silk", "Nylon", "Cotton", "Polyester"]}, "correct_option": 2, "difficulty": "easy"},
            {"question": {"en": "How should used pads be disposed?"}, "options": {"en": ["Flush in toilet", "Wrap in paper and bin", "Throw openly", "Burn directly"]}, "correct_option": 1, "difficulty": "easy"},
        ],
    },
    {
        "name": "Puberty & Growth", "slug": "puberty",
        "description": "Understanding the changes during adolescence",
        "questions": [
            {"question": {"en": "At what age does puberty typically start for girls?"}, "options": {"en": ["5-7 years", "8-13 years", "15-18 years", "20-25 years"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "What is the first sign of puberty in most girls?"}, "options": {"en": ["Periods start", "Breast development", "Voice change", "Facial hair"]}, "correct_option": 1, "difficulty": "medium"},
            {"question": {"en": "Growth spurts during puberty are caused by?"}, "options": {"en": ["Eating more", "Growth hormones", "Sleeping less", "Exercise only"]}, "correct_option": 1, "difficulty": "medium"},
            {"question": {"en": "Acne during puberty is caused by?"}, "options": {"en": ["Dirty skin only", "Hormonal changes", "Eating sweets", "Cold weather"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "Is mood swing during puberty normal?"}, "options": {"en": ["No, never", "Yes, completely normal", "Only for boys", "Only after 18"]}, "correct_option": 1, "difficulty": "easy"},
        ],
    },
    {
        "name": "Mental Health", "slug": "mental-health",
        "description": "Understanding emotions, stress, and well-being",
        "questions": [
            {"question": {"en": "What is a healthy way to deal with stress?"}, "options": {"en": ["Bottling up feelings", "Talking to someone you trust", "Skipping meals", "Staying alone always"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "How many hours of sleep do teenagers need?"}, "options": {"en": ["4-5 hours", "6-7 hours", "8-10 hours", "12+ hours"]}, "correct_option": 2, "difficulty": "easy"},
            {"question": {"en": "Which activity can improve mental health?"}, "options": {"en": ["Excessive screen time", "Regular exercise", "Skipping school", "Isolating yourself"]}, "correct_option": 1, "difficulty": "easy"},
            {"question": {"en": "Feeling sad during periods is?"}, "options": {"en": ["Abnormal", "A sign of weakness", "Normal due to hormones", "Dangerous"]}, "correct_option": 2, "difficulty": "easy"},
        ],
    },
]

# ── LEARN DATA ───────────────────────────────────────────────────

LEARN_DATA = [
    {
        "name": "Understanding Your Body", "slug": "body", "icon": "Heart",
        "articles": [
            {
                "title": {"en": "What is Puberty?"},
                "content": {"en": "Puberty is the time in life when your body begins to change and develop from a child into an adult. For girls, this usually starts between ages 8-13.\n\nDuring puberty, you may notice your body growing taller, developing breasts, growing body hair, and eventually starting your menstrual period.\n\nThese changes are completely normal and happen to every girl!\n\n**Key changes during puberty:**\n- Growth spurts (getting taller)\n- Breast development\n- Body hair growth\n- Skin changes (sometimes acne)\n- Menstruation begins\n- Emotional changes\n- Wider hips\n- Body odor increases"},
                "content_type": "article",
            },
            {
                "title": {"en": "The Menstrual Cycle Explained"},
                "content": {"en": "The menstrual cycle is a monthly process that your body goes through. The average cycle lasts about 28 days, but 21-35 days is normal.\n\n**Phase 1: Menstruation (Day 1-5)**\nYour period — the uterine lining sheds.\n\n**Phase 2: Follicular Phase (Day 1-13)**\nYour body prepares an egg. Estrogen rises.\n\n**Phase 3: Ovulation (Day 14)**\nAn egg is released from the ovary.\n\n**Phase 4: Luteal Phase (Day 15-28)**\nThe body prepares for possible pregnancy. If the egg isn't fertilized, hormone levels drop and the cycle restarts.\n\n**Remember:** Every girl's cycle is different, and irregular periods are common in the first 2 years!"},
                "content_type": "article",
            },
            {
                "title": {"en": "Understanding Your Reproductive System"},
                "content": {"en": "The female reproductive system includes several important organs:\n\n**Ovaries** — Two small organs that store eggs and produce hormones (estrogen, progesterone).\n\n**Fallopian Tubes** — Connect the ovaries to the uterus. This is where fertilization happens.\n\n**Uterus (Womb)** — A muscular organ where a baby grows. The lining (endometrium) sheds during your period.\n\n**Cervix** — The lower part of the uterus that connects to the vagina.\n\n**Vagina** — The canal that connects the uterus to the outside of the body.\n\nKnowing your body helps you understand what's normal and when to seek help from a doctor."},
                "content_type": "article",
            },
            {
                "title": {"en": "Dealing with Period Cramps"},
                "content": {"en": "Period cramps (dysmenorrhea) are very common and usually not a cause for concern.\n\n**Why do cramps happen?**\nYour uterus contracts to shed its lining. Chemicals called prostaglandins cause these contractions.\n\n**Natural remedies:**\n- 🔥 Place a hot water bottle on your lower belly\n- 🚶‍♀️ Light exercise or walking\n- 🧘 Gentle yoga stretches\n- 🍵 Warm drinks (ginger tea, warm water)\n- 😴 Rest when needed\n- 🍌 Eat potassium-rich foods (bananas)\n\n**When to see a doctor:**\n- Pain is so severe you can't do daily activities\n- Heavy bleeding (soaking a pad in 1 hour)\n- Cramps last longer than your period\n- You have a fever during periods"},
                "content_type": "article",
            },
        ],
    },
    {
        "name": "Nutrition & Health", "slug": "nutrition", "icon": "Apple",
        "articles": [
            {
                "title": {"en": "Iron-Rich Foods for Girls"},
                "content": {"en": "Iron is especially important for girls because you lose iron during your period.\n\n**Iron-rich foods to eat daily:**\n- 🥬 Green leafy vegetables (spinach, fenugreek)\n- 🫘 Lentils and beans (dal, rajma, chole)\n- 🥜 Nuts and seeds (almonds, sesame, pumpkin seeds)\n- 🍎 Fruits (pomegranate, dates, figs, raisins)\n- 🥚 Eggs\n- 🫙 Jaggery (gur)\n\n**Tips to absorb more iron:**\n- Eat Vitamin C foods (lemon, orange, amla) with iron-rich meals\n- Avoid tea/coffee during meals — they block iron absorption\n- Cook in iron utensils (kadai, tawa)"},
                "content_type": "article",
            },
            {
                "title": {"en": "Building a Balanced Diet"},
                "content": {"en": "A balanced diet gives your growing body everything it needs.\n\n**Your plate should include:**\n\n🌾 **Carbohydrates (Energy)** — Roti, rice, oats, potatoes\n🥗 **Proteins (Growth)** — Dal, paneer, eggs, soybean, chicken\n🥬 **Vitamins & Minerals** — Fruits and vegetables of all colors\n🥛 **Calcium (Bones)** — Milk, curd, cheese, ragi\n💧 **Water** — 8-10 glasses daily\n\n**Healthy eating tips:**\n- Eat breakfast every day — never skip it!\n- Include one fruit and one vegetable in every meal\n- Snack on nuts, sprouts, or fruit instead of chips\n- Reduce sugary drinks — choose water, buttermilk, or nimbu pani\n- Eat home-cooked food as much as possible"},
                "content_type": "article",
            },
            {
                "title": {"en": "Foods to Eat During Periods"},
                "content": {"en": "What you eat during periods can help reduce cramps and boost your mood!\n\n**Foods that help:**\n- 🍌 Bananas — reduce bloating and cramps\n- 🍫 Dark chocolate — improves mood (in small amounts!)\n- 🍵 Ginger tea — reduces nausea and pain\n- 🥬 Leafy greens — replace iron lost during bleeding\n- 🐟 Fish or flaxseeds — omega-3 reduces inflammation\n- 🍶 Warm water and soups — soothe cramps\n- 🥜 Nuts — provide healthy fats and energy\n\n**Foods to avoid:**\n- ❌ Too much salt (causes bloating)\n- ❌ Caffeine (can worsen cramps)\n- ❌ Fried and spicy food (may cause discomfort)\n- ❌ Cold carbonated drinks"},
                "content_type": "article",
            },
        ],
    },
    {
        "name": "Hygiene & Self-Care", "slug": "hygiene", "icon": "Sparkles",
        "articles": [
            {
                "title": {"en": "Menstrual Hygiene: A Complete Guide"},
                "content": {"en": "Good menstrual hygiene is essential for your health.\n\n**Choosing the right product:**\n- **Sanitary pads** — Most common, easy to use\n- **Menstrual cups** — Reusable, eco-friendly, lasts 10+ years\n- **Cloth pads** — Reusable, budget-friendly\n\n**Important practices:**\n- Change pads every 4-6 hours\n- Wash hands before and after changing\n- Clean genital area with water (front to back)\n- Wrap used pads in paper before disposal\n- Bathe daily during periods\n- Wear clean, cotton underwear\n- Never use soap inside the vagina — water is enough"},
                "content_type": "article",
            },
            {
                "title": {"en": "Daily Hygiene Habits Every Girl Should Know"},
                "content": {"en": "Good hygiene keeps you healthy and confident!\n\n**Daily habits:**\n🚿 **Bathing** — Shower or bathe daily with soap\n🦷 **Oral care** — Brush twice a day, morning and night\n👐 **Hand washing** — Before eating, after toilet, after touching animals\n👗 **Clean clothes** — Change underwear daily, wash clothes regularly\n💅 **Nail care** — Keep nails short and clean\n👟 **Foot care** — Wash feet daily, wear clean socks\n\n**During periods, extra care:**\n- Carry extra pads in your bag\n- Use a small pouch for pad disposal\n- Change stained clothes as soon as possible\n- Don't feel embarrassed — periods are natural!"},
                "content_type": "article",
            },
        ],
    },
    {
        "name": "Mental Well-being", "slug": "mental-health", "icon": "Heart",
        "articles": [
            {
                "title": {"en": "Managing Stress as a Teenager"},
                "content": {"en": "Feeling stressed is normal, but learning to manage it is important.\n\n**Common causes of stress:**\n- School pressure and exams\n- Body changes during puberty\n- Friendship and relationship issues\n- Family expectations\n- Social media comparison\n\n**Healthy ways to cope:**\n- 🗣️ Talk to someone you trust (parent, teacher, friend)\n- 📝 Write in a journal\n- 🏃‍♀️ Exercise regularly\n- 🧘 Practice deep breathing\n- 🎵 Listen to music\n- 📵 Take breaks from social media\n- 😴 Get 8-10 hours of sleep\n\n**Remember:** It's okay to not be okay. Asking for help is a sign of strength, not weakness!"},
                "content_type": "article",
            },
            {
                "title": {"en": "Body Positivity: Loving Your Changing Body"},
                "content": {"en": "During puberty, your body changes — and that's beautiful!\n\n**Important truths:**\n- Every body is different and unique\n- There is no 'perfect' body shape\n- Weight gain during puberty is normal and healthy\n- Comparing yourself to social media images is unfair — most are edited\n- Your worth is not defined by how you look\n\n**Building confidence:**\n- Focus on what your body CAN do, not how it looks\n- Surround yourself with positive people\n- Wear clothes that make YOU feel good\n- Exercise for fun and health, not to change your body\n- Celebrate your strengths and talents\n\n💜 You are enough, exactly as you are!"},
                "content_type": "article",
            },
        ],
    },
    {
        "name": "Safety & Rights", "slug": "safety", "icon": "BookOpen",
        "articles": [
            {
                "title": {"en": "Good Touch vs Bad Touch"},
                "content": {"en": "Understanding the difference between good and bad touch is very important for your safety.\n\n**Good touch** makes you feel:\n- Safe and comfortable\n- Happy (like a hug from family)\n- Cared for (like a doctor's examination with a parent present)\n\n**Bad touch** makes you feel:\n- Uncomfortable or scared\n- Confused or uneasy\n- It involves private body parts without medical reason\n\n**What to do if you experience bad touch:**\n1. Say NO firmly\n2. Move away from the person\n3. Tell a trusted adult immediately\n4. It is NEVER your fault\n5. Keep telling until someone listens\n\n**Remember:** Your body belongs to YOU. No one has the right to touch you without your consent."},
                "content_type": "article",
            },
            {
                "title": {"en": "Know Your Rights as a Girl"},
                "content": {"en": "Every girl in India has legal rights that protect her:\n\n**Right to Education**\n- Free education until age 14 (Right to Education Act)\n- No one can stop you from going to school\n\n**Right to Health**\n- Access to healthcare and nutrition\n- Government schemes like ICDS provide free health services\n\n**Protection from Child Marriage**\n- Legal age for marriage is 18 for girls\n- Child marriage is a crime\n\n**Protection from Harassment**\n- POCSO Act protects children from sexual offenses\n- Schools must have complaint committees\n\n**Helpline Numbers:**\n- Childline: 1098 (24x7, free)\n- Women Helpline: 181\n- Police: 100"},
                "content_type": "article",
            },
        ],
    },
]

# ── FLASHCARD DATA ───────────────────────────────────────────────

FLASHCARD_DATA = [
    {
        "name": "Body Basics", "slug": "body-basics",
        "description": "Learn key facts about your body", "category": "health",
        "cards": [
            {"front": {"en": "What is menstruation?"}, "back": {"en": "The monthly shedding of the uterine lining. A normal, healthy process for all girls."}},
            {"front": {"en": "What is ovulation?"}, "back": {"en": "Release of a mature egg from the ovary, usually around day 14 of the cycle."}},
            {"front": {"en": "What causes period cramps?"}, "back": {"en": "Prostaglandins — chemicals causing uterus contractions. Heat packs and light exercise help!"}},
            {"front": {"en": "How much blood is lost per period?"}, "back": {"en": "About 30-40 ml (2-3 tablespoons). It seems more due to tissue and fluids."}},
            {"front": {"en": "What is PMS?"}, "back": {"en": "Premenstrual Syndrome — mood swings, bloating, cramps that occur 1-2 weeks before your period."}},
            {"front": {"en": "What is a normal cycle length?"}, "back": {"en": "21-35 days is normal. Average is 28 days. Irregular cycles are common in teens!"}},
        ],
    },
    {
        "name": "Nutrition Facts", "slug": "nutrition-facts",
        "description": "Key nutrition knowledge for growing girls", "category": "nutrition",
        "cards": [
            {"front": {"en": "Why is iron important for girls?"}, "back": {"en": "Girls lose iron during periods. Low iron = anemia (tiredness, weakness, dizziness)."}},
            {"front": {"en": "What is calcium needed for?"}, "back": {"en": "Strong bones and teeth! Teens build most bone mass now. Eat dairy, ragi, leafy greens."}},
            {"front": {"en": "Name 3 iron-rich Indian foods"}, "back": {"en": "1. Spinach (palak)\n2. Lentils (dal)\n3. Jaggery (gur)\nBonus: Pomegranate, dates, sesame!"}},
            {"front": {"en": "Why drink water during periods?"}, "back": {"en": "Reduces bloating, headaches, and fatigue. Aim for 8-10 glasses daily during periods."}},
            {"front": {"en": "What does Vitamin C do?"}, "back": {"en": "Boosts immunity, helps absorb iron, heals wounds. Found in amla, orange, lemon, guava."}},
        ],
    },
    {
        "name": "Hygiene Essentials", "slug": "hygiene-essentials",
        "description": "Important hygiene facts and practices", "category": "hygiene",
        "cards": [
            {"front": {"en": "How often to change a pad?"}, "back": {"en": "Every 4-6 hours, even on light days. This prevents infection and odor."}},
            {"front": {"en": "Pad vs Menstrual Cup?"}, "back": {"en": "Pads: disposable, easy. Cups: reusable 10+ years, eco-friendly, cost-saving. Both are safe!"}},
            {"front": {"en": "Can you bathe during periods?"}, "back": {"en": "YES! Bathing during periods is important for hygiene. Warm water can even help with cramps."}},
            {"front": {"en": "How to dispose of pads?"}, "back": {"en": "Wrap in newspaper/wrapper → put in dustbin. Never flush! It blocks drains."}},
        ],
    },
]


async def seed():
    """Insert seed data into the database."""
    async with async_session_factory() as db:
        existing = await db.execute(select(QuizCategory).limit(1))
        if existing.scalar_one_or_none():
            print("⚠️  Data already seeded, skipping.")
            return

        print("🌱 Seeding quiz data...")
        for cat_data in QUIZ_DATA:
            cat_id = uid()
            db.add(QuizCategory(id=cat_id, name=cat_data["name"], slug=cat_data["slug"], description=cat_data["description"]))
            for q in cat_data["questions"]:
                db.add(Quiz(id=uid(), category_id=cat_id, **q))

        print("📚 Seeding learn data...")
        for cat_data in LEARN_DATA:
            cat_id = uid()
            db.add(LearnCategory(id=cat_id, name=cat_data["name"], slug=cat_data["slug"], icon=cat_data["icon"]))
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
