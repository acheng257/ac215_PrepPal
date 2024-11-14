'use client';

import React, { useState } from 'react';
import styles from './styles.module.css';

const Pantry = () => {
  const [ingredients, setIngredients] = useState([]);
  const [newIngredients, setNewIngredients] = useState('');

  const updatePantry = async (add, subtract) => {
    const apiUrl = 'http://localhost:9000';
    try {
      const response = await fetch(`${apiUrl}/update_pantry`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ add, subtract }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.detail);
      } else {
        const data = await response.json();
        console.log(data.message);
      }
    } catch (error) {
      console.error('Error updating pantry:', error);
    }
  };

  const handleQuantityChange = (index, delta) => {
    setIngredients((prev) => {
      const updatedIngredients = prev.map((ing, i) =>
        i === index ? { ...ing, quantity: ing.quantity + delta } : ing
      ).filter((ing) => ing.quantity > 0);

      const ingredient = prev[index];
      const action = delta > 0 ? { [ingredient.name]: delta } : { [ingredient.name]: -delta };

      updatePantry(delta > 0 ? action : null, delta < 0 ? action : null);

      return updatedIngredients;
    });
  };

  const handleSubmit = () => {
    const parsed = newIngredients.split(',').map((item) => {
      const [name, quantity] = item.trim().split(' ');
      return { name, quantity: parseInt(quantity) || 0 };
    });

    setIngredients((prev) => [...prev, ...parsed]);
    setNewIngredients('');

    const addItems = parsed.reduce((acc, { name, quantity }) => {
      if (quantity > 0) acc[name] = quantity;
      return acc;
    }, {});

    updatePantry(addItems, null);
  };

  return (
    <div className={styles.container}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1>Your Pantry</h1>
          <p>Welcome to your pantry! Upload new ingredients or edit existing ones below.</p>
        </div>
      </section>

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
