import streamlit as st
import time
import re
from io import BytesIO
from PIL import Image
import numpy as np
from app import effects
import styling
import database


def show_payment_form(style):
    st.markdown(styling.payment_form_css, unsafe_allow_html=True)

    # Initialize states for OTP process
    if "awaiting_otp" not in st.session_state:
        st.session_state.awaiting_otp = False
    if "otp_verified" not in st.session_state:
        st.session_state.otp_verified = False

    with st.container():
        st.subheader(f"PAY TO UNLOCK '{style}' STYLE")

        options = ["Card", "UPI", "Net Banking"]
        payment_option = st.radio("Choose Payment Method", options, horizontal=True)

        # ---- Payment Details ---- #
        if payment_option == "Card":
            st.write("💳 **Card Payment**")
            col1, col2, col3 = st.columns(3)
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
                upi = st.selectbox("Select UPI", ["PhonePe", "Google Pay", "Paytm", "Amazon Pay UPI"])
                upi_id = st.text_input("UPI ID")
            with col2:
                if upi == "PhonePe":
                    st.image("img/PhonePe.png", width=150)
                elif upi == "Google Pay":
                    st.image("img/Gpay.jpg", width=150)
                elif upi == "Paytm":
                    st.image("img/paytm.png", width=150)
                elif upi == "Amazon Pay UPI":
                    st.image("img/amazon_pay.png", width=150)

        elif payment_option == "Net Banking":
            st.write("🏦 **Net Banking Payment**")
            col1, col2 = st.columns(2)
            with col1:
                bank = st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis Bank", "PNB", "Others"])
            with col2:
                acct_num = st.text_input("Account No")
                mobile_no = st.text_input("Mobile No")

        st.info(f"💰 Amount to Pay: ₹{effects[style]['price']}")

        # ---------------- OTP Step ---------------- #
        if not st.session_state.awaiting_otp:
            pay = st.button("Confirm Payment")

            if pay:
                # --- Validation --- #
                if payment_option == "Card":
                    if not card_no or not expiry or not cvv:
                        st.error("Please fill all card details.")
                        return
                    if not (card_no.isdigit() and len(card_no) == 16):
                        st.error("Please enter a valid 16-digit card number.")
                        return
                    if not re.match(r"^(0[1-9]|1[0-2])/\d{2}$", expiry):
                        st.error("Expiry must be in MM/YY format.")
                        return
                    if not (cvv.isdigit() and len(cvv) in [3, 4]):
                        st.error("Please enter a valid 3 or 4-digit CVV.")
                        return

                elif payment_option == "UPI":
                    upi_pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+$"
                    if not upi_id or not re.match(upi_pattern, upi_id):
                        st.error("Please enter valid UPI ID")
                        return

                elif payment_option == "Net Banking":
                    if not bank or not acct_num or not mobile_no:
                        st.error("Please fill all net banking details.")
                        return
                    if not (acct_num.isdigit() and 9 <= len(acct_num) <= 16):
                        st.error("Please enter a valid 9-16-digit account number.")
                        return
                    if not (mobile_no.isdigit() and len(mobile_no) == 10):
                        st.error("Please enter a valid 10-digit mobile number.")
                        return

                # After validation, show OTP input
                st.session_state.awaiting_otp = True
                st.rerun()

        else:
            # OTP verification step
            st.success("✅ Payment details validated successfully!")
            st.info("Enter the 6-digit OTP sent to your registered mobile/email (Demo OTP).")

            otp_input = st.text_input("Enter OTP", max_chars=6, type="password")
            verify_otp = st.button("Verify & Complete Payment")

            if verify_otp:
                if not otp_input:
                    st.error("Please enter OTP to continue.")
                    return
                # Simulate OTP processing
                with st.spinner("🔒 Verifying OTP..."):
                    time.sleep(1.5)
                st.session_state.otp_verified = True
                st.session_state.awaiting_otp = False
                st.rerun()

        # ---------------- Payment Success ---------------- #
        if st.session_state.otp_verified:
            with st.spinner("💫 Processing payment..."):
                time.sleep(1.5)
                
            try:
                con = database.get_db_connection()
                cur = con.cursor()
                
                image_id = st.session_state.get("image_id")
                
                cur.execute("""
                    UPDATE user_images SET payment_status = 'paid' WHERE id = %s            
                """, (image_id,))
                
                con.commit()
                cur.close()
            except Exception as e:
                print(f"Payment update failed: {e}")
            finally:
                con.close()

            st.session_state.paid_styles.add(style)
            st.session_state.payment_success = True

            st.success(f"✅ Payment successful for '{style}' style!")
            st.balloons()

            # Reset OTP states
            st.session_state.otp_verified = False
            st.session_state.awaiting_otp = False
            st.session_state.show_payment = False


def get_image_download_link(img: Image.Image, style_choice):
    st.markdown(styling.download_btn_css, unsafe_allow_html=True)

    buf = BytesIO()

    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)

    img.save(buf, format="PNG")
    buf.seek(0)
    download_btn = st.download_button(
        label="⬇️ Download Cartoon Image",
        data=buf,
        file_name=f"{style_choice}.png",
        mime="image/png",
    )
    
    if download_btn:
        try:
            con = database.get_db_connection()
            cur = con.cursor()
            image_id = st.session_state.get("image_id")
            cur.execute("""UPDATE user_images SET download_status = 'downloaded' where id = %s""",(image_id,))
            
            con.commit()
            cur.close
        except Exception as e:
            print(f"An error occured: {e}")
        finally:
            con.close()
