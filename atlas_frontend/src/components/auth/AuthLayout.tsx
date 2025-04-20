import React from 'react';

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen">
      <div className="w-1/2 bg-gradient-to-b from-purple-200 to-purple-400 flex flex-col justify-center items-center">
        <h1 className="text-4xl font-bold text-white mb-4">Atlas</h1>
        <p className="text-white text-lg">Get Started with Us</p>
        <p className="text-white text-sm mt-2">Complete these easy steps to register your account</p>
      </div>
      <div className="w-1/2 flex justify-center items-center">{children}</div>
    </div>
  );
};

export default AuthLayout;