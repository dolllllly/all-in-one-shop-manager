import streamlit as st
from supabase import create_client
from datetime import datetime, timezone
import csv
import io

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Dewangan Family Shop Manager",
    page_icon="🛒",
    layout="wide"
)

SHOPS = ["Grocery", "Hardware", "Stationery", "Electronics"]
PEOPLE = ["Ritesh", "Jamuna", "Vijay"]
PRIORITIES = ["High", "Medium", "Low"]

SHOP_ICONS = {
    "Grocery": "🥦",
    "Hardware": "🔧",
    "Stationery": "📚",
    "Electronics": "💻"
}

SHOP_COLORS = {
    "Grocery": "#16a34a",
    "Hardware": "#ea580c",
    "Stationery": "#2563eb",
    "Electronics": "#9333ea"
}

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "selected_shop_card" not in st.session_state:
    st.session_state["selected_shop_card"] = None

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #fff7ed 0%, #fdf2f8 45%, #eff6ff 100%
    );
    color: #1f2937 !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3, h4 {
    font-weight: 800 !important;
    color: #4338ca !important;
}

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] strong,
[data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"],
[data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {
    color: #374151;
}

.hero-banner {
    background: linear-gradient(
        135deg, #6d28d9, #db2777, #f97316
    );
    padding: 30px;
    border-radius: 22px;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(109, 40, 217, 0.20);
}

.hero-banner h1 {
    color: #ffffff !important;
    margin: 5px 0;
    font-size: 30px;
}

.hero-banner p {
    color: #fff7ed !important;
    font-size: 16px;
    margin: 8px 0 0;
}

.hero-icon {
    font-size: 42px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #312e81, #6d28d9, #9333ea
    );
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff, #f5f3ff);
    border: 1px solid #ddd6fe;
    padding: 22px 18px;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(109, 40, 217, 0.10);
}

[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #6d28d9 !important;
    font-weight: 800;
}

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #7c3aed, #db2777);
    color: #ffffff !important;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #be185d);
    box-shadow: 0 5px 15px rgba(124, 58, 237, 0.22);
    transform: translateY(-2px);
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    color: #1f2937 !important;
    background-color: #ffffff !important;
    border: 1px solid #c4b5fd !important;
    border-radius: 10px !important;
    -webkit-text-fill-color: #1f2937 !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9ca3af !important;
    -webkit-text-fill-color: #9ca3af !important;
}

[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-color: #c4b5fd !important;
    border-radius: 10px !important;
}

[data-baseweb="select"] *,
[data-baseweb="popover"] * {
    color: #1f2937;
}

[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.92);
    padding: 22px;
    border: 1px solid #e9d5ff;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(124, 58, 237, 0.07);
}

[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #ddd6fe;
    border-radius: 15px;
    margin-bottom: 10px;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #374151 !important;
}

.shop-card {
    background: #ffffff;
    padding: 22px 12px 15px;
    border-radius: 18px;
    border: 1px solid #e9d5ff;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.04);
    min-height: 150px;
}

.shop-card h4 {
    margin: 8px 0;
}

.shop-card p {
    color: #6b7280 !important;
    margin: 0;
    font-size: 14px;
}

.login-card {
    background: #ffffff;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #e9d5ff;
    text-align: center;
    margin-bottom: 20px;
}

.login-card h3 {
    color: #6d28d9 !important;
}

.login-card p {
    color: #6b7280 !important;
}

.history-card {
    background: #ffffff;
    padding: 16px;
    border: 1px solid #e9d5ff;
    border-left: 5px solid #7c3aed;
    border-radius: 14px;
    margin-bottom: 12px;
}

