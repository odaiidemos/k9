import { useMutation, useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch } from '@store/hooks';
import { setCredentials, logout as logoutAction } from '@store/slices/authSlice';
import apiClient from '@services/api/apiClient';

interface LoginRequest {
  username: string;
  password: string;
  mfa_token?: string;
}

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: {
    id: string;
    username: string;
    full_name: string;
    email: string;
    role: string;
    is_mfa_enabled: boolean;
  };
  mfa_required: boolean;
}

interface RefreshTokenRequest {
  refresh_token: string;
}

interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
}

export const useLogin = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  return useMutation({
    mutationFn: async (credentials: LoginRequest): Promise<LoginResponse> => {
      const response = await apiClient.post('/auth/login', credentials);
      return response.data;
    },
    onSuccess: (data) => {
      if (data.mfa_required) {
        // Don't set credentials yet, wait for MFA verification
        return;
      }
      
      dispatch(
        setCredentials({
          user: data.user,
          accessToken: data.access_token,
          refreshToken: data.refresh_token,
        })
      );
      navigate('/dashboard');
    },
  });
};

export const useLogout = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  return useMutation({
    mutationFn: async () => {
      await apiClient.post('/auth/logout');
    },
    onSuccess: () => {
      dispatch(logoutAction());
      navigate('/login');
    },
    onError: () => {
      // Logout anyway even if API call fails
      dispatch(logoutAction());
      navigate('/login');
    },
  });
};

export const useRefreshToken = () => {
  return useMutation({
    mutationFn: async (refreshToken: string): Promise<RefreshTokenResponse> => {
      const response = await apiClient.post('/auth/refresh', {
        refresh_token: refreshToken,
      });
      return response.data;
    },
  });
};

export const useCurrentUser = () => {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: async () => {
      const response = await apiClient.get('/auth/me');
      return response.data;
    },
  });
};
