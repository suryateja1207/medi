import subprocess
import sys
import streamlit as st
import os
import requests




# Hugging Face API


def query_hf_assistant(user_input):
    API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
    headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}",
}

    payload = {
        "messages": [{"role": "user", "content": user_input}],
        "model": "meta-llama/Meta-Llama-3-8B-Instruct"
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"





#################################################


from pathlib import Path

def install_from_requirements(requirements_file='requirements.txt'):
    """
    Install packages from a requirements file
    
    Args:
        requirements_file (str): Path to requirements file
    
    Returns:
        bool: True if installation successful, False otherwise
    """
    try:
        # Check if requirements file exists
        if not os.path.exists(requirements_file):
            st.error(f"❌ Requirements file '{requirements_file}' not found!")
            return False
        
        st.info(f"📦 Installing packages from {requirements_file}...")
        
        # Show progress
        with st.spinner("Installing packages..."):
            # Run pip install command
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", requirements_file],
                capture_output=True,
                text=True,
                check=True
            )
        
        st.success("✅ All packages installed successfully!")
        
        # Show installation output (optional)
        if st.checkbox("Show installation details"):
            st.text(result.stdout)
            
        return True
        
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Failed to install packages: {e}")
        st.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return False

def check_and_install_requirements(requirements_file='requirements.txt'):
    """
    Check if packages are installed and install if missing
    
    Args:
        requirements_file (str): Path to requirements file
    """
    try:
        # Read requirements file
        if not os.path.exists(requirements_file):
            st.warning(f"⚠️ Requirements file '{requirements_file}' not found!")
            return
        
        with open(requirements_file, 'r') as f:
            requirements = f.read().strip().split('\n')
        
        # Filter out empty lines and comments
        requirements = [req.strip() for req in requirements 
                      if req.strip() and not req.strip().startswith('#')]
        
        missing_packages = []
        
        # Check each package
        for requirement in requirements:
            # Extract package name (handle versions like package>=1.0.0)
            package_name = requirement.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('!=')[0]
            
            try:
                __import__(package_name)
                st.success(f"✅ {package_name} is already installed")
            except ImportError:
                missing_packages.append(requirement)
                st.warning(f"⚠️ {package_name} is missing")
        
        # Install missing packages
        if missing_packages:
            st.info(f"📦 Found {len(missing_packages)} missing packages")
            
            if st.button("Install Missing Packages"):
                return install_from_requirements(requirements_file)
        else:
            st.success("🎉 All required packages are already installed!")
            
    except Exception as e:
        st.error(f"❌ Error checking requirements: {str(e)}")

