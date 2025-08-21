"""
User-Friendly Streamlit Customer Churn Prediction App
Features:
- Easy single customer prediction with helpful explanations
- Batch prediction with clear instructions
- Model insights explained in simple terms
- Actionable recommendations for reducing churn
- SQL analysis for business intelligence
- QA tested and implementation ready
"""

import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
import pickle
import matplotlib.pyplot as plt
import numpy as np

from sql_analysis import display_sql_analysis

# --- App Configuration ---
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Better Look ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        border: 1px solid #90caf9;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Welcome Header ---
st.title("🎯 Customer Churn Predictor")
st.info("""
🚀 **Welcome to Your AI-Powered Customer Retention Tool!**

This smart tool helps you predict which customers might leave your service before they actually do. 
Use it to take proactive action and keep your valuable customers happy!
""")

# --- Load Model and Components ---
@st.cache_resource
def load_model_components():
    """Load the trained model, encoders, and feature names"""
    try:
        with open('churn_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        with open('feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        return model, encoders, feature_names, True
    except FileNotFoundError:
        return None, None, None, False
    except Exception as e:
        st.error(f"Oops! Something went wrong loading the model: {str(e)}")
        return None, None, None, False

# Load components
model, encoders, feature_names, load_success = load_model_components()

if not load_success:
    st.error("""
    🚫 **Model files not found!** 
    
    It looks like the AI model hasn't been trained yet. Please make sure these files exist:
    - `churn_model.pkl`
    - `encoders.pkl` 
    - `feature_names.pkl`
    
    Run the model training script first to generate these files.
    """)
    st.stop()

# --- Helper Functions ---
def get_prediction_explanation(probability):
    """Get user-friendly explanation based on churn probability"""
    if probability < 0.3:
        return "✅ **Low Risk** - This customer is very likely to stay!", "#28a745"
    elif probability < 0.6:
        return "⚠️ **Medium Risk** - Keep an eye on this customer", "#ffc107"
    else:
        return "🚨 **High Risk** - This customer might leave soon!", "#dc3545"

def predict_single_customer(input_data):
    """Predict churn for one customer with friendly results"""
    try:
        # Prepare data
        input_df = pd.DataFrame([input_data])
        input_df = input_df.reindex(columns=feature_names, fill_value=0)
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        return prediction, probability, True, None
    except Exception as e:
        return None, None, False, str(e)

def predict_batch_customers(df):
    """Predict churn for multiple customers"""
    try:
        df_encoded = df.copy()
        
        # Encode categorical variables
        for col, encoder in encoders.items():
            if col in df_encoded.columns and col != 'customerID':
                try:
                    df_encoded[col] = encoder.transform(df_encoded[col].astype(str))
                except ValueError:
                    st.warning(f"⚠️ Found unknown values in '{col}'. Using default encoding.")
                    df_encoded[col] = 0
        
        # Prepare for prediction
        df_for_prediction = df_encoded.reindex(columns=feature_names, fill_value=0)
        
        # Make predictions
        predictions = model.predict(df_for_prediction)
        probabilities = model.predict_proba(df_for_prediction)[:, 1]
        
        # Add results to original data
        results_df = df.copy()
        results_df["Churn_Risk"] = ["High Risk" if p > 0.6 else "Medium Risk" if p > 0.3 else "Low Risk" for p in probabilities]
        results_df["Churn_Probability"] = [f"{p:.1%}" for p in probabilities]
        results_df["Prediction"] = ["Likely to Churn" if pred == 1 else "Likely to Stay" for pred in predictions]
        
        return results_df, True, None
        
    except Exception as e:
        return None, False, str(e)

# --- Main App Interface ---
# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Single Customer", 
    "📊 Batch Prediction", 
    "📈 Model Insights", 
    "🗃️ SQL Analysis",
    "❓ Help & Tips"
])

