"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { FileText, ArrowLeft, CheckCircle2, Circle, Target, Loader2, ChevronDown, ChevronRight, Square, CheckSquare } from "lucide-react";
import { toast } from "sonner";
import clsx from "clsx";
import { API_URL } from "@/lib/api";


export default function EditalSkillTree() {
  const { id } = useParams();
  const router = useRouter();
  const [edital, setEdital] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [checkingIn, setCheckingIn] = useState<string | null>(null);
  const [expandedGroups, setExpandedGroups] = useState<string[]>([]);

  useEffect(() => {
    fetchEdital();
  }, [id]);

  const fetchEdital = () => {
    fetch(`${API_URL}/api/editais/${id}`)

      .then((res) => res.json())
      .then((data) => {
        setEdital(data);
        setLoading(false);
        // Expand the first group by default
        if (data.topics && data.topics.length > 0) {
          const firstTopic = data.topics[0].name;
          const firstGroup = firstTopic.split(" - ")[0] || "Geral";
          setExpandedGroups([firstGroup]);
        }
      });
  };

  const handleStudyCheckIn = async (topicId: string) => {
    setCheckingIn(topicId);
    try {
      const res = await fetch(`${API_URL}/api/study/toggle/${topicId}`, {

        method: "POST"
      });
      if (res.ok) {
        const data = await res.json();
        toast.success(data.is_completed ? "Tópico Concluído!" : "Progresso Removido", {
          description: data.intersection_count > 0 
            ? `${data.intersection_count} tópicos relacionados foram sincronizados.` 
            : 'Sincronizado com sua Skill Tree.'
        });
        fetchEdital();
      }
    } catch (e) {
      toast.error("Erro ao atualizar progresso");
    } finally {
      setCheckingIn(null);
    }
  };

  const toggleGroup = (group: string) => {
    setExpandedGroups(prev => 
      prev.includes(group) ? prev.filter(g => g !== group) : [...prev, group]
    );
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center bg-[#121212]">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
      </div>
    );
  }

  if (!edital || !edital.topics) {
    return (
      <div className="flex flex-col h-full items-center justify-center bg-[#121212]">
        <Target className="w-16 h-16 text-zinc-600 mb-4" />
        <h2 className="text-xl font-bold text-white mb-2">Edital não encontrado</h2>
        <button onClick={() => router.push('/editais')} className="bg-indigo-600 px-6 py-2 rounded-xl font-bold">Voltar</button>
      </div>
    );
  }

  // Grouping logic: Granular (Discipline - Topic Principal)
  const groupOrder: string[] = [];
  const groupedTopics = edital.topics.reduce((acc: any, topic: any) => {
    const parts = topic.name.split(" - ");
    const discipline = parts[0] || "Geral";
    const mainTopic = parts.length > 1 ? parts[1] : "Geral";
    const subtopicName = parts.length > 2 ? parts.slice(2).join(" - ") : (parts[1] || topic.name);
    
    // Group by Discipline + Main Topic (since we no longer have numbers)
    const groupName = parts.length > 1 ? `${discipline} - ${mainTopic}` : discipline;

    if (!acc[groupName]) {
      acc[groupName] = [];
      groupOrder.push(groupName);
    }
    acc[groupName].push({ ...topic, subtopicName });
    return acc;
  }, {});

  const completed = edital.topics.filter((t: any) => t.is_completed).length;
  const total = edital.topics.length;
  const progress = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="flex flex-col h-full overflow-y-auto bg-[#121212] p-4 lg:p-10 hide-scrollbar pb-32">
      <div className="max-w-5xl mx-auto w-full">
        <button onClick={() => router.back()} className="flex items-center gap-2 text-zinc-500 hover:text-white transition-colors mb-8 text-sm font-medium">
          <ArrowLeft className="w-4 h-4" /> Voltar
        </button>

        {/* Header imersivo */}
        <div className="mb-16 bg-[#1E1E1E] p-8 lg:p-10 rounded-[2.5rem] border border-white/5 relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 p-10 opacity-5">
            <Target className="w-40 h-40 text-white" />
          </div>
          <div className="relative z-10">
            <h1 className="text-3xl lg:text-4xl font-black text-white mb-3 tracking-tight">{edital.title}</h1>
            <p className="text-zinc-500 text-sm mb-8 font-medium">Mapa de Conquista • {total} tópicos para dominar</p>
            
            <div className="max-w-md">
              <div className="flex justify-between text-[10px] font-black text-zinc-400 mb-2 uppercase tracking-[0.2em]">
                <span>Status da Operação</span>
                <span className="text-indigo-400">{progress}% Concluído</span>
              </div>
              <div className="w-full bg-white/5 rounded-full h-2.5 p-0.5 border border-white/5">
                <div 
                  className="bg-indigo-500 h-full rounded-full transition-all duration-1000 shadow-[0_0_20px_rgba(99,102,241,0.4)]" 
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Trilha em Zigzag (Path) */}
        <div className="relative space-y-12 before:absolute before:inset-0 before:ml-6 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-1 before:bg-gradient-to-b before:from-transparent before:via-indigo-500/20 before:to-transparent">
          
          {groupOrder.map((groupName, index) => {
            const groupTopics = groupedTopics[groupName];
            const groupCompleted = groupTopics.filter((t: any) => t.is_completed).length;
            const isExpanded = expandedGroups.includes(groupName);
            const isFullyDone = groupCompleted === groupTopics.length;

            return (
              <div key={groupName} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                
                {/* O "Pilar" / Círculo da Trilha */}
                <div className={clsx(
                  "flex items-center justify-center w-12 h-12 rounded-2xl border-4 border-[#121212] shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 transition-all duration-500",
                  isFullyDone ? "bg-emerald-500 text-white shadow-[0_0_20px_rgba(16,185,129,0.3)]" : "bg-[#1E1E1E] text-zinc-500 shadow-xl border-white/5"
                )}>
                  {isFullyDone ? <CheckCircle2 className="w-6 h-6" /> : <span className="text-sm font-black">{index + 1}</span>}
                </div>
                
                {/* Balão da Disciplina */}
                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-3rem)] transition-all duration-300">
                  <div className={clsx(
                    "bg-[#1E1E1E] border rounded-[2rem] overflow-hidden shadow-2xl transition-all duration-300",
                    isExpanded ? "border-indigo-500/30 scale-[1.02]" : "border-white/5 hover:border-white/10"
                  )}>
                    
                    {/* Header do Balão */}
                    <button 
                      onClick={() => toggleGroup(groupName)}
                      className="w-full p-6 text-left flex items-center justify-between group/btn"
                    >
                      <div className="flex-1">
                        <h3 className={clsx(
                          "text-base font-black uppercase tracking-tight mb-1 transition-colors",
                          isFullyDone ? "text-emerald-400" : "text-white"
                        )}>
                          {groupName}
                        </h3>
                        <div className="flex items-center gap-3">
                          <div className="h-1 w-20 bg-white/5 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-indigo-500" 
                              style={{ width: `${(groupCompleted / groupTopics.length) * 100}%` }}
                            />
                          </div>
                          <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-widest">
                            {groupCompleted} / {groupTopics.length} Subtópicos
                          </span>
                        </div>
                      </div>
                      
                      <div className={clsx(
                        "w-8 h-8 rounded-full flex items-center justify-center bg-white/5 transition-all group-hover/btn:bg-indigo-500 group-hover/btn:text-white",
                        isExpanded ? "rotate-180 bg-indigo-500 text-white" : "text-zinc-500"
                      )}>
                        <ChevronDown className="w-4 h-4" />
                      </div>
                    </button>

                    {/* Lista de Subtópicos (Dropdown dentro do balão) */}
                    {isExpanded && (
                      <div className="px-4 pb-6 space-y-2 animate-in fade-in slide-in-from-top-4 duration-300">
                        <div className="h-px bg-white/5 mb-4 mx-2" />
                        {groupTopics.map((topic: any) => (
                          <div 
                            key={topic.id}
                            onClick={() => handleStudyCheckIn(topic.id)}
                            className={clsx(
                              "flex items-center gap-3 p-3 rounded-xl border transition-all cursor-pointer group/item",
                              topic.is_completed 
                                ? "bg-emerald-500/5 border-emerald-500/20" 
                                : "bg-black/20 border-white/5 hover:border-indigo-500/30"
                            )}
                          >
                            <div className={clsx(
                              "transition-colors",
                              topic.is_completed ? "text-emerald-500" : "text-zinc-700 group-hover/item:text-indigo-400"
                            )}>
                              {topic.is_completed ? <CheckSquare className="w-4 h-4" /> : <Square className="w-4 h-4" />}
                            </div>
                            
                            <div className="flex-1">
                              <p className={clsx(
                                "text-[13px] font-semibold leading-tight transition-colors",
                                topic.is_completed ? "text-emerald-400/50 line-through" : "text-zinc-300"
                              )}>
                                {topic.subtopicName}
                              </p>
                            </div>

                            {checkingIn === topic.id && (
                              <Loader2 className="w-3 h-3 text-indigo-500 animate-spin" />
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
}
