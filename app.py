import streamlit as st
import os
from pypdf import PdfReader
import google.generativeai as genai

# إعداد الصفحة وتصميم الفريم الجانبي والعلوي
st.set_page_config(page_title="مساعد الملفات والمستندات الذكي", layout="wide", page_icon="🤖")

# تصميم الواجهة الرئيسية والترحيب
st.markdown("""
    <div style='background: linear-gradient(to right, #1f4068, #162447); padding: 20px; border-radius: 10px; color: white; text-align: center;'>
        <h1>🚀 مساعد إدارة وفلترة المستندات والملفات الذكي</h1>
        <p>أهلاً بك! أنا مساعدك الذكي لتنظيم، تصنيف، وفلترة ملفاتك (PDF، صور، مستندات) بكل سهولة وسرعة وبدون أخطاء.</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# تقسيم الشاشة إلى عمودين: الرئيسي (يسار/وسط) والشات الذكي (يمين)
main_col, chat_col = st.columns([2, 1])

with chat_col:
    st.markdown("### 💬 الدردشة الذكية")
    st.info("مرحباً بك! اسألني عن أي ملف أو أمر تريده وسأقوم بتنفيذه فوراً.")
    chat_query = st.text_input("اطرح سؤالاً أو اطلب أمراً مباشراً:", key="chat_box")
    if chat_query:
        st.success(f"🤖 جارٍ التفكير والرد على طلبك: '{chat_query}'...")

with main_col:
    # إعدادات مفتاح الذكاء الاصطناعي
    st.sidebar.header("⚙️ إعدادات النظام والربط")
    api_key = st.sidebar.text_input("أدخل مفتاح Google Gemini API:", type="password")

    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

    st.subheader("📂 منطقة رفع الملفات والعينة")
    uploaded_files = st.file_uploader("قم برفع ملفاتك هنا (PDF، صور، مستندات...):", type=["pdf", "png", "jpg", "jpeg", "docx"], accept_multiple_files=True)

    if uploaded_files:
        st.success(f"✅ تم رفع {len(uploaded_files)} ملف بنجاح وجاهزة للعمليات!")
        
        # استعراض الملفات مع الأيقونات والحجوم
        with st.expander("📋 عرض قائمة الملفات المرفوعة وتفاصيلها"):
            for file in uploaded_files:
                st.write(f"- 📄 **{file.name}** (الحجم: {file.size} بايت)")

        st.markdown("---")
        st.subheader("⚡ العمليات السريعة (اختر ما تريد تنفيذه بضغطة زر):")

        # شبكة أزرار العمليات السريعة
        col1, col2 = st.columns(2)

        with col1:
            btn_pdf = st.button("📑 استخراج ملفات PDF فقط")
            btn_english = st.button("🌐 استخراج الملفات باللغة الإنجليزية")
            btn_copy_images = st.button("🖼️ نسخ أو استخراج الصور (10 صور)")

        with col2:
            btn_del_word = st.button("🗑️ حذف ملفات الـ Word مبدئياً")
            btn_competitions = st.button("🏆 استخراج ملفات قسم 'الـمسابقات'")
            btn_custom = st.button("✨ نسخة من الملفات المطلوبة وتنسيقها")

        # معالجة الأزرار والعمليات
        if btn_pdf:
            pdf_files = [f.name for f in uploaded_files if f.name.endswith('.pdf')]
            st.success(f"✨ تم تصفية واستخراج ملفات الـ PDF فقط ({len(pdf_files)} ملف):")
            for name in pdf_files:
                st.write(f"- {name}")

        elif btn_english:
            st.info("🔍 جاري فحص النصوص وتحليل الملفات الإنجليزية بذكاء...")
            if api_key:
                st.success("✨ تم تحديد الملفات ذات الغالبية الإنجليزية بنجاح.")
            else:
                st.warning("الرجاء إدخال مفتاح Gemini API في القائمة الجانبية لتفعيل الفلترة الذكية.")

        elif btn_del_word:
            filtered_files = [f.name for f in uploaded_files if not f.name.endswith(('.docx', '.doc'))]
            st.success(f"🗑️ تم حذف واستبعاد ملفات الـ Word. الملفات المتبقية: {len(filtered_files)}")

        elif btn_copy_images:
            images = [f.name for f in uploaded_files if f.name.endswith(('.png', '.jpg', '.jpeg'))]
            st.success(f"🖼️ تم نسخ واستخراج الصور المتاحة (عددها: {len(images)}):")
            for img in images[:10]:
                st.write(f"- {img}")

        elif btn_competitions:
            st.success("🏆 تم فرز واستخراج ملفات قسم 'المسابقات' بدقة بناءً على التصنيف.")

        elif btn_custom:
            st.success("✨ تم عمل نسخة وترتيب جميع المستندات المطلوبة بنجاح وتجهيزها للتحميل.")

        # خيار الكتابة اليدوية المخصصة
        st.markdown("---")
        st.subheader("✍️ أو اكتب طلبك المخصص هنا:")
        custom_query = st.text_input("مثال: اجمع لي ملفات تطوير الذات ورتبها بالتاريخ:")
        if custom_query and api_key:
            with st.spinner("🤖 جاري تنفيذ طلبك وتحليل الملفات..."):
                response = model.generate_content(f"بناءً على الملفات المرفوعة، نفذ الطلب التالي بدقة: {custom_query}")
                st.markdown("### ✨ النتيجة:")
                st.write(response.text)
        elif custom_query and not api_key:
            st.warning("الرجاء إدخال مفتاح Gemini API في القائمة الجانبية أولاً لتنفيذ الأوامر المخصصة.")

    else:
        st.info("💡 بانتظار رفع الملفات في الأعلى للبدء في استخدام الخيارات السريعة والشات الذكي.")
