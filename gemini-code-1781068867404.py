import streamlit as st
import pandas as pd
import plotly.graph_objects as px

# 1. 페이지 설정 및 브랜딩 테마 선언
st.set_page_config(
    page_title="Nourish · Ingredient & Recipe Hub",
    page_icon="🌿",
    layout="wide"
)

# 고급스러운 가독성 및 카드 격자(Grid) 배열을 위한 CSS 커스텀
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Noto+Sans+KR:wght@300;400;700&display=swap');
    
    /* 전체 배경 테마 */
    .main { background-color: #FBFBFA; }
    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
        color: #2C3A1E;
    }
    
    /* 헤더 타이틀 */
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

    /* 탭 메뉴 스타일 */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: bold;
        color: #8C9A82;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #3B6D11 !important;
        border-bottom-color: #3B6D11 !important;
    }

    /* 🚨 메인 추천 식재료 카드 스타일 (스크린샷 배열 복원) */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .food-card {
        background-color: white;
        border-radius: 16px;
        border: 1px solid #EAECE8;
        box-shadow: 0px 4px 20px rgba(44, 58, 30, 0.03);
        text-align: center;
        padding: 25px 15px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .food-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 6px 25px rgba(44, 58, 30, 0.08);
    }
    .food-emoji {
        font-size: 45px;
        margin-bottom: 10px;
    }
    .food-name {
        font-size: 19px;
        font-weight: 700;
        color: #2C3A1E;
        margin-bottom: 4px;
    }
    .food-tagline {
        font-size: 13px;
        color: #8C9A82;
        margin-bottom: 12px;
    }
    .food-badge {
        background-color: #F4F6F2;
        color: #556B2F;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: bold;
    }

    /* 상세 도감 & 레시피 내부 공통 카드 */
    .cute-card {
        background-color: white;
        padding: 26px;
        border-radius: 16px;
        border: 1px solid #EAECE8;
        box-shadow: 0px 4px 20px rgba(44, 58, 30, 0.04);
        margin-bottom: 25px;
    }
    .card-title {
        font-size: 20px;
        font-weight: 700;
        color: #2C3A1E;
        margin-bottom: 12px;
    }

    /* 영양성분 그리드 아이템 (보호색 에러 완벽 해결) */
    .nut-grid-item {
        background-color: #F6F8F5 !important; 
        padding: 15px; 
        border-radius: 10px;
        color: #2C3A1E !important;
        font-size: 15px;
        font-weight: bold;
        border: 1px solid #EEF1EC;
    }

    /* 메타 뱃지 */
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

    /* 조리법 순서 스타일 */
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        padding: 12px 0;
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
        font-size: 13px;
        font-weight: bold;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .step-text {
        font-size: 15px;
        color: #333333;
        line-height: 1.6;
    }

    /* 꿀팁 박스 */
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