def create_requirements_file():
    """
    Create a sample requirements.txt file
    """
    requirements_content = """# Web framework
streamlit>=1.28.0

# Data manipulation
pandas>=2.0.0
numpy>=1.24.0

# Visualization
plotly>=5.15.0

# HTTP requests
requests>=2.31.0

# Additional packages as needed
# matplotlib>=3.7.0
# seaborn>=0.12.0
# scikit-learn>=1.3.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    
    st.success("✅ Sample requirements.txt file created!")

# Alternative: Install specific packages programmatically
def install_specific_packages():
    """
    Install specific packages without requirements file
    """
    required_packages = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "requests>=2.31.0"
    ]
    
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            st.success(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            st.error(f"❌ Failed to install {package}")

# Usage example for your Streamlit app
def main():
    st.title("Package Installation Manager")
    
    # Option 1: Install from requirements file
    st.header("Option 1: Install from Requirements File")
    
    if st.button("Check Requirements"):
        check_and_install_requirements()
    
    if st.button("Force Install from Requirements"):
        install_from_requirements()
    
    # Option 2: Create requirements file
    st.header("Option 2: Create Requirements File")
    
    if st.button("Create Sample Requirements.txt"):
        create_requirements_file()
    
    # Option 3: Install specific packages
    st.header("Option 3: Install Specific Packages")
    
    if st.button("Install Core Packages"):
        install_specific_packages()

if __name__ == "__main__":
    main()
# Page configuration (with error handling)
try:
    st.set_page_config(
        page_title="HealthCare Plus - Your Medical Companion",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except Exception as e:
    # Fallback if page config fails
    print(f"Warning: Could not set page config: {e}")

# Display installation status (only if packages were just installed)
if "packages_installed" not in st.session_state:
    st.session_state.packages_installed = True

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #A23B72;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: black;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .emergency-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "appointments" not in st.session_state:
    st.session_state.appointments = []
if "patient_records" not in st.session_state:
    st.session_state.patient_records = []

# Sidebar navigation
st.sidebar.title("🏥 HealthCare Plus")
st.sidebar.markdown("---")

pages = {
    "🏠 Home": "home",
    "🩺 Symptom Checker": "symptom_checker",
    "📊 Health Calculators": "calculators",
    "📅 Book Appointment": "appointment",
    "📋 Patient Records": "records",
    "📚 Health Information": "health_info",
    "🤖 AI Assistant": "ai_assistant",
    "🚨 Emergency": "emergency",
}

selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
page = pages[selected_page]

# Emergency contact info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 Emergency Contacts")
st.sidebar.markdown("""
- **Emergency**: 911 (US) / 108 (India)
- **Poison Control**: 1-800-222-1222
- **Crisis Hotline**: 988
""")

# Main content based on selected page
if page == "home":
    # Home Page
    st.markdown(
        '<h1 class="main-header">🏥 HealthCare Plus</h1>', unsafe_allow_html=True
    )
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666;">Your comprehensive medical companion for better health management</p>',
        unsafe_allow_html=True,
    )

    # Quick stats/metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Patients Served", "10,000+", "↗️ 15%")
    with col2:
        st.metric("👨‍⚕️ Doctors Available", "150+", "↗️ 8%")
    with col3:
        st.metric("🏥 Partner Hospitals", "25", "↗️ 3")
    with col4:
        st.metric("⭐ Satisfaction Rate", "98.5%", "↗️ 2.1%")

    st.markdown("---")

    # Quick access buttons
    st.markdown('<h2 class="sub-header">Quick Access</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🩺 Check Symptoms", use_container_width=True):
            st.session_state.page = "symptom_checker"
            st.rerun()

    with col2:
        if st.button("📅 Book Appointment", use_container_width=True):
            st.session_state.page = "appointment"
            st.rerun()

    with col3:
        if st.button("📊 Health Calculators", use_container_width=True):
            st.session_state.page = "calculators"
            st.rerun()

    # Health tips
    st.markdown("---")
    st.markdown('<h2 class="sub-header">Daily Health Tips</h2>', unsafe_allow_html=True)

    tips = [
        "💧 Drink at least 8 glasses of water daily",
        "🚶‍♀️ Take a 30-minute walk every day",
        "🥗 Include 5 servings of fruits and vegetables in your diet",
        "😴 Get 7-9 hours of quality sleep",
        "🧘‍♀️ Practice stress management techniques",
        "🏥 Schedule regular health check-ups",
    ]

    for tip in tips:
        st.markdown(f'<div class="info-box">{tip}</div>', unsafe_allow_html=True)

elif page == "symptom_checker":
    st.markdown(
        '<h1 class="main-header">🩺 Symptom Checker</h1>', unsafe_allow_html=True
    )

    st.warning(
        "⚠️ This tool is for informational purposes only. Please consult a healthcare professional for proper diagnosis and treatment."
    )

    # Symptom checker form
    with st.form("symptom_form"):
        st.markdown("### Tell us about your symptoms")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            duration = st.selectbox(
                "How long have you had these symptoms?",
                [
                    "Less than 24 hours",
                    "1-3 days",
                    "4-7 days",
                    "1-2 weeks",
                    "More than 2 weeks",
                ],
            )

        with col2:
            severity = st.selectbox("Symptom severity", ["Mild", "Moderate", "Severe"])
            temperature = st.checkbox("Fever/High temperature")
            pain = st.checkbox("Pain")

        # Symptom selection
        symptoms = st.multiselect(
            "Select your symptoms:",
            [
                "Headache",
                "Fever",
                "Cough",
                "Sore throat",
                "Nausea",
                "Vomiting",
                "Diarrhea",
                "Fatigue",
                "Dizziness",
                "Chest pain",
                "Shortness of breath",
                "Abdominal pain",
                "Back pain",
                "Joint pain",
                "Rash",
                "Swelling",
            ],
        )

        additional_info = st.text_area("Additional information (optional)")

        submitted = st.form_submit_button("Analyze Symptoms")

        if submitted and symptoms:
            st.markdown("---")
            st.markdown("### Analysis Results")

            # Simple symptom analysis (this would be more sophisticated in a real app)
            if "fever" in [s.lower() for s in symptoms] or temperature:
                st.markdown(
                    '<div class="emergency-box">🌡️ <strong>Fever detected:</strong> Monitor temperature and stay hydrated. Consider seeing a doctor if fever persists or exceeds 101°F (38.3°C).</div>',
                    unsafe_allow_html=True,
                )

            if "chest pain" in [s.lower() for s in symptoms]:
                st.markdown(
                    '<div class="emergency-box">🚨 <strong>Chest pain:</strong> This could be serious. Consider seeking immediate medical attention if severe or accompanied by shortness of breath.</div>',
                    unsafe_allow_html=True,
                )

            if severity == "Severe":
                st.markdown(
                    '<div class="emergency-box">⚡ <strong>Severe symptoms:</strong> Consider seeking medical attention promptly.</div>',
                    unsafe_allow_html=True,
                )

            # General recommendations
            st.markdown(
                '<div class="info-box">📋 <strong>General Recommendations:</strong><br>• Rest and stay hydrated<br>• Monitor symptoms<br>• Contact healthcare provider if symptoms worsen<br>• Seek immediate care for severe symptoms</div>',
                unsafe_allow_html=True,
            )

            # Visualization
            if len(symptoms) > 1:
                fig = px.bar(
                    x=symptoms, y=[1] * len(symptoms), title="Reported Symptoms"
                )
                fig.update_layout(showlegend=False, yaxis_title="Presence")
                st.plotly_chart(fig, use_container_width=True)

elif page == "calculators":
    st.markdown(
        '<h1 class="main-header">📊 Health Calculators</h1>', unsafe_allow_html=True
    )

    calculator_type = st.selectbox(
        "Choose a calculator:",
        [
            "BMI Calculator",
            "BMR Calculator",
            "Heart Rate Zones",
            "Water Intake Calculator",
        ],
    )

    if calculator_type == "BMI Calculator":
        st.markdown("### Body Mass Index (BMI) Calculator")

        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input(
                "Weight (kg)", min_value=1.0, max_value=500.0, value=70.0
            )
            height = st.number_input(
                "Height (cm)", min_value=50.0, max_value=250.0, value=170.0
            )

        if weight and height:
            bmi = weight / ((height / 100) ** 2)

            with col2:
                st.metric("Your BMI", f"{bmi:.1f}")

                if bmi < 18.5:
                    category = "Underweight"
                    color = "blue"
                elif 18.5 <= bmi < 25:
                    category = "Normal weight"
                    color = "green"
                elif 25 <= bmi < 30:
                    category = "Overweight"
                    color = "orange"
                else:
                    category = "Obese"
                    color = "red"

                st.markdown(
                    f'<div style="color: {color}; font-weight: bold;">Category: {category}</div>',
                    unsafe_allow_html=True,
                )

            # BMI visualization
            fig = go.Figure()
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=bmi,
                    title={"text": "BMI"},
                    domain={"x": [0, 1], "y": [0, 1]},
                    gauge={
                        "axis": {"range": [None, 40]},
                        "bar": {"color": color},
                        "steps": [
                            {"range": [0, 18.5], "color": "lightblue"},
                            {"range": [18.5, 25], "color": "lightgreen"},
                            {"range": [25, 30], "color": "orange"},
                            {"range": [30, 40], "color": "lightcoral"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 30,
                        },
                    },
                )
            )
            st.plotly_chart(fig, use_container_width=True)

    elif calculator_type == "BMR Calculator":
        st.markdown("### Basal Metabolic Rate (BMR) Calculator")

        col1, col2 = st.columns(2)
        with col1:
            gender_bmr = st.selectbox("Gender", ["Male", "Female"], key="bmr_gender")
            age_bmr = st.number_input(
                "Age", min_value=1, max_value=120, value=30, key="bmr_age"
            )
            weight_bmr = st.number_input(
                "Weight (kg)",
                min_value=1.0,
                max_value=500.0,
                value=70.0,
                key="bmr_weight",
            )
            height_bmr = st.number_input(
                "Height (cm)",
                min_value=50.0,
                max_value=250.0,
                value=170.0,
                key="bmr_height",
            )

        if weight_bmr and height_bmr and age_bmr:
            # Mifflin-St Jeor Equation
            if gender_bmr == "Male":
                bmr = 10 * weight_bmr + 6.25 * height_bmr - 5 * age_bmr + 5
            else:
                bmr = 10 * weight_bmr + 6.25 * height_bmr - 5 * age_bmr - 161

            with col2:
                st.metric("Your BMR", f"{bmr:.0f} calories/day")

                activity_levels = {
                    "Sedentary": 1.2,
                    "Lightly active": 1.375,
                    "Moderately active": 1.55,
                    "Very active": 1.725,
                    "Extremely active": 1.9,
                }

                st.markdown("#### Daily Calorie Needs:")
                for level, multiplier in activity_levels.items():
                    calories = bmr * multiplier
                    st.write(f"**{level}**: {calories:.0f} calories/day")

elif page == "appointment":
    st.markdown(
        '<h1 class="main-header">📅 Book Appointment</h1>', unsafe_allow_html=True
    )

    with st.form("appointment_form"):
        st.markdown("### Schedule Your Appointment")

        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input("Full Name*")
            phone = st.text_input("Phone Number*")
            email = st.text_input("Email Address*")
            age_apt = st.number_input("Age", min_value=1, max_value=120, value=30)

        with col2:
            department = st.selectbox(
                "Department*",
                [
                    "General Medicine",
                    "Cardiology",
                    "Dermatology",
                    "Orthopedics",
                    "Gynecology",
                    "Pediatrics",
                    "Neurology",
                    "Psychiatry",
                ],
            )
            doctor = st.selectbox(
                "Preferred Doctor",
                [
                    "Dr. Smith (General Medicine)",
                    "Dr. Johnson (Cardiology)",
                    "Dr. Brown (Dermatology)",
                    "Dr. Davis (Orthopedics)",
                ],
            )
            appointment_date = st.date_input("Preferred Date", min_value=date.today())
            appointment_time = st.time_input("Preferred Time")

        reason = st.text_area("Reason for Visit")
        insurance = st.checkbox("I have health insurance")

        submitted = st.form_submit_button("Book Appointment")

        if submitted:
            if patient_name and phone and email:
                appointment = {
                    "name": patient_name,
                    "phone": phone,
                    "email": email,
                    "age": age_apt,
                    "department": department,
                    "doctor": doctor,
                    "date": appointment_date,
                    "time": appointment_time,
                    "reason": reason,
                    "insurance": insurance,
                    "status": "Scheduled",
                }

                st.session_state.appointments.append(appointment)
                st.success("✅ Appointment booked successfully!")
                st.balloons()

                # Display appointment details
                st.markdown("### Appointment Confirmation")
                st.markdown(f"**Patient:** {patient_name}")
                st.markdown(f"**Department:** {department}")
                st.markdown(f"**Doctor:** {doctor}")
                st.markdown(
                    f"**Date & Time:** {appointment_date} at {appointment_time}"
                )
                st.markdown(
                    f"**Confirmation ID:** APT-{len(st.session_state.appointments):04d}"
                )
            else:
                st.error("Please fill in all required fields marked with *")

    # Display existing appointments
    if st.session_state.appointments:
        st.markdown("---")
        st.markdown("### Your Appointments")

        df_appointments = pd.DataFrame(st.session_state.appointments)
        st.dataframe(
            df_appointments[["name", "department", "doctor", "date", "time", "status"]],
            use_container_width=True,
        )

elif page == "records":
    st.markdown(
        '<h1 class="main-header">📋 Patient Records</h1>', unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["Add Record", "View Records"])

    with tab1:
        with st.form("patient_record_form"):
            st.markdown("### Add Patient Record")

            col1, col2 = st.columns(2)

            with col1:
                record_name = st.text_input("Patient Name*")
                record_id = st.text_input("Patient ID*")
                blood_group = st.selectbox(
                    "Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
                )
                allergies = st.text_input("Allergies (comma-separated)")

            with col2:
                chronic_conditions = st.text_area("Chronic Conditions")
                medications = st.text_area("Current Medications")
                emergency_contact = st.text_input("Emergency Contact")
                last_checkup = st.date_input("Last Checkup")

            vital_signs = st.checkbox("Add Vital Signs")

            if vital_signs:
                col3, col4 = st.columns(2)
                with col3:
                    bp_systolic = st.number_input(
                        "Blood Pressure (Systolic)",
                        min_value=70,
                        max_value=200,
                        value=120,
                    )
                    bp_diastolic = st.number_input(
                        "Blood Pressure (Diastolic)",
                        min_value=40,
                        max_value=130,
                        value=80,
                    )
                with col4:
                    heart_rate = st.number_input(
                        "Heart Rate (bpm)", min_value=40, max_value=200, value=70
                    )
                    temperature = st.number_input(
                        "Temperature (°F)", min_value=95.0, max_value=110.0, value=98.6
                    )

            submitted_record = st.form_submit_button("Add Record")

            if submitted_record:
                if record_name and record_id:
                    record = {
                        "name": record_name,
                        "patient_id": record_id,
                        "blood_group": blood_group,
                        "allergies": allergies,
                        "chronic_conditions": chronic_conditions,
                        "medications": medications,
                        "emergency_contact": emergency_contact,
                        "last_checkup": last_checkup,
                        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }

                    if vital_signs:
                        record.update(
                            {
                                "bp_systolic": bp_systolic,
                                "bp_diastolic": bp_diastolic,
                                "heart_rate": heart_rate,
                                "temperature": temperature,
                            }
                        )

                    st.session_state.patient_records.append(record)
                    st.success("✅ Patient record added successfully!")
                else:
                    st.error("Please fill in required fields")

    with tab2:
        if st.session_state.patient_records:
            st.markdown("### Patient Records Database")

            # Search functionality
            search_term = st.text_input("Search by patient name or ID:")

            df_records = pd.DataFrame(st.session_state.patient_records)

            if search_term:
                mask = df_records["name"].str.contains(
                    search_term, case=False, na=False
                ) | df_records["patient_id"].str.contains(
                    search_term, case=False, na=False
                )
                df_records = df_records[mask]

            if not df_records.empty:
                st.dataframe(df_records, use_container_width=True)

                # Visualizations
                if "bp_systolic" in df_records.columns:
                    st.markdown("### Vital Signs Overview")

                    col1, col2 = st.columns(2)
                    with col1:
                        fig_bp = px.scatter(
                            df_records,
                            x="name",
                            y=["bp_systolic", "bp_diastolic"],
                            title="Blood Pressure Readings",
                        )
                        st.plotly_chart(fig_bp, use_container_width=True)

                    with col2:
                        fig_hr = px.bar(
                            df_records,
                            x="name",
                            y="heart_rate",
                            title="Heart Rate Readings",
                        )
                        st.plotly_chart(fig_hr, use_container_width=True)
            else:
                st.info("No records found.")
        else:
            st.info("No patient records available. Add some records to get started.")

elif page == "health_info":
    st.markdown(
        '<h1 class="main-header">📚 Health Information</h1>', unsafe_allow_html=True
    )

    info_category = st.selectbox(
        "Choose a category:",
        ["General Health", "Nutrition", "Exercise", "Mental Health", "Preventive Care"],
    )

    if info_category == "General Health":
        st.markdown("""
        ### 🏥 General Health Guidelines
        
        #### Daily Health Habits
        - **Hydration**: Drink 8-10 glasses of water daily
        - **Sleep**: Aim for 7-9 hours of quality sleep
        - **Hygiene**: Regular handwashing and dental care
        - **Stress Management**: Practice relaxation techniques
        
        #### Warning Signs to Watch For
        - Persistent fever above 101°F (38.3°C)
        - Severe headaches or vision changes
        - Chest pain or difficulty breathing
        - Sudden weight loss or gain
        - Changes in bowel or bladder habits
        """)

    elif info_category == "Nutrition":
        st.markdown("""
        ### 🥗 Nutrition Guidelines
        
        #### Balanced Diet Basics
        - **Fruits & Vegetables**: 5-9 servings daily
        - **Whole Grains**: 3-5 servings daily
        - **Protein**: Lean meats, fish, beans, nuts
        - **Dairy**: Low-fat options, 2-3 servings daily
        - **Healthy Fats**: Olive oil, avocados, nuts
        
        #### Foods to Limit
        - Processed and packaged foods
        - Sugary drinks and snacks
        - High-sodium foods
        - Trans fats and saturated fats
        """)

        # Nutrition visualization
        nutrients = ["Carbs", "Protein", "Fats", "Vitamins", "Minerals"]
        percentages = [45, 20, 30, 3, 2]

        fig = px.pie(
            values=percentages,
            names=nutrients,
            title="Recommended Daily Nutrient Distribution",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif info_category == "Exercise":
        st.markdown("""
        ### 🏃‍♀️ Exercise Guidelines
        
        #### Weekly Exercise Recommendations
        - **Cardio**: 150 minutes moderate or 75 minutes vigorous
        - **Strength Training**: 2-3 sessions per week
        - **Flexibility**: Daily stretching or yoga
        - **Balance**: Especially important for older adults
        
        #### Types of Exercise
        - **Aerobic**: Walking, swimming, cycling, dancing
        - **Strength**: Weight lifting, resistance bands, bodyweight
        - **Flexibility**: Stretching, yoga, tai chi
        - **Balance**: Yoga, tai chi, balance exercises
        """)

        # Exercise tracking chart
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cardio = [30, 0, 45, 0, 30, 60, 0]
        strength = [0, 45, 0, 45, 0, 0, 30]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Cardio (min)", x=days, y=cardio))
        fig.add_trace(go.Bar(name="Strength (min)", x=days, y=strength))
        fig.update_layout(title="Sample Weekly Exercise Schedule")
        st.plotly_chart(fig, use_container_width=True)

    elif page == "ai_assistant":
                
        st.write("🛠️ Debug: Entered AI Assistant page")

        try:
            st.write("✅ query_hf_assistant loaded")

            with st.form("ai_assistant_form"):
                user_query = st.text_area("📝 Your question:")
                submitted = st.form_submit_button("Ask")

            if submitted:
                st.write("🛠️ Debug: Button pressed")
                st.write(f"User input: {user_query}")
                response = query_hf_assistant(user_query)
                st.success(response)
        except Exception as e:
            st.error(f"❌ Exception: {e}")


user_input = st.text_area("💬 Ask me anything medical-related:")
if st.button("Ask"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        st.info("Sending to Hugging Face...")
        answer = query_hf_assistant(user_input)
        st.success(answer)

elif page == "emergency":
    st.markdown(
        '<h1 class="main-header">🚨 Emergency Information</h1>', unsafe_allow_html=True
    )

    st.markdown(
        '<div class="emergency-box">⚠️ <strong>If this is a life-threatening emergency, call 911 immediately!</strong></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🚑 When to Call 911
        - Chest pain or heart attack symptoms
        - Difficulty breathing or choking
        - Severe bleeding or trauma
        - Loss of consciousness
        - Severe allergic reactions
        - Stroke symptoms (FAST: Face, Arms, Speech, Time)
        - Severe burns
        - Drug overdose
        """)

        st.markdown("""
        ### 📞 Important Numbers
        - **Emergency Services**: 911 (US) / 108 (India)
        - **Poison Control**: 1-800-222-1222
        - **Crisis/Suicide Hotline**: 988
        - **Non-Emergency Medical**: 311
        """)

    with col2:
        st.markdown("""
        ### 🏥 Nearest Hospitals
        1. **City General Hospital**
           - Distance: 2.1 miles
           - Phone: (555) 123-4567
           - Emergency Room: 24/7
        
        2. **Metro Medical Center**
           - Distance: 3.5 miles
           - Phone: (555) 234-5678
           - Trauma Center: Level 1
        
        3. **Community Health Hospital**
           - Distance: 4.2 miles
           - Phone: (555) 345-6789
           - Pediatric Emergency: Available
        """)

        st.markdown("""
        ### 🚨 First Aid Basics
        - **CPR**: 30 compressions, 2 breaths
        - **Choking**: Heimlich maneuver
        - **Bleeding**: Apply direct pressure
        - **Burns**: Cool water, no ice
        - **Poisoning**: Call Poison Control first
        """)

# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏥 HealthCare Plus - Your trusted medical companion</p>
    <p>⚠️ This application is for informational purposes only and does not replace professional medical advice.</p>
    <p>📞 For emergencies, always call your local emergency number.</p>
</div>
""",
    unsafe_allow_html=True,
)
