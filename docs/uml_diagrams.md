# Smart Expense Tracker - Comprehensive UML Diagrams

This document contains professional, high-resolution UML diagrams for the **Smart Expense Tracker** project. 
To ensure perfectly centered connections (exactly attaching to the middle-left, middle-right, top-center, and bottom-center), these diagrams strictly utilize directional layouts (Left-to-Right `LR` and Top-to-Bottom `TB`) which automatically enforce clean, non-overlapping routing.

---

## 1. Use Case Diagram
**Purpose:** Maps out the interactions between the User (Actor) and the core features of the system.
**Layout:** Left-to-Right (`LR`) ensures arrows exit the right side of the actor and enter exactly the middle-left side of each use case oval.

```mermaid
flowchart LR
    %% Actor
    User((User))

    %% System Boundary
    subgraph "Smart Expense Tracker System"
        direction TB
        UC1(["Register / Login"])
        UC2(["Add Expense"])
        UC3(["Edit / Delete Expense"])
        UC4(["Manage Categories"])
        UC5(["Set Monthly Budget"])
        UC6(["View Visual Analytics"])
        UC7(["Export Data to CSV"])
        UC8(["Toggle Dark/Light Theme"])
    end

    %% Clean precise connections
    User ==> UC1
    User ==> UC2
    User ==> UC3
    User ==> UC4
    User ==> UC5
    User ==> UC6
    User ==> UC7
    User ==> UC8
```

---

## 2. Class Diagram
**Purpose:** Defines the Object-Oriented structure, including class properties, methods, and relationships.
**Layout:** Left-to-Right (`LR`) to cleanly align associations and inheritance arrows without overcrowding.

```mermaid
classDiagram
    direction LR

    class User {
        +int id
        +String username
        +String theme_preference
        +register(username, password) User
        +login(username, password) User
        +update_theme(theme)
    }

    class Category {
        +int id
        +int user_id
        +String name
        +create(user_id, name) Category
        +get_all(user_id) List~Category~
        +initialize_defaults(user_id)
    }

    class Expense {
        +int id
        +int user_id
        +int category_id
        +float amount
        +String date
        +String description
        +add(user_id, category_id, amount, date, desc) Expense
        +update(id, amount, date, desc, category_id)
        +delete(id)
        +get_all(user_id, search_term, category_id) List~Expense~
    }

    class Budget {
        +int id
        +int user_id
        +int month
        +int year
        +float amount
        +set_budget(user_id, month, year, amount)
        +get_budget(user_id, month, year) float
    }

    %% Relationships connecting middle-right to middle-left
    User "1" --> "*" Category : manages >
    User "1" --> "*" Expense : logs >
    User "1" --> "*" Budget : sets >
    Category "1" <-- "*" Expense : < categorized by
```

---

## 3. Sequence Diagram (Adding an Expense)
**Purpose:** Details the step-by-step chronological sequence of operations when a user adds a new expense.
**Layout:** Time flows from top to bottom. Horizontal messages perfectly align to the exact center of each participant's vertical lifeline.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant DashboardView
    participant ExpenseModel
    participant Database

    User->>DashboardView: Enters amount, category, date, desc
    User->>DashboardView: Clicks "Save Expense"
    DashboardView->>ExpenseModel: add(user_id, category_id, amount, date, desc)
    
    rect rgb(240, 248, 255)
        ExpenseModel->>ExpenseModel: Validate amount > 0
        ExpenseModel->>ExpenseModel: Validate date format
    end

    ExpenseModel->>Database: INSERT INTO expenses...
    Database-->>ExpenseModel: return last_row_id
    ExpenseModel-->>DashboardView: return Expense Object
    
    DashboardView->>Database: Fetch updated expenses list
    Database-->>DashboardView: Return updated list
    DashboardView-->>User: Refresh Table & Show Success Message
```

---

## 4. Activity Diagram (System Login & Dashboard Flow)
**Purpose:** Illustrates the workflow and decision paths within the application.
**Layout:** Top-to-Bottom (`TB`) guarantees that control arrows attach exactly to the top and bottom center points of each state box and decision diamond.

```mermaid
flowchart TB
    %% Nodes
    Start([Start Application])
    InitDB[Initialize SQLite Database]
    ShowAuth[Show Login/Register Screen]
    InputCreds[/User Enters Credentials/]
    Validate{Credentials Valid?}
    
    ShowDash[Load Dashboard View]
    FetchData[Fetch Expenses & Budgets]
    UserAction{Select Action}
    
    AddExp[Add New Expense]
    ViewChart[View Analytics Chart]
    ExportCSV[Export CSV Report]
    
    Logout([Logout / End])

    %% Clean, vertically aligned connections
    Start --> InitDB
    InitDB --> ShowAuth
    ShowAuth --> InputCreds
    InputCreds --> Validate
    
    Validate -- No --> ShowAuth
    Validate -- Yes --> ShowDash
    
    ShowDash --> FetchData
    FetchData --> UserAction
    
    UserAction --> AddExp
    UserAction --> ViewChart
    UserAction --> ExportCSV
    
    AddExp --> FetchData
    ViewChart --> UserAction
    ExportCSV --> UserAction
    
    UserAction --> Logout
```
