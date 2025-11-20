# 💪 Gym Exercise Database

A comprehensive web application for browsing and filtering thousands of gym exercises, including Palestra (gym) and Calisthenics workouts.

## Features

- 🔍 **Search**: Search exercises by name or description
- 🎯 **Smart Filters**: Filter by muscle group, equipment, level, and more
- 📊 **Advanced Filters**: Filter by training goals (hypertrophy, strength, power, endurance)
- 📱 **Responsive Design**: Works on desktop and mobile
- ⬇️ **Export**: Download filtered results as CSV

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd gym
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Make sure you have these files in your repository:
   - `app.py` (the Streamlit app)
   - `cb.csv` (your exercise database)
   - `requirements.txt` (Python dependencies)
   - `.streamlit/config.toml` (optional: theme configuration)

2. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit - Gym Exercise Database"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file path (`app.py`)
5. Click "Deploy"

Your app will be live in a few minutes at: `https://share.streamlit.io/[your-username]/[your-repo]/main/app.py`

### Step 3: (Optional) Custom Domain

Once deployed, you can set up a custom domain in the Streamlit Cloud settings.

## Data Structure

The app uses a CSV file (`cb.csv`) with the following key columns:

- **Esercizio**: Exercise name
- **Gruppo muscolare**: Muscle group
- **Attrezzo**: Equipment needed
- **Livello**: Difficulty level (Principiante, Intermedio, Avanzato)
- **Classe**: Category (Palestra, Chalistenics)
- **Training goals**: Ratings for hypertrophy, strength, power, endurance (1-5)
- And 50+ more detailed attributes

## Usage

1. **Search**: Use the search bar to find specific exercises
2. **Filter**: Select filters from the sidebar to narrow down results
3. **View Details**: Click on an exercise name in the dropdown to see full details
4. **Export**: Download your filtered results as CSV

## Technologies Used

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Python**: Backend logic

## License

MIT License

## Author

Davide Baldelli