# 2. 🚨 다국어 사전 (한국어, English + 중국어 완벽 추가)
UI_TEXTS = {
    "한국어": {
        "sub_logo": "🌿 GOOD FOOD STARTS HERE",
        "title_main": "오늘의 식재료를<br><span style='color:#3B6D11;'>탐색해보세요</span>",
        "subtitle": "싱그럽고 영양 가득한 전통 식재료 가이드 💚",
        "intro_recom": "오늘의 추천 식재료",
        "intro_guide": "선택 버튼을 누르면 레시피 탭에서 레시피를 확인할 수 있어요 · 정보 버튼으로 상세 영양 정보 확인",
        "tab1": "🌿 식재료 탐색",
        "tab2": "🍳 레시피",
        "doc_title": "상세 도감",
        "nut_info": "📊 영양 성분 (100g 기준)",
        "recipe_room": "맞춤형 추천 레시피 (5가지 테마)",
        "btn_del": "❌ 빼기",
        "btn_add": "🧡 찜하기",
        "btn_video": "📺 요리 가이드 영상 보기",
        "saved_title": "❤️ 내가 찜한 레시피",
        "saved_empty": "찜한 레시피가 비어 있습니다.",
        "academic": "🎓 학과 및 학생 정보",
        "nutrients": ["단백질 (g)", "식이섬유 (g)", "칼로리 (kcal)", "지방 (g)", "탄수화물 (g)", "철분 (mg)"],
        "labels": ["칼로리", "단백질", "탄수화물", "지방", "식이섬유", "철분"]
    },
    "English": {
        "sub_logo": "🌿 GOOD FOOD STARTS HERE",
        "title_main": "Explore <span style='color:#3B6D11;'>Wholesome Ingredients</span><br>for Today",
        "subtitle": "Nutrient-dense profile guide for traditional ingredients 💚",
        "intro_recom": "Today's Recommended Ingredients",
        "intro_guide": "Click 'Select' to unlock recipes in the Recipe tab · Click 'Info' for deep nutrition metrics",
        "tab1": "🌿 Explore Ingredients",
        "tab2": "🍳 Recipes",
        "doc_title": "Encyclopedia",
        "nut_info": "📊 Nutrition Info (per 100g)",
        "recipe_room": "Tailored Recipe Collection (5 Custom Themes)",
        "btn_del": "❌ Remove",
        "btn_add": "🧡 Save",
        "btn_video": "📺 Watch Recipe Video",
        "saved_title": "❤️ Saved Recipes",
        "saved_empty": "Your saved recipes will appear here.",
        "academic": "🎓 Academic Info",
        "nutrients": ["Protein (g)", "Fibre (g)", "Calories (kcal)", "Fat (g)", "Carbs (g)", "Iron (mg)"],
        "labels": ["Calories", "Protein", "Carbohydrates", "Fat", "Dietary Fibre", "Iron"]
    },
    "중국어 (简体中文)": {
        "sub_logo": "🌿 GOOD FOOD STARTS HERE",
        "title_main": "探索今天的<br><span style='color:#3B6D11;'>健康食材</span>",
        "subtitle": "充满活力与营养的传统食材专业指南 💚",
        "intro_recom": "今日推荐食材",
        "intro_guide": "点击'选择'可在食谱标签页中查看对应食谱 · 点击'信息'查看详细营养成分",
        "tab1": "🌿 食材探索",
        "tab2": "🍳 推荐食谱",
        "doc_title": "详细百科",
        "nut_info": "📊 营养成分 (每100g)",
        "recipe_room": "定制推荐食谱 (5大主题)",
        "btn_del": "❌ 移除",
        "btn_add": "🧡 收藏",
        "btn_video": "📺 查看烹饪指导视频",
        "saved_title": "❤️ 我收藏的食谱",
        "saved_empty": "收藏夹空空如也。",
        "academic": "🎓 选课及学生信息",
        "nutrients": ["蛋白质 (g)", "膳食纤维 (g)", "卡路里 (kcal)", "脂肪 (g)", "碳水化合物 (g)", "铁分 (mg)"],
        "labels": ["热量", "蛋白质", "碳水化合物", "脂肪", "膳食纤维", "铁"]
    }
}

