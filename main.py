import streamlit as st
import pandas as pd
import os

# إعدادات الواجهة
st.set_page_config(page_title="مغسلة العائلة", page_icon="🧺", layout="centered")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 10px; }
    .laundry-card { padding: 15px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 10px; background-color: #f9f9f9; color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧺 كشف ملابس المغسلة")

DB_FILE = "laundry_notes.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "نوع الملابس", "العدد"])

def save_item(name, item_type, count):
    df = load_data()
    new_entry = {"الاسم": name, "نوع الملابس": item_type, "العدد": count}
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# نموذج إضافة ملابس
with st.expander("➕ إضافة ملابس جديدة", expanded=True):
    name = st.selectbox("من صاحب الملابس؟", ["أنا", "الوالد", "الوالدة", "أخي", "أختي"])
    item_type = st.text_input("وش الملابس؟ (مثلاً: ثياب، قمصان، قطع)")
    count = st.number_input("كم عددها؟", min_value=1, step=1)
    
    if st.button("إضافة للكشف"):
        if item_type:
            save_item(name, item_type, count)
            st.success("تمت الإضافة")
            st.rerun()

st.divider()

# عرض الكشف الحالي
st.subheader("📋 الكشف الحالي")
df = load_data()

if not df.empty:
    for _, row in df.iterrows():
        st.markdown(f"""
        <div class="laundry-card">
            <strong>👤 {row['الاسم']}</strong><br>
            👔 {row['نوع الملابس']} : {row['العدد']} قطع
        </div>
        """, unsafe_allow_html=True)
    
    st.write(f"**إجمالي القطع:** {df['العدد'].sum()}")
    
    # ميزة الـ Restart (تصفير البيانات)
    st.divider()
    if st.button("🗑️ تم الدفع واستلام الملابس (تصفير الكشف)"):
        # حذف الملف لعمل ريستارت
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.success("تم تصفير الكشف بنجاح! جاهزون للأسبوع القادم.")
            st.rerun()
else:
    st.info("الكشف فارغ حالياً. لا توجد ملابس للمغسلة.")
