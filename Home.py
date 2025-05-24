import streamlit as st
import base64

# Set page config
st.set_page_config(page_title="About Carbon Footprint", layout="centered")
st.title("Carbon Emission")

# Function to get base64 string of the image
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Background image
img_path = "Images/background_min.jpg"
img_base64 = get_base64(img_path)

# Inject CSS
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

.container {{
    background-color: rgba(255, 255, 255, 0.85);
    padding: 3rem;
    border-radius: 20px;
    margin: auto;
    max-width: 900px;
    font-family: 'Arial', sans-serif;
    color: #333;
}}

[data-testid="stSidebar"] {{
    background-color: black;
    color: #333;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Main content
st.markdown('<div class="container">', unsafe_allow_html=True)

st.markdown("### 🌳 **About Carbon Footprint**")
st.write(
    "🌱 **Carbon Vision** is an intelligent application that predicts your carbon footprint based on your daily lifestyle activities. "
    "From your travel habits to energy consumption, it helps you understand your environmental impact and guides you toward sustainable choices."
)

st.markdown("### 🌳 **Why It Matters**")
st.subheader("🌿 **Climate Impact**")
st.write("Reducing your carbon footprint is a crucial step in the fight against climate change. The carbon emissions we release into the atmosphere contribute to the greenhouse effect, which leads to global warming and the disruption of weather patterns. By making small, everyday changes, you directly contribute to mitigating the impact of climate change, helping to preserve ecosystems, wildlife, and the health of the planet. Carbon Vision plays a key role by showing you exactly how much you’re contributing and providing guidance on how to lessen that impact.")

st.subheader("🌿 **Resource Conservation**")
st.write("Cutting down on carbon emissions often means using fewer natural resources, such as fossil fuels, water, and raw materials. By reducing energy consumption, opting for more sustainable transportation options, and minimizing waste, you help conserve precious resources that are vital for sustaining life on Earth. When we use resources more efficiently, we help reduce the strain on ecosystems and ensure that these resources remain available for future generations.")

st.subheader("🌿 **Health and Well-being**")
st.write("Lowering emissions isn’t just about the environment—it also promotes healthier lifestyle choices. Sustainable practices such as walking, cycling, eating locally, and using less energy can improve your overall health. For example, reducing car travel lowers pollution, leading to cleaner air, which in turn benefits respiratory health. Additionally, promoting more plant-based diets and sustainable food practices can lead to better nutrition, reduced health risks, and increased well-being. Lower emissions mean healthier people and healthier communities.")

st.subheader("🌿 **Sustainable Practices**")
st.write("By actively working to reduce carbon emissions, you contribute to the wider adoption of sustainable practices in society. These practices help conserve the environment, prevent depletion of natural resources, and protect biodiversity. Whether it’s reducing waste, choosing renewable energy, or supporting eco-friendly businesses, each choice you make helps shift society toward sustainability. Carbon Vision encourages these choices by making it easy for users to see the benefits of their actions and understand the positive changes they are making in the world.")

st.subheader("🌿 **Responsibility**")
st.write("Taking responsibility for reducing emissions is more than just an individual effort—it’s about fostering a culture of environmental awareness and accountability. By tracking your carbon footprint and making informed decisions, you take a proactive role in tackling climate change. It’s a collective responsibility that extends beyond personal actions to include communities, businesses, and governments. Carbon Vision helps you track this responsibility, making it easier to stay accountable and continuously improve your environmental impact.")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation button
if st.button("➡️ Track your Carbon Footprint!"):
    st.switch_page("pages/01_CarbonFootprint.py")
