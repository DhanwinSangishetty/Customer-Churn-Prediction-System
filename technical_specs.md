# 🔧 Technical Specifications
## Customer Churn Prediction System

**Version**: 1.0  
**Date**: August 2025  
**Document Type**: Technical Architecture  
**Audience**: Developers, System Architects, IT Teams

---

## 🏗️ System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Interface │    │  Business Logic  │    │   Data Layer    │
│   (Streamlit)   │◄──►│   (Python ML)    │◄──►│  (SQLite/CSV)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        ▲                        ▲                        ▲
        │                        │                        │
   User Requests            ML Predictions           Data Storage
```

### Component Overview
| Component | Technology | Purpose | Dependencies |
|-----------|------------|---------|--------------|
| **Frontend** | Streamlit 1.28+ | Web UI & user interaction | streamlit, matplotlib |
| **ML Engine** | scikit-learn 1.3+ | Prediction algorithms | pandas, numpy, pickle |
| **Database** | SQLite 3 | Analytics & reporting | sqlite3, pandas |
| **Data Processing** | pandas 2.0+ | Data manipulation | numpy, python-dateutil |

---

## 📊 Data Architecture

### Data Flow Diagram
```
CSV Upload → Data Validation → Feature Engineering → Model Prediction → Results Display
     ▲              ▲                    ▲                 ▲              ▲
   User Input   Format Check       Encoding/Scaling   ML Algorithm   User Interface
```

### Database Schema

#### Customer Data Table
```sql
CREATE TABLE customers (
    customerID TEXT PRIMARY KEY,
    gender TEXT,
    SeniorCitizen INTEGER,
    Partner TEXT,
    Dependents TEXT,
    tenure INTEGER,
    PhoneService TEXT,
    MultipleLines TEXT,
    InternetService TEXT,
    OnlineSecurity TEXT,
    OnlineBackup TEXT,
    DeviceProtection TEXT,
    TechSupport TEXT,
    StreamingTV TEXT,
    StreamingMovies TEXT,
    Contract TEXT,
    PaperlessBilling TEXT,
    PaymentMethod TEXT,
    MonthlyCharges REAL,
    TotalCharges REAL,
    Churn TEXT
);
```

#### Predictions Table
```sql
CREATE TABLE predictions (
    prediction_id INTEGER PRIMARY KEY,
    customerID TEXT,
    churn_probability REAL,
    risk_level TEXT,
    prediction_date DATETIME,
    model_version TEXT,
    FOREIGN KEY (customerID) REFERENCES customers(customerID)
);
```

---

## 🤖 Machine Learning Architecture

### Model Specifications
| Parameter | Value | Justification |
|-----------|-------|---------------|
| **Algorithm** | Random Forest | Handles mixed data types well, interpretable |
| **Estimators** | 100 trees | Balance between performance and speed |
| **Max Depth** | 10 | Prevents overfitting while maintaining accuracy |
| **Random State** | 42 | Ensures reproducible results |

### Feature Engineering Pipeline
1. **Data Cleaning**: Handle missing values, data type conversion
2. **Categorical Encoding**: Label encoding for categorical variables
3. **Feature Selection**: Use all available customer attributes
4. **Model Training**: Random Forest with cross-validation
5. **Model Persistence**: Save model, encoders, and feature names

### Model Files Structure
```
models/
├── churn_model.pkl      # Trained Random Forest model
├── encoders.pkl         # Label encoders for categorical data
└── feature_names.pkl    # List of feature names for prediction
```

---

## 🗃️ SQL Analytics Architecture

### Business Intelligence Queries

#### Customer Segmentation Analysis
```sql
-- Segment customers by risk level and contract type
SELECT 
    Contract,
    CASE 
        WHEN avg_churn_prob > 0.6 THEN 'High Risk'
        WHEN avg_churn_prob > 0.3 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_segment,
    customer_count,
    avg_monthly_revenue,
    total_revenue_at_risk
FROM (
    SELECT 
        Contract,
        AVG(churn_probability) as avg_churn_prob,
        COUNT(*) as customer_count,
        AVG(MonthlyCharges) as avg_monthly_revenue,
        SUM(CASE WHEN churn_probability > 0.6 THEN MonthlyCharges ELSE 0 END) as total_revenue_at_risk
    FROM customer_predictions
    GROUP BY Contract
) segments;
```

#### Revenue Impact Analysis
```sql
-- Calculate potential revenue loss by service type
SELECT 
    InternetService,
    COUNT(*) as total_customers,
    SUM(CASE WHEN churn_probability > 0.6 THEN MonthlyCharges * 12 ELSE 0 END) as annual_revenue_at_risk,
    AVG(churn_probability) as avg_risk_score
