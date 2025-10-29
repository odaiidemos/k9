import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

interface PasswordResetRequest {
  email: string;
}

interface PasswordResetConfirm {
  token: string;
  password: string;
  password_confirm: string;
}

const FLASK_API_BASE = import.meta.env.VITE_FLASK_API_URL || 'http://localhost:5000';

export const useRequestPasswordReset = () => {
  return useMutation({
    mutationFn: async (data: PasswordResetRequest) => {
      const response = await axios.post(`${FLASK_API_BASE}/password-reset/request`, data);
      return response.data;
    },
  });
};

export const useConfirmPasswordReset = () => {
  return useMutation({
    mutationFn: async (data: PasswordResetConfirm) => {
      const response = await axios.post(`${FLASK_API_BASE}/password-reset/reset/${data.token}`, {
        password: data.password,
        password_confirm: data.password_confirm,
      });
      return response.data;
    },
  });
};
