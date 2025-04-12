"""Streamlit app UI flow."""
import streamlit as st
import yaml
from agent import prepare_agent_for_product  # make sure this is exposed
from agent import tools, llm  # your tool list and LLM
from langchain.agents import initialize_agent, AgentType
from helpers.other_helpers import load_config

st.set_page_config(page_title="Velu - Price Scraper Agent", page_icon="💰")

st.markdown("""
    <style>
    body {
        background-color: #1a1a2e;
    }
    .stApp {
        background-color: #1a1a2e;
        color: #e0e0ff;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #7a3fd0;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #9d59f2;
        transition: 0.2s ease-in-out;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #9d59f2, #7a3fd0);
    }
    .st-expanderHeader {
        font-weight: bold;
        color: #e0e0ff;
    }
    .stMarkdown, .stText, .stSubheader, .stCaption {
        color: #e0e0ff;
    }
    </style>
""", unsafe_allow_html=True)

logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
with logo_col2:
    st.image("velu_logo.png", width=200)
st.title("💰 Velu - Price Scraper Agent")
st.markdown("Velu is an agent that can help you keep track of your figure-collecting wishlist and find you the lowest prices available at supported websites!")
st.markdown("Find out more at https://github.com/karikowska/velu-price-scraper.")

full_config = load_config()
wishlist = full_config["products"]

# Show wishlist
st.divider()
st.subheader("📝 Your Wishlist")
st.markdown("Here are the products you're tracking:")
for item in wishlist:
    st.markdown(f"- **{item['name']}** — Max ¥{item['max_price']}")
st.markdown("You can change the wishlist and settings in the sidebar on the left before submitting it to the agent.")

st.sidebar.title("⚙️ Settings")

edit_mode = st.sidebar.checkbox("Edit Wishlist")

if edit_mode:
    if "editable_products" not in st.session_state:
        st.session_state.editable_products = full_config["products"]

    st.subheader("✍️ Edit Wishlist")
    st.markdown("Click on the product name to open up a menu and edit it. You can click on the bin icon on the right to delete an item. Keep in mind that after deleting, the item will be erased from the YAML file but you must save and refresh the page for the UI to update.")

    updated_products = []
    for i, product in enumerate(full_config["products"]):
        cols = st.columns([10, 1])
        with cols[0].expander(f"Product {i+1}: {product['name']}"):
            name = st.text_input(f"Name", value=product["name"], key=f"name_{i}")
            max_price = st.number_input(f"Max Price ¥", value=product["max_price"], key=f"price_{i}")
            desired_currency = st.selectbox(f"Currency", options=["JPY", "USD", "EUR", "GBP"], key=f"currency_{i}")
            st.markdown("**Note**: The agent will only check prices in JPY, but you can set your preferred currency for the wishlist.")
            sites = st.multiselect(
                f"Sites",
                options=full_config["config"]["allowed_sites"],
                default=product.get("sites", []),
                key=f"sites_{i}"
            )
            updated_products.append({
                "name": name,
                "max_price": max_price,
                "sites": sites
            })
        if cols[1].button("🗑️", key=f"delete_{i}"):
            st.session_state.editable_products.pop(i)
            st.rerun()


    st.markdown("### ➕ Add New Item")
    with st.form("add_product_form"):
        new_name = st.text_input("New Product Name")
        new_price = st.number_input("New Max Price ¥", min_value=0, value=5000)
        new_sites = st.multiselect("Sites to Search", options=full_config["config"]["allowed_sites"], default=full_config["config"]["allowed_sites"])
        submitted = st.form_submit_button("Add to Wishlist")
        if submitted and new_name:
            updated_products.append({"name": new_name, "max_price": new_price, "sites": new_sites})
            st.success(f"Added: {new_name}")

    st.markdown("*Important*: To save your results, you must click the button below. This will overwrite your current wishlist and settings in the config file, with what you wrote above.")
    if st.button("💾 Save Changes"):
        new_config = {
            "products": st.session_state.editable_products,
            "config": {
                "allowed_sites": full_config["config"]["allowed_sites"]
            }
        }
        with open("config/wishlist.yaml", "w", encoding="utf-8") as f:
            yaml.dump(new_config, f, allow_unicode=True)
        st.success("✅ Wishlist updated!")

# Run agent + display results
if st.button("Run Velu!"):
    with st.spinner("Velu is hard at work, finding relevant results and scraping prices..."):
        results = []
        total = len(wishlist)
        progress_bar = st.progress(0)

        for i, product in enumerate(wishlist):
            selected_tools, prompt = prepare_agent_for_product(product, tools, full_config["config"])
            agent = initialize_agent(
                tools=selected_tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True,
                verbose=True,
            )
            result = agent.run(prompt)
            results.append((product["name"], result))

            # update progress
            progress = (i + 1) / total
            progress_bar.progress(progress)

    st.success("✅ All done!")
    st.subheader("📊 Velu's best finds:")

    for name, result in results:
        with st.expander(f"{name}"):
            st.markdown(result)

st.caption("This app uses LangChain to compare prices from configured stores and show the lowest one below your budget.")
