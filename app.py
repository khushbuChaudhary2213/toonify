import streamlit as st
import auth
import base64
import tempfile
import toon
from streamlit_option_menu import option_menu


####### BACKGROUND IMAGE ######
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
                border: 4px solid black; 
                border-radius: 20px; 
                padding: 40px 80px;
                overflow: hidden;
                z-index: 1;
            }}
            .hero-title h1{{
                margin-bottom:20px;
                
            }}
            .hero-title span{{
                color: black;
                font-weight:300px;
                margin-top:12px;
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


##### Initialize session states if not present #####
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None



#### Main view: Welcome and hero section#####
def show_home():
        st.markdown("""
                    <style>
                        [data-testid="stFileUploader"]{
                            # height:280px;
                            background-color: #c7c6c6d4;
                            border-radius: 22px;
                            border: 4px solid black; 
                            padding: 22px;
                            margin-bottom: 18px;
                            transition: box-shadow 0.2s;
                            margin-top:12px;    
                        }
                        
                        [data-testid="stFileUploaderFileName"],[class="st-emotion-cache-c8ta4l e1w49r0d0"]{
                            color:#212121;
                            font-weight:bold;
                        }
                        [class="st-emotion-cache-c8ta4l e1w49r0d0"]{
                            color:#212121;
                            font-weight:bold;
                        }
                        [data-testid="stWidgetLabel"] p{
                            color:#212121;
                            font-size:18px;
                            font-weight:bold;
                        }
                        [data-testid="stSelectbox"]{
                            background-color: #c7c6c6d4;
                            border-radius: 22px;
                            border-bottom:None;
                            border: 4px solid black; 
                            padding: 22px;
                            margin-top:12px;    
                        }
                        [data-testid="stElementContainer"] [data-testid="stButton"]{
                            width:342px;
                            border-top:none;
                            border: 4px solid black; 
                            border-radius: 22px;
                            padding:22px;
                            background-color:#c7c6c6d4;
                            transition:all 0.2s ease-in-out;
                        }
                        [data-testid="stBaseButton-secondary"]:hover{
                            background: #024979;
                            color:white;
                            border:1px solid black;   
                        }
                        [data-testid="stElementContainer"] [data-testid="stMarkdown"] p{
                            background-color:#c7c6c6d4;
                            color:#212121;
                            padding:16px;
                            border-radius:22px;
                            font-size:18px;
                            font-weight:bold;
                            
                        }
                        [data-testid="stHeadingWithActionElements"] h6{
                            color:black;
                                margin-top: 20px;
                                font-size: 22px;
                                border: 2px solid #1764a6;
                                padding: 10px;
                        }
                        [data-testid="stImageContainer"] img{
                            margin-top:20px;
                        }
                    </style>
                    """,unsafe_allow_html=True)
        st.markdown(
            """
            <div class='hero-title'>
                <h1 style="color:#026cb2; border-bottom:3px solid #026cb2; padding-bottom:4px">Welcome In Toonify</h1>
                <span>Turn your photos into artwork, sketches, and cartoons with a click – the most simple, beautiful, and no-nonsense cartoonizer and photo editor for all. This project empowers everyone to transform ordinary photos into extraordinary cartoon masterpieces and unique art styles, all in seconds.</span>
                <h6>In one click you can generate your toonified image,but you need to login first</h6>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.session_state.current_user == None:
            col1, col2 = st.columns(2)
            with col1:
                st.image("./img/person-1.png",caption="Original")
            with col2:
                st.image("./img/cartoon_Classic Cartoon.png",caption="Classic Cartoon")
        
        styles ={"Pencil Sketch","Colored Sketch","Classic Cartoon","Oil Painting","Udnie Style Cartoon","Mosaic Style Cartoon","Candy Style Cartoon","Disney Cartoon"}
        
        if st.session_state.current_user != None:
            col1, col2 = st.columns(2)
            with col1:
                image = st.file_uploader("Upload Image:", type=['jpg','png','jpeg'])

            if image:
                with col2:
                    options = list(styles) 
                    style_choice = st.selectbox("Choose a cartoon style:", options)
                    st.write("Click on button to generate image:")
                    generate_btn = st.button("Generate")
            
                if generate_btn and image:
                    # Add the spinner here
                    with st.spinner("Generating image..."):
                        # Write the image to a temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                            tmp_file.write(image.getbuffer())
                            temp_image_path = tmp_file.name
                            
                        if style_choice == 'None':
                            pass 
                        if style_choice == "Pencil Sketch":
                            toon.pencilSketch(temp_image_path)
                        if style_choice == "Oil Painting":
                            toon.oilPainting(temp_image_path)
                        if style_choice == "Colored Sketch":
                            toon.coloredSketch(temp_image_path)
                        if style_choice == "Classic Cartoon":
                            toon.classic_cartoon(temp_image_path)
                        if style_choice == "Udnie Style Cartoon":
                            toon.cartoon_neural_style(temp_image_path, "models/udnie.pth")
                        if style_choice == "Mosaic Style Cartoon":
                            toon.cartoon_neural_style(temp_image_path, "models/mosaic.pth")
                        # if style_choice == "RainPrincess Style Cartoon":
                        #     cartoon.cartoon_neural_style(temp_image_path, "models/rain_princess.pth")
                        if style_choice == "Disney Cartoon":
                            toon.disney_cartoon(temp_image_path)
                        if style_choice == "Candy Style Cartoon":
                            toon.cartoon_neural_style(temp_image_path, "models/candy.pth")
                        else:
                            pass
        else :
            pass

##### ACCOUNT SECTION ####
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
                    [data-testid="stLayoutWrapper"]{
                        margin-top:18px;
                        background-color:#c7c6c6d4;
                        color:black;
                        border-radius: 12px;
                        text-align:center;
                        padding:12px;
                    }
                    [data-testid="stHeadingWithActionElements"] h3{
                      text-align:center;
                      background-color: #c7c6c6d4; 
                      margin-top:12px;
                      color:black;
                      border-radius: 20px;   
                    }
                    [data-testid="stBaseButton-secondary"]{
                        margin-left: 20px;
                        border-radius: 12px; /* rounded pill shape */
                        background-color:#5f5f5fd2; 
                        width:280px;
                        border: 3px solid black;
                        color:#bebdbd;
                        cursor: pointer;
                        transition: background-color 0.3s, color 0.3s;
                    }
                    [data-testid="stBaseButton-secondary"]:hover{
                        background-color:black;
                    }
                    [data-testid="stBaseButton-secondary"] p{
                        font-weight: 600;
                        font-size:24px;
                    }
                    [data-testid="stHorizontalBlock"]{
                        padding:12px;
                    }
                </style>
                <div class='account'>
                    <h1>Account Section</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.subheader("""Logged In As""")
        user = st.session_state.current_user
        # user = {"username":"Khushbu","email":"asdf@gmail.com","date_of_birth":"2025-09-12","address":"sdfisoan","gender":"Female","pincode":121656}
    
        #### EDIT FORM ####
        def show_edit_form():
            st.session_state.edit_mode = True
    
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False
        
        if not st.session_state.edit_mode:
            # Show user details
            with st.container():
                st.markdown(f"#### Name => {user['username']}")
                email = user['email'].replace("@", "@ ").replace(".", ". ")
                st.markdown(f"#### Email => {email}")
                st.markdown(f"#### Date Of Birth => {user['date_of_birth']}")
                st.markdown(f"#### Address => {user['address']}")
                st.markdown(f"#### Gender => {user['gender']}")
                st.markdown(f"#### Pincode => {user['pincode']}")
            
            col1, col2 = st.columns(2)    
            with col1:
                st.button("Edit User Details",on_click=show_edit_form)
            with col2:
               if st.button("Log Out", on_click=auth.logout_user):
                   st.session_state.current_user = None
        else:
            auth.edit_details(user)

####### NAV BAR ######
nav_items_after_login = ["Home","Account","Log Out"]
nav_icons_after_login = ["house","person","box-arrow-right"]
# nav_items_before_login = ["Login","Home"]
# nav_icons_before_login = ["person-circle","house"]

# Render menu and store selected index in session_state
nav_css = {"container":{"padding":"5px","background-color":"#323232fc","border-radius": "8px","transition": "background-color 0.2s"}
           ,"nav-link": {"color": "white", "font-size": "18px", "--hover-color": "#444"}
           ,"nav-link-selected": {"background-color": "#024979", "color": "#fff"}
           }

# Render menu once
if st.session_state.current_user is not None:
    selected_nav = option_menu(
        menu_title=None,
        options=nav_items_after_login ,
        icons=nav_icons_after_login ,
        orientation="horizontal",
        default_index=0,
        styles=nav_css,
        key="nav_bar"
    )    

            
if st.session_state.current_user is None:
    if st.session_state.show_signup:
        st.session_state.show_login = False
        auth.signup()
        
    else:
        st.session_state.show_login = True
        st.session_state.show_signup = False
        auth.login()

    
else:
    if selected_nav == "Home":
        show_home()

    elif selected_nav == "Account":
        show_account()

    elif selected_nav == "Log Out": 

        st.session_state.current_user = None
        st.session_state.show_login = True
        st.session_state.show_signup = False
        st.session_state["selected_nav"] = "Login" 
        
        st.rerun()
    


