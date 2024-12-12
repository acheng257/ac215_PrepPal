DROP TABLE IF EXISTS recipes CASCADE;
DROP TABLE IF EXISTS pantry CASCADE;
DROP TABLE IF EXISTS user_history CASCADE;
DROP TABLE IF EXISTS user_preferences CASCADE;
DROP TABLE IF EXISTS users CASCADE;
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(200) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. user_preferences table
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY,  -- Primary key and foreign key to users(user_id)
    recipe_history UUID[],
    allergies TEXT[],
    favorite_cuisines TEXT[],
    favorite_recipes UUID[],
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),  -- Timestamp of the last preference update
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE  -- Foreign key to users table
);

CREATE TABLE user_history (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    details JSONB,                     -- Stores additional details in JSON format
    recommendation_id UUID,
    recommendation_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pantry (
    user_id UUID PRIMARY KEY,
    items JSONB NOT NULL DEFAULT '{}'::JSONB,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE recipes (
    recipe_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(100) UNIQUE NOT NULL,
    instructions TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    cooking_time INT NOT NULL,  -- in minutes
    calories INT NOT NULL,
    protein INT NOT NULL,       -- in grams
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- Indexes
CREATE INDEX idx_users_phone_number ON users(user_id);
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
