import streamlit as st
import auth
import base64
import tempfile
from streamlit_option_menu import option_menu
import payment
import cv2
import toon
import styling

st.set_page_config(page_title="Toonify", layout="centered")

# Set the app background
styling.set_background_image("./img/bg-img.png")

##### Initialize session states if not present #####
keys_for_false = ["show_login","show_signup","show_payment","payment_success"]
keys_for_none = ["current_user","processed_img","original_img","tmp_path","selected_style"]

for key in keys_for_false:
    if key not in  st.session_state:
        st.session_state[key] = False
for key in keys_for_none:
    if key not in  st.session_state:
        st.session_state[key] = None

if "paid_styles" not in st.session_state:
    st.session_state.paid_styles = set()

def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

##### HEADER #####
st.markdown("<div class='header'><div class='top-title'>Toonify</div></div>", unsafe_allow_html=True)
    
##### STYLES DATA ##### 
effects = {
    "Pencil Sketch": {
        "func": toon.pencilSketch,
        "filename": "pencil_sketch.png",
        "price" : "10"
    },
    "Colored Sketch": {
        "func": toon.coloredSketch,
        "filename": "colored_sketch.png",
        "price" : "15"
    },
    "Oil Painting": {
        "func": toon.oilPainting,
        "filename": "oil_painting.png",
        "price" :"20"
    },
    "Classic Cartoon": {
        "func": toon.classic_cartoon,
        "filename": "classic_cartoon.png",
        "price" : "25"
    },
    "Udnie Style Cartoon": {
        "func": toon.cartoon_neural_style,   # function reference
        "filename": "Udnie_style_cartoon.png",
        "args": [],                          # positional args besides image_input
        "kwargs": {                          # keyword arguments
            "style_model_path": "models/udnie.pth",
            "resize": 512,
            "add_edges": True
        },
        "price" : "50"
    },
    "Candy Style Cartoon": {
        "func": toon.cartoon_neural_style,   # function reference
        "filename": "Candy_style_cartoon.png",
        "args": [],                          # positional args besides image_input
        "kwargs": {                          # keyword arguments
            "style_model_path": "models/candy.pth",
            "resize": 512,
            "add_edges": True
        },
        "price" : "50"
    },
    "Mosaic Style Cartoon": {
        "func": toon.cartoon_neural_style,   # function reference
        "filename": "Mosaic_style_cartoon.png",
        "args": [],                          # positional args besides image_input
        "kwargs": {                          # keyword arguments
            "style_model_path": "models/mosaic.pth",
            "resize": 512,
            "add_edges": True
        },
        "price" : "50"
    },
    "Disney Cartoon": {
        "func": toon.disney_cartoon,
        "filename": "disney_style_cartoon.png",
        "price" : "40"
    },  
}
        
#### FUNCTION for RESETTING the GENERATED IMAGE and PAYMENT FORM #####
def on_style_nd_image_change():
    st.session_state.processed_img = None
    st.session_state.show_payment = False
    st.session_state.payment_success = False
    st.session_state.paid_styles = set()
    
    
#### DASHBOARD VIEW BEFORE LOGIN #####
def show_dashboard():
    st.markdown(styling.home_css,unsafe_allow_html=True)
    st.markdown(
                """
                <div class='hero-title'>
                    <h1 style="color:#026cb2; border-bottom:3px solid #026cb2; padding-bottom:4px">Welcome In Toonify</h1>
                    <span>Turn your photos into artwork, sketches, and cartoons with a click – the most simple, beautiful, and no-nonsense cartoonizer and photo editor for all</span>
                    <h6>In one click you can generate your toonified image</h6>  
                    
                </div>
                """,
                unsafe_allow_html=True
        )
    st.subheader("Preview:")
    st.image("img/Preview-1.png")

    
