# Smart Campus Queue Management System

A comprehensive web-based queue management system for campus services built with Flask (Python) and vanilla JavaScript. This project demonstrates the implementation of core data structures and algorithms in a practical, real-world application.

## 🎯 Project Overview

This system manages queues for campus service counters (Finance Office, Library, and Administration). It issues tokens, handles normal and priority queues, predicts waiting times, supports staff queue operations, and generates rating analytics.

**Important Note:** This system intentionally does NOT use a database. All data is stored in-memory using Python data structures to clearly demonstrate how these structures work in practice. Data will reset when the server restarts - this is by design.

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Running

1. Navigate to the project directory:
```bash
cd smart_queue
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:3000
```

The application will be running on port 3000.

## 📁 Project Structure

```
smart_queue/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── routes/
│   ├── user_routes.py              # User-facing API endpoints
│   └── staff_routes.py             # Staff API endpoints
├── services/
│   ├── queue_service.py            # Main business logic
│   ├── algorithms.py               # All algorithms implementation
│   └── data_structures/
│       ├── normal_queue.py         # FIFO queue using deque
│       ├── priority_heap.py        # Min-heap for priority queue
│       ├── skipped_stack.py        # LIFO stack for skipped tokens
│       ├── token_registry.py       # HashMap for token storage
│       └── rating_map.py           # HashMap for ratings
├── templates/
│   ├── dashboard.html              # Main dashboard
│   ├── token.html                  # Token request page
│   ├── public_display.html         # Public queue display
│   ├── counter_control.html        # Staff counter controls
│   ├── sort_filter.html            # Sort and filter page
│   ├── ratings.html                # Feedback submission
│   ├── analytics.html              # Rating analytics
│   └── algorithm_docs.html         # Algorithm documentation
└── static/
    ├── css/
    │   └── style.css               # All styles
    └── js/
        ├── common.js               # Shared utilities
        ├── user.js                 # User-facing JavaScript
        └── staff.js                # Staff JavaScript
```

## 🗂️ Data Structures Used

### 1. Queue (FIFO - First In First Out)
- **Implementation:** `collections.deque`
- **File:** `services/data_structures/normal_queue.py`
- **Purpose:** Manages normal (non-priority) tokens in First-Come-First-Served order
- **Operations:**
  - `enqueue()` - O(1): Add token to the back of the queue
  - `dequeue()` - O(1): Remove token from the front of the queue
  - `peek()` - O(1): View the front token without removing it
  - `is_empty()` - O(1): Check if queue is empty
  - `size()` - O(1): Get number of tokens in queue

### 2. Priority Queue (Min-Heap)
- **Implementation:** `heapq` (Python's heap implementation)
- **File:** `services/data_structures/priority_heap.py`
- **Purpose:** Manages priority tokens where Emergency > Staff > Student
- **Operations:**
  - `push()` - O(log n): Insert token with priority level
  - `pop()` - O(log n): Remove and return highest priority token
  - `peek()` - O(1): View highest priority token without removing
- **Priority Levels:** 
  - Emergency: 1 (highest)
  - Staff: 2
  - Student: 3 (lowest)

### 3. Stack (LIFO - Last In First Out)
- **Implementation:** Python `list`
- **File:** `services/data_structures/skipped_stack.py`
- **Purpose:** Stores skipped tokens for recall functionality
- **Operations:**
  - `push()` - O(1): Add skipped token to top of stack
  - `pop()` - O(1): Remove and return most recently skipped token
  - `peek()` - O(1): View top token without removing
- **Use Case:** When a customer isn't ready when called, their token is pushed onto the stack and can be recalled later

### 4. HashMap (Dictionary)
- **Implementation:** Python `dict`
- **Files:** 
  - `services/data_structures/token_registry.py` - Token storage
  - `services/data_structures/rating_map.py` - Rating storage
- **Purpose:** Fast O(1) lookup for tokens and ratings
- **Operations:**
  - `insert()` - O(1) average: Add new entry
  - `lookup()` - O(1) average: Retrieve entry by key
  - `update()` - O(1) average: Modify existing entry
  - `delete()` - O(1) average: Remove entry
- **Use Cases:**
  - Token Registry: Quick token lookup by ID
  - Rating Map: Aggregate ratings by department

## 🧮 Algorithms Implemented

### 1. Merge Sort
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n)
- **File:** `services/algorithms.py`
- **Purpose:** Sort queue views by various criteria (token ID, priority, time, department)
- **How it works:**
  1. Divide array into two halves
  2. Recursively sort each half
  3. Merge the sorted halves back together
- **Why Merge Sort:** Stable sorting algorithm with guaranteed O(n log n) performance

### 2. Waiting Time Prediction
- **Time Complexity:** O(1)
- **File:** `services/algorithms.py`
- **Formula:** `waiting_time = (queue_position - 1) × average_service_time`
- **Purpose:** Provide estimated wait time for each token
- **Example:** If you're position 4 in queue and average service time is 5 minutes:
  - Waiting time = (4 - 1) × 5 = 15 minutes

### 3. Load Balancing Algorithm (Shortest Queue First)
- **Time Complexity:** O(n) where n = number of counters per department
- **File:** `services/algorithms.py`
- **Purpose:** Assign incoming tokens to the counter with the least load
- **How it works:**
  1. Get all counters for the department
  2. Count current queue length for each counter
  3. Assign token to counter with minimum queue length
- **Benefit:** Distributes load evenly across counters, reducing overall wait times

### 4. Skip & Recall Algorithm
- **Skip Operation:** O(1)
  - Remove current token from service
  - Push token onto skip stack
  - Mark token status as SKIPPED
