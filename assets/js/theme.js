class ThemeManager {
    constructor() {
        // Available themes from the CSS
        this.themes = [
            "default", // No theme class
            "dark",
            "nature",
            "sunset",
            "ocean",
            "desert",
            "nordic",
            "autumn",
            "cyber",
            "academia",
            "myspace",
        ];

        // Get the saved theme from localStorage or use default
        this.currentTheme = localStorage.getItem("theme") || "default";

        // Apply the saved theme on initialization
        this.applyTheme(this.currentTheme);

        // Check for prefers-color-scheme and apply dark theme if preferred
        this.applyPreferredColorScheme();
    }

    // Get list of available themes
    /**
     * Returns a copy of available themes array
     * @returns {readonly string[]} Array of theme names
     */
    getThemes() {
        return Object.freeze([...this.themes]);
    }

    /**
     * Returns the currently active theme name
     * @returns {string} Current theme name
     */
    getCurrentTheme() {
        return this.currentTheme;
    }

    /**
     * Applies a theme to the document
     * @param {string} themeName - Name of the theme to apply
     * @returns {boolean} Success status
     * @fires ThemeManager#themeChanged
     */
    applyTheme(themeName) {
        // Validate theme name
        if (!this.themes.includes(themeName)) {
            console.error(
                `Theme "${themeName}" not found. Available themes: ${this.themes.join(", ")}`,
            );
            return false;
        }

        if (!document.body) {
            console.error("Document body not available");
            return false;
        }

        // Remove any existing theme classes
        document.body.classList.remove(
            ...this.themes.map((theme) => `theme-${theme}`),
        );

        // Apply new theme if it's not default
        if (themeName !== "default") {
            document.body.classList.add(`theme-${themeName}`);
        }

        // Save to localStorage
        try {
            localStorage.setItem("theme", themeName);
        } catch (e) {
            console.warn("Failed to save theme to localStorage:", e);
        }

        // Update current theme
        this.currentTheme = themeName;

        // Dispatch theme change event
        window.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme: themeName }
        }));

        return true;
    }

    // Toggle between light and dark themes
    toggleDarkMode() {
        const newTheme = this.currentTheme === "dark" ? "default" : "dark";
        return this.applyTheme(newTheme);
    }

    // Get a random theme
    setRandomTheme() {
        const randomIndex = Math.floor(Math.random() * this.themes.length);
        return this.applyTheme(this.themes[randomIndex]);
    }

    // Apply preferred color scheme based on user preference
    applyPreferredColorScheme() {
        const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
        if (prefersDarkScheme && this.currentTheme === "default") {
            this.applyTheme("dark");
        }
    }
}

// Usage example:
// const themeManager = new ThemeManager();
//
// // Change theme
// themeManager.applyTheme('ocean');
//
// // Toggle dark mode
// themeManager.toggleDarkMode();
//
// // Get current theme
// console.log(themeManager.getCurrentTheme());
//
// // Get list of available themes
// console.log(themeManager.getThemes());
//
// // Set random theme
// themeManager.setRandomTheme();
