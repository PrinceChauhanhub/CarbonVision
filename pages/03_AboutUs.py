import streamlit as st

# Custom CSS for centering and styling
st.markdown("""
    <style>
    .team-member {
        text-align: center;
    }
    .team-member img {
        width: 130px;  /* Adjusted width for all team members' images */
        border-radius: 50%;
    }
    .supervisor {
        text-align: center;
        margin-bottom: 20px;  /* Space below the supervisor's section */
    }
    .supervisor img {
        width: 80px;  /* Reduced the size of professor's image to 80px */
        border-radius: 50%;
        margin-bottom: 10px;  /* Space between image and text */
    }
    .linkedin-link {
        color: #0A66C2;  /* LinkedIn blue */
    }
    </style>
""", unsafe_allow_html=True)

# Under the supervision section (Placed at the top)
st.write("### This Project is Developed Under the supervision of")

# Centralized supervisor photo and name with custom CSS class
st.markdown('<div class="supervisor">', unsafe_allow_html=True)
st.image("Images/shiva_sir.jpg", width=180)  # Fixed the issue by removing the height argument
st.write("**Dr. Shiva Prakash**")
st.write("**Professor, Department of ITCA, MMMUT**")
st.markdown("[LinkedIn](https://www.linkedin.com/in/dr-shiva-prakash-080a0856/)", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Team members section below the professor
st.header("By Our Team")

# Create a horizontal layout for team members
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="team-member">', unsafe_allow_html=True)
    st.image("Images/prince.jpg", width=130)
    st.write("**Prince Chauhan**")
    st.write("Roll No: 2023073042")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/princechauhan22/)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="team-member">', unsafe_allow_html=True)
    st.image("Images/sanskrati.jpeg", width=130)
    st.write("**Sanskrati Mishra**")
    st.write("Roll No: 2023073052")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/sanskrati-mishra-13b94b21b/)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="team-member">', unsafe_allow_html=True)
    st.image("Images/shivam.jpeg", width=170)
    st.write("**Shivam Sahu**")
    st.write("Roll No: 2023073059")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/shivam-sahu91/)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
