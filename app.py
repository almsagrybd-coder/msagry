import streamlit as st
from google import genai
from google.genai import types

# إعداد عنوان الصفحة وشكلها
st.set_page_config(page_title="شات المصاقري", page_icon="🤖")
st.title("🤖 شات المصاقري الذكي")
st.write("مرحباً بك! اسألني عن أي شيء وسأجيبك فوراً.")

# مفتاح الأمان المباشر للتجربة المحلية
API_KEY = "AIzaSyC7P2NrHsRb4A3MJS13ZNWbp6k3cGtZ9dQ"

# إنشاء اتصال نشط مع السيرفر في كل لقطة تحديث
client = genai.Client(api_key=API_KEY)

# إنشاء قائمة لتخزين وعرض تاريخ المحادثة على الشاشة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة على الشاشة ليظهر كشات حقيقي
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# استقبال سؤال جديد من المستخدم
if user_question := st.chat_input("اكتب سؤالك هنا..."):
    # 1. عرض سؤال المستخدم فوراً وحفظه في الذاكرة
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "text": user_question})

    # 2. بناء هيكل المحادثة بالكامل (التاريخ + السؤال الحالي) في قائمة واحدة
    formatted_contents = []
    for msg in st.session_state.messages:
        role_label = "user" if msg["role"] == "user" else "model"
        formatted_contents.append(
            types.Content(role=role_label, parts=[types.Part.from_text(text=msg["text"])])
        )

    # 3. إرسال المحادثة بالكامل دفعة واحدة بطريقة مضمونة ومستقرة
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=formatted_contents, # تمرير كامل السياق هنا ليحفظ الذاكرة
                config=types.GenerateContentConfig(
                    system_instruction="أنت 'شات المصاقري'، مساعد ذكي ومطور برمجيات محترف. نحن الآن في عام 2026، إجاباتك دقيقة ومحدثة وتخاطب أصدقاء المطور عبد الرحمن المصاقري بكل ود واحترام."
                )
            )
            st.markdown(response.text)
    
    # 4. حفظ إجابة البوت في الذاكرة ليراها المستخدم في المرة القادمة
    st.session_state.messages.append({"role": "assistant", "text": response.text})