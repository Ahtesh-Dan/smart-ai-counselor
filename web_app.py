import gradio as gr
from google import genai
import sqlite3
import logging
import os
logging.basicConfig(filename='admission_server.log',level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s')
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ai_admission_counselor(name, percentage, interest):
    logging.info(f"nayi lead ayyi-name{name},percentage{percentage},interest{interest}")
    conn = sqlite3.connect("aks_Univerity.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admission_leads 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, interest TEXT, ai_suggested_branch TEXT)''')
    
    prompt = f"""
    You are an expert AI Admission Counselor for AKS University, Satna.
    Student Name: {name}
    12th Percentage: {percentage}
    Interest/Field: {interest}
    
    Task:
    1. Student ke interest aur percentage ke hisaab se AKS University Satna ki sabse best branch/degree suggest karo.
    2. Unke career field ke baare mein 10  basic interview questions do taaki wo admission ke liye khud ko test kar sakein.
    3. Tone encouraging aur professional (Hinglish) honi chahiye.
    """
    
    try:
        response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
        ai_report = response.text.strip()
        
        cursor.execute("INSERT INTO admission_leads (name, interest, ai_suggested_branch) VALUES (?, ?, ?)", 
                       (name, f"Interest: {interest}, Marks: {percentage}", ai_report))
        conn.commit()
    except Exception as e:
        print(f"\n❌ ASLI ERROR YAHAN HAI: {e}\n")
        ai_report = "Kuch gadbad hai! Kripya Google Cloud terminal (black screen) par dekhein, wahan asli error print hua hai."
    finally:
        conn.close()
        
    return ai_report
def get_all_leads():
    conn=sqlite3.connect("aks_Univerity.db")
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT id, name, interest, ai_suggested_branch FROM admission_leads")
        data=cursor.fetchall()
    except:
          data=[]
    conn.close()
    return data
with gr.Blocks() as app:
    gr.Markdown("<center><h1>🎓 AKS University - Smart AI Admission Cell</h1></center>")
    
    with gr.Tab("📝 Student Form"):
        with gr.Row():
            name = gr.Textbox(label="Student ka Naam")
            percentage = gr.Textbox(label="12th Percentage (e.g. 75%)")
            interest = gr.Textbox(label="Interest (e.g. Computer, Mechanical)")
        
        submit_btn = gr.Button("Submit Application", variant="primary")
        output_report = gr.Textbox(label="🏆 AI Final Admission Report", lines=8)
        
        submit_btn.click(fn=ai_admission_counselor, inputs=[name, percentage, interest], outputs=output_report)
        
    with gr.Tab("🔒 Admin Panel (All Leads)"):
        gr.Markdown("### 📊 Database Records (AKS University Admission Cell)")
        refresh_btn = gr.Button("🔄 Load / Refresh Data")
        
        data_table = gr.Dataframe(headers=["ID", "Name", "Interest", "AI Suggested Branch"])
        
        refresh_btn.click(fn=get_all_leads, inputs=[], outputs=data_table)

app.launch(server_name="0.0.0.0",server_port=7860)