#### Main view: Welcome and hero section#####
def show_home():
        st.markdown(styling.home_css,unsafe_allow_html=True)
        st.markdown(
                """
                <div class='hero-title'>
                    <h1 style="color:#026cb2; border-bottom:3px solid #026cb2; padding-bottom:4px">Welcome In Toonify</h1>
                    <span>Turn your photos into artwork, sketches, and cartoons with a click – the most simple, beautiful, and no-nonsense cartoonizer and photo editor for all</span>
                    
                </div>
                """,
                unsafe_allow_html=True
        )
        
        if st.session_state.current_user is not None:           
            image = st.file_uploader("Upload Image:", type=['jpg','png','jpeg'], on_change=on_style_nd_image_change)
                
            if image:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                     tmp_file.write(image.getbuffer())
                     temp_image_path = tmp_file.name
                     st.session_state.tmp_path = temp_image_path
                
                styles = effects.keys()
                options = list(styles) 
                
                cola1, cola2 = st.columns(2)
                with cola1:
                    style_choice = st.selectbox("Choose a cartoon style:", options, on_change=on_style_nd_image_change)
                with cola2:
                    st.write("Click on button to generate image:")
                    generate_btn = st.button("Generate")
                    
                img_array = cv2.imread(st.session_state.tmp_path)
                st.session_state.original_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            
                if generate_btn and image:
                    effect_info = effects[style_choice]
                    func = effect_info["func"]
                    args = effect_info.get("args", [])
                    kwargs = effect_info.get("kwargs", {})
                    
                    processed = func(st.session_state.tmp_path, *args, **kwargs)
                    
                    st.session_state.processed_img = processed
                        
                col1, col2 = st.columns(2)
                with col1:
                    if st.session_state.original_img is not None:
                        st.image(st.session_state.original_img, caption="Original Image")
                with col2:
                    if st.session_state.original_img is not None:
                        if st.session_state.processed_img is not None:
                            st.image(st.session_state.processed_img, caption=f"{style_choice}")
                        else:
                            st.text("Click on generate button above. ⬆️")
                            
                                      
                if style_choice in st.session_state.paid_styles:
                    payment.get_image_download_link(st.session_state.processed_img,style_choice)
                    st.session_state.payment_success = False  # reset flag
                    
                if (style_choice not in st.session_state.paid_styles) and (st.session_state.processed_img is not None):
                    if not st.session_state.show_payment and not st.session_state.payment_success:
                        if st.button("📩 Download"):
                            st.session_state.show_payment = True

                    # Show form if Download clicked
                    if st.session_state.show_payment:
                        payment.show_payment_form(style_choice)

                    # Automatically show download if payment done
                    if st.session_state.payment_success:
                        payment.get_image_download_link(st.session_state.processed_img,style_choice)


##### Profile SECTION ####
def show_profile():
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
        st.markdown(styling.profile_css,unsafe_allow_html=True)
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


####### NAV BAR #####

# ---------- NAVBAR CONFIG ----------
nav_items_after_login = ["Home", "Profile", "Log Out"]
nav_icons_after_login = ["house", "person", "box-arrow-right"]

nav_items_before_login = ["Home", "Login"]
nav_icons_before_login = ["house", "person-circle"]

# ---------- SESSION STATE DEFAULTS ----------
if "menu_choice" not in st.session_state:
    st.session_state.menu_choice = "Login"
    

if st.session_state.current_user:
        # Menu shown after login
        selected = option_menu(
            None,
            nav_items_after_login,
            icons=nav_icons_after_login,
            styles=styling.nav_css,
            orientation="horizontal",
            default_index=nav_items_after_login.index(st.session_state.menu_choice)
            if st.session_state.menu_choice in nav_items_after_login
            else 0,
        )
else:
        # Menu shown before login
        selected = option_menu(
            None,
            nav_items_before_login,
            icons=nav_icons_before_login,
            styles=styling.nav_css,
            orientation="horizontal",
            default_index=1,
        )
        
st.session_state.menu_choice = selected  # keep track of the selection

# ---------- PAGE LOGIC ----------
if st.session_state.current_user is None:
    # ---- BEFORE LOGIN ----
    if selected == "Home":
        show_dashboard()
    elif selected == "Login":
        if st.session_state.show_signup:
            st.session_state.show_login = False
            auth.signup()
        else:
            st.session_state.show_login = True
            st.session_state.show_signup = False
            auth.login()
else:
    # ---- AFTER LOGIN ----
    if selected == "Home":
        show_home()
    elif selected == "Profile":
        show_profile()
    elif selected == "Log Out":
        reset_session()
        st.session_state.menu_choice = "Home"  
        st.rerun()
