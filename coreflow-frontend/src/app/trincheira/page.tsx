"use client";

import { useEnergyStore } from "@/store/useEnergyStore";
import { CheckCircle2, ChevronRight, Play, Zap, ShieldAlert } from "lucide-react";
import { toast } from "sonner";
import { useState, useEffect } from "react";
import clsx from "clsx";

// Os ícones mapeados pela resposta da API
const getIconForType = (type: string) => {
  if (type === "theory") return <Zap className="w-5 h-5 text-amber-500" />;
  if (type === "exercise") return <CheckCircle2 className="w-5 h-5 text-emerald-500" />;
  if (type === "flashcard") return <Play className="w-5 h-5 text-blue-400" />;
  return <ChevronRight className="w-5 h-5 text-zinc-400" />;
};

export default function TrincheiraPage() {
  const { energy } = useEnergyStore();
  const [missions, setMissions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [completedTasks, setCompletedTasks] = useState<string[]>([]);
  const [isAdding, setIsAdding] = useState(false);
  const [newMissionTitle, setNewMissionTitle] = useState("");

  const fetchMissions = async () => {
    setIsLoading(true);
    try {
      const energyQuery = energy === "high" ? "high_focus" : energy === "low" ? "low_focus" : "neutral";
      const res = await fetch(`http://localhost:8000/api/missions?energy_state=${energyQuery}`);
      const data = await res.json();
      setMissions(data);
      // Extrair missões que vieram completas do banco (se aplicável)
      setCompletedTasks(data.filter((m: any) => m.status === 'completed').map((m: any) => m.id));
    } catch (error) {
      console.error("Erro ao buscar missões da API", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMissions();
  }, [energy]);

  const handleTaskToggle = async (mission: any, isCurrentlyCompleted: boolean) => {
    // Optimistic UI update
    if (isCurrentlyCompleted) {
      setCompletedTasks(completedTasks.filter(id => id !== mission.id));
      toast("Missão desmarcada", { description: "De volta para a trincheira." });
    } else {
      setCompletedTasks([...completedTasks, mission.id]);
      toast.success("Missão Concluída!", { description: `${mission.title}` });
    }

    try {
      await fetch(`http://localhost:8000/api/missions/${mission.id}/toggle`, {
        method: "PUT"
      });
    } catch (e) {
      toast.error("Erro ao sincronizar com servidor");
      fetchMissions(); // Revert on failure
    }
  };

  const handleAddMission = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMissionTitle.trim()) return;

    try {
      const res = await fetch("http://localhost:8000/api/missions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: newMissionTitle,
          energy_cost: energy === "high" ? "high_focus" : energy === "low" ? "low_focus" : "neutral"
        })
      });
      if (res.ok) {
        toast.success("Missão Adicionada");
        setNewMissionTitle("");
        setIsAdding(false);
        fetchMissions();
      }
    } catch (e) {
      toast.error("Erro ao adicionar missão");
    }
  };

  const currentMissions = missions;

  return (
    <div className="max-w-2xl mx-auto p-4 sm:p-8 relative min-h-screen">
      
      {/* Header */}
      <header className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Trincheira</h1>
          <p className="text-sm text-zinc-500">
            {energy === "high" ? "Foco Total" : energy === "low" ? "Modo Recuperação" : "Foco Estável"}
          </p>
        </div>
        <div className="text-right flex items-center gap-4">
          <div>
            <span className="text-xs font-bold text-zinc-600 uppercase tracking-widest">Missões Ativas</span>
            <p className="text-xl font-bold text-zinc-300">{currentMissions.length - completedTasks.length}</p>
          </div>
          <button 
            onClick={() => setIsAdding(!isAdding)}
            className="w-10 h-10 rounded-xl bg-indigo-500 text-white flex items-center justify-center font-bold hover:bg-indigo-600 transition-colors"
          >
            +
          </button>
        </div>
      </header>

      {/* Add Mission Form */}
      {isAdding && (
        <form onSubmit={handleAddMission} className="mb-6 animate-in fade-in slide-in-from-top-4">
          <input 
            type="text" 
            autoFocus
            value={newMissionTitle}
            onChange={(e) => setNewMissionTitle(e.target.value)}
            placeholder="Qual é a nova missão?" 
            className="w-full bg-[#1E1E1E] border border-indigo-500/50 rounded-2xl p-4 text-white focus:outline-none focus:border-indigo-500 placeholder:text-zinc-600"
          />
        </form>
      )}

      {/* Mission List */}
      <div className="space-y-4 pb-24">
        {isLoading && (
          <div className="text-center text-zinc-500 py-12 animate-pulse">
            Iniciando ADHD Engine... Consultando Supabase...
          </div>
        )}
        
        {!isLoading && currentMissions.length === 0 && (
          <div className="text-center text-zinc-500 py-12">
            Nenhuma missão pendente encontrada para este estado de energia.
          </div>
        )}

        {!isLoading && currentMissions.map((mission, index) => {
          const isCompleted = completedTasks.includes(mission.id);
          
          return (
            <div 
              key={mission.id}
              onClick={() => handleTaskToggle(mission, isCompleted)}
              className={clsx(
                "p-5 rounded-3xl flex items-center justify-between group transition-all duration-500 select-none cursor-pointer",
                isCompleted 
                  ? "bg-emerald-500/5 border border-emerald-500/20 opacity-50 grayscale scale-[0.98]" 
                  : "bg-[#1E1E1E] border border-white/5 hover:-translate-y-1 hover:border-white/10 hover:shadow-lg animate-in fade-in slide-in-from-bottom-4 fill-mode-both"
              )}
              style={{ animationDelay: isCompleted ? '0ms' : `${index * 100}ms` }}
            >
              <div className="flex items-center gap-4">
                <div className={clsx(
                  "w-12 h-12 rounded-2xl flex items-center justify-center transition-transform",
                  isCompleted ? "bg-emerald-500/20 text-emerald-500" : "bg-[#2A2A2A] group-hover:scale-110"
                )}>
                  {isCompleted ? <CheckCircle2 className="w-6 h-6" /> : getIconForType(mission.type)}
                </div>
                
                <div>
                  <h4 className={clsx(
                    "font-semibold text-lg transition-colors mb-1",
                    isCompleted ? "text-zinc-500 line-through" : "text-zinc-200 group-hover:text-white"
                  )}>
                    {mission.title}
                  </h4>
                  
                  <div className="flex items-center gap-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 uppercase tracking-wider">
                      {mission.source}
                    </span>
                    <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider">
                      #{mission.type}
                    </span>
                    <span className="w-1 h-1 rounded-full bg-zinc-700"></span>
                    <span className="text-xs text-zinc-500 font-medium">~ 30m</span>
                  </div>
                </div>
              </div>
              
              <div className={clsx(
                "w-8 h-8 rounded-full flex items-center justify-center transition-colors",
                isCompleted ? "bg-transparent text-emerald-500" : "text-zinc-600 group-hover:text-emerald-400"
              )}>
                <CheckCircle2 className="w-5 h-5" />
              </div>
            </div>
          );
        })}
      </div>

      {/* FAB - Escudo de Imprevistos */}
      <button 
        className="fixed bottom-24 right-6 sm:bottom-8 sm:right-8 w-14 h-14 rounded-full bg-rose-500/20 border border-rose-500/50 text-rose-400 flex items-center justify-center shadow-[0_0_20px_rgba(244,63,94,0.3)] hover:scale-110 hover:bg-rose-500/30 transition-all z-50"
        title="Modo Evento (Escudo)"
        onClick={() => toast("Escudo Ativado", { description: "Sua ofensiva foi protegida hoje." })}
      >
        <ShieldAlert className="w-6 h-6" />
      </button>

    </div>
  );
}
