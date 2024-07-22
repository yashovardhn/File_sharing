# File Sharing Project

## Overview

The File Sharing Project is a Django-based web application that allows users to upload, manage, and download files. It includes user authentication, email verification, and file handling features.

## Features

- User authentication with email verification
- File upload and download functionality
- API endpoints for file management
- Secure file access and permissions

## Installation

### Prerequisites

- Python 3.x
- Django
- Django REST framework

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yashovardhn/File_sharing.git
    cd File_sharing
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## Usage

1. **Signup:**
   - Navigate to `/signup/` to create a new account. An email verification link will be sent to your email.

2. **Verify Email:**
   - Click the verification link sent to your email to activate your account.

3. **Upload Files:**
   - Use the `/api/files/` endpoint to upload files (supported types: pptx, docx, xlsx).

4. **Download Files:**
   - Access the `/api/files/<file_id>/download/` endpoint to download files you have uploaded.

## API Endpoints

- **File List and Create:** `GET /api/files/` | `POST /api/files/`
- **File Retrieve, Update, and Delete:** `GET /api/files/<file_id>/` | `PUT /api/files/<file_id>/` | `DELETE /api/files/<file_id>/`

## Configuration

- **Email Settings:** Configure email settings in `settings.py` for account verification emails.

## Contributing

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit your changes and push to your fork.
4. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [your-email@example.com](mailto:your-email@example.com).
