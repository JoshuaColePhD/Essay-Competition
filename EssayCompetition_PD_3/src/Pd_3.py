# %% import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% import data
df = pd.read_csv('EssayCompetition_PD_3/data/E_Essay_Scores.csv')

# %% inspect data
print(df.info())
print(df.head())
print(df.describe())

# %% clean data
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
print(df.dtypes)
print(df.head())

# %% RENAME COLUMNS TO CLEAN NAMES
rename_map = {
    "Email Address": "Email",
    "Essay ID": "Essay_ID",
    "1. Content & Ideas:\nThe essay clearly answers the prompt with strong, original ideas. Shows thought, insight, or creativity.5 = Excellent, 4 = Strong, 3 = Satisfactory, 2 = Developing, 1 = Needs Improvement": "Content_Ideas",
    "2. Organization & Flow\n\nThe essay has a clear beginning, middle, and end. Transitions are smooth and ideas are easy to follow.": "Organization_Flow",
    "3. Voice & Style\n\nThe writing sounds confident and engaging. The tone fits the topic and feels authentic.": "Voice_Style",
    "4. Evidence & Support\n\nThe essay uses examples, facts, or quotes that effectively support the main points.": "Evidence_Support",
    "5. Conventions (Grammar & Mechanics)\n\nThe writing is easy to read with few grammar, spelling, or punctuation mistakes.": "Conventions",
    "How much AI-generated content do you think is in this paper?": "AI_Content_Level"
}

df = df.rename(columns=rename_map)

# %% DEFINE RUBRIC COLUMNS (CLEAN NAMES)
likert_cols = [
    "Content_Ideas",
    "Organization_Flow",
    "Voice_Style",
    "Evidence_Support",
    "Conventions"
]

# %% CREATE TOTAL POINTS (NOW IT ACTUALLY EXISTS)
df["Total_Points"] = df[likert_cols].sum(axis=1)

# Make sure all scoring columns are numeric
score_cols = likert_cols + ["Total_Points"]
df[score_cols] = df[score_cols].apply(pd.to_numeric, errors="coerce")

# Drop rows where total points is missing
df = df.dropna(subset=["Total_Points"])

# %% GROUP AND AGGREGATE BY ESSAY
agg_cols = ["Total_Points"] + likert_cols

final_averages_df = (
    df
    .groupby("Essay_ID")[agg_cols]
    .mean()
    .reset_index()
)

# %% RENAME AGGREGATED COLUMNS TO CLEAR NAMES
new_col_names = {
    "Total_Points": "Avg_Total_Points_Sum",
    "Content_Ideas": "Avg_Content_Ideas",
    "Organization_Flow": "Avg_Organization_Flow",
    "Voice_Style": "Avg_Voice_Style",
    "Evidence_Support": "Avg_Evidence_Support",
    "Conventions": "Avg_Conventions_Grammar"
}
final_averages_df = final_averages_df.rename(columns=new_col_names)

# %% CALCULATE FINAL 5-POINT CONSENSUS SCORE
# Max Total_Points per rater = 25 (5 criteria * 5 points),
# so dividing the average total by 5 gives a 1–5 scale.
final_averages_df["Final_Overall_Score_5_Point"] = (
    final_averages_df["Avg_Total_Points_Sum"] / 5
)

# %% OUTPUT RESULTS
print("--- Final Averaging Results (First 5 Rows) ---")
print(final_averages_df.head())

# Save the results to a new CSV file
final_averages_df.to_csv(
    'EssayCompetition_Beta/data/essay_final_averages.csv',
    index=False
)

# %% RANK ESSAYS
df_ranked = final_averages_df.sort_values(
    "Final_Overall_Score_5_Point",
    ascending=False
)

print("--- Top Ranked Essays ---")
print(df_ranked.head())

# %% VISUALIZE TOP 3 RANKED ESSAYS

# 1. Sort and select Top 3
df_top3 = df_ranked.sort_values(
    by="Final_Overall_Score_5_Point",
    ascending=False
).head(3).copy()

plt.figure(figsize=(10, 6))

# 2. Create horizontal barplot
ax = sns.barplot(
    data=df_top3,
    x="Final_Overall_Score_5_Point",
    y="Essay_ID",
    palette="viridis"
)

# 3. Add annotations to each bar
for i, bar in enumerate(ax.patches):
    essay_id = df_top3.iloc[i]["Essay_ID"]
    score_value = bar.get_width()
    text = f"{essay_id} ({score_value:.2f})"

    ax.text(
        x=score_value + 0.05,
        y=bar.get_y() + bar.get_height() / 2,
        s=text,
        va="center",
        fontsize=10,
        color="black"
    )

# 4. Styling
plt.title("Top 3 Essays Ranked by Final Overall Score (5-Point Scale)", fontsize=14)
plt.xlabel("Final Overall Score (5-Point Scale)", fontsize=12)
plt.ylabel("Essay ID", fontsize=12)
plt.xlim(0, 5)
plt.grid(axis="x", linestyle="--", alpha=0.6)
plt.tight_layout()

# 5. Show plot
plt.show()

# %% CLASS AVERAGE
class_average = final_averages_df["Final_Overall_Score_5_Point"].mean()
print(f"Class Average Final Overall Score (5-Point Scale): {class_average:.2f}")

# %% Visualize Top 3 Ranked Essays
# %% RANK & SUMMARY METRICS

# Sort essays from highest to lowest final score
df_ranked = final_averages_df.sort_values(
    "Final_Overall_Score_5_Point",
    ascending=False
)

# 1️⃣ Top 3 of Class
top3 = df_ranked.head(3).copy()
print("\n=== Top 3 Essays in the Class ===")
print(top3[["Essay_ID", "Final_Overall_Score_5_Point"]])

# 2️⃣ Class Average
class_average = final_averages_df["Final_Overall_Score_5_Point"].mean()
print(f"\n=== Class Average (5-Point Scale) ===\n{class_average:.2f}")

# 3️⃣ Top Overall (Single Best Essay)
top_overall = df_ranked.iloc[0]
print("\n=== Top Overall Essay ===")
print(f"Essay ID: {top_overall['Essay_ID']}")
print(f"Final Overall Score (5-Point Scale): {top_overall['Final_Overall_Score_5_Point']:.2f}")

# %% VISUALIZE DISTRIBUTION OF AI RATINGS

plt.figure(figsize=(8, 5))

ax = sns.countplot(
    data=df,
    x="AI_Content_Level"
)

plt.title("Distribution of AI-Generated Content Judgments", fontsize=14)
plt.xlabel("Perceived AI Level (1 = none, 5 = mostly AI)", fontsize=12)
plt.ylabel("Number of Ratings", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()