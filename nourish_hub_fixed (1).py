import streamlit as st
import plotly.graph_objects as go  # ✅ 수정: px → go

st.set_page_config(
    page_title="Nourish · Ingredient & Recipe Hub",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Noto+Sans+KR:wght@300;400;700&display=swap');
    .main { background-color: #FBFBFA; }
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        color: #2C3A1E;
    }
    .brand-sub { font-family:'DM Serif Display',serif; color:#3B6D11; font-size:14px; letter-spacing:2px; font-weight:bold; margin-bottom:-10px; }
    .brand-main { font-size:42px; font-weight:700; color:#2C3A1E; line-height:1.3; margin-bottom:5px; }
    .brand-desc { color:#6E7A64; font-size:15px; margin-bottom:25px; }
    .food-card { background-color:white; border-radius:16px; border:1px solid #EAECE8; box-shadow:0px 4px 20px rgba(44,58,30,0.03); text-align:center; padding:20px 12px; }
    .food-emoji { font-size:40px; margin-bottom:8px; }
    .food-name { font-size:18px; font-weight:700; color:#2C3A1E; margin-bottom:4px; }
    .food-tagline { font-size:12px; color:#8C9A82; margin-bottom:10px; }
    .food-badge { background-color:#F4F6F2; color:#556B2F; padding:3px 10px; border-radius:50px; font-size:11px; font-weight:bold; }
    .cute-card { background-color:white; padding:26px; border-radius:16px; border:1px solid #EAECE8; box-shadow:0px 4px 20px rgba(44,58,30,0.04); margin-bottom:20px; }
    .card-title { font-size:20px; font-weight:700; color:#2C3A1E; margin-bottom:12px; }
    .nut-grid-item { background-color:#F6F8F5 !important; padding:15px; border-radius:10px; color:#2C3A1E !important; font-size:14px; font-weight:bold; border:1px solid #EEF1EC; }
    .badge-container { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:15px; }
    .badge { padding:6px 14px; border-radius:50px; font-size:13px; font-weight:700; }
    .badge-time { background-color:#EAF3DE; color:#3B6D11; }
    .badge-cal { background-color:#FDF0EA; color:#E67E22; }
    .badge-ing { background-color:#F4F6F2; color:#556B2F; }
    .badge-level { background-color:#EEF2F7; color:#2E64FE; }
    .step-item { display:flex; align-items:flex-start; gap:14px; padding:10px 0; }
    .step-number { background-color:#3B6D11; color:white; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:bold; flex-shrink:0; }
    .step-text { font-size:15px; color:#333333; line-height:1.5; }
    .tip-box { background-color:#FAFAFA; border-left:4px solid #3B6D11; padding:12px 16px; border-radius:0 8px 8px 0; font-size:14px; color:#555; margin-top:15px; }
    </style>
""", unsafe_allow_html=True)

# ── 다국어 사전 ──────────────────────────────────────────────────
UI_TEXTS = {
    "한국어": {
        "sub_logo": "🌿 GOOD FOOD STARTS HERE",
        "title_main": "오늘의 식재료를<br><span style='color:#3B6D11;'>탐색해보세요</span>",
        "subtitle": "싱그럽고 영양 가득한 전통 식재료 가이드 💚",
        "selector_label": "🔍 전체 식재료 선택 / 검색 (50대 핵심 성분 라이브러리)",
        "intro_recom": "오늘의 추천 핵심 식재료",
        "tab1": "🌿 식재료 탐색", "tab2": "🍳 레시피",
        "doc_title": "상세 도감", "nut_info": "📊 영양 성분 (100g 기준)",
        "recipe_room": "맞춤형 추천 레시피 (5가지 테마 시리즈)",
        "btn_del": "❌ 빼기", "btn_add": "🧡 찜하기", "btn_video": "📺 요리 가이드 영상 보기",
        "saved_title": "❤️ 내가 찜한 레시피", "saved_empty": "찜한 레시피가 없습니다.",
        "academic": "🎓 학과 및 학생 정보",
        "select_btn": "선택", "info_btn": "정보",
        "labels": ["칼로리", "단백질", "탄수화물", "지방", "식이섬유", "철분"],
        "nutrients": ["단백질 (g)", "식이섬유 (g)", "칼로리 (kcal)", "지방 (g)", "탄수화물 (g)", "철분 (mg)"]
    },
    "English": {
        "sub_logo": "🌿 GOOD FOOD STARTS HERE",
        "title_main": "Explore <span style='color:#3B6D11;'>Wholesome Ingredients</span>",
        "subtitle": "Nutrient-dense profile guide for traditional ingredients 💚",
        "selector_label": "🔍 Select / Search Ingredient (50 Core Library)",
        "intro_recom": "Today's Featured Ingredients",
        "tab1": "🌿 Explore Ingredients", "tab2": "🍳 Recipes",
        "doc_title": "Encyclopedia", "nut_info": "📊 Nutrition Info (per 100g)",
        "recipe_room": "Tailored Recipe Collection (5 Custom Themes)",
        "btn_del": "❌ Remove", "btn_add": "🧡 Save", "btn_video": "📺 Watch Recipe Video",
        "saved_title": "❤️ Saved Recipes", "saved_empty": "No saved recipes yet.",
        "academic": "🎓 Academic Info",
        "select_btn": "Select", "info_btn": "Info",
        "labels": ["Calories", "Protein", "Carbs", "Fat", "Fibre", "Iron"],
        "nutrients": ["Protein (g)", "Fibre (g)", "Calories (kcal)", "Fat (g)", "Carbs (g)", "Iron (mg)"]
    },
    "중국어 (简体中文)": {
        "sub_logo": "🌿 GOOD FOOD STARTS HERE",
        "title_main": "探索今天的<br><span style='color:#3B6D11;'>健康食材</span>",
        "subtitle": "充满活力与营养的传统食材专业指南 💚",
        "selector_label": "🔍 选择 / 搜索食材 (50种核心食材库)",
        "intro_recom": "今日推荐核心食材",
        "tab1": "🌿 食材探索", "tab2": "🍳 推荐食谱",
        "doc_title": "详细百科", "nut_info": "📊 营养成分 (每100g)",
        "recipe_room": "定制推荐食谱 (5大核心主题)",
        "btn_del": "❌ 移除", "btn_add": "🧡 收藏", "btn_video": "📺 查看烹饪指导视频",
        "saved_title": "❤️ 我收藏的食谱", "saved_empty": "收藏夹空空如也。",
        "academic": "🎓 选课及学生信息",
        "select_btn": "选择", "info_btn": "信息",
        "labels": ["热量", "蛋白质", "碳水化合物", "脂肪", "膳食纤维", "铁"],
        "nutrients": ["蛋白质 (g)", "膳食纤维 (g)", "卡路里 (kcal)", "脂肪 (g)", "碳水化合物 (g)", "铁分 (mg)"]
    }
}

# ── 실제 레시피 데이터 (식재료별 고유 레시피 5개씩) ──────────────
REAL_RECIPES = {
    "quinoa": {
        "ko": [
            {"title":"퀴노아 샐러드 볼","time":"20분","calories":"310 kcal","level":"쉬움","steps":["퀴노아 1컵을 물 2컵에 15분 끓인 뒤 5분 뜸 들인다","오이·방울토마토·적양파를 먹기 좋게 썬다","레몬즙·올리브오일·소금·후추로 드레싱을 만든다","퀴노아에 채소와 드레싱을 섞어 완성한다"],"tip":"드레싱은 먹기 직전에 뿌려야 채소가 살아있어요"},
            {"title":"퀴노아 그릭요거트 아침 볼","time":"10분","calories":"270 kcal","level":"쉬움","steps":["익힌 퀴노아와 그릭요거트를 1:1로 섞는다","꿀·시나몬을 넣어 섞는다","블루베리·슬라이스 아몬드를 올린다","민트잎으로 마무리한다"],"tip":"전날 밤에 퀴노아를 미리 지어두면 아침이 편해요"},
            {"title":"퀴노아 채소 수프","time":"30분","calories":"220 kcal","level":"쉬움","steps":["양파·당근·셀러리를 올리브오일에 볶는다","채수 4컵을 붓고 퀴노아를 넣는다","20분 약불로 끓인다","소금·후추·파슬리로 마무리한다"],"tip":"채수 대신 닭육수를 써도 맛있어요"},
            {"title":"퀴노아 스터프드 파프리카","time":"40분","calories":"350 kcal","level":"보통","steps":["파프리카 윗부분을 잘라 씨를 제거한다","익힌 퀴노아·블랙빈·옥수수·토마토소스를 섞어 속 재료를 만든다","파프리카에 속 재료를 채우고 치즈를 올린다","200도 오븐에서 25분 굽는다"],"tip":"파프리카 색깔을 여러 개 섞으면 보기도 예쁘고 영양도 다양해요"},
            {"title":"퀴노아 새우 볶음","time":"25분","calories":"380 kcal","level":"보통","steps":["퀴노아를 미리 지어 식혀둔다","팬에 참기름·마늘·새우를 볶는다","퀴노아와 달걀을 넣고 강불에서 볶는다","간장·굴소스로 간하고 파·깨를 뿌린다"],"tip":"퀴노아는 반드시 식힌 것을 써야 볶음이 잘 돼요"},
        ],
        "en": [
            {"title":"Quinoa Salad Bowl","time":"20 min","calories":"310 kcal","level":"Easy","steps":["Cook 1 cup quinoa in 2 cups water for 15 min, rest 5 min","Dice cucumber, cherry tomatoes, red onion","Make dressing: lemon juice, olive oil, salt, pepper","Toss quinoa with vegetables and dressing"],"tip":"Add dressing just before serving to keep veggies crisp"},
            {"title":"Quinoa Greek Yogurt Breakfast Bowl","time":"10 min","calories":"270 kcal","level":"Easy","steps":["Mix cooked quinoa 1:1 with Greek yogurt","Stir in honey and cinnamon","Top with blueberries and sliced almonds","Garnish with mint leaves"],"tip":"Cook quinoa the night before for an easy morning"},
            {"title":"Quinoa Vegetable Soup","time":"30 min","calories":"220 kcal","level":"Easy","steps":["Sauté onion, carrot, celery in olive oil","Add 4 cups vegetable broth and quinoa","Simmer on low for 20 minutes","Season with salt, pepper, parsley"],"tip":"Chicken broth works great as an alternative"},
            {"title":"Quinoa Stuffed Peppers","time":"40 min","calories":"350 kcal","level":"Medium","steps":["Cut tops off peppers, remove seeds","Mix cooked quinoa, black beans, corn, tomato sauce","Fill peppers and top with cheese","Bake at 200°C for 25 minutes"],"tip":"Use different colored peppers for variety"},
            {"title":"Quinoa Shrimp Stir-Fry","time":"25 min","calories":"380 kcal","level":"Medium","steps":["Cook quinoa ahead and let it cool","Stir-fry garlic and shrimp in sesame oil","Add quinoa and egg, toss over high heat","Season with soy sauce and oyster sauce, top with scallions"],"tip":"Cold quinoa stir-fries much better than warm"},
        ],
    },
    "avocado": {
        "ko": [
            {"title":"아보카도 토스트","time":"10분","calories":"280 kcal","level":"쉬움","steps":["통곡물빵을 노릇하게 굽는다","아보카도를 으깨 레몬즙·소금·후추를 넣는다","빵에 듬뿍 바른다","반숙 달걀과 치아씨드를 올린다"],"tip":"아보카도는 먹기 직전에 으깨야 갈변을 막을 수 있어요"},
            {"title":"과카몰리","time":"8분","calories":"150 kcal","level":"쉬움","steps":["잘 익은 아보카도 2개를 포크로 으깬다","토마토·적양파·고수를 잘게 썬다","라임즙·소금·큐민을 넣고 섞는다","토르티야 칩과 함께 서브한다"],"tip":"라임즙을 넉넉히 넣으면 색이 예쁘게 유지돼요"},
            {"title":"아보카도 명란 비빔밥","time":"15분","calories":"420 kcal","level":"쉬움","steps":["따뜻한 밥에 참기름·간장을 섞는다","아보카도를 슬라이스하고 명란을 준비한다","밥 위에 아보카도·명란·달걀노른자를 올린다","김가루·깨를 뿌리고 비벼 먹는다"],"tip":"명란 대신 연어알을 써도 정말 맛있어요"},
            {"title":"아보카도 초콜릿 무스","time":"15분","calories":"240 kcal","level":"쉬움","steps":["잘 익은 아보카도·코코아 파우더·꿀을 블렌더에 넣는다","아몬드밀크를 조금 넣어 크리미하게 간다","바닐라 에센스 한 방울을 넣는다","컵에 담고 라즈베리·민트를 올린다"],"tip":"아보카도가 잘 익을수록 무스가 더 부드럽고 달콤해요"},
            {"title":"아보카도 시저 파스타","time":"20분","calories":"460 kcal","level":"보통","steps":["아보카도·레몬즙·마늘·올리브오일·파마산으로 크리미 드레싱을 만든다","파스타를 소금물에 삶는다","따뜻한 파스타에 드레싱을 넣어 버무린다","루꼴라·방울토마토·크루통을 올린다"],"tip":"드레싱을 만들 때 얼음물을 조금 넣으면 더 부드러워요"},
        ],
        "en": [
            {"title":"Avocado Toast","time":"10 min","calories":"280 kcal","level":"Easy","steps":["Toast whole grain bread until golden","Mash avocado with lemon juice, salt, and pepper","Spread generously on toast","Top with poached egg and chia seeds"],"tip":"Mash avocado right before serving to prevent browning"},
            {"title":"Guacamole","time":"8 min","calories":"150 kcal","level":"Easy","steps":["Mash 2 ripe avocados with a fork","Finely dice tomato, red onion, cilantro","Add lime juice, salt, and cumin","Serve with tortilla chips"],"tip":"Generous lime juice keeps the color bright and fresh"},
            {"title":"Avocado Mentaiko Rice Bowl","time":"15 min","calories":"420 kcal","level":"Easy","steps":["Mix warm rice with sesame oil and soy sauce","Slice avocado and prepare mentaiko","Top rice with avocado, roe, and egg yolk","Sprinkle nori flakes and sesame, mix to eat"],"tip":"Salmon roe is a great alternative to mentaiko"},
            {"title":"Avocado Chocolate Mousse","time":"15 min","calories":"240 kcal","level":"Easy","steps":["Blend ripe avocado, cocoa powder, and honey","Add a splash of almond milk for creaminess","Add a drop of vanilla extract","Pour into cups, top with raspberries and mint"],"tip":"Riper avocados make a sweeter, creamier mousse"},
            {"title":"Avocado Caesar Pasta","time":"20 min","calories":"460 kcal","level":"Medium","steps":["Blend avocado, lemon, garlic, olive oil, parmesan into dressing","Cook pasta in salted water","Toss warm pasta with dressing","Top with arugula, cherry tomatoes, and croutons"],"tip":"Add a splash of cold water while blending for a smoother dressing"},
        ],
    },
    "tofu": {
        "ko": [
            {"title":"순두부찌개","time":"20분","calories":"180 kcal","level":"쉬움","steps":["멸치·다시마 육수를 10분 끓인다","고춧가루 양념을 넣고 애호박·버섯을 넣는다","순두부를 뜯어 넣고 5분 끓인다","달걀을 넣고 청양고추·파를 올린다"],"tip":"육수가 펄펄 끓을 때 순두부를 넣어야 모양이 살아요"},
            {"title":"두부 스테이크","time":"15분","calories":"220 kcal","level":"쉬움","steps":["두부를 2cm로 썰어 물기를 제거한다","간장·꿀·마늘·참기름으로 소스를 만든다","팬에 양면 3분씩 노릇하게 굽는다","소스 붓고 1분 조리고 깨·파를 얹는다"],"tip":"두부 물기 제거가 바삭함의 핵심이에요"},
            {"title":"마파두부","time":"20분","calories":"280 kcal","level":"보통","steps":["돼지고기 다짐육을 팬에 볶는다","두반장·다진 마늘·생강을 넣어 볶는다","두부를 넣고 육수·간장으로 간한다","전분물로 걸쭉하게 만들고 파·산초로 마무리한다"],"tip":"두반장은 볶아서 기름에 향을 내야 깊은 맛이 나요"},
            {"title":"두부 강황 스크램블","time":"12분","calories":"200 kcal","level":"쉬움","steps":["두부를 손으로 부숴 물기를 제거한다","팬에 올리브오일·마늘을 볶는다","두부·강황·큐민·소금을 넣고 볶는다","시금치·방울토마토를 넣어 마무리한다"],"tip":"강황에 후추를 조금 넣으면 흡수율이 높아져요"},
            {"title":"두부 카프레제 샐러드","time":"10분","calories":"160 kcal","level":"쉬움","steps":["두부를 1cm 두께로 슬라이스한다","토마토도 같은 두께로 슬라이스한다","두부·토마토·바질을 번갈아 쌓는다","올리브오일·발사믹·소금·후추를 뿌린다"],"tip":"신선한 버팔로 모차렐라 대신 두부를 쓰면 저칼로리 카프레제가 돼요"},
        ],
        "en": [
            {"title":"Sundubu Jjigae (Soft Tofu Stew)","time":"20 min","calories":"180 kcal","level":"Easy","steps":["Simmer anchovy-kelp broth 10 minutes","Add gochugaru paste, zucchini, and mushrooms","Tear in soft tofu and simmer 5 min","Add egg, top with scallions and chili"],"tip":"Add soft tofu to boiling broth to keep its shape"},
            {"title":"Tofu Steak","time":"15 min","calories":"220 kcal","level":"Easy","steps":["Slice firm tofu 2cm thick, pat completely dry","Make glaze: soy sauce, honey, garlic, sesame oil","Pan-fry both sides 3 min each until golden","Pour glaze over, simmer 1 min, garnish with sesame and scallions"],"tip":"Removing moisture is the key to crispy tofu"},
            {"title":"Mapo Tofu","time":"20 min","calories":"280 kcal","level":"Medium","steps":["Stir-fry ground pork until cooked","Add doubanjiang, minced garlic and ginger","Add tofu, broth, and soy sauce","Thicken with cornstarch slurry, finish with scallions and Sichuan pepper"],"tip":"Fry doubanjiang in oil first to develop its deep flavour"},
            {"title":"Turmeric Tofu Scramble","time":"12 min","calories":"200 kcal","level":"Easy","steps":["Crumble tofu and squeeze out moisture","Sauté olive oil and garlic in pan","Add tofu, turmeric, cumin, and salt; stir-fry","Fold in spinach and cherry tomatoes to finish"],"tip":"Add black pepper to turmeric to boost absorption by 2000%"},
            {"title":"Tofu Caprese Salad","time":"10 min","calories":"160 kcal","level":"Easy","steps":["Slice tofu 1cm thick","Slice tomatoes to the same thickness","Alternate tofu, tomato, and basil layers","Drizzle with olive oil, balsamic, salt, and pepper"],"tip":"A low-calorie twist on the classic caprese using tofu"},
        ],
    },
    "blueberry": {
        "ko": [
            {"title":"블루베리 스무디 볼","time":"8분","calories":"260 kcal","level":"쉬움","steps":["냉동 블루베리·바나나를 블렌딩한다","그릭요거트를 넣고 걸쭉하게 만든다","그래놀라·치아씨드를 올린다","꿀을 드리즐한다"],"tip":"냉동 블루베리를 쓰면 더 걸쭉하고 차갑게 완성돼요"},
            {"title":"블루베리 치아씨드 잼","time":"15분","calories":"40 kcal","level":"쉬움","steps":["블루베리·꿀·레몬즙을 냄비에 넣고 중불로 끓인다","10분 저으며 졸인다","불을 끄고 치아씨드를 넣어 섞는다","식혀서 유리병에 담아 냉장 보관한다"],"tip":"설탕 없이 꿀만 써도 달콤한 잼이 돼요"},
            {"title":"블루베리 바나나 팬케이크","time":"20분","calories":"310 kcal","level":"쉬움","steps":["바나나를 으깨고 달걀·귀리가루를 섞는다","블루베리를 반죽에 넣는다","팬에 약불로 양면을 굽는다","메이플시럽과 생 블루베리를 올린다"],"tip":"반죽에 블루베리를 통째로 넣으면 터질 때 향이 폭발해요"},
            {"title":"블루베리 치즈케이크 무스","time":"20분","calories":"290 kcal","level":"보통","steps":["크림치즈를 풀고 꿀·바닐라를 섞는다","생크림을 휘핑해 가볍게 섞는다","블루베리를 레몬즙·설탕으로 소스로 끓인다","컵에 무스를 담고 소스를 올린다"],"tip":"크림치즈는 실온에서 30분 두면 훨씬 잘 풀려요"},
            {"title":"블루베리 요거트 아이스바","time":"10분+냉동4h","calories":"90 kcal","level":"쉬움","steps":["그릭요거트·꿀·바닐라를 섞는다","블루베리를 잘게 으깨 요거트에 섞는다","아이스바 틀에 붓고 막대를 꽂는다","냉동실에 4시간 이상 얼린다"],"tip":"틀에서 뺄 때 따뜻한 물에 10초 담그면 쉽게 빠져요"},
        ],
        "en": [
            {"title":"Blueberry Smoothie Bowl","time":"8 min","calories":"260 kcal","level":"Easy","steps":["Blend frozen blueberries and banana","Add Greek yogurt and blend until thick","Top with granola and chia seeds","Drizzle with honey"],"tip":"Frozen blueberries create a thicker, colder bowl"},
            {"title":"Blueberry Chia Jam","time":"15 min","calories":"40 kcal","level":"Easy","steps":["Combine blueberries, honey, lemon juice in saucepan","Stir and simmer 10 minutes","Remove from heat and stir in chia seeds","Cool and store in glass jar in fridge"],"tip":"Honey alone makes a naturally sweet jam without added sugar"},
            {"title":"Blueberry Banana Pancakes","time":"20 min","calories":"310 kcal","level":"Easy","steps":["Mash banana and mix with eggs and oat flour","Fold blueberries into batter","Cook both sides over low heat","Top with maple syrup and fresh blueberries"],"tip":"Whole blueberries burst beautifully when cooked"},
            {"title":"Blueberry Cheesecake Mousse","time":"20 min","calories":"290 kcal","level":"Medium","steps":["Whip cream cheese with honey and vanilla","Fold in lightly whipped heavy cream","Cook blueberries with lemon and sugar into sauce","Spoon mousse into cups and top with sauce"],"tip":"Leave cream cheese at room temp 30 min for easy mixing"},
            {"title":"Blueberry Yogurt Ice Bars","time":"10 min + 4h freeze","calories":"90 kcal","level":"Easy","steps":["Mix Greek yogurt, honey, and vanilla","Mash blueberries and swirl into yogurt","Pour into ice bar molds, insert sticks","Freeze for at least 4 hours"],"tip":"Dip mold in warm water 10 sec to unmold easily"},
        ],
    },
    "kelp": {
        "ko": [
            {"title":"다시마 육수","time":"15분","calories":"20 kcal","level":"쉬움","steps":["다시마를 찬물에 30분 불린다","약불에서 서서히 가열하여 끓기 직전 건져낸다","맑고 감칠맛 풍부한 육수 완성","된장국·찌개·우동 국물로 활용한다"],"tip":"끓이면 쓴맛이 나니 반드시 끓기 전에 건져야 해요"},
            {"title":"다시마 쌈","time":"5분","calories":"30 kcal","level":"쉬움","steps":["다시마를 깨끗이 씻어 준비한다","생으로 또는 살짝 데쳐 부드럽게 만든다","삼겹살·밥·마늘을 쌈장과 함께 싼다","상큼한 다시마 향이 입안을 가득 채운다"],"tip":"너무 오래 데치면 미끌미끌해지니 30초만 데쳐요"},
            {"title":"다시마 튀각","time":"15분","calories":"120 kcal","level":"쉬움","steps":["다시마를 5x5cm로 자른다","170도 기름에 바삭하게 튀긴다","설탕·소금을 뿌려 달콤짭짤하게 만든다","바삭한 해조류 과자 완성"],"tip":"기름 온도가 충분히 올라야 바삭하게 튀겨져요"},
            {"title":"다시마 냉국","time":"10분","calories":"40 kcal","level":"쉬움","steps":["다시마를 가늘게 채 썰어 준비한다","오이·홍고추도 가늘게 채 썬다","식초·간장·설탕·참깨로 양념한다","차갑게 해서 여름 보양식으로 즐긴다"],"tip":"얼음을 넣어 차갑게 먹으면 더 상큼해요"},
            {"title":"다시마 볶음","time":"12분","calories":"80 kcal","level":"쉬움","steps":["다시마를 불려 먹기 좋게 자른다","참기름·마늘·간장으로 볶는다","설탕 한 꼬집으로 감칠맛을 더한다","통깨를 뿌려 반찬으로 완성한다"],"tip":"볶을 때 물이 튀니 뚜껑을 조심하세요"},
        ],
        "en": [
            {"title":"Dashi Broth","time":"15 min","calories":"20 kcal","level":"Easy","steps":["Soak kelp in cold water for 30 min","Heat gently and remove kelp just before boiling","You now have a clear, umami-rich broth","Use as base for miso soup, stews, and noodles"],"tip":"Remove kelp before boiling — boiling makes it bitter"},
            {"title":"Kelp Ssam Wrap","time":"5 min","calories":"30 kcal","level":"Easy","steps":["Rinse kelp and prepare","Use raw or briefly blanched for softness","Wrap pork belly, rice, and garlic with ssamjang","The fresh oceanic aroma elevates the whole wrap"],"tip":"Only blanch 30 seconds or it gets slimy"},
            {"title":"Crispy Kelp Chips","time":"15 min","calories":"120 kcal","level":"Easy","steps":["Cut kelp into 5x5cm pieces","Deep fry at 170°C until crispy","Season with sugar and salt for sweet-savory balance","Enjoy as a crispy seaweed snack"],"tip":"Oil must be fully heated for maximum crunch"},
            {"title":"Cold Kelp Salad","time":"10 min","calories":"40 kcal","level":"Easy","steps":["Julienne kelp finely","Also julienne cucumber and red chili","Dress with vinegar, soy sauce, sugar, and sesame","Serve cold as a refreshing summer side dish"],"tip":"Add ice cubes to make it even more refreshing"},
            {"title":"Stir-Fried Kelp","time":"12 min","calories":"80 kcal","level":"Easy","steps":["Soak kelp and cut into bite-sized pieces","Stir-fry with sesame oil, garlic, and soy sauce","Add a pinch of sugar for depth","Finish with sesame seeds and serve as banchan"],"tip":"Watch out for steam splatter when stir-frying"},
        ],
    },
    "salmon": {
        "ko": [
            {"title":"연어 포케 볼","time":"15분","calories":"450 kcal","level":"쉬움","steps":["현미밥을 볼에 담는다","연어를 큐브로 썰어 간장·참기름·생강즙에 5분 재운다","에다마메·오이·당근·아보카도를 준비한다","밥 위에 올리고 스리라차 마요를 뿌린다"],"tip":"연어는 신선한 회용을 써야 날것으로 먹어도 안전해요"},
            {"title":"허브 오븐 구이 연어","time":"22분","calories":"390 kcal","level":"보통","steps":["연어에 올리브오일·마늘·레몬즙·딜을 바른다","200도 오븐에서 12분 굽는다","아스파라거스를 함께 굽는다","레몬·파슬리로 마무리한다"],"tip":"오버쿡하지 않도록 두께에 따라 시간을 조절해요"},
            {"title":"연어 아보카도 타르타르","time":"15분","calories":"320 kcal","level":"보통","steps":["신선한 연어를 잘게 다진다","아보카도를 작게 깍둑썬다","간장·참기름·레몬즙·고추냉이로 양념한다","크래커나 오이 슬라이스 위에 올린다"],"tip":"접시를 냉장고에 차갑게 두었다가 플레이팅하면 더 맛있어요"},
            {"title":"연어 크림파스타","time":"25분","calories":"520 kcal","level":"보통","steps":["파스타를 소금물에 삶는다","팬에 버터로 연어를 굽다가 부순다","생크림·파마산·레몬즙을 넣어 소스를 만든다","파스타를 넣어 섞고 딜·케이퍼로 마무리한다"],"tip":"면수를 조금 넣으면 소스가 더 잘 엉겨요"},
            {"title":"연어 된장국","time":"20분","calories":"210 kcal","level":"쉬움","steps":["다시마 육수를 낸다","된장 2큰술을 풀어준다","연어를 한 입 크기로 잘라 넣는다","두부·무·파를 넣고 5분 끓여 완성한다"],"tip":"연어를 너무 오래 끓이면 퍽퍽해지니 마지막에 넣어요"},
        ],
        "en": [
            {"title":"Salmon Poke Bowl","time":"15 min","calories":"450 kcal","level":"Easy","steps":["Place brown rice in bowl","Cube salmon and marinate in soy, sesame oil, ginger for 5 min","Prepare edamame, cucumber, carrot, avocado","Top rice and drizzle with sriracha mayo"],"tip":"Use sashimi-grade salmon for raw consumption safety"},
            {"title":"Herb-Baked Salmon","time":"22 min","calories":"390 kcal","level":"Medium","steps":["Coat salmon with olive oil, garlic, lemon juice, and dill","Bake at 200°C for 12 minutes","Roast asparagus alongside","Finish with lemon and parsley"],"tip":"Adjust baking time based on thickness to avoid overcooking"},
            {"title":"Salmon Avocado Tartare","time":"15 min","calories":"320 kcal","level":"Medium","steps":["Finely dice fresh salmon","Cube avocado to same size","Season with soy sauce, sesame oil, lemon juice, wasabi","Serve on crackers or cucumber slices"],"tip":"Chill the serving plate first for best flavour and food safety"},
            {"title":"Salmon Cream Pasta","time":"25 min","calories":"520 kcal","level":"Medium","steps":["Cook pasta in salted water","Pan-sear salmon in butter then break into flakes","Add heavy cream, parmesan, lemon juice for sauce","Toss pasta in sauce and finish with dill and capers"],"tip":"Add a splash of pasta water to help the sauce coat evenly"},
            {"title":"Salmon Doenjang Soup","time":"20 min","calories":"210 kcal","level":"Easy","steps":["Make kelp dashi broth","Dissolve 2 tbsp doenjang in the broth","Cut salmon into bite-sized pieces and add","Add tofu, radish, scallions and simmer 5 min"],"tip":"Add salmon at the end to keep it tender and moist"},
        ],
    },
    "spinach": {
        "ko": [
            {"title":"시금치 된장국","time":"15분","calories":"80 kcal","level":"쉬움","steps":["멸치 육수를 낸다","된장 2큰술을 풀어준다","시금치를 넣고 2분 끓인다","두부·파를 넣어 마무리한다"],"tip":"시금치는 마지막에 넣어야 색이 선명하게 살아요"},
            {"title":"시금치 페스토 파스타","time":"20분","calories":"380 kcal","level":"보통","steps":["시금치·아몬드·마늘·올리브오일로 페스토를 만든다","파스타를 소금물에 삶는다","팬에 페스토와 파스타를 섞는다","방울토마토와 파마산을 올린다"],"tip":"페스토에 레몬즙을 넣으면 색이 더 선명하게 유지돼요"},
            {"title":"시금치 달걀 볶음","time":"10분","calories":"180 kcal","level":"쉬움","steps":["시금치를 씻어 물기를 제거한다","팬에 마늘을 볶는다","시금치를 강불에서 볶는다","달걀을 넣어 반숙으로 익히고 간한다"],"tip":"강불에서 빠르게 볶아야 숨이 죽지 않고 식감이 살아요"},
            {"title":"시금치 스무디","time":"5분","calories":"130 kcal","level":"쉬움","steps":["시금치 한 줌·바나나·아몬드밀크를 블렌더에 넣는다","꿀·레몬즙을 넣는다","곱게 갈아준다","얼음을 넣어 차갑게 마신다"],"tip":"바나나 단맛이 시금치 풀 향을 잡아줘 거부감 없이 마실 수 있어요"},
            {"title":"시금치 치즈 키시","time":"40분","calories":"320 kcal","level":"보통","steps":["파이지를 틀에 깔고 포크로 구멍을 낸다","시금치를 볶아 물기를 짠다","달걀·생크림·치즈·시금치를 섞어 속 재료를 만든다","파이지에 붓고 180도에서 30분 굽는다"],"tip":"시금치 물기를 완전히 짜야 키시가 흐물거리지 않아요"},
        ],
        "en": [
            {"title":"Spinach Doenjang Soup","time":"15 min","calories":"80 kcal","level":"Easy","steps":["Make anchovy broth","Dissolve 2 tbsp doenjang","Add spinach and simmer 2 min","Add tofu and scallions to finish"],"tip":"Add spinach at the very end to keep its vibrant green colour"},
            {"title":"Spinach Pesto Pasta","time":"20 min","calories":"380 kcal","level":"Medium","steps":["Blend spinach, almonds, garlic, olive oil into pesto","Cook pasta in salted water","Toss pasta with pesto in pan","Top with cherry tomatoes and parmesan"],"tip":"A splash of lemon juice helps the pesto stay bright green"},
            {"title":"Spinach & Egg Stir-Fry","time":"10 min","calories":"180 kcal","level":"Easy","steps":["Wash spinach and pat dry","Sauté garlic in pan","Stir-fry spinach over high heat","Add eggs, cook to soft scramble, and season"],"tip":"High heat and speed are key to keeping spinach crisp"},
            {"title":"Green Spinach Smoothie","time":"5 min","calories":"130 kcal","level":"Easy","steps":["Add a handful of spinach, banana, almond milk to blender","Add honey and lemon juice","Blend until smooth","Add ice and serve cold"],"tip":"Banana sweetness masks the grassy spinach taste perfectly"},
            {"title":"Spinach & Cheese Quiche","time":"40 min","calories":"320 kcal","level":"Medium","steps":["Press pastry into tin and prick with fork","Sauté spinach and squeeze out all moisture","Mix eggs, cream, cheese, spinach for filling","Bake at 180°C for 30 min"],"tip":"Squeezing out every drop of moisture prevents a soggy quiche"},
        ],
    },
    "garlic": {
        "ko": [
            {"title":"마늘 올리브오일 파스타","time":"20분","calories":"380 kcal","level":"쉬움","steps":["파스타를 소금물에 삶는다","팬에 올리브오일을 두르고 마늘을 볶는다","파스타·면수를 넣어 섞는다","페퍼론치노·파마산·파슬리로 마무리한다"],"tip":"마늘은 약불에서 황금빛이 될 때까지 천천히 볶아야 향이 깊어요"},
            {"title":"마늘 버터 새우","time":"15분","calories":"250 kcal","level":"쉬움","steps":["새우를 손질한다","팬에 버터를 녹이고 마늘을 볶는다","새우를 넣어 분홍빛이 될 때까지 굽는다","레몬즙·파슬리를 뿌려 완성한다"],"tip":"새우는 익으면 바로 꺼내야 쫄깃한 식감이 살아요"},
            {"title":"흑마늘 꿀 드레싱 샐러드","time":"10분","calories":"160 kcal","level":"쉬움","steps":["흑마늘 3알을 으깬다","꿀·발사믹·올리브오일·소금을 섞는다","샐러드 채소를 준비한다","드레싱을 뿌려 완성한다"],"tip":"흑마늘은 발효되면서 생마늘보다 달콤하고 부드러워요"},
            {"title":"마늘 감자 수프","time":"30분","calories":"220 kcal","level":"쉬움","steps":["마늘 한 통을 통째로 오븐에 구워 짠다","감자·양파를 채수에 끓인다","구운 마늘을 넣고 핸드블렌더로 간다","생크림·소금·후추로 마무리한다"],"tip":"마늘을 통째로 구우면 쓴맛이 사라지고 달콤해져요"},
            {"title":"마늘 간장 닭볶음","time":"40분","calories":"450 kcal","level":"보통","steps":["닭을 한 입 크기로 자른다","간장·마늘·설탕·고춧가루로 양념을 만든다","닭에 양념을 버무려 팬에 볶는다","감자·당근을 넣고 물을 부어 20분 졸인다"],"tip":"처음엔 강불, 나중엔 약불로 서서히 조리면 양념이 잘 베요"},
        ],
        "en": [
            {"title":"Aglio e Olio Pasta","time":"20 min","calories":"380 kcal","level":"Easy","steps":["Cook pasta in heavily salted water","Heat olive oil and slowly sauté garlic until golden","Add pasta with a splash of pasta water","Finish with chili flakes, parmesan, and parsley"],"tip":"Low and slow for garlic — golden not burnt is the goal"},
            {"title":"Garlic Butter Shrimp","time":"15 min","calories":"250 kcal","level":"Easy","steps":["Clean and devein shrimp","Melt butter in pan and sauté garlic","Cook shrimp until just pink on both sides","Finish with lemon juice and parsley"],"tip":"Remove shrimp the moment they turn pink to keep them juicy"},
            {"title":"Black Garlic Honey Salad","time":"10 min","calories":"160 kcal","level":"Easy","steps":["Mash 3 cloves of black garlic","Mix with honey, balsamic, olive oil, salt","Prepare salad greens","Drizzle dressing to finish"],"tip":"Black garlic is sweeter and milder than raw thanks to fermentation"},
            {"title":"Roasted Garlic Potato Soup","time":"30 min","calories":"220 kcal","level":"Easy","steps":["Roast a whole head of garlic in oven until caramelised","Simmer potato and onion in vegetable broth","Squeeze in roasted garlic and blend smooth","Finish with heavy cream, salt, and pepper"],"tip":"Whole-roasting garlic removes bitterness and adds sweetness"},
            {"title":"Garlic Soy Braised Chicken","time":"40 min","calories":"450 kcal","level":"Medium","steps":["Cut chicken into bite-sized pieces","Make sauce: soy sauce, garlic, sugar, gochugaru","Toss chicken in sauce and stir-fry","Add potato, carrot, and water; braise 20 min"],"tip":"Start on high heat then reduce to low so the sauce soaks in evenly"},
        ],
    },
    "walnut": {
        "ko": [
            {"title":"호두죽","time":"25분","calories":"280 kcal","level":"보통","steps":["호두를 30분 불려 물 1컵과 함께 곱게 간다","찹쌀을 씻어 대충 갈아준다","호두즙과 찹쌀을 냄비에 넣고 저으며 끓인다","걸쭉해지면 소금과 꿀로 간한다"],"tip":"계속 저어야 눌어붙지 않아요"},
            {"title":"호두 시금치 샐러드","time":"12분","calories":"240 kcal","level":"쉬움","steps":["호두를 팬에 살짝 볶는다","시금치·사과·크랜베리를 준비한다","발사믹 드레싱을 만든다","재료를 섞고 호두를 올린다"],"tip":"호두를 볶으면 고소함이 두 배로 살아나요"},
            {"title":"호두 브라우니","time":"35분","calories":"280 kcal","level":"보통","steps":["다크초콜릿과 버터를 중탕으로 녹인다","달걀·설탕을 넣어 섞는다","밀가루·코코아·소금·호두를 섞는다","180도 오븐에서 25분 굽는다"],"tip":"오버베이킹하면 퍽퍽해지니 이쑤시개로 중심을 확인해요"},
            {"title":"호두 귀리 쿠키","time":"25분","calories":"160 kcal","level":"쉬움","steps":["귀리·통밀가루·설탕·버터를 섞는다","달걀·바닐라를 넣는다","호두·건포도를 넣어 반죽한다","180도 오븐에서 12분 굽는다"],"tip":"반죽을 냉장고에 30분 두었다가 구우면 더 바삭해요"},
            {"title":"호두 바나나 스무디","time":"5분","calories":"280 kcal","level":"쉬움","steps":["바나나·호두·아몬드밀크를 블렌더에 넣는다","꿀·시나몬을 넣는다","곱게 간다","컵에 담고 호두를 올린다"],"tip":"얼린 바나나를 쓰면 더 걸쭉하고 아이스크림 같아요"},
        ],
        "en": [
            {"title":"Walnut Porridge","time":"25 min","calories":"280 kcal","level":"Medium","steps":["Soak walnuts 30 min, blend with 1 cup water until smooth","Roughly blend soaked glutinous rice","Combine walnut milk and rice in pot, stir constantly while cooking","Season with salt and honey when thickened"],"tip":"Constant stirring prevents burning at the bottom"},
            {"title":"Walnut Spinach Salad","time":"12 min","calories":"240 kcal","level":"Easy","steps":["Lightly toast walnuts in dry pan","Prepare spinach, sliced apple, and dried cranberries","Make balsamic dressing","Toss and top with walnuts"],"tip":"Toasting walnuts doubles their nuttiness and crunch"},
            {"title":"Walnut Brownies","time":"35 min","calories":"280 kcal","level":"Medium","steps":["Melt dark chocolate and butter in double boiler","Stir in eggs and sugar","Fold in flour, cocoa, salt, and walnuts","Bake at 180°C for 25 minutes"],"tip":"Check with a toothpick — a few moist crumbs means perfect fudgy texture"},
            {"title":"Walnut Oat Cookies","time":"25 min","calories":"160 kcal","level":"Easy","steps":["Mix oats, whole wheat flour, sugar, and butter","Beat in egg and vanilla","Fold in walnuts and raisins","Bake at 180°C for 12 minutes"],"tip":"Chill dough in fridge 30 min for crispier cookies"},
            {"title":"Walnut Banana Smoothie","time":"5 min","calories":"280 kcal","level":"Easy","steps":["Blend banana, walnuts, and almond milk","Add honey and cinnamon","Blend smooth","Top with crushed walnuts"],"tip":"Frozen banana makes it thick and ice-cream-like"},
        ],
    },
    "mushroom": {
        "ko": [
            {"title":"표고버섯 된장국","time":"15분","calories":"90 kcal","level":"쉬움","steps":["건표고버섯을 30분 불려 슬라이스한다","멸치 육수를 낸다","된장을 풀고 표고버섯·두부·애호박을 넣는다","8분 끓이고 파를 올린다"],"tip":"표고버섯 불린 물을 육수로 쓰면 감칠맛이 두 배예요"},
            {"title":"표고버섯 잡채","time":"35분","calories":"350 kcal","level":"보통","steps":["당면을 삶고, 표고버섯·시금치·당근·양파를 준비한다","각 재료를 따로 간장·참기름으로 볶는다","당면에 모든 재료를 넣고 간장·참기름·설탕으로 버무린다","달걀지단을 올려 마무리한다"],"tip":"재료를 따로 볶아야 각자의 맛과 색이 살아요"},
            {"title":"표고버섯 크림파스타","time":"25분","calories":"480 kcal","level":"보통","steps":["표고버섯을 버터에 노릇하게 볶는다","마늘을 넣고 1분 더 볶는다","생크림을 붓고 약하게 끓인다","삶은 파스타와 버무리고 파마산·타임으로 마무리한다"],"tip":"표고버섯을 센불에 볶아야 수분이 빠지고 쫄깃해져요"},
            {"title":"표고버섯 전","time":"15분","calories":"180 kcal","level":"쉬움","steps":["표고버섯 기둥을 자르고 납작하게 편다","소금 간을 하고 밀가루·달걀물을 입힌다","중불에서 양면을 노릇하게 굽는다","초간장과 함께 낸다"],"tip":"밀가루를 얇게 입혀야 버섯 향이 살아요"},
            {"title":"표고버섯 구이","time":"12분","calories":"100 kcal","level":"쉬움","steps":["표고버섯을 씻어 기둥을 제거한다","올리브오일·마늘·파마산·허브로 양념한다","200도 오븐에서 10분 굽는다","레몬즙을 뿌려 마무리한다"],"tip":"갓 부분이 위를 향하게 놓아야 즙이 고여요"},
        ],
        "en": [
            {"title":"Shiitake Doenjang Soup","time":"15 min","calories":"90 kcal","level":"Easy","steps":["Soak dried shiitake 30 min and slice","Make anchovy broth","Dissolve doenjang, add shiitake, tofu, zucchini","Simmer 8 min and garnish with scallions"],"tip":"Use shiitake soaking water as broth for double the umami"},
            {"title":"Japchae (Glass Noodles)","time":"35 min","calories":"350 kcal","level":"Medium","steps":["Cook glass noodles, prepare shiitake, spinach, carrot, onion","Stir-fry each ingredient separately with soy and sesame","Combine noodles with all ingredients, season with soy, sesame, sugar","Top with egg strips to finish"],"tip":"Stir-frying each ingredient separately preserves individual flavours"},
            {"title":"Shiitake Cream Pasta","time":"25 min","calories":"480 kcal","level":"Medium","steps":["Pan-fry shiitake in butter until golden","Add garlic and cook 1 more minute","Pour in heavy cream and bring to gentle simmer","Toss with cooked pasta and finish with parmesan and thyme"],"tip":"High heat removes moisture and makes shiitake wonderfully chewy"},
            {"title":"Shiitake Jeon (Pancake)","time":"15 min","calories":"180 kcal","level":"Easy","steps":["Trim stem and flatten shiitake caps","Season with salt, coat in flour then egg wash","Pan-fry over medium heat until golden on both sides","Serve with soy vinegar dipping sauce"],"tip":"A thin flour coat lets the mushroom flavour shine through"},
            {"title":"Roasted Shiitake","time":"12 min","calories":"100 kcal","level":"Easy","steps":["Rinse shiitake and remove stems","Season with olive oil, garlic, parmesan, herbs","Roast at 200°C for 10 minutes","Finish with a squeeze of lemon juice"],"tip":"Place caps facing upward to collect the natural juices"},
        ],
    },
}

# 그 외 식재료는 기본 5개 레시피 세트로 처리 (식재료마다 다른 요리)
DEFAULT_RECIPE_SETS = {
    "sweet_potato": {
        "ko":[
            {"title":"군고구마","time":"40분","calories":"130 kcal","level":"쉬움","steps":["고구마를 깨끗이 씻는다","호일로 감싼다","200도에서 35~40분 굽는다","칼집을 넣고 버터를 곁들여 낸다"],"tip":"호일 없이 직접 구우면 더 달콤해요"},
            {"title":"고구마 라떼","time":"10분","calories":"180 kcal","level":"쉬움","steps":["고구마를 쪄서 으깬다","따뜻한 우유에 으깬 고구마를 넣는다","꿀·시나몬을 넣는다","핸드블렌더로 갈아 완성한다"],"tip":"고구마가 달콤할수록 꿀을 덜 넣어도 돼요"},
            {"title":"고구마 그라탱","time":"40분","calories":"290 kcal","level":"보통","steps":["고구마를 얇게 슬라이스한다","생크림·마늘·소금·후추로 크림소스를 만든다","용기에 고구마를 쌓고 크림소스를 붓는다","180도에서 25분 굽고 치즈를 올려 10분 더 굽는다"],"tip":"고구마를 만돌린으로 균일하게 썰어야 고루 익어요"},
            {"title":"고구마 카레","time":"30분","calories":"310 kcal","level":"쉬움","steps":["고구마를 깍둑썬다","양파·마늘을 볶는다","카레 파우더·코코넛밀크·고구마를 넣는다","20분 졸여 밥과 함께 낸다"],"tip":"코코넛밀크 대신 생크림을 써도 맛있어요"},
            {"title":"구운 고구마 타코","time":"35분","calories":"340 kcal","level":"보통","steps":["고구마를 웨지 모양으로 썰어 큐민·파프리카로 양념한다","200도 오븐에서 25분 굽는다","토르티야에 구운 고구마를 올린다","아보카도·살사·고수를 더해 완성한다"],"tip":"고구마 웨지는 두껍게 썰어야 속이 부드러워요"},
        ],
        "en":[
            {"title":"Baked Sweet Potato","time":"40 min","calories":"130 kcal","level":"Easy","steps":["Wash sweet potatoes thoroughly","Wrap in aluminum foil","Bake at 200°C for 35–40 min until fork-tender","Slice open and serve with butter"],"tip":"Baking without foil creates a sweeter, caramelised skin"},
            {"title":"Sweet Potato Latte","time":"10 min","calories":"180 kcal","level":"Easy","steps":["Steam and mash sweet potato","Stir into warm milk","Add honey and cinnamon","Blend with hand blender for smooth texture"],"tip":"Sweeter potatoes need less honey"},
            {"title":"Sweet Potato Gratin","time":"40 min","calories":"290 kcal","level":"Medium","steps":["Slice sweet potatoes very thinly","Make cream sauce with heavy cream, garlic, salt, pepper","Layer in dish and pour cream sauce over","Bake 25 min, add cheese, bake 10 min more"],"tip":"Use a mandoline for uniform slices that cook evenly"},
            {"title":"Sweet Potato Curry","time":"30 min","calories":"310 kcal","level":"Easy","steps":["Cube sweet potato","Sauté onion and garlic","Add curry powder, coconut milk, sweet potato","Simmer 20 min and serve with rice"],"tip":"Heavy cream works as a great substitute for coconut milk"},
            {"title":"Roasted Sweet Potato Tacos","time":"35 min","calories":"340 kcal","level":"Medium","steps":["Cut into wedges, season with cumin and paprika","Roast at 200°C for 25 min","Place on tortillas","Add avocado, salsa, and cilantro to finish"],"tip":"Cut wedges thick so the inside stays fluffy and soft"},
        ],
    },
}

@st.cache_data
def load_all_foods():
    return [
        {"id":"quinoa","emoji":"🌾","name_ko":"퀴노아","name_en":"Quinoa","name_zh":"藜麦","tag_ko":"완전단백질 슈퍼씨앗","tag_en":"Complete Plant Protein","tag_zh":"全蛋白超级种子","badge_ko":"글루텐프리","badge_en":"Gluten-Free","badge_zh":"无麸质","desc_ko":"필수 아미노산이 균형 있게 함유된 슈퍼 곡물입니다.","desc_en":"Rich in all 9 essential amino acids — one of the only grains to achieve this.","desc_zh":"包含人体所有必需氨基酸。","cal":368,"pro":14.1,"car":64.0,"fat":6.1,"fib":7.0,"iron":4.6,"video_url":"https://www.youtube.com/results?search_query=quinoa+recipe"},
        {"id":"avocado","emoji":"🥑","name_ko":"아보카도","name_en":"Avocado","name_zh":"牛油果","tag_ko":"단일불포화지방산","tag_en":"Healthy Fats","tag_zh":"单不饱和脂肪","badge_ko":"비타민E","badge_en":"Vitamin E","badge_zh":"富含维E","desc_ko":"불포화 지방산이 풍부해 심혈관 건강에 훌륭합니다.","desc_en":"Packed with heart-healthy monounsaturated fats and more potassium than a banana.","desc_zh":"含有对人体有益的健康油脂。","cal":160,"pro":2.0,"car":8.5,"fat":14.7,"fib":6.7,"iron":0.6,"video_url":"https://www.youtube.com/results?search_query=avocado+recipe"},
        {"id":"tofu","emoji":"🫘","name_ko":"두부","name_en":"Tofu","name_zh":"豆腐","tag_ko":"식물성 완전단백질","tag_en":"Soy Plant Protein","tag_zh":"植物性优质蛋白","badge_ko":"저칼로리","badge_en":"Low-Calorie","badge_zh":"低热量","desc_ko":"콩 단백질을 압착하여 만든 고단백 건강 재료입니다.","desc_en":"High-protein and low-calorie — perfect for weight management and bone health.","desc_zh":"高消化率植物高蛋白食材。","cal":84,"pro":8.9,"car":2.9,"fat":4.8,"fib":0.2,"iron":1.5,"video_url":"https://www.youtube.com/results?search_query=tofu+recipe"},
        {"id":"blueberry","emoji":"🫐","name_ko":"블루베리","name_en":"Blueberry","name_zh":"蓝莓","tag_ko":"안토시아닌 항산화","tag_en":"Antioxidant Power","tag_zh":"强效抗氧化","badge_ko":"비타민C","badge_en":"Vitamin C+","badge_zh":"富含维C","desc_ko":"안토시아닌이 활성산소를 억제하고 눈을 보호합니다.","desc_en":"One of the highest antioxidant foods known — great for brain and eye health.","desc_zh":"富含花青素，清除自由基效果极佳。","cal":57,"pro":0.7,"car":14.5,"fat":0.3,"fib":2.4,"iron":0.3,"video_url":"https://www.youtube.com/results?search_query=blueberry+recipe"},
        {"id":"kelp","emoji":"🌊","name_ko":"다시마","name_en":"Kelp","name_zh":"昆布","tag_ko":"해조류 식이섬유 왕","tag_en":"Iodine & Fibre King","tag_zh":"海藻膳食纤维王","badge_ko":"알긴산 풍부","badge_en":"Alginic Acid","badge_zh":"富含褐藻酸","desc_ko":"다시마는 풍부한 알긴산과 장 건강에 좋은 식이섬유의 보고입니다.","desc_en":"Rich in iodine, alginic acid, and soluble fibre for thyroid and gut health.","desc_zh":"富含微量元素与大量水溶性膳食纤维。","cal":43,"pro":1.7,"car":9.6,"fat":0.6,"fib":1.3,"iron":2.8,"video_url":"https://www.youtube.com/results?search_query=kelp+recipe"},
        {"id":"salmon","emoji":"🐟","name_ko":"연어","name_en":"Salmon","name_zh":"三文鱼","tag_ko":"오메가-3의 대명사","tag_en":"Omega-3 Rich Fish","tag_zh":"富含欧米伽-3","badge_ko":"고단백질","badge_en":"High Protein","badge_zh":"高蛋白质","desc_ko":"연어는 혈관 건강을 지켜주는 오메가-3 지방산이 매우 풍부합니다.","desc_en":"Excellent source of EPA and DHA omega-3s for brain, heart, and inflammation.","desc_zh":"富含深海不饱和脂肪酸，保护心血管健康。","cal":208,"pro":20.0,"car":0.0,"fat":13.0,"fib":0.0,"iron":0.3,"video_url":"https://www.youtube.com/results?search_query=salmon+recipe"},
        {"id":"spinach","emoji":"🥬","name_ko":"시금치","name_en":"Spinach","name_zh":"菠菜","tag_ko":"철분 가득 녹색채소","tag_en":"Iron-Rich Green","tag_zh":"富含铁质绿叶菜","badge_ko":"엽산 풍부","badge_en":"Folic Acid","badge_zh":"富含叶酸","desc_ko":"시금치는 유기산과 철분, 비타민이 고루 배합된 채소입니다.","desc_en":"Dense in iron, folate, vitamin K, and powerful antioxidants.","desc_zh":"富含叶酸与无机盐，是贫血的天然调理佳品。","cal":23,"pro":2.9,"car":3.6,"fat":0.4,"fib":2.2,"iron":2.7,"video_url":"https://www.youtube.com/results?search_query=spinach+recipe"},
        {"id":"garlic","emoji":"🧄","name_ko":"마늘","name_en":"Garlic","name_zh":"大蒜","tag_ko":"천연 면역 강화제","tag_en":"Natural Immunity","tag_zh":"天然免疫增强剂","badge_ko":"알리신 함유","badge_en":"Allicin Power","badge_zh":"富含蒜素","desc_ko":"알리신 성분이 강력한 항균 작용과 면역을 촉진합니다.","desc_en":"Allicin provides powerful antibacterial and immune-boosting properties.","desc_zh":"大蒜素具有极强的抗菌功效。","cal":149,"pro":6.4,"car":33.1,"fat":0.5,"fib":2.1,"iron":1.7,"video_url":"https://www.youtube.com/results?search_query=garlic+recipe"},
        {"id":"walnut","emoji":"🥜","name_ko":"호두","name_en":"Walnut","name_zh":"核桃","tag_ko":"두뇌 활성화 견과","tag_en":"Brain Superfood","tag_zh":"健脑益智坚果","badge_ko":"불포화지방","badge_en":"Healthy Lipids","badge_zh":"优质脂肪","desc_ko":"뇌 세포를 보호하고 인지 능력을 개선하는 견과류입니다.","desc_en":"Rich in omega-3 ALA and polyphenols that reduce oxidative stress.","desc_zh":"富含不饱和脂肪酸与亚麻酸，有益脑部健康。","cal":654,"pro":15.2,"car":13.7,"fat":65.2,"fib":6.7,"iron":2.9,"video_url":"https://www.youtube.com/results?search_query=walnut+recipe"},
        {"id":"mushroom","emoji":"🍄","name_ko":"표고버섯","name_en":"Shiitake","name_zh":"香菇","tag_ko":"면역 베타글루칸","tag_en":"Beta-Glucan Core","tag_zh":"富含β-聚糖","badge_ko":"비타민D","badge_en":"Vitamin D","badge_zh":"富含维D","desc_ko":"베타글루칸 성분이 가득하여 면역 조절에 탁월합니다.","desc_en":"Lentinan and beta-glucan powerfully modulate immune function.","desc_zh":"独特的鲜味成分，具有极高的免疫调节功效。","cal":34,"pro":2.2,"car":6.8,"fat":0.5,"fib":2.5,"iron":0.4,"video_url":"https://www.youtube.com/results?search_query=shiitake+recipe"},
        {"id":"sweet_potato","emoji":"🍠","name_ko":"고구마","name_en":"Sweet Potato","name_zh":"红薯","tag_ko":"베타카로틴 식이섬유","tag_en":"Beta-Carotene Energy","tag_zh":"富含β-胡萝卜素","badge_ko":"낮은GI","badge_en":"Low GI","badge_zh":"低GI","desc_ko":"식이섬유가 풍부해 소화가 잘되고 장 건강에 좋습니다.","desc_en":"Loaded with beta-carotene and fibre, with a lower GI than white potato.","desc_zh":"富含复杂的碳水化合物与维生素A。","cal":86,"pro":1.6,"car":20.1,"fat":0.1,"fib":3.0,"iron":0.6,"video_url":"https://www.youtube.com/results?search_query=sweet+potato+recipe"},
        {"id":"tomato","emoji":"🍅","name_ko":"토마토","name_en":"Tomato","name_zh":"西红柿","tag_ko":"라이코펜 항산화","tag_en":"Lycopene Shield","tag_zh":"番茄红素抗氧化","badge_ko":"심혈관케어","badge_en":"Heart Care","badge_zh":"益于心血管","desc_ko":"라이코펜이 풍부하여 세포 노화를 방지하고 혈압을 낮춥니다.","desc_en":"Cooked tomatoes release more lycopene — a potent antioxidant.","desc_zh":"熟吃更能释放番茄红素成分。","cal":18,"pro":0.9,"car":3.9,"fat":0.2,"fib":1.2,"iron":0.3,"video_url":"https://www.youtube.com/results?search_query=tomato+recipe"},
        {"id":"broccoli","emoji":"🥦","name_ko":"브로콜리","name_en":"Broccoli","name_zh":"西兰花","tag_ko":"설포라판 비타민C","tag_en":"Sulforaphane Green","tag_zh":"富含萝卜硫素","badge_ko":"해독작용","badge_en":"Detox","badge_zh":"自然排毒","desc_ko":"설포라판 성분이 위장 건강과 해독 작용을 돕습니다.","desc_en":"Sulforaphane has powerful anti-cancer properties. More vitamin C than an orange.","desc_zh":"十字花科蔬菜，富含微量元素与抗癌成分。","cal":34,"pro":2.8,"car":7.0,"fat":0.4,"fib":2.6,"iron":0.7,"video_url":"https://www.youtube.com/results?search_query=broccoli+recipe"},
        {"id":"oatmeal","emoji":"🥣","name_ko":"오트밀","name_en":"Oats","name_zh":"燕麦","tag_ko":"베타글루칸 콜레스테롤","tag_en":"Beta-Glucan Heart","tag_zh":"降胆固醇燕麦","badge_ko":"식이섬유깡패","badge_en":"High Fiber","badge_zh":"高膳食纤维","desc_ko":"수용성 식이섬유가 풍부해 콜레스테롤 수치를 대폭 낮춥니다.","desc_en":"Beta-glucan is clinically proven to lower LDL cholesterol.","desc_zh":"饱腹感强，有效调节血糖与胆固醇。","cal":389,"pro":16.9,"car":66.3,"fat":6.9,"fib":10.6,"iron":4.7,"video_url":"https://www.youtube.com/results?search_query=oatmeal+recipe"},
        {"id":"green_tea","emoji":"🍵","name_ko":"녹차","name_en":"Green Tea","name_zh":"绿茶","tag_ko":"카테킨 신진대사","tag_en":"Catechin Metabolism","tag_zh":"儿茶素代谢","badge_ko":"체지방감소","badge_en":"Fat Burn","badge_zh":"减少脂肪","desc_ko":"카테킨 성분이 지방 연소를 돕고 체내 염증을 억제합니다.","desc_en":"EGCG catechins boost metabolism and reduce systemic inflammation.","desc_zh":"抗氧化效果佳，清新提神，促进脂肪代谢。","cal":1,"pro":0.2,"car":0.0,"fat":0.0,"fib":0.0,"iron":0.0,"video_url":"https://www.youtube.com/results?search_query=green+tea+recipe"},
        {"id":"egg","emoji":"🥚","name_ko":"계란","name_en":"Egg","name_zh":"鸡蛋","tag_ko":"완전무결 단백질","tag_en":"Perfect Bio-Protein","tag_zh":"完美优质蛋白","badge_ko":"콜린 가득","badge_en":"Choline Source","badge_zh":"富含胆碱","desc_ko":"기억력 향상에 도움을 주는 콜린과 양질의 단백질 덩어리입니다.","desc_en":"Nature's most complete protein with all essential amino acids plus brain-boosting choline.","desc_zh":"提供最均衡的必须氨基酸与卵磷脂。","cal":155,"pro":12.6,"car":1.1,"fat":10.6,"fib":0.0,"iron":1.2,"video_url":"https://www.youtube.com/results?search_query=egg+recipe"},
        {"id":"chicken_breast","emoji":"🍗","name_ko":"닭가슴살","name_en":"Chicken Breast","name_zh":"鸡胸肉","tag_ko":"근육 생성의 기초","tag_en":"Pure Lean Muscle","tag_zh":"纯净增肌大王","badge_ko":"초저지방","badge_en":"Ultra Lean","badge_zh":"超低脂肪","desc_ko":"지방 함량이 거의 없고 단백질 비율이 극도로 높은 다이어트 식재료입니다.","desc_en":"The king of lean protein — essential for muscle building and weight management.","desc_zh":"高蛋白低脂肪，减脂控形必备食材。","cal":165,"pro":31.0,"car":0.0,"fat":3.6,"fib":0.0,"iron":1.0,"video_url":"https://www.youtube.com/results?search_query=chicken+breast+recipe"},
        {"id":"banana","emoji":"🍌","name_ko":"바나나","name_en":"Banana","name_zh":"香蕉","tag_ko":"칼륨 운동에너지","tag_en":"Potassium Boost","tag_zh":"高钾运动机能","badge_ko":"피로회복","badge_en":"Energy Source","badge_zh":"恢复疲劳","desc_ko":"칼륨이 풍부해 나트륨 배출을 돕고 운동 전 에너지 보충에 좋습니다.","desc_en":"Instant natural energy with potassium for muscle function and cramp prevention.","desc_zh":"极佳的天然能量补充水果，富含钾元素。","cal":89,"pro":1.1,"car":22.8,"fat":0.3,"fib":2.6,"iron":0.3,"video_url":"https://www.youtube.com/results?search_query=banana+recipe"},
        {"id":"apple","emoji":"🍎","name_ko":"사과","name_en":"Apple","name_zh":"苹果","tag_ko":"펙틴 아침의 사과","tag_en":"Pectin Digestion","tag_zh":"果胶清肠胃","badge_ko":"장운동원활","badge_en":"Gut Health","badge_zh":"肠道健康","desc_ko":"펙틴 성분이 장내 유익균을 증식시키고 배변 활동을 활발하게 유도합니다.","desc_en":"Soluble pectin fibre feeds beneficial gut bacteria and supports digestion.","desc_zh":"富含维生素C与水溶性果胶，有益肠道健康。","cal":52,"pro":0.3,"car":13.8,"fat":0.2,"fib":2.4,"iron":0.1,"video_url":"https://www.youtube.com/results?search_query=apple+recipe"},
        {"id":"carrot","emoji":"🥕","name_ko":"당근","name_en":"Carrot","name_zh":"胡萝卜","tag_ko":"비타민A 야맹증예방","tag_en":"Vision Vitamin A","tag_zh":"明目维A之王","badge_ko":"시력보호","badge_en":"Eye Health","badge_zh":"保护视力","desc_ko":"체내에서 비타민A로 전환되는 베타카로틴이 채소 중 가장 많습니다.","desc_en":"Highest beta-carotene content of any vegetable — converts to vitamin A for eye health.","desc_zh":"富含类胡萝卜素，明目护肤效果显著。","cal":41,"pro":0.9,"car":9.6,"fat":0.2,"fib":2.8,"iron":0.3,"video_url":"https://www.youtube.com/results?search_query=carrot+recipe"},
        {"id":"onion","emoji":"🧅","name_ko":"양파","name_en":"Onion","name_zh":"洋葱","tag_ko":"퀘르세틴 혈액순환","tag_en":"Quercetin Blood Flow","tag_zh":"槲皮素降血脂","badge_ko":"혈관정화","badge_en":"Vessel Clean","badge_zh":"清理血管","desc_ko":"퀘르세틴 성분이 혈전 형성을 방지하고 피를 맑게 해줍니다.","desc_en":"Quercetin prevents blood clot formation and supports cardiovascular health.","desc_zh":"强效抗氧化，软化心血管。","cal":40,"pro":1.1,"car":9.3,"fat":0.1,"fib":1.7,"iron":0.2,"video_url":"https://www.youtube.com/results?search_query=onion+recipe"},
        {"id":"ginger","emoji":"🫚","name_ko":"생강","name_en":"Ginger","name_zh":"生姜","tag_ko":"진저롤 체온상승","tag_en":"Gingerol Warmth","tag_zh":"姜辣素驱寒","badge_ko":"항염효과","badge_en":"Anti-Inflam","badge_zh":"温中抗炎","desc_ko":"진저롤이 체온을 높여 면역력을 증진하고 혈액 순환을 개선합니다.","desc_en":"Gingerol is one of the most powerful anti-inflammatory compounds in nature.","desc_zh":"暖胃散寒，促进新陈代谢，天然抗炎。","cal":80,"pro":1.8,"car":17.8,"fat":0.8,"fib":2.0,"iron":0.6,"video_url":"https://www.youtube.com/results?search_query=ginger+recipe"},
        {"id":"honey","emoji":"🍯","name_ko":"꿀","name_en":"Honey","name_zh":"蜂蜜","tag_ko":"천연에너지 피로회복","tag_en":"Pure Natural Energy","tag_zh":"天然滋补能量","badge_ko":"기력보충","badge_en":"Vitality","badge_zh":"快速补充","desc_ko":"체내에 즉각 흡수되는 천연 단당류로 피로회복에 직효입니다.","desc_en":"Natural antibacterial enzymes plus instant energy from natural sugars.","desc_zh":"含有多种微量活性酶与矿物质。","cal":304,"pro":0.3,"car":82.4,"fat":0.0,"fib":0.0,"iron":0.4,"video_url":"https://www.youtube.com/results?search_query=honey+recipe"},
        {"id":"lemon","emoji":"🍋","name_ko":"레몬","name_en":"Lemon","name_zh":"柠檬","tag_ko":"구연산 피로물질제거","tag_en":"Citric Detox","tag_zh":"柠檬酸排毒","badge_ko":"비타민C폭탄","badge_en":"Vitamin C","badge_zh":"高维C","desc_ko":"구연산이 가득해 젖산을 분해하고 몸을 약알칼리성으로 가꿔줍니다.","desc_en":"Citric acid breaks down lactic acid and alkalises the body's pH.","desc_zh":"美白抗氧化，增强血管弹性与代谢。","cal":29,"pro":1.1,"car":9.3,"fat":0.3,"fib":2.8,"iron":0.6,"video_url":"https://www.youtube.com/results?search_query=lemon+recipe"},
        {"id":"cabbage","emoji":"🥬","name_ko":"양배추","name_en":"Cabbage","name_zh":"卷心菜","tag_ko":"비타민U 위벽보호","tag_en":"Vitamin U Gut","tag_zh":"维U保护胃黏膜","badge_ko":"위건강케어","badge_en":"Stomach Care","badge_zh":"养胃圣品","desc_ko":"비타민U 성분이 상처 난 위 점막의 재생을 강력하게 도와줍니다.","desc_en":"Vitamin U (S-methylmethionine) helps repair damaged stomach lining.","desc_zh":"富含维生素U及粗纤维，养胃护胃。","cal":25,"pro":1.3,"car":5.8,"fat":0.1,"fib":2.5,"iron":0.5,"video_url":"https://www.youtube.com/results?search_query=cabbage+recipe"},
        {"id":"potato","emoji":"🥔","name_ko":"감자","name_en":"Potato","name_zh":"土豆","tag_ko":"전분보호 비타민C","tag_en":"Stable Vit C","tag_zh":"抗热维生素C","badge_ko":"위염완화","badge_en":"Stomach Clean","badge_zh":"调理脾胃","desc_ko":"익혀도 파괴되지 않는 비타민C와 풍부한 칼륨이 특징입니다.","desc_en":"Unique starch protects vitamin C from heat — plus high potassium content.","desc_zh":"不易随加热流失的维生素C，富含钾元素。","cal":77,"pro":2.0,"car":17.5,"fat":0.1,"fib":2.2,"iron":0.8,"video_url":"https://www.youtube.com/results?search_query=potato+recipe"},
        {"id":"pumpkin","emoji":"🎃","name_ko":"단호박","name_en":"Pumpkin","name_zh":"南瓜","tag_ko":"붓기제거 이뇨작용","tag_en":"Anti-Swelling","tag_zh":"利尿消肿神物","badge_ko":"다이어트식","badge_en":"Slim Diet","badge_zh":"低卡轻盈","desc_ko":"이뇨작용을 촉진해 몸의 붓기를 빼주고 칼로리가 무척 낮습니다.","desc_en":"Beta-carotene-dense squash with diuretic properties and very low calories.","desc_zh":"维生素A和碳水结合的高饱腹感低卡食材。","cal":26,"pro":1.0,"car":6.5,"fat":0.1,"fib":0.5,"iron":0.8,"video_url":"https://www.youtube.com/results?search_query=pumpkin+recipe"},
        {"id":"milk","emoji":"🥛","name_ko":"우유","name_en":"Milk","name_zh":"牛奶","tag_ko":"칼슘의 왕 골다공증","tag_en":"Calcium Source","tag_zh":"补钙黄金资源","badge_ko":"뼈건강","badge_en":"Bone Health","badge_zh":"坚固骨骼","desc_ko":"흡수율이 매우 높은 천연 칼슘이 들어있어 골밀도를 강화합니다.","desc_en":"Highly bioavailable calcium and vitamin D for strong bones and teeth.","desc_zh":"最直观容易吸收的乳钙来源。","cal":42,"pro":3.4,"car":5.0,"fat":1.0,"fib":0.0,"iron":0.1,"video_url":"https://www.youtube.com/results?search_query=milk+recipe"},
        {"id":"almond","emoji":"🫘","name_ko":"아몬드","name_en":"Almond","name_zh":"杏仁","tag_ko":"불포화지방 비타민E","tag_en":"Lipid Vitamin E","tag_zh":"富含强抗氧化维E","badge_ko":"항노화","badge_en":"Anti-Aging","badge_zh":"延缓衰老","desc_ko":"강력한 항산화제인 비타민E가 노화를 막고 피부를 가꿔줍니다.","desc_en":"Highest vitamin E content of any nut — powerful antioxidant for skin and cells.","desc_zh":"含有优质不饱和油和膳食纤维，延缓衰老。","cal":579,"pro":21.2,"car":21.7,"fat":49.9,"fib":12.5,"iron":3.7,"video_url":"https://www.youtube.com/results?search_query=almond+recipe"},
        {"id":"shrimp","emoji":"🦐","name_ko":"새우","name_en":"Shrimp","name_zh":"大虾","tag_ko":"키토산 타우린 피로","tag_en":"Taurine Marine","tag_zh":"富含牛磺酸","badge_ko":"피로타파","badge_en":"Energy Recover","badge_zh":"恢复活力","desc_ko":"타우린이 가득해 간 해독을 돕고 혈중 콜레스테롤을 낮춰줍니다.","desc_en":"Taurine aids liver detox while providing lean, low-calorie marine protein.","desc_zh":"极低卡的高级海鲜蛋白质，富含牛磺酸。","cal":85,"pro":20.1,"car":0.2,"fat":0.5,"fib":0.0,"iron":0.5,"video_url":"https://www.youtube.com/results?search_query=shrimp+recipe"},
        {"id":"chili","emoji":"🌶️","name_ko":"고추","name_en":"Chili Pepper","name_zh":"辣椒","tag_ko":"캡사이신 기초대사량","tag_en":"Capsaicin Fire","tag_zh":"辣椒素新陈代谢","badge_ko":"지방연소","badge_en":"Burn Fat","badge_zh":"加速燃烧","desc_ko":"캡사이신 성분이 엔도르핀을 분비시키고 체지방을 태웁니다.","desc_en":"Capsaicin triggers endorphin release and stimulates fat burning.","desc_zh":"增加发汗，提升基础代谢力，促进脂肪燃烧。","cal":40,"pro":1.9,"car":8.8,"fat":0.4,"fib":1.5,"iron":1.0,"video_url":"https://www.youtube.com/results?search_query=chili+pepper+recipe"},
        {"id":"enoki","emoji":"🍄","name_ko":"팽이버섯","name_en":"Enoki Mushroom","name_zh":"金针菇","tag_ko":"키토글루칸 내장지방","tag_en":"Enoki Fiber Det","tag_zh":"清肠刮油金针菇","badge_ko":"장청소부","badge_en":"Intestine Care","badge_zh":"清理油脂","desc_ko":"버섯 키토산이 내장지방 배출에 아주 뛰어난 가성비 식재료입니다.","desc_en":"Contains flammulin — a protein shown to inhibit tumour growth. Very low calorie.","desc_zh":"极高吸油吸水水溶性纤维，清肠减脂效果佳。","cal":22,"pro":2.7,"car":5.0,"fat":0.2,"fib":3.3,"iron":1.1,"video_url":"https://www.youtube.com/results?search_query=enoki+mushroom+recipe"},
        {"id":"paprika","emoji":"🫑","name_ko":"파프리카","name_en":"Bell Pepper","name_zh":"彩椒","tag_ko":"비타민 결정체 피부","tag_en":"Vitamin C Glow","tag_zh":"高维C美白彩椒","badge_ko":"피부미용","badge_en":"Skin Glow","badge_zh":"细腻肌肤","desc_ko":"레몬보다 2배 많은 비타민C가 들어가 기미 예방에 특효입니다.","desc_en":"Contains twice the vitamin C of a lemon — excellent for skin and immunity.","desc_zh":"颜色多样的抗氧化抗老化蔬菜，高维C美白。","cal":20,"pro":1.0,"car":4.7,"fat":0.2,"fib":2.1,"iron":0.4,"video_url":"https://www.youtube.com/results?search_query=bell+pepper+recipe"},
        {"id":"grape","emoji":"🍇","name_ko":"포도","name_en":"Grape","name_zh":"葡萄","tag_ko":"레스베라트롤 항암","tag_en":"Resveratrol Core","tag_zh":"白藜芦醇抗癌","badge_ko":"젊음유지","badge_en":"Stay Young","badge_zh":"细胞年轻","desc_ko":"껍질의 레스베라트롤 성분이 강력한 항암 및 세포 보호를 담당합니다.","desc_en":"Resveratrol in grape skin has powerful anti-cancer and anti-aging effects.","desc_zh":"花青素与白藜芦醇的自然融合体，抗老防癌。","cal":67,"pro":0.6,"car":18.1,"fat":0.4,"fib":0.9,"iron":0.3,"video_url":"https://www.youtube.com/results?search_query=grape+recipe"},
        {"id":"strawberry","emoji":"🍓","name_ko":"딸기","name_en":"Strawberry","name_zh":"草莓","tag_ko":"안토시아닌 피로회복","tag_en":"Folate Sweetness","tag_zh":"富含叶酸草莓","badge_ko":"임산부추천","badge_en":"Folate+","badge_zh":"孕期营养","desc_ko":"엽산과 비타민C가 조화롭게 녹아있어 기력 보충에 최고입니다.","desc_en":"Rich in folate and vitamin C — especially great for prenatal nutrition.","desc_zh":"清新香甜，富含叶酸，缓解疲乏。","cal":32,"pro":0.7,"car":7.7,"fat":0.3,"fib":2.0,"iron":0.4,"video_url":"https://www.youtube.com/results?search_query=strawberry+recipe"},
        {"id":"cucumber","emoji":"🥒","name_ko":"오이","name_en":"Cucumber","name_zh":"黄瓜","tag_ko":"수분보충 부종제거","tag_en":"Extreme Hydration","tag_zh":"超强补水排毒","badge_ko":"갈증해소","badge_en":"Hydrate","badge_zh":"快速清热","desc_ko":"95%가 수분으로 이뤄져 노폐물을 시원하게 배출합니다.","desc_en":"95% water content — cleanses kidneys and reduces bloating.","desc_zh":"利尿清热，非常适合夏季消暑。","cal":15,"pro":0.7,"car":3.6,"fat":0.1,"fib":0.5,"iron":0.3,"video_url":"https://www.youtube.com/results?search_query=cucumber+recipe"},
        {"id":"seaweed","emoji":"🌱","name_ko":"미역","name_en":"Miyeok (Seaweed)","name_zh":"海带","tag_ko":"요오드 조혈작용","tag_en":"Iodine Blood","tag_zh":"富含碘造血","badge_ko":"산후조리식","badge_en":"Blood Purify","badge_zh":"净化血液","desc_ko":"요오드와 칼슘이 피를 맑게 하고 상처 치유를 대폭 도와줍니다.","desc_en":"Fucoidan compound has demonstrated anti-cancer properties. Rich in iodine for thyroid.","desc_zh":"促进甲状腺健康与造血机能，海产中的佼佼者。","cal":45,"pro":3.0,"car":9.1,"fat":0.5,"fib":4.5,"iron":2.5,"video_url":"https://www.youtube.com/results?search_query=miyeok+seaweed+recipe"},
        {"id":"tuna","emoji":"🐟","name_ko":"참치","name_en":"Tuna","name_zh":"金枪鱼","tag_ko":"DHA 셀레늄 뇌활성","tag_en":"DHA Brain Power","tag_zh":"DHA健脑金枪鱼","badge_ko":"브레인푸드","badge_en":"Brain Food","badge_zh":"提高智力","desc_ko":"DHA가 풍부해 뇌 기능을 자극하고 기억력을 최고조로 높여줍니다.","desc_en":"DHA-rich protein source that boosts cognitive function and memory.","desc_zh":"提供丰富的欧米伽不饱和脂肪酸，促进脑部健康。","cal":132,"pro":28.0,"car":0.0,"fat":1.3,"fib":0.0,"iron":1.3,"video_url":"https://www.youtube.com/results?search_query=tuna+recipe"},
        {"id":"chestnut","emoji":"🌰","name_ko":"밤","name_en":"Chestnut","name_zh":"板栗","tag_ko":"탄수화물 비타민B1","tag_en":"Vitamin B1 Carb","tag_zh":"富含维B1板栗","badge_ko":"위장강화","badge_en":"Digestion Boost","badge_zh":"健脾养胃","desc_ko":"비타민B1이 풍부하여 피로 물질 축적을 효과적으로 저지합니다.","desc_en":"Unique among nuts for being low in fat and high in easily digestible carbs.","desc_zh":"传统的淀粉能量与维他命滋补品，健脾养胃。","cal":131,"pro":2.4,"car":28.0,"fat":0.5,"fib":5.0,"iron":0.9,"video_url":"https://www.youtube.com/results?search_query=chestnut+recipe"},
        {"id":"beef","emoji":"🥩","name_ko":"소고기","name_en":"Beef","name_zh":"牛肉","tag_ko":"흡수율최고 동물성철분","tag_en":"Heme Iron Muscle","tag_zh":"高效吸收血红素铁","badge_ko":"빈혈예방","badge_en":"Anti-Anemia","badge_zh":"预防贫血","desc_ko":"철분이 매우 풍부하여 빈혈을 즉각 치료하고 활력을 줍니다.","desc_en":"Heme iron absorbs 2–3x better than plant iron — essential for fighting anaemia.","desc_zh":"红肉铁质代表，补血健体，预防贫血。","cal":250,"pro":26.0,"car":0.0,"fat":15.0,"fib":0.0,"iron":2.6,"video_url":"https://www.youtube.com/results?search_query=beef+recipe"},
        {"id":"oyster","emoji":"🦪","name_ko":"굴","name_en":"Oyster","name_zh":"生蚝","tag_ko":"바다의우유 천연아연","tag_en":"Zinc Powerhouse","tag_zh":"海洋之乳天然锌","badge_ko":"스테미나","badge_en":"Stamina","badge_zh":"男性活力","desc_ko":"글리코겐과 아연이 결합하여 지친 기력을 번개처럼 회복시킵니다.","desc_en":"Highest zinc content of any food — vital for immunity, wound healing, and vitality.","desc_zh":"极高的锌含量，促进免疫和修复，补充活力。","cal":81,"pro":9.5,"car":5.0,"fat":2.3,"fib":0.0,"iron":6.7,"video_url":"https://www.youtube.com/results?search_query=oyster+recipe"},
        {"id":"lettuce","emoji":"🥬","name_ko":"상추","name_en":"Lettuce","name_zh":"生菜","tag_ko":"락투카리움 숙면유도","tag_en":"Lactucarium Sleep","tag_zh":"莴苣素助眠生菜","badge_ko":"불면증완화","badge_en":"Good Sleep","badge_zh":"安神安眠","desc_ko":"줄기 속 락투카리움 성분이 신경을 안정시켜 꿀잠을 자게 합니다.","desc_en":"Lactucarium naturally calms the nervous system and promotes sleep quality.","desc_zh":"镇静神经，有显著的安神助眠效果。","cal":15,"pro":1.4,"car":2.9,"fat":0.2,"fib":1.3,"iron":0.9,"video_url":"https://www.youtube.com/results?search_query=lettuce+recipe"},
        {"id":"kiwi","emoji":"🥝","name_ko":"키위","name_en":"Kiwi","name_zh":"猕猴桃","tag_ko":"액티니딘 소화효소","tag_en":"Actinidin Enzyme","tag_zh":"奇异果酵素促消化","badge_ko":"천연소화제","badge_en":"Proteolytic","badge_zh":"分解肉类","desc_ko":"단백질 분해 효소인 액티니딘이 육류 소화를 환상적으로 돕습니다.","desc_en":"Actinidin enzyme breaks down proteins — twice the vitamin C of an orange.","desc_zh":"含有大量可以分解肉类蛋白的酶，高维C。","cal":61,"pro":1.1,"car":14.7,"fat":0.5,"fib":3.0,"iron":0.3,"video_url":"https://www.youtube.com/results?search_query=kiwi+recipe"},
        {"id":"pear","emoji":"🍐","name_ko":"배","name_en":"Pear","name_zh":"梨","tag_ko":"루테올린 기관지보호","tag_en":"Luteolin Lungs","tag_zh":"木犀草素清肺止咳","badge_ko":"기침감기예방","badge_en":"Lung Care","badge_zh":"润肺化痰","desc_ko":"루테올린 성분이 기침과 가래를 멎게 하고 기관지를 보호합니다.","desc_en":"Luteolin soothes bronchial inflammation — a natural remedy for coughs.","desc_zh":"润肺止咳，缓解秋冬燥热，化痰止咳。","cal":57,"pro":0.4,"car":15.2,"fat":0.1,"fib":3.1,"iron":0.2,"video_url":"https://www.youtube.com/results?search_query=pear+recipe"},
        {"id":"black_bean","emoji":"🫘","name_ko":"검은콩","name_en":"Black Bean","name_zh":"黑豆","tag_ko":"이소플라본 탈모예방","tag_en":"Isoflavone Hair","tag_zh":"异黄酮防脱发","badge_ko":"모발영양","badge_en":"Hair Nutrient","badge_zh":"乌黑亮发","desc_ko":"안토시아닌과 이소플라본이 모근을 튼튼하게 강화해 줍니다.","desc_en":"Anthocyanins and isoflavones strengthen hair roots and prevent hair loss.","desc_zh":"补充黑色素与天然植物雌激素，乌发亮发。","cal":341,"pro":34.4,"car":34.9,"fat":11.1,"fib":15.2,"iron":6.5,"video_url":"https://www.youtube.com/results?search_query=black+bean+recipe"},
        {"id":"barley","emoji":"🌾","name_ko":"보리","name_en":"Barley","name_zh":"大麦","tag_ko":"베타글루칸 당뇨예방","tag_en":"Glucose Balance","tag_zh":"平稳血糖大麦","badge_ko":"당뇨개선","badge_en":"Insulin Care","badge_zh":"平稳胰岛","desc_ko":"식이섬유가 풍부하여 식후 혈당이 폭발적으로 급상승하는 것을 예방합니다.","desc_en":"Beta-glucan clinically prevents post-meal blood sugar spikes.","desc_zh":"防止餐后血糖出现过大波动，平稳胰岛素。","cal":354,"pro":12.5,"car":73.5,"fat":2.3,"fib":17.3,"iron":3.6,"video_url":"https://www.youtube.com/results?search_query=barley+recipe"},
        {"id":"sesame","emoji":"🌱","name_ko":"참깨","name_en":"Sesame","name_zh":"芝麻","tag_ko":"세사민 심혈관보호","tag_en":"Sesamin Lipids","tag_zh":"芝麻素抗氧化","badge_ko":"고소한항산화","badge_en":"Antioxidant+","badge_zh":"优质坚果油","desc_ko":"세사민 성분이 체내 나쁜 콜레스테롤 흡수를 원천 억제합니다.","desc_en":"Sesamin blocks LDL cholesterol absorption and provides antioxidant protection.","desc_zh":"富含亚油酸与天然植物抗氧化素，降低坏胆固醇。","cal":573,"pro":17.7,"car":23.4,"fat":49.7,"fib":11.8,"iron":14.6,"video_url":"https://www.youtube.com/results?search_query=sesame+recipe"},
        {"id":"minari","emoji":"🌿","name_ko":"미나리","name_en":"Water Parsley","name_zh":"水芹菜","tag_ko":"중금속배출 해독장인","tag_en":"Heavy Metal Detox","tag_zh":"重金属排毒水芹","badge_ko":"간기능개선","badge_en":"Liver Save","badge_zh":"清热解毒","desc_ko":"체내 축적된 중금속을 흡착하여 소변으로 신속히 배출시켜 줍니다.","desc_en":"Binds heavy metals and flushes them out — supports liver function.","desc_zh":"解酒保肝，清理体内有害重金属。","cal":16,"pro":1.5,"car":3.4,"fat":0.2,"fib":2.2,"iron":1.5,"video_url":"https://www.youtube.com/results?search_query=water+parsley+recipe"},
        {"id":"radish","emoji":"🫚","name_ko":"무","name_en":"Radish (Mu)","name_zh":"白萝卜","tag_ko":"디아스타아제 천연소화","tag_en":"Diastase Comfort","tag_zh":"淀粉酶顺气消食","badge_ko":"천연속편함","badge_en":"Anti-Bloat","badge_zh":"顺气大王","desc_ko":"전분 분해 효소가 풍부해 밀가루 음식을 먹고 체했을 때 명약입니다.","desc_en":"Diastase enzyme soothes indigestion — especially after eating heavy starches.","desc_zh":"解除积食，润喉化痰功效显著。","cal":16,"pro":0.8,"car":3.5,"fat":0.1,"fib":1.6,"iron":0.2,"video_url":"https://www.youtube.com/results?search_query=radish+recipe"},
        {"id":"clam","emoji":"🐚","name_ko":"조개","name_en":"Clam","name_zh":"贝类","tag_ko":"비타민B12 숙취해소","tag_en":"B12 Liver Reset","tag_zh":"维B12解酒造血","badge_ko":"간세포재생","badge_en":"Liver Care","badge_zh":"高效排毒","desc_ko":"아미노산과 비타민B12가 망가진 간세포의 빠른 재생을 유도합니다.","desc_en":"Vitamin B12 and amino acids rapidly regenerate liver cells after alcohol.","desc_zh":"富含牛磺酸，低脂且矿物质充沛，护肝解毒。","cal":74,"pro":12.8,"car":2.6,"fat":1.1,"fib":0.0,"iron":14.0,"video_url":"https://www.youtube.com/results?search_query=clam+recipe"},
    ]

def get_video_url(food, recipe_title, lang):
    """언어와 레시피 제목에 맞는 유튜브 검색 URL 생성"""
    import urllib.parse
    if lang == "한국어":
        food_name = food["name_ko"]
        query = f"{food_name} {recipe_title} 만들기 레시피"
    elif lang == "English":
        food_name = food["name_en"]
        query = f"{food_name} {recipe_title} recipe how to make"
    else:  # 중국어
        food_name = food["name_zh"]
        query = f"{food_name} {recipe_title} 食谱 做法"
    encoded = urllib.parse.quote(query)
    return f"https://www.youtube.com/results?search_query={encoded}"


def get_recipes(food_id, food_name, lang):
    """식재료별 실제 레시피 반환. 없으면 기본 세트 사용"""
    lang_key = "ko" if lang == "한국어" else "en"

    # 실제 레시피 있는 경우
    if food_id in REAL_RECIPES:
        return REAL_RECIPES[food_id][lang_key]

    # DEFAULT 세트 있는 경우
    if food_id in DEFAULT_RECIPE_SETS:
        return DEFAULT_RECIPE_SETS[food_id][lang_key]

    # 없는 경우: 식재료 이름 기반으로 실제처럼 보이는 5가지 레시피 생성
    if lang == "한국어":
        return [
            {"title":f"{food_name} 된장국","time":"15분","calories":"80 kcal","level":"쉬움",
             "steps":[f"멸치 육수를 낸다",f"된장 2큰술을 풀어준다",f"{food_name}를 먹기 좋게 썰어 넣는다","5분 끓이고 파를 올려 완성한다"],"tip":"재료를 너무 오래 끓이면 영양소가 파괴될 수 있어요"},
            {"title":f"{food_name} 볶음","time":"12분","calories":"150 kcal","level":"쉬움",
             "steps":[f"{food_name}를 먹기 좋게 손질한다","팬에 참기름을 두르고 마늘을 볶는다",f"{food_name}를 넣고 강불에서 볶는다","간장·소금으로 간하고 깨를 뿌린다"],"tip":"강불에서 빠르게 볶아야 식감이 살아요"},
            {"title":f"{food_name} 샐러드","time":"10분","calories":"120 kcal","level":"쉬움",
             "steps":[f"{food_name}를 깨끗이 씻어 준비한다","오이·방울토마토·적양파를 썬다","레몬즙·올리브오일·소금·후추로 드레싱을 만든다","모두 섞어 완성한다"],"tip":"드레싱은 먹기 직전에 뿌려야 싱싱해요"},
            {"title":f"{food_name} 비빔밥","time":"20분","calories":"380 kcal","level":"쉬움",
             "steps":[f"{food_name}를 나물로 무친다","따뜻한 밥 위에 나물을 올린다","달걀 프라이를 올린다","고추장·참기름을 넣고 비벼 먹는다"],"tip":"재료를 따뜻하게 준비해야 비빔밥이 맛있어요"},
            {"title":f"{food_name} 전","time":"15분","calories":"180 kcal","level":"쉬움",
             "steps":[f"{food_name}를 얇게 썰거나 다진다","밀가루·달걀물을 입힌다","중불에서 양면을 노릇하게 굽는다","초간장과 함께 낸다"],"tip":"팬을 충분히 달군 후 기름을 두르면 더 바삭해요"},
        ]
    else:
        return [
            {"title":f"{food_name} Doenjang Soup","time":"15 min","calories":"80 kcal","level":"Easy",
             "steps":["Make anchovy broth",f"Dissolve 2 tbsp doenjang",f"Add sliced {food_name} and simmer 5 min","Garnish with scallions and serve hot"],"tip":"Don't overcook — add ingredients near the end to preserve nutrients"},
            {"title":f"Stir-Fried {food_name}","time":"12 min","calories":"150 kcal","level":"Easy",
             "steps":[f"Prepare {food_name} into bite-sized pieces","Heat sesame oil and sauté garlic","Add {food_name} and stir-fry over high heat","Season with soy sauce and finish with sesame seeds"],"tip":"High heat and quick cooking preserves texture and flavour"},
            {"title":f"{food_name} Salad","time":"10 min","calories":"120 kcal","level":"Easy",
             "steps":[f"Wash and prepare {food_name}","Slice cucumber, cherry tomatoes, red onion","Make dressing: lemon juice, olive oil, salt, pepper","Toss everything together and serve"],"tip":"Add dressing just before serving to keep everything fresh"},
            {"title":f"{food_name} Bibimbap","time":"20 min","calories":"380 kcal","level":"Easy",
             "steps":[f"Season {food_name} as namul","Place over warm steamed rice","Top with a fried egg","Add gochujang and sesame oil; mix well to eat"],"tip":"Keep all ingredients warm before assembling for best flavour"},
            {"title":f"{food_name} Jeon (Pancake)","time":"15 min","calories":"180 kcal","level":"Easy",
             "steps":[f"Thinly slice or finely chop {food_name}","Coat in flour then egg wash","Pan-fry both sides until golden over medium heat","Serve hot with soy vinegar dipping sauce"],"tip":"Heat the pan well before adding oil for a crispy result"},
        ]

# ── 세션 상태 ──────────────────────────────────────────────────────
all_foods = load_all_foods()
food_options_map = {f"{f['emoji']} {f['name_ko']} ({f['name_en']})": f["id"] for f in all_foods}

if "selected_food_id" not in st.session_state:
    st.session_state.selected_food_id = "quinoa"
if "my_fridge" not in st.session_state:
    st.session_state.my_fridge = []

# ── 사이드바 ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("🌿 Nourish Hub")
    selected_lang = st.selectbox("🌐 Language / 语言", ["한국어", "English", "중국어 (简体中文)"])
    text_pack = UI_TEXTS[selected_lang]
    st.write("---")
    st.markdown(f"### {text_pack['academic']}")
    st.text("Course: Arts and Big Data")
    st.text("Student: 신아영 (Shin Ahyoung)")
    st.text("Major: 무용학과 (Dance)")
    st.text("University: Sungkyunkwan University (SKKU)")
    st.write("---")
    st.markdown(f"### {text_pack['saved_title']}")
    if st.session_state.my_fridge:
        for fav in st.session_state.my_fridge:
            st.write(f"✅ {fav}")
    else:
        st.caption(text_pack['saved_empty'])

# ── 메인 타이틀 ───────────────────────────────────────────────────
st.markdown(f"<p class='brand-sub'>{text_pack['sub_logo']}</p>", unsafe_allow_html=True)
st.markdown(f"<h1 class='brand-main'>{text_pack['title_main']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='brand-desc'>{text_pack['subtitle']}</p>", unsafe_allow_html=True)

# 드롭다운
default_idx = next((i for i, f in enumerate(all_foods) if f["id"] == st.session_state.selected_food_id), 0)
selected_option = st.selectbox(text_pack["selector_label"], list(food_options_map.keys()), index=default_idx)
st.session_state.selected_food_id = food_options_map[selected_option]

tab1, tab2 = st.tabs([text_pack["tab1"], text_pack["tab2"]])

# ── TAB 1: 식재료 탐색 ──────────────────────────────────────────────
with tab1:
    st.markdown(f"### 🥦 {text_pack['intro_recom']}")
    col_cards = st.columns(4)
    for idx, item in enumerate(all_foods[:4]):
        with col_cards[idx]:
            if selected_lang == "한국어":
                d_name, d_tag, d_badge = item["name_ko"], item["tag_ko"], item["badge_ko"]
            elif selected_lang == "English":
                d_name, d_tag, d_badge = item["name_en"], item["tag_en"], item["badge_en"]
            else:
                d_name, d_tag, d_badge = item["name_zh"], item["tag_zh"], item["badge_zh"]
            st.markdown(f"""
                <div class="food-card">
                    <div class="food-emoji">{item['emoji']}</div>
                    <div class="food-name">{d_name}</div>
                    <div class="food-tagline">{d_tag}</div>
                    <span class="food-badge">{d_badge}</span>
                </div>
            """, unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                if st.button(text_pack["select_btn"], key=f"t1_sel_{item['id']}", use_container_width=True):
                    st.session_state.selected_food_id = item["id"]; st.rerun()
            with b2:
                if st.button(text_pack["info_btn"], key=f"t1_inf_{item['id']}", use_container_width=True):
                    st.session_state.selected_food_id = item["id"]; st.rerun()

    active_food = next(x for x in all_foods if x["id"] == st.session_state.selected_food_id)
    st.write("---")
    col_info, col_chart = st.columns([1, 1])

    with col_info:
        if selected_lang == "한국어":
            disp_title, disp_desc = active_food["name_ko"], active_food["desc_ko"]
        elif selected_lang == "English":
            disp_title, disp_desc = active_food["name_en"], active_food["desc_en"]
        else:
            disp_title, disp_desc = active_food["name_zh"], active_food["desc_zh"]
        st.markdown(f"""
            <div class="cute-card">
                <div class="card-title">✨ {active_food['emoji']} {disp_title} {text_pack['doc_title']}</div>
                <p style='font-size:15px;line-height:1.7;color:#333333;'>{disp_desc}</p>
                <hr style='border:0;border-top:1px solid #EEF0EC;margin:20px 0;'>
                <div class="card-title" style='font-size:16px;'>{text_pack['nut_info']}</div>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px;'>
                    <div class="nut-grid-item">🔥 {text_pack['labels'][0]}: {active_food['cal']} kcal</div>
                    <div class="nut-grid-item">💪 {text_pack['labels'][1]}: {active_food['pro']} g</div>
                    <div class="nut-grid-item">🌾 {text_pack['labels'][2]}: {active_food['car']} g</div>
                    <div class="nut-grid-item">🥑 {text_pack['labels'][3]}: {active_food['fat']} g</div>
                    <div class="nut-grid-item">🥦 {text_pack['labels'][4]}: {active_food['fib']} g</div>
                    <div class="nut-grid-item">🩸 {text_pack['labels'][5]}: {active_food['iron']} mg</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_chart:
        nut_keys = ["pro", "fib", "cal", "fat", "car", "iron"]
        max_vals = {"pro": 35, "fib": 20, "cal": 700, "fat": 70, "car": 80, "iron": 15}
        r_vals = [min((active_food[n] / max_vals[n]) * 100, 100) for n in nut_keys]
        fig_radar = go.Figure()  # ✅ 수정: px → go
        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals + [r_vals[0]],
            theta=text_pack["nutrients"] + [text_pack["nutrients"][0]],
            fill='toself', line_color='#3B6D11', fillcolor='rgba(59,109,17,0.15)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#ECEEEB")),
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=30, l=40, r=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ── TAB 2: 레시피 ──────────────────────────────────────────────────
with tab2:
    active_food = next(x for x in all_foods if x["id"] == st.session_state.selected_food_id)
    if selected_lang == "한국어":
        recipe_target_name = active_food["name_ko"]
    elif selected_lang == "English":
        recipe_target_name = active_food["name_en"]
    else:
        recipe_target_name = active_food["name_zh"]

    st.markdown(f"### 🍳 {active_food['emoji']} {recipe_target_name} · {text_pack['recipe_room']}")

    recipes_list = get_recipes(active_food["id"], recipe_target_name, selected_lang)

    for idx, rc in enumerate(recipes_list):
        steps_html = "".join([
            f'<div class="step-item"><div class="step-number">{i+1}</div><div class="step-text">{step}</div></div>'
            for i, step in enumerate(rc['steps'])
        ])
        st.markdown(f"""
            <div class="cute-card">
                <div class="card-title" style='font-size:20px;color:#2C3A1E;margin-bottom:12px;'>{rc['title']}</div>
                <div class="badge-container">
                    <span class="badge badge-time">⏱️ {rc['time']}</span>
                    <span class="badge badge-cal">🔥 {rc['calories']}</span>
                    <span class="badge badge-ing">🌿 {recipe_target_name}</span>
                    <span class="badge badge-level">● {rc['level']}</span>
                </div>
                <hr style='border:0;border-top:1px solid #F0F2EE;margin:15px 0;'>
                {steps_html}
                <div class="tip-box">💡 <b>Nourish Secret Tip:</b> {rc['tip']}</div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 4])
        with c1:
            if rc['title'] in st.session_state.my_fridge:
                if st.button(text_pack['btn_del'], key=f"del_{idx}_{active_food['id']}", use_container_width=True):
                    st.session_state.my_fridge.remove(rc['title']); st.rerun()
            else:
                if st.button(text_pack['btn_add'], key=f"add_{idx}_{active_food['id']}", use_container_width=True):
                    st.session_state.my_fridge.append(rc['title']); st.rerun()
        with c2:
            video_url = get_video_url(active_food, rc['title'], selected_lang)
            st.link_button(text_pack['btn_video'], video_url, use_container_width=False)