FROM customer_predictions
GROUP BY InternetService
ORDER BY annual_revenue_at_risk DESC;
```

---

## 🔄 API Specifications

### Internal Function APIs

#### Single Prediction API
```python
def predict_single_customer(input_data: dict) -> tuple:
    """
    Predict churn for single customer
    
    Args:
        input_data (dict): Customer features as key-value pairs
        
    Returns:
        tuple: (prediction, probability, success, error_message)
            - prediction (int): 0 or 1 (stay or churn)
            - probability (float): Churn probability 0-1
            - success (bool): Whether prediction succeeded
            - error_message (str): Error details if failed
    """
```

#### Batch Prediction API
```python
def predict_batch_customers(df: pandas.DataFrame) -> tuple:
    """
    Predict churn for multiple customers
    
    Args:
        df (pandas.DataFrame): Customer data with required columns
        
    Returns:
        tuple: (results_df, success, error_message)
            - results_df (DataFrame): Original data + predictions
            - success (bool): Whether prediction succeeded
            - error_message (str): Error details if failed
    """
```

#### SQL Analysis API
```python
def run_churn_analysis_queries() -> dict:
    """
    Execute business intelligence queries
    
    Returns:
        dict: Analysis results with keys:
            - 'contract_analysis': Contract performance DataFrame
            - 'revenue_impact': Revenue analysis DataFrame
            - 'risk_segments': Customer segments DataFrame
            - 'service_analysis': Service utilization DataFrame
    """
```

---

## 🔧 Configuration Management

### Environment Variables
```python
# Application configuration
APP_TITLE = "Customer Churn Predictor"
APP_ICON = "📊"
LAYOUT = "wide"

# Model configuration
MODEL_PATH = "models/churn_model.pkl"
ENCODERS_PATH = "models/encoders.pkl"
FEATURES_PATH = "models/feature_names.pkl"

# Database configuration
DATABASE_PATH = "customer_data.db"
BACKUP_INTERVAL = 3600  # seconds

# Performance settings
MAX_BATCH_SIZE = 1000
CACHE_TTL = 3600  # seconds
PREDICTION_TIMEOUT = 30  # seconds
```

### File Paths Configuration
```python
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')
DOCS_DIR = os.path.join(BASE_DIR, '..', 'docs')

