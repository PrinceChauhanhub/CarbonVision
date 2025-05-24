import streamlit as st
import matplotlib.pyplot as plt
import pdfkit
import tempfile
import os
import base64
import re
from datetime import datetime
import platform

# Path to wkhtmltopdf executable
if platform.system() == "Windows":
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
else:
    path_wkhtmltopdf = "/usr/bin/wkhtmltopdf"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Save matplotlib figure as base64 image
def fig_to_base64(fig):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
        fig.savefig(tmpfile.name, bbox_inches='tight')
        tmpfile_path = tmpfile.name

    with open(tmpfile_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    os.unlink(tmpfile_path)
    plt.close(fig)

    return f"data:image/png;base64,{encoded}"

# Helper to clean emojis (for PDF)
def clean_emojis(html):
    replacements = {
        "📊": "📊",
        "🌱": "🌱",
        "🚶‍♂️": "🚶‍♂️",
        "🚗": "🚗",
        "🗑": "🗑",
        "⚡": "⚡",
        "🛒": "🛒",
        "📋": "📋",
        "✈️": "✈️",
        "♻️": "♻️",
    }
    for emoji, text in replacements.items():
        html = html.replace(emoji, text)

    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )
    html = emoji_pattern.sub("", html)
    return html

def show_dashboard():
    st.title("📊 Your Personalized Carbon Footprint Dashboard")

    if "input_data" not in st.session_state:
        st.error("No data available. Please calculate your carbon footprint first.")
        st.stop()

    input_data = st.session_state.input_data
    prediction = st.session_state.prediction

    # Estimated Carbon Footprint
    st.metric(label="🌱 Estimated Carbon Footprint", value=f"{prediction:.2f} units")

    # --- Personal Section ---
    st.header("🚶‍♂️ Personal Profile")

    gender = input_data.get('gender', 'Unknown')
    body_type = input_data.get('body_type', 'Unknown')
    social_activity = input_data.get('social_activity', 'Unknown')
    diet = input_data.get('diet', 'Unknown')
    shower_frequency = input_data.get('shower_frequency', 'Unknown')

    st.write(f"**Sex**: {gender}")
    st.write(f"**Body Type**: {body_type}")

    # Feedback for personal profile
    st.write(f"**Diet**: {diet}")
    if diet.lower() in ['vegan', 'vegetarian']:
        diet_feedback = "Great diet choice! You're helping the environment by eating plant-based."
        st.success(f" {diet_feedback}")
    elif diet.lower() in ['pescatarian']:
        diet_feedback = "Good diet choice! But consider eating more plant-based meals."
        st.info(f" {diet_feedback}")
    else:
        diet_feedback = "Eating more plant-based meals can lower your carbon footprint."
        st.warning(f" {diet_feedback}")
        
    st.write(f"**Social Activity**: {social_activity}")
    if social_activity.lower() == "never":
        social_feedback = "Low social activity can indirectly reduce travel emissions. Nice!"
        st.success(f" {social_feedback}")
    else:
        social_feedback = "Active social life? Try carpooling or using public transport for outings."
        st.info(f" {social_feedback}")
        
    st.write(f"**Shower Frequency**: {shower_frequency}")
    if shower_frequency.lower() in ['once a day', 'less frequently']:
        shower_feedback = "Good shower habits! Saving water and energy."
        st.success(f" {shower_feedback}")
    else:
        shower_feedback = "Try reducing shower frequency or duration to save water."
        st.warning(f" {shower_feedback}")

    # --- Transport Section ---
    st.header("🚗 Transport Overview")
    vehicle_distance = input_data.get('vehicle_monthly_distance_km', 0)
    st.write(f"**Vehicle Monthly Distance**: {vehicle_distance} km")

    # Improved Vehicle Distance Graph
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.bar(['Monthly Travel by Person'], [vehicle_distance], color='green', width=0.5)
    ax1.set_ylabel("Distance Travelled (km)")
    ax1.set_title("Distance Travel by Person Via Vehicle")
    ax1.set_ylim(0, max(vehicle_distance * 1.2, 100))  # Set a reasonable y-limit
    st.pyplot(fig1)
    vehicle_graph_base64 = fig_to_base64(fig1)
    
    if vehicle_distance > 1000:
        vehicle_feedback = "High vehicle usage detected. Consider carpooling or biking more often."
        st.warning(f"🚗 {vehicle_feedback}")
    else:
        vehicle_feedback = "Great! Your vehicle usage is within a reasonable range."
        st.success(f"🚗 {vehicle_feedback}")

    air_travel = input_data.get('air_travel_frequency', 'never')
    st.write(f"**Air Travel Frequency**: {air_travel}")

    # Feedback for transport
    if air_travel.lower() in ["frequently", "very frequently"]:
        air_feedback = "Frequent air travel significantly increases your footprint. Reduce if possible."
        st.error(f"✈️ {air_feedback}")
    else:
        air_feedback = "Low air travel! Good for minimizing emissions."
        st.success(f"✈️ {air_feedback}")

    # --- Waste Management ---
    st.header("🗑 Waste Management")
    waste_bag_count = input_data.get('waste_bag_weekly_count', 0)
    recycling_raw = input_data.get('recycling', [])
    if isinstance(recycling_raw, str):
        import ast
        try:
            recycling = ast.literal_eval(recycling_raw)
        except:
            recycling = []
    else:
        recycling = recycling_raw

    st.write(f"**Waste Bags per Week**: {waste_bag_count}")
    st.write(f"**Recycling Materials**: {', '.join(recycling) if recycling else 'None'}")

    waste_labels = ['Waste Bags per Week', 'Recycling Materials']
    waste_values = [waste_bag_count, len(recycling)]

    fig2, ax2 = plt.subplots()
    ax2.bar(waste_labels, waste_values, color=['orange', 'lightgreen'])
    ax2.set_ylabel("Count")
    ax2.set_title("Waste and Recycling Overview")
    st.pyplot(fig2)
    waste_graph_base64 = fig_to_base64(fig2)

    # Feedback for waste
    if waste_bag_count > 5:
        waste_feedback = "You produce a lot of waste weekly. Try composting and reducing waste."
        st.warning(f"🗑 {waste_feedback}")
    else:
        waste_feedback = "Excellent! You are producing a small amount of waste."
        st.success(f"🗑 {waste_feedback}")

    if recycling:
        recycling_feedback = "Good job recycling materials!"
        st.success(f"♻️ {recycling_feedback}")
    else:
        recycling_feedback = "Start recycling to contribute to waste reduction."
        st.warning(f"♻️ {recycling_feedback}")

    # --- Energy Usage ---
    st.header("⚡ Energy Usage")
    heating_energy = input_data.get('heating_energy_source', 'Unknown')
    energy_efficiency = input_data.get('energy_efficiency', 'Unknown')
    tv_pc_hours = input_data.get('tv_pc_daily_hours', 0)
    internet_hours = input_data.get('internet_daily_hours', 0)

    st.write(f"**Heating Energy Source**: {heating_energy}")
    # Feedback for energy
    if heating_energy.lower() in ['electricity', 'natural gas']:
        heating_feedback = "Great eco-friendly heating source!"
        st.success(f"🔋 {heating_feedback}")
    else:
        heating_feedback = "Consider switching to renewable heating if possible."
        st.warning(f"⚡ {heating_feedback}")

    st.write(f"**Energy Efficiency Devices**: {energy_efficiency}")
    if energy_efficiency.lower() == "yes":
        efficiency_feedback = "Awesome! Energy-efficient devices reduce carbon footprint."
        st.success(f"💡 {efficiency_feedback}")
    else:
        efficiency_feedback = "Try investing in energy-efficient appliances."
        st.warning(f"💡 {efficiency_feedback}")

    st.write(f"**Daily PC/TV Hours**: {tv_pc_hours} hours")
    if tv_pc_hours > 5:
        tv_pc_feedback = "Too much screen time! Reduce PC/TV usage to save electricity."
        st.warning(f"🖥 {tv_pc_feedback}")
    else:
        tv_pc_feedback = "Good! Your screen time is moderate."
        st.success(f"🖥 {tv_pc_feedback}")
        
    st.write(f"**Daily Internet Hours**: {internet_hours} hours")
    if internet_hours > 8:
        internet_feedback = "High internet usage. Consider reducing time online to save energy."
        st.warning(f"🖥 {internet_feedback}")
    else:
        internet_feedback = "Good! Your internet usage is moderate."
        st.success(f"🖥 {internet_feedback}")
        
    # --- Consumption Section ---
    st.header("🛒 Consumption")

    grocery_bill = input_data.get('monthly_grocery_bill', 0)
    clothes_bought = input_data.get('new_clothes_monthly', 0)

    st.write(f"**Monthly Grocery Bill**: ${grocery_bill}")
    st.write(f"**New Clothes Bought Monthly**: {clothes_bought} items")

    # Feedback for consumption
    if grocery_bill > 54:
        grocery_feedback = "High grocery bill! Consider buying local and seasonal products."
        st.warning(f" {grocery_feedback}")
    else:
        grocery_feedback = "Good job managing your grocery expenses."
        st.success(f" {grocery_feedback}")

    if clothes_bought > 5:
        clothes_feedback = "Buying many clothes monthly can increase your carbon footprint. Buy mindfully."
        st.warning(f" {clothes_feedback}")
    else:
        clothes_feedback = "Minimal clothing purchases. Good for sustainability!"
        st.success(f" {clothes_feedback}")

    # --- Generate PDF Button ---
    st.subheader("📋 Download Your Full Report")
    if st.button("Generate & Download PDF"):
        # Generate a complete HTML report with all dashboard data
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Carbon Footprint Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2E7D32; text-align: center; }}
                h2 {{ color: #1976D2; margin-top: 20px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
                .metric {{ font-size: 24px; font-weight: bold; color: #2E7D32; text-align: center; margin: 20px 0; }}
                .success {{ color: green; }}
                .warning {{ color: orange; }}
                .error {{ color: red; }}
                .info {{ color: blue; }}
                img {{ max-width: 100%; height: auto; margin: 10px 0; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <h1>Your Personalized Carbon Dashboard</h1>
            <p>Report generated on {datetime.now().strftime('%B %d, %Y')}</p>
            
            <div class="metric">Estimated Carbon Footprint: {prediction:.2f} units</div>
            
            <h2>Personal Profile</h2>
            <p><strong>Sex:</strong> {gender}</p>
            <p><strong>Body Type:</strong> {body_type}</p>
            <p><strong>Diet:</strong> {diet}</p>
            <p class="{'success' if diet.lower() in ['vegan', 'vegetarian'] else 'info' if diet.lower() in ['pescatarian'] else 'warning'}">{diet_feedback}</p>
            
            <p><strong>Social Activity:</strong> {social_activity}</p>
            <p class="{'success' if social_activity.lower() == 'never' else 'info'}">{social_feedback}</p>
            
            <p><strong>Shower Frequency:</strong> {shower_frequency}</p>
            <p class="{'success' if shower_frequency.lower() in ['once a day', 'less frequently'] else 'warning'}">{shower_feedback}</p>
            
            <h2>Transport Overview</h2>
            <p><strong>Vehicle Monthly Distance:</strong> {vehicle_distance} km</p>
            <img src="{vehicle_graph_base64}" alt="Vehicle Distance Graph">
            <p class="{'success' if vehicle_distance <= 700 else 'warning'}">{vehicle_feedback}</p>
            
            <p><strong>Air Travel Frequency:</strong> {air_travel}</p>
            <p class="{'success' if air_travel.lower() not in ['frequently', 'very frequently'] else 'error'}">{air_feedback}</p>
            
            <h2>Waste Management</h2>
            <p><strong>Waste Bags per Week:</strong> {waste_bag_count}</p>
            <p><strong>Recycling Materials:</strong> {', '.join(recycling) if recycling else 'None'}</p>
            <img src="{waste_graph_base64}" alt="Waste Management Graph">
            <p class="{'success' if waste_bag_count <= 5 else 'warning'}">{waste_feedback}</p>
            <p class="{'success' if recycling else 'warning'}">{recycling_feedback}</p>
            
            <h2>Energy Usage</h2>
            <p><strong>Heating Energy Source:</strong> {heating_energy}</p>
            <p class="{'success' if heating_energy.lower() in ['electricity', 'natural gas'] else 'warning'}">{heating_feedback}</p>
            
            <p><strong>Energy Efficiency Devices:</strong> {energy_efficiency}</p>
            <p class="{'success' if energy_efficiency.lower() == 'yes' else 'warning'}">{efficiency_feedback}</p>
            
            <p><strong>Daily PC/TV Hours:</strong> {tv_pc_hours} hours</p>
            <p class="{'success' if tv_pc_hours <= 5 else 'warning'}">{tv_pc_feedback}</p>
            
            <p><strong>Daily Internet Hours:</strong> {internet_hours} hours</p>
            <p class="{'success' if internet_hours <= 8 else 'warning'}">{internet_feedback}</p>
            
            <h2>Consumption</h2>
            <p><strong>Monthly Grocery Bill:</strong> ${grocery_bill}</p>
            <p class="{'success' if grocery_bill <= 54 else 'warning'}">{grocery_feedback}</p>
            
            <p><strong>New Clothes Bought Monthly:</strong> {clothes_bought} items</p>
            <p class="{'success' if clothes_bought <= 5 else 'warning'}">{clothes_feedback}</p>
            
            <h2>Recommendations for Reducing Your Carbon Footprint</h2>
            <ul>
                <li>Consider reducing meat consumption or adopting a more plant-based diet</li>
                <li>Use public transportation, carpooling, or biking instead of driving alone</li>
                <li>Reduce waste by composting food scraps and recycling more materials</li>
                <li>Invest in energy-efficient appliances and LED lighting</li>
                <li>Reduce water usage with shorter showers and water-saving fixtures</li>
                <li>Buy local and seasonal products to reduce transportation emissions</li>
                <li>Choose sustainable and durable clothing options, shop less frequently</li>
            </ul>
            
            <div class="footer">
                <p>This report is generated based on your provided information. For a more detailed analysis, consult with an environmental expert.</p>
            </div>
        </body>
        </html>
        """

        cleaned_html_report = clean_emojis(html_report)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_html:
            tmp_html.write(cleaned_html_report.encode('utf-8'))
            tmp_html_path = tmp_html.name

        pdf_path = tmp_html_path.replace('.html', '.pdf')
        
        try:
            pdfkit.from_file(tmp_html_path, pdf_path, configuration=config, options={'enable-local-file-access': ''})
            
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Report as PDF",
                    data=pdf_file,
                    file_name="carbon_dashboard_report.pdf",
                    mime="application/pdf"
                )
            
            st.success("PDF generated successfully! Click the button above to download.")
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            st.info("If using Windows, please make sure wkhtmltopdf is installed at the specified path.")
        finally:
            # Clean up temporary files
            if os.path.exists(tmp_html_path):
                os.unlink(tmp_html_path)
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)

if __name__ == "__main__":
    show_dashboard()