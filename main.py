import streamlit as st
import pandas as pd
from datetime import datetime
import os

# إعدادات الواجهة لتظهر بشكل احترافي
st.set_page_config(page_title="ملاحظات العائلة", page_icon="🏠", layout="centered")

# تصميم الواجهة باستخدام CSS بسيط لتحسين الخطوط والألوان
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    .note-card { padding: 15px; border-radius: 10px; border: 1px solid #444; margin-bottom: 10px; background-color: #1e1e1e; }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 مجلس العائلة الرقمي")
st.write("اكتب ملاحظتك ليراها الجميع")

# قاعدة البيانات (ملف CSV)
DB_FILE = "family_notes.csv"

def load_notes():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["التاريخ", "الاسم", "الملاحظة"])

def save_note(name, text):
    df = load_notes()
    new_note = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "الاسم": name,
        "الملاحظة": text
    }
    df = pd.concat([df, pd.DataFrame([new_note])], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# القسم الخاص بإضافة ملاحظة جديدة
with st.expander("➕ أضف ملاحظة جديدة", expanded=True):
    user_name = st.text_input("اسمك")
    note_content = st.text_area("ماذا يدور في ذهنك؟")
    if st.button("نشر الملاحظة"):
        if user_name and note_content:
            save_note(user_name, note_content)
            st.success("تم النشر!")
            st.rerun() # لإعادة تحديث الصفحة وعرض الملاحظة فوراً
        else:
            st.warning("يرجى ملء جميع الخانات")

st.divider()

# عرض الملاحظات السابقة بتصميم "بطاقات"
st.subheader("📌 آخر التحديثات")
notes_df = load_notes()

if not notes_df.empty:
    # عرض الأحدث أولاً
    for _, row in notes_df.iloc[::-1].iterrows():
        st.markdown(f"""
        <div class="note-card">
            <small style="color: #888;">{row['التاريخ']}</small><br>
            <strong>👤 {row['الاسم']}:</strong>
            <p style="margin-top: 5px;">{row['الملاحظة']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("لا توجد ملاحظات بعد. كن أول من يكتب!")
