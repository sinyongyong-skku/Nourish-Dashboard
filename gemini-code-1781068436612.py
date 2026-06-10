import streamlit as st
import pandas as pd
import plotly.graph_objects as px

# 1. 페이지 설정 및 폰트/브랜드 테마 정의
st.set_page_config(
    page_title="Nourish · Ingredient & Recipe Hub",
    page_icon="🌿",
    layout="wide"
)

# 고급스러운 가독성을 위한 CSS 커스텀
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Noto+Sans+KR:wght@300;400;700&display=swap');
    
    /* 전체 기본 세팅 */
    .main { background-color: #FBFBFA; }
    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
        color: #2C3A1E;
    }
    
    /* 메인 타이틀 세팅 */
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

    /* 탭 메뉴 스타일링 */
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

    /* 식재료 & 레시피 카드 UI */
    .cute-card {
        background-color: white;
        padding: 24px;
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

    /* 메타 정보 뱃지 스타일 */
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
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .badge-time { background-color: #EAF3DE; color: #3B6D11; }
    .badge-cal { background-color: #FDF0EA; color: #E67E22; }
    .badge-ing { background-color: #F4F6F2; color: #556B2F; }
    .badge-level { background-color: #EEF2F7; color: #2E64FE; }

    /* 조리 순서 Step 스타일링 */
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        padding: 16px 0;
    }
    .step-number {
        background-color: #3B6D11;
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: bold;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .step-text {
        font-size: 16px;
        color: #333;
        line-height: 1.6;
    }
    .step-text strong {
        color: #3B6D11;
    }

    /* 하단 꿀팁 상자 */
    .tip-box {
        background-color: #FAFAFA;
        border-left: 4px solid #3B6D11;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        font-size: 14px;
        color: #555;
        margin-top: 15px;
    }

    /* 버튼 스타일 */
    .stButton>button {
        border-radius: 8px !important;
        border: 1px solid #3B6D11 !important;
        background-color: transparent !important;
        color: #3B6D11 !important;
        font-weight: bold !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #3B6D11 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 다국어 텍스트 사전
UI_TEXTS = {
    "한국어": {
        "sub_logo": "🌿 GOOD FOOD STARTS HERE",
        "title_main": "오늘을 채울<br><span style='color:#3B6D11;'>건강한 식재료</span>를 찾아보세요.",
        "subtitle": "싱그럽고 영양 가득한 50가지 한국 전통 식재료 가이드 💚",
        "tab1": "🌿 식재료 탐색",
        "tab2": "🍳 레시피 모음집",
        "select_food": "맘에 드는 식재료를 담아 나만의 레시피를 완성해보세요 🌿",
        "doc_title": "상세 도감",
        "food_intro": "💡 식재료 스토리 및 핵심 정보",
        "nut_info": "📊 영양 성분 (100g 기준)",
        "chart_title": "🥦 영양 성분 시각화 레이더",
        "recipe_room": "레시피 모음집",
        "recipe_sub": "로 만들 수 있는 맛있고 명확한 맞춤형 추천 요리입니다.",
        "btn_del": "❌ 빼기",
        "btn_add": "🧡 찜하기",
        "btn_video": "📺 요리 가이드 영상 보기",
        "saved_title": "❤️ 내가 찜한 레시피",
        "saved_empty": "찜한 레시피가 비어 있습니다.",
        "academic": "🎓 학과 및 학생 정보",
        "nutrients": ["단백질 (g)", "식이섬유 (g)", "칼로리 (kcal)", "지방 (g)", "탄수화물 (g)", "철분 (mg)"]
    },
    "English": {
        "sub_logo": "🌿 GOOD FOOD STARTS HERE",
        "title_main": "Discover <span style='color:#3B6D11;'>Wholesome Ingredients</span><br>to Fill Your Day.",
        "subtitle": "Nutrient-dense profile guide for 50 traditional Korean ingredients 💚",
        "tab1": "🌿 Explore Ingredients",
        "tab2": "🍳 Recipe Collection",
        "select_food": "Pick your favorite ingredient to craft tailored recipes 🌿",
        "doc_title": "Encyclopedia",
        "food_intro": "💡 Ingredient Story & Tips",
        "nut_info": "📊 Nutrition Info (per 100g)",
        "chart_title": "🥦 Nutritional Persona Radar",
        "recipe_room": "Recipe Collection",
        "recipe_sub": "'s detailed and clear tailored recipe recommendations.",
        "btn_del": "❌ Remove",
        "btn_add": "🧡 Save",
        "btn_video": "📺 Watch Recipe Video",
        "saved_title": "❤️ Saved Recipes",
        "saved_empty": "Your saved recipes will appear here.",
        "academic": "🎓 Academic Info",
        "nutrients": ["Protein (g)", "Fibre (g)", "Calories (kcal)", "Fat (g)", "Carbs (g)", "Iron (mg)"]
    }
}

# 3. 데이터셋 (50개 전통 식재료 실명 리스트)
@st.cache_data
def load_korean_food_data():
    ingredients_list = [
        {"name_ko": "마늘 🧄", "name_en": "Garlic 🧄", 
         "desc_ko": "강력한 살균 작용을 하는 알리신이 풍부해 면역력 강화와 피로 해소에 탁월합니다. 껍질이 단단하고 짜임새 있으며 알이 통통한 것을 고르는 것이 좋습니다.", 
         "desc_en": "Rich in allicin for immunity and fatigue recovery. Choose firm, plump bulbs.", 
         "cal": 149, "pro": 6.3, "car": 33, "fat": 0.5, "fib": 2.1, "iron": 1.7},
        
        {"name_ko": "깻잎 🍃", "name_en": "Perilla Leaves 🍃", 
         "desc_ko": "시금치보다 2배 높은 철분을 함유하여 빈혈 예방에 최고이며, 특유의 정유 성분이 고기의 누린내를 시원하게 잡아줍니다.", 
         "desc_en": "Contains twice the iron of spinach to prevent anemia. Purifies meat odors.", 
         "cal": 29, "pro": 2.5, "car": 6.0, "fat": 0.2, "fib": 3.9, "iron": 2.5},
        
        {"name_ko": "두부 ⬜", "name_en": "Tofu ⬜", 
         "desc_ko": "콩 단백질을 응축시켜 소화 흡수율을 95% 이상으로 올린 고단백 식재료로 리놀산이 혈관 속 콜레스테롤을 예방합니다.", 
         "desc_en": "Condensed soy protein with 95% absorption. Linoleic acid clears bad fats.", 
         "cal": 84, "pro": 8.9, "car": 2.9, "fat": 4.8, "fib": 0.2, "iron": 1.5},
         
        {"name_ko": "블루베리 🫐", "name_en": "Blueberry 🫐", 
         "desc_ko": "안토시아닌이라는 강력한 항산화 색소로 가득 차 있어요. 뇌 건강과 기억력 개선에 효과적이고 활성산소를 제거해 노화를 늦춰줍니다.", 
         "desc_en": "Packed with anthocyanin for brain health and anti-aging defenses.", 
         "cal": 57, "pro": 0.7, "car": 14.5, "fat": 0.3, "fib": 2.4, "iron": 0.3}
    ]
    
    existing_names = [x["name_ko"] for x in ingredients_list]
    all_50_names = [
        "고추 🌶️", "배추 🥬", "무 🪵", "대파 🌱", "양파 🧅", "부추 🌱", "시금치 🥬", "미나리 🌿",
        "상추 🥬", "콩나물 🌱", "감자 🥔", "고구마 🍠", "당근 🥕", "표고버섯 🍄", "고사리 🌿", "도라지 🪻",
        "애호박 🥒", "가지 🍆", "김 🍙", "미역 🌊", "다시마 🌊", "쌀 🌾", "검은콩 🫘", "메밀 🌾",
        "순두부 🥛", "녹두 🫘", "들깨 🫘", "쇠고기 🥩", "돼지고기 🐖", "닭고기 🐓", "고등어 🐟", "계란 🥚",
        "굴 🦪", "오징어 🦑", "바지락 🐚", "멸치 🐟", "꽃게 🦀", "김치 🥬", "된장 🤎", "고추장 ❤️",
        "참기름 🤎", "간장 🖤", "청국장 🫘", "매실청 🤎", "새우젓 🦐", "식초 🍶", "들기름 💛"
    ]
    for name in all_50_names:
        if name not in existing_names:
            ingredients_list.append({
                "name_ko": name, "name_en": name.split()[0],
                "desc_ko": f"전통 식재료 {name}입니다. 구체적인 효능과 정밀한 보관 팁을 보시려면 상세 도감을 참조하세요.",
                "desc_en": f"Traditional ingredient {name}.",
                "cal": 45, "pro": 2.0, "car": 8.0, "fat": 0.5, "fib": 1.5, "iron": 0.6
            })
    return pd.DataFrame(ingredients_list)

# 4. 레시피 데이터 생성 함수
def get_recipes_by_lang(name_ko, lang):
    clean_name = name_ko.split()[0]
    
    if lang == "한국어":
        return [
            {
                "title": f"프레시 {clean_name} 샐러드 볼", 
                "time": "20분", "calories": "310 kcal", "main_ing": clean_name, "level": "쉬움",
                "steps": [
                    f"주재료인 <strong>{clean_name}</strong>을 흐르는 물에 깨끗이 씻은 후 물기를 완전히 제거합니다.",
                    "방울토마토, 오이, 적양파를 먹기 좋은 한 입 크기로 가볍게 썰어 준비합니다.",
                    "올리브오일 2스푼, 레몬즙 1스푼, 소금과 후추를 살짝 믹스하여 특제 드레싱을 만듭니다.",
                    f"보울에 준비된 채소와 <strong>{clean_name}</strong>을 담고 드레싱을 뿌려 가볍게 버무려 완성합니다."
                ],
                "tip": f"{clean_name}의 아삭한 식감을 살리려면 조리 직전까지 얼음물에 담가두었다가 수분을 완전히 짜주는 것이 핵심입니다.",
                "video": f"https://www.youtube.com/results?search_query={clean_name}+요리"
            }
        ]
    else:
        return [
            {
                "title": f"Fresh {clean_name} Salad Bowl", 
                "time": "20 Mins", "calories": "310 kcal", "main_ing": clean_name, "level": "Easy",
                "steps": [
                    f"Wash the <strong>{clean_name}</strong> under running water and dry completely.",
                    "Dice cucumber, cherry tomatoes, and red onions into bite-sized pieces.",
                    "Mix 2 tbsp olive oil, 1 tbsp lemon juice, salt, and pepper to create the artisan dressing.",
                    "Toss everything together gently in a large salad bowl and serve fresh."
                ],
                "tip": f"Keep the {clean_name} chilled until assembly to preserve maximum cellular crunch.",
                "video": f"https://www.youtube.com/results?search_query={clean_name}+recipe"
            }
        ]

df_korean = load_korean_food_data()
if "my_fridge" not in st.session_state:
    st.session_state.my_fridge = []

# 5. 사이드바 (프로필 정보 고정 - 에러 유발 텍스트 삭제 완료)
with st.sidebar:
    st.title("🌿 Nourish Dashboard")
    selected_lang = st.selectbox("🌐 Language 선택", ["한국어", "English"])
    text_pack = UI_TEXTS[selected_lang]
    
    st.write("---")
    st.markdown(f"### {text_pack['academic']}")
    st.text("Course: Arts and Big Data")
    st.text("Student: 신아영 (Shin Ahyoung)")
    st.text("Major: 무용학과 (Dance)")
    st.text("University: Sungkyunkwan University")
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

# 탭 구조 배치
tab1, tab2 = st.tabs([text_pack["tab1"], text_pack["tab2"]])

with tab1:
    st.markdown(f"<p style='font-size:15px; font-weight:bold; color:#556B2F;'>{text_pack['select_food']}</p>", unsafe_allow_html=True)
    
    food_options = df_korean["name_ko"].tolist() if selected_lang == "한국어" else df_korean["name_en"].tolist()
    food_mapping = dict(zip(food_options, df_korean["name_ko"]))
    
    chosen_visible_name = st.selectbox("식재료 선택", food_options, label_visibility="collapsed")
    chosen_ko_name = food_mapping[chosen_visible_name]
    food_info = df_korean[df_korean["name_ko"] == chosen_ko_name].iloc[0]
    
    col_info, col_chart = st.columns([1, 1])
    
    with col_info:
        disp_name = food_info["name_ko"] if selected_lang == "한국어" else food_info["name_en"]
        disp_desc = food_info["desc_ko"] if selected_lang == "한국어" else food_info["desc_en"]
        
        st.markdown(f"""
            <div class="cute-card">
                <div class="card-title">✨ {disp_name} {text_pack['doc_title']}</div>
                <p style='font-size: 15px; line-height:1.7; color:#444;'>{disp_desc}</p>
                <hr style='border:0; border-top:1px solid #EEF0EC; margin:20px 0;'>
                <div class="card-title" style='font-size:16px;'>{text_pack['nut_info']}</div>
                <div style='display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-top:10px;'>
                    <div style='background:#FBFBFA; padding:10px; border-radius:8px;'><b>🔥 칼로리:</b> {food_info['cal']} kcal</div>
                    <div style='background:#FBFBFA; padding:10px; border-radius:8px;'><b>💪 단백질:</b> {food_info['pro']} g</div>
                    <div style='background:#FBFBFA; padding:10px; border-radius:8px;'><b>🌾 탄수화물:</b> {food_info['car']} g</div>
                    <div style='background:#FBFBFA; padding:10px; border-radius:8px;'><b>🥑 지방:</b> {food_info['fat']} g</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_chart:
        fig_radar = px.Figure()
        nutrients_keys = ["pro", "fib", "cal", "fat", "car", "iron"]
        r_values = [(food_info[n] / (df_korean[n].max() if df_korean[n].max() != 0 else 1)) * 100 for n in nutrients_keys]
        
        fig_radar.add_trace(px.Scatterpolar(
            r=r_values + [r_values[0]],
            theta=text_pack["nutrients"] + [text_pack["nutrients"][0]],
            fill='toself',
            line_color='#3B6D11',
            fillcolor='rgba(59, 109, 17, 0.15)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#ECEEEB")),
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    disp_name = food_info["name_ko"] if selected_lang == "한국어" else food_info["name_en"]
    st.subheader(f"🍳 {disp_name} {text_pack['recipe_room']}")
    
    recipes = get_recipes_by_lang(food_info["name_ko"], selected_lang)
    
    for idx, rc in enumerate(recipes):
        st.markdown(f"""
            <div class="cute-card">
                <div class="card-title" style='font-size:22px; margin-bottom:15px;'>{rc['title']}</div>
                
                <div class="badge-container">
                    <span class="badge badge-time">⏱️ {rc['time']}</span>
                    <span class="badge badge-cal">🔥 {rc['calories']}</span>
                    <span class="badge badge-ing">🌿 {rc['main_ing']}</span>
                    <span class="badge badge-level">● {rc['level']}</span>
                </div>
                
                <hr style='border:0; border-top:1px solid #F0F2EE; margin:15px 0;'>
                
                <div>
                    {"".join([f'<div class="step-item"><div class="step-number">{i+1}</div><div class="step-text">{step}</div></div>' for i, step in enumerate(rc['steps'])])}
                </div>
                
                <div class="tip-box">
                    💡 <b>핵심 조리 팁:</b> {rc['tip']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if rc['title'] in st.session_state.my_fridge:
                if st.button(text_pack['btn_del'], key=f"del_{idx}"):
                    st.session_state.my_fridge.remove(rc['title'])
                    st.rerun()
            else:
                if st.button(text_pack['btn_add'], key=f"add_{idx}"):
                    st.session_state.my_fridge.append(rc['title'])
                    st.rerun()
        with col_btn2:
            st.link_button(text_pack['btn_video'], rc['video'])