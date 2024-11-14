'use client';

import React, { useState } from 'react';
import styles from './styles.module.css';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import Link from 'next/link';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await fetch('http://localhost:9000/login', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Response from backend:', data);
        router.push('/preppal');
      } else {
        console.error('Failed to log in');
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    }
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
          <Link href="/signup" className={styles.loginLink}>Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;


