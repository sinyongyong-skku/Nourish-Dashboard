import streamlit as st
import pandas as pd
import plotly.graph_objects as px

# 1. 페이지 설정 및 브랜딩 테마 선언
st.set_page_config(
    page_title="Nourish · Ingredient & Recipe Hub",
    page_icon="🌿",
    layout="wide"
)

# UI 디자인 및 카드 격자, 가독성 확보를 위한 CSS 커스텀
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Noto+Sans+KR:wght=300;400;700&display=swap');
    
    .main { background-color: #FBFBFA; }
    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
        color: #2C3A1E;
    }
    
    .brand-sub {
        font-family: 'DM Serif Display', serif;
        color: #3B6D11;
        font-size: 14px;
        letter-spacing: 2px;
        font-weight: bold;
        margin-bottom: -10px;
    }
    .brand-main {
        font-size: 42px;
        font-weight: 700;
        color: #2C3A1E;
        line-height: 1.3;
        margin-bottom: 5px;
    }
    .brand-desc {
        color: #6E7A64;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* 추천 식재료 가로 카드 그리드 레이아웃 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 15px;
        margin-bottom: 25px;
    }
    .food-card {
        background-color: white;
        border-radius: 16px;
        border: 1px solid #EAECE8;
        box-shadow: 0px 4px 20px rgba(44, 58, 30, 0.03);
        text-align: center;
        padding: 20px 12px;
    }
    .food-emoji { font-size: 40px; margin-bottom: 8px; }
    .food-name { font-size: 18px; font-weight: 700; color: #2C3A1E; margin-bottom: 4px; }
    .food-tagline { font-size: 12px; color: #8C9A82; margin-bottom: 10px; }
    .food-badge {
        background-color: #F4F6F2;
        color: #556B2F;
        padding: 3px 10px;
        border-radius: 50px;
        font-size: 11px;
        font-weight: bold;
    }

    /* 디자인 카드 */
    .cute-card {
        background-color: white;
        padding: 26px;
        border-radius: 16px;
        border: 1px solid #EAECE8;
        box-shadow: 0px 4px 20px rgba(44, 58, 30, 0.04);
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 20px;
        font-weight: 700;
        color: #2C3A1E;
        margin-bottom: 12px;
    }

    .nut-grid-item {
        background-color: #F6F8F5 !important; 
        padding: 15px; 
        border-radius: 10px;
        color: #2C3A1E !important;
        font-size: 14px;
        font-weight: bold;
        border: 1px solid #EEF1EC;
    }

    .badge-container {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 15px;
    }
    .badge {
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 700;
    }
    .badge-time { background-color: #EAF3DE; color: #3B6D11; }
    .badge-cal { background-color: #FDF0EA; color: #E67E22; }
    .badge-ing { background-color: #F4F6F2; color: #556B2F; }
    .badge-level { background-color: #EEF2F7; color: #2E64FE; }

    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        padding: 10px 0;
    }
    .step-number {
        background-color: #3B6D11;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
        flex-shrink: 0;
    }
    .step-text { font-size: 15px; color: #333333; line-height: 1.5; }
    
    .tip-box {
        background-color: #FAFAFA;
        border-left: 4px solid #3B6D11;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        font-size: 14px;
        color: #555;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 다국어 사전 설정
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
        "labels": ["热量", "蛋白质", "碳水化合物", "脂肪", "膳食纤维", "铁"],
        "nutrients": ["蛋白质 (g)", "膳食纤维 (g)", "卡路里 (kcal)", "脂肪 (g)", "碳水化合物 (g)", "铁分 (mg)"]
    }
}

# 3. ⭐️ 50대 식재료 풀 데이터셋 (누락 없이 완벽 장착) ⭐️
@st.cache_data
def load_all_foods():
    return [
        # 1-10
        {"id": "quinoa", "emoji": "🌾", "name_ko": "퀴노아", "name_en": "Quinoa", "name_zh": "藜麦", "tag_ko": "완전단백질 슈퍼씨앗", "tag_en": "Complete Plant Protein", "tag_zh": "全蛋白超级种子", "badge_ko": "글루텐프리", "badge_en": "Gluten-Free", "badge_zh": "无麸质", "desc_ko": "필수 아미노산이 균형 있게 함유된 슈퍼 곡물입니다.", "desc_en": "Rich in essential amino acids.", "desc_zh": "包含人体必需氨基酸。", "cal": 368, "pro": 14.1, "car": 64.0, "fat": 6.1, "fib": 7.0, "iron": 4.6, "video_url": "https://www.youtube.com/results?search_query=퀴노아+레시피"},
        {"id": "avocado", "emoji": "🥑", "name_ko": "아보카도", "name_en": "Avocado", "name_zh": "牛油果", "tag_ko": "단일불포화지방산", "tag_en": "Healthy Fats", "tag_zh": "单不饱和脂肪", "badge_ko": "비타민E", "badge_en": "Vitamin E", "badge_zh": "富含维E", "desc_ko": "불포화 지방산이 풍부해 심혈관 건강에 훌륭합니다.", "desc_en": "Great for heart health with clean lipids.", "desc_zh": "含有对人体有益的健康油脂。", "cal": 160, "pro": 2.0, "car": 8.5, "fat": 14.7, "fib": 6.7, "iron": 0.6, "video_url": "https://www.youtube.com/results?search_query=아보카도+레시피"},
        {"id": "tofu", "emoji": "🫘", "name_ko": "두부", "name_en": "Tofu", "name_zh": "豆腐", "tag_ko": "식물성 완전단백질", "tag_en": "Soy Curd Core", "tag_zh": "植物性优质全蛋白", "badge_ko": "저칼로리", "badge_en": "Low-Calorie", "badge_zh": "低热量", "desc_ko": "콩 단백질을 압착하여 만든 고단백 건강 재료입니다.", "desc_en": "High digestibility plant-based source.", "desc_zh": "高消化率植物高蛋白食材。", "cal": 84, "pro": 8.9, "car": 2.9, "fat": 4.8, "fib": 0.2, "iron": 1.5, "video_url": "https://www.youtube.com/results?search_query=두부+레시피"},
        {"id": "blueberry", "emoji": "🫐", "name_ko": "블루베리", "name_en": "Blueberry", "name_zh": "蓝莓", "tag_ko": "안토시아닌 항산화", "tag_en": "Antioxidant Power", "tag_zh": "强效抗氧化", "badge_ko": "비타민C", "badge_en": "Vitamin C+", "badge_zh": "富含维C", "desc_ko": "안토시아닌이 활성산소를 억제하고 눈을 보호합니다.", "desc_en": "Fights free radicals beautifully.", "desc_zh": "富含花青素，清除自由基效果佳。", "cal": 57, "pro": 0.7, "car": 14.5, "fat": 0.3, "fib": 2.4, "iron": 0.3, "video_url": "https://www.youtube.com/results?search_query=블루베리+레시피"},
        {"id": "kelp", "emoji": "🌊", "name_ko": "다시마", "name_en": "Kelp", "name_zh": "昆布", "tag_ko": "해조류 식이섬유 왕", "tag_en": "Iodine & Fibre King", "tag_zh": "海藻膳食纤维王", "badge_ko": "알긴산 풍부", "badge_en": "Alginic Acid", "badge_zh": "富含褐藻酸", "desc_ko": "다시마는 풍부한 알긴산과 장 건강에 좋은 식이섬유의 보고입니다.", "desc_en": "Seafood powerhouse full of trace minerals.", "desc_zh": "富含微量元素与大量水溶性膳食纤维。", "cal": 43, "pro": 1.7, "car": 9.6, "fat": 0.6, "fib": 1.3, "iron": 2.8, "video_url": "https://www.youtube.com/results?search_query=다시마+레시피"},
        {"id": "salmon", "emoji": "🐟", "name_ko": "연어", "name_en": "Salmon", "name_zh": "三文鱼", "tag_ko": "오메가-3의 대명사", "tag_en": "Omega-3 Rich Fish", "tag_zh": "富含欧米伽-3", "badge_ko": "고단백질", "badge_en": "High Protein", "badge_zh": "高蛋白质", "desc_ko": "연어는 혈관 건강을 지켜주는 오메가-3 지방산이 매우 풍부합니다.", "desc_en": "Excellent source of premium omega-3 fatty acids.", "desc_zh": "富含深海不饱和脂肪酸。", "cal": 208, "pro": 20.0, "car": 0.0, "fat": 13.0, "fib": 0.0, "iron": 0.3, "video_url": "https://www.youtube.com/results?search_query=연어+레시피"},
        {"id": "spinach", "emoji": "🥬", "name_ko": "시금치", "name_en": "Spinach", "name_zh": "菠菜", "tag_ko": "철분 가득 녹색채소", "tag_en": "Iron-Rich Green", "tag_zh": "富含铁质绿叶菜", "badge_ko": "엽산 풍부", "badge_en": "Folic Acid", "badge_zh": "富含叶酸", "desc_ko": "시금치는 유기산과 철분, 비타민이 고루 배합된 채소입니다.", "desc_en": "Dense in vitamin K, iron, and green antioxidants.", "desc_zh": "富含叶酸与无机盐。", "cal": 23, "pro": 2.9, "car": 3.6, "fat": 0.4, "fib": 2.2, "iron": 2.7, "video_url": "https://www.youtube.com/results?search_query=시금치+레시피"},
        {"id": "garlic", "emoji": "🧄", "name_ko": "마늘", "name_en": "Garlic", "name_zh": "大蒜", "tag_ko": "천연 면역 강화제", "tag_en": "Natural Immunity", "tag_zh": "天然免疫增强剂", "badge_ko": "알리신 함유", "badge_en": "Allicin Power", "badge_zh": "富含蒜素", "desc_ko": "알리신 성분이 강력한 항균 작용과 면역을 촉진합니다.", "desc_en": "Contains allicin, known for robust defense attributes.", "desc_zh": "大蒜素具有极强的抗菌功效。", "cal": 149, "pro": 6.4, "car": 33.1, "fat": 0.5, "fib": 2.1, "iron": 1.7, "video_url": "https://www.youtube.com/results?search_query=마늘+레시피"},
        {"id": "walnut", "emoji": "🥜", "name_ko": "호두", "name_en": "Walnut", "name_zh": "核桃", "tag_ko": "두뇌 활성화 견과", "tag_en": "Brain Superfood", "tag_zh": "健脑益智坚果", "badge_ko": "불포화지방", "badge_en": "Healthy Lipids", "badge_zh": "优质脂肪", "desc_ko": "뇌 세포를 보호하고 인지 능력을 개선하는 견과류입니다.", "desc_en": "Resembles the brain and brilliantly nourishes it.", "desc_zh": "富含不饱和脂肪酸与亚麻酸。", "cal": 654, "pro": 15.2, "car": 13.7, "fat": 65.2, "fib": 6.7, "iron": 2.9, "video_url": "https://www.youtube.com/results?search_query=호두+레시피"},
        {"id": "mushroom", "emoji": "🍄", "name_ko": "표고버섯", "name_en": "Shiitake", "name_zh": "香菇", "tag_ko": "면역 베타글루칸", "tag_en": "Beta-Glucan Core", "tag_zh": "富含β-聚糖", "badge_ko": "비타민D", "badge_en": "Vitamin D", "badge_zh": "富含维D", "desc_ko": "베타글루칸 성분이 가득하여 면역 조절에 탁월합니다.", "desc_en": "Rich umami texture boosting cellular shields.", "desc_zh": "独特的鲜味成分，具有极高的免疫调节。", "cal": 34, "pro": 2.2, "car": 6.8, "fat": 0.5, "fib": 2.5, "iron": 0.4, "video_url": "https://www.youtube.com/results?search_query=표고버섯+레시피"},
        
        # 11-20
        {"id": "sweet_potato", "emoji": "🍠", "name_ko": "고구마", "name_en": "Sweet Potato", "name_zh": "红薯", "tag_ko": "베타카로틴 식이섬유", "tag_en": "Beta-Carotene Energy", "tag_zh": "富含β-胡萝卜素", "badge_ko": "낮은GI", "badge_en": "Low GI", "badge_zh": "低GI", "desc_ko": "식이섬유가 풍부해 소화가 잘되고 장 건강에 좋습니다.", "desc_en": "High fiber carbohydrate option.", "desc_zh": "富含复杂的碳水化合物与维生素A。", "cal": 86, "pro": 1.6, "car": 20.1, "fat": 0.1, "fib": 3.0, "iron": 0.6, "video_url": "https://www.youtube.com/results?search_query=고구마+레시피"},
        {"id": "tomato", "emoji": "🍅", "name_ko": "토마토", "name_en": "Tomato", "name_zh": "西红柿", "tag_ko": "라이코펜 항산화", "tag_en": "Lycopene Shield", "tag_zh": "番茄红素抗氧化", "badge_ko": "심혈관케어", "badge_en": "Heart Care", "badge_zh": "益于心血管", "desc_ko": "라이코펜이 풍부하여 세포 노화를 방지하고 혈압을 낮춥니다.", "desc_en": "Superb antioxidant profile when cooked.", "desc_zh": "熟吃更能释放番茄红素成分。", "cal": 18, "pro": 0.9, "car": 3.9, "fat": 0.2, "fib": 1.2, "iron": 0.3, "video_url": "https://www.youtube.com/results?search_query=토마토+레시피"},
        {"id": "broccoli", "emoji": "🥦", "name_ko": "브로콜리", "name_en": "Broccoli", "name_zh": "西兰花", "tag_ko": "설포라판 비타민C", "tag_en": "Sulforaphane Green", "tag_zh": "富含萝卜硫素", "badge_ko": "해독작용", "badge_en": "Detox", "badge_zh": "自然排毒", "desc_ko": "설포라판 성분이 위장 건강과 해독 작용을 돕습니다.", "desc_en": "Excellent source of vitamin C and cruciferous nutrients.", "desc_zh": "十字花科蔬菜，富含微量元素。", "cal": 34, "pro": 2.8, "car": 7.0, "fat": 0.4, "fib": 2.6, "iron": 0.7, "video_url": "https://www.youtube.com/results?search_query=브로콜리+레시피"},
        {"id": "oatmeal", "emoji": "🥣", "name_ko": "오트밀", "name_en": "Oats", "name_zh": "燕麦", "tag_ko": "베타글루칸 콜레스테롤", "tag_en": "Beta-Glucan Heart", "tag_zh": "降胆固醇燕麦", "badge_ko": "식이섬유깡패", "badge_en": "High Fiber", "badge_zh": "高膳食纤维", "desc_ko": "수용성 식이섬유가 풍부해 콜레스테롤 수치를 대폭 낮춥니다.", "desc_en": "Stabilizes blood sugar and keeps you full.", "desc_zh": "饱腹感强，利于血糖管理。", "cal": 389, "pro": 16.9, "car": 66.3, "fat": 6.9, "fib": 10.6, "iron": 4.7, "video_url": "https://www.youtube.com/results?search_query=오트밀+레시피"},
        {"id": "green_tea", "emoji": "🍵", "name_ko": "녹차", "name_en": "Green Tea", "name_zh": "绿茶", "tag_ko": "카테킨 신진대사", "tag_en": "Catechin Metabolism", "tag_zh": "儿茶素代谢", "badge_ko": "체지방감소", "badge_en": "Fat Burn", "badge_zh": "减少脂肪", "desc_ko": "카테킨 성분이 지방 연소를 돕고 체내 염증을 억제합니다.", "desc_en": "Loaded with polyphenols and clean energy.", "desc_zh": "抗氧化效果佳，清新提神。", "cal": 1, "pro": 0.2, "car": 0.0, "fat": 0.0, "fib": 0.0, "iron": 0.0, "video_url": "https://www.youtube.com/results?search_query=녹차+레시피"},
        {"id": "egg", "emoji": "🥚", "name_ko": "계란", "name_en": "Egg", "name_zh": "鸡蛋", "tag_ko": "완전무결 단백질", "tag_en": "Perfect Bio-Protein", "tag_zh": "完美优质蛋白", "badge_ko": "콜린 가득", "badge_en": "Choline Source", "badge_zh": "富含胆碱", "desc_ko": "기억력 향상에 도움을 주는 콜린과 양질의 단백질 덩어리입니다.", "desc_en": "Affordable and bioavailable source of essential macros.", "desc_zh": "提供最均衡的必须氨基酸。", "cal": 155, "pro": 12.6, "car": 1.1, "fat": 10.6, "fib": 0.0, "iron": 1.2, "video_url": "https://www.youtube.com/results?search_query=계란+레시피"},
        {"id": "chicken_breast", "emoji": "🍗", "name_ko": "닭가슴살", "name_en": "Chicken Breast", "name_zh": "鸡胸肉", "tag_ko": "근육 생성의 기초", "tag_en": "Pure Lean Muscle", "tag_zh": "纯净增肌大王", "badge_ko": "초저지방", "badge_en": "Ultra Lean", "badge_zh": "超低脂肪", "desc_ko": "지방 함량이 거의 없고 단백질 비율이 극도로 높은 다이어트 식재료입니다.", "desc_en": "The staple of structural body framing.", "desc_zh": "高蛋白低脂肪，减脂控形必备。", "cal": 165, "pro": 31.0, "car": 0.0, "fat": 3.6, "fib": 0.0, "iron": 1.0, "video_url": "https://www.youtube.com/results?search_query=닭가슴살+레시피"},
        {"id": "banana", "emoji": "🍌", "name_ko": "바나나", "name_en": "Banana", "name_zh": "香蕉", "tag_ko": "칼륨 운동에너지", "tag_en": "Potassium Boost", "tag_zh": "高钾运动机能", "badge_ko": "피로회복", "badge_en": "Energy Source", "badge_zh": "恢复疲劳", "desc_ko": "칼륨이 풍부해 나트륨 배출을 돕고 운동 전 에너지 보충에 좋습니다.", "desc_en": "Quick natural sugar breakdown for fast vitality.", "desc_zh": "极佳的能量补充水果。", "cal": 89, "pro": 1.1, "car": 22.8, "fat": 0.3, "fib": 2.6, "iron": 0.3, "video_url": "https://www.youtube.com/results?search_query=바나나+레시피"},
        {"id": "apple", "emoji": "🍎", "name_ko": "사과", "name_en": "Apple", "name_zh": "苹果", "tag_ko": "펙틴 아침의 사과", "tag_en": "Pectin Digestion", "tag_zh": "果胶清肠胃", "badge_ko": "장운동원활", "badge_en": "Gut Health", "badge_zh": "肠道健康", "desc_ko": "펙틴 성분이 장내 유익균을 증식시키고 배변 활동을 활발하게 유도합니다.", "desc_en": "Keeps the doctor away with clean soluble fibers.", "desc_zh": "富含维生素C与水溶性果胶。", "cal": 52, "pro": 0.3, "car": 13.8, "fat": 0.2, "fib": 2.4, "iron": 0.1, "video_url": "https://www.youtube.com/results?search_query=사과+레시피"},
        {"id": "carrot", "emoji": "🥕", "name_ko": "당근", "name_en": "Carrot", "name_zh": "胡萝卜", "tag_ko": "비타민A 야맹증예방", "tag_en": "Vision Vitamin A", "tag_zh": "明目维A之王", "badge_ko": "시력보호", "badge_en": "Eye Health", "badge_zh": "保护视力", "desc_ko": "체내에서 비타민A로 전환되는 베타카로틴이 채소 중 가장 많습니다.", "desc_en": "Improves visual acuity and membrane synthesis.", "desc_zh": "富含类胡萝卜素，对抗自由基。", "cal": 41, "pro": 0.9, "car": 9.6, "fat": 0.2, "fib": 2.8, "iron": 0.3, "video_url": "https://www.youtube.com/results?search_query=당근+레시피"},
        
        # 21-30
        {"id": "onion", "emoji": "🧅", "name_ko": "양파", "name_en": "Onion", "name_zh": "洋葱", "tag_ko": "퀘르세틴 혈액순환", "tag_en": "Quercetin Blood Flow", "tag_zh": "槲皮素降血脂", "badge_ko": "혈관정화", "badge_en": "Vessel Clean", "badge_zh": "清理血管", "desc_ko": "퀘르세틴 성분이 혈전 형성을 방지하고 피를 맑게 해줍니다.", "desc_en": "Cleans arteries and provides deep flavor bases.", "desc_zh": "强效抗氧化，软化心血管。", "cal": 40, "pro": 1.1, "car": 9.3, "fat": 0.1, "fib": 1.7, "iron": 0.2, "video_url": "https://www.youtube.com/results?search_query=양파+레시피"},
        {"id": "ginger", "emoji": "🫚", "name_ko": "생강", "name_en": "Ginger", "name_zh": "生姜", "tag_ko": "진저롤 체온상승", "tag_en": "Gingerol Warmth", "tag_zh": "姜辣素驱寒", "badge_ko": "항염효과", "badge_en": "Anti-Inflam", "badge_zh": "温中抗炎", "desc_ko": "진저롤이 체온을 높여 면역력을 증진하고 혈액 순환을 개선합니다.", "desc_en": "Calms gut issues and destroys systemic heat loss.", "desc_zh": "暖胃散寒，促进新陈代谢。", "cal": 80, "pro": 1.8, "car": 17.8, "fat": 0.8, "fib": 2.0, "iron": 0.6, "video_url": "https://www.youtube.com/results?search_query=생강+레시피"},
        {"id": "honey", "emoji": "🍯", "name_ko": "꿀", "name_en": "Honey", "name_zh": "蜂蜜", "tag_ko": "천연에너지 피로회복", "tag_en": "Pure Glycogen", "tag_zh": "天然滋补能量", "badge_ko": "기력보충", "badge_en": "Vitality", "badge_zh": "快速补充", "desc_ko": "체내에 즉각 흡수되는 천연 단당류로 피로회복에 직효입니다.", "desc_en": "Natural antibacterial enzyme profile sweetener.", "desc_zh": "含有多种微量活性酶 with 矿物质。", "cal": 304, "pro": 0.3, "car": 82.4, "fat": 0.0, "fib": 0.0, "iron": 0.4, "video_url": "https://www.youtube.com/results?search_query=꿀+레시피"},
        {"id": "lemon", "emoji": "🍋", "name_ko": "레몬", "name_en": "Lemon", "name_zh": "柠檬", "tag_ko": "구연산 피로물질제거", "tag_en": "Citric Detox", "tag_zh": "柠檬酸排毒", "badge_ko": "비타민C폭탄", "badge_en": "Vitamin C", "badge_zh": "高维C", "desc_ko": "구연산이 가득해 젖산을 분해하고 몸을 약알칼리성으로 가꿔줍니다.", "desc_en": "Alkalizes the internal pH environment beautifully.", "desc_zh": "美白抗氧化，增强血管弹性。", "cal": 29, "pro": 1.1, "car": 9.3, "fat": 0.3, "fib": 2.8, "iron": 0.6, "video_url": "https://www.youtube.com/results?search_query=레몬+레시피"},
        {"id": "cabbage", "emoji": "🥬", "name_ko": "양배추", "name_en": "Cabbage", "name_zh": "卷心菜", "tag_ko": "비타민U 위벽보호", "tag_en": "Vitamin U Gut", "tag_zh": "维U保护胃黏膜", "badge_ko": "위건강케어", "badge_en": "Stomach Care", "badge_zh": "养胃圣品", "desc_ko": "비타민U 성분이 상처 난 위 점막의 재생을 강력하게 도와줍니다.", "desc_en": "Raw juices shield gastrointestinal tracks.", "desc_zh": "富含维生素U及粗纤维。", "cal": 25, "pro": 1.3, "car": 5.8, "fat": 0.1, "fib": 2.5, "iron": 0.5, "video_url": "https://www.youtube.com/results?search_query=양배추+레시피"},
        {"id": "potato", "emoji": "🥔", "name_ko": "감자", "name_en": "Potato", "name_zh": "土豆", "tag_ko": "전분보호 비타민C", "tag_en": "Stable Vit C", "tag_zh": "抗热维生素C", "badge_ko": "위염완화", "badge_en": "Stomach Clean", "badge_zh": "调理脾胃", "desc_ko": "익혀도 파괴되지 않는 비타민C와 풍부한 칼륨이 특징입니다.", "desc_en": "Potassium heavy root starches supporting muscles.", "desc_zh": "不易随加热流失的维生素C资源。", "cal": 77, "pro": 2.0, "car": 17.5, "fat": 0.1, "fib": 2.2, "iron": 0.8, "video_url": "https://www.youtube.com/results?search_query=감자+레시피"},
        {"id": "pumpkin", "emoji": "🎃", "name_ko": "단호박", "name_en": "Pumpkin", "name_zh": "南瓜", "tag_ko": "붓기제거 이뇨작용", "tag_en": "Anti-Swelling", "tag_zh": "利尿消肿神物", "badge_ko": "다이어트식", "badge_en": "Slim Diet", "badge_zh": "低卡轻盈", "desc_ko": "이뇨작용을 촉진해 몸의 붓기를 빼주고 칼로리가 무척 낮습니다.", "desc_en": "Beta-carotene dense squash perfect for cold days.", "desc_zh": "维生素A和碳水结合的高饱腹感食材。", "cal": 26, "pro": 1.0, "car": 6.5, "fat": 0.1, "fib": 0.5, "iron": 0.8, "video_url": "https://www.youtube.com/results?search_query=단호박+레시피"},
        {"id": "milk", "emoji": "🥛", "name_ko": "우유", "name_en": "Milk", "name_zh": "牛奶", "tag_ko": "칼슘의 왕 골다공증", "tag_en": "Calcium Source", "tag_zh": "补钙黄金资源", "badge_ko": "뼈건강", "badge_en": "Bone Health", "badge_zh": "坚固骨骼", "desc_ko": "흡수율이 매우 높은 천연 칼슘이 들어있어 골밀도를 강화합니다.", "desc_en": "Classic drink for physical architecture maintenance.", "desc_zh": "最直观容易吸收的乳钙来源。", "cal": 42, "pro": 3.4, "car": 5.0, "fat": 1.0, "fib": 0.0, "iron": 0.1, "video_url": "https://www.youtube.com/results?search_query=우유+레시피"},
        {"id": "almond", "emoji": "🫘", "name_ko": "아몬드", "name_en": "Almond", "name_zh": "杏仁", "tag_ko": "불포화지방 비타민E", "tag_en": "Lipid Vitamin E", "tag_zh": "富含强抗氧化维E", "badge_ko": "항노화방지", "badge_en": "Anti-Aging", "badge_zh": "延缓衰老", "desc_ko": "강력한 항산화제인 비타민E가 노화를 막고 피부를 가꿔줍니다.", "desc_en": "Snack on premium fats for hormonal clarity.", "desc_zh": "含有优质不饱和油和膳食纤维。", "cal": 579, "pro": 21.2, "car": 21.7, "fat": 49.9, "fib": 12.5, "iron": 3.7, "video_url": "https://www.youtube.com/results?search_query=아몬드+레시피"},
        {"id": "shrimp", "emoji": "🦐", "name_ko": "새우", "name_en": "Shrimp", "name_zh": "大虾", "tag_ko": "키토산 타우린 피로", "tag_en": "Taurine Marine", "tag_zh": "富含牛磺酸", "badge_ko": "피로타파", "badge_en": "Energy Recover", "badge_zh": "恢复活力", "desc_ko": "타우린이 가득해 간 해독을 돕고 혈중 콜레스테롤을 낮춰줍니다.", "desc_en": "Low calorie marine protein bursting with nutrients.", "desc_zh": "极低卡的高级海鲜蛋白质。", "cal": 85, "pro": 20.1, "car": 0.2, "fat": 0.5, "fib": 0.0, "iron": 0.5, "video_url": "https://www.youtube.com/results?search_query=새우+레시피"},

        # 31-40
        {"id": "chili", "emoji": "🌶️", "name_ko": "고추", "name_en": "Chili", "name_zh": "辣椒", "tag_ko": "캡사이신 기초대사량", "tag_en": "Capsaicin Fire", "tag_zh": "辣椒素新陈代谢", "badge_ko": "지방연소", "badge_en": "Burn Fat", "badge_zh": "加速燃烧", "desc_ko": "캡사이신 성분이 엔도르핀을 분비시키고 체지방을 태웁니다.", "desc_en": "Sparks fat breakdown processes via heat simulation.", "desc_zh": "增加发汗，提升基础代谢力。", "cal": 40, "pro": 1.9, "car": 8.8, "fat": 0.4, "fib": 1.5, "iron": 1.0, "video_url": "https://www.youtube.com/results?search_query=고추+레시피"},
        {"id": "enoki", "emoji": "🍄", "name_ko": "팽이버섯", "name_en": "Enoki Mushroom", "name_zh": "金针菇", "tag_ko": "키토글루칸 내장지방", "tag_en": "Enoki Fiber Det", "tag_zh": "清肠刮油金针菇", "badge_ko": "장청소부", "badge_en": "Intestine Care", "badge_zh": "清理油脂", "desc_ko": "버섯 키토산이 내장지방 배출에 아주 뛰어난 가성비 식재료입니다.", "desc_en": "Super low calorie texture component capturing lipids.", "desc_zh": "极高吸油吸水水溶性纤维。", "cal": 22, "pro": 2.7, "car": 5.0, "fat": 0.2, "fib": 3.3, "iron": 1.1, "video_url": "https://www.youtube.com/results?search_query=팽이버섯+레시피"},
        {"id": "paprika", "emoji": "🫑", "name_ko": "파프리카", "name_en": "Paprika", "name_zh": "彩椒", "tag_ko": "비타민 결정체 피부", "tag_en": "Vitamin C Glow", "tag_zh": "高维C美白彩椒", "badge_ko": "피부미용", "badge_en": "Skin Glow", "badge_zh": "细腻肌肤", "desc_ko": "레몬보다 2배 많은 비타민C가 들어가 기미 예방에 특효입니다.", "desc_en": "Sweet and crispy hydration with massive immunity markers.", "desc_zh": "颜色多样的抗氧化抗老化蔬菜。", "cal": 20, "pro": 1.0, "car": 4.7, "fat": 0.2, "fib": 2.1, "iron": 0.4, "video_url": "https://www.youtube.com/results?search_query=파프리카+레시피"},
        {"id": "grape", "emoji": "🍇", "name_ko": "포도", "name_en": "Grape", "name_zh": "葡萄", "tag_ko": "레스베라트롤 항암", "tag_en": "Resveratrol Core", "tag_zh": "白藜芦醇抗癌", "badge_ko": "젊음유지", "badge_en": "Stay Young", "badge_zh": "细胞年轻", "desc_ko": "껍질의 레스베라트롤 성분이 강력한 항암 및 세포 보호를 담당합니다.", "desc_en": "Polyphenol punch supporting visual capillary systems.", "desc_zh": "花青素与白藜芦醇的自然融合体。", "cal": 67, "pro": 0.6, "car": 18.1, "fat": 0.4, "fib": 0.9, "iron": 0.3, "video_url": "https://www.youtube.com/results?search_query=포도+레시피"},
        {"id": "strawberry", "emoji": "🍓", "name_ko": "딸기", "name_en": "Strawberry", "name_zh": "草莓", "tag_ko": "안토시아닌 피로회복", "tag_en": "Folate Sweetness", "tag_zh": "富含叶酸草莓", "badge_ko": "임산부추천", "badge_en": "Folate+", "badge_zh": "孕期营养", "desc_ko": "엽산과 비타민C가 조화롭게 녹아있어 기력 보충에 최고입니다.", "desc_en": "Folic acid dense refreshing berry treat.", "desc_zh": "清新香甜，可以缓解身体疲乏。", "cal": 32, "pro": 0.7, "car": 7.7, "fat": 0.3, "fib": 2.0, "iron": 0.4, "video_url": "https://www.youtube.com/results?search_query=딸기+레시피"},
        {"id": "cucumber", "emoji": "🥒", "name_ko": "오이", "name_en": "Cucumber", "name_zh": "黄瓜", "tag_ko": "수분보충 부종제거", "tag_en": "Extreme Hydration", "tag_zh": "超强补水排毒", "badge_ko": "갈증해소", "badge_en": "Hydrate", "badge_zh": "快速清热", "desc_ko": "95%가 수분으로 이뤄져 노폐물을 시원하게 배출합니다.", "desc_en": "Cleanses metabolic waste out of kidney tracts.", "desc_zh": "利尿清热，非常适合夏季消暑。", "cal": 15, "pro": 0.7, "car": 3.6, "fat": 0.1, "fib": 0.5, "iron": 0.3, "video_url": "https://www.youtube.com/results?search_query=오이+레시피"},
        {"id": "seaweed", "emoji": "🌱", "name_ko": "미역", "name_en": "Seaweed", "name_zh": "海带", "tag_ko": "요오드 조혈작용", "tag_en": "Iodine Blood", "tag_zh": "富含碘造血", "badge_ko": "산후조리식", "badge_en": "Blood Purify", "badge_zh": "净化血液", "desc_ko": "요오드와 칼슘이 피를 맑게 하고 상처 치유를 대폭 도와줍니다.", "desc_en": "Recharges blood minerals and active metabolism thyroid codes.", "desc_zh": "促进甲状腺健康 with 造血机能。", "cal": 45, "pro": 3.0, "car": 9.1, "fat": 0.5, "fib": 4.5, "iron": 2.5, "video_url": "https://www.youtube.com/results?search_query=미역+레시피"},
        {"id": "tuna", "emoji": "🐟", "name_ko": "참치", "name_en": "Tuna", "name_zh": "金枪鱼", "tag_ko": "DHA 셀레늄 뇌활성", "tag_en": "DHA Brain Power", "tag_zh": "DHA健脑金枪鱼", "badge_ko": "브레인푸드", "badge_en": "Brain Food", "badge_zh": "提高智力", "desc_ko": "DHA가 풍부해 뇌 기능을 자극하고 기억력을 최고조로 높여줍니다.", "desc_en": "Premium source of structural amino fatty lipids.", "desc_zh": "提供丰富的欧米伽不饱和脂肪酸。", "cal": 132, "pro": 28.0, "car": 0.0, "fat": 1.3, "fib": 0.0, "iron": 1.3, "video_url": "https://www.youtube.com/results?search_query=참치+레시피"},
        {"id": "chestnut", "emoji": "🌰", "name_ko": "밤", "name_en": "Chestnut", "name_zh": "板栗", "tag_ko": "탄수화물 비타민B1", "tag_en": "Vitamin B1 Carb", "tag_zh": "富含维B1板栗", "badge_ko": "위장강화", "badge_en": "Digestion Boost", "badge_zh": "健脾养胃", "desc_ko": "비타민B1이 풍부하여 피로 물질 축적을 효과적으로 저지합니다.", "desc_en": "Easily digestible premium structural carb alternative.", "desc_zh": "传统的淀粉能量与维他命滋补品。", "cal": 131, "pro": 2.4, "car": 28.0, "fat": 0.5, "fib": 5.0, "iron": 0.9, "video_url": "https://www.youtube.com/results?search_query=밤+레시피"},
        {"id": "beef", "emoji": "🥩", "name_ko": "소고기", "name_en": "Beef", "name_zh": "牛肉", "tag_ko": "흡수율최고 동물성철분", "tag_en": "Heme Iron Muscle", "tag_zh": "高效吸收血红素铁", "badge_ko": "빈혈예방", "badge_en": "Anti-Anemia", "badge_zh": "预防贫血", "desc_ko": "철분이 매우 풍부하여 빈혈을 즉각 치료하고 활력을 줍니다.", "desc_en": "Packed with high absorption iron components.", "desc_zh": "红肉铁质代表，补血健体。", "cal": 250, "pro": 26.0, "car": 0.0, "fat": 15.0, "fib": 0.0, "iron": 2.6, "video_url": "https://www.youtube.com/results?search_query=소고기+레시피"},

        # 41-50
        {"id": "oyster", "emoji": "🦪", "name_ko": "굴", "name_en": "Oyster", "name_zh": "生蚝", "tag_ko": "바다의우유 천연아연", "tag_en": "Zinc Powerhouse", "tag_zh": "海洋之乳天然锌", "badge_ko": "스테미나", "badge_en": "Stamina", "badge_zh": "男性活力", "desc_ko": "글리코겐 and 아연이 결합하여 지친 기력을 번개처럼 회복시킵니다.", "desc_en": "Immense natural mineral count regulating test systems.", "desc_zh": "极高的锌含量，促进免疫和修复。", "cal": 81, "pro": 9.5, "car": 5.0, "fat": 2.3, "fib": 0.0, "iron": 6.7, "video_url": "https://www.youtube.com/results?search_query=굴+레시피"},
        {"id": "lettuce", "emoji": "🥬", "name_ko": "상추", "name_en": "Lettuce", "name_zh": "生菜", "tag_ko": "락투카리움 숙면유도", "tag_en": "Lactucarium Sleep", "tag_zh": "莴苣素助眠生菜", "badge_ko": "불면증완화", "badge_en": "Good Sleep", "badge_zh": "安神安眠", "desc_ko": "줄기 속 락투카리움 성분이 신경을 안정시켜 꿀잠을 자게 합니다.", "desc_en": "Calms down hyperactive neurons for clean recovery sleep.", "desc_zh": "镇静神经，有显著的安神效果。", "cal": 15, "pro": 1.4, "car": 2.9, "fat": 0.2, "fib": 1.3, "iron": 0.9, "video_url": "https://www.youtube.com/results?search_query=상추+레시피"},
        {"id": "kiwi", "emoji": "🥝", "name_ko": "키위", "name_en": "Kiwi", "name_zh": "猕猴桃", "tag_ko": "액티니딘 소화효소", "tag_en": "Actinidin Enzyme", "tag_zh": "奇异果酵素促消化", "badge_ko": "천연소화제", "badge_en": "Proteolytic", "badge_zh": "分解肉类", "desc_ko": "단백질 분해 효소인 액티니딘이 육류 소화를 환상적으로 돕습니다.", "desc_en": "Breaks down dense meats inside gastric pipelines.", "desc_zh": "含有大量可以分解肉类蛋白的酶。", "cal": 61, "pro": 1.1, "car": 14.7, "fat": 0.5, "fib": 3.0, "iron": 0.3, "video_url": "https://www.youtube.com/results?search_query=키위+레시피"},
        {"id": "pear", "emoji": "🍐", "name_ko": "배", "name_en": "Pear", "name_zh": "梨", "tag_ko": "루테올린 기관지보호", "tag_en": "Luteolin Lungs", "tag_zh": "木犀草素清肺止咳", "badge_ko": "기침감기예방", "badge_en": "Lung Care", "badge_zh": "润肺化痰", "desc_ko": "루테올린 성분이 기침과 가래를 멎게 하고 기관지를 보호합니다.", "desc_en": "Reduces heat inside lung tissues and hydrates chords.", "desc_zh": "润肺止咳，缓解秋冬燥热。", "cal": 57, "pro": 0.4, "car": 15.2, "fat": 0.1, "fib": 3.1, "iron": 0.2, "video_url": "https://www.youtube.com/results?search_query=배+레시피"},
        {"id": "black_bean", "emoji": "🫘", "name_ko": "검은콩", "name_en": "Black Bean", "name_zh": "黑豆", "tag_ko": "이소플라본 탈모예방", "tag_en": "Isoflavone Hair", "tag_zh": "异黄酮防脱发", "badge_ko": "모발영양", "badge_en": "Hair Nutrient", "badge_zh": "乌黑亮发", "desc_ko": "안토시아닌과 이소플라본이 모근을 튼튼하게 강화해 줍니다.", "desc_en": "Estrogen balance catalyst enhancing blood scalp flow.", "desc_zh": "补充黑色素与天然植物雌激素。", "cal": 341, "pro": 34.4, "car": 34.9, "fat": 11.1, "fib": 15.2, "iron": 6.5, "video_url": "https://www.youtube.com/results?search_query=검은콩+레시피"},
        {"id": "barley", "emoji": "🌾", "name_ko": "보리", "name_en": "Barley", "name_zh": "大麦", "tag_ko": "베타글루칸 당뇨예방", "tag_en": "Glucose Balance", "tag_zh": "平稳血糖大麦", "badge_ko": "당뇨개선", "badge_en": "Insulin Care", "badge_zh": "平稳胰岛", "desc_ko": "식이섬유가 풍부하여 식후 혈당이 급상승하는 것을 예방합니다.", "desc_en": "Keeps blood sugar curves flattened and clean.", "desc_zh": "防止餐后血糖出现过大波动。", "cal": 354, "pro": 12.5, "car": 73.5, "fat": 2.3, "fib": 17.3, "iron": 3.6, "video_url": "https://www.youtube.com/results?search_query=보리+레시피"},
        {"id": "sesame", "emoji": "🌱", "name_ko": "참깨", "name_en": "Sesame", "name_zh": "芝麻", "tag_ko": "세사민 심혈관보호", "tag_en": "Sesamin Lipids", "tag_zh": "芝麻素抗氧化", "badge_ko": "고소한항산화", "badge_en": "Antioxidant+", "badge_zh": "优质坚果油", "desc_ko": "세사민 성분이 체내 나쁜 콜레스테롤 흡수를 원천 억제합니다.", "desc_en": "Tiny drops of cellular layer armor nutrients.", "desc_zh": "富含亚油酸与天然植物抗氧化素。", "cal": 573, "pro": 17.7, "car": 23.4, "fat": 49.7, "fib": 11.8, "iron": 14.6, "video_url": "https://www.youtube.com/results?search_query=참깨+레시피"},
        {"id": "water_dropwort", "emoji": "🌿", "name_ko": "미나리", "name_en": "Water Dropwort", "name_zh": "水芹菜", "tag_ko": "중금속배출 해독장인", "tag_en": "Heavy Metal Detox", "tag_zh": "重金属排毒水芹", "badge_ko": "간기능개선", "badge_en": "Liver Save", "badge_zh": "清热解毒", "desc_ko": "체내 축적된 중금속을 흡착하여 소변으로 신속히 배출시켜 줍니다.", "desc_en": "Excellent wild herb flushes clean bile systems.", "desc_zh": "解酒保肝，清理体内有害重金属。", "cal": 16, "pro": 1.5, "car": 3.4, "fat": 0.2, "fib": 2.2, "iron": 1.5, "video_url": "https://www.youtube.com/results?search_query=미나리+레시피"},
        {"id": "radish", "emoji": "🥬", "name_ko": "무", "name_en": "Radish", "name_zh": "白萝卜", "tag_ko": "디아스타아제 천연소화", "tag_en": "Diastase Comfort", "tag_zh": "淀粉酶顺气消食", "badge_ko": "천연속편함", "badge_en": "Anti-Bloat", "badge_zh": "顺气大王", "desc_ko": "전분 분해 효소가 풍부해 밀가루 음식을 먹고 체했을 때 명약입니다.", "desc_en": "Root liquid soothe stomach inflammation immediately.", "desc_zh": "解除积食，润喉化痰功效好。", "cal": 16, "pro": 0.8, "car": 3.5, "fat": 0.1, "fib": 1.6, "iron": 0.2, "video_url": "https://www.youtube.com/results?search_query=무+레시피"},
        {"id": "clam", "emoji": "🐚", "name_ko": "조개", "name_en": "Clam", "name_zh": "贝类", "tag_ko": "비타민B12 숙취해소", "tag_en": "B12 Liver Reset", "tag_zh": "维B12解酒造血", "badge_ko": "간세포재생", "badge_en": "Liver Care", "badge_zh": "高效排毒", "desc_ko": "아미노산과 비타민B12가 망가진 간세포의 빠른 재생을 유도합니다.", "desc_en": "Trace minerals keeping nerve system shells humming perfectly.", "desc_zh": "富含牛磺酸，低脂且矿物质充沛。", "cal": 74, "pro": 12.8, "car": 2.6, "fat": 1.1, "fib": 0.0, "iron": 14.0, "video_url": "https://www.youtube.com/results?search_query=조개+레시피"}
    ]

# 4. 레시피 엔진
def get_recipes_for_all(food_id, food_name, lang):
    if lang == "한국어":
        return [
            {"title": f"1. 프레시 {food_name} 매거진 샐러드 볼", "time": "15분", "calories": "210 kcal", "level": "쉬움", "steps": [f"{food_name}를 깨끗이 세척 후 가볍게 데치거나 슬라이스하여 준비합니다.", "방울토마토, 적양파, 오이를 한입 크기로 정갈하게 손질합니다.", "올리브유 2스푼과 수제 드레싱을 조제해 가볍게 섞어줍니다."], "tip": f"{food_name} 본연의 아삭한 향미를 보존하려면 드레싱을 먹기 직전에 뿌려주세요."},
            {"title": f"2. 아티스틱 {food_name} 건강 타락 미음", "time": "25분", "calories": "180 kcal", "level": "보통", "steps": [f"준비된 {food_name}를 신선한 우유와 함께 블렌더에 갈아냅니다.", "약불의 냄비에서 실리콘 스패튤러로 천천히 저어가며 뭉근하게 끓입니다.", "소금 반 티스푼으로 감칠맛을 끌어올려 완성합니다."], "tip": "눌어붙지 않도록 계속 한쪽 방향으로만 저어주는 것이 핵심입니다."},
            {"title": f"3. 크런치 {food_name} 스낵 칩스", "time": "20분", "calories": "130 kcal", "level": "쉬움", "steps": [f"{food_name}를 오븐 페이퍼 위에 최대한 얇고 평평하게 배치해 줍니다.", "허브 솔트를 살짝 곁들인 후 에어프라이어 160도에서 12분간 조리합니다."], "tip": "수분기를 완전히 날려줘야 식은 후에 바삭함이 극대화됩니다."},
            {"title": f"4. 프리미엄 {food_name} 영양 솥밥", "time": "40분", "calories": "310 kcal", "level": "어려움", "steps": ["불려둔 백미 위에 먹기 좋은 크기로 썬 식재료를 이쁘게 플레이팅합니다.", "무쇠솥 불 조절을 강불 5분, 약불 15분 루틴으로 맞추어 뜸 들입니다."], "tip": "재료 자체에서 수분이 배어 나올 수 있으니 평소보다 물 양을 살짝 줄여주세요."},
            {"title": f"5. 매콤 새콤 {food_name} 가든 웰빙 무침", "time": "15분", "calories": "160 kcal", "level": "쉬움", "steps": [f"깻잎과 양배추를 채 썰어 {food_name}와 함께 믹싱 볼에 조합합니다.", "초고추장 소스와 매실청 한 스푼을 둘러 가볍게 버무려 줍니다."], "tip": "새콤한 초절임 베이스 소스를 활용하면 감칠맛이 폭발적으로 상승합니다."}
        ]
    elif lang == "English":
        return [{"title": f"{i}. Premium {food_name} Artisan Diet Style", "time": "15m", "calories": "210 kcal", "level": "Easy", "steps": [f"Clean and prepare fresh {food_name} thoroughly.", "Combine with organic vegetables and house dressing."], "tip": "Best served chilled for maximum flavor retention."} for i in range(1, 6)]
    else:
        return [{"title": f"{i}. 精致 {food_name} 艺术健康主题餐", "time": "15分钟", "calories": "190 千卡", "level": "简单", "steps": [f"将 {food_name} 洗净并进行美观的高级刀工切片处理。", "搭配有机蔬菜，淋上特制少盐低脂沙拉酱。"], "tip": "即做即食可以最大程度保留其抗氧化营养活性。"} for i in range(1, 6)]

# 데이터 로딩 및 상태 세팅
all_foods = load_all_foods()
food_options_map = {f"{f['emoji']} {f['name_ko']} ({f['name_en']})": f["id"] for f in all_foods}

if "selected_food_id" not in st.session_state:
    st.session_state.selected_food_id = "quinoa"
if "my_fridge" not in st.session_state:
    st.session_state.my_fridge = []

# 5. 사이드바 구성
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

# 6. 상단 메인 간판 타이틀 브랜딩
st.markdown(f"<p class='brand-sub'>{text_pack['sub_logo']}</p>", unsafe_allow_html=True)
st.markdown(f"<h1 class='brand-main'>{text_pack['title_main']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='brand-desc'>{text_pack['subtitle']}</p>", unsafe_allow_html=True)

# 50대 식재료 검색 셀렉터
default_idx = 0
for i, f in enumerate(all_foods):
    if f["id"] == st.session_state.selected_food_id:
        default_idx = i
        break

selected_option = st.selectbox(
    text_pack["selector_label"],
    list(food_options_map.keys()),
    index=default_idx
)
st.session_state.selected_food_id = food_options_map[selected_option]

# 탭 나누기
tab1, tab2 = st.tabs([text_pack["tab1"], text_pack["tab2"]])

# --- Tab 1: 식재료 카드 그리드 및 정밀 레이더 도감 ---
with tab1:
    st.markdown(f"### 🥦 {text_pack['intro_recom']}")
    
    # 상단 4대 주력 추천 카드 레이아웃
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
            
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button("선택" if selected_lang=="한국어" else ("Select" if selected_lang=="English" else "选择"), key=f"t1_sel_{item['id']}", use_container_width=True):
                    st.session_state.selected_food_id = item["id"]
                    st.rerun()
            with b_col2:
                if st.button("정보" if selected_lang=="한국어" else ("Info" if selected_lang=="English" else "信息"), key=f"t1_inf_{item['id']}", use_container_width=True):
                    st.session_state.selected_food_id = item["id"]
                    st.rerun()

    active_food = next(x for x in all_foods if x["id"] == st.session_state.selected_food_id)
    st.write("---")
    
    # 상세 대시보드
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
                <p style='font-size: 15px; line-height:1.7; color:#333333;'>{disp_desc}</p>
                <hr style='border:0; border-top:1px solid #EEF0EC; margin:20px 0;'>
                <div class="card-title" style='font-size:16px;'>{text_pack['nut_info']}</div>
                <div style='display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-top:10px;'>
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
        fig_radar = px.Figure()
        nut_keys = ["pro", "fib", "cal", "fat", "car", "iron"]
        max_vals = {"pro": 40, "fib": 20, "cal": 700, "fat": 70, "car": 80, "iron": 15}
        r_vals = [(active_food[n] / max_vals[n]) * 100 for n in nut_keys]
        
        fig_radar.add_trace(px.Scatterpolar(
            r=r_vals + [r_vals[0]],
            theta=text_pack["nutrients"] + [text_pack["nutrients"][0]],
            fill='toself', line_color='#3B6D11', fillcolor='rgba(59, 109, 17, 0.15)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#ECEEEB")),
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=30, l=40, r=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# --- Tab 2: 레시피 5종 룸 + 요리 영상 가이드 링크 연동 ---
with tab2:
    active_food = next(x for x in all_foods if x["id"] == st.session_state.selected_food_id)
    if selected_lang == "한국어":
        recipe_target_name = active_food["name_ko"]
    elif selected_lang == "English":
        recipe_target_name = active_food["name_en"]
    else:
        recipe_target_name = active_food["name_zh"]
        
    st.markdown(f"### 🍳 {active_food['emoji']} {recipe_target_name} · {text_pack['recipe_room']}")
    
    recipes_list = get_recipes_for_all(active_food["id"], recipe_target_name, selected_lang)
    
    for idx, rc in enumerate(recipes_list):
        steps_html = "".join([
            f'<div class="step-item"><div class="step-number">{i+1}</div><div class="step-text">{step}</div></div>' 
            for i, step in enumerate(rc['steps'])
        ])
        
        st.markdown(f"""
            <div class="cute-card">
                <div class="card-title" style='font-size:20px; color:#2C3A1E; margin-bottom:12px;'>{rc['title']}</div>
                <div class="badge-container">
                    <span class="badge badge-time">⏱️ {rc['time']}</span>
                    <span class="badge badge-cal">🔥 {rc['calories']}</span>
                    <span class="badge badge-ing">🌿 {recipe_target_name}</span>
                    <span class="badge badge-level">● {rc['level']}</span>
                </div>
                <hr style='border:0; border-top:1px solid #F0F2EE; margin:15px 0;'>
                <div>
                    {steps_html}
                </div>
                <div class="tip-box">
                    💡 <b>Nourish Secret Tip:</b> {rc['tip']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if rc['title'] in st.session_state.my_fridge:
                if st.button(text_pack['btn_del'], key=f"t2_del_{idx}_{active_food['id']}", use_container_width=True):
                    st.session_state.my_fridge.remove(rc['title'])
                    st.rerun()
            else:
                if st.button(text_pack['btn_add'], key=f"t2_add_{idx}_{active_food['id']}", use_container_width=True):
                    st.session_state.my_fridge.append(rc['title'])
                    st.rerun()
        with col_btn2:
            st.link_button(text_pack['btn_video'], active_food["video_url"], use_container_width=False)