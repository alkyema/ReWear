import streamlit as st
import requests
import json

BASE_URL = "http://localhost:8888"  # Change to your deployed backend URL

st.set_page_config(page_title="ReWear Admin Dashboard", layout="wide")
st.title("👕 ReWear Backend Admin Dashboard")

menu = st.sidebar.selectbox("Choose Action", [
    "📦 View All Items",
    "🆕 Create Item",
    "🖼️ Upload Images",
    "🧩 Create Item with Images",
    "🔀 Swap Items",
    "👤 Signup",
    "🔐 Login",
    "📧 Generate OTP",
    "✅ Verify OTP",
    "🔑 Change Password"
])

def handle_response(resp):
    if resp.status_code == 200:
        st.success(resp.json())
    else:
        st.error(f"{resp.status_code} - {resp.text}")

# 1. View All Items
if menu == "📦 View All Items":
    response = requests.get(f"{BASE_URL}/items/")
    if response.status_code == 200:
        items = response.json()
        st.json(items)
    else:
        st.error("Failed to fetch items")

# 2. Create Item
elif menu == "🆕 Create Item":
    with st.form("create_item_form"):
        name = st.text_input("Item Name")
        description = st.text_area("Description")
        owner_id = st.text_input("Owner ID")
        submitted = st.form_submit_button("Create Item")

        if submitted:
            data = {
                "name": name,
                "description": description,
                "owner_id": owner_id
            }
            response = requests.post(f"{BASE_URL}/items/", json=data)
            handle_response(response)

# 3. Upload Images
elif menu == "🖼️ Upload Images":
    tags = st.text_input("Tags (comma-separated)", "rewear")
    context = st.text_input("Context", "Item Number")
    files = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)

    if st.button("Upload"):
        if files:
            multipart_data = [("files", (f.name, f, f.type)) for f in files]
            response = requests.post(
                f"{BASE_URL}/upload-images",
                files=multipart_data,
                data={"tags": tags, "context": context}
            )
            handle_response(response)

# 4. Create Item with Images
elif menu == "🧩 Create Item with Images":
    name = st.text_input("Item Name")
    description = st.text_area("Description")
    owner_id = st.text_input("Owner ID")
    files = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)

    if st.button("Create Item with Images"):
        if files:
            item_data = {
                "name": name,
                "description": description,
                "owner_id": owner_id
            }

            multipart_data = [("files", (f.name, f, f.type)) for f in files]
            multipart_data.append(("item_data", (None, json.dumps(item_data), "application/json")))

            response = requests.post(f"{BASE_URL}/items/create-with-images", files=multipart_data)
            handle_response(response)

# 5. Swap Items
elif menu == "🔀 Swap Items":
    id1 = st.text_input("Item ID 1")
    id2 = st.text_input("Item ID 2")

    if st.button("Swap Items"):
        response = requests.post(f"{BASE_URL}/swap/{id1}/{id2}")
        handle_response(response)

# 6. Signup
elif menu == "👤 Signup":
    with st.form("signup_form"):
        Username = st.text_input("Username")
        userID = st.text_input("User ID")
        Password = st.text_input("Password", type="password")
        Email = st.text_input("Email")
        Contact = st.text_input("Contact Number")
        profile_pic = st.file_uploader("Upload Profile Pic", type=["jpg", "png"])
        submit = st.form_submit_button("Signup")

        if submit:
            files = {"profile_pic": (profile_pic.name, profile_pic, profile_pic.type)} if profile_pic else None
            data = {
                "Username": Username,
                "userID": userID,
                "Password": Password,
                "Email": Email,
                "Contact": Contact
            }
            response = requests.post(f"{BASE_URL}/signup", data=data, files=files)
            handle_response(response)

# 7. Login
elif menu == "🔐 Login":
    userID = st.text_input("User ID")
    Password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(f"{BASE_URL}/login", json={
            "userID": userID,
            "Password": Password
        })
        handle_response(response)

# 8. Generate OTP
elif menu == "📧 Generate OTP":
    Email = st.text_input("Email to send OTP")

    if st.button("Send OTP"):
        response = requests.post(f"{BASE_URL}/generateOTP", json={"Email": Email})
        handle_response(response)

# 9. Verify OTP
elif menu == "✅ Verify OTP":
    otp = st.text_input("Enter OTP")

    if st.button("Verify"):
        response = requests.post(f"{BASE_URL}/OTPverify", json={"verOTP": otp})
        handle_response(response)

# 10. Change Password
elif menu == "🔑 Change Password":
    Email = st.text_input("Email")
    new_password = st.text_input("New Password", type="password")

    if st.button("Change Password"):
        response = requests.post(f"{BASE_URL}/PasswordChange", json={
            "Email": Email,
            "Password": new_password
        })
        handle_response(response)
