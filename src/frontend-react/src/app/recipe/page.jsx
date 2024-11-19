'use client';

import React from 'react';
import { useSearchParams } from 'next/navigation';
import styles from './styles.module.css';

const Recipe = () => {
  const searchParams = useSearchParams();

  // Extract parameters from URL search params
  const name = searchParams.get('name') || 'Recipe Name';
  const cookingTime = searchParams.get('cookingTime') || '45 minutes';
  const calories = searchParams.get('calories') || '350';
  const ingredients = JSON.parse(searchParams.get('ingredients') || '[]'); // Parse back to array
  const [user, setUser] = useState(DataService.GetUser());

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
                  1. Mix ingredients<br />
                  2. Bake at 350°F<br />
                  3. Let cool
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
