import streamlit as st
import streamlit_shadcn_ui as ui
import time
import main
import uuid
import dbcreator as db

def notification(value: str):
    values = ('already_exists', 'blocked', 'unblocked')
    if value == values[0]:
        st.toast(f'Already Exists: {input_value}',icon='🚫')
    if value == values[1]:
        st.toast(f'Blocked: {input_value}',icon='✋')
    if value == values[2]:
        st.toast(f'UnBlocked: {input_value}',icon='🔓')

st.header("Web Blocker")

# st.logo(
#     image=r"../icons/app_blocking.png", size="large", link=None, icon_image=None
# )
st.sidebar.write("Instructions")

if "rows" not in st.session_state:
    ids = db.get_uuids()
    st.session_state["rows"] = []
    print(ids)
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

input_value = ui.input(default_value="", type='text', placeholder="Enter text here", key="input1")

blocked = ui.button("Click", key="clk_btn")

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