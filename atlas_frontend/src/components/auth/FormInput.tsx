import React from 'react';

interface FormInputProps {
  label: string;
  type: string;
  placeholder: string;
}

const FormInput: React.FC<FormInputProps> = ({ label, type, placeholder }) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <input
        type={type}
        placeholder={placeholder}
        className="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
      />
    </div>
  );
};

export default FormInput;