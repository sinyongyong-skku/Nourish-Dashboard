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

    /* 백엔드 서식 전용 디자인 카드 (HTML 렌더링 정상화) */
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
        "doc_