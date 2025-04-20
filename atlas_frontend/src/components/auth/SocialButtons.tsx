import React from 'react';

const SocialButtons: React.FC = () => {
  return (
    <div className="flex gap-4 mb-6">
      <button className="flex items-center justify-center w-40 h-10 border rounded-md shadow-sm">
        <img src="/google-icon.svg" alt="Google" className="w-5 h-5 mr-2" />
        Google
      </button>
      <button className="flex items-center justify-center w-40 h-10 border rounded-md shadow-sm">
        <img src="/linkedin-icon.svg" alt="LinkedIn" className="w-5 h-5 mr-2" />
        LinkedIn
      </button>
    </div>
  );
};