import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Gym Exercise Database",
    page_icon="💪",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('db.csv')
    return df

# Main app
def main():
    st.title("💪 Gym Exercise Database")
    st.markdown("Browse and filter thousands of exercises for your workout routine")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Search bar
    search_query = st.sidebar.text_input("🔎 Search Exercise", "")
    
    # Primary filters
    st.sidebar.subheader("Primary Filters")
    
    # Classe filter
    classe_options = ['All'] + sorted(df['Classe'].dropna().unique().tolist())
    selected_classe = st.sidebar.selectbox("Classe", classe_options)
    
    # Gruppo muscolare filter
    gruppo_options = ['All'] + sorted(df['Gruppo muscolare'].dropna().unique().tolist())
    selected_gruppo = st.sidebar.selectbox("Gruppo Muscolare", gruppo_options)
    
    # Livello filter
    livello_options = ['All'] + sorted(df['Livello'].dropna().unique().tolist())
    selected_livello = st.sidebar.selectbox("Livello", livello_options)
    
    # Attrezzo filter
    attrezzo_options = ['All'] + sorted(df['Attrezzo'].dropna().unique().tolist())
    selected_attrezzo = st.sidebar.selectbox("Attrezzo", attrezzo_options)
    
    # Advanced filters (collapsible)
    with st.sidebar.expander("🎯 Advanced Filters"):
        # Training goals with sliders
        st.markdown("**Training Goals (1-5)**")
        ipertrofia_range = st.slider("Ipertrofia", 1, 5, (1, 5))
        forza_range = st.slider("Forza", 1, 5, (1, 5))
        potenza_range = st.slider("Potenza", 1, 5, (1, 5))
        resistenza_range = st.slider("Resistenza", 1, 5, (1, 5))
        
        # Other advanced filters
        difficolta_options = ['All'] + sorted([str(x) for x in df['Difficolta Apprendimento'].dropna().unique().tolist()])
        selected_difficolta = st.selectbox("Difficoltà Apprendimento", difficolta_options)
        
        spazio_options = ['All'] + sorted([str(x) for x in df['Spazio Necessario'].dropna().unique().tolist()])
        selected_spazio = st.selectbox("Spazio Necessario", spazio_options)
        
        rischio_options = ['All'] + sorted([str(x) for x in df['Rischio Infortuni'].dropna().unique().tolist()])
        selected_rischio = st.selectbox("Rischio Infortuni", rischio_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Search filter
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Esercizio'].str.contains(search_query, case=False, na=False) |
            filtered_df['Descrizione'].str.contains(search_query, case=False, na=False)
        ]
    
    # Primary filters
    if selected_classe != 'All':
        filtered_df = filtered_df[filtered_df['Classe'] == selected_classe]
    
    if selected_gruppo != 'All':
        filtered_df = filtered_df[filtered_df['Gruppo muscolare'] == selected_gruppo]
    
    if selected_livello != 'All':
        filtered_df = filtered_df[filtered_df['Livello'] == selected_livello]
    
    if selected_attrezzo != 'All':
        filtered_df = filtered_df[filtered_df['Attrezzo'] == selected_attrezzo]
    
    # Advanced filters
    # Convert to numeric for comparison
    filtered_df['Adatto Ipertrofia (1-5)_num'] = pd.to_numeric(filtered_df['Adatto Ipertrofia (1-5)'], errors='coerce')
    filtered_df['Adatto Forza_num'] = pd.to_numeric(filtered_df['Adatto Forza'], errors='coerce')
    filtered_df['Adatto Potenza (1-5)_num'] = pd.to_numeric(filtered_df['Adatto Potenza (1-5)'], errors='coerce')
    filtered_df['Adatto Resistenza (1-5)_num'] = pd.to_numeric(filtered_df['Adatto Resistenza (1-5)'], errors='coerce')
    
    # Only apply filters if not at default range (1-5)
    if ipertrofia_range != (1, 5):
        filtered_df = filtered_df[
            (filtered_df['Adatto Ipertrofia (1-5)_num'] >= ipertrofia_range[0]) &
            (filtered_df['Adatto Ipertrofia (1-5)_num'] <= ipertrofia_range[1])
        ]
    
    if forza_range != (1, 5):
        filtered_df = filtered_df[
            (filtered_df['Adatto Forza_num'] >= forza_range[0]) &
            (filtered_df['Adatto Forza_num'] <= forza_range[1])
        ]
    
    if potenza_range != (1, 5):
        filtered_df = filtered_df[
            (filtered_df['Adatto Potenza (1-5)_num'] >= potenza_range[0]) &
            (filtered_df['Adatto Potenza (1-5)_num'] <= potenza_range[1])
        ]
    
    if resistenza_range != (1, 5):
        filtered_df = filtered_df[
            (filtered_df['Adatto Resistenza (1-5)_num'] >= resistenza_range[0]) &
            (filtered_df['Adatto Resistenza (1-5)_num'] <= resistenza_range[1])
        ]
    
    if selected_difficolta != 'All':
        filtered_df = filtered_df[filtered_df['Difficolta Apprendimento'].astype(str) == selected_difficolta]
    
    if selected_spazio != 'All':
        filtered_df = filtered_df[filtered_df['Spazio Necessario'].astype(str) == selected_spazio]
    
    if selected_rischio != 'All':
        filtered_df = filtered_df[filtered_df['Rischio Infortuni'].astype(str) == selected_rischio]
    
    # Drop temporary numeric columns
    filtered_df = filtered_df.drop(columns=['Adatto Ipertrofia (1-5)_num', 'Adatto Forza_num', 
                                             'Adatto Potenza (1-5)_num', 'Adatto Resistenza (1-5)_num'])
    
    # Display results
    st.subheader(f"📊 Results: {len(filtered_df)} exercises found")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Exercises", len(filtered_df))
    with col2:
        st.metric("Muscle Groups", filtered_df['Gruppo muscolare'].nunique())
    with col3:
        st.metric("Equipment Types", filtered_df['Attrezzo'].nunique())
    with col4:
        avg_difficulty = filtered_df['Difficolta Apprendimento'].mode()[0] if len(filtered_df) > 0 else "N/A"
        st.metric("Most Common Difficulty", avg_difficulty)
    
    # Display columns selection
    display_columns = [
        'Esercizio', 'Gruppo muscolare', 'Livello', 'Attrezzo', 'Obiettivo',
        'Adatto Ipertrofia (1-5)', 'Adatto Forza', 'Difficolta Apprendimento',
        'Spazio Necessario', 'Rischio Infortuni', 'Classe'
    ]
    
    # Show dataframe
    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        height=600
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download filtered results as CSV",
        data=csv,
        file_name='filtered_exercises.csv',
        mime='text/csv',
    )
    
    # Exercise details expander
    if len(filtered_df) > 0:
        st.subheader("🔍 Exercise Details")
        selected_exercise = st.selectbox(
            "Select an exercise to view details:",
            filtered_df['Esercizio'].tolist()
        )
        
        if selected_exercise:
            exercise_data = filtered_df[filtered_df['Esercizio'] == selected_exercise].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Basic Info")
                st.markdown(f"**Exercise:** {exercise_data['Esercizio']}")
                st.markdown(f"**Muscle Group:** {exercise_data['Gruppo muscolare']}")
                st.markdown(f"**Equipment:** {exercise_data['Attrezzo']}")
                st.markdown(f"**Level:** {exercise_data['Livello']}")
                st.markdown(f"**Objective:** {exercise_data['Obiettivo']}")
                
                if pd.notna(exercise_data['Descrizione']):
                    st.markdown("### Description")
                    st.write(exercise_data['Descrizione'])
            
            with col2:
                st.markdown("### Training Metrics")
                st.markdown(f"**Hypertrophy:** {exercise_data['Adatto Ipertrofia (1-5)']}/5")
                st.markdown(f"**Strength:** {exercise_data['Adatto Forza']}/5")
                st.markdown(f"**Power:** {exercise_data['Adatto Potenza (1-5)']}/5")
                st.markdown(f"**Endurance:** {exercise_data['Adatto Resistenza (1-5)']}/5")
                st.markdown(f"**Difficulty:** {exercise_data['Difficolta Apprendimento']}")
                st.markdown(f"**Space Required:** {exercise_data['Spazio Necessario']}")
                st.markdown(f"**Injury Risk:** {exercise_data['Rischio Infortuni']}")
                
                if pd.notna(exercise_data.get('Reps Target')):
                    st.markdown(f"**Target Reps:** {exercise_data['Reps Target']}")
                if pd.notna(exercise_data.get('Serie Target')):
                    st.markdown(f"**Target Sets:** {exercise_data['Serie Target']}")

if __name__ == "__main__":
    main()

