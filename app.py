import streamlit as st
import auth
import base64
import tempfile
import uuid
from streamlit_option_menu import option_menu
import database
import cv2
import toon
import styling
import payment
import os
import numpy as np
from PIL import Image

st.set_page_config(page_title="Toonify", layout="centered")

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
    # "Disney Cartoon": {
    #     "func": toon.disney_cartoon,
    #     "filename": "disney_style_cartoon.png",
    #     "price" : "40"
    # },  
}

# ---------- NAVBAR CONFIG (Constants) ----------
NAV_ITEMS_AFTER_LOGIN = ["Home", "Profile", "Log Out"]
NAV_ICONS_AFTER_LOGIN = ["house", "person", "box-arrow-right"]
NAV_ITEMS_BEFORE_LOGIN = ["Home", "Login"]
NAV_ICONS_BEFORE_LOGIN = ["house", "person-circle"]


##### FUNCTION DEFINITIONS #####
def reset_session():
    # Keep menu_choice to prevent flicker on rerun, delete everything else
    menu_choice = st.session_state.get("menu_choice", "Home")
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.menu_choice = menu_choice # Restore it
        
#### FUNCTION for RESETTING the GENERATED IMAGE and PAYMENT FORM #####
def on_style_nd_image_change():
    st.session_state.processed_img = None
    st.session_state.show_payment = False
    st.session_state.payment_success = False
    # st.session_state.paid_styles = set()
    
def save_image(processed, save_path):
    if isinstance(processed, np.ndarray):
        # OpenCV image
        cv2.imwrite(save_path, processed)

    elif isinstance(processed, Image.Image):
        # PIL image
        processed.save(save_path)

    else:
        raise ValueError("Unsupported image type")

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
img1 = get_base64_image("img/previewImg/Pencil Sketch.png")    
img2 = get_base64_image("img/previewImg/Colored Sketch.png")    
img3 = get_base64_image("img/previewImg/Oil Painting.png")    
img4 = get_base64_image("img/previewImg/Classic Cartoon.png")    
img5 = get_base64_image("img/previewImg/Candy Style Cartoon.png")    
img6 = get_base64_image("img/previewImg/Mosaic Style Cartoon.png")    
img7 = get_base64_image("img/previewImg/Udnie Style Cartoon.png")    

#### DASHBOARD VIEW BEFORE LOGIN #####
def show_dashboard():
    st.markdown(styling.dashboard_css,unsafe_allow_html=True)
    st.markdown(styling.hero_css,unsafe_allow_html=True)
    st.markdown(styling.preview_css, unsafe_allow_html=True)
    st.markdown(
                f"""
                <div class='hero-title'>
                    <h1 style="color:#026cb2; border-bottom:3px solid #026cb2; padding-bottom:4px">Welcome In Toonify</h1>
                    <span>Turn your photos into artwork, sketches, and cartoons with a click – the most simple, beautiful, and no-nonsense cartoonizer and photo editor for all</span>
                    <h6>In one click you can generate your toonified image. <br>Firstly, you need to Login/Signup</h6>  
                </div>
                <div class="usage-steps-div">
                    <p class="usage-steps-heading" style="font-size:24px">Simple steps to convert the real image into <span>TOONIFIED</span> image</p>                    
                    <div class="usage-steps">
                        <div class="usage-step">
                            <h5>Upload Your Image & Select Style</h5>
                            <p>Upload a clear photo that you want to convert into given styles.Explore our collection of unique cartoon styles from classic anime looks to soft sketch tones
                                </p>
                        </div>
                        <div class="usage-step">
                            <h5>AI Processing & Cartoon Generation</h5>
                            <p>Once the payment is complete, our AI model gets to work!
                            Within a few seconds, it transforms your image into a stunning cartoon version.</p>
                        </div>
                        <div class="usage-step">
                            <h5>Make Payment to Unlock Style</h5>
                            <p>Each style comes with a small, per-use price.
                                Choose your preferred payment method (Card, UPI, or Net Banking), enter the details, and confirm.
                                </p>
                        </div>
                        <div class="usage-step">
                            <h5>Download Your Cartoon Image</h5>
                            <p>After the cartoonization is finished, preview your image directly on the dashboard.
                                Click on the download button to instantly save your cartoon artwork to your device.</p>
                        </div>  
                    </div>
                </div>
                <h3>Preview:</h3>
                <div class="preview-container">
                    <div class="preview-card">
                        <img src="data:image/png;base64,{img1}">
                        <h4 class="preview-title">Pencil Sketch </h4>
                        <p class="preview-quality">Classic • High Detail</p>
                    </div>
                    <div class="preview-card">
                        <img src="data:image/png;base64,{img2}">
                        <h4 class="preview-title"> Colored Sketch </h4>
                        <p class="preview-quality">Artistic • Vibrant</p>
                    </div>
                    <div class="preview-card">
                        <img src="data:image/png;base64,{img3}">
                        <h4 class="preview-title"> Oil Painting </h4>
                        <p class="preview-quality">Premium • Rich Texture</p>
                    </div>
                    <div class="preview-card">
                        <img src="data:image/png;base64,{img4}">
                        <h4 class="preview-title"> Classic Cartoon</h4>
                        <p class="preview-quality">Smooth • HD</p>
                    </div>
                    <div class="preview-card">
                        <img src="data:image/png;base64,{img5}">
                        <h4 class="preview-title"> Candy Style</h4>
                        <p class="preview-quality">Bright • Fun</p>
                    </div>
                    <div class="preview-card">
                        <img src="data:image/png;base64,{img6}">
                        <h4  class="preview-title"> Mosaic Style</h4>
                        <p class="preview-quality">Creative • Pattern</p>
                    </div>

                </div>
                
                """,
                unsafe_allow_html=True
        )

    
    
