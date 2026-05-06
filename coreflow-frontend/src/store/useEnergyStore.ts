import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type EnergyState = "high" | "neutral" | "low" | null;

interface EnergyStore {
  energy: EnergyState;
  setEnergy: (energy: EnergyState) => void;
}

export const useEnergyStore = create<EnergyStore>()(
  persist(
    (set) => ({
      energy: null,
      setEnergy: (energy) => set({ energy }),
    }),
    {
      name: 'coreflow-energy-storage',
    }
  )
);
