import streamlit as st
from PIL import Image
from utils.predictor import predict
from utils.advisor import get_advice

st.set_page_config(
    page_title="Crop Disease Detector",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 Crop Disease Detection System")
st.markdown("Upload a leaf photo to get instant disease diagnosis and treatment advice.")
st.divider()

uploaded_file = st.file_uploader(
    "Upload a leaf image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Uploaded leaf", use_container_width=True)
    
    with col2:
        with st.spinner("Analyzing leaf..."):
            result = predict(image)
        
        confidence = result["confidence"]
        
        if confidence < 50:
            st.warning("⚠️ Image unclear. Please upload a clearer leaf photo.")
        else:
            if result["disease"].lower() == "healthy":
                st.success(f"✅ This {result['crop']} leaf appears **healthy**!")
            else:
                st.error(f"🔴 Disease Detected")
            
            st.metric("Crop", result["crop"])
            st.metric("Disease", result["disease"])
            st.metric("Confidence", f"{confidence}%")
    
    if confidence >= 50 and result["disease"].lower() != "healthy":
        st.divider()
        st.subheader("📋 Treatment Advisory")
        
        with st.spinner("Getting expert advice..."):
            advice = get_advice(result["crop"], result["disease"], confidence)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.info(f"**🦠 Cause**\n\n{advice['cause']}")
            st.warning(f"**⚡ Immediate Action**\n\n{advice['immediate_action']}")
        
        with col4:
            st.success(f"**💊 Treatment**\n\n{advice['treatment']}")
            st.info(f"**🛡️ Prevention**\n\n{advice['prevention']}")
        
        st.divider()
        st.subheader("اردو خلاصہ")
        st.markdown(f"### {advice['urdu_summary']}")