import React from 'react';
import styles from './styles.module.css';

const Recipe = () => {
  return (
    <div className={styles.appContainer}>
      {/* Hero Section */}
      <section className={styles.hero}>
          <div className={styles.heroContent}>
              <h1>Recipe Name</h1>
          </div>
      </section>

      <main className={styles.mainContent}>
        <div className={styles.recipeCard}>
          <div className={styles.recipeGrid}>
            <div className={styles.leftColumn}>
              <h2 className={styles.recipeName}>Sample Recipe</h2>
              <div className={styles.recipeDetails}>
                <div>
                  <h3 className={styles.sectionTitle}>Serving Size</h3>
                  <p className={styles.text}>4 servings</p>
                </div>
                <div>
                  <h3 className={styles.sectionTitle}>Total Time</h3>
                  <p className={styles.text}>45 minutes</p>
                </div>
                <div>
                  <h3 className={styles.sectionTitle}>Ingredients</h3>
                  <ul className={styles.ingredientsList}>
                    <li>2 cups flour</li>
                    <li>1 cup sugar</li>
                    <li>3 eggs</li>
                  </ul>
                </div>
              </div>
            </div>
            <div className={styles.rightColumn}>
              <div className={styles.nutritionCard}>
                <h3 className={styles.sectionTitle}>Nutrition Facts</h3>
                <div className={styles.nutritionDetails}>
                  <p className={styles.text}>Calories: 350</p>
                  <p className={styles.text}>Sugar: 15g</p>
                  <p className={styles.text}>Protein: 8g</p>
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
