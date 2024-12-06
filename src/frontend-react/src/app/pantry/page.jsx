"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./styles.module.css";
import DataService from "@/services/DataService";
import { BASE_API_URL } from "../../services/Common";

const Pantry = () => {
  const [ingredients, setIngredients] = useState([]);
  const [newIngredients, setNewIngredients] = useState("");
  // const [userId, setUserId] = useState(null); // Use state for userId
  const [userId, setUserId] = useState(DataService.GetUser());
  // const apiUrl = "http://localhost:9000/pantry";
  const apiUrl = `${BASE_API_URL}/pantry`;
  const router = useRouter();

  // Fetch userId from localStorage when the component mounts
  useEffect(() => {
    const storedUserId = localStorage.getItem("userId");
    if (!storedUserId) {
      alert("User not logged in. Redirecting to login page.");
      router.push("/login"); // Redirect to login if userId is missing
      return;
    }
    setUserId(storedUserId); // Set userId in state
  }, [router]);

  useEffect(() => {
    if (!userId) return;

    const fetchPantry = async () => {
      try {
        const response = await fetch(`${apiUrl}/${userId}`);
        if (!response.ok) {
          const errorData = await response.json();
          alert(errorData.detail);
          return;
        }
        const data = await response.json();
        if (data && data.items) {
          setIngredients(
            Object.entries(data.items).map(([name, quantity]) => ({
              name,
              quantity
            }))
          );
        } else {
          console.error('Unexpected response structure:', data);
          setIngredients([]);
        }
      } catch (error) {
        console.error("Error fetching pantry:", error);
      }
    };

    fetchPantry();
  }, [apiUrl, userId]);

  const updatePantry = async (updatedPantry) => {
    if (!userId) {
      alert("User ID is missing. Please log in again.");
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/${userId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ items: updatedPantry })
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.detail);
        return;
      }

      console.log("Pantry updated successfully");
    } catch (error) {
      console.error("Error updating pantry:", error);
    }
  };

  const deletePantryItem = async (itemName) => {
    if (!userId) {
      alert("User ID is missing. Please log in again.");
      return;
    }

    try {
      const updatedPantry = ingredients.reduce((acc, ing) => {
        if (ing.name !== itemName) acc[ing.name] = ing.quantity;
        return acc;
      }, {});

      await updatePantry(updatedPantry);

      setIngredients((prev) => prev.filter((ing) => ing.name !== itemName));
    } catch (error) {
      console.error("Error deleting pantry item:", error);
    }
  };

  const handleQuantityChange = (index, delta) => {
    setIngredients((prev) => {
      const updatedIngredients = prev
        .map((ing, i) =>
          i === index ? { ...ing, quantity: ing.quantity + delta } : ing
        )
        .filter((ing) => ing.quantity > 0);

      const updatedPantry = updatedIngredients.reduce(
        (acc, { name, quantity }) => {
          acc[name] = quantity;
          return acc;
        },
        {}
      );

      updatePantry(updatedPantry);

      return updatedIngredients;
    });
  };

  const handleSubmit = () => {
    if (!userId) {
      alert("User ID is missing. Please log in again.");
      return;
    }

    const parsed = newIngredients
    .split(",") // Split the string by commas to get individual ingredients
    .map((item) => {
      const trimmed = item.trim(); // Remove leading/trailing whitespace
      const lastSpaceIndex = trimmed.lastIndexOf(" "); // Find the last space in the string

      // If there's no space, the format is invalid (e.g., "salt")
      if (lastSpaceIndex === -1) {
        alert(`Invalid input: "${trimmed}". Use format: "apple 3, pear 2".`);
        return null;
      }

      // Extract the name and quantity based on the last space
      const name = trimmed.substring(0, lastSpaceIndex).trim();
      const quantityStr = trimmed.substring(lastSpaceIndex + 1).trim();

      // Parse the quantity to an integer
      const quantity = parseInt(quantityStr, 10);

      // Validate the parsed values
      if (!name || isNaN(quantity)) {
        alert(
          `Invalid input: "${trimmed}". Use format: "apple 3, pear 2".`
        );
        return null;
      }

      return { name, quantity };
    })
    .filter((item) => item !== null);

    if (parsed.length === 0) return;

    const newItems = parsed.reduce((acc, { name, quantity }) => {
      if (quantity > 0) acc[name] = quantity;
      return acc;
    }, {});

    updatePantry({
      ...ingredients.reduce((acc, ing) => {
        acc[ing.name] = ing.quantity;
        return acc;
      }, {}),
      ...newItems
    });

    setIngredients((prev) => [...prev, ...parsed]);
    setNewIngredients("");
  };

  return (
    <div className={styles.container}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1>Your Pantry</h1>
          <p>
            Welcome to your pantry! Upload new ingredients or edit existing ones
            below.
          </p>
        </div>
      </section>

      <main className={styles.main}>
        <h2 className={styles.mainHeading}>Your Pantry</h2>

        <div className={styles.grid}>
          <div className={styles.ingredientList}>
            {ingredients.length === 0 ? (
              <p className={styles.emptyMessage}>
                Your pantry is empty. Time to stock up!
              </p>
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
                  <button
                    onClick={() => deletePantryItem(ing.name)}
                    className={styles.deleteBtn}
                  >
                    Delete
                  </button>
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
