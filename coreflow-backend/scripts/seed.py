import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal, engine
from app.models.user import Profile, EnergyState
from app.models.mission import Mission, MissionType, MissionSource
import app.models.taxonomy

def seed_db():
    db = SessionLocal()
    
    # Check if a profile exists
    profile = db.query(Profile).first()
    if not profile:
        profile = Profile(current_battery=EnergyState.neutral, xp_points=0)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        print(f"Created Profile: {profile.id}")

    # Check if missions exist
    existing_missions = db.query(Mission).count()
    if existing_missions == 0:
        missions_data = [
            # High Energy Missions (Theory, high cognitive load)
            Mission(user_id=profile.id, title="Estatística Descritiva: Variância e Desvio Padrão", type=MissionType.theory, source=MissionSource.jupiterweb, energy_cost=EnergyState.high_focus, base_priority=10),
            Mission(user_id=profile.id, title="Resolver Simulados PCSP Avançado", type=MissionType.exercise, source=MissionSource.qconcursos, energy_cost=EnergyState.high_focus, base_priority=9),
            Mission(user_id=profile.id, title="Arquitetura de Computadores: Pipeline", type=MissionType.theory, source=MissionSource.manual, energy_cost=EnergyState.high_focus, base_priority=8),
            
            # Neutral Energy Missions (Balanced, medium load)
            Mission(user_id=profile.id, title="Revisão Espaçada: Redes TCP/IP", type=MissionType.flashcard, source=MissionSource.manual, energy_cost=EnergyState.neutral, base_priority=7),
            Mission(user_id=profile.id, title="15 Questões de Banco de Dados Média", type=MissionType.exercise, source=MissionSource.qconcursos, energy_cost=EnergyState.neutral, base_priority=6),
            Mission(user_id=profile.id, title="Ler artigo sobre Segurança da Informação", type=MissionType.routine, source=MissionSource.manual, energy_cost=EnergyState.neutral, base_priority=5),
            
            # Low Energy Missions (Easy, recovery)
            Mission(user_id=profile.id, title="Organizar mesa de estudos e planner", type=MissionType.routine, source=MissionSource.manual, energy_cost=EnergyState.low_focus, base_priority=4),
            Mission(user_id=profile.id, title="Flashcards Rápidos - Idioma", type=MissionType.flashcard, source=MissionSource.manual, energy_cost=EnergyState.low_focus, base_priority=3),
            Mission(user_id=profile.id, title="Assistir vídeo de resolução de exercícios curta", type=MissionType.theory, source=MissionSource.manual, energy_cost=EnergyState.low_focus, base_priority=2),
        ]
        
        db.bulk_save_objects(missions_data)
        db.commit()
        print("Missions Seeded Successfully!")
    else:
        print("Database already seeded with missions.")
        
    db.close()

if __name__ == "__main__":
    seed_db()