- **Recall Operation:** O(log n)
  - Pop token from skip stack - O(1)
  - Reinsert into priority queue with high priority - O(log n)
  - Mark token status as WAITING
- **Purpose:** Handle customers who aren't ready when their turn comes

### 5. Rating Analytics Algorithm
- **Average Calculation:** O(n) where n = number of ratings
- **Distribution Calculation:** O(n)
- **Sorting by Average:** O(d log d) where d = number of departments
- **File:** `services/algorithms.py` and `services/data_structures/rating_map.py`
- **Purpose:** Aggregate and analyze service ratings
- **Metrics Calculated:**
  - Average rating per department
  - Total rating count
  - Rating distribution (1-5 stars)
  - Sorted ranking of departments

### 6. Filter Algorithm
- **Time Complexity:** O(n) where n = number of tokens
- **File:** `services/algorithms.py`
- **Purpose:** Filter tokens based on multiple criteria
- **Supported Filters:**
  - Department (Finance, Library, Administration)
  - User Type (Student, Staff, Emergency)
  - Status (WAITING, SERVING, SERVED, SKIPPED)
  - Counter assignment

## 🎯 Features

### User Features
- **Token Request:** Submit name, type, and department to get a queue token
- **Queue Status:** View live status of all counters and estimated wait times
- **Feedback System:** Rate service and provide feedback after completion

### Staff Features
- **Counter Control:** Serve next token, skip, complete service, and recall skipped tokens
- **Dashboard:** Real-time statistics and recent activity
- **Sort & Filter:** View and sort queue by multiple criteria
- **Analytics:** View department ratings and performance metrics

### System Features
- **Auto-refresh:** Public display updates every 3 seconds
- **Priority Handling:** Emergency tokens get highest priority
- **Load Balancing:** Tokens automatically assigned to least-loaded counter
- **Real-time Updates:** All pages show live data from in-memory structures

## 🔍 Why No Database?

This project intentionally does NOT use a database to:

1. **Demonstrate Data Structures:** Shows how fundamental data structures work in a real application
2. **Educational Purpose:** Makes it easy to see and understand queue operations, priority handling, and algorithms
3. **Simplicity:** Reduces complexity and dependencies for learning purposes
4. **Real-time Performance:** All operations happen in-memory with O(1) or O(log n) complexity

In a production system, you would add:
- Database for persistence (PostgreSQL, MySQL)
- Redis for caching and real-time updates
- Authentication and authorization
- WebSocket for live updates

## 📊 API Endpoints

### User Endpoints
- `POST /api/token/request` - Request a new token
- `GET /api/queue/status` - Get current queue status
- `GET /api/token/<token_id>` - Get specific token information
- `POST /api/rating` - Submit rating and feedback
- `GET /api/analytics` - Get rating analytics

### Staff Endpoints
- `POST /api/staff/serve` - Serve next token at a counter
- `POST /api/staff/complete` - Complete current service
- `POST /api/staff/skip` - Skip current token
- `POST /api/staff/recall` - Recall a skipped token
- `GET /api/staff/counter/<counter>` - Get counter status
- `GET /api/staff/queue/sorted` - Get sorted and filtered queue view
- `GET /api/staff/skipped/<department>` - Get skipped tokens for department

### Dashboard Endpoints
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/activity` - Get recent activity

## 🧪 Testing the System

### Test Scenario 1: Basic Token Flow
1. Go to Token Request page
2. Submit a request (Student, Finance)
3. Note your token number
4. Go to Public Display - see your token in the queue
5. Go to Counter Control
6. Select Finance-1 counter
7. Click "Serve Next" - your token should be called
8. Click "Complete Service"
9. Submit feedback on the Feedback page

### Test Scenario 2: Priority Queue
1. Request 3 tokens in order:
   - Student (John)
   - Emergency (Jane)
   - Staff (Bob)
2. Go to Counter Control
3. Click "Serve Next"
4. Notice that Emergency (Jane) is served first, despite arriving second
5. Next click serves Staff (Bob)
6. Finally Student (John) is served

### Test Scenario 3: Skip and Recall
1. Serve a token
2. Click "Skip Token"
3. Serve next token
4. Click "Recall Skipped"
5. The skipped token returns to queue with high priority

### Test Scenario 4: Load Balancing
1. Request multiple tokens for the same department
2. Notice they are distributed across Finance-1 and Finance-2 automatically
3. Check Sort & Filter page to see distribution

## 👨‍🏫 Learning Outcomes

After completing this project, you will understand:

1. **Data Structures in Practice:**
   - How queues handle FIFO operations
   - How priority queues efficiently manage priorities
   - How stacks enable undo/recall functionality
   - How hashmaps provide fast lookups

2. **Algorithm Design:**
   - Implementing merge sort from scratch
   - Designing prediction algorithms
   - Creating load balancing strategies
   - Building analytics systems

3. **System Architecture:**
   - MVC/layered architecture
   - API design principles
   - Frontend-backend communication
   - Real-time updates

4. **Time Complexity:**
   - Understanding Big O notation
   - Analyzing algorithm efficiency
   - Choosing appropriate data structures

## 🛠️ Technology Stack

- **Backend:** Flask (Python 3.8+)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Data Storage:** In-memory Python data structures
- **Architecture:** MVC pattern with RESTful APIs

## 📝 Notes

- All data is stored in memory and will be lost on server restart
- No authentication system (for simplicity)
- No persistent storage (by design)
- Auto-refresh intervals can be adjusted in JavaScript files
- Suitable for educational purposes and coursework demonstration

## 🙏 Credits

Created for Programming Data Structures and Algorithms coursework.
Demonstrates practical implementation of fundamental CS concepts.
