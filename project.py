import os
import pandas as pd
import matplotlib.pyplot as plt
import gradio as gr


def analyze_feedback_from_df(df):

   
    required = ['Overall', 'Teaching', 'Content', 'Interaction']
    missing = [c for c in required if c not in df.columns]

    if missing:
        summary = f"⚠ Missing expected columns: {missing}\nAvailable: {list(df.columns)}"
        return summary, None, None, None


    summary = "Preview of Data:\n"
    summary += str(df.head()) + "\n\nSummary Stats:\n"
    summary += str(df.describe()) + "\n"


    plt.figure()
    plt.hist(df['Overall'])
    plt.title("Overall Satisfaction Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of Students")
    hist_path = "hist.png"
    plt.savefig(hist_path)
    plt.close()

    mean_scores = df[['Teaching', 'Content', 'Interaction']].mean()
    plt.figure()
    mean_scores.plot(kind="bar")
    plt.title("Average Rating by Category")
    plt.ylabel("Average Rating")
    bar_path = "bar.png"
    plt.savefig(bar_path)
    plt.close()

  
    plt.figure()
    mean_scores.plot(kind="pie", autopct='%1.1f%%')
    plt.title("Category-wise Satisfaction Share")
    plt.ylabel("")
    pie_path = "pie.png"
    plt.savefig(pie_path)
    plt.close()

    return summary, hist_path, bar_path, pie_path




print("Current folder:", os.getcwd())
print("Files here:", os.listdir())

candidates = [f for f in os.listdir() if f.startswith("student_feedback") and f.endswith(".csv")]
if candidates:
    csv_path = os.path.join(os.getcwd(), candidates[0])
    print(f"Auto-selected CSV: {csv_path}")
else:
    csv_path = r"F:\new project\student_feedback.csv"

df = pd.read_csv(csv_path)
print("CSV loaded successfully\n")
print(df.head())



def analyze_feedback(file):
    df_uploaded = pd.read_csv(file.name)
    return analyze_feedback_from_df(df_uploaded)


# ---------- GRADIO UI ----------
with gr.Blocks(title="Student Feedback Survey Analysis") as app:

    gr.Markdown("## 📊 Student Feedback Survey Analysis\nUpload your CSV to see trends & charts.")

    file_input = gr.File(label="Upload student_feedback.csv")
    summary_out = gr.Textbox(label="Dataset Summary", lines=12)
    img1 = gr.Image(label="Overall Satisfaction Histogram")
    img2 = gr.Image(label="Category-wise Bar Chart")
    img3 = gr.Image(label="Satisfaction Share Pie Chart")

    analyze_btn = gr.Button("Analyze Feedback")

    analyze_btn.click(
        fn=analyze_feedback,
        inputs=file_input,
        outputs=[summary_out, img1, img2, img3]
    )

app.launch(share=True)
