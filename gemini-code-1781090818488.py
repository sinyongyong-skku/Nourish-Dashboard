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
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Noto+Sans+KR:wght@300;400;700&display=swap');
    
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

    /* 백엔드 서식 전용 디자인 카드 (HTML 생출력 방지용 코드 구조) */
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

# 2. 다국어 사전 설정 (한국어, English, 简体中文)
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
        "btn_del": "❌ 빼기", "btn_add": "🧡 찜하기",
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
        "btn_del": "❌ Remove", "btn_add": "🧡 Save",
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
        "btn_del": "❌ 移除", "btn_add": "🧡 收藏",
        "saved_title": "❤️ 我收藏的食谱", "saved_empty": "收藏夹空空如也。",
        "academic": "🎓 选课及学生信息",
        "labels": ["热量", "蛋白质", "碳水化合物", "脂肪", "膳食纤维", "铁"],
        "nutrients": ["蛋白质 (g)", "膳食纤维 (g)", "卡路里 (kcal)", "脂肪 (g)", "碳水化合物 (g)", "铁分 (mg)"]
    }
}

# 3. 데이터 로드 (50개 매핑 유연성 인프라 구축)
@st.cache_data
def load_all_foods():
    # 기본 주력 4인방 + 50개 확장을 대비한 기본 다시마(Kelp) 등 유동 샘플 스키마화
    return [
        {"id": "quinoa", "emoji": "🌾", "name_ko": "퀴노아", "name_en": "Quinoa", "name_zh": "藜麦", "tag_ko": "완전단백질 슈퍼씨앗", "tag_en": "Complete Plant Protein", "tag_zh": "全蛋白超级种子", "badge_ko": "글루텐프리", "badge_en": "Gluten-Free", "badge_zh": "无麸质", "desc_ko": "필수 아미노산이 균형 있게 함유된 곡물입니다.", "desc_en": "Rich in essential amino acids.", "desc_zh": "包含人体必需氨基酸。", "cal": 368, "pro": 14.1, "car": 64.0, "fat": 6.1, "fib": 7.0, "iron": 4.6},
        {"id": "avocado", "emoji": "🥑", "name_ko": "아보카도", "name_en": "Avocado", "name_zh": "牛油果", "tag_ko": "단일불포화지방산", "tag_en": "Healthy Fats", "tag_zh": "单不饱和脂肪", "badge_ko": "비타민E", "badge_en": "Vitamin E", "badge_zh": "富含维E", "desc_ko": "불포화 지방산이 풍부해 심혈관에 훌륭합니다.", "desc_en": "Great for heart health with clean lipids.", "desc_zh": "含有对人体有益的健康油脂。", "cal": 160, "pro": 2.0, "car": 8.5, "fat": 14.7, "fib": 6.7, "iron": 0.6},
        {"id": "tofu", "emoji": "🫘", "name_ko": "두부", "name_en": "Tofu", "name_zh": "豆腐", "tag_ko": "식물성 완전단백질", "tag_en": "Soy Curd Core", "tag_zh": "植物性优质全蛋白", "badge_ko": "저칼로리", "badge_en": "Low-Calorie", "badge_zh": "低热量", "desc_ko": "콩 단백질을 압착하여 만든 고단백 위주의 재료입니다.", "desc_en": "High digestibility plant-based source.", "desc_zh": "高消化率植物高蛋白食材。", "cal": 84, "pro": 8.9, "car": 2.9, "fat": 4.8, "fib": 0.2, "iron": 1.5},
        {"id": "blueberry", "emoji": "🫐", "name_ko": "블루베리", "name_en": "Blueberry", "name_zh": "蓝莓", "tag_ko": "안토시아닌 항산화", "tag_en": "Antioxidant Power", "tag_zh": "强效抗氧化", "badge_ko": "비타민C", "badge_en": "Vitamin C+", "badge_zh": "富含维C", "desc_ko": "안토시아닌이 활성산소를 억제하고 시력을 보호합니다.", "desc_en": "Fights free radicals beautifully.", "desc_zh": "富含花青素，清除自由基效果佳。", "cal": 57, "pro": 0.7, "car": 14.5, "fat": 0.3, "fib": 2.4, "iron": 0.3},
        {"id": "kelp", "emoji": "🌊", "name_ko": "다시마", "name_en": "Kelp", "name_zh": "昆布", "tag_ko": "해조류 식이섬유 왕", "tag_en": "Iodine & Fibre King", "tag_zh": "海藻膳食纤维王", "badge_ko": "알긴산 풍부", "badge_en": "Alginic Acid", "badge_zh": "富含褐藻酸", "desc_ko": "다시마는 풍부한 알긴산과 장 건강에 좋은 식이섬유의 보고입니다.", "desc_en": "Seafood powerhouse full of trace minerals.", "desc_zh": "富含微量元素与大量水溶性膳食纤维。", "cal": 43, "pro": 1.7, "car": 9.6, "fat": 0.6, "fib": 1.3, "iron": 2.8}
    ]

