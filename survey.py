import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Import CSV data using pandas
    df = pd.read_csv('surveyData.csv')
    
    # Specify the Likert scale columns (Q1 to Q10)
    likert_columns = [f'Q{i}' for i in range(1, 11)]

   # Output mean and standard deviation for each column
    for column in likert_columns:
        try:
            # Exclude non-numeric values before calculations
            numeric_values = pd.to_numeric(df[column], errors='coerce')
            numeric_values = numeric_values[numeric_values.notna()]  # Exclude NaN values
            
            # Calculate mean and standard deviation
            column_mean = numeric_values.mean()
            column_std = numeric_values.std()

            print(f"Column: {column}, Mean: {column_mean}, Std Dev: {column_std}")
        except ValueError as e:
            print(f"Error processing column {column}: {e}")

    likert_scale_values = [1, 2, 3, 4, 5]
    likert_columns = []

    # Identify Likert scale columns
    for col in df.columns[17:27]:
        try:
            numeric_values = pd.to_numeric(df[col], errors='coerce')
            if numeric_values[numeric_values.notna()].isin(likert_scale_values).all():
                # print(f"Likert scale column found: {col}")
                likert_columns.append(col)
        except ValueError as e:
            print(f"Error processing column {col}: {e}")

    if not likert_columns:
        print("No Likert scale columns found.")
        return
    
    # Create a DataFrame to store the counts
    likert_counts = pd.DataFrame(index=likert_scale_values, columns=likert_columns)

    # Populate the DataFrame with counts
    for column in likert_columns:
        try:
            # Exclude non-numeric values before converting to integers
            numeric_values = pd.to_numeric(df[column], errors='coerce')
            numeric_values = numeric_values[numeric_values.notna()]  # Exclude NaN values
            numeric_values = numeric_values.astype('Int64')  # Convert to nullable integers
            likert_counts[column] = numeric_values.value_counts().reindex(likert_scale_values)
        except ValueError as e:
            print(f"Error processing column {column}: {e}")

    # Plot the stacked bar chart
    plt.figure(figsize=(14, 8))
    likert_counts.T.plot(kind='bar', stacked=True, colormap='viridis')

    plt.title('SUS Likert Distribution')
    plt.xlabel('Questions')
    plt.ylabel('Count')

    # Handle NaN values in the legend
    plt.legend(title='Likert Scale', loc='upper left', bbox_to_anchor=(1, 1))

    plt.xticks(rotation=45, ha='right')
    plt.show()

if __name__ == "__main__":
    main()
