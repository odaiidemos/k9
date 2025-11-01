import { apiClient } from '../api/apiClient';
import type { Notification } from '../../types/handler';

export const notificationService = {
  async getNotifications(unreadOnly: boolean = false): Promise<Notification[]> {
    const response = await apiClient.get<Notification[]>('/handler-daily/notifications', {
      params: { unread_only: unreadOnly }
    });
    return response.data;
  },

  async markAsRead(notificationId: string): Promise<Notification> {
    const response = await apiClient.post<Notification>(`/handler-daily/notifications/${notificationId}/read`);
    return response.data;
  },

  async markAllAsRead(): Promise<{ message: string; count: number }> {
    const response = await apiClient.post<{ message: string; count: number }>('/handler-daily/notifications/mark-all-read');
    return response.data;
  },

  async getUnreadCount(): Promise<number> {
    const response = await apiClient.get<{ count: number }>('/handler-daily/notifications/unread-count');
    return response.data.count;
  }
};
