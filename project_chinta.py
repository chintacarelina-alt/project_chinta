import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Survey Analysis ✨",
    page_icon="🌸",
    layout="wide"
)

# --- 2. CUSTOM CSS (Pink Pastel Edition) ---
st.markdown("""
<style>
    /* Background Gradient Pink Pastel Lembut (Strawberry Milk) */
    .stApp {
        background-color: #fce4ec;
        background-image: linear-gradient(135deg, #fff0f6 0%, #f8bbd0 100%);
    }
    
    /* Judul: Warna Deep Raspberry biar kontras & ga nabrak */
    h1 {
        color: #880e4f; /* Pink Tua Gelap */
        font-family: 'Comic Sans MS', sans-serif;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.6); /* Kasih bayangan putih dikit */
    }
    
    /* Teks biasa biar agak gelap dikit biar kebaca */
    p, label, .stMarkdown {
        color: #4a148c; /* Ungu tua gelap */
    }

    /* Kotak Tabel & Card biar putih bersih */
    .stDataFrame, .stExpander {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Pemanis Selectbox */
    .stSelectbox > div > div {
        background-color: #ffffff;
        color: #880e4f;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LANGUAGE DICTIONARY ---
lang = {
    'EN': {
        'title': "✨ Survey Data Analysis Tool ✨",
        'sidebar_title': "⚙️ Configuration",
        'upload_label': "📂 Upload Data (CSV/Excel)",
        'desc_header': "📊 Descriptive Analysis",
        'assoc_header': "🔗 Association Analysis",
        'show_data': "👀 Raw Data Preview (All Rows)",
        'stats': "📈 Descriptive Statistics",
        'cat_dist': "Bar Chart (Categorical)",
        'num_dist': "Histogram (Numerical)",
        'corr_matrix': "❤️ Correlation Matrix",
        'crosstab': "🧩 Cross-Tabulation (Heatmap)",
        'select_col_x': "👉 Select Column X",
        'select_col_y': "👉 Select Column Y",
        'no_data': "👋 Please upload a dataset to begin!",
        'welcome': "Welcome! Let's analyze your data easily.",
        'success': "Yippii! File uploaded & Cleaned successfully :b 🎈",
        'warning_unique': "⚠️ Columns with too many unique values (Names, Emails) are hidden to prevent errors."
    },
    'ID': {
        'title': "✨ Alat Analisis Data Survei ✨",
        'sidebar_title': "⚙️ Konfigurasi",
        'upload_label': "📂 Unggah Data (CSV/Excel)",
        'desc_header': "📊 Analisis Deskriptif",
        'assoc_header': "🔗 Analisis Asosiasi",
        'show_data': "👀 Pratinjau Data (Semua Baris)",
        'stats': "📈 Statistik Deskriptif",
        'cat_dist': "Diagram Batang (Kategorikal)",
        'num_dist': "Histogram (Numerik)",
        'corr_matrix': "❤️ Matriks Korelasi",
        'crosstab': "🧩 Tabulasi Silang (Heatmap)",
        'select_col_x': "👉 Pilih Kolom X",
        'select_col_y': "👉 Pilih Kolom Y",
        'no_data': "👋 Silakan unggah dataset untuk memulai!",
        'welcome': "Selamat Datang! Mari analisis data dengan mudah.",
        'success': "Yippii! File berhasil diunggah & Dibersihkan ;B 🎈",
        'warning_unique': "⚠️ Kolom dengan terlalu banyak nilai unik (Nama, Email) disembunyikan agar grafik bagus."
    }
}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920349.png", width=80)
    selected_lang = st.selectbox("Language / Bahasa", ['EN', 'ID'])
    txt = lang[selected_lang]
    
    st.header(txt['sidebar_title'])
    uploaded_file = st.file_uploader(txt['upload_label'], type=['csv', 'xlsx'])

# --- 5. MAIN PAGE ---
st.title(txt['title'])
st.write(f"<center>{txt['welcome']}</center>", unsafe_allow_html=True)
st.markdown("---")

# Set Theme for Plots (Biar Grafiknya juga agak pinky)
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#fff0f6", "grid.color": "#f8bbd0"})

if uploaded_file is not None:
    # --- LOAD DATA ---
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # 🧹 SMART CLEANING ROBOT
        for col in df.columns:
            if any(x in col.lower() for x in ['usia', 'umur', 'age']):
                try:
                    df[col] = df[col].astype(str).str.extract(r'(\d+)')
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    pass
        
        if 'balloons_shown' not in st.session_state:
            st.balloons()
            st.toast(txt['success'], icon="🎈")
            st.session_state['balloons_shown'] = True

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # --- TABS ---
    tab1, tab2 = st.tabs([txt['desc_header'], txt['assoc_header']])

    # --- FILTER KOLOM ---
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    all_obj_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    valid_cat_cols = [c for c in all_obj_cols if df[c].nunique() < 50]

    # === TAB 1: DESCRIPTIVE ===
    with tab1:
        with st.expander(txt['show_data'], expanded=True):
            st.write(f"**Dimensions:** {df.shape[0]} Rows, {df.shape[1]} Columns")
            st.dataframe(df, height=500, use_container_width=True) 

        st.subheader(txt['stats'])
        st.dataframe(df.describe(), use_container_width=True)

        st.markdown("---")
        
        c1, c2 = st.columns(2)
        
        # Categorical Plot
        with c1:
            st.subheader(txt['cat_dist'])
            if len(valid_cat_cols) > 0:
                selected_cat = st.selectbox(f"{txt['select_col_x']} (Cat)", valid_cat_cols)
                fig, ax = plt.subplots(figsize=(6, 4))
                # Warna grafik jadi Pink Pastel (RdPu)
                sns.countplot(y=df[selected_cat], ax=ax, palette="RdPu", 
                              order=df[selected_cat].value_counts().iloc[:10].index)
                st.pyplot(fig)
            else:
                st.info("No categorical data available.")

        # Numerical Plot
        with c2:
            st.subheader(txt['num_dist'])
            if len(num_cols) > 0:
                selected_num = st.selectbox(f"{txt['select_col_x']} (Num)", num_cols)
                fig, ax = plt.subplots(figsize=(6, 4))
                # Warna Histogram Pink
                sns.histplot(df[selected_num], kde=True, ax=ax, color="#ec407a")
                st.pyplot(fig)
            else:
                st.info("No numerical data.")

    # === TAB 2: ASSOCIATION ===
    with tab2:
        st.subheader(txt['corr_matrix'])
        if len(num_cols) > 1:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(df[num_cols].corr(), annot=True, cmap='RdPu', ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Need 2+ numerical columns for correlation.")

        st.markdown("---")
        st.subheader(txt['crosstab'])
        st.caption(txt['warning_unique'])

        if len(valid_cat_cols) > 1:
            c_sel1, c_sel2 = st.columns(2)
            with c_sel1:
                x_col = st.selectbox(txt['select_col_x'], valid_cat_cols, key='cx')
            with c_sel2:
                y_col = st.selectbox(txt['select_col_y'], valid_cat_cols, key='cy', index=1)
            
            if x_col != y_col:
                ct = pd.crosstab(df[x_col], df[y_col])
                fig, ax = plt.subplots(figsize=(8, 5))
                # Heatmap warna Pink-Ungu biar aesthetic
                sns.heatmap(ct, annot=True, fmt='d', cmap="PuRd", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Pick different columns.")
        else:
            st.info("Need 2+ valid categorical columns.")

else:
    st.info(txt['no_data'])