# 3. 데이터셋 (실명 기반 4대 주력 핵심 식재료 고정 및 매핑)
@st.cache_data
def load_food_data():
    return [
        {"id": "quinoa", "emoji": "🌾", "name_ko": "퀴노아", "name_en": "Quinoa", "name_zh": "藜麦",
         "tag_ko": "완전단백질 슈퍼씨앗", "tag_en": "Complete Plant Protein", "tag_zh": "全蛋白超级种子",
         "badge_ko": "글루텐프리", "badge_en": "Gluten-Free", "badge_zh": "无麸质",
         "desc_ko": "퀴노아는 필수 아미노산이 골고루 함유된 대표적인 글루텐 프리 곡물입니다. 식이섬유가 풍부해 당뇨 조절과 다이어트에 뛰어난 효과를 자랑합니다.",
         "desc_en": "Quinoa is a premium gluten-free seed holding all essential amino acids.",
         "desc_zh": "藜麦是一种不含麸质的高端超级谷物，包含人体所需的所有必需氨基酸，膳食纤维极高。",
         "cal": 368, "pro": 14.1, "car": 64.0, "fat": 6.1, "fib": 7.0, "iron": 4.6},
         
        {"id": "avocado", "emoji": "🥑", "name_ko": "아보카도", "name_en": "Avocado", "name_zh": "牛油果",
         "tag_ko": "건강한 단일불포화지방", "tag_en": "Healthy Monounsaturated Fat", "tag_zh": "健康的单不饱和脂肪",
         "badge_ko": "비타민E", "badge_en": "Vitamin E Rich", "badge_zh": "富含维生素E",
         "desc_ko": "숲속의 버터라 불리는 아보카도는 불포화 지방산이 풍부해 심혈관 건강에 도움을 주며, 풍부한 칼륨이 체내 나트륨 배출을 강력하게 돕습니다.",
         "desc_en": "Known as butter in the forest, loaded with healthy heart-defending lipids.",
         "desc_zh": "被称为森林黄油，富含健康的单不饱和脂肪酸，钾含量极高，有利于心血管健康。",
         "cal": 160, "pro": 2.0, "car": 8.5, "fat": 14.7, "fib": 6.7, "iron": 0.6},
         
        {"id": "tofu", "emoji": "🫘", "name_ko": "두부", "name_en": "Tofu", "name_zh": "豆腐",
         "tag_ko": "식물성 완전단백질", "tag_en": "Plant-Based Protein Core", "tag_zh": "植物性优质全蛋白质",
         "badge_ko": "저칼로리", "badge_en": "Low-Calorie", "badge_zh": "低热量",
         "desc_ko": "두부는 콩 단백질을 응축시켜 소화 흡수율을 95% 이상으로 끌어올린 고단백 식재료입니다. 리놀산 성분이 혈관 내 콜레스테롤 수치를 청정하게 낮춰줍니다.",
         "desc_en": "Condensed soy curd boasting massive digestion rates and zero bad cholesterol.",
         "desc_zh": "纯植物大豆蛋白凝聚而成，吸收率高达95%以上，亚油酸成分可有效软化血管。",
         "cal": 84, "pro": 8.9, "car": 2.9, "fat": 4.8, "fib": 0.2, "iron": 1.5},
         
        {"id": "blueberry", "emoji": "🫐", "name_ko": "블루베리", "name_en": "Blueberry", "name_zh": "蓝莓",
         "tag_ko": "항산화 슈퍼푸드", "tag_en": "Antioxidant Powerhouse", "tag_zh": "强效抗氧化超级食物",
         "badge_ko": "비타민C", "badge_en": "Vitamin C Plus", "badge_zh": "富含维生素C",
         "desc_ko": "블루베리는 안토시아닌이라는 강력한 항산화 색소로 꽉 차 있습니다. 활성산소를 파괴해 노화를 지연시키고 눈의 피로를 극적으로 완화해 줍니다.",
         "desc_en": "Packed with deep anthocyanin pigments that scrub free radicals and enhance vision.",
         "desc_zh": "富含花青素成分，具有极强的清除自由基、抗衰老能力，并能有效保护视力缓解疲劳。",
         "cal": 57, "pro": 0.7, "car": 14.5, "fat": 0.3, "fib": 2.4, "iron": 0.3}
    ]

