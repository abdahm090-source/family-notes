import streamlit as st
import pandas as pd
import os

# إعدادات الواجهة
st.set_page_config(page_title="مغسلة العائلة", page_icon="🧺", layout="centered")

# تصميم الواجهة لتناسب الجوال واللغة العربية
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-testid="stBlock"] { direction: rtl; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; height: 3em; }
    .laundry-card { padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; background-color: #ffffff; color: #333; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .urgent { color: red; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧺 كشف ملابس المغسلة")

DB_FILE = "laundry_notes.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "نوع الملابس", "العدد", "نوع الخدمة"])

def save_item(name, item_type, count, service):
    df = load_data()
    new_entry = {"الاسم": name, "نوع الملابس": item_type, "العدد": count, "نوع الخدمة": service}
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# نموذج إضافة ملابس
with st.expander("➕ إضافة أغراض للمغسلة", expanded=True):
    # الخيارات المطلوبة
    family_members = ["دلول", "نصور", "عبود", "الوالدة"]
    service_types = [
        "غسيل وكوي عادي", 
        "غسيل وكوي مستعجل", 
        "كوي عادي", 
        "كوي مستعجل"
    ]
    
    name = st.selectbox("صاحب الملابس:", family_members)
    item_type = st.text_input("وش الملابس؟ (مثلاً: ثياب، قمصان)")
    count = st.number_input("العدد:", min_value=1, step=1)
    service = st.radio("نوع الخدمة:", service_types)
    
    if st.button("إضافة إلى الكشف"):
        if item_type:
            save_item(name, item_type, count, service)
            st.success(f"تمت إضافة ملابس {name}")
            st.rerun()
        else:
            st.error("يرجى كتابة نوع الملابس")

st.divider()

# عرض الكشف الحالي
st.subheader("📋 كشف الملابس الحالي")
df = load_data()

if not df.empty:
    for _, row in df.iterrows():
        # تمييز المستعجل بلون مختلف
        is_urgent = "مستعجل" in row['نوع الخدمة']
        service_style = "class='urgent'" if is_urgent else ""
        
        st.markdown(f"""
        <div class="laundry-card">
            <strong>👤 {row['الاسم']}</strong><br>
            👕 {row['نوع الملابس']} : {row['العدد']} قطع<br>
            <span {service_style}>⚡ {row['نوع الخدمة']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write(f"**إجمالي القطع المودعة:** {df['العدد'].sum()}")
    
    # ميزة الـ Restart
    st.divider()
    if st.button("🗑️ تم الاستلام والدفع (تصفير الكشف)"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.success("تم تصفير الكشف. الله يعطيك العافية!")
            st.rerun()
else:
    st.info("لا توجد ملابس مسجلة حالياً.")
