# Quality Assurance Test Plan
## Customer Churn Prediction Application

**Project**: Telco Customer Churn Predictor  
**Version**: 1.0  
**Date**: August 2025  
**Tester**: Implementation Analyst  

---

## 📋 Test Overview

### Objectives
- Verify all application features work correctly
- Ensure data accuracy and model reliability
- Validate user experience and error handling
- Confirm business requirements are met

### Scope
- Single customer prediction functionality
- Batch prediction with CSV upload
- Model insights and reporting
- SQL analysis components
- User interface and navigation

---

## 🧪 Test Cases

### **TC001: Application Startup**
- **Priority**: Critical
- **Description**: Verify application loads without errors
- **Prerequisites**: All model files present
- **Steps**:
  1. Navigate to project directory
  2. Run `streamlit run churn_app.py`
  3. Open browser to localhost:8501
- **Expected Result**: App loads with welcome message, no error messages
- **Status**: ⏳ Pending

### **TC002: Model Loading**
- **Priority**: Critical
- **Description**: Verify AI model loads correctly
- **Steps**:
  1. Start application
  2. Check for model loading messages
  3. Verify no error popups appear
- **Expected Result**: 
  - Model, encoders, and feature names load successfully
  - No "Model files not found" error
- **Status**: ⏳ Pending

### **TC003: Single Customer Prediction - Valid Data**
- **Priority**: High
- **Description**: Test single customer prediction with valid inputs
- **Test Data**:
  - Gender: Female
  - Senior Citizen: No
  - Partner: Yes
  - Tenure: 12 months
  - Monthly Charges: $75.00
  - Contract: Month-to-month
  - Payment Method: Electronic check
- **Steps**:
  1. Navigate to "Single Customer" tab
  2. Fill in all required fields with test data
  3. Click "Predict Churn Risk"
- **Expected Result**:
  - Risk level displayed (High/Medium/Low)
  - Probability percentage shown
  - Actionable recommendations provided
- **Status**: ⏳ Pending

### **TC004: Single Customer Prediction - Edge Cases**
- **Priority**: Medium
- **Description**: Test with boundary values
- **Test Cases**:
  - Minimum tenure (0 months)
  - Maximum tenure (72+ months)
  - Very high monthly charges ($200+)
  - Very low monthly charges ($20)
- **Expected Result**: Valid predictions for all edge cases
- **Status**: ⏳ Pending

### **TC005: Batch Prediction - Valid CSV**
- **Priority**: High
- **Description**: Test CSV upload with valid customer data
- **Test Data**: Create test CSV with 5 customers
- **Steps**:
  1. Navigate to "Batch Prediction" tab
  2. Upload valid CSV file
  3. Click "Run Batch Prediction"
- **Expected Result**:
  - File uploads successfully
  - Predictions generated for all customers
  - Results table displays with risk levels
  - Download button available
- **Status**: ⏳ Pending

### **TC006: Batch Prediction - Invalid CSV**
- **Priority**: High
- **Description**: Test error handling with invalid CSV
- **Test Cases**:
  - Empty CSV file
  - CSV with missing columns
  - CSV with invalid data types
  - Non-CSV file upload
- **Expected Result**: Clear error messages, no app crash
- **Status**: ⏳ Pending

### **TC007: Model Insights Display**
- **Priority**: Medium
- **Description**: Verify feature importance chart loads
- **Steps**:
  1. Navigate to "Model Insights" tab
  2. Check feature importance chart
  3. Verify explanations are shown
- **Expected Result**:
  - Chart displays correctly
  - Top features are highlighted
  - Business explanations provided
- **Status**: ⏳ Pending

### **TC008: SQL Analysis Functionality**
- **Priority**: High
- **Description**: Test SQL analysis components
- **Steps**:
  1. Navigate to SQL Analysis section
  2. Click "Refresh Database"
  3. Click "Run Business Analysis"
- **Expected Result**:
  - Database creates successfully  
  - SQL queries execute without errors
  - Business insights display in tables
- **Status**: ⏳ Pending

### **TC009: Help Documentation**
- **Priority**: Low
- **Description**: Verify help content is useful
- **Steps**:
  1. Navigate to "Help & Tips" tab
  2. Review all help sections
- **Expected Result**: Clear, helpful documentation for users
- **Status**: ⏳ Pending

### **TC010: Data Validation**
- **Priority**: High
- **Description**: Verify predictions are reasonable
- **Test Method**: Manual validation of known customer profiles
- **Sample Tests**:
  - New customer, month-to-month → Should be High Risk
  - Long-term customer, 2-year contract → Should be Low Risk
- **Expected Result**: Predictions align with business logic
- **Status**: ⏳ Pending

---

## 🐛 Defect Log

| ID | Date | Severity | Description | Status | Resolution |
|----|------|----------|-------------|---------|------------|
| DEF001 | 2025-08-20 | Medium | Model loading takes >30 seconds | Open | Investigating |
| DEF002 | 2025-08-20 | Low | Chart colors not colorblind-friendly | Open | Enhancement planned |

---

## 📊 Test Results Summary

| Test Category | Total | Passed | Failed | Pending |
|---------------|-------|--------|---------|---------|
| Critical | 2 | 0 | 0 | 2 |
| High | 4 | 0 | 0 | 4 |
| Medium | 3 | 0 | 0 | 3 |
| Low | 1 | 0 | 0 | 1 |
| **TOTAL** | **10** | **0** | **0** | **10** |

---

## ✅ Test Environment

- **Operating System**: Windows 11 / macOS / Linux
- **Python Version**: 3.8+
- **Browser**: Chrome 91+, Firefox 89+, Safari 14+
- **Dependencies**: streamlit, pandas, scikit-learn, matplotlib

---

## 🚀 User Acceptance Criteria

### Must Have (Critical)
- [ ] Application starts without errors
- [ ] Single customer predictions are accurate
- [ ] Batch CSV processing works reliably
- [ ] SQL analysis provides business insights

### Should Have (High Priority)
- [ ] Error messages are user-friendly
- [ ] Performance is acceptable (<5 seconds for predictions)
- [ ] Results can be exported/downloaded

### Nice to Have (Medium Priority)
- [ ] Charts are visually appealing
- [ ] Help documentation is comprehensive
- [ ] Mobile-responsive design

---

## 📝 Test Execution Notes

**Execution Instructions**:
1. Run all Critical tests first
2. Document any failures immediately
3. Take screenshots of defects
4. Record actual vs expected results
5. Note performance metrics

**Sign-off Requirements**:
- All Critical tests must pass
- No more than 2 High-priority defects
- Performance within acceptable limits
- Business stakeholder approval

---

**Test Plan Approved By**: Implementation Analyst  
**Review Date**: August 20, 2025  
**Next Review**: Before production deployment