'use client';

import React, { useState } from 'react';
import styles from './styles.module.css';
import Header from '@/components/layout/Header';

const PrepPal = () => {
  const [filters, setFilters] = useState({
    cookingTime: 30,
    servings: 4,
    cuisine: 'all',
    ingredients: []
  });

  const recipes = [
    {
      name: 'Pasta Primavera',
      cookingTime: '25 mins',
      ingredients: ['pasta', 'vegetables', 'olive oil'],
      calories: 320
    },
    {
      name: 'Grilled Salmon',
      cookingTime: '20 mins',
      ingredients: ['salmon', 'lemon', 'herbs'],
      calories: 420
    },
    {
      name: 'Chicken Stir-Fry',
      cookingTime: '15 mins',
      ingredients: ['chicken', 'vegetables', 'soy sauce'],
      calories: 500
    },
    {
      name: 'Quinoa Bowl',
      cookingTime: '30 mins',
      ingredients: ['quinoa', 'avocado', 'chickpeas'],
      calories: 400
    }
  ];

  return (
    <div className={styles.appContainer}>
      <Header />

      <main className={styles.mainContent}>
        <div className={styles.gridContainer}>
          <div className={styles.filtersSection}>
            <h2>Filters</h2>
            <div className={styles.filterGroup}>
              <label>Cooking Time</label>
              <input
                type="range"
                min="0"
                max="120"
                value={filters.cookingTime}
                onChange={(e) => setFilters({ ...filters, cookingTime: Number(e.target.value) })}
              />
              <span>{filters.cookingTime} minutes</span>
            </div>
            <div className={styles.filterGroup}>
              <label>Servings</label>
              <input
                type="range"
                min="1"
                max="12"
                value={filters.servings}
                onChange={(e) => setFilters({ ...filters, servings: Number(e.target.value) })}
              />
              <span>{filters.servings} servings</span>
            </div>
            <div className={styles.filterGroup}>
              <label>Cuisine</label>
              <select
                value={filters.cuisine}
                onChange={(e) => setFilters({ ...filters, cuisine: e.target.value })}
              >
                <option value="all">All Cuisines</option>
                <option value="italian">Italian</option>
                <option value="asian">Asian</option>
                <option value="mexican">Mexican</option>
              </select>
            </div>
            <div className={styles.filterGroup}>
              <label>Ingredients</label>
              <input
                type="text"
                placeholder="Enter ingredients separated by commas"
                value={filters.ingredients}
                onChange={(e) => setFilters({
                  ...filters,
                  ingredients: e.target.value.split(',').map(ingredient => ingredient.trim())
                })}
              />
              <span>Ingredients: {filters.ingredients.join(', ')}</span>
            </div>
            <button>Submit</button>
          </div>

          <div className={styles.recipeGrid}>
            {recipes.map((recipe, index) => (
              <div key={index} className={styles.recipeCard}>
                <div className={styles.recipeDetails}>
                  <h3>{recipe.name}</h3>
                  <p>Cooking time: {recipe.cookingTime}</p>
                  <h4>Ingredients:</h4>
                  <ul>
                    {recipe.ingredients.map((ingredient, idx) => (
                      <li key={idx}>• {ingredient}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.chatbotSection}>
          <div className={styles.chatHistory}>Chat history will appear here...</div>
          <div className={styles.chatInput}>
            <input type="text" placeholder="Ask about recipes or cooking tips..." />
            <button>Send</button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PrepPal;
