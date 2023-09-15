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
   
Note: Replace the empty string with your desired secret key.

5. Create a `.env` file in the root directory of the project and add the following environment variables:

    ```
    DJANGO_SECRET_KEY=<your-secret-key>
    ```

Note: Replace `<your-secret-key>` with your desired secret key.

## Environment Variables

 You can set up environment variables in the `.env` file to configure the application. For example, the `DJANGO_SECRET_KEY` variable can be set to your desired secret key.

The project uses environment variables to store sensitive information. Follow the steps below to set up your environment:


1. Create a file named `.env` in the root directory of the project.

2. Copy the contents from `.env.sample` into `.env`.

3. Replace the values in `.env` with your actual environment variable values.

**Note:** Make sure not to commit your `.env` file to version control. It should be listed in the `.gitignore` file.

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