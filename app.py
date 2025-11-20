import streamlit as st
import pandas as pd
import numpy as np
import re

# Page configuration
st.set_page_config(
    page_title="BlueGym",
    page_icon="💪",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('db.csv')
    return df

def parse_rating(value):
    """Parse rating values like '3-4', '4 (Molto buono)', etc. to numeric"""
    if pd.isna(value):
        return None
    
    value_str = str(value).strip()
    
    # Extract first number from the string
    match = re.search(r'(\d+)', value_str)
    if match:
        return int(match.group(1))
    return None

def is_in_range(value, min_val, max_val):
    """Check if a rating value falls within the specified range"""
    if pd.isna(value):
        return True  # Include rows with missing values
    
    value_str = str(value).strip()
    
    # Handle range values like "3-4"
    if '-' in value_str:
        parts = value_str.split('-')
        try:
            low = int(parts[0])
            high = int(parts[1])
            # Check if the range overlaps with the filter range
            return not (high < min_val or low > max_val)
        except:
            pass
    
    # Extract numeric value
    parsed = parse_rating(value)
    if parsed is None:
        return True  # Include if we can't parse
    
    return min_val <= parsed <= max_val

# Main app
def main():
    st.title("💪 BlueGym")
    st.markdown("Esplora e filtra migliaia di esercizi per la tua routine di allenamento")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filtri")
    
    # Search bar
    search_query = st.sidebar.text_input("🔎 Cerca Esercizio", "")
    
    # Primary filters
    st.sidebar.subheader("Filtri Principali")
    
    # Classe filter
    classe_options = ['Tutti'] + sorted(df['Classe'].dropna().unique().tolist())
    selected_classe = st.sidebar.selectbox("Classe", classe_options)
    
    # Gruppo muscolare filter
    gruppo_options = ['Tutti'] + sorted(df['Gruppo muscolare'].dropna().unique().tolist())
    selected_gruppo = st.sidebar.selectbox("Gruppo Muscolare", gruppo_options)
    
    # Livello filter
    livello_options = ['Tutti'] + sorted(df['Livello'].dropna().unique().tolist())
    selected_livello = st.sidebar.selectbox("Livello", livello_options)
    
    # Attrezzo filter
    attrezzo_options = ['Tutti'] + sorted(df['Attrezzo'].dropna().unique().tolist())
    selected_attrezzo = st.sidebar.selectbox("Attrezzo", attrezzo_options)
    
    # Advanced filters (collapsible)
    with st.sidebar.expander("🎯 Filtri Avanzati"):
        # Training goals with sliders
        st.markdown("**Obiettivi di Allenamento (1-5)**")
        ipertrofia_range = st.slider("Ipertrofia", 1, 5, (1, 5))
        forza_range = st.slider("Forza", 1, 5, (1, 5))
        potenza_range = st.slider("Potenza", 1, 5, (1, 5))
        resistenza_range = st.slider("Resistenza", 1, 5, (1, 5))
        
        # Other advanced filters
        difficolta_options = ['Tutti'] + sorted([str(x) for x in df['Difficolta Apprendimento'].dropna().unique().tolist()])
        selected_difficolta = st.selectbox("Difficoltà Apprendimento", difficolta_options)
        
        spazio_options = ['Tutti'] + sorted([str(x) for x in df['Spazio Necessario'].dropna().unique().tolist()])
        selected_spazio = st.selectbox("Spazio Necessario", spazio_options)
        
        rischio_options = ['Tutti'] + sorted([str(x) for x in df['Rischio Infortuni'].dropna().unique().tolist()])
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
    if selected_classe != 'Tutti':
        filtered_df = filtered_df[filtered_df['Classe'] == selected_classe]
    
    if selected_gruppo != 'Tutti':
        filtered_df = filtered_df[filtered_df['Gruppo muscolare'] == selected_gruppo]
    
    if selected_livello != 'Tutti':
        filtered_df = filtered_df[filtered_df['Livello'] == selected_livello]
    
    if selected_attrezzo != 'Tutti':
        filtered_df = filtered_df[filtered_df['Attrezzo'] == selected_attrezzo]
    
    # Advanced filters - Training goals
    # Only filter if slider is changed from default
    if ipertrofia_range != (1, 5):
        filtered_df = filtered_df[
            filtered_df['Adatto Ipertrofia (1-5)'].apply(
                lambda x: is_in_range(x, ipertrofia_range[0], ipertrofia_range[1])
            )
        ]
    
    if forza_range != (1, 5):
        filtered_df = filtered_df[
            filtered_df['Adatto Forza'].apply(
                lambda x: is_in_range(x, forza_range[0], forza_range[1])
            )
        ]
    
    if potenza_range != (1, 5):
        filtered_df = filtered_df[
            filtered_df['Adatto Potenza (1-5)'].apply(
                lambda x: is_in_range(x, potenza_range[0], potenza_range[1])
            )
        ]
    
    if resistenza_range != (1, 5):
        filtered_df = filtered_df[
            filtered_df['Adatto Resistenza (1-5)'].apply(
                lambda x: is_in_range(x, resistenza_range[0], resistenza_range[1])
            )
        ]
    
    if selected_difficolta != 'Tutti':
        filtered_df = filtered_df[filtered_df['Difficolta Apprendimento'].astype(str) == selected_difficolta]
    
    if selected_spazio != 'Tutti':
        filtered_df = filtered_df[filtered_df['Spazio Necessario'].astype(str) == selected_spazio]
    
    if selected_rischio != 'Tutti':
        filtered_df = filtered_df[filtered_df['Rischio Infortuni'].astype(str) == selected_rischio]
    
    # Display results
    st.subheader(f"📊 Risultati: {len(filtered_df)} esercizi trovati")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Esercizi Totali", len(filtered_df))
    with col2:
        st.metric("Gruppi Muscolari", filtered_df['Gruppo muscolare'].nunique())
    with col3:
        st.metric("Tipi di Attrezzo", filtered_df['Attrezzo'].nunique())
    with col4:
        if len(filtered_df) > 0 and filtered_df['Difficolta Apprendimento'].mode().shape[0] > 0:
            avg_difficulty = filtered_df['Difficolta Apprendimento'].mode()[0]
        else:
            avg_difficulty = "N/A"
        st.metric("Difficoltà Più Comune", avg_difficulty)
    
    # Display columns selection
    display_columns = [
        'Esercizio', 'Gruppo muscolare', 'Livello', 'Attrezzo', 'Obiettivo',
        'Adatto Ipertrofia (1-5)', 'Adatto Forza', 'Difficolta Apprendimento',
        'Spazio Necessario', 'Rischio Infortuni', 'Classe'
    ]
    
    # Show dataframe
    if len(filtered_df) > 0:
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            height=600
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Scarica risultati filtrati come CSV",
            data=csv,
            file_name='esercizi_filtrati.csv',
            mime='text/csv',
        )
        
        # Exercise details expander
        st.subheader("🔍 Dettagli Esercizio")
        selected_exercise = st.selectbox(
            "Seleziona un esercizio per visualizzare i dettagli:",
            filtered_df['Esercizio'].tolist()
        )
        
        if selected_exercise:
            exercise_data = filtered_df[filtered_df['Esercizio'] == selected_exercise].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Informazioni Base")
                st.markdown(f"**Esercizio:** {exercise_data['Esercizio']}")
                st.markdown(f"**Gruppo Muscolare:** {exercise_data['Gruppo muscolare']}")
                st.markdown(f"**Attrezzo:** {exercise_data['Attrezzo']}")
                st.markdown(f"**Livello:** {exercise_data['Livello']}")
                st.markdown(f"**Obiettivo:** {exercise_data['Obiettivo']}")
                
                if pd.notna(exercise_data['Descrizione']):
                    st.markdown("### Descrizione")
                    st.write(exercise_data['Descrizione'])
            
            with col2:
                st.markdown("### Metriche di Allenamento")
                st.markdown(f"**Ipertrofia:** {exercise_data['Adatto Ipertrofia (1-5)']}")
                st.markdown(f"**Forza:** {exercise_data['Adatto Forza']}")
                st.markdown(f"**Potenza:** {exercise_data['Adatto Potenza (1-5)']}")
                st.markdown(f"**Resistenza:** {exercise_data['Adatto Resistenza (1-5)']}")
                st.markdown(f"**Difficoltà:** {exercise_data['Difficolta Apprendimento']}")
                st.markdown(f"**Spazio Richiesto:** {exercise_data['Spazio Necessario']}")
                st.markdown(f"**Rischio Infortuni:** {exercise_data['Rischio Infortuni']}")
                
                if pd.notna(exercise_data.get('Reps Target')):
                    st.markdown(f"**Ripetizioni Target:** {exercise_data['Reps Target']}")
                if pd.notna(exercise_data.get('Serie Target')):
                    st.markdown(f"**Serie Target:** {exercise_data['Serie Target']}")
    else:
        st.warning("⚠️ Nessun esercizio trovato con i filtri selezionati. Prova a modificare i criteri di ricerca.")

if __name__ == "__main__":
    main()
