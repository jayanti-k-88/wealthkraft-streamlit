import streamlit as st
from streamlit_option_menu import option_menu
from savings_flow import savings_goal_page
from insurance_form import insurance_form_page
from investment_content import investment_page
from chat_utils import handle_chat
from PIL import Image

# Set up the page configuration
st.set_page_config(page_title="WealthKraft FinTech", layout="wide")

# Custom styles
st.markdown("""
    <style>
        .title-font { font-size: 42px; font-weight: bold; margin-top: 0.5rem; }
        .highlight { color: #00BFFF; }
        .subtitle { font-size: 18px; color: #4f4f4f; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# Load the image
#logo = Image.open("WealthKraft_Logo.jpg")

# Create a two-column layout for logo and title
#col1, col2 = st.columns([1, 6])
#with col1:
#    st.image(logo, width=150)
#with col2:
# Title and greeting
st.markdown('<div class="title-font" align="center">Welcome to <span class="highlight">W</span>ealth<span class="highlight">K</span>raft FinTech</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle" align="center">Crafting intelligent personalized wealth strategies for you</div>', unsafe_allow_html=True)

st.markdown("### 👋 Hi, I am **Finnie**, your personal finance advisor")
st.markdown("##### Explore our range of products and services by clicking on the menu options below.")

# Navigation menu
selected = option_menu(
    menu_title=None,
    options=["Savings Goals", "Investment Portfolio Optimization", "Insurance Recommendation", "Ask me Anything"],
    icons=["piggy-bank", "graph-up", "shield-check", "question-circle"],
    orientation="horizontal",
    default_index=0
)

# Track last selected menu to detect change and trigger refresh
if "last_selected" not in st.session_state:
    st.session_state.last_selected = selected
elif st.session_state.last_selected != selected:
    st.session_state.last_selected = selected
    st.rerun()  # Force a refresh when switching menus

# Route based on selection
if selected == "Savings Goals":
    savings_goal_page()
elif selected == "Insurance Recommendation":
    insurance_form_page()
elif selected == "Investment Portfolio Optimization":
    investment_page()
elif selected == "Ask me Anything":
    st.subheader("🤔 Have questions? Ask me anything !")
    st.markdown("Need Help With Your Personal Finances? I'm Here For You! Whether you're trying to budget smarter, save more, invest wisely, or just make sense of your monthly expenses, you've come to the right place. Ask me anything about personal finance — from managing debt and planning for retirement to understanding credit scores, cutting unnecessary costs, or making the most of your income.")

# Chat at the bottom
handle_chat()