.footer {
    text-align: center;
    color: #7c3aed;
    padding: 20px 0;
    font-size: 14px;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    [data-testid="stMetric"] {
        padding: 14px;
    }

    .hero-banner {
        padding: 20px;
    }

    .hero-banner h1 {
        font-size: 24px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DESIGN HELPERS
# =========================================================

def show_banner(title, subtitle, icon="🛒"):
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-icon">{icon}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def show_footer():
    st.markdown("""
    <div class="footer">
        💜 Made for the Dewangan Family
        <br>
        One Family • Four Shops • One Smart Shopping List
    </div>
    """, unsafe_allow_html=True)


def format_date(value):
    if not value:
        return "—"

    try:
        parsed = datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        )

        if parsed.tzinfo is not None:
            parsed = parsed.astimezone()

        return parsed.strftime("%d %b %Y, %I:%M %p")

    except (ValueError, TypeError, AttributeError):
        return str(value)


def display_quantity(value):
    """Display a dash when quantity is empty or NULL."""
    return value.strip() if value and value.strip() else "—"


# =========================================================
# DATABASE CONNECTION
# =========================================================

@st.cache_resource
def connect_database():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )


try:
    supabase = connect_database()
except Exception:
    st.error(
        "Could not connect to the database. "
        "Please check your Supabase settings."
    )
    st.stop()


def get_items():
    """Fetch all saved items, newest first."""
    all_items = []
    page_size = 1000
    start = 0

    while True:
        result = (
            supabase.table("shop_items")
            .select("*")
            .order("created_at", desc=True)
            .range(start, start + page_size - 1)
            .execute()
        )

        batch = result.data or []
        all_items.extend(batch)

        if len(batch) < page_size:
            break

        start += page_size

    return all_items


def add_item(data):
    supabase.table("shop_items").insert(data).execute()


def update_item(item_id, data):
    (
        supabase.table("shop_items")
        .update(data)
        .eq("id", item_id)
        .execute()
    )


