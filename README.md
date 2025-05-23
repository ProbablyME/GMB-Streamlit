# GMBLERS Analytics Dashboard

A Streamlit-based analytics dashboard for League of Legends team data.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Secrets
Copy the example secrets file and configure your actual values:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then edit `.streamlit/secrets.toml` with your actual values:

```toml
[auth]
password = "your_actual_password"

[database]
mongodb_connection_string = "your_actual_mongodb_connection_string"
```

**Important:** Never commit the actual `secrets.toml` file to version control. It's already included in `.gitignore`.

### 3. Run the Application
```bash
streamlit run app.py
```

## Features

- **Scrims Overview**: Detailed view of individual games with draft analysis, scoreboard, and player performance
- **Team Stats**: Overall team statistics including win rates, objective control, and side preference
- **Player Stats**: Individual player performance metrics and game history

## Security

This application uses Streamlit's built-in secrets management to protect sensitive information:
- Authentication password stored in secrets
- Database connection strings stored in secrets
- Secrets file excluded from version control 