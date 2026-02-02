import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { supabase } from '../lib/supabase';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      loading: true,
      
      login: async (email, password) => {
        try {
          const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password,
          });

          if (error) throw error;

          set({
            user: data.user,
            token: data.session?.access_token,
            loading: false,
          });

          return { success: true };
        } catch (error) {
          console.error('Login error:', error);
          return { success: false, error: error.message };
        }
      },

      register: async (email, password) => {
        try {
          const { data, error } = await supabase.auth.signUp({
            email,
            password,
          });

          if (error) throw error;

          set({
            user: data.user,
            token: data.session?.access_token,
            loading: false,
          });

          return { success: true };
        } catch (error) {
          console.error('Register error:', error);
          return { success: false, error: error.message };
        }
      },

      logout: async () => {
        try {
          await supabase.auth.signOut();
          set({
            user: null,
            token: null,
            loading: false,
          });
        } catch (error) {
          console.error('Logout error:', error);
        }
      },

      initialize: async () => {
        try {
          const { data: { session } } = await supabase.auth.getSession();
          
          set({
            user: session?.user || null,
            token: session?.access_token || null,
            loading: false,
          });
        } catch (error) {
          console.error('Initialize auth error:', error);
          set({ loading: false });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
      }),
    }
  )
);
