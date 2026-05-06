-- Extensão para geração de UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tipos Enum para categorização e fluxo de estado
CREATE TYPE energy_state AS ENUM ('high_focus', 'low_focus', 'neutral');
CREATE TYPE mission_type AS ENUM ('theory', 'exercise', 'flashcard', 'routine');
CREATE TYPE mission_source AS ENUM ('jupiterweb', 'qconcursos', 'manual');

-- ==============================================================================
-- 1. PROFILES (Extensão do auth.users do Supabase com Gamificação/Foco)
-- ==============================================================================
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    current_battery energy_state DEFAULT 'neutral',
    xp_points INTEGER DEFAULT 0,
    frozen_mode BOOLEAN DEFAULT FALSE, -- Ativação do "Modo Evento" (pausa estratégica de métricas)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 2. MOTOR DE INTERSEÇÃO E TAGGING UNIVERSAL
-- ==============================================================================
CREATE TABLE public.tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL, -- Ex: '#probabilidade', '#redes-tcp-ip'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Hierarquia do Conhecimento: Disciplina > Assunto > Tópico
CREATE TABLE public.disciplines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) -- Ex: 'college', 'contest', 'certifications'
);

CREATE TABLE public.subjects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    discipline_id UUID REFERENCES public.disciplines(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE public.topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id UUID REFERENCES public.subjects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    knowledge_level INTEGER DEFAULT 0, -- 0 a 100 (Barra de progresso de proficiência)
    is_completed BOOLEAN DEFAULT FALSE
);

-- Interseção: Tópicos <-> Tags Universais
CREATE TABLE public.topic_tags (
    topic_id UUID REFERENCES public.topics(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES public.tags(id) ON DELETE CASCADE,
    PRIMARY KEY (topic_id, tag_id)
);

-- Mapeamento de Editais Ativos
CREATE TABLE public.editais (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'active'
);

CREATE TABLE public.edital_topics (
    edital_id UUID REFERENCES public.editais(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES public.topics(id) ON DELETE CASCADE,
    PRIMARY KEY (edital_id, topic_id)
);

-- ==============================================================================
-- 3. FILA DE EXECUÇÃO BASEADA EM ESTADO (ADHD-Aware Engine)
-- ==============================================================================
CREATE TABLE public.missions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    source mission_source DEFAULT 'manual',
    type mission_type,
    energy_cost energy_state NOT NULL, -- Crucial para o filtro de bateria na Home
    status VARCHAR(50) DEFAULT 'pending', -- 'pending' ou 'completed' (roleta/catraca contínua)
    base_priority INTEGER DEFAULT 0, -- Auxilia o algoritmo dinâmico
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Interseção: Missões <-> Tags Universais (O gatilho de atualização cruzada)
CREATE TABLE public.mission_tags (
    mission_id UUID REFERENCES public.missions(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES public.tags(id) ON DELETE CASCADE,
    PRIMARY KEY (mission_id, tag_id)
);

-- ==============================================================================
-- 4. HÁBITOS FLUTUANTES (Ausência de Atraso Punitivo)
-- ==============================================================================
CREATE TABLE public.habits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    target_frequency INTEGER NOT NULL, -- Quantidade alvo (Ex: 4x)
    frequency_period_days INTEGER DEFAULT 7, -- Na janela de X dias (Ex: por semana)
    energy_cost energy_state NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE public.habit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    habit_id UUID REFERENCES public.habits(id) ON DELETE CASCADE,
    executed_at TIMESTAMPTZ DEFAULT NOW(),
    battery_state_at_execution energy_state -- Para recompensar esforço em dias de "Baixo Foco" (XP extra)
);

-- ==============================================================================
-- 5. MOTOR DE SCRAPING E AUTOMAÇÃO (QConcursos / JúpiterWeb)
-- ==============================================================================
CREATE TABLE public.qconcursos_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    discipline_id UUID REFERENCES public.disciplines(id) ON DELETE CASCADE,
    questions_solved INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);
