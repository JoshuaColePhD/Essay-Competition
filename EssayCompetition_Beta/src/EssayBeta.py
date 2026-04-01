# %% import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# %% import data
df = pd.read_csv('EssayCompetition_Beta/data/beta_data.csv')

# %% inspect data
df.dtypes
print(df.info())

# %% clean data
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
print(df.dtypes)
print(df.head())

# %%
# 1. DEFINE COLUMN NAMES (MUST MATCH YOUR HEADERS EXACTLY)
likert_cols = [
    '1. Content & Ideas:\nThe essay clearly answers the prompt with strong, original ideas. Shows thought, insight, or creativity.5 = Excellent, 4 = Strong, 3 = Satisfactory, 2 = Developing, 1 = Needs Improvement',
    '2. Organization & Flow\n\nThe essay has a clear beginning, middle, and end. Transitions are smooth and ideas are easy to follow.',
    '3. Voice & Style\n\nThe writing sounds confident and engaging. The tone fits the topic and feels authentic.',
    '4. Evidence & Support\n\nThe essay uses examples, facts, or quotes that effectively support the main points.',
    '5. Conventions (Grammar & Mechanics)\n\nThe writing is easy to read with few grammar, spelling, or punctuation mistakes.'
]

agg_cols = ['Total Points'] + likert_cols

# 2. DATA CLEANING AND TYPE CONVERSION
# Ensure all score columns are treated as numbers and drop incomplete rows
for col in agg_cols:
    # 'coerce' turns non-numeric values (like text or errors) into NaN
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows where the score data is missing
df.dropna(subset=['Total Points'], inplace=True)


# 3. GROUP AND AGGREGATE (THE CORE STEP)
# This performs the equivalent of hundreds of AVERAGEIF statements
final_averages_df = df.groupby('Essay ID')[agg_cols].mean().reset_index()


# 4. CLEAN UP COLUMN NAMES
# Create readable names for the output table
new_col_names = {
    'Total Points': 'Avg_Total_Points_Sum',
    likert_cols[0]: 'Avg_Content_Ideas',
    likert_cols[1]: 'Avg_Organization_Flow',
    likert_cols[2]: 'Avg_Voice_Style',
    likert_cols[3]: 'Avg_Evidence_Support',
    likert_cols[4]: 'Avg_Conventions_Grammar'
}
final_averages_df.rename(columns=new_col_names, inplace=True)


# 5. CALCULATE FINAL 5-POINT CONSENSUS SCORE
# Assuming the max score is 5 for each of the 5 criteria (Max Total = 25)
final_averages_df['Final_Overall_Score_5_Point'] = final_averages_df['Avg_Total_Points_Sum'] / 5


# 6. OUTPUT RESULTS
print("--- Final Averaging Results (First 5 Rows) ---")
print(final_averages_df.head())

# Save the results to a new CSV file
final_averages_df.to_csv('EssayCompetition_Beta/data/essay_final_averages.csv', index=False)

# %% rank
df_ranked = final_averages_df.sort_values('Final_Overall_Score_5_Point', ascending=False)

# %% inspect ranked
print(df_ranked.head())

# %% visualize ranking
df_top_essays = df_ranked.sort_values(by='Final_Overall_Score_5_Point', ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x='Final_Overall_Score_5_Point', y='Essay ID', data=df_top_essays, palette='viridis')
plt.title('Top Essays by Final Overall Score (5-Point Scale)')
plt.xlabel('Final Overall Score (5-Point Scale)')
plt.ylabel('Essay ID')
plt.xlim(0, 5)
plt.tight_layout()
plt.show()