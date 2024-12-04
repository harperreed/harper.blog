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
    }

    // Get list of available themes
    getThemes() {
        return this.themes;
    }

    // Get current active theme
    getCurrentTheme() {
        return this.currentTheme;
    }

    // Apply a theme to the document
    applyTheme(themeName) {
        // Validate theme name
        if (!this.themes.includes(themeName)) {
            console.error(
                `Theme "${themeName}" not found. Available themes: ${this.themes.join(", ")}`,
            );
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
        localStorage.setItem("theme", themeName);

        // Update current theme
        this.currentTheme = themeName;

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
