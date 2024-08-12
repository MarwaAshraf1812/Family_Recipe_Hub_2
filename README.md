# Family Recipe Hub

Welcome to the Family Recipe Hub! This project is a comprehensive web application designed to manage and share family recipes, community posts, and user profiles. Built with Django and Django REST Framework, the application provides a robust platform for users to engage with recipes, post comments, and maintain profiles.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Family Recipe Hub is designed to bring family members together by allowing them to:

- Share and manage family recipes.
- Post and interact with community posts.
- Manage personal profiles and preferences.
- Receive notifications for new comments on their posts.

## Features

- **User Authentication**: Register, log in, and manage user accounts.
- **Recipe Management**: Create, update, and delete recipes with ingredients and instructions.
- **Category and Subcategory Management**: Organize recipes into categories and subcategories.
- **Community Posts**: Create posts, participate in conversations, and comment on posts.
- **User Profiles**: Manage user profiles and view other users’ profiles.
- **Notifications**: Receive notifications when new comments are added to posts.

## Technologies Used

- **Django**: A high-level Python web framework for rapid development.
- **Django REST Framework**: A powerful toolkit for building Web APIs.
- **PostgreSQL/MySQL/SQLite**: Database systems (configured in `settings.py`).
- **Bootstrap**: For responsive and modern UI design.
- **Heroku/AWS**: For deployment (optional).

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Pip (Python package installer)
- Virtualenv (recommended)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MarwaAshraf1812/FamilyRecipeHub.git
   cd FamilyRecipeHub
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create Superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.
