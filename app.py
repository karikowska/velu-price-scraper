"""Streamlit app UI flow."""
import streamlit as st
import yaml
from agent import prepare_agent_for_product  # make sure this is exposed
from agent import tools, llm  # your tool list and LLM
from langchain.agents import initialize_agent, AgentType
from helpers.other_helpers import load_config

st.set_page_config(page_title="Velu - Price Scraper Agent", page_icon="💰")
st.title("💰 Velu - Price Scraper Agent")
st.markdown("Velu is an agent that can help you keep track of your figure-collecting wishlist and find you the lowest prices available at supported websites. Find out more at https://github.com/karikowska/velu-price-scraper.")

full_config = load_config()
wishlist = full_config["products"]

# Show wishlist
st.subheader("📝 Your Wishlist")
st.markdown("Here are the products you're tracking:")
for item in wishlist:
    st.markdown(f"- **{item['name']}** — Max ¥{item['max_price']}")
st.markdown("You can change the wishlist and settings in the sidebar on the left before submitting it to the agent.")

st.sidebar.title("⚙️ Settings")

edit_mode = st.sidebar.checkbox("Edit Wishlist & Config")

if edit_mode:
    st.subheader("✍️ Edit Wishlist")

    updated_products = []
    for i, product in enumerate(full_config["products"]):
        with st.expander(f"Product {i+1}: {product['name']}"):
            name = st.text_input(f"Name", value=product["name"], key=f"name_{i}")
            max_price = st.number_input(f"Max Price ¥", value=product["max_price"], key=f"price_{i}")
            sites = st.multiselect(
                f"Sites {i+1}",
                options=full_config["config"]["allowed_sites"],
                default=product.get("sites", []),
                key=f"sites_{i}"
            )
            updated_products.append({
                "name": name,
                "max_price": max_price,
                "sites": sites
            })

    # st.subheader("🧮 Config")
    # interval = st.number_input("Price Check Interval (minutes)", value=full_config["config"]["check_interval_minutes"])

    if st.button("💾 Save Changes"):
        new_config = {
            "products": updated_products,
            "config": {
                # "check_interval_minutes": interval,
                "allowed_sites": full_config["config"]["allowed_sites"]  # or let user edit this too
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
        st.markdown(f"**{name}**")
        st.markdown(result)

st.caption("This app uses LangChain to compare prices from configured stores and show the lowest one below your budget.")