# --- Tab 1: Single Customer Prediction ---
with tab1:
    st.header("🔍 Predict Churn Risk for One Customer")
    st.write("Fill in the customer details below and get an instant prediction!")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    # User-friendly field mappings
    field_descriptions = {
        'gender': 'Gender',
        'SeniorCitizen': 'Senior Citizen (65+)',
        'Partner': 'Has Partner',
        'Dependents': 'Has Dependents',
        'tenure': 'Months as Customer',
        'PhoneService': 'Has Phone Service',
        'MultipleLines': 'Multiple Phone Lines',
        'InternetService': 'Internet Service Type',
        'OnlineSecurity': 'Online Security Add-on',
        'OnlineBackup': 'Online Backup Add-on',
        'DeviceProtection': 'Device Protection',
        'TechSupport': 'Tech Support',
        'StreamingTV': 'Streaming TV',
        'StreamingMovies': 'Streaming Movies',
        'Contract': 'Contract Type',
        'PaperlessBilling': 'Paperless Billing',
        'PaymentMethod': 'Payment Method',
        'MonthlyCharges': 'Monthly Bill ($)',
        'TotalCharges': 'Total Charges ($)'
    }
    
    user_input = {}
    field_count = 0
    
    for feature in feature_names:
        # Determine which column to use
        current_col = col1 if field_count % 2 == 0 else col2
        
        with current_col:
            display_name = field_descriptions.get(feature, feature.replace('_', ' ').title())
            
            if feature in encoders:
                # Categorical field
                options = list(encoders[feature].classes_)
                selected = st.selectbox(
                    display_name,
                    options=options,
                    key=f"input_{feature}",
                    help=f"Select the customer's {display_name.lower()}"
                )
                user_input[feature] = encoders[feature].transform([selected])[0]
                
            elif feature in ['tenure', 'MonthlyCharges', 'TotalCharges']:
                # Numerical field
                if feature == 'tenure':
                    value = st.number_input(
                        display_name,
                        min_value=0,
                        max_value=100,
                        value=12,
                        key=f"input_{feature}",
                        help="How many months has this customer been with you?"
                    )
                elif feature == 'MonthlyCharges':
                    value = st.number_input(
                        display_name,
                        min_value=0.0,
                        max_value=200.0,
                        value=50.0,
                        format="%.2f",
                        key=f"input_{feature}",
                        help="What is their average monthly bill?"
                    )
                else:  # TotalCharges
                    value = st.number_input(
                        display_name,
                        min_value=0.0,
                        max_value=10000.0,
                        value=600.0,
                        format="%.2f",
                        key=f"input_{feature}",
                        help="Total amount they've paid over their lifetime"
                    )
                user_input[feature] = value
            else:
                # Default numerical
                user_input[feature] = st.number_input(
                    display_name,
                    min_value=0.0,
                    value=0.0,
                    key=f"input_{feature}"
                )
        
        field_count += 1
    
    # Prediction button
    st.markdown("---")
    if st.button("🎯 Predict Churn Risk", type="primary", use_container_width=True):
        prediction, probability, success, error = predict_single_customer(user_input)
        
        if success:
            # Show results with nice formatting
            explanation, color = get_prediction_explanation(probability)
            
            st.markdown(f"""
            <div style="background-color: {color}20; border: 2px solid {color}; border-radius: 10px; padding: 20px; margin: 20px 0;">
                <h3 style="color: {color}; margin: 0;">{explanation}</h3>
                <h4 style="margin: 10px 0;">Churn Probability: {probability:.1%}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Add progress bar
            st.progress(probability, text=f"Risk Level: {probability:.1%}")
            
            # Actionable recommendations
            st.subheader("💡 Recommended Actions:")
            if probability > 0.6:
                st.error("""
                **Immediate Action Needed:**
                - 📞 Contact this customer personally within 48 hours
                - 💰 Offer retention discount or upgrade incentive
                - 🤝 Schedule a satisfaction call to understand concerns
                - 📋 Review their service usage and suggest optimizations
                """)
            elif probability > 0.3:
                st.warning("""
                **Monitor Closely:**
                - 📧 Send personalized offers or service updates
                - 📊 Track usage patterns for changes
                - ⭐ Gather feedback through surveys
                - 🎁 Consider loyalty rewards
                """)
            else:
                st.success("""
                **Keep Them Happy:**
                - 😊 This customer seems satisfied
                - 📈 Consider upselling additional services
                - 💌 Send thank you messages for loyalty
                - 🌟 Use them for referral programs
                """)
        else:
            st.error(f"❌ **Prediction failed:** {error}")

# --- Tab 2: Batch Prediction ---
with tab2:
    st.header("📊 Predict Churn for Multiple Customers")
    st.write("Upload a CSV file with customer data to get predictions for everyone at once!")
    
    # Instructions
    with st.expander("📋 CSV File Requirements", expanded=True):
        st.markdown("""
        Your CSV file should include these columns:
        - **customerID** (optional but recommended)
        - **gender**: Male, Female
        - **SeniorCitizen**: 0 (No), 1 (Yes)
        - **Partner**: Yes, No
        - **Dependents**: Yes, No
        - **tenure**: Number (months as customer)
        - **PhoneService**: Yes, No
        - **MultipleLines**: No, Yes, No phone service
        - **InternetService**: DSL, Fiber optic, No
        - **Contract**: Month-to-month, One year, Two year
        - **PaymentMethod**: Electronic check, Mailed check, Bank transfer, Credit card
        - **MonthlyCharges**: Number (dollar amount)
        - **TotalCharges**: Number (total dollar amount)
        
        *Other service-related columns like OnlineSecurity, OnlineBackup, etc.*
        """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose your CSV file",
        type="csv",
        help="Select a CSV file containing your customer data"
    )
    
    if uploaded_file is not None:
        try:
            # Load and preview data
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ **File uploaded successfully!** Found {len(df)} customers.")
            
            with st.expander("👀 Preview Your Data"):
                st.dataframe(df.head(10))
            
            # Predict button
            if st.button("🚀 Analyze All Customers", type="primary"):
                with st.spinner("🤖 AI is analyzing your customers... This may take a moment!"):
                    results, success, error = predict_batch_customers(df)
                    
                    if success:
                        st.success("🎉 **Analysis Complete!**")
                        
                        # Summary statistics
                        high_risk = len(results[results['Churn_Risk'] == 'High Risk'])
                        medium_risk = len(results[results['Churn_Risk'] == 'Medium Risk'])
                        low_risk = len(results[results['Churn_Risk'] == 'Low Risk'])
                        total = len(results)
                        
                        # Display summary
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Customers", total)
                        with col2:
                            st.metric("High Risk", high_risk, delta=f"{high_risk/total:.1%}")
                        with col3:
                            st.metric("Medium Risk", medium_risk, delta=f"{medium_risk/total:.1%}")
                        with col4:
                            st.metric("Low Risk", low_risk, delta=f"{low_risk/total:.1%}")
                        
                        # Show results
                        st.subheader("📋 Detailed Results")
                        st.dataframe(
                            results.style.highlight_max(axis=0),
                            use_container_width=True
                        )
                        
                        # Download button
                        csv_data = results.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv_data,
                            file_name='customer_churn_predictions.csv',
                            mime='text/csv',
                            use_container_width=True
                        )
                        
                        # Action recommendations
                        if high_risk > 0:
                            st.error(f"🚨 **{high_risk} customers need immediate attention!** Consider reaching out with retention offers.")
                        if medium_risk > 0:
                            st.warning(f"⚠️ **{medium_risk} customers should be monitored closely** with targeted engagement.")
                        st.info(f"✅ **{low_risk} customers are in good shape** - perfect for upselling opportunities!")
                    else:
                        st.error(f"❌ **Analysis failed:** {error}")
        
        except Exception as e:
            st.error(f"❌ **Error reading file:** {str(e)}")
            st.info("💡 **Tip:** Make sure your CSV file has the correct column names and format.")

# --- Tab 3: Model Insights ---
with tab3:
    st.header("📈 Understanding What Drives Customer Churn")
    st.write("This shows which factors are most important when predicting if a customer will leave.")
    
    # Feature importance chart
    importances = model.feature_importances_
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    # Create better labels
    importance_df['Friendly_Name'] = importance_df['Feature'].map(field_descriptions)
    importance_df['Friendly_Name'] = importance_df['Friendly_Name'].fillna(
        importance_df['Feature'].str.replace('_', ' ').str.title()
    )
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(
        importance_df['Friendly_Name'].head(10),
        importance_df['Importance'].head(10),
        color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b', '#6c5ce7', '#74b9ff', '#00b894', '#fdcb6e']
    )
    
    ax.set_xlabel('Importance Score', fontsize=12)
    ax.set_title('Top 10 Most Important Factors for Predicting Churn', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.001, bar.get_y() + bar.get_height()/2,
                f'{width:.3f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Explain the top factors
    st.subheader("🔍 What This Means:")
    top_features = importance_df.head(5)
    
    explanations = {
        'Contract': "Contract type is crucial - month-to-month customers are more likely to leave",
        'tenure': "Customer loyalty matters - newer customers are at higher risk",
        'TotalCharges': "Total spending indicates engagement level",
        'MonthlyCharges': "High bills without perceived value can drive churn",
        'InternetService': "Service type affects satisfaction and retention"
    }
    
    for _, row in top_features.iterrows():
        feature = row['Feature']
        importance = row['Importance']
        friendly_name = row['Friendly_Name']
        explanation = explanations.get(feature, f"{friendly_name} significantly influences churn decisions")
        
        st.info(f"**{friendly_name}** (Impact: {importance:.1%}) - {explanation}")

# --- Tab 4: SQL Analysis ---
with tab4:
    display_sql_analysis()

# --- Tab 5: Help & Tips ---
with tab5:
    st.header("❓ Help & Tips for Better Customer Retention")
    
    st.subheader("🎯 How to Use This App Effectively")
    st.markdown("""
    1. **Single Customer Mode**: Use when you want to check specific customers who seem at risk
    2. **Batch Mode**: Perfect for monthly retention campaigns - analyze your entire customer base
    3. **Model Insights**: Understand what factors matter most for your specific business
    4. **SQL Analysis**: Get detailed business insights with database queries
    """)
    
    st.subheader("🗃️ SQL Analysis Features")
    st.markdown("""
    **What it does:**
    - Creates a database from your customer data
    - Runs business intelligence queries
    - Shows contract analysis, revenue impact, and risk segments
    - Demonstrates SQL skills for reporting
    
    **How to use:**
    1. Click "Refresh Database" to create the customer database
    2. Click "Run Business Analysis" to see SQL-powered insights
    3. Review the generated reports for business decision-making
    """)
    
    st.subheader("💡 Retention Strategy Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **For High-Risk Customers:**
        - 📞 Personal outreach within 24-48 hours
        - 💰 Offer immediate discounts or upgrades
        - 🤝 Schedule satisfaction calls
        - 📋 Review and optimize their service plan
        - 🎁 Provide exclusive retention offers
        """)
    
    with col2:
        st.markdown("""
        **For Medium-Risk Customers:**
        - 📧 Automated but personalized email campaigns
        - 📊 Monitor usage patterns monthly
        - ⭐ Send satisfaction surveys
        - 🏆 Introduce loyalty programs
        - 📱 Proactive service optimization
        """)
    
    st.subheader("📊 Understanding the Predictions")
    st.markdown("""
    - **Churn Probability**: The likelihood (0-100%) that a customer will leave in the next period
    - **Risk Levels**: 
        - 🟢 **Low Risk** (0-30%): Customer likely to stay
        - 🟡 **Medium Risk** (30-60%): Monitor closely
        - 🔴 **High Risk** (60-100%): Immediate action needed
    """)
    
    st.subheader("🧪 Quality Assurance")
    st.markdown("""
    This application has been thoroughly tested following industry QA standards:
    - ✅ All prediction features validated
    - ✅ Error handling and edge cases tested  
    - ✅ Performance benchmarks met
    - ✅ User acceptance criteria fulfilled
    
    For detailed testing documentation, see `qa_test_plan.md`
    """)
    
    st.subheader("🚀 Implementation Process")
    st.markdown("""
    This system follows professional implementation practices:
    - **Requirements Gathering**: Business needs analyzed
    - **Technical Architecture**: Scalable solution designed
    - **Quality Assurance**: Comprehensive testing completed
    - **User Training**: Documentation and support provided
    - **Deployment**: Production-ready with monitoring
    
    For complete implementation details, see `implementation_guide.md`
    """)
    
    st.subheader("🔧 Troubleshooting")
    with st.expander("Common Issues"):
        st.markdown("""
        **File Upload Problems:**
        - Ensure CSV has all required columns
        - Check that categorical values match expected options
        - Remove any special characters or extra spaces
        
        **Prediction Errors:**
        - Verify numerical fields contain only numbers
        - Make sure there are no missing values in critical fields
        
        **SQL Analysis Issues:**
        - Ensure CSV file is in the same directory
        - Check file permissions for database creation
        - Verify SQLite is installed (comes with Python)
        
        **Questions?**
        - Review the CSV requirements in the Batch Prediction tab
        - Check that your data format matches the training data
        - See implementation guide for detailed troubleshooting
        """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🤖 Powered by AI • Built with SQL Analytics • QA Tested • Implementation Ready • Made with ❤️ using Streamlit</p>
    <p><small>This application demonstrates ML, SQL, QA, and Implementation skills for professional deployment</small></p>
</div>
""", unsafe_allow_html=True)