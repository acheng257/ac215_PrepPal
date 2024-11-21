import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";


/** @type {import('eslint').Linter.Config[]} */
export default [{
    files: ["**/*.{js,mjs,cjs,jsx}"],
    languageOptions: {
      globals: globals.browser
    },
    settings: {
      react: {
        version: "detect",
      }
    },
    ...pluginJs.configs.recommended,
    ...pluginReact.configs.flat.recommended,
    rules: {
      "react/prop-types": "off", // Disable prop-types rule
      "react/react-in-jsx-scope": "off", // Disable React-in-scope rule for JSX
    },
  }];
