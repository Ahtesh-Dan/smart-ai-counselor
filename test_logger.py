import logging

logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("System successfully start ho gaya hai.")
logging.warning("Dhyan dein: Server ki memory thodi kam ho rahi hai.")
logging.error("CRITICAL: Database se connection toot gaya!")

print("Chief, logs chupchaap 'app.log' file mein save ho gaye hain!")
