import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("Employee-Attrition.csv")

# Page Config
st.set_page_config(page_title="HR Attrition Dashboard", layout="wide")

# Title
st.title("💼 HR Analytics Dashboard")
st.markdown("### Employee Attrition Insights")

# KPIs
attrition_rate = df['Attrition'].value_counts(normalize=True)['Yes'] * 100
avg_age = df[df['Attrition']=='Yes']['Age'].mean()
avg_salary = df[df['Attrition']=='Yes']['MonthlyIncome'].mean()
top_dept = df[df['Attrition']=='Yes']['Department'].mode()[0]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Attrition Rate", f"{attrition_rate:.1f}%")
kpi2.metric("Avg Age (Resigned)", f"{avg_age:.1f} yrs")
kpi3.metric("Avg Salary (Resigned)", f"${avg_salary:,.0f}")
kpi4.metric("Top Dept (Attrition)", top_dept)

st.markdown("---")

# Row 1: Department-wise Attrition & Pie Chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Department-wise Attrition")
    dept_attr = df.groupby("Department")['Attrition'].value_counts(normalize=True).unstack().fillna(0)
    dept_attr['Yes'] = dept_attr['Yes'] * 100
    st.bar_chart(dept_attr['Yes'])

with col2:
    st.subheader("📌 Overall Attrition")
    fig, ax = plt.subplots()
    df['Attrition'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#66b3ff','#ff9999'], ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

# Row 2: Age Distribution & Salary vs Attrition
col3, col4 = st.columns(2)

with col3:
    st.subheader("📌 Age Distribution by Attrition")
    fig, ax = plt.subplots()
    sns.kdeplot(df[df['Attrition']=='Yes']['Age'], shade=True, label="Resigned", ax=ax, color="red")
    sns.kdeplot(df[df['Attrition']=='No']['Age'], shade=True, label="Stayed", ax=ax, color="green")
    ax.legend()
    st.pyplot(fig)

with col4:
    st.subheader("📌 Salary vs Attrition")
    fig, ax = plt.subplots()
    sns.boxplot(x="Attrition", y="MonthlyIncome", data=df, palette="Set2", ax=ax)
    st.pyplot(fig)

st.markdown("✅ Dashboard built for HR to quickly identify attrition trends (Age, Salary, Department).")