# Data files
TRAINING_DATA = os.path.join(DATA_DIR, 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
SAMPLE_DATA = os.path.join(DATA_DIR, 'test_customers.csv')
```

---

## 🚀 Deployment Architecture

### Development Environment
```yaml
Environment: Local development
Python: 3.8+
Dependencies: requirements.txt
Launch: streamlit run src/churn_app.py
Access: http://localhost:8501
```

### Production Environment
```yaml
Platform: Streamlit Cloud
Repository: GitHub integration
Branch: main
Build: Automatic on push
URL: https://app-name.streamlit.app
Monitoring: Built-in Streamlit metrics
```

### Scaling Considerations
| Component | Current Limit | Scaling Strategy |
|-----------|---------------|------------------|
| **Concurrent Users** | 100 | Horizontal scaling with load balancer |
| **Batch Size** | 1000 customers | Implement chunking for larger datasets |
| **Model Training** | Manual trigger | Automated retraining pipeline |
| **Data Storage** | SQLite file | Migrate to PostgreSQL for production |

---

## 🔐 Security Specifications

### Data Security
- **Input Validation**: All user inputs sanitized and validated
- **SQL Injection Prevention**: Parameterized queries only
- **File Upload Security**: CSV validation and size limits
- **Data Privacy**: No persistent storage of customer data

### Application Security
```python
# Input validation example
def validate_customer_data(data: dict) -> bool:
    required_fields = ['tenure', 'MonthlyCharges', 'Contract']
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True

# SQL injection prevention
def safe_query(query: str, params: tuple) -> pd.DataFrame:
    conn = sqlite3.connect(DATABASE_PATH)
    return pd.read_sql_query(query, conn, params=params)
```

---

## 📊 Performance Specifications

### Response Time Requirements
| Operation | Target | Acceptable | Critical |
|-----------|--------|------------|----------|
| **Single Prediction** | <2 seconds | <5 seconds | <10 seconds |
| **Batch Processing (100 customers)** | <10 seconds | <30 seconds | <60 seconds |
| **SQL Analytics** | <5 seconds | <15 seconds | <30 seconds |
| **Model Loading** | <10 seconds | <20 seconds | <30 seconds |

### Resource Requirements
| Resource | Minimum | Recommended | Maximum |
|----------|---------|-------------|---------|
| **RAM** | 2GB | 4GB | 8GB |
| **CPU** | 1 core | 2 cores | 4 cores |
| **Storage** | 500MB | 1GB | 2GB |
| **Network** | 1 Mbps | 5 Mbps | 10 Mbps |

---

## 🧪 Testing Architecture

### Unit Testing Framework
```python
# Example test structure
def test_single_prediction():
    """Test single customer prediction functionality"""
    sample_data = {
        'tenure': 12,
        'MonthlyCharges': 50.0,
        'Contract': 'Month-to-month'
    }
    prediction, probability, success, error = predict_single_customer(sample_data)
    assert success == True
    assert 0 <= probability <= 1
    assert prediction in [0, 1]
```

### Integration Testing
- **Database Integration**: SQL query execution and data retrieval
- **Model Integration**: Prediction pipeline end-to-end
- **UI Integration**: Streamlit component functionality

### Performance Testing
- **Load Testing**: 100 concurrent users simulation
- **Stress Testing**: Maximum batch size processing
- **Memory Testing**: Long-running session monitoring

---

## 📝 Error Handling Architecture

### Error Categories
| Category | Examples | Handling Strategy |
|----------|----------|-------------------|
| **User Input Errors** | Invalid CSV format, missing columns | Validation with user-friendly messages |
| **Model Errors** | Prediction failures, encoding errors | Graceful degradation with error logging |
| **System Errors** | File not found, memory issues | Exception handling with fallback options |
| **Network Errors** | Database connection issues | Retry logic with timeout |

### Error Response Format
```python
{
    "success": false,
    "error_type": "VALIDATION_ERROR",
    "message": "Missing required column: tenure",
    "details": "CSV file must contain all required customer attributes",
    "timestamp": "2025-08-20T23:58:00Z"
}
```

---

## 🔄 Maintenance & Updates

### Model Retraining Schedule
- **Frequency**: Monthly or when accuracy drops below 75%
- **Data Requirements**: Minimum 1000 new customer records
- **Validation**: Hold-out test set with business validation
- **Deployment**: A/B testing before full rollout

### System Updates
```python
# Version management
SYSTEM_VERSION = "1.0.0"
MODEL_VERSION = "1.0.0"
LAST_UPDATED = "2025-08-20"

# Update procedures
def check_model_freshness():
    """Check if model needs retraining based on performance metrics"""
    
def backup_current_model():
    """Create backup before updating model"""
    
def validate_new_model():
    """Validate new model performance before deployment"""
```

---

## 📋 Technical Dependencies

### Core Dependencies
```txt
streamlit>=1.28.0          # Web application framework
pandas>=2.0.3              # Data manipulation
scikit-learn>=1.3.0        # Machine learning
matplotlib>=3.7.2          # Visualization
numpy>=1.24.3             # Numerical computing
```

### Development Dependencies
```txt
pytest>=7.4.0             # Testing framework
black>=23.7.0             # Code formatting
flake8>=6.0.0             # Code linting
jupyter>=1.0.0            # Development notebooks
```

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, Linux
- **Browser**: Chrome 91+, Firefox 89+, Safari 14+
- **Internet**: Required for initial deployment setup

---

## 📞 Technical Support

### Documentation Links
- [Implementation Guide](implementation_guide.md) - Complete deployment process
- [QA Test Plan](qa_test_plan.md) - Quality assurance procedures  
- [User Manual](user_manual.md) - End-user instructions
- [README](../README.md) - Project overview and quick start

### Support Contacts
- **Technical Issues**: IT Help Desk
- **Model Performance**: Data Science Team
- **Business Questions**: Implementation Analyst
- **User Training**: Training Coordinator

---

**Document Version**: 1.0  
**Last Updated**: August 20, 2025  
**Next Review**: December 2025  
**Document Owner**: Implementation Analyst