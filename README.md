# Fitness_app

Fitness_app is an all-in-one Python application designed to help anyone on their fitness journey. Whether you're just starting out or looking to optimize your workout routine, this app provides tools to track your weight, build customized workout plans, and guide you through your exercises.

## Features

- **Weight Tracking**: Log and monitor your progress over time.
- **Workout Planner**: Create and manage personalized workout plans.
- **Guided Workouts**: View, perform, and advance through your scheduled exercises.
- **Throttling Constraints**: API rate limits ensure fair use and optimal performance.
- **JWT Authentication**: Secure access and user management using JSON Web Tokens.
- **Interactive API Documentation**: Explore and test endpoints via Swagger UI.

## Getting Started

### Prerequisites

- Python 3.13.7
- All required libraries are listed in [`requirements.txt`](requirements.txt).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sasori2134/Fitness_app.git
   cd Fitness_app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

run migrations in the project folder:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

start the api:
```bash
python manage.py runserver
```

NOTE!!!: You have to specify your goal_weight when you register

### Accessing the API Docs

After starting the app, access the Swagger UI at:

```
api/swagger/
```

This interactive documentation makes it easy to explore and test all available endpoints.

## Usage

- Register and log in to securely access your data (JWT authentication required).
- Begin tracking your weight and planning workouts.
- Use the API documentation at `api/swagger/` to experiment with features and endpoints.

## Contributing

Contributions are welcome! Please submit issues or pull requests for improvements and new features.
