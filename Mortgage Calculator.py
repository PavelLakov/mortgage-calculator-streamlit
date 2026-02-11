import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Custom CSS for fancy design
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background-color: #0066ff;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #0052cc;
    }
    .stNumberInput > div > div > input {
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 8px;
    }
    .stSelectbox > div > div > div {
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .stTextInput > div > div > input {
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 8px;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)


def calculate_monthly_payment(principal, annual_rate, loan_term_years):
    monthly_rate = annual_rate / 12 / 100
    num_payments = loan_term_years * 12
    if monthly_rate == 0:
        return principal / num_payments
    payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    return payment


def generate_amortization_schedule(principal, annual_rate, loan_term_years, extra_payment=0):
    monthly_rate = annual_rate / 12 / 100
    num_payments = loan_term_years * 12
    monthly_payment = calculate_monthly_payment(principal, annual_rate, loan_term_years)
    schedule = []
    balance = principal
    total_interest = 0
    cumulative_principal = 0
    cumulative_interest = 0
    chart_data = {'Month': [], 'Principal Paid': [], 'Interest Paid': []}
    for month in range(1, num_payments + 1):
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest + extra_payment
        balance -= principal_payment
        total_interest += interest
        cumulative_principal += principal_payment
        cumulative_interest += interest
        if balance < 0:
            balance = 0
        schedule.append({
            'Month': month,
            'Payment': monthly_payment + extra_payment,
            'Principal': principal_payment,
            'Interest': interest,
            'Balance': balance
        })
        chart_data['Month'].append(month)
        chart_data['Principal Paid'].append(cumulative_principal)
        chart_data['Interest Paid'].append(cumulative_interest)
        if balance <= 0:
            break
    return pd.DataFrame(schedule), total_interest, pd.DataFrame(chart_data)


st.title("Mortgage Calculator")

col1, col2 = st.columns([1, 2])

with col1:
    home_price = st.number_input("Home price", min_value=0.0, value=425000.0, step=1000.0)

    st.write("Down payment")

    dp_col1, dp_col2 = st.columns(2)

    if 'down_payment' not in st.session_state:
        st.session_state.down_payment = 21250.0
    if 'down_payment_percent' not in st.session_state:
        st.session_state.down_payment_percent = 5.0


    def update_dp_percent():
        if home_price > 0:
            st.session_state.down_payment_percent = (st.session_state.down_payment / home_price) * 100


    def update_dp_amount():
        st.session_state.down_payment = home_price * (st.session_state.down_payment_percent / 100)


    with dp_col1:
        down_payment = st.number_input("$", min_value=0.0, value=st.session_state.down_payment, key='dp_amount',
                                       on_change=update_dp_percent, step=250.0)

    with dp_col2:
        down_payment_percent = st.number_input("%", min_value=0.0, max_value=100.0,
                                               value=st.session_state.down_payment_percent, key='dp_percent',
                                               on_change=update_dp_amount, step=1.0)

    loan_term = st.selectbox("Loan term", ["30 years", "20 years", "15 years", "10 years","5 years"], index=0)
    loan_term_years = int(loan_term.split()[0])

    interest_rate = st.number_input("Interest rate", min_value=0.0, value=5.0, step=0.125)

    zip_code = st.text_input("ZIP code")

    expander = st.expander("Taxes, insurance, HOA fees")
    with expander:
        property_tax_rate = st.number_input("Annual Property Tax Rate (%)", min_value=0.0, value=0.8, step=0.1)
        homeowners_insurance = st.number_input("Annual Homeowners Insurance", min_value=0.0, value=792.0, step=100.0)
        hoa_fees = st.number_input("Monthly HOA Fees", min_value=0.0, value=0.0, step=10.0)

    st.button("Update")

with col2:
    tab1, tab2 = st.tabs(["Payment breakdown", "Amortization"])

    with tab1:
        principal = home_price - down_payment
        monthly_principal_interest = calculate_monthly_payment(principal, interest_rate, loan_term_years)

        monthly_property_tax = (home_price * (property_tax_rate / 100)) / 12
        monthly_insurance = homeowners_insurance / 12
        total_monthly_payment = monthly_principal_interest + monthly_property_tax + monthly_insurance + hoa_fees

        st.subheader("Monthly payment breakdown")
        st.write("Based on your inputted interest rate")

        pie_col, break_col = st.columns(2)

        with pie_col:
            labels = ['Principal & Interest', 'Property Tax', "Homeowner's Insurance"]
            values = [monthly_principal_interest, monthly_property_tax, monthly_insurance]
            colors = ['#00AEEF', '#B2FF59', '#AB47BC']  # Adjusted colors to match image: blue, light green, purple

            if hoa_fees > 0:
                labels.append('HOA Fees')
                values.append(hoa_fees)
                colors.append('#FFD700')

            fig = px.pie(names=labels, values=values, hole=0.8, color_discrete_sequence=colors)
            fig.update_traces(textinfo='none')
            fig.update_layout(
                annotations=[
                    dict(text=f"${total_monthly_payment:,.0f}/mo", x=0.5, y=0.5, font_size=28, showarrow=False)],
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=300,
                width=300
            )
            st.plotly_chart(fig, use_container_width=True)

        with break_col:
            st.markdown('<div style="color: #00AEEF; font-weight: bold;">Principal & Interest</div>',
                        unsafe_allow_html=True)
            st.write(f"${monthly_principal_interest:,.2f}")
            st.markdown('<div style="color: #B2FF59; font-weight: bold;">Property Tax</div>', unsafe_allow_html=True)
            st.write(f"+ ${monthly_property_tax:,.0f}")
            st.markdown('<div style="color: #AB47BC; font-weight: bold;">Homeowner\'s Insurance</div>',
                        unsafe_allow_html=True)
            st.write(f"+ ${monthly_insurance:,.0f}")
            if hoa_fees > 0:
                st.markdown('<div style="color: #FFD700; font-weight: bold;">HOA Fees</div>', unsafe_allow_html=True)
                st.write(f"+ ${hoa_fees:,.0f}")

    with tab2:
        extra_payment = st.number_input("Extra Monthly Payment", min_value=0.0, value=0.0, step=10.0)
        if st.button("Generate Schedule & Chart", key="generate_btn"):
            schedule_df, total_interest, chart_df = generate_amortization_schedule(principal, interest_rate,
                                                                                   loan_term_years, extra_payment)

            st.dataframe(schedule_df.style.format({
                'Payment': '${:,.2f}',
                'Principal': '${:,.2f}',
                'Interest': '${:,.2f}',
                'Balance': '${:,.2f}'
            }).background_gradient(subset=['Balance'], cmap='Blues'))

            st.info(f"Total Interest Paid: ${total_interest:,.2f}")
            st.info(f"Loan Paid Off in {len(schedule_df)} months")

            # Chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(chart_df['Month'], chart_df['Principal Paid'], label='Principal Paid', color='green')
            ax.plot(chart_df['Month'], chart_df['Interest Paid'], label='Interest Paid', color='red')
            ax.set_xlabel('Month')
            ax.set_ylabel('Amount ($)')
            ax.set_title('Cumulative Principal and Interest Over Time')
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)