import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Import CSV data using pandas
    df = pd.read_csv('surveyData.csv')
    # Get the number of columns
    # total_columns = df.shape[1]
    # print (total_columns)

    likert_scale_values = [1,2,3,4,5]
    # Print the values of each identified Likert scale column
    # Identify columns with Likert scale values
    likert_columns = []
    for col in df.columns[18:27]:
        try:
            numeric_values = pd.to_numeric(df[col], errors='coerce')
            if numeric_values[numeric_values.notna()].isin([1, 2, 3, 4, 5]).all():
                print(f"Likert scale column found: {col}")
                likert_columns.append(col)
        except ValueError as e:
            print(f"Error processing column {col}: {e}")

    # Check if there are Likert scale columns
    if not likert_columns:
        print("No Likert scale columns found.")
        return

    # Step 3: Create a DataFrame to store the counts
    likert_counts = pd.DataFrame(index=likert_scale_values, columns=likert_columns)

    # Step 4: Populate the DataFrame with counts
    for column in likert_columns:
        try:
            # Exclude non-numeric values before converting to integers
            numeric_values = pd.to_numeric(df[column], errors='coerce')
            numeric_values = numeric_values[numeric_values.notna()]  # Exclude NaN values
            numeric_values = numeric_values.astype('Int64')  # Convert to nullable integers
            likert_counts[column] = numeric_values.value_counts().reindex(likert_scale_values)
        except ValueError as e:
            print(f"Error processing column {column}: {e}")

    # Step 5: Plot the stacked bar chart
    plt.figure(figsize=(14, 8))
    likert_counts.T.plot(kind='bar', stacked=True, colormap='viridis')
    
    plt.title('Likert Scale Distribution for Each Question')
    plt.xlabel('Questions')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Likert Scale')
    plt.show()

if __name__ == "__main__":
    main()