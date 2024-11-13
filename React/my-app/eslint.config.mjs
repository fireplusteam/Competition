import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";

export default [
    { files: ["**/*.{js,mjs,cjs,jsx}"] },
    { files: ["**/*.js"], languageOptions: { sourceType: "commonjs" } },
    { languageOptions: { globals: globals.browser } },
    pluginJs.configs.recommended,
    pluginReact.configs.flat.recommended,
    {
        rules: {
            "no-unused-vars": "warn",
            "no-undef": "error",
            semi: "warn",
            quotes: "warn",
        },
        parserOptions: {
            sourceType: "module",
        },
    },
];
