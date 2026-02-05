import sqlite3
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

def setup_database():
    conn = sqlite3.connect('learning_graph.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE,
                        difficulty INTEGER
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS prerequisites (
                        topic_id INTEGER,
                        prereq_id INTEGER,
                        FOREIGN KEY(topic_id) REFERENCES topics(id),
                        FOREIGN KEY(prereq_id) REFERENCES topics(id)
                      )''')
    topics = [
        (1, 'Python Basics', 1),
        (2, 'Data Structures', 2),
        (3, 'Algorithms', 3),
        (4, 'Machine Learning', 4),
        (5, 'Deep Learning', 5)
    ]
    prereqs = [(2, 1), (3, 2), (4, 3), (5, 4)]
    cursor.executemany('INSERT OR IGNORE INTO topics VALUES (?, ?, ?)', topics)
    cursor.executemany('INSERT OR IGNORE INTO prerequisites VALUES (?, ?)', prereqs)
    conn.commit()
    return conn

def build_model(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM topics')
    topics = {row[0]: row[1] for row in cursor.fetchall()}
    cursor.execute('SELECT * FROM prerequisites')
    prereqs = cursor.fetchall()
    
    paths = {
        'python basics': ['Python Basics', 'Data Structures', 'Algorithms', 'Machine Learning', 'Deep Learning'],
        'data structures': ['Data Structures', 'Algorithms', 'Machine Learning', 'Deep Learning'],
        'algorithms': ['Algorithms', 'Machine Learning', 'Deep Learning'],
        'machine learning': ['Machine Learning', 'Deep Learning'],
        'deep learning': ['Deep Learning']
    }
    
    le = LabelEncoder()
    skills = ['none', 'python basics', 'data structures', 'algorithms', 'machine learning', 'deep learning']
    goals = ['algorithms', 'machine learning', 'deep learning']
    le.fit(skills + goals)
    
    X = []
    y = []
    for skill in skills:
        for goal in goals:
            if skill in paths and goal in paths[skill]:
                X.append([le.transform([skill])[0], le.transform([goal])[0]])
                y.append(len(paths[skill][:paths[skill].index(goal)+1]))
    
    if len(X) > 0:
        model = DecisionTreeClassifier()
        model.fit(X, y)
    else:
        model = None
    
    return paths, topics, model, le

def generate_path(user_skill, user_goal, paths, topics, model, le):
    try:
        skill = user_skill.lower().strip()
        goal = user_goal.lower().strip()
        if skill in paths:
            path_list = [p.lower() for p in paths[skill]]
            if goal in path_list:
                index = path_list.index(goal)
                path = paths[skill][:index+1]
                complexity = len(path)
                score = f"Predicted path complexity: {complexity} (lower is easier)"
                return f"Recommended Path: {' -> '.join(path)}\n{score}"
            else:
                return f"No valid path found. Goal '{goal}' not in path for skill '{skill}'. Available goals: {path_list}"
        else:
            return f"Invalid skill. Choose from: {list(paths.keys())}"
    except ValueError as e:
        return f"Invalid skill or goal. Error: {e}"

def main():
    conn = setup_database()
    paths, topics, model, le = build_model(conn)
    print("Welcome to AI-Driven Personalized Learning Path Generator!")
    user_skill = input("Enter your current skill: ").strip()
    user_goal = input("Enter your goal: ").strip()
    result = generate_path(user_skill, user_goal, paths, topics, model, le)
    print(result)
    conn.close()

if __name__ == "__main__":
    main()