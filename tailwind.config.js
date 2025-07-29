/** @type {import('tailwindcss').Config} */

module.exports = {
    content: [
        './insight_ui/templates/**/**/**/*.html',
        './insight_ui/templates/**/**/*.html',
        './insight_ui/templates/**/*.html',
        './templates/**/*.html',
        './templates/*.html',
    ],
    darkMode: 'class',
    theme: {
        extend: {
            fontFamily: {
                'sans': ['Inter', 'sans-serif'],
            },
            colors: {
                'insight-primary': '#3b82f6',
                'insight-primary-hover': '#60a5fa',
                'insight-primary-active': '#93c5fd',
                'insight-secondary': '#6b7280',
                'insight-secondary-hover': '#94a3b8',
                'insight-secondary-active': '#cbd5e1',
                'insight-success': '#10b981',
                'insight-success-hover': '#34d399',
                'insight-success-active': '#6ee7b7',
                'insight-warning': '#f59e0b',
                'insight-warning-hover': '#fbbf24',
                'insight-warning-active': '#fcd34d',
                'insight-error': '#ef4444',
                'insight-error-hover': '#f87171',
                'insight-error-active': '#fca5a5',
                'insight-info': '#06b6d4',
                'insight-info-hover': '#22d3ee',
                'insight-info-active': '#67e8f9',
                'insight-text-primary': '#262626',
                'insight-text-secondary': '#737373',
                'insight-text-primary-dark': '#e5e7eb',
                'insight-text-secondary-dark': '#94a3b8',
                'insight-text-link': '#3b82f6',
                'insight-text-link-hover': '#93c5fd',
            },
            screens: {
                '3xl': '1920px',
                '4xl': '2560px',
                '5xl': '3840px',
            },
        },
    },
    plugins: [],
}
