import streamlit as st
import time 
import re 
from io import BytesIO
from PIL import Image
import numpy as np
from app import effects
import styling

# -----------------------
# FUNCTION FOR DOWNLOADING THE GENERATED IMAGE

def show_payment_form(style):
    st.markdown(styling.payment_form_css,unsafe_allow_html=True)

    with st.container():
        st.subheader(f"PAY TO UNLOCK '{style}' STYLE")
        
        options = ["Card", "UPI", "Net Banking"]
        payment_option = st.radio("Choose Payment Method", options, horizontal=True)

        if payment_option == "Card":
            st.write("💳 **Card Payment**")
            col1,col2,col3 = st.columns(3)
            with col1:
                card_no = st.text_input("Card Number")
            with col2:
                expiry = st.text_input("Expiry (MM/YY)")
            with col3:
                cvv = st.text_input("CVV", type="password")

        elif payment_option == "UPI":
            st.write("📱 **UPI Payment**")
            col1, col2 = st.columns(2)
            with col1:
                upi = st.selectbox("Select UPI", ["PhonePe","Google Pay","Paytm","Amazon Pay UPI"])
                upi_id = st.text_input("UPI ID")
            with col2:
                if upi == "PhonePe":
                    st.image("img/PhonePe.png",width=150)
                if upi == "Google Pay":
                    st.image("img/Gpay.jpg",width=150)
                if upi == "Paytm":
                    st.image("img/paytm.png",width=150)
                if upi == "Amazon Pay UPI":
                    st.image("img/amazon_pay.png",width=150)

            
        elif payment_option == "Net Banking":
            st.write("🏦 **Net Banking Payment**")
            col1, col2 = st.columns(2)
            with col1:
                bank = st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis Bank", "PNB", "Others"])
            with col2:
                acct_num = st.text_input("Account No")
                mobile_no = st.text_input("Mobile No")
            

        st.info(f"💰 Amount to Pay: ₹{effects[style]['price']}")

        pay = st.button("Confirm Payment")

        if pay:
            # --- Validation --- #
            if payment_option == "Card":
                if not card_no and not expiry and not cvv:
                    st.error("Please fill all card details.")
                    return
                if not (card_no.isdigit() and len(card_no) == 16):
                    st.error("Please enter a valid 16-digit card number.")
                    return
                if not re.match(r"^(0[1-9]|1[0-2])/\d{2}$", expiry):
                    st.error("Expiry must be in MM/YY format.")
                    return
                if not (cvv.isdigit() and len(cvv) in [3,4]):
                    st.error("Please enter a valid 3 or 4-digit CVV.")
                    return
                
            elif payment_option == "UPI":
                upi_pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+$"
                if  not upi_id or not re.match(upi_pattern, upi_id):
                    st.error("Please enter valid UPI ID")
                    return
                
            elif payment_option == "Net Banking":
                if (not bank and not acct_num and not mobile_no):
                    st.error("Please fill all net banking details.")
                    return
                    
                if  (not acct_num.isdigit() or (len(acct_num) > 16 or len(acct_num) < 9)):
                    st.error("Please enter a valid 9-16-digit account number.")
                    return
                if  (not mobile_no.isdigit() or (len(mobile_no) != 10)):
                    st.error("Please enter a valid 10-digit mobile number.")
                    return

            # --- Simulated Payment Process --- #
            
            with st.spinner("💫 Processing payment..."):
                time.sleep(1.5)

            # --- Payment Success Actions --- #
            st.session_state.paid_styles.add(style)
            st.session_state.show_payment = False
            st.session_state.payment_success = True

            if st.session_state.payment_success:
                st.session_state.show_payment = False
                st.success(f"✅ Payment successful for '{style}' style!")
                st.balloons()
            
        
def get_image_download_link(img: Image.Image, style_choice):
    st.markdown(styling.download_btn_css,unsafe_allow_html=True)
    
    buf = BytesIO()

    # ✅ Convert NumPy array to PIL before saving
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)

    img.save(buf, format="PNG")
    buf.seek(0)
    st.download_button(
                        label="⬇️ Download Cartoon Image",
                        data=buf,
                        file_name=f"{style_choice}.png",
                        mime="image/png"
                    )
   
        