import base64
import streamlit as st

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
            
            .account{{
                text-align:center;
                background-color: #c7c6c6d4; 
                color:black;
                border-radius: 20px; 
            }}
            
        </style>
    """
    
    st.markdown(page_css, unsafe_allow_html=True)
    
hero_css= """
    <style>
        .hero-title {
                        text-align: center;
                        background-color: #c7c6c6d4; 
                        border: 4px solid black; 
                        border-radius: 20px; 
                        padding: 40px 80px;
                        overflow: hidden;
                        z-index: 1;
                    }
                    .hero-title h1{
                        margin-bottom:20px;
                        
                    }
                    .hero-title span{
                        color: black;
                        font-weight:300px;
                        margin-top:12px;
                    }
                    .hero-title h6{
                        color:black;
                        margin-top: 20px;
                        font-size: 22px;
                        border: 2px solid #1764a6;
                        padding: 10px;
                    }
    </style>
"""
    
#### CSS for DASHBOARD ####
dashboard_css = """
                <style>
                    [data-testid="stHeadingWithActionElements"] h3{
                                    background-color: #c7c6c6d4;
                                    border-radius: 22px;
                                    border: 4px solid black; 
                                    text-align: center;
                                    margin-top: 12px;
                                    color: black;
                                    margin-bottom:20px;
                                }
                    
                    .usage-steps-div {
                        margin-top: 40px;
                        padding: 20px 30px;
                        border-radius: 15px;
                        border:4px solid black;
                        background: #c7c6c6d4;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    }

                    .usage-steps-heading {
                        text-align: center;
                        font-weight: 600;
                        margin-bottom: 30px;
                        color: black;
                    }

                    .usage-steps-heading span {
                        color: #026cb2;
                        font-weight: 700;
                    }

                    .usage-steps {
                        display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        gap: 25px;
                        padding: 10px;
                        position: relative;
                    }

                    .usage-step {
                        background: #f9fcff;
                        padding: 20px;
                        border-radius: 15px;
                        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
                        text-align: center;
                        border: 1px solid #e0eefc;
                        transition: all 0.3s ease-in-out;
                    }

                    .usage-step:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 6px 15px rgba(2,108,178,0.2);
                        border-color: #026cb2;
                    }


                    .usage-step h5{
                        color: #026cb2;
                        font-weight: 600;
                        margin-bottom: 8px;
                        font-size: 1.1rem;
                    }

                    .usage-step p {
                        color: #333;
                        font-size: 0.95rem;
                        font-weight:500;
                        line-height: 1.5;
                        margin-bottom: 0;
                    }
                </style>
            """
            
preview_css = """
        <style>

            .preview-container {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }

            .preview-card {
                background: white;
                border-radius: 12px;
                padding: 10px;
                width: 220px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.2s ease;
            }
            
            .preview-card [data-testid="stHeadingWithActionElements"]{
                color:black;
            }

            .preview-card:hover {
                transform: translateY(-5px);
            }

            .preview-card img {
                width: 100%;
                border-radius: 10px;
            }

            .preview-title {

                margin-top: 8px;
            }

            .preview-quality {
                font-size: 14px;
                color: gray;
            }
        </style>
    """
    
    
#### CSS for NAVBAR ####
nav_css = {
    "container": {
        "padding": "5px",
        "background-color": "#323232fc",
        "border-radius": "8px",
        "transition": "background-color 0.2s"
    },
    "nav-link": {
        "color": "white",
        "font-size": "18px",
        "--hover-color": "#444"
    },
    "nav-link-selected": {
        "background-color": "#024979",
        "color": "#fff"
    }
}

#### CSS for HOMEPAGE and DASHBOARD ####
home_css = """
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
                            # margin-top:12px;    
                        }
                        [data-testid="stElementContainer"] [data-testid="stButton"]{
                            width:314px;
                            border-top:none;
                            border-radius: 22px;
                            padding:18px;
                            background-color:#c7c6c6d4;
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
                        [data-testid="stFullScreenFrame"]{
                            margin-top:24px;
                        }
                        [data-testid="stImageContainer"] img{
                            # margin-top:20px;
                        }
                        [data-testid="stCaptionContainer"] p{
                            color: #000000;
                            font-size: 20px;
                            background-color: white;
                            font-weight: bold;
                            text-transform: uppercase;
                        }
                        [data-testid="stVerticalBlock"] {
                            gap:12px;
                        }
                        [data-testid="stColumn"] [data-testid="stVerticalBlock"] [data-testid="stElementContainer"] [data-testid="stSelectbox"]{
                            height:160px;
                        }
                        [data-testid="stLayoutWrapper"] {
                            backdrop-filter:blur(20px);
                            background-color: #aeaeae4a !important;  
                            padding: 30px;
                            border-radius: 15px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                            margin: auto;
                        }
                        [data-testid="stHeadingWithActionElements"] h3{
                            background-color: #c7c6c6d4;
                            border-radius: 22px;
                            border: 4px solid black; 
                            text-align: center;
                            margin-top: 12px;
                            color: black;
                        }
                        [data-testid="stFileUploaderDropzone"]{
                            background-color: transparent;
                        }
                        [data-testid="stFileUploaderDropzoneInstructions"]{
                            border:1px solid black;
                        }
                        [class="st-emotion-cache-ysg2um e1d2qte93"],[class="st-emotion-cache-15cv43h e1d2qte94"],[class="st-emotion-cache-1qjeh18 e1d2qte92"]{
                            color:black;
                        }
                        [data-testid="stText"]{
                                text-align: center;
                                margin: 150px 20px;
                                text-decoration: underline;
                                font-size: 24px
                        }
                    </style>
                    """

#### CSS for ACCOUNT SECTION ####
profile_css =   """
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
                """      

#### CSS for FORM ####
form_css = """
        <style>
        [data-testid="stElementContainer"]{
            margin-bottom:-10px;
        }
        [data-testid="stLayoutWrapper"] {
            backdrop-filter:blur(20px);
            background-color: #aeaeae4a !important;  
            padding: 30px;
            border-radius: 15px;
            # color:black;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin: auto;
        }
        [data-testid="stHeadingWithActionElements"]{
            text-align:center;
            margin-top:0;
        }
        div.stButton > button {
                margin-top: 10px;
                border-radius: 12px; /* rounded pill shape */
                background-color:#5f5f5f81;
                font-weight: 600;
                border: 3px solid black;
                cursor: pointer;
                transition: background-color 0.3s, color 0.3s;
        }
        div.stButton > button:hover {
                background-color: black;
                color:white;
        }
        
        </style>
        """

#### CSS for EDIT DETAILS OF USER ####
edit_details_css = """
                    <style>
                        .div.stButton > button{
                            margin-top:0px;
                            padding-top:0px;
                        }
                        [data-testid="stBaseButton-secondary"]{
                            margin-left:18px;
                            padding:0;
                        }
                    </style>
                """
    
#### CSS for PAYMENT FORM ####            
payment_form_css = """
                <style>
                    [data-testid="stHeadingWithActionElements"] h3{
                        font-weight:bold;
                        text-align:center;
                        font-size:32px;
                        border:1px solid black;
                        padding-left:12px;
                        border-radius: 15px;
                        margin-bottom: 10px;
                        background-color:#aeaeae4a;   
                    }
                </style>
                """

#### CSS for DOWNLOAD BUTTON ####
download_btn_css = """
                <style>
                    [data-testid="stDownloadButton"]{
                            width:314px;
                            border-top:none;
                            border-radius: 22px;
                            padding:18px;
                            background-color:#c7c6c6d4; 
                    }
                </style>
                """