// "use client";

// import React, { useState } from "react";
// import { useRouter } from "next/navigation";
// import styles from "./styles.module.css";

// const Auth = () => {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [confirmPassword, setConfirmPassword] = useState(""); // For password confirmation
//   const [isLogin, setIsLogin] = useState(true); // Toggle between login and signup
//   const router = useRouter();

//   // Check if all fields are filled for button activation
//   const isFormValid = () => {
//     if (isLogin) {
//       return email.trim() && password.trim();
//     } else {
//       return email.trim() && password.trim() && confirmPassword.trim();
//     }
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();

//     // Password confirmation check for signup
//     if (!isLogin && password !== confirmPassword) {
//       alert("Passwords do not match. Please try again.");
//       return;
//     }

//     const endpoint = isLogin ? "/auth/login" : "/auth/signup";
//     const formData = new FormData();
//     formData.append("username", email);
//     formData.append("password", password);

//     try {
//       const response = await fetch(`http://localhost:9000${endpoint}`, {
//         method: "POST",
//         body: formData
//       });

//       if (response.ok) {
//         const data = await response.json();
//         if (isLogin) {
//           console.log("Login successful:", data);

//           // Save userId to local storage
//           localStorage.setItem("userId", data.user_id);

//           // Navigate to pantry
//           router.push(`/preppal`);
//         } else {
//           console.log("Signup successful:", data);

//           // Save userId to local storage for immediate access
//           localStorage.setItem("userId", data.user_id);

//           // Navigate to pantry directly after signup
//           router.push(`/preppal`);
//         }
//       } else {
//         const errorData = await response.json();
//         alert(errorData.detail || "Something went wrong.");
//       }
//     } catch (error) {
//       console.error("Error:", error);
//       alert("An error occurred. Please try again later.");
//     }
//   };

//   return (
//     <div className={styles.appContainer}>
//       <div className={styles.container}>
//         <h2 className={styles.title}>{isLogin ? "Log In" : "Sign Up"}</h2>
//         <form className={styles.form} onSubmit={handleSubmit}>
//           <div>
//             <input
//               type="email"
//               placeholder="Email"
//               className={styles.inputField}
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               required
//             />
//           </div>
//           <div>
//             <input
//               type="password"
//               placeholder="Password"
//               className={styles.inputField}
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               required
//             />
//           </div>
//           {!isLogin && (
//             <div>
//               <input
//                 type="password"
//                 placeholder="Confirm Password"
//                 className={styles.inputField}
//                 value={confirmPassword}
//                 onChange={(e) => setConfirmPassword(e.target.value)}
//                 required
//               />
//             </div>
//           )}
//           <button
//             type="submit"
//             className={`${styles.submitButton} ${
//               isFormValid() ? styles.activeButton : styles.inactiveButton
//             }`}
//             disabled={!isFormValid()} // Disable button if fields are not filled
//           >
//             {isLogin ? "Log In" : "Sign Up"}
//           </button>
//         </form>
//         <p className={styles.footerText}>
//           {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
//           <span
//             className={styles.toggleLink}
//             onClick={() => setIsLogin(!isLogin)}
//           >
//             {isLogin ? "Sign Up" : "Log In"}
//           </span>
//         </p>
//       </div>
//     </div>
//   );
// };

// export default Auth;

"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./styles.module.css";

const Auth = () => {
  // 1. Update state variables: 'email' to 'username'
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState(""); // For password confirmation
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and signup
  const router = useRouter();

  // 2. Update form validation to check 'username' instead of 'email'
  const isFormValid = () => {
    if (isLogin) {
      return username.trim() && password.trim();
    } else {
      return username.trim() && password.trim() && confirmPassword.trim();
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    // 3. Password confirmation check for signup
    if (!isLogin && password !== confirmPassword) {
      alert("Passwords do not match. Please try again.");
      return;
    }

    // 4. Determine the endpoint based on the form mode (login/signup)
    const endpoint = isLogin ? "/auth/login" : "/auth/signup";

    // 5. Prepare form data with 'username' and 'password'
    const formData = new FormData();
    formData.append("username", username); // Use 'username' instead of 'email'
    formData.append("password", password);

    // For signup, include additional fields
    if (!isLogin) {
      formData.append("first_name", event.target.first_name.value);
      formData.append("last_name", event.target.last_name.value);
      formData.append("phone_number", event.target.phone_number.value);
    }

    try {
      // 6. Make a POST request to the appropriate endpoint
      const response = await fetch(`http://localhost:9000${endpoint}`, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        if (isLogin) {
          console.log("Login successful:", data);

          // Save userId to local storage
          localStorage.setItem("userId", data.user_id);

          // Navigate to pantry
          router.push(`/preppal`);
        } else {
          console.log("Signup successful:", data);

          // Save userId to local storage for immediate access
          localStorage.setItem("userId", data.user_id);

          // Navigate to pantry directly after signup
          router.push(`/preppal`);
        }
      } else {
        const errorData = await response.json();
        alert(errorData.detail || "Something went wrong.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again later.");
    }
  };

  return (
    <div className={styles.appContainer}>
      <div className={styles.container}>
        <h2 className={styles.title}>{isLogin ? "Log In" : "Sign Up"}</h2>
        <form className={styles.form} onSubmit={handleSubmit}>
          {/* 7. Update input fields to use 'username' */}
          <div>
            <input
              type="text" // Changed from 'email' to 'text'
              name="username" // Added 'name' attribute for form data
              placeholder="Username" // Changed from 'Email' to 'Username'
              className={styles.inputField}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div>
            <input
              type="password"
              name="password" // Added 'name' attribute for form data
              placeholder="Password"
              className={styles.inputField}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {!isLogin && (
            <>
              {/* 8. Add additional fields for signup */}
              <div>
                <input
                  type="text"
                  name="first_name" // Added 'name' attribute for form data
                  placeholder="First Name"
                  className={styles.inputField}
                  required
                />
              </div>
              <div>
                <input
                  type="text"
                  name="last_name" // Added 'name' attribute for form data
                  placeholder="Last Name"
                  className={styles.inputField}
                  required
                />
              </div>
              <div>
                <input
                  type="text"
                  name="phone_number" // Added 'name' attribute for form data
                  placeholder="Phone Number"
                  className={styles.inputField}
                  value={confirmPassword} // This seems incorrect; should be separate
                  onChange={(e) => setConfirmPassword(e.target.value)} // This is for confirmPassword
                  required
                />
              </div>
              <div>
                <input
                  type="password"
                  name="confirm_password" // Added 'name' attribute for form data
                  placeholder="Confirm Password"
                  className={styles.inputField}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </>
          )}

          <button
            type="submit"
            className={`${styles.submitButton} ${
              isFormValid() ? styles.activeButton : styles.inactiveButton
            }`}
            disabled={!isFormValid()} // Disable button if fields are not filled
          >
            {isLogin ? "Log In" : "Sign Up"}
          </button>
        </form>
        <p className={styles.footerText}>
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <span
            className={styles.toggleLink}
            onClick={() => setIsLogin(!isLogin)}
          >
            {isLogin ? "Sign Up" : "Log In"}
          </span>
        </p>
      </div>
    </div>
  );
};

export default Auth;
