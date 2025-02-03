import { create } from 'zustand';
import { Style } from '../types/style';

interface StyleStore {
  styles: Style[];
  setStyles: (styles: Style[]) => void;
}

export const useStyleStore = create<StyleStore>((set) => ({
  styles: [],
  setStyles: (styles) => set({ styles }),
}));