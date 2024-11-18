'use client';

import React, { useState } from 'react';
import styles from './Signup.module.css';
import { useRouter } from 'next/navigation';
import { Link } from 'react-router-dom';
import Header from '@/components/layout/Header';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter()

  const handleSubmit = (event) => {
    event.preventDefault();

    // TODO: Add login logic, e.g., API request to validate user credentials
    alert("Form submitted successfully!");
    window.location.assign('index.html');
  };

  return (
    <div className={styles.appContainer}>
      <Header />

      <div className={styles.container}>
        <h2 className={styles.title}>Log In</h2>
        <form className={styles.form} onSubmit={handleSubmit}>
          <div>
            <input
              type="email"
              placeholder="Email"
              className={styles.inputField}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="Password"
              className={styles.inputField}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className={styles.submitButton}>Log In</button>
        </form>
        <p className={styles.footerText}>
          Don't have an account?{' '}
          {/* <a href="Signup.jsx" className={styles.loginLink}>Sign Up</a> */}
          <Link to="/signup">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
