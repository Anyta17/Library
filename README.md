# Library API

The project allows users to borrow books


## Setup Instructions

To set up the project locally, follow these steps:

1. Clone the repository:

    ```
    git clone https://github.com/Anyta17/Library.git
    ```

2. Navigate to the project directory:

    ```
    cd library
    ```

3. Create a virtual environment and activate it:

    ```
    python -m venv venv
    venv\Scripts\activate
    ```

4. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

6. Apply the database migrations:

    ```
    python manage.py migrate
    ```

**Note on Database:** Ensure that you have removed the actual database file from the repository, as it should not be stored in version control. Running the migrations will create a new database file.

7. Start the development server:

  ```
  python manage.py runserver
  ```

## API Endpoints

The API provides the following endpoints:

* `/books/`: List and create books.
* `/books/<int:pk>/`: Retrieve, update, and delete individual books.
* `/borrowings/`: List and create borrowings.
* `/borrowings/<int:pk>/`: Retrieve, update, and delete individual borrowings.
