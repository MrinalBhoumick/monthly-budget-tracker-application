import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
import os

# ------------------ Setup ------------------
USER_DB = "users.csv"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(page_title="Budget Tracker", layout="wide", page_icon="💰")

# ------------------ User Handling ------------------
def load_users():
    if os.path.exists(USER_DB):
        return pd.read_csv(USER_DB)
    else:
        return pd.DataFrame(columns=['username', 'password'])

def save_user(username, password):
    users = load_users()
    new_user_df = pd.DataFrame([[username, password]], columns=['username', 'password'])
    users = pd.concat([users, new_user_df], ignore_index=True)
    users.to_csv(USER_DB, index=False)

def validate_user(username, password):
    users = load_users()
    return any((users['username'] == username) & (users['password'] == password))

# ------------------ App Title ------------------
st.markdown("<h1 style='text-align: center;'>💼 Multi-User Budget Tracker</h1>", unsafe_allow_html=True)

# ------------------ Session ------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ------------------ Login / Signup ------------------
if not st.session_state.logged_in:
    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab_login:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if validate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab_signup:
        st.subheader("Create an Account")
        new_user = st.text_input("Choose a Username")
        new_pass = st.text_input("Choose a Password", type="password")
        if st.button("Sign Up"):
            if new_user and new_pass:
                save_user(new_user, new_pass)
                st.success("Account created! Please login.")
            else:
                st.error("Fields cannot be empty.")

# ------------------ Main App ------------------
else:
    user_file = os.path.join(DATA_DIR, f"{st.session_state.username}.csv")

    if 'data' not in st.session_state:
        if os.path.exists(user_file):
            df = pd.read_csv(user_file)
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            st.session_state.data = df
        else:
            st.session_state.data = pd.DataFrame(columns=['Date', 'Category', 'Type', 'Amount', 'Note'])

    # ------------- Sidebar ------------------
    st.sidebar.title("⚙️ Monthly Setup")
    monthly_income = st.sidebar.number_input("In-Hand Income (₹)", min_value=0, value=17900, step=100)
    rent = st.sidebar.number_input("Flat Rent (₹)", min_value=0, value=4500, step=100)
    loan = st.sidebar.number_input("Education Loan EMI (₹)", min_value=0, value=2877, step=100)
    sip = st.sidebar.number_input("SIP Investment (₹)", min_value=0, value=1500, step=100)
    gold_sip = st.sidebar.number_input("Gold SIP (₹)", min_value=0, value=2400, step=100)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.data = None
        st.rerun()

    # ------------- Tabs ------------------
    tab1, tab2, tab3 = st.tabs(["➕ Add Entry", "📊 Dashboard", "📁 Export"])

    # Tab 1: Add Entry
    tab1.subheader("➕ Add a New Transaction")
    with tab1.form("entry_form"):
        date = st.date_input("Date", datetime.today())
        txn_type = st.selectbox("Type", ["Expense", "Income"])
        category = st.text_input("Category (e.g. Food, Salary)")
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        note = st.text_input("Note (Optional)")
        submit = st.form_submit_button("Add Entry")

        if submit:
            new_entry = pd.DataFrame([[date, category, txn_type, amount, note]],
                                     columns=['Date', 'Category', 'Type', 'Amount', 'Note'])
            data = st.session_state.data

            data = pd.concat([data, new_entry], ignore_index=True)
            data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
            data.to_csv(user_file, index=False)
            st.session_state.data = data
            st.success("✅ Entry added!")

    # Tab 2: Dashboard
    with tab2:
        st.subheader(f"📊 Dashboard Summary - {st.session_state.username}")
        data = st.session_state.data

        # Summary
        monthly_expenses = data[data['Type'] == 'Expense']['Amount'].sum()
        actual_income = data[data['Type'] == 'Income']['Amount'].sum() + monthly_income
        fixed_expenses = rent + loan + sip + gold_sip
        total_expenses = monthly_expenses + fixed_expenses
        savings = actual_income - total_expenses

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Income", f"₹{actual_income:.2f}")
        col2.metric("💸 Total Expenses", f"₹{total_expenses:.2f}")
        col3.metric("📈 Savings", f"₹{savings:.2f}")

        st.divider()

        # Pie Chart
        st.subheader("📌 Expense Breakdown")
        expense_data = data[data['Type'] == 'Expense']
        if not expense_data.empty:
            fig_pie = px.pie(expense_data, names='Category', values='Amount', title='Expenses by Category')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expenses added yet.")

        # Monthly Trends
        st.subheader("📅 Monthly Trends")
        if not data.empty:
            trend_data = data.copy()
            trend_data['Month'] = pd.to_datetime(trend_data['Date'], errors='coerce').dt.to_period('M').astype(str)
            trend_summary = trend_data.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
            fig_bar = px.bar(trend_summary, x='Month', y='Amount', color='Type', barmode='group',
                             title="Monthly Income & Expenses")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No transactions yet.")

        # Data Table
        st.subheader("📋 All Transactions")
        sorted_data = data.sort_values(by="Date", ascending=False, na_position="last")
        st.dataframe(sorted_data, use_container_width=True)

    # Tab 3: Export
    with tab3:
        st.subheader("📁 Export Budget to Excel")
        if st.button("Export to Excel"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                data.to_excel(writer, index=False, sheet_name='BudgetData')
                pd.DataFrame({
                    'Metric': ['Income', 'Expenses', 'Savings'],
                    'Amount (₹)': [actual_income, total_expenses, savings]
                }).to_excel(writer, index=False, sheet_name='Summary')
            output.seek(0)
            st.download_button("📥 Download Excel",
                               output,
                               file_name=f"{st.session_state.username}_Budget.xlsx",
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
