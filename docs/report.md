# Smart Expense Tracker with Analytics
**Final Year Project Report**

## 1. Title Page
**Project Title**: Smart Expense Tracker with Analytics
**Developed By**: [Student Name]
**Supervised By**: [Supervisor Name]
**Institution**: [University/College Name]
**Date**: [Date]

## 2. Abstract
This project introduces a comprehensive Smart Expense Tracker designed to help individuals monitor their financial habits. The application provides an intuitive graphical user interface for tracking daily expenses, setting monthly budgets, and visualizing spending patterns through analytics. Developed using Python, Tkinter, and SQLite, it emphasizes object-oriented programming, data persistence, and robust exception handling.

## 3. Acknowledgement
I would like to express my sincere gratitude to my supervisor and peers for their continuous support and guidance throughout the development of this project.

## 4. Table of Contents
1. Introduction
2. Problem Statement
3. Objectives
4. Scope
5. Technologies
6. Functional Requirements
7. Non-Functional Requirements
8. Agile Model
9. System Design
10. Database Design
11. GUI Design
12. Implementation
13. Testing
14. Software Process Improvement (SPI)
15. Refactoring
16. Exception Handling
17. GitHub Integration
18. Deployment
19. Peer Review
20. Conclusion & Future Work

## 5. Introduction
Managing personal finances can be challenging without proper tools. The Smart Expense Tracker offers a reliable, offline, desktop-based solution to track income and expenses efficiently.

## 6. Problem Statement
Many existing expense trackers are either overly complex, require continuous internet connectivity, or lack visual analytics. There is a need for a lightweight, secure, desktop application that provides quick data entry and insightful graphical summaries.

## 7. Objectives
- Develop a user-friendly desktop GUI.
- Implement robust CRUD operations for expenses.
- Provide data visualization for spending analysis.
- Ensure data security via offline SQLite storage and authentication.

## 8. Scope
The application is designed for individual users on Windows platforms. It covers expense logging, categorizing, budgeting, and exporting data, but does not include multi-user network synchronization.

## 9. Technologies
- **Programming Language**: Python 3
- **GUI Framework**: Tkinter
- **Database**: SQLite3
- **Visualization**: Matplotlib
- **Testing**: `unittest`

## 10. Functional Requirements
- User registration and login.
- Add, Edit, Delete, and View expenses.
- Categorize expenses.
- Set monthly budgets.
- Generate and view analytical charts.
- Export expense data to CSV.

## 11. Non-Functional Requirements
- **Performance**: The application must load within 3 seconds.
- **Reliability**: Graceful error handling for invalid inputs.
- **Usability**: Intuitive design requiring minimal learning.

## 12. Agile Model
This project followed Agile methodology:
- **Sprint Planning**: Divided tasks into UI setup, database schema, CRUD logic, and analytics.
- **Iterative Development**: Built the core database first, followed by basic UI, then advanced features.
- **Continuous Testing**: Unit tests were written and run frequently.
- **Feedback Integration**: UI was adjusted based on peer testing.

## 13. System Design
The application uses an MVC-inspired architecture, separating GUI elements (`src/gui`), business logic (`src/models.py`), and data access (`src/database.py`).

## 14. Use Case Diagram
- **User**: Logs in -> Adds Expense -> Views Dashboard -> Generates Report -> Exports CSV.
*(For detailed UML, see uml_diagrams.md)*

## 15. Flowcharts
Start -> Login/Register -> Dashboard -> [Add Expense | View Analytics | Export] -> Logout -> End.

## 16. Database Design
- **Users**: id, username, password, theme
- **Categories**: id, user_id, name
- **Expenses**: id, user_id, category_id, amount, date, description
- **Budgets**: id, user_id, month, year, amount

## 17. GUI Design
Clean, modern interface utilizing Tkinter's `ttk` styles. Includes a dark/light mode toggle for better accessibility.

## 18. Implementation
Developed using OOP principles. Custom exceptions (`AppError`) manage application state cleanly.

## 19. Testing
Automated unit testing covers model validations, database connections, and utility functions using the Python `unittest` module.

## 20. Software Process Improvement (SPI)
- **Initial Issues**: Hardcoded database paths caused crashes on different machines.
- **Improvement**: Implemented dynamic path resolution and a robust `init_db()` startup check.
- **UI Enhancements**: Transitioned from basic Tkinter widgets to styled `ttk` widgets.

## 21. Refactoring
Legacy monolithic code was refactored into a modular package (`src/`), eliminating duplication and improving readability. For example, database connection logic was centralized in `get_connection()`.

## 22. Exception Handling
Comprehensive `try...except...finally` blocks ensure the application does not crash on invalid input or file locks, utilizing Tkinter `messagebox` for user alerts.

## 23. GitHub
Version control was maintained using Git, with frequent, descriptive commits. See `github_guide.md` for details.

## 24. Deployment
Packaged into a standalone Windows executable using PyInstaller. See `deployment.md` for instructions.

## 25. Peer Review
Feedback indicated the need for a dark mode, which was subsequently implemented. Input validation was tightened based on beta testing.

## 26. Learning Outcomes
Gained proficiency in Tkinter UI design, SQLite integration, Matplotlib visualization, and Python packaging.

## 27. Conclusion
The Smart Expense Tracker successfully meets all functional requirements, providing a robust tool for personal financial management.

## 28. Future Work
- Integration with bank APIs.
- Receipt scanning via OCR.
- Mobile application counterpart.

## 29. References
- Python Documentation: https://docs.python.org/3/
- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
- Matplotlib Documentation: https://matplotlib.org/
