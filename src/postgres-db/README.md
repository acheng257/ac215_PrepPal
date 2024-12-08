# PrepPal Database Schema

This repository contains the database schema and setup files for the PrepPal application. The schema is designed to store user information, user preferences, recipes, and session history.

## Tables

### 1. `users` Table

Stores core user identity and registration information.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `user_id` | UUID | PRIMARY KEY | Unique identifier for each user |
| `first_name` | VARCHAR(50) | NOT NULL | User's first name |
| `last_name` | VARCHAR(50) | NOT NULL | User's last name |
| `username` | VARCHAR(50) | NOT NULL | User's username |
| `password` | VARCHAR(200) | NOT NULL | User's password |
| `phone_number` | VARCHAR(20) | UNIQUE, NOT NULL | User's phone number |
| `registration_date` | TIMESTAMP WITH TZ | DEFAULT NOW() | Date and time when the user registered |
| `last_updated` | TIMESTAMP WITH TZ | DEFAULT NOW() | Timestamp of the last update to the user's record |

### 2. `user_preferences` Table

Contains user-specific training preferences and attributes.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `user_id` | UUID | PRIMARY KEY | Identifier of the user (references `users` table) |
| `recipe_history` | UUID[] | PRIMARY KEY | Unique identifier for each user |
| `allergies` | TEXT[] |  | List of any allergies for the user |
| `favorite_cuisines` | TEXT[] |  | List of user's favorite cuisines |
| `favorite_recipes` | UUID[] |  | List of IDs corresponding to user's favorite recipes |
| `last_updated` | TIMESTAMP | DEFAULT NOW() | Timestamp of the last update to user preferences |

### 3. `user_history` Table

Contains personalized training plans for each user.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique identifier for session history of different users |
| `user_id` | UUID | NOT NULL | Unique identifier of the user |
| `details` | JSONB | | JSON containing details of session history |
| `recommendation_id` | UUID | | Identifier of the recommendation data |
| `recommendation_data` | JSONB | | Last recommended recipes to the user |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp of the last user history creation |

### 4. `pantry` Table

Contains details for each training session within a plan.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `user_id` | UUID | PRIMARY KEY | Unique identifier for each user |
| `items` | JSONB | NOT NULL | Items contained in user's pantry |
| `last_updated` | TIMESTAMP | DEFAULT NOW() | Timestamp of last pantry update |

### 5. `recipes` Table

Stores detailed performance metrics for completed sessions.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `recipe_id` | UUID | PRIMARY KEY | Unique identifier for each recipe |
| `title` | VARCHAR(100) | NOT NULL | Title of recipe dish |
| `instructions` | TEXT | NOT NULL | Instructions for the recipe |
| `ingredients` | TEXT | NOT NULL | Ingredients required for recipe |
| `cooking_time` | INT | NOT NULL | Total time required for recipe in minutes |
| `calories` | INT | NOT NULL | Calories in recipe |
| `protein` | INT | NOT NULL | Protein in recipe |
| `user_id` | UUID | NOT NULL | Unique identifier of user who favorited the recipe |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Timestamp of when the recipe was added |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Timestamp of when the recipe was updated |

## Indexes

The schema includes the following indexes to optimize query performance:

- `idx_users_id` on `users(phone_number)`
- `idx_user_preferences_user_id` on `user_preferences(user_id)`

## **Instructions to Run Locally**
To run the database locally, you can follow the instructions below.

1. **Clone the Repository**

   ```bash
   git clone https://github.com/acheng257/ac215_PrepPal
   cd ac215_PrepPal/src/postgres-db
   ```

2. **Run the Setup Script**

   ```bash
   ./setup.sh
   ```

   This script will remove any existing Docker containers and images named `preppal_db`, build the new image, and run the container.

3. **Verify the Setup**

   - Check if the container is running:

     ```bash
     docker ps
     ```

   - You should see `preppal_db` in the list of running containers.

4. **Connect to the Database**

   - Use a PostgreSQL client or `psql` to connect:

     ```bash
     psql -h localhost -p 5432 -U postgres -d preppal_db
     ```

     Enter the password `postgres` when prompted.

     or

   - Connect through the container:

   ```bash
   docker exec -it container_id psql -U postgres -d preppal_db
   ```

5. **Inspect the Tables**

   - Once connected, list the tables:

     ```sql
     \dt
     ```

   - You should see the tables listed above.

---

## Notes

- **Database Credentials**:

  - **Username**: `postgres`
  - **Password**: `postgres`
  - **Database**: `running_coach_db`
