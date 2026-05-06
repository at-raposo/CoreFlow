from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.qc_scraper import fetch_qconcursos_stats
import logging

logger = logging.getLogger(__name__)

def run_daily_scraping():
    logger.info("Running daily background scraping jobs...")
    try:
        stats = fetch_qconcursos_stats()
        logger.info(f"QConcursos Sync successful: {stats}")
        # In a complete implementation, we would save this to a timeseries table
        # to plot the user's progress over time on the dashboard.
    except Exception as e:
        logger.error(f"Error in background scraping: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Run everyday at 3:00 AM
    trigger = CronTrigger(hour=3, minute=0)
    scheduler.add_job(run_daily_scraping, trigger=trigger)
    
    scheduler.start()
    logger.info("Background Scheduler started.")
