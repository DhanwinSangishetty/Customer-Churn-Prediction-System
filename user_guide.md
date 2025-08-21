# 👤 User Guide - Customer Churn Predictor

## 🚀 Getting Started

### What This Tool Does
- Predicts which customers might leave your service
- Provides actionable recommendations to keep customers
- Analyzes business data with SQL reports
- Helps plan retention campaigns

---

## 🔍 How to Use Each Feature

### **Single Customer Prediction**
1. Navigate to "Single Customer" tab
2. Fill in the customer information
3. Click "Predict Churn Risk"
4. Review the risk level and recommendations

**When to Use:** 
- Customer calls with concerns
- Before contract renewal meetings
- Planning account reviews

### **Batch Customer Analysis**
1. Navigate to "Batch Prediction" tab  
2. Upload your CSV file with customer data
3. Click "Analyze All Customers"
4. Download results for your team

**When to Use:**
- Monthly retention campaigns
- Quarterly business reviews
- Marketing list preparation

### **SQL Business Analytics**
1. Navigate to "SQL Analysis" tab
2. Click "Refresh Database" 
3. Click "Run Business Analysis"
4. Review the reports and insights

**When to Use:**
- Executive reporting
- Identifying trends and patterns
- Strategic planning sessions

### **Model Insights**
1. Navigate to "Model Insights" tab
2. Review the feature importance chart
3. Read the business explanations

**When to Use:**
- Understanding what causes churn
- Training team members
- Strategy development

---

## 📊 Understanding the Results

### Risk Levels
- 🔴 **High Risk (60-100%)**: Contact within 48 hours
- 🟡 **Medium Risk (30-60%)**: Monitor and engage proactively  
- 🟢 **Low Risk (0-30%)**: Focus on upselling opportunities

### Recommended Actions

#### For High-Risk Customers:
- Personal phone call from account manager
- Offer retention discount (10-20%)
- Schedule satisfaction review meeting
- Escalate to senior staff if needed

#### For Medium-Risk Customers:
- Send personalized email campaigns
- Offer service upgrades or add-ons
- Conduct satisfaction survey
- Add to loyalty program

#### For Low-Risk Customers:
- Send appreciation messages
- Present upselling opportunities
- Request referrals or testimonials
- Use for case studies

---

## 🛠️ Troubleshooting

### Common Issues

**CSV Upload Problems:**
- Make sure your CSV has all required columns
- Check that data matches the expected format
- Remove special characters or extra spaces

**Prediction Errors:**
- Verify all numerical fields contain only numbers
- Ensure no critical fields are empty
- Check data quality and formatting

**SQL Analysis Not Working:**
- Make sure the CSV file is accessible
- Try refreshing the database
- Check that SQLite is working properly

### Getting Help
1. Check the error message for specific guidance
2. Review your data format requirements
3. Try with the provided sample data first
4. Contact technical support if issues persist

---

## 💡 Best Practices

### Daily Usage
- Check high-risk customers from recent interactions
- Use predictions during customer service calls
- Update retention actions in your CRM

### Weekly/Monthly Usage
- Run batch analysis on your customer base
- Export results for marketing campaigns
- Review SQL analytics for business trends

### Strategic Usage
- Use insights for business planning
- Share analytics with leadership team
- Adjust strategies based on findings

---

## 📋 Data Requirements

### Required Columns for CSV Upload
- customerID, gender, SeniorCitizen, Partner, Dependents
- tenure, PhoneService, MultipleLines, InternetService
- Contract, PaperlessBilling, PaymentMethod  
- MonthlyCharges, TotalCharges
- Plus service columns: OnlineSecurity, OnlineBackup, etc.

### Data Format Tips
- Use exact column names as shown
- Ensure categorical values match training data
- Keep numerical fields clean (no $ signs or commas)
- Remove empty rows or missing critical data

---

## 📞 Support

For questions or issues:
- Review this user guide and troubleshooting section
- Check the main README.md for technical details
- See qa_test_plan.md for testing procedures
- See implementation_guide.md for setup details

---

**Quick Reference Card:**

| Task | Steps | Expected Time |
|------|-------|---------------|
| Single prediction | Fill form → Click predict → Review results | 2-3 minutes |
| Batch analysis | Upload CSV → Click analyze → Download results | 5-10 minutes |
| SQL insights | Refresh DB → Run analysis → Review reports | 3-5 minutes |
| Troubleshooting | Check error → Review format → Try again | 5-15 minutes |

**Remember:** This tool is designed to help you make data-driven decisions about customer retention. The predictions are guidance to help prioritize your efforts - always combine with your business knowledge and customer relationships.