#### Main view: Welcome and hero section#####
def show_home():
        st.markdown(styling.home_css,unsafe_allow_html=True)
        st.markdown(styling.hero_css,unsafe_allow_html=True)
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
                    
                    # ensure folder exists
                    os.makedirs("images", exist_ok=True)
                    
                    # create unique filename
                    original_filename = f"{uuid.uuid4()}_original.png"
                    original_save_path = os.path.join("images", original_filename)

                    # save original image
                    img = Image.open(st.session_state.tmp_path)
                    img.save(original_save_path)
                    
                    # create unique filename
                    base_filename = effect_info["filename"]
                    unique_filename = f"{uuid.uuid4()}_{base_filename}"
                    save_path = os.path.join("images",unique_filename)
                    
                    # save processed_img into a folder
                    save_image(processed, save_path)
                    
                    user_id = st.session_state.current_user['id']
                    original_image_url = original_save_path
                    processed_image_url = save_path
                    
                    con = None
                    cur = None
                    try:
                        con = database.get_db_connection()
                        cur = con.cursor()
                        cur.execute("""INSERT INTO user_images (user_id,style, original_image_url, processed_image_url) VALUES (%s,%s, %s, %s) RETURNING id""",(user_id,style_choice, original_image_url, processed_image_url))
                        
                        result = cur.fetchone()
                        
                        image_id = result[0]
                        con.commit()

                        st.session_state["image_id"] = image_id
                        cur.close()
                    except Exception as e:
                        print("Failed to execute the insert user_image query.")
                        print(e)
                    finally:
                        if con:
                            con.close()
                    
                        
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
                            
                
                    
                isPaid = style_choice in st.session_state.paid_styles 
                                      
                if isPaid and st.session_state.processed_img is not None:
                    payment.get_image_download_link(st.session_state.processed_img,style_choice)
                    st.session_state.show_payment = False
                    st.session_state.payment_success = False  # reset flag
                    
                if not isPaid:
                    if not st.session_state.show_payment and st.session_state.processed_img is not None:
                        if st.button("📩 Download") :
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



def main():
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
    
    if "menu_choice" not in st.session_state:
        st.session_state.menu_choice = "Home"

    ##### HEADER #####
    st.markdown("<div class='header'><div class='top-title'>Toonify</div></div>", unsafe_allow_html=True)

    ####### NAV BAR #####
    if st.session_state.current_user:
            # Menu shown after login
            selected = option_menu(
                None,
                NAV_ITEMS_AFTER_LOGIN,
                icons=NAV_ICONS_AFTER_LOGIN,
                styles=styling.nav_css,
                orientation="horizontal",
                key="navbar_after_login",
                default_index=NAV_ITEMS_AFTER_LOGIN.index(st.session_state.menu_choice)
                if st.session_state.menu_choice in NAV_ITEMS_AFTER_LOGIN
                else 0,
            )
    else:
            # Menu shown before login
            selected = option_menu(
                None,
                NAV_ITEMS_BEFORE_LOGIN,
                icons=NAV_ICONS_BEFORE_LOGIN,
                styles=styling.nav_css,
                orientation="horizontal",
                default_index=NAV_ITEMS_BEFORE_LOGIN.index(st.session_state.menu_choice)
                if st.session_state.menu_choice in NAV_ITEMS_BEFORE_LOGIN
                else 1,
                key="navbar_before_login", # Renamed key back, it's safe now
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
            st.session_state.menu_choice = "Login"  
            st.rerun() # This is the single, correct rerun for logout.


# --- This line ensures main() ONLY runs when you execute `streamlit run app.py` ---
if __name__ == "__main__":
    main()