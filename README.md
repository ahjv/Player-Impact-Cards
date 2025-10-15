# Player Impact Cards

Player Impact Cards is a web application that visualizes the true on-court impact of NBA players. It moves beyond traditional box score statistics to show how each player influences team performance on both offense and defense.

## Overview
The project combines advanced analytics and clear data visualization to make basketball performance easier to understand. Each player’s card highlights key performance metrics that summarize their strengths, weaknesses, and overall impact in one accessible view.

## Features
- Comprehensive impact metrics, including on/off splits, efficiency differentials, and matchup-adjusted defensive ratings.  
- Custom formulas such as Defensive Impact Score (DIS) and Offensive Creation Index (OCI) to provide deeper insight.  
- Responsive React dashboard built with Next.js and TailwindCSS for a clean, intuitive interface.  
- Data pipeline for scraping, cleaning, and aggregating statistics before storing them in DynamoDB.  
- Interactive comparison tools to explore player and team-level trends.

## Tech Stack
- **Frontend:** Next.js, React, TailwindCSS, Recharts  
- **Backend:** Node.js, Express  
- **Database:** DynamoDB  
- **Data Processing:** Python (pandas, NumPy)

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/ahjv/Player-Impact-Cards.git
   cd Player-Impact-Cards
2. Install Dependencies;
   npm install

3. Run Development Server;
    npm start

