# Django Insight UI Package – Comprehensive Development Prompt

You are tasked with creating a fully production-ready, modern Django UI package called `django-insight-ui` with the following features, architecture, and quality requirements:

## 1. Project Overview

- Name: `django-insight-ui`
- Purpose: A modern, extensible, and highly accessible Django UI framework that delivers reusable, WCAG 2.1 AA-compliant components and development best practices.
- Core Stack: Django (LTS), django-HTMX, TailwindCSS from CDN, Alpine.js, UV, and automated accessibility.

## 2. Project Architecture & Structure

- Use UV as the Python package manager.
- Strictly follow the outlined directory structure (see below).
- Support for docs, tests, playground, and an examples/demo project.

Replicate exactly this file/folder structure:
```
<strukturierter Verzeichnisbaum, siehe oben>
```
No changes to the structure. No flattening. No merging. No omission.

## 3. Development Workflow

- ONLY use uv, NEVER pip
- Installation: `uv add package`
- Running tools: `uv run tool`
- Upgrading: `uv add --dev package --upgrade-package package`
- FORBIDDEN: `uv pip install`, `@latest` syntax
- Install all dependencies (prod/dev/docs/test/security/performance)
- Setup pre-commit hooks
- Automated testing, linting, type checking, accessibility & security checks per commands given below.

Only use UV for package management!

## Error Resolution

1. CI Failures
   - Fix order:
 1. Formatting
 2. Type errors
 3. Linting
   - Type errors:
 - Get full line context
 - Check Optional types
 - Add type narrowing
 - Verify function signatures

2. Common Issues
   - Line length:
 - Break strings with parentheses
 - Multi-line function calls
 - Split imports
   - Types:
 - Add None checks
 - Narrow string types
 - Match existing patterns
   - Pytest:
 - If the tests aren't finding the anyio pytest mark, try adding PYTEST_DISABLE_PLUGIN_AUTOLOAD=""
   to the start of the pytest run command eg:
   `PYTEST_DISABLE_PLUGIN_AUTOLOAD="" uv run --frozen pytest`

3. Best Practices
   - Check git status before commits
   - Run formatters before type checks
   - Keep changes minimal
   - Follow existing patterns
   - Document public APIs
   - Test thoroughly

## 4. Key Features & Implementation Requirements

### 4.1. UI Components

- Navbar, Sidebar, Breadcrumbs, Tables, Alerts, Forms, Modals, Cards, Widgets
- Responsive, mobile-first, with dark/light/high-contrast modes
- Full keyboard navigation, ARIA roles, skip links, and semantic markup

### 4.2. Template Tags

- For all core UI elements (alerts, forms, tables, i18n, modals, etc.)
- Each tag supports accessibility and i18n out of the box

### 4.3. Accessibility

- Strict WCAG 2.1 AA compliance across all components
- High-contrast mode, screen reader live regions, focus management, skip links, ARIA everywhere
- Automated accessibility test suite (axe-core, Playwright, selenium integration)

### 4.4. Internationalization

- Full multi-language support (en, es, fr, de, ar, zh)
- RTL support for relevant languages
- Date, number, currency formatting via template tags
- Lazy loading, code splitting, CSS purging, optimized images, critical CSS
- Customizable via settings

### 4.6. Security

- CSRF, XSS, CSP, input/file validation, secure headers
- Pre-configured middleware and template best practices

### 4.7. HTMX Integration

- Progressive enhancement, dynamic updates, infinite scroll, WebSocket support, form validation via HTMX
- Custom HTMX extension points

### 4.8. Design System

- Design tokens via CSS variables for all theming, colors, spacings, typography, focus states, etc.
- Easy extension for custom themes

### 4.9. Configuration

- Single INSIGHT_UI dict in Django settings to override defaults: theme, branding, features, i18n, security, analytics, and component overrides

### 4.10. Documentation

- Written in Markdown, mkdocs-compatible, covering:
- Installation, Quickstart, API, customization, accessibility, examples, advanced topics
- Component playground and live demos

## 5. Testing

- Test suite for:
- All template tags
- All UI components (snapshot, accessibility, i18n, security, performance)
- Browser-based accessibility testing (axe, Playwright)
- Keyboard navigation and screen reader compatibility

## 6. CI/CD

- CI: Test, lint, type-check, accessibility-audit on every PR and main
- Release: Automated release pipeline with changelog, tag, and PyPI upload

## 7. Deliverables

- A UV-managed, installable Django package with the described directory and file structure
- All listed UI components and template tags, fully tested and documented
- Out-of-the-box accessibility and i18n
- Complete docs and example/demo project
- A11y, security, performance, and testing integrated by default

## 8. Prompt Format (for LLMs or devs)

Prompt block format:
- [Feature/Component]: {short description}
- Acceptance Criteria: (bulleted list)
- Directory/Files to update: (relative paths)
- Code Example/Template: (if relevant)
- Test Cases: (if relevant)

Repeat for each major feature/component as prompt building blocks.

## 9. Output Example for LLMs

> [Navbar Component: Responsive, Accessible Navbar]
> Acceptance Criteria:
> - Renders as <nav role="navigation" aria-label="Main navigation">
> - Hamburger menu is keyboard accessible, ARIA-compliant
> - Language and color mode toggles support keyboard/ARIA
> Directory/Files to update:
> - insight_ui/templates/insight_ui/components/navbar.html
> - insight_ui/static/insight_ui/js/components.js
> Code Example:
> ```django
> {% load insight_tags %}
> {% navbar brand="MyApp" links=nav_links theme=theme %}
> ```
> Test Cases:
> - Test navbar is rendered for all screen sizes
> - Test skip links and hamburger menu for keyboard navigation
> - Test ARIA landmarks and roles

Deliver all code, documentation, and configuration strictly according to this prompt. No creative deviation or omission. Everything must be testable, documented, accessible, and extensible out-of-the-box.