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
import Link from "next/link"; // Ensure Link is imported
import styles from "./styles.module.css";
import { BASE_API_URL } from "../../services/Common";

const Login = () => {
  // State variables for login
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  // Form validation: ensure both fields are filled
  const isFormValid = () => {
    return username.trim() !== "" && password.trim() !== "";
  };

  // Handle form submission for login
  const handleSubmit = async (event) => {
    event.preventDefault();

    const endpoint = "/auth/login";

    // Prepare form data
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
      // Make a POST request to the login endpoint
      const response = await fetch(`${BASE_API_URL}${endpoint}`, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Login successful:", data);

        // Save userId to local storage
        localStorage.setItem("userId", data.user_id);
        localStorage.setItem("username", data.username);
        localStorage.setItem("name", data.first_name);

        // Navigate to the main pantry page
        router.push("/preppal");
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
        <h2 className={styles.title}>Log In</h2>
        <form className={styles.form} onSubmit={handleSubmit}>
          {/* Username Input Field */}
          <div>
            <input
              type="text"
              name="username"
              placeholder="Username"
              className={styles.inputField}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          {/* Password Input Field */}
          <div>
            <input
              type="password"
              name="password"
              placeholder="Password"
              className={styles.inputField}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className={`${styles.submitButton} ${
              isFormValid() ? styles.activeButton : styles.inactiveButton
            }`}
            disabled={!isFormValid()} // Disable button if form is invalid
          >
            Log In
          </button>
        </form>

        {/* Redirect Link to Signup Page */}
        <p className={styles.footerText}>
          Don't have an account?{" "}
          <Link href="/signup" className={styles.toggleLink}>
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
