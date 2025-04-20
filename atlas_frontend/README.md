# Atlas Frontend

This is the frontend of the **Atlas Workspace Management Platform**, built with [Next.js](https://nextjs.org) and styled using **Tailwind CSS**. The project is modular, scalable, and designed for seamless integration with backend APIs.

---

## 🚀 **Getting Started**

### **Prerequisites**
Make sure you have the following installed:
- **Node.js** (v18.17 or later) - [Download Node.js](https://nodejs.org/)
- **npm** (comes with Node.js), **yarn**, or **pnpm**
- Git for version control

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/atlas-frontend.git
   cd atlas-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   Create a `.env.local` file in the root directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

### **Development**

Start the development server:
```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to see the application.

---

## 🛠️ **Project Setup**

Built with modern technologies:
- **Next.js 14**: For server-side rendering and API routes
- **TypeScript**: For type safety and better DX
- **Tailwind CSS**: For utility-first styling
- **React Icons**: For beautiful icons
- **shadcn/ui**: For reusable UI components

---

## 📁 **Folder Structure**

```
atlas_frontend/
├── src/
│   ├── app/           # Next.js app router pages
│   ├── components/    # Reusable components
│   │   ├── auth/     # Authentication components
│   │   ├── layout/   # Layout components (Navbar, Footer)
│   │   └── sections/ # Page sections (Hero, Resources)
│   └── styles/       # Global styles
├── public/           # Static assets
└── tests/           # Test files
```

---

## ✨ **Key Features**

- 🎨 **Modern UI/UX**: Clean, responsive design with Tailwind CSS
- 🔒 **Authentication**: Secure user authentication system
- 📱 **Responsive**: Mobile-first approach
- 🔍 **Search & Filter**: Advanced workspace search capabilities
- 📅 **Booking System**: Intuitive workspace booking interface
- 🔄 **Real-time Updates**: Live availability status
- 🌐 **Integration Ready**: Connects with various third-party tools

---

## 🧪 **Testing**

Run the test suite:
```bash
npm test
```

For development with watch mode:
```bash
npm test -- --watch
```

---

## 📦 **Building for Production**

1. Build the application:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm start
   ```

3. For deployment, we recommend using:
   - [Vercel](https://vercel.com) (Zero-configuration)
   - [Netlify](https://www.netlify.com)
   - [AWS Amplify](https://aws.amazon.com/amplify/)

---

## 👥 **Contributing**

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) and [Contributing Guidelines](CONTRIBUTING.md).

---

## 📄 **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 **Support**

For support, reach out to:
- Create an issue
- Contact the team at support@atlas.com
- Join our [Discord community](https://discord.gg/atlas)