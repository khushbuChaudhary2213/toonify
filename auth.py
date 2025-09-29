import streamlit as st
import re
import bcrypt
import datetime

from database import get_db_connection

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
        div.stButton > button:hover {background-color: #5599ff;
                background-color: black;
                color:white;
        }
        </style>
        """

#### VALIDATION FUNCTIONS ####

def is_valid_email(email):
    # Basic regex for email validation
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

def is_strong_password(password):
    # Password must be 8+ chars, with uppercase, lowercase, digit, special char
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True

def validate_pincode(number_input):
    try:
        pincode = int(number_input)
    except ValueError:
        return False
    return 100000 <= pincode <= 999999


def username_exists(username):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE username=%s", (username,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        st.error(f"Error checking username: {e}")
        return False


def get_user_by_username(username):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username, password,email, date_of_birth, address, gender, pincode FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        st.error(f"Error fetching user: {e}")
        return None

#### FORM SHOW AND HIDE LOGIC USING SESSION STATE ####

def show_login():
    st.session_state.show_login = True
    st.session_state.show_signup = False

def show_signup():
    st.session_state.show_login = False
    st.session_state.show_signup = True
def logout_user():
    st.session_state.current_user=None
def close_edit_form():
    st.session_state.edit_mode = False
    

#### LOGIN FORM ####
def login():
    if "current_user" not in st.session_state:
        st.session_state.current_user = None

    st.markdown(form_css,
        unsafe_allow_html=True,
    )
    st.markdown("""
                <style>
                    [data-testid="stLayoutWrapper"]{
                        width:400px;
                    }
                    div.stButton > button {
                        width: 340px;
                    }
                </style>
                """,
        unsafe_allow_html=True,
    )
    with st.container():
        st.title("Login Form")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.button("Log In")
        
        if submit:
            if not username or not password:
                st.error("Please fill in both Username and Password.")
            else:
                user = get_user_by_username(username)
                if user is None:
                    st.error("Invalid username or password.")
                else:
                    stored_username, stored_hash,stored_email, stored_dob,stored_address, stored_gender,stored_pincode = user
                    if bcrypt.checkpw(
                        password.encode(),
                        stored_hash.encode() if isinstance(stored_hash, str) else stored_hash,
                    ):
                        st.session_state.current_user = {
                            "username": stored_username,
                            "email": stored_email,
                            "date_of_birth": stored_dob,
                            "address": stored_address,
                            "gender": stored_gender,
                            "pincode": stored_pincode,
                        }

                        st.success(f"Welcome back, {stored_username}!")

                    else:
                        st.error("Invalid username or password.")
        
    
        if st.session_state.current_user:
            st.markdown(f"### Logged in as {st.session_state.current_user["username"]}")
            if st.button("Log Out", on_click=logout_user):
                st.session_state.current_user = None
        st.write("---")
        st.subheader("Don't have an account?")
        st.button("Create New Account", on_click=show_signup,key="sign_btn")

#### SIGN UP FORM ####
def signup():
    st.markdown(form_css,unsafe_allow_html=True,)
    with st.container():
        st.markdown("""
                     <style>
                        div.stButton > button{
                             width: 640px;
                        }    
                    </style>
                    """,unsafe_allow_html=True)
        st.title("Create A New Account")
        cola1, cola2 = st.columns(2)
        with cola1:
            username = st.text_input("Username")
            address = st.text_area("Address")
        with cola2:
            dob = st.date_input(
                "DOB",
                value=None,
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today()
            )
            gender = st.radio("Gender",["Male","Female","Other"], key="gender")
        col1, col2 = st.columns(2,vertical_alignment="center")
        with col1:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
        with col2:
            pincode = st.text_input("Pincode")
            confirm = st.text_input("Confirm Password", type="password")
        submit = st.button("Sign Up")
        
        if submit:
            if not username or not email or not password or not confirm or not dob or not address or not gender or not pincode:
                st.error("Please fill in all fields.")
            elif username_exists(username):
                st.error("Username already taken. Try another.")
            elif not is_valid_email(email):
                st.error("Invalid email format.")
            elif not validate_pincode(pincode):
                st.error("Pincode must be a 6-digit Number")
            elif not is_strong_password(password):
                st.error(
                    "Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character."
                )
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute(
                            "INSERT INTO users (username, email, password, date_of_birth, address, gender, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (
                                username,
                                email,
                                hashed_pw.decode() if hasattr(hashed_pw, 'decode') else hashed_pw,
                                dob,
                                address,
                                gender,
                                pincode  # add pincode value here
                            )
                            )   
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("Account created successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        st.write("---")
        st.subheader("Already have an account?")
        st.button("Log In", on_click=show_login)  
 
#### EDIT USER DETAILS ####       
def edit_details(user):
    st.markdown("""
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
                """,unsafe_allow_html=True)
    st.markdown(form_css,unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Name", value=user.get("username", ""))
            email = st.text_input("Email", value=user.get("email", ""))
            address = st.text_area("Address", value=user.get("address", ""))
        with col2:
            date_of_birth = st.date_input("Date Of Birth", value=user.get("date_of_birth"))
            pincode = st.number_input("Pincode", value=int(user.get("pincode") or 100000), min_value=100000, max_value=999999, step=1)
    
    col1, col2 = st.columns(2,vertical_alignment="center")
    with col1:
        if st.button("Save Changes"):
            conn = get_db_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE users SET username=%s, email=%s, date_of_birth=%s, address=%s, pincode=%s
                        WHERE username=%s
                    """, (username, email, date_of_birth, address, pincode, user["username"]))
                    conn.commit()
                    cur.close()
                    
                    # Update session state
                    st.session_state.current_user.update({
                        "username": username,
                        "email": email,
                        "date_of_birth": date_of_birth,
                        "address": address,
                        "pincode": pincode
                    })
                    st.success("Account details updated successfully!")
                    st.button("Close",on_click=close_edit_form)
                except Exception as e:
                    st.error(f"Failed to update user details: {e}")
                finally:
                    conn.close()
    with col2:
        st.button("Cancel",on_click=close_edit_form)