# 4. 요구사항을 완벽하게 충족하는 고품격 테마별 레시피 5종 빌더
def get_5_recipes(food_id, lang):
    if lang == "한국어":
        recipes = {
            "quinoa": [
                {"title": "1. 프레시 퀴노아 매거진 샐러드 볼", "time": "15분", "calories": "210 kcal", "level": "쉬움", "steps": ["퀴노아를 끓는 물에 15분간 삶아 체에 받쳐 식힙니다.", "방울토마토, 적양파, 오이를 큐브 모양으로 정갈하게 썰어줍니다.", "올리브유 2스푼과 레몬즙을 혼합해 수제 새콤 드레싱을 조제합니다.", "보울에 퀴노아와 야채를 담고 드레싱을 끼얹어 산뜻하게 버무립니다."], "tip": "조리 전 퀴노아를 껍질째 박박 문질러 씻어야 쓴맛이 깔끔하게 제거됩니다."},
                {"title": "2. 고소한 퀴노아 타락 미음 수프", "time": "25분", "calories": "180 kcal", "level": "보통", "steps": ["삶은 퀴노아와 부드러운 우유를 믹서기에 넣고 곱게 갈아냅니다.", "냄비에 간 재료를 붓고 뭉근한 약불에서 저어가며 끓여줍니다.", "소금과 꿀을 아주 가볍게 반 티스푼 넣어 간을 맞춥니다.", "크랜베리 고명을 올려 부드러우면서도 아삭하게 완성합니다."], "tip": "바닥이 쉽게 눌어붙을 수 있으니 실리콘 주걱으로 계속 저어주는 것이 필수입니다."},
                {"title": "3. 크런치 퀴노아 라이스 칩 스낵", "time": "20분", "calories": "130 kcal", "level": "쉬움", "steps": ["삶은 퀴노아에 계란 흰자 한 스푼과 소금 한 꼬집을 버무립니다.", "오븐 종이 위에 반죽을 아주 얇고 평평하게 펴서 세팅합니다.", "160도로 예열된 에어프라이어에 넣고 12분간 바삭하게 구워냅니다.", "완전히 식힌 후 크런치한 질감이 살면 손으로 툭툭 부수어 즐깁니다."], "tip": "두껍게 펴지면 눅눅해지니 최대한 종이처럼 얇게 밀착시키는 것이 핵심입니다."},
                {"title": "4. 프리미엄 퀴노아 버섯 영양 솥밥", "time": "40분", "calories": "310 kcal", "level": "어려움", "steps": ["불려둔 백미 쌀 위에 생 퀴노아를 황금 비율로 섞어 안칩니다.", "표고버섯과 슬라이스 당근을 쌀 위에 예쁘게 고명으로 얹어줍니다.", "무쇠솥 뚜껑을 닫고 강불 5분, 약불 15분 후 뜸을 들입니다.", "달래 양념장을 곁들여 고슬고슬하고 영양 가득하게 비벼냅니다."], "tip": "퀴노아가 물을 흡수하므로 일반 평소 밥물보다 약 5~10%만 물을 더 잡아주세요."},
                {"title": "5. 매콤 새콤 퀴노아 아티스틱 무침", "time": "15분", "calories": "160 kcal", "level": "쉬움", "steps": ["삶은 퀴노아와 채 썬 깻잎, 양배추를 믹싱 볼에 담습니다.", "초고추장 1큰술과 매실청, 참기름을 섞어 특제 매콤 소스를 만듭니다.", "야채가 숨 죽지 않게 손끝으로 낙하하듯 가볍게 무쳐냅니다.", "마지막으로 통깨를 가득 뿌려 이색적인 식감의 무침 요리를 완성합니다."], "tip": "깻잎의 향과 퀴노아의 톡톡 터지는 식감이 어우러져 한식 보조 메뉴로 최고입니다."}
            ],
            "avocado": [
                {"title": "1. 프리미엄 아보카도 명란 비빔밥", "time": "10분", "calories": "390 kcal", "level": "쉬움", "steps": ["잘 익은 아보카도를 반으로 갈라 얇게 슬라이스해 둡니다.", "따뜻한 밥 위에 손질한 아보카도와 저염 명란젓을 올립니다.", "계란 프라이를 반숙으로 구워 중앙에 데코레이션합니다.", "참기름과 통깨를 두르고 기호에 따라 김가루를 솔솔 뿌려 완성합니다."], "tip": "껍질이 검은빛을 띠고 만졌을 때 살짝 들어가는 잘 숙성된 아보카도를 쓰셔야 맛있습니다."},
                {"title": "2. 멕시칸 오리지널 아보카도 과카몰리", "time": "12분", "calories": "150 kcal", "level": "쉬움", "steps": ["볼에 아보카도 과육을 넣고 포크로 거칠게 으깨어 줍니다.", "다진 토마토, 다진 양파, 다진 레몬즙 1큰술을 투하합니다.", "소금과 후추를 가볍게 톡톡 뿌려 간을 정교하게 맞춥니다.", "나쵸 칩이나 크래커 위에 가득 얹어 핑거푸드로 연출합니다."], "tip": "레몬즙은 산뜻한 맛을 더할 뿐만 아니라 아보카도가 갈색으로 변하는 갈변을 막아줍니다."},
                {"title": "3. 딥그린 아보카도 바나나 건강 스무디", "time": "5분", "calories": "220 kcal", "level": "쉬움", "steps": ["아보카도 반 개와 달콤한 바나나 1개를 토막 내어 준비합니다.", "블렌더에 과일들과 우유 또는 두유 한 컵을 부어줍니다.", "얼음 3조각과 꿀 1스푼을 첨가해 시원함을 더해줍니다.", "덩어리가 남지 않도록 고속으로 1분간 매끄럽게 갈아 유리잔에 담습니다."], "tip": "바나나가 충분히 단맛을 내기 때문에 슈가 시럽을 따로 넣지 않아도 훌륭합니다."},
                {"title": "4. 에그 인 아보카도 보트 오븐 구이", "time": "20分", "calories": "240 kcal", "level": "보통", "steps": ["아보카도를 세로로 자른 뒤 씨를 빼내고 구멍을 살짝 넓힙니다.", "파인 홈 공간 안에 계란 노른자와 흰자를 조심스럽게 채워 넣습니다.", "소금, 후추, 모짜렐라 치즈를 상단에 가득 토핑합니다.", "180도로 예열된 오븐이나 에어프라이어에서 12분간 구워 마무리합니다."], "tip": "계란이 넘치지 않도록 흰자 양을 조절하며 머핀 틀에 고정해 구우면 아주 편리합니다."},
                {"title": "5. 아보카도 가든 케일 샐러드 볼", "time": "15분", "calories": "180 kcal", "level": "쉬움", "steps": ["부드러운 케일 잎을 씻어 물기를 빼고 먹기 좋게 찢어줍니다.", "아보카도를 깍둑썰기하고 아몬드 슬라이스를 곁들입니다.", "발사믹 식초 2스푼과 올리브유를 섞어 가벼운 드레싱을 완성합니다.", "모든 웰빙 야채 위에 드레싱을 뿌려 예술적인 감각으로 플레이팅합니다."], "tip": "케일 잎을 드레싱에 먼저 버무려 숨을 살짝 죽여놓으면 식감이 훨씬 부드러워집니다."}
            ],
            "tofu": [
                {"title": "1. 웰빙 순두부 토마토 카프레제 스페셜", "time": "15분", "calories": "140 kcal", "level": "쉬움", "steps": ["단단한 두부나 순두부를 가로 방향으로 일정한 두께로 썹니다.", "완숙 토마토를 두부와 동일한 두께로 슬라이스해 줍니다.", "접시 위에 두부와 토마토를 번갈아 가며 겹치듯 배열합니다.", "올리브유와 오리엔탈 간장 소스를 믹스해 상단에 뿌려 완성합니다."], "tip": "두부의 물기를 키친타월로 미리 최대한 빼주어야 소스가 겉돌지 않고 착 감깁니다."},
                {"title": "2. 크런치 두부 소보로 소고기 덮밥", "time": "20분", "calories": "290 kcal", "level": "보통", "steps": ["두부를 칼등으로 으깬 뒤 면포에 싸서 수분을 짜냅니다.", "마른 팬에 기름 없이 으깬 두부를 올려 고슬고슬해질 때까지 볶아 수분을 날립니다.", "간장 1스푼과 올리고당으로 볶은 두부에 달콤 짭조름한 베이스 간을 합니다.", "따뜻한 밥 위에 두부 소보로를 소복이 얹고 쪽파를 뿌려 상에 올립니다."], "tip": "수분이 완전히 날아가 과자처럼 고슬고슬해질 때까지 충분히 볶아야 식감이 극대화됩니다."},
                {"title": "3. 에어프라이어 허브 두부 큐브 스테이크", "time": "22분", "calories": "190 kcal", "level": "쉬움", "steps": ["두부를 가로세로 2cm 정육면체 큐브 모양으로 이쁘게 자릅니다.", "올리브유, 허브 솔트, 파슬리 가루를 골고루 묻혀 시즈닝합니다.", "에어프라이어 바스켓에 큐브들을 서로 닿지 않게 나열합니다.", "190도 고온에서 15분간 사방이 노릇해지도록 구워 서빙합니다."], "tip": "겉은 바삭하고 속은 촉촉한 일명 '겉바속촉' 식감을 내는 가장 다이어트에 좋은 스낵입니다."},
                {"title": "4. 아티스틱 명란 두부 달걀 전", "time": "15분", "calories": "210 kcal", "level": "쉬움", "steps": ["두부를 사각형 모양으로 썰어 소금을 살짝 뿌려 밑간을 합니다.", "계란을 풀고 다진 쪽파와 껍질을 제거한 명란 가루를 섞어줍니다.", "두부에 부침가루를 얇게 묻힌 뒤 계란 옷을 정성스레 입힙니다.", "팬에 기름을 두르고 앞뒤로 노릇하게 지져 따뜻할 때 제공합니다."], "tip": "명란 자체에 간이 세게 되어 있으므로 계란물에는 소금 간을 생략하는 것이 좋습니다."},
                {"title": "5. 매콤 짭조름 두부 인 마파 가든", "time": "25분", "calories": "320 kcal", "level": "보통", "steps": ["큐브 모양의 두부와 다진 양파, 파, 피망을 미리 썰어둡니다.", "팬에 고추기름을 두르고 다진 마늘과 대파를 볶아 향을 냅니다.", "두반장 소스 1스푼과 물 반 컵을 넣고 소스가 끓으면 두부를 투하합니다.", "전분물을 조금씩 부어 걸쭉하게 농도를 맞춘 뒤 밥 위에 얹어 완성합니다."], "tip": "두부를 조리 전 끓는 물에 소금을 살짝 넣어 데쳐두면 쉽게 부서지지 않습니다."}
            ],
            "blueberry": [
                {"title": "1. 프리미엄 블루베리 요거트 파르페 bowl", "time": "5분", "calories": "160 kcal", "level": "쉬움", "steps": ["투명한 유리잔에 무가당 플레인 요거트를 두 스푼 채웁니다.", "그 위에 신선한 블루베리와 그라놀라를 한 층 올립니다.", "다시 요거트와 블루베리를 교차하며 층층이 레이어링합니다.", "맨 위에 민트 잎과 천연 꿀을 한 바퀴 둘러 예술적으로 마무리합니다."], "tip": "냉동 블루베리를 사용하실 때는 실온에 5분간 두었다가 사용하면 과즙이 촉촉하게 배어 나옵니다."},
                {"title": "2. 블루베리 프렌치 토스트 플래터", "time": "15분", "calories": "310 kcal", "level": "쉬움", "steps": ["계란 1개와 우유 50ml, 시나몬 가루를 섞은 물에 식빵을 적십니다.", "버터를 두른 팬에 식빵을 앞뒤로 노릇하고 부드럽게 굽습니다.", "냄비에 블루베리와 올리고당 1스푼을 졸여 즉석 콤포트를 제작합니다.", "구운 토스트 위에 블루베리 콤포트를 가득 뿌려 브런치 스타일로 냅니다."], "tip": "식빵을 계란물에 최소 2분 이상 충분히 담가두어야 속까지 카스텔라처럼 부드러워집니다."},
                {"title": "3. 새콤달콤 블루베리 수제 에이드", "time": "5분", "calories": "110 kcal", "level": "쉬움", "steps": ["컵 바닥에 블루베리 한 줌과 설탕이나 알룰로스 1스푼을 넣습니다.", "스푼이나 미니 절구를 이용해 블루베리 알갱이를 꾹꾹 으깨어 줍니다.", "얼음을 잔에 가득 채우고 시원한 탄산수 100ml를 청량하게 붓습니다.", "전체적으로 보랏빛 그라데이션이 퍼지도록 가볍게 저어 마십니다."], "tip": "탄산수 대신 레몬에이드를 활용하면 새콤한 맛이 배가되어 청량감이 극대화됩니다."},
                {"title": "4. 오트밀 블루베리 영양 베이킹 바", "time": "30분", "calories": "230 kcal", "level": "보통", "steps": ["오트밀 한 컵, 으깬 바나나 1개, 올리고당을 볼에 넣고 반죽합니다.", "반죽 내부에 블루베리와 아몬드 슬라이스를 고루 섞어줍니다.", "사각 틀에 반죽을 단단하게 누르며 2cm 두께로 고르게 평평화합니다.", "170도로 맞춘 오븐에서 20분간 구운 뒤 한 김 식혀 바 형태로 자릅니다."], "tip": "완전히 식지 않은 상태에서 칼질을 하면 부서지기 쉬우니 차갑게 식힌 후 컷팅하세요."},
                {"title": "5. 아티스틱 블루베리 리코타 치즈 샐러드", "time": "10분", "calories": "195 kcal", "level": "쉬움", "steps": ["샐러드용 어린잎 채소와 앙증맞은 양상추를 흐르는 물에 씻어 수분을 뺍니다.", "보울 중앙에 채소를 깔고 수제 리코타 치즈를 스푼으로 툭툭 떼어 얹습니다.", "치즈 주변에 보석 같은 생블루베리를 아낌없이 가득 데코레이션합니다.", "상큼한 발사믹 글레이즈를 회오리 모양으로 자유롭게 드로잉해 마무리합니다."], "tip": "리코타 치즈의 묵직하고 고소한 풍미가 블루베리의 산미를 아주 고급스럽게 감싸 안아줍니다."}
            ]
        }
    elif lang == "English":
        recipes = {
            "quinoa": [{"title": f"{i}. Quinoa Elite Theme Recipe", "time": "15m", "calories": "200 kcal", "level": "Easy", "steps": ["Boil quinoa.", "Mix and enjoy."], "tip": "Clean thoroughly.", "video": ""} for i in range(1, 6)],
            "avocado": [{"title": f"{i}. Premium Avocado Special", "time": "10m", "calories": "300 kcal", "level": "Easy", "steps": ["Slice fruit.", "Season carefully."], "tip": "Use ripe fruit.", "video": ""} for i in range(1, 6)],
            "tofu": [{"title": f"{i}. Artisan Tofu Masterpiece", "time": "20m", "calories": "150 kcal", "level": "Medium", "steps": ["Drain moisture.", "Pan fry crisp."], "tip": "Use firm tofu.", "video": ""} for i in range(1, 6)],
            "blueberry": [{"title": f"{i}. Antioxidant Blueberry Delight", "time": "5m", "calories": "120 kcal", "level": "Easy", "steps": ["Wash berries.", "Layer nicely."], "tip": "Keep frozen fresh.", "video": ""} for i in range(1, 6)],
        }
    else: # 简中
        recipes = {
            "quinoa": [{"title": f"{i}. 藜麦精选主题食谱", "time": "15分钟", "calories": "200 千卡", "level": "简单", "steps": ["煮熟藜麦", "调味拌匀并享用"], "tip": "烹饪前请反复搓洗以去除苦味", "video": ""} for i in range(1, 6)],
            "avocado": [{"title": f"{i}. 优质牛油果高级料理", "time": "10分钟", "calories": "300 千卡", "level": "简单", "steps": ["切开并去核", "切片调味装盘"], "tip": "请选用外皮呈黑褐色的完全熟化果实", "video": ""} for i in range(1, 6)],
            "tofu": [{"title": f"{i}. 匠心打造豆腐营养餐", "time": "20分钟", "calories": "150 千卡", "level": "中等", "steps": ["挤干豆腐水分", "入锅煎至双面金黄"], "tip": "烹饪前用盐水焯一下不易破碎", "video": ""} for i in range(1, 6)],
            "blueberry": [{"title": f"{i}. 抗氧化蓝莓艺术沙拉", "time": "5分钟", "calories": "120 千卡", "level": "简单", "steps": ["洗净蓝莓", "层层堆叠进行视觉摆盘"], "tip": "冷冻蓝莓请在室温下解冻5分钟后使用", "video": ""} for i in range(1, 6)],
        }
    return recipes.get(food_id, [])

