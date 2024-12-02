'use client';

import { React, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import styles from './styles.module.css';
import DataService from '@/services/DataService';

const apiUrl = "http://localhost:9000/pantry";

const Recipe = () => {
  const searchParams = useSearchParams();

  const name = searchParams.get('name') || 'Recipe Name';
  const cookingTime = searchParams.get('cookingTime') || '45 minutes';
  const calories = searchParams.get('calories') || '350';
  const ingredients = JSON.parse(searchParams.get('ingredients') || '[]');
  const instructions = JSON.parse(searchParams.get('instructions') || '[]');
  const [user, setUser] = useState(DataService.GetUser());

  const handleUseRecipe = async () => {
    try {
      const userId = user;
      if (!userId) {
        alert('User not logged in');
        return;
      }

      const response = await fetch(`${apiUrl}/${userId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch pantry');
      }
      const pantryData = await response.json();
      let pantry = pantryData.items || {};

      console.log("Pantry is", pantry);

      const parseIngredient = (ingredientStr) => {
        const parts = ingredientStr.trim().split(' ');
        const quantity = parseFloat(parts[0]);
        const ingredientName = parts.slice(1).join(' ').toLowerCase();
        return { quantity, ingredientName };
      };

      // Remove ingredients used in the recipe from the pantry
      ingredients.forEach(ingredientStr => {
        const { quantity: recipeQuantity, ingredientName } = parseIngredient(ingredientStr);

        if (pantry.hasOwnProperty(ingredientName)) {
          const pantryQuantity = pantry[ingredientName];

          const updatedQuantity = pantryQuantity - recipeQuantity;
          console.log("quantities are", pantryQuantity, recipeQuantity)

          if (updatedQuantity <= 0) {
            delete pantry[ingredientName];
          } else {
            pantry[ingredientName] = updatedQuantity;
          }
        } else {
          console.warn(`Ingredient "${ingredientName}" not found in pantry.`);
        }
      });

      console.log("updated pantry is", JSON.stringify(pantry))
      const updateResponse = await fetch(`${apiUrl}/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ items: pantry }),
      });

      if (!updateResponse.ok) {
        throw new Error('Failed to update pantry');
      }

      alert('Pantry updated successfully');
    } catch (error) {
      console.error(error);
      alert('An error occurred while updating the pantry');
    }
  };


  return (
    <div className={styles.appContainer}>
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1>{name}</h1>
        </div>
      </section>

      <main className={styles.mainContent}>
        <div className={styles.recipeCard}>
          <div className={styles.recipeGrid}>
            <div className={styles.leftColumn}>
              <h2 className={styles.recipeName}>{name}</h2>
              <div className={styles.recipeDetails}>
                <div>
                  <h3 className={styles.sectionTitle}>Total Time</h3>
                  <p className={styles.text}>{cookingTime}</p>
                </div>
                <div>
                  <h3 className={styles.sectionTitle}>Ingredients</h3>
                  <ul className={styles.ingredientsList}>
                    {ingredients.length > 0 ? (
                      ingredients.map((ingredient, idx) => (
                        <li key={idx}>{ingredient}</li>
                      ))
                    ) : (
                      <>
                        <li>2 cups flour</li>
                        <li>1 cup sugar</li>
                        <li>3 eggs</li>
                      </>
                    )}
                  </ul>
                  <button onClick={handleUseRecipe}>Use this recipe</button>
                </div>
              </div>
            </div>
            <div className={styles.rightColumn}>
              <div className={styles.nutritionCard}>
                <h3 className={styles.sectionTitle}>Nutrition Facts</h3>
                <div className={styles.nutritionDetails}>
                  <p className={styles.text}>Calories: {calories}</p>
                </div>
              </div>
              <div className={styles.instructionsCard}>
                <h3 className={styles.sectionTitle}>Instructions</h3>
                <div className={styles.instructionsText}>
                  <ol>
                    {instructions.length > 0 ? (
                      instructions.map((step, idx) => (
                        <li key={idx}>{step}</li>
                      ))
                    ) : (
                      <li>No instructions provided.</li>
                    )}
                  </ol>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Recipe;