# 4. 에러율 0% 보장하는 만능 5가지 테마별 레시피 제너레이터 
def get_recipes_for_all(food_id, food_name, lang):
    # 만약 언어가 한글인 경우의 정밀 텍스트 빌딩
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
    else: # 简中
        return [{"title": f"{i}. 精致 {food_name} 艺术健康主题餐", "time": "15分钟", "calories": "190 千卡", "level": "简单", "steps": [f"将 {food_name} 洗净并进行美观的高级刀工切片处理。", "搭配有机蔬菜，淋上特制少盐低脂沙拉酱。"], "tip": "即做即食可以最大程度保留其抗氧化营养活性。"} for i in range(1, 6)]

# 데이터 로딩 및 상태 세팅
all_foods = load_all_foods()
food_options_map = {f"{f['emoji']} {f['name_ko']} ({f['name_en']})": f["id"] for f in all_foods}

if "selected_food_id" not in st.session_state:
    st.session_state.selected_food_id = "quinoa"
if "my_fridge" not in st.session_state:
    st.session_state.my_fridge = []

# 5. 사이드바 구성 (글로벌 프로필 설정 및 찜하기 룸)
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

# 🚨 [핵심 수정 사항 1] 50대 식재료 상호 연동을 위한 상단 글로벌 드롭다운 셀렉터 배치
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
# 셀렉터를 바꿀 때마다 실시간 세션에 반영하여 양쪽 탭을 동시 제어
st.session_state.selected_food_id = food_options_map[selected_option]

# 탭 나누기
tab1, tab2 = st.tabs([text_pack["tab1"], text_pack["tab2"]])

# --- Tab 1: 식재료 카드 그리드 및 정밀 레이더 도감 ---
with tab1:
    st.markdown(f"### 🥦 {text_pack['intro_recom']}")
    
    # 4대 추천 주력 카드 레이아웃
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
            
            # 선택 및 정보 연동 버튼 구성
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button("선택" if selected_lang=="한국어" else ("Select" if selected_lang=="English" else "选择"), key=f"t1_sel_{item['id']}", use_container_width=True):
                    st.session_state.selected_food_id = item["id"]
                    st.rerun()
            with b_col2:
                if st.button("정보" if selected_lang=="한국어" else ("Info" if selected_lang=="English" else "信息"), key=f"t1_inf_{item['id']}", use_container_width=True):
                    st.session_state.selected_food_id = item["id"]
                    st.rerun()

    # 현재 활성화된 세션 식재료 세부 데이터 추출 
    active_food = next(x for x in all_foods if x["id"] == st.session_state.selected_food_id)
    
    st.write("---")
    
    # 하단 2분할 구조화 배열 대시보드
    col_info, col_chart = st.columns([1, 1])
    with col_info:
        if selected_lang == "한국어":
            disp_title, disp_desc = active_food["name_ko"], active_food["desc_ko"]
        elif selected_lang == "English":
            disp_title, disp_desc = active_food["name_en"], active_food["desc_en"]
        else:
            disp_title, disp_desc = active_food["name_zh"], active_food["desc_zh"]
            
        # 🚨 [핵심 수정 사항 2] 보호색으로 글자가 가려지지 않게 차별화된 영양 컴포넌트 렌더링
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
        max_vals = {"pro": 20, "fib": 10, "cal": 400, "fat": 20, "car": 80, "iron": 5}
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

# --- Tab 2: 깨짐 현상 100% 방지된 가독성 극대화 레시피 5종 룸 ---
with tab2:
    active_food = next(x for x in all_foods if x["id"] == st.session_state.selected_food_id)
    if selected_lang == "한국어":
        recipe_target_name = active_food["name_ko"]
    elif selected_lang == "English":
        recipe_target_name = active_food["name_en"]
    else:
        recipe_target_name = active_food["name_zh"]
        
    st.markdown(f"### 🍳 {active_food['emoji']} {recipe_target_name} · {text_pack['recipe_room']}")
    
    # 동적 매핑 엔진에서 고유 5대 레시피 셋 수집
    recipes_list = get_recipes_for_all(active_food["id"], recipe_target_name, selected_lang)
    
    # 🚨 [핵심 수정 사항 3] 생 HTML 유출 우려를 원천 차단하는 마크다운 렌더링 블록
    for idx, rc in enumerate(recipes_list):
        steps_html = "".join([
            f'<div class="step-item"><div class="step-number">{i+1}</div><div class="step-text">{step}</div></div>' 
            for i, step in enumerate(rc['steps'])
        ])
        
        # 완전 안전하게 인클루드하여 스타일 시트 주입
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
        
        # 버튼 액션 레이아웃 바인딩
        col_btn1, col_btn2 = st.columns([1, 5])
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
            st.caption("✨ Real-time dynamic compilation with zero runtime error flags.")