def delete_item(item_id):
    (
        supabase.table("shop_items")
        .delete()
        .eq("id", item_id)
        .execute()
    )


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state["logged_in"]:

    show_banner(
        "Dewangan Family Shop Manager",
        "Your family's smart and simple shopping companion",
        "🛍️"
    )

    left, center, right = st.columns([1, 1.4, 1])

    with center:

        st.markdown("""
        <div class="login-card">
            <div style="font-size: 45px;">🔐</div>
            <h3>Welcome Back!</h3>
            <p>Enter your family password to continue.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):

            password = st.text_input(
                "Family Password",
                type="password",
                placeholder="Enter your password"
            )

            submitted = st.form_submit_button(
                "🔓 Login",
                use_container_width=True
            )

            if submitted:

                if password == st.secrets["APP_PASSWORD"]:
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")

    show_footer()
    st.stop()


# =========================================================
# MAIN HEADER
# =========================================================

show_banner(
    "Dewangan Family Shop Manager",
    "One family • Four shops • One smart shopping list",
    "🛍️"
)

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown("### 👋 Welcome to your family shopping dashboard!")

with header_right:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()


# =========================================================
# LOAD DATA
# =========================================================

try:
    items = get_items()
except Exception:
    st.error("Unable to load products. Please try again.")
    st.stop()

pending = [
    item for item in items
    if item["status"] == "Pending"
]

purchased = [
    item for item in items
    if item["status"] == "Purchased"
]


# =========================================================
# DASHBOARD
# =========================================================

st.subheader("📊 Your Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("🛍️ Total Products", len(items))
c2.metric("⏳ Pending", len(pending))
c3.metric("✅ Purchased", len(purchased))

st.divider()


# =========================================================
# CLICKABLE SHOP CARDS
# =========================================================

st.subheader("🏪 Explore Your Shops")
st.caption("Click a shop to view its pending shopping list.")

cols = st.columns(4)

for col, shop in zip(cols, SHOPS):

    count = sum(
        1 for item in pending
        if item["shop"] == shop
    )

    with col:

        st.markdown(f"""
        <div class="shop-card"
             style="border-top: 5px solid {SHOP_COLORS[shop]};">
            <div style="font-size: 35px;">{SHOP_ICONS[shop]}</div>
            <h4 style="color: {SHOP_COLORS[shop]} !important;">
                {shop}
            </h4>
            <p>{count} pending item(s)</p>
        </div>
        """, unsafe_allow_html=True)

        label = (
            "✓ Viewing This Shop"
            if st.session_state["selected_shop_card"] == shop
            else f"View {shop} List →"
        )

        if st.button(
            label,
            key=f"shop_{shop}",
            use_container_width=True
        ):

            if st.session_state["selected_shop_card"] == shop:
                st.session_state["selected_shop_card"] = None
            else:
                st.session_state["selected_shop_card"] = shop

            st.rerun()


# =========================================================
# SELECTED SHOP LIST
# =========================================================

selected_card_shop = st.session_state["selected_shop_card"]

if selected_card_shop:

    st.divider()

    st.subheader(
        f"{SHOP_ICONS[selected_card_shop]} "
        f"{selected_card_shop} Shopping List"
    )

    shop_items = [
        item for item in items
        if item["shop"] == selected_card_shop
        and item["status"] == "Pending"
    ]

    if not shop_items:
        st.success(
            f"🎉 No pending products in {selected_card_shop}!"
        )

    else:
        st.markdown(f"**{len(shop_items)} product(s) to purchase**")

        for item in shop_items:

            with st.container(border=True):

                product_col, quantity_col, priority_col = st.columns(
                    [3, 2, 1.5]
                )

                with product_col:
                    st.markdown(f"### 📦 {item['product']}")
                    st.caption(f"Added by {item['added_by']}")

                with quantity_col:
                    st.markdown("**Quantity**")
                    st.write(display_quantity(item.get("quantity")))

                with priority_col:
                    st.markdown("**Priority**")

                    if item["priority"] == "High":
                        st.error("🔴 High")
                    elif item["priority"] == "Medium":
                        st.warning("🟠 Medium")
                    else:
                        st.success("🟢 Low")

                if item.get("notes"):
                    st.caption(f"📝 {item['notes']}")

                if st.button(
                    "✅ Mark as Purchased",
                    key=f"quick_buy_{item['id']}",
                    use_container_width=True
                ):

                    try:
                        update_item(item["id"], {
                            "status": "Purchased",
                            "purchased_at": datetime.now(
                                timezone.utc
                            ).isoformat()
                        })

                        st.rerun()

                    except Exception:
                        st.error("Could not update purchase status.")

    if st.button("✖ Close Shop List", key="close_shop_list"):
        st.session_state["selected_shop_card"] = None
        st.rerun()


st.divider()


# =========================================================
# ADD PRODUCT
# =========================================================

st.subheader("➕ Add a Product")
st.caption("Add something your family needs.")

with st.form("add_product", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:

        shop = st.selectbox("🏪 Select Shop", SHOPS)

        product = st.text_input(
            "📦 Product Name",
            placeholder="e.g. Rice, Hammer, Notebook"
        )

        quantity = st.text_input(
            "🔢 Quantity (optional)",
            placeholder="e.g. 5 kg, 12 pieces, 2 boxes"
        )

    with col2:

        priority = st.selectbox("🚦 Priority", PRIORITIES)
        added_by = st.selectbox("👤 Added By", PEOPLE)

        notes = st.text_input(
            "📝 Notes (optional)",
            placeholder="Any extra details..."
        )

    submitted = st.form_submit_button(
        "➕ Add to Shopping List",
        use_container_width=True
    )

    if submitted:

        if not product.strip():
            st.warning("Please enter the product name.")

        else:

            try:
                add_item({
                    "shop": shop,
                    "product": product.strip(),
                    "quantity": quantity.strip() or None,
                    "priority": priority,
                    "added_by": added_by,
                    "notes": notes.strip(),
                    "status": "Pending"
                })

                st.success(
                    f"🎉 {product.strip()} added successfully!"
                )
                st.rerun()

            except Exception:
                st.error("Could not add the product. Please try again.")


st.divider()


# =========================================================
# COMPLETE SHOPPING LIST
# =========================================================

st.subheader("📋 Complete Family Shopping List")

f1, f2 = st.columns(2)

with f1:
    selected_shop = st.selectbox(
        "🏪 Filter by Shop",
        ["All Shops"] + SHOPS,
        key="filter_shop"
    )

with f2:
    selected_status = st.selectbox(
        "📌 Filter by Status",
        ["Pending", "Purchased", "All"],
        key="filter_status"
    )


filtered_items = [
    item for item in items
    if (
        selected_shop == "All Shops"
        or item["shop"] == selected_shop
    )
    and (
        selected_status == "All"
        or item["status"] == selected_status
    )
]

st.markdown(f"**Showing {len(filtered_items)} product(s)**")

if not filtered_items:
    st.info("🛒 No products found for these filters.")

for item in filtered_items:

    status_icon = (
        "🟡" if item["status"] == "Pending"
        else "🟢"
    )

    shop_icon = SHOP_ICONS.get(item["shop"], "🛒")

    with st.expander(
        f"{status_icon} {shop_icon} "
        f"{item['product']} — {item['shop']}"
    ):

        info1, info2, info3 = st.columns(3)

        with info1:
            st.markdown("**📦 Quantity**")
            st.write(display_quantity(item.get("quantity")))

        with info2:
            st.markdown("**🚦 Priority**")
            st.write(item["priority"])

        with info3:
            st.markdown("**📌 Status**")
            st.write(item["status"])

        st.write(f"👤 **Added by:** {item['added_by']}")
        st.write(
            f"📅 **Date added:** "
            f"{format_date(item.get('created_at'))}"
        )

        if item.get("purchased_at"):
            st.write(
                f"🛍️ **Date purchased:** "
                f"{format_date(item.get('purchased_at'))}"
            )

        if item.get("notes"):
            st.write(f"📝 **Notes:** {item['notes']}")

        st.divider()
        st.markdown("### ✏️ Edit Product")

        with st.form(f"edit_{item['id']}"):

            new_product = st.text_input(
                "Product Name",
                value=item["product"],
                key=f"name_{item['id']}"
            )

            new_quantity = st.text_input(
                "Quantity (optional)",
                value=item.get("quantity") or "",
                key=f"qty_{item['id']}"
            )

            new_priority = st.selectbox(
                "Priority",
                PRIORITIES,
                index=PRIORITIES.index(item["priority"]),
                key=f"priority_{item['id']}"
            )

            new_notes = st.text_input(
                "Notes",
                value=item.get("notes") or "",
                key=f"notes_{item['id']}"
            )

            save = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )

            if save:

                if not new_product.strip():
                    st.warning("Please enter the product name.")

                else:

                    try:
                        update_item(item["id"], {
                            "product": new_product.strip(),
                            "quantity": new_quantity.strip() or None,
                            "priority": new_priority,
                            "notes": new_notes.strip()
                        })

                        st.success("Product updated successfully!")
                        st.rerun()

                    except Exception:
                        st.error("Could not update the product.")

        if item["status"] == "Pending":

            if st.button(
                "✅ Mark as Purchased",
                key=f"buy_{item['id']}",
                use_container_width=True
            ):

                try:
                    update_item(item["id"], {
                        "status": "Purchased",
                        "purchased_at": datetime.now(
                            timezone.utc
                        ).isoformat()
                    })

                    st.rerun()

                except Exception:
                    st.error("Could not update purchase status.")

        else:

            if st.button(
                "↩️ Mark as Pending",
                key=f"pending_{item['id']}",
                use_container_width=True
            ):

                try:
                    update_item(item["id"], {
                        "status": "Pending",
                        "purchased_at": None
                    })

                    st.rerun()

                except Exception:
                    st.error("Could not update purchase status.")

        with st.popover("🗑️ Delete Product"):

            st.warning(
                f"Are you sure you want to delete {item['product']}?"
            )

            if st.button(
                "Yes, Delete",
                key=f"delete_{item['id']}",
                type="primary"
            ):

                try:
                    delete_item(item["id"])
                    st.rerun()

                except Exception:
                    st.error("Could not delete the product.")


# =========================================================
# ALL-TIME SHOPPING HISTORY
# =========================================================

st.divider()

st.subheader("🕘 All-Time Shopping History")

st.caption(
    "View saved products, who added them, "
    "and when they were added or purchased."
)

with st.expander("📚 Open Shopping History", expanded=False):

    if not items:

        st.info(
            "Your shopping history will appear here "
            "after you add products."
        )

    else:

        h1, h2, h3 = st.columns(3)

        with h1:
            history_shop = st.selectbox(
                "Filter history by shop",
                ["All Shops"] + SHOPS,
                key="history_shop"
            )

        with h2:
            history_status = st.selectbox(
                "Filter history by status",
                ["All", "Pending", "Purchased"],
                key="history_status"
            )

        with h3:
            history_person = st.selectbox(
                "Filter history by family member",
                ["Everyone"] + PEOPLE,
                key="history_person"
            )

        history_items = [
            item for item in items
            if (
                history_shop == "All Shops"
                or item["shop"] == history_shop
            )
            and (
                history_status == "All"
                or item["status"] == history_status
            )
            and (
                history_person == "Everyone"
                or item["added_by"] == history_person
            )
        ]

        history_items.sort(
            key=lambda item: item.get("created_at") or "",
            reverse=True
        )

        st.markdown(
            f"### 📦 {len(history_items)} historical record(s)"
        )

        if not history_items:

            st.info("No history matches these filters.")

        else:

            for item in history_items:

                icon = (
                    "🟡" if item["status"] == "Pending"
                    else "🟢"
                )

                with st.expander(
                    f"{icon} {item['product']} — {item['shop']}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.markdown("**📦 Quantity**")
                        st.write(display_quantity(item.get("quantity")))

                        st.markdown("**🚦 Priority**")
                        st.write(item.get("priority", "—"))

                        st.markdown("**👤 Added by**")
                        st.write(item.get("added_by", "—"))

                    with col2:

                        st.markdown("**📌 Status**")
                        st.write(item.get("status", "—"))

                        st.markdown("**📅 Date added**")
                        st.write(
                            format_date(item.get("created_at"))
                        )

                        st.markdown("**🛍️ Date purchased**")
                        st.write(
                            format_date(item.get("purchased_at"))
                        )

                    if item.get("notes"):
                        st.markdown("**📝 Notes**")
                        st.write(item["notes"])

            # CSV DOWNLOAD WITHOUT PANDAS

            csv_buffer = io.StringIO()

            fieldnames = [
                "Product",
                "Shop",
                "Quantity",
                "Priority",
                "Added By",
                "Status",
                "Date Added",
                "Date Purchased",
                "Notes"
            ]

            writer = csv.DictWriter(
                csv_buffer,
                fieldnames=fieldnames
            )

            writer.writeheader()

            for item in history_items:

                writer.writerow({
                    "Product": item.get("product", ""),
                    "Shop": item.get("shop", ""),
                    "Quantity": item.get("quantity") or "",
                    "Priority": item.get("priority", ""),
                    "Added By": item.get("added_by", ""),
                    "Status": item.get("status", ""),
                    "Date Added": format_date(
                        item.get("created_at")
                    ),
                    "Date Purchased": format_date(
                        item.get("purchased_at")
                    ),
                    "Notes": item.get("notes") or ""
                })

            st.download_button(
                "⬇️ Download Shopping History (CSV)",
                data="\ufeff" + csv_buffer.getvalue(),
                file_name="dewangan_shop_history.csv",
                mime="text/csv",
                use_container_width=True
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()
show_footer()
