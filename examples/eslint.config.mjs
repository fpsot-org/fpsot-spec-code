// SPDX-License-Identifier: Apache-2.0
// Example for COD-603 and COD-010: ESLint 10 flat configuration with typescript-eslint 8.
import { defineConfig } from "eslint/config";
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import comments from "@eslint-community/eslint-plugin-eslint-comments/configs";
import prettier from "eslint-config-prettier/flat";

export default defineConfig([
  // COD-011: generated code and build output are excluded by path.
  { ignores: ["dist/", "target/", "src/generated/"] },
  js.configs.recommended,
  tseslint.configs.strictTypeChecked,
  tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
  // JavaScript files, such as this configuration, have no type information.
  {
    files: ["**/*.{js,mjs,cjs}"],
    ...tseslint.configs.disableTypeChecked,
  },
  comments.recommended,
  {
    rules: {
      // COD-010: each disable comment gives its reason after "--".
      "@eslint-community/eslint-comments/require-description": "error",
      "@eslint-community/eslint-comments/no-unlimited-disable": "error",
    },
  },
  // Prettier owns the layout: turn off the rules that conflict with it.
  prettier,
]);
