# Contributing to Atlas Frontend

Thank you for your interest in contributing to Atlas! This document provides guidelines and steps for contributing to our frontend application.

## 🤝 Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/atlas-frontend.git
   cd atlas-frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💻 Development Guidelines

### Code Style

- Use TypeScript for all new code
- Follow the existing code style and formatting
- Use functional components and hooks for React components
- Keep components small and focused
- Use meaningful variable and function names
- Add comments for complex logic
- Use proper TypeScript types (avoid `any`)

### Commits

- Use conventional commits format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `style:` for formatting changes
  - `refactor:` for code refactoring
  - `test:` for adding tests
  - `chore:` for maintenance tasks

Example: `feat: add user authentication component`

### Testing

- Write tests for new features
- Update existing tests when modifying features
- Ensure all tests pass before submitting PR
- Test your changes in different browsers

### File Structure

- Place new components in appropriate directories under `src/components/`
- Keep related files together
- Follow the established project structure
- Create new directories if needed (discuss in issue first)

## 🔄 Pull Request Process

1. **Update Documentation**
   - Add comments to your code
   - Update README.md if needed
   - Add JSDoc comments for functions/components

2. **Create Pull Request**
   - Update your fork with the latest main branch
   - Push your changes
   - Create a PR with a clear title and description

3. **PR Description Template**
   ```markdown
   ## Description
   [Describe your changes here]

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Tested manually
   - [ ] Screenshots attached (for UI changes)

   ## Related Issues
   Fixes #[issue number]
   ```

4. **Review Process**
   - Maintainers will review your PR
   - Address any requested changes
   - Once approved, maintainers will merge

## 🐛 Reporting Bugs

Create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (browser, OS, etc.)

## 💡 Feature Requests

Create an issue with:
- Clear title and description
- Problem you're trying to solve
- Proposed solution
- Alternative solutions considered
- Screenshots/mockups if applicable

## 📝 Documentation

- Keep documentation up to date
- Use clear and concise language
- Include code examples when helpful
- Update TypeScript types and comments

## 🔨 Tools & Environment

- VS Code is recommended
- Install recommended extensions:
  - ESLint
  - Prettier
  - TypeScript and JavaScript Language Features

## 📊 Performance Considerations

- Optimize imports
- Use React.memo when appropriate
- Lazy load components when possible
- Optimize images and assets
- Consider bundle size impact

