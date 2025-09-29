import streamlit as st
# from auth import login
import auth
import base64
from streamlit_option_menu import option_menu

nav_items = ["Home","Login","Account"]

nav_css = {"container":{"padding":"5px","background-color":"#323232fc","border-radius": "8px","transition": "background-color 0.2s"}
           ,"nav-link": {"color": "white", "font-size": "18px", "--hover-color": "#444"}
           ,"nav-link-selected": {"background-color": "#024979", "color": "#fff"}
           }

selected_nav = option_menu(menu_title=None,
                           options=nav_items,
                           icons=["house","arrow-up-circle","person"],
                           default_index=1,
                           orientation="horizontal",
                           styles=nav_css,
                           key="nav_bar"
                        )



def set_background_image(image_path: str) -> None:
    """Set a background image for the Streamlit app using base64 encoding."""
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    page_css = f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                position: relative;
                background-image: url("data:image/jpg;base64,{encoded_image}");
                background-position: center;
                background-size: cover;
            }}
            [class="st-emotion-cache-scp8yw e3g0k5y6"] {{
                display: none;
            }}
            [data-testid="stHeader"] {{
                background-color: rgba(0, 0, 0, 0);
            }}
            .header {{
                position: fixed;
                top: 0;
                left: 0;
                height: 80px;
                width: 100vw;
                background-color: #121212bf;
                z-index: 100;
                padding: 0 20px;
            }}
            .top-title{{
                text-align:center;
                font-size: 42px;
                font-weight: 800;
                color: #69a5cc;
                font-family: 'Inter', sans-serif;
                letter-spacing: -2px;
                text-shadow:8px 4px 0 black;
            }}
            .hero-title {{
                text-align: center;
                background-color: #c7c6c6d4; 
                color : black;
                border: 4px solid black; 
                border-radius: 20px; 
                padding: 40px 80px;
                overflow: hidden;
                z-index: 1;
                font-weight: 700;
            }}
            .account{{
                text-align:center;
                background-color: #c7c6c6d4; 
                color:black;
                border-radius: 20px; 
            }}
        </style>
    """
    st.markdown(page_css, unsafe_allow_html=True)


# Set the app background
set_background_image("./img/bg-img.png")

st.markdown("<div class='header'><div class='top-title'>Toonify</div></div>", unsafe_allow_html=True)


# Initialize session states if not present
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None


# Main view: Welcome and hero section with login/signup buttons
def show_home():
        st.markdown(
            """
            <div class='hero-title'>
                <h1 style="color:#026cb2; border-bottom:3px solid #026cb2; padding-bottom:4px">Welcome In Toonify</h1>
                <p style="margin-top:10px">Turn your photos into artwork, sketches, and cartoons with a click – 
                the most simple, beautiful, and no-nonsense cartoonizer and photo editor for all.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.session_state.current_user != None:
            image = st.file_uploader("Upload Image:", type=['jpg','png','jpeg'])
            if image:
                st.image(image)
        else :
            pass

def show_account():
    if st.session_state.current_user == None:
        st.markdown(
                """
                <div class='account'>
                    <h1>You've not logged in Yet</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
                """
                <style>
                    [data-testid="stHeadingWithActionElements"] h3{
                      text-align:center;
                      background-color: #c7c6c6d4; 
                      margin-top:12px;
                      color:black;
                      border-radius: 20px;   
                    }
                    [data-testid="stBaseButton-secondary"]{
                        margin: 24px 0 0 140px;
                        color:black;
                        border-radius: 12px; /* rounded pill shape */
                        background-color:#c7c6c6d4;
                        width:400px;
                        border: 3px solid black;
                        cursor: pointer;
                        transition: background-color 0.3s, color 0.3s;
                    }
                    [data-testid="stBaseButton-secondary"]:hover{
                        color:white;
                    }
                    [data-testid="stBaseButton-secondary"] p{
                        font-weight: 600;
                        font-size:24px;
                    }
                </style>
                <div class='account'>
                    <h1>Account Section</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.subheader("""Logged In As""")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Name:")
            st.subheader("Email:")
        with col2:
            st.subheader(f"{st.session_state.current_user["username"]}")
            email = st.session_state.current_user["email"].replace("@", "@ ").replace(".", ". ")
            st.subheader(email)
        if st.button("Log Out", on_click=auth.logout_user):
            st.session_state.current_user = None
        
        
if selected_nav == "Home":
    show_home()
elif selected_nav == "Login":
   if st.session_state.show_signup == False:
       st.session_state.show_login = True
       st.session_state.show_signup = False
       auth.login()     
   else :
       st.session_state.show_login = False
       auth.signup()
        
elif selected_nav == "Account":
    pass
    # show account or signup logic here as needed
    if st.session_state.current_user == None:
            show_account()
            
    else:
       if st.session_state.current_user:
            show_account()
            
    


