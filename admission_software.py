import sqlite3
from  google import genai
client=genai.Client(api_key="YOUR_API_KEY_HERE")
conn = sqlite3.connect("aks_Univerity.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS admission_leads 
 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, interest TEXT, ai_suggested_branch TEXT)''')    
print("🎓 AKS University - Smart Admission Cell mein aapka swagat hai!\n")
student_name = input("student ka naam darj karein")
student_interest= input(f'{student_name} ko kis cheez me interest hai ? (jaise- computer, machine,kheti ):')
student_percentage=input("12th clss ka percentage darj karein jaise(75%):")
student_subject=input("12th class ka subject darj karo jaise(pcm,pcb.art):")
print("\n⚙️ AI aapke interest ke hisaab se ek chota sa test taiyar kar raha hai... Kripya intezar karein...\n")
test_prompt=f"student{student_name},ne 12th mein subject{student_subject} se padha hai aur us ka interest hai {student_interest} mein hai,uska basic knowledege check kar ne keliye 3 question banao(mcq)me taki course select kar ne assaani ho.question english me honey chaiye.STRICT WARNING:Answer ko display nhe kar na hai warna student cheating kar le ga."
test_response=client.models.generate_content(model="gemini-3.8-flash",contents=test_prompt)
ai_question=test_response.text.strip()
print("___" *50)
print(ai_question)
print("__"*50)
print("\nUpar diye gye sawalo ka jawab ek sath dejiye.")
student_answer=input("Apne jawab yahan likehin(1-A,2-B,3_C):")
print("\n🤖 AI aapke jawab check kar raha hai aur AKS University ke best courses dhoondh raha hai...\n")
eval_prompt=f"""student_name"{student_name} 12th subject:student _subject{student_subject} Interest:student_intereste{student_interest}
apne (Ai)student se ye sawal puche the:{ai_question}
student ne jawab diye hai :{student_answer}
Task:
1. Student ke jawabo ko check karo aur batao ki kitne sahi hain.
2. Uske performance, marks aur interest ke hisaab se AKS University Satna ki sabse best branch/degree suggest karo.
3. Jawab professional aur encouraging (Hinglish) bhasha mein hona chahiye.
"""
eval_response=client.models.generate_content(model="gemini-3.8-flash",contents=eval_prompt)
final_suggestion=eval_response.text.strip()
print("----" * 60)
print=(f"🏆 FINAL ADMISSION REPORT:\n\n{final_suggestion}")
print("----" * 60)
cursor.execute("INSERT INTO admission_leads (name, interest, ai_suggested_branch) VALUES (?, ?, ?)", 
               (student_name, f"Interest: {student_interest}, Marks: {student_percentage}", final_suggestion))

conn.commit()
conn.close()
print("\n✅ Success: Student ka test result aur AI ki salah tijori (Database) mein safely lock ho gayi!")