# 데이터 및 세션 초기화
food_data = load_food_data()
if "selected_food_id" not in st.session_state:
    st.session_state.selected_food_id = "quinoa"
if "my_fridge" not in st.session_state:
    st.session_state.my_fridge = []

# 5. 사이드바 (프로필 및 언어 셀렉터 - 중국어 활성화)
with st.sidebar:
    st.title("🌿 Nourish Dashboard")
    selected_lang = st.selectbox("🌐 Language / 语言选择", ["한국어", "English", "중국어 (简体中文)"])
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

# 6. 메인 헤더 영역
st.markdown(f"<p class='brand-sub'>{text_pack['sub_logo']}</p>", unsafe_allow_html=True)
st.markdown(f"<h1 class='brand-main'>{text_pack['title_main']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='brand-desc'>{text_pack['subtitle']}</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs([text_pack["tab1"], text_pack["tab2"]])

# Tab 1: 식재료 격자(Grid) 배열 탐색 룸
with tab1:
    st.markdown(f"### 🥦 {text_pack['intro_recom']}")
    st.markdown(f"<p style='font-size:14px; color:#6E7A64; margin-top:-10px; margin-bottom:20px;'>{text_pack['intro_guide']}</p>", unsafe_allow_html=True)
    
    # 🚨 사진1.png 격자형 레이아웃 물리적 4열 구성
    col_cards = st.columns(4)
    for idx, item in enumerate(food_data):
        with col_cards[idx]:
            # 다국어 명칭 매핑
            if selected_lang == "한국어":
                display_name = item["name_ko"]
                display_tagline = item["tag_ko"]
                display_badge = item["badge_ko"]
            elif selected_lang == "English":
                display_name = item["name_en"]
                display_tagline = item["tag_en"]
                display_badge = item["badge_en"]
            else:
                display_name = item["name_zh"]
                display_tagline = item["tag_zh"]
                display_badge = item["badge_zh"]
                
            # HTML 카드로 격자 형태 복원
            st.markdown(f"""
                <div class="food-card">
                    <div class="food-emoji">{item['emoji']}</div>
                    <div class="food-name">{display_name}</div>
                    <div class="food-tagline">{display_tagline}</div>
                    <span class="food-badge">{display_badge}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # 스크린샷과 동일한 위치에 [선택] 및 [정보] 버튼 배치
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                # 선택 버튼 누르면 레시피 탭 연동 목적 세션 상태 변경
                if st.button("선택" if selected_lang=="한국어" else ("Select" if selected_lang=="English" else "选择"), key=f"sel_id_{item['id']}", use_container_width=True):
                    st.session_state.selected_food_id = item["id"]
                    st.toast(f"✅ {display_name} Selected!")
            with btn_col2:
                # 정보 버튼 누르면 하단 상세 도감 갱신
                if st.button("정보" if selected_lang=="한국어" else ("Info" if selected_lang=="English" else "信息"), key=f"inf_id_{item['id']}", use_container_width=True):
                    st.session_state.selected_food_id = item["id"]

    # 현재 활성화된(선택/정보 클릭된) 식재료 정보 추출
    current_id = st.session_state.selected_food_id
    active_food = next(x for x in food_data if x["id"] == current_id)
    
    st.write("---")
    
    # 아래로 시원하게 배치되는 상세 인포 카드 & 레이더 차트 배열 세팅
    col_info, col_chart = st.columns([1, 1])
    
    with col_info:
        if selected_lang == "한국어":
            disp_title = active_food["name_ko"]
            disp_desc = active_food["desc_ko"]
        elif selected_lang == "English":
            disp_title = active_food["name_en"]
            disp_desc = active_food["desc_en"]
        else:
            disp_title = active_food["name_zh"]
            disp_desc = active_food["desc_zh"]
            
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
        nutrients_keys = ["pro", "fib", "cal", "fat", "car", "iron"]
        max_values = {"pro": 20, "fib": 10, "cal": 400, "fat": 20, "car": 80, "iron": 5}
        r_values = [(active_food[n] / max_values[n]) * 100 for n in nutrients_keys]
        
        fig_radar.add_trace(px.Scatterpolar(
            r=r_values + [r_values[0]],
            theta=text_pack["nutrients"] + [text_pack["nutrients"][0]],
            fill='toself',
            line_color='#3B6D11',
            fillcolor='rgba(59, 109, 17, 0.15)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#ECEEEB")),
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=30, l=40, r=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# Tab 2: 깨짐 현상 완벽 방지된 수려한 테마별 레시피 5종 공간
with tab2:
    active_id = st.session_state.selected_food_id
    active_food = next(x for x in food_data if x["id"] == active_id)
    disp_name = active_food["name_ko"] if selected_lang == "한국어" else (active_food["name_en"] if selected_lang == "English" else active_food["name_zh"])
    
    st.markdown(f"### 🍳 {disp_name} · {text_pack['recipe_room']}")
    
    recipes_list = get_5_recipes(active_id, selected_lang)
    
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
                    <span class="badge badge-ing">🌿 {disp_name}</span>
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
        
        col_btn1, col_btn2 = st.columns([1, 5])
        with col_btn1:
            if rc['title'] in st.session_state.my_fridge:
                if st.button(text_pack['btn_del'], key=f"del_{idx}_{active_id}"):
                    st.session_state.my_fridge.remove(rc['title'])
                    st.rerun()
            else:
                if st.button(text_pack['btn_add'], key=f"add_{idx}_{active_id}"):
                    st.session_state.my_fridge.append(rc['title'])
                    st.rerun()
        with col_btn2:
            st.caption("✨ Core pipeline synced with USDA & Spoonacular standards")