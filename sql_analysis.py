# SQL Analysis Module for Customer Churn Project
"""
This module provides SQL-based analysis of customer data for business insights.
Demonstrates SQL skills required for Implementation Analyst role.
"""

import sqlite3
import pandas as pd
import streamlit as st

def create_customer_database():
    """Create SQLite database from CSV data"""
    try:
        # Load the CSV data
        df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
        
        # Create SQLite connection
        conn = sqlite3.connect('customer_data.db')
        
        # Create table from DataFrame
        df.to_sql('customers', conn, index=False, if_exists='replace')
        
        conn.close()
        return True, "Database created successfully!"
        
    except Exception as e:
        return False, f"Error creating database: {str(e)}"

def run_churn_analysis_queries():
    """Execute business analysis queries"""
    try:
        conn = sqlite3.connect('customer_data.db')
        
        # Query 1: Churn rate by contract type
        query_1 = """
        SELECT 
            Contract,
            COUNT(*) as total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
            ROUND(
                (SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
            ) as churn_rate_percent,
            ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges,
            ROUND(AVG(tenure), 1) as avg_tenure_months
        FROM customers 
        GROUP BY Contract
        ORDER BY churn_rate_percent DESC;
        """
        
        # Query 2: Revenue impact analysis
        query_2 = """
        SELECT 
            InternetService,
            COUNT(*) as total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN TotalCharges ELSE 0 END) as lost_revenue,
            COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) as churned_customers,
            ROUND(AVG(CASE WHEN Churn = 'Yes' THEN MonthlyCharges END), 2) as avg_monthly_charge_churned
        FROM customers
        WHERE TotalCharges != ' ' AND TotalCharges IS NOT NULL
        GROUP BY InternetService
        ORDER BY lost_revenue DESC;
        """
        
        # Query 3: High-risk customer segments
        query_3 = """
        SELECT 
            tenure_group,
            payment_method,
            COUNT(*) as customer_count,
            churn_rate,
            avg_charges
        FROM (
            SELECT 
                CASE 
                    WHEN tenure <= 12 THEN 'New (0-12 months)'
                    WHEN tenure <= 36 THEN 'Medium (13-36 months)'
                    ELSE 'Long-term (36+ months)'
                END as tenure_group,
                PaymentMethod as payment_method,
                COUNT(*) as customer_count,
                ROUND(
                    (SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
                ) as churn_rate,
                ROUND(AVG(MonthlyCharges), 2) as avg_charges
            FROM customers
            GROUP BY tenure_group, PaymentMethod
        )
        ORDER BY churn_rate DESC
        LIMIT 10;
        """
        
        # Query 4: Service add-on analysis
        query_4 = """
        SELECT 
            'Online Security' as service,
            OnlineSecurity as has_service,
            COUNT(*) as customers,
            ROUND(
                (SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
            ) as churn_rate
        FROM customers 
        GROUP BY OnlineSecurity
        
        UNION ALL
        
        SELECT 
            'Tech Support' as service,
            TechSupport as has_service,
            COUNT(*) as customers,
            ROUND(
                (SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
            ) as churn_rate
        FROM customers 
        GROUP BY TechSupport
        
        ORDER BY service, churn_rate DESC;
        """
        
        # Execute queries
        contract_analysis = pd.read_sql_query(query_1, conn)
        revenue_impact = pd.read_sql_query(query_2, conn)
        risk_segments = pd.read_sql_query(query_3, conn)
        service_analysis = pd.read_sql_query(query_4, conn)
        
        conn.close()
        
        return {
            'contract_analysis': contract_analysis,
            'revenue_impact': revenue_impact,
            'risk_segments': risk_segments,
            'service_analysis': service_analysis
        }
        
    except Exception as e:
        return f"Error running queries: {str(e)}"

def get_customer_details_query(customer_id):
    """Get detailed information for a specific customer"""
    try:
        conn = sqlite3.connect('customer_data.db')
        
        query = """
        SELECT 
            customerID,
            gender,
            SeniorCitizen,
            Partner,
            Dependents,
            tenure,
            PhoneService,
            InternetService,
            Contract,
            PaperlessBilling,
            PaymentMethod,
            MonthlyCharges,
            TotalCharges,
            Churn,
            CASE 
                WHEN tenure <= 12 THEN 'High Risk - New Customer'
                WHEN Contract = 'Month-to-month' THEN 'Medium Risk - Short Contract'
                ELSE 'Low Risk - Established Customer'
            END as risk_category
        FROM customers 
        WHERE customerID = ?
        """
        
        result = pd.read_sql_query(query, conn, params=[customer_id])
        conn.close()
        
        return result
        
    except Exception as e:
        return f"Error getting customer details: {str(e)}"

def create_sql_reporting_queries():
    """Generate SQL queries for common business reports"""
    
    queries = {
        "Monthly Churn Report": """
        -- Monthly churn analysis for executive dashboard
        SELECT 
            strftime('%Y-%m', 'now') as report_month,
            COUNT(*) as total_customers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
            ROUND(
                (SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
            ) as churn_rate_percent,
            SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) as monthly_revenue_at_risk,
            SUM(CASE WHEN Churn = 'Yes' THEN TotalCharges ELSE 0 END) as total_lost_revenue
        FROM customers;
        """,
        
        "High-Risk Customers": """
        -- Identify customers most likely to churn
        SELECT 
            customerID,
            tenure,
            Contract,
            MonthlyCharges,
            PaymentMethod,
            CASE 
                WHEN tenure <= 6 AND Contract = 'Month-to-month' THEN 'Very High'
                WHEN tenure <= 12 AND PaymentMethod = 'Electronic check' THEN 'High'
                WHEN Contract = 'Month-to-month' AND MonthlyCharges > 70 THEN 'Medium'
                ELSE 'Low'
            END as risk_level
        FROM customers 
        WHERE Churn = 'No'
        ORDER BY 
            CASE 
                WHEN tenure <= 6 AND Contract = 'Month-to-month' THEN 1
                WHEN tenure <= 12 AND PaymentMethod = 'Electronic check' THEN 2
                WHEN Contract = 'Month-to-month' AND MonthlyCharges > 70 THEN 3
                ELSE 4
            END;
        """,
        
        "Revenue Analysis": """
        -- Revenue impact by customer segment
        SELECT 
            Contract,
            InternetService,
            COUNT(*) as customers,
            SUM(MonthlyCharges) as total_monthly_revenue,
            AVG(MonthlyCharges) as avg_monthly_revenue,
            SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) as at_risk_revenue
        FROM customers
        GROUP BY Contract, InternetService
        ORDER BY at_risk_revenue DESC;
        """
    }
    
    return queries

# Streamlit integration functions
def display_sql_analysis():
    """Display SQL analysis in Streamlit app"""
    st.header("📊 SQL-Based Business Analysis")
    
    # Create database button
    if st.button("🔄 Refresh Database", help="Create/update the customer database"):
        success, message = create_customer_database()
        if success:
            st.success(message)
        else:
            st.error(message)
    
    # Run analysis
    if st.button("🚀 Run Business Analysis"):
        with st.spinner("Running SQL queries..."):
            results = run_churn_analysis_queries()
            
            if isinstance(results, dict):
                # Display Contract Analysis
                st.subheader("📋 Churn Rate by Contract Type")
                st.dataframe(results['contract_analysis'])
                
                # Display Revenue Impact
                st.subheader("💰 Revenue Impact Analysis")
                st.dataframe(results['revenue_impact'])
                
                # Display High-Risk Segments
                st.subheader("⚠️ High-Risk Customer Segments")
                st.dataframe(results['risk_segments'])
                
                # Display Service Analysis
                st.subheader("🛠️ Service Add-on Impact")
                st.dataframe(results['service_analysis'])
                
            else:
                st.error(results)
    
    # Show SQL queries
    with st.expander("🔍 View SQL Queries Used"):
        queries = create_sql_reporting_queries()
        for title, query in queries.items():
            st.subheader(title)
            st.code(query, language='sql')

if __name__ == "__main__":
    # Test the functions
    print("Creating database...")
    success, msg = create_customer_database()
    print(msg)
    
    if success:
        print("Running analysis...")
        results = run_churn_analysis_queries()
        if isinstance(results, dict):
            print("Contract Analysis:")
            print(results['contract_analysis'])
        else:
            print(results)