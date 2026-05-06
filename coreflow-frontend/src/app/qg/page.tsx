"use client";

import { useEnergyStore } from "@/store/useEnergyStore";
import { Battery, BatteryCharging, BatteryWarning, Target, BarChart3, GraduationCap } from "lucide-react";
import clsx from "clsx";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { useState, useEffect, useRef } from "react";

export default function QgPage() {
  const { energy, setEnergy } = useEnergyStore();
  const router = useRouter();
  const [isUploading, setIsUploading] = useState(false);
  const [qcStats, setQcStats] = useState({ acertos: 85, questoes_hoje: 142, disciplinas: 3 });
  const [isSyncingQc, setIsSyncingQc] = useState(false);
  
  const [isSelectingCargo, setIsSelectingCargo] = useState(false);
  const [availableCargos, setAvailableCargos] = useState<string[]>([]);
  const [tempFilePath, setTempFilePath] = useState("");
  const [isGeneratingTree, setIsGeneratingTree] = useState(false);
  const [parsingProgress, setParsingProgress] = useState(0);
  const [parsingStatus, setParsingStatus] = useState("Iniciando...");
  const [missions, setMissions] = useState<any[]>([]);
  const [isLoadingMissions, setIsLoadingMissions] = useState(false);

  // --- Sistema Dinâmico de Frases ---
  interface Quote {
    text: string;
    author: string;
    category: 'anime' | 'math' | 'cs' | 'perito';
  }

  const [dailyPhrase, setDailyPhrase] = useState<Quote>({
    text: "A ciência forense é o seu idioma; a justiça, sua missão.",
    author: "Provérbio Pericial",
    category: 'perito'
  });

  const localQuotes: Quote[] = [
    { text: "A verdade deixa rastros — e o perito sabe segui-los.", author: "Edmond Locard", category: 'perito' },
    { text: "Perito criminal: especialista em transformar caos em clareza.", author: "Verônica Oliveira", category: 'perito' },
    { text: "A ciência forense é o seu idioma; a justiça, sua missão.", author: "Academia de Polícia", category: 'perito' },
    { text: "Vestígios são testemunhas que não mentem.", author: "Hans Gross", category: 'perito' },
    { text: "A matemática é o alfabeto com o qual Deus escreveu o universo.", author: "Galileu Galilei", category: 'math' },
    { text: "Na matemática, a arte de propor uma questão deve ser mantida em valor mais alto do que a de resolvê-la.", author: "Georg Cantor", category: 'math' },
    { text: "A melhor maneira de prever o futuro é inventá-lo.", author: "Alan Kay", category: 'cs' },
    { text: "Computadores são inúteis. Eles só podem dar respostas.", author: "Pablo Picasso", category: 'cs' },
    { text: "O software é uma combinação de arte e engenharia.", author: "Bill Gates", category: 'cs' }
  ];

  useEffect(() => {
    const fetchDynamicQuote = async () => {
      // Tenta buscar de APIs externas, se falhar usa o banco local
      try {
        const types = ['anime', 'cs', 'perito'];
        const selectedType = types[new Date().getDate() % types.length];

        if (selectedType === 'anime') {
          const res = await fetch('https://animechan.xyz/api/random');
          if (res.ok) {
            const data = await res.json();
            setDailyPhrase({ text: data.quote, author: `${data.character} (${data.anime})`, category: 'anime' });
            return;
          }
        } else if (selectedType === 'cs') {
          const res = await fetch('https://api.quotable.io/random?tags=technology');
          if (res.ok) {
            const data = await res.json();
            setDailyPhrase({ text: data.content, author: data.author, category: 'cs' });
            return;
          }
        }
        
        // Fallback para banco local se API falhar ou tipo for perito/math
        const local = localQuotes[new Date().getDate() % localQuotes.length];
        setDailyPhrase(local);
      } catch (e) {
        const local = localQuotes[new Date().getDate() % localQuotes.length];
        setDailyPhrase(local);
      }
    };

    fetchDynamicQuote();
  }, []);
  // ----------------------------------

  useEffect(() => {
    const fetchMissions = async () => {
      setIsLoadingMissions(true);
      try {
        // Map store energy to backend enum
        const stateMap = { high: "high_focus", neutral: "neutral", low: "low_focus" };
        const res = await fetch(`http://localhost:8000/api/missions?energy_state=${stateMap[energy]}`);
        if (res.ok) {
          const data = await res.json();
          setMissions(data);
        }
      } catch (e) {
        console.error("Erro ao buscar missões", e);
      } finally {
        setIsLoadingMissions(false);
      }
    };
    fetchMissions();
  }, [energy]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isGeneratingTree) {
      const statuses = [
        "Iniciando extração...",
        "Lendo Conteúdo Programático...",
        "Mapeando disciplinas...",
        "Identificando sub-tópicos...",
        "Gerando tags universais...",
        "Cruzando com Skill Tree...",
        "Finalizando estrutura..."
      ];
      
      interval = setInterval(() => {
        setParsingProgress(prev => {
          const next = prev + (prev < 90 ? 1 : 0.2);
          const clampedNext = Math.min(next, 99.9); // Mantém em 99.9% até o servidor responder
          
          // Update status message based on progress
          const statusIdx = Math.min(Math.floor((clampedNext / 100) * statuses.length), statuses.length - 1);
          setParsingStatus(statuses[statusIdx]);
          
          return clampedNext;
        });
      }, 150);
    } else {
      setParsingProgress(0);
    }
    return () => clearInterval(interval);
  }, [isGeneratingTree]);

  useEffect(() => {
    const fetchQcStats = async () => {
      setIsSyncingQc(true);
      try {
        const res = await fetch("http://localhost:8000/api/sync/qc/stats");
        if (res.ok) {
          const data = await res.json();
          setQcStats(data);
        }
      } catch (error) {
        console.error("Erro ao sincronizar QConcursos", error);
      } finally {
        setIsSyncingQc(false);
      }
    };
    fetchQcStats();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith(".pdf")) {
      toast.error("Formato Inválido", { description: "Por favor, envie apenas arquivos PDF." });
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setIsUploading(true);
    toast("Analisando PDF...", { description: "Buscando os cargos disponíveis no edital." });

    try {
      const res = await fetch("http://localhost:8000/api/editais/extract-cargos", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        setAvailableCargos(data.cargos);
        setTempFilePath(data.file_path);
        setIsSelectingCargo(true);
        toast.success("Cargos encontrados!");
      } else {
        toast.error("Erro na leitura do PDF.");
      }
    } catch (error) {
      toast.error("Erro de conexão com o servidor.");
    } finally {
      setIsUploading(false);
      e.target.value = ''; // Reset input
    }
  };

  const handleCargoSelect = async (cargoName: string) => {
    setIsGeneratingTree(true);
    toast("Gerando Skill Tree...", { description: `Extraindo subtópicos para: ${cargoName}` });

    try {
      const res = await fetch("http://localhost:8000/api/editais/parse-cargo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          file_path: tempFilePath,
          cargo_name: cargoName
        }),
      });

      if (res.ok) {
        const data = await res.json();
        toast.success("Edital Processado!", { description: "Redirecionando..." });
        setIsSelectingCargo(false);
        router.push(`/editais/${data.edital_id}`);
      } else {
        toast.error("Erro ao gerar Skill Tree.");
      }
    } catch (error) {
      toast.error("Erro de conexão com o servidor.");
    } finally {
      setIsGeneratingTree(false);
    }
  };

  const handleEnergySelect = (selectedEnergy: "high" | "neutral" | "low") => {
    setEnergy(selectedEnergy);
    toast.success("Bateria atualizada!", { description: "Sua trincheira foi reorganizada." });
    setTimeout(() => {
      router.push("/trincheira");
    }, 800);
  };

  return (
    <div className="max-w-5xl mx-auto p-4 sm:p-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      
      {/* Hero Motivation */}
      <section className="text-center my-12 sm:my-16 flex flex-col items-center">
        <h1 className="max-w-4xl text-2xl sm:text-4xl md:text-5xl font-black italic tracking-tight text-white mb-4 animate-in fade-in zoom-in duration-1000">
          "{dailyPhrase.text}"
        </h1>
        <div className="flex items-center gap-3">
          <p className="text-zinc-500 font-medium tracking-widest uppercase text-[10px] sm:text-xs">— {dailyPhrase.author}</p>
          <span className="text-[8px] font-black px-1.5 py-0.5 rounded bg-white/5 text-zinc-600 uppercase tracking-tighter border border-white/5">
            #{dailyPhrase.category}
          </span>
        </div>
      </section>

      {/* Missions Section (Nova!) */}
      <section className="mb-16">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-sm font-semibold text-zinc-400 uppercase tracking-widest flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Missões Recomendadas
          </h2>
          <button 
            onClick={() => router.push("/trincheira")}
            className="text-[10px] font-bold text-indigo-400 hover:text-indigo-300 uppercase tracking-widest transition-colors"
          >
            Ver Todas
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {isLoadingMissions ? (
            Array(3).fill(0).map((_, i) => (
              <div key={i} className="h-24 bg-[#1E1E1E] rounded-3xl animate-pulse border border-white/5" />
            ))
          ) : missions.length > 0 ? (
            missions.slice(0, 3).map((mission) => (
              <div 
                key={mission.id}
                className="group relative bg-[#1E1E1E] border border-white/5 p-5 rounded-3xl hover:border-indigo-500/30 transition-all cursor-default overflow-hidden"
              >
                <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                  <Target className="w-12 h-12 text-white" />
                </div>
                <h4 className="text-sm font-bold text-zinc-200 mb-2 line-clamp-1">{mission.title}</h4>
                <div className="flex items-center gap-2">
                  <span className={clsx(
                    "text-[8px] font-black px-1.5 py-0.5 rounded uppercase tracking-tighter",
                    mission.energy_cost === "high_focus" ? "bg-indigo-500/20 text-indigo-400" :
                    mission.energy_cost === "neutral" ? "bg-emerald-500/20 text-emerald-400" :
                    "bg-rose-500/20 text-rose-400"
                  )}>
                    {mission.energy_cost.replace("_focus", "")}
                  </span>
                  <span className="text-[10px] text-zinc-500 font-medium">Prioridade {mission.base_priority}</span>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-full bg-[#1E1E1E] border border-dashed border-zinc-800 p-8 rounded-3xl text-center">
              <p className="text-zinc-500 text-sm italic">Nenhuma missão pendente para seu nível de energia.</p>
            </div>
          )}
        </div>
      </section>

      {/* Energy Selector */}
      <section className="mb-16">
        <h2 className="text-sm font-semibold text-zinc-400 uppercase tracking-widest mb-6 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
          Check-in de Energia
        </h2>
        
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <button 
            onClick={() => handleEnergySelect("high")}
            className={clsx(
              "group flex items-center p-4 rounded-3xl transition-all duration-300 border bg-[#1E1E1E]",
              energy === "high" ? "border-indigo-500/50 shadow-[0_0_30px_rgba(99,102,241,0.2)]" : "border-white/5 hover:border-indigo-500/30"
            )}
          >
            <div className={clsx("p-3 rounded-2xl mr-4 transition-colors", energy === "high" ? "bg-indigo-500/20 text-indigo-400" : "bg-[#2A2A2A] text-zinc-400 group-hover:text-indigo-400 group-hover:bg-indigo-500/10")}>
              <BatteryCharging className="w-6 h-6" />
            </div>
            <div className="text-left">
              <h3 className="font-semibold text-zinc-200">Alto Foco</h3>
              <p className="text-xs text-zinc-500">Medicado / Alta energia</p>
            </div>
          </button>

          <button 
            onClick={() => handleEnergySelect("neutral")}
            className={clsx(
              "group flex items-center p-4 rounded-3xl transition-all duration-300 border bg-[#1E1E1E]",
              energy === "neutral" ? "border-emerald-500/50 shadow-[0_0_30px_rgba(16,185,129,0.2)]" : "border-white/5 hover:border-emerald-500/30"
            )}
          >
            <div className={clsx("p-3 rounded-2xl mr-4 transition-colors", energy === "neutral" ? "bg-emerald-500/20 text-emerald-400" : "bg-[#2A2A2A] text-zinc-400 group-hover:text-emerald-400 group-hover:bg-emerald-500/10")}>
              <Battery className="w-6 h-6" />
            </div>
            <div className="text-left">
              <h3 className="font-semibold text-zinc-200">Foco Neutro</h3>
              <p className="text-xs text-zinc-500">Estável / Sessões comuns</p>
            </div>
          </button>

          <button 
            onClick={() => handleEnergySelect("low")}
            className={clsx(
              "group flex items-center p-4 rounded-3xl transition-all duration-300 border bg-[#1E1E1E]",
              energy === "low" ? "border-rose-500/50 shadow-[0_0_30px_rgba(244,63,94,0.15)]" : "border-white/5 hover:border-rose-500/30"
            )}
          >
            <div className={clsx("p-3 rounded-2xl mr-4 transition-colors", energy === "low" ? "bg-rose-500/20 text-rose-400" : "bg-[#2A2A2A] text-zinc-400 group-hover:text-rose-400 group-hover:bg-rose-500/10")}>
              <BatteryWarning className="w-6 h-6" />
            </div>
            <div className="text-left">
              <h3 className="font-semibold text-zinc-200">Baixo Foco</h3>
              <p className="text-xs text-zinc-500">Exausto / Tarefas fáceis</p>
            </div>
          </button>
        </div>
      </section>

      {/* Dashboard Grid */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Goals & Progress */}
        <div className="space-y-6">
          <div className="bg-[#1E1E1E] border border-white/5 rounded-3xl p-6">
            <div className="flex items-center gap-3 mb-6">
              <Target className="w-5 h-5 text-[#FFCC00]" />
              <h3 className="font-semibold text-zinc-100">Alvo Atual</h3>
            </div>
            <div className="bg-[#2A2A2A] p-4 rounded-2xl border border-white/5 flex items-center justify-between mb-4">
              <div>
                <p className="text-sm font-medium text-zinc-200">Perito Criminal - PCSP</p>
                <p className="text-xs text-zinc-500">Edital Ativo</p>
              </div>
              <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-md">Em Progresso</span>
            </div>
            
            <label className="w-full flex items-center justify-center cursor-pointer py-3 rounded-xl border border-dashed border-zinc-700 text-zinc-500 text-sm font-medium hover:border-indigo-500 hover:text-indigo-400 transition-colors">
              {isUploading ? "Lendo PDF... (Pode demorar)" : "+ Anexar Novo Edital (PDF)"}
              <input type="file" accept=".pdf" className="hidden" onChange={handleFileUpload} disabled={isUploading} />
            </label>
          </div>

          <div className="bg-[#1E1E1E] border border-white/5 rounded-3xl p-6">
            <div className="flex items-center gap-3 mb-6">
              <BarChart3 className="w-5 h-5 text-[#0F4780]" />
              <h3 className="font-semibold text-zinc-100">Radar de Evolução</h3>
            </div>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-zinc-400">Matemática (IME-USP)</span>
                  <span className="text-zinc-200">45%</span>
                </div>
                <div className="h-1.5 w-full bg-[#2A2A2A] rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 w-[45%] rounded-full"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-zinc-400">Edital PCSP</span>
                  <span className="text-zinc-200">12%</span>
                </div>
                <div className="h-1.5 w-full bg-[#2A2A2A] rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 w-[12%] rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* QConcursos Sync */}
        <div className="bg-[#1E1E1E] border border-white/5 rounded-3xl p-6 h-full flex flex-col">
          <div className="flex items-center gap-3 mb-6">
            <GraduationCap className="w-5 h-5 text-indigo-400" />
            <h3 className="font-semibold text-zinc-100 flex items-center gap-2">
              Sincronização QConcursos
              {isSyncingQc && <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>}
            </h3>
          </div>
          
          <div className="flex-1 flex flex-col justify-center items-center py-8">
            <div className="relative w-32 h-32 mb-6">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-[#2A2A2A]"
                  strokeWidth="3"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className="text-indigo-500"
                  strokeWidth="3"
                  strokeDasharray={`${qcStats.acertos}, 100`}
                  strokeLinecap="round"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-black text-white">{qcStats.acertos}%</span>
                <span className="text-[10px] text-zinc-500 font-medium uppercase tracking-wider">Acertos</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 w-full text-center">
              <div className="bg-[#2A2A2A] p-4 rounded-2xl">
                <p className="text-2xl font-bold text-white mb-1">{qcStats.questoes_hoje}</p>
                <p className="text-[10px] text-zinc-500 uppercase tracking-widest">Questões Hoje</p>
              </div>
              <div className="bg-[#2A2A2A] p-4 rounded-2xl">
                <p className="text-2xl font-bold text-white mb-1">{qcStats.disciplinas}</p>
                <p className="text-[10px] text-zinc-500 uppercase tracking-widest">Disciplinas</p>
              </div>
            </div>
          </div>
        </div>

      </section>

      {/* Modal de Seleção de Cargo */}
      {isSelectingCargo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300">
          <div className="bg-[#1E1E1E] border border-white/10 rounded-3xl p-8 max-w-lg w-full shadow-2xl relative">
            <h2 className="text-2xl font-black text-white mb-2">Selecione seu Cargo</h2>
            <p className="text-zinc-400 text-sm mb-6">Encontramos os seguintes cargos neste edital. Qual você deseja destrinchar?</p>
            
            <div className="max-h-60 overflow-y-auto pr-2 space-y-3 mb-6">
              {availableCargos.length > 0 ? (
                availableCargos.map((cargo, idx) => (
                  <button 
                    key={idx}
                    onClick={() => handleCargoSelect(cargo)}
                    disabled={isGeneratingTree}
                    className="w-full text-left p-4 rounded-2xl bg-[#2A2A2A] border border-white/5 hover:border-indigo-500 hover:bg-indigo-500/10 transition-colors group"
                  >
                    <span className="text-sm font-semibold text-zinc-200 group-hover:text-indigo-400">{cargo}</span>
                  </button>
                ))
              ) : (
                <div className="text-center p-6 text-zinc-500">Nenhum cargo identificado claramente.</div>
              )}
            </div>

            <div className="flex justify-end gap-3">
              <button 
                onClick={() => setIsSelectingCargo(false)}
                disabled={isGeneratingTree}
                className="px-6 py-2 rounded-xl text-sm font-bold text-zinc-400 hover:text-white transition-colors"
              >
                Cancelar
              </button>
            </div>
            
            {isGeneratingTree && (
              <div className="absolute inset-0 bg-[#1E1E1E]/95 backdrop-blur-md flex flex-col items-center justify-center rounded-3xl z-20 p-8 border border-indigo-500/20 shadow-[0_0_50px_rgba(99,102,241,0.1)]">
                <div className="relative mb-8">
                  <div className="w-20 h-20 border-4 border-indigo-500/10 border-t-indigo-500 rounded-full animate-spin" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-sm font-black text-white">{Math.floor(parsingProgress)}%</span>
                  </div>
                </div>
                
                <h3 className="text-xl font-bold text-white mb-2 animate-pulse">{parsingStatus}</h3>
                <p className="text-zinc-500 text-xs text-center mb-8">O Gemini está lendo cada linha do seu cargo para criar a trilha perfeita.</p>
                
                <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
                  <div 
                    className="h-full bg-indigo-500 shadow-[0_0_15px_rgba(99,102,241,0.5)] transition-all duration-300 ease-out" 
                    style={{ width: `${parsingProgress}%` }}
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
}
