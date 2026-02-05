1: Requirements.txt (Lists libraries for easy installation) scikit-learn numpy

2: .gitignore (Ignores unnecessary files like database or cache) pycache/ *.pyc learning_graph.db .DS_Store

4:

AI-Driven Personalized Learning Path Generator
Overview
This is an AI-driven application that generates personalized learning paths based on user skills and goals. It uses a knowledge graph stored in SQL, graph algorithms for path finding, and machine learning for complexity predictions. The project combines Python, SQL, and AI to create a unique tool for educational planning.

Features
Knowledge Graph: Topics and prerequisites stored in SQLite database.
Path Generation: Recommends step-by-step learning paths.
AI Predictions: Uses machine learning to predict path complexity.
User-Friendly: Simple command-line interface.
Technologies Used
Python 3.12.0
SQLite (for database)
scikit-learn (for machine learning)
NumPy
Installation
Clone the repository: git clone https://github.com/aarushdeshmukh/LearningPathGenerator.git
Navigate to the folder: cd LearningPathGenerator
Install dependencies: pip install -r requirements.txt
Run the app: python learning_path.py
Usage
Enter your current skill (e.g., "python basics").
Enter your goal (e.g., "machine learning").
Get a recommended path and complexity score.
Example Output
Author
Name: [Aarush Deshmukh]
College Year: [3rd Year]
License
This project is open-source. Feel free to contribute!

Contributing
Fork the repo, make changes, and submit a pull request.
