'use client';

import React, { useState } from 'react';
import styles from './Pantry.module.css';

const Pantry = () => {
  const [ingredients, setIngredients] = useState([]);
  const [newIngredients, setNewIngredients] = useState('');

  const handleQuantityChange = (index, delta) => {
    setIngredients((prev) => {
      const updatedIngredients = prev.map((ing, i) =>
        i === index ? { ...ing, quantity: ing.quantity + delta } : ing
      );
      return updatedIngredients.filter((ing) => ing.quantity > 0);
    });
  };

  const handleSubmit = () => {
    const parsed = newIngredients.split(',').map((item) => {
      const [name, quantity] = item.trim().split(' ');
      return { name, quantity: parseInt(quantity) || 0 };
    });
    setIngredients((prev) => [...prev, ...parsed]);
    setNewIngredients('');
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>PrepPal</h1>
        <div className={styles.userInfo}>
          <span>Welcome, John Doe</span>
          <div className={styles.avatar}>👤</div>
        </div>
      </header>

      <nav className={styles.nav}>
        <ul>
          <li><a href="#">My Pantry</a></li>
          <li><a href="recipe.html">Recipes</a></li>
        </ul>
      </nav>

      <main className={styles.main}>
        <h2 className={styles.mainHeading}>Your Pantry</h2>

        <div className={styles.grid}>
          <div className={styles.ingredientList}>
            {ingredients.length === 0 ? (
              <p className={styles.emptyMessage}>Your pantry is empty. Time to stock up!</p>
            ) : (
              ingredients.map((ing, index) => (
                <div key={index} className={styles.ingredientItem}>
                  <span className={styles.ingredientName}>{ing.name}</span>
                  <div className={styles.quantityControls}>
                    <button
                      onClick={() => handleQuantityChange(index, -1)}
                      className={styles.quantityBtn}
                    >
                      -
                    </button>
                    <span className={styles.quantity}>{ing.quantity}</span>
                    <button
                      onClick={() => handleQuantityChange(index, 1)}
                      className={styles.quantityBtn}
                    >
                      +
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className={styles.ingredientInput}>
            <textarea
              value={newIngredients}
              onChange={(e) => setNewIngredients(e.target.value)}
              placeholder="Enter ingredients in comma-separated format (ex: apple 3, onion 2)"
              className={styles.textarea}
            ></textarea>
            <button onClick={handleSubmit} className={styles.submitBtn}>
              Submit
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Pantry;
