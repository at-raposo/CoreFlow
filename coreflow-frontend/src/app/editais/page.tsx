"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { FileText, ChevronRight, Loader2, Trash2 } from "lucide-react";

export default function EditaisPage() {
  const [editais, setEditais] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchEditais = () => {
    fetch("http://localhost:8000/api/editais/")
      .then((res) => res.json())
      .then((data) => {
        setEditais(data);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchEditais();
  }, []);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm("Tem certeza que deseja apagar este edital e todo o seu progresso?")) return;
    
    try {
      const res = await fetch(`http://localhost:8000/api/editais/${id}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        fetchEditais();
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col h-full overflow-y-auto bg-[#121212] p-6 lg:p-10 hide-scrollbar pb-32">
      <div className="max-w-4xl mx-auto w-full">
        <div className="mb-10">
          <h1 className="text-3xl font-black text-white mb-2 flex items-center gap-3">
            <FileText className="w-8 h-8 text-indigo-500" />
            Meus Editais
          </h1>
          <p className="text-zinc-500">Visualize as árvores de habilidade dos seus concursos ativos.</p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {editais.map((edital) => (
              <div 
                key={edital.id}
                onClick={() => router.push(`/editais/${edital.id}`)}
                className="bg-[#1E1E1E] p-6 rounded-3xl border border-white/5 cursor-pointer hover:border-indigo-500/50 transition-all group"
              >
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="text-xl font-bold text-white mb-1 group-hover:text-indigo-400 transition-colors">{edital.title}</h3>
                    <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-md uppercase tracking-wider">{edital.status}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button 
                      onClick={(e) => handleDelete(e, edital.id)}
                      className="p-2 text-zinc-600 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                      title="Apagar edital"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                    <ChevronRight className="text-zinc-600 group-hover:text-indigo-400" />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-xs text-zinc-400 font-medium">
                    <span>Progresso</span>
                    <span className="text-white">{edital.progress}%</span>
                  </div>
                  <div className="w-full bg-[#2A2A2A] rounded-full h-2">
                    <div 
                      className="bg-indigo-500 h-2 rounded-full transition-all duration-1000" 
                      style={{ width: `${edital.progress}%` }}
                    />
                  </div>
                  <p className="text-xs text-zinc-500 text-right">{edital.total_topics} tópicos mapeados</p>
                </div>
              </div>
            ))}
            
            {editais.length === 0 && (
              <div className="col-span-full bg-[#1E1E1E] p-10 rounded-3xl border border-dashed border-zinc-700 text-center">
                <p className="text-zinc-500 mb-4">Nenhum edital cadastrado.</p>
                <button 
                  onClick={() => router.push('/qg')}
                  className="bg-white text-black px-6 py-2 rounded-xl text-sm font-bold hover:bg-zinc-200"
                >
                  Ir para o QG anexar PDF
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
