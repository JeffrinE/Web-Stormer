import streamlit as st
import streamlit_shadcn_ui as ui
import time
import main
import uuid
import dbcreator as db
import cred_creator as cd

if 'vote' not in st.session_state:
    st.session_state['voted'] = False
    st.session_state['new_passwd'] = None

def notification(val: str):
    values = ['error', 'success']
    if val == values[0]:
        st.toast("An Error has occured. Please check your password.", icon='🔒')
    else:
        st.toast("Password change successfull", icon='🚫')

@st.dialog("Cast your vote")
def change_password(item):
    if st.session_state['voted']:
        st.write(f"Change Your Password")
        og_passwd = st.text_input("Original Password", type="password")
        new_passwd = st.text_input("New Password", type="password")
        confirm_passwd = st.text_input("Confirm Password", type="password")
        if st.button("Submit"):
            st.session_state.new_passwd = {og_passwd, new_passwd, confirm_passwd}
            is_changed = cd.change_password("admin", og_passwd=og_passwd, new_passwd=new_passwd, confirm_passwd=confirm_passwd)
            if is_changed:
                pass
            else:
                notification()
                time.sleep(2)
            st.rerun()


def main_page():

    def notification(value: str):
        values = ('already_exists', 'blocked', 'unblocked')
        if value == values[0]:
            st.toast(f'Already Exists: {input_value}',icon='🚫')
        if value == values[1]:
            st.toast(f'Blocked: {input_value}',icon='✋')
        if value == values[2]:
            st.toast(f'UnBlocked: {input_value}',icon='🔓')

    st.header("Web Blocker")
    input_value = ui.input(default_value="", type='text', placeholder="Enter text here", key="input1")
    blocked = ui.button("Click", key="clk_btn")

    st.sidebar.write("Instructions")
    change_passwd = st.sidebar.container(border=True)
    change_passwd.write("Change Password")

    if change_passwd.button("Change Password"):
        st.session_state['voted'] = True
        change_password('A')

    if "rows" not in st.session_state:
        ids = db.get_uuids()
        st.session_state["rows"] = []
        st.session_state["rows"] += ids

    ids = db.get_uuids()
    rows_collection = []
    rows_collection += ids

    def add_row(url: str):
        element_id = uuid.uuid4()
        data = str(element_id)
        st.session_state["rows"].append(data)
        main.block_website(row_id=data, website=url)

    def remove_row(row_id: str):
        data = str(row_id)
        main.unblock_website(row_id)
        notification('unblocked')
        st.session_state["rows"].remove(data)

    if blocked and input_value:
        if main.is_website_blocked(input_value):
            notification('already_exists')
        else:
            add_row(input_value)
            notification('blocked')

    def generate_row(row_id):
        row_container = st.empty()
        row_columns = row_container.columns((3, 2, 1))
        row_name = row_columns[0].text(db.show_from_id(row_id)[0])
        row_columns[2].button("🗑️", key=f"del_{row_id}", on_click=remove_row, args=[row_id])
        return {"name": row_name}

    for row in st.session_state["rows"]:
        row_data = generate_row(row)
        rows_collection.append(row_data)
    menu = st.columns(2)

#-----------------------------------------------------------------------------------------------------------------------

def notification():
    st.toast(f'Incorrect Username or Password',icon='🚫')

st.title("Welcome Back")

if "page" not in st.session_state:
    st.session_state.page = "login"#login change to login fgrvcbsjdc
if "userid" not in st.session_state:
    st.session_state.userid = ""

def next(action, username, passd):
    if action == "login":
        passwd = cd.is_user_in_db(user=username, passwd=str(passd))
        if passwd:
            st.session_state.page = "feed" # Go to next page
        else:
            st.session_state.page="login"
            notification()

placeholder = st.empty()
if st.session_state.page == "login":
    placeholder.empty()
    username = st.text_input("User Name",type="default",placeholder="username")
    passd = st.text_input("User ID",type="password",placeholder="4 digit pin")
    if st.button("login",on_click=next,args=("login", username, str(passd))):
        pass
elif st.session_state.page == "feed":
    placeholder.empty()
    main_page()
