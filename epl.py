import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("epl_2018_2019.csv")

# Rename columns
df.rename(columns={"Nat": "Nationality", "Pos": "Position"}, inplace=True)

# Rename Values
df["Position"] = df["Position"].replace({
    "G": "Goalkeeper",
    "D": "Defender",
    "M": "Midfielder",
    "F": "Forward"
})

# Remove rows where "Name" is missing
df.dropna(subset=["Name"], inplace=True)

# Count International players players
international_players = df[df["Nationality"] != "ENG"]
num_international_players = len(international_players)

# Count English (domestic) players
num_domestic = len(df) - num_international_players

# Data for pie chart
labels = ["International Players", "Domestic Players"]
sizes = [num_international_players, num_domestic]
colors = ["skyblue", "lightcoral"]

# Create pie chart
plt.figure(figsize=(7, 7))
plt.pie(
    sizes, labels=labels, colors=colors, autopct=lambda p: f"{p:.1f}%\n({int(p*sum(sizes)/100)})",
    startangle=140, wedgeprops={"edgecolor": "black"}
)
plt.title("Distribution of International vs. Domestic Players in EPL (2018-19)")
plt.show()


# Total players
total_players = len(df)

# Percentage of International players players
percentage_non_english = len(international_players) / total_players * 100
print(f"International Players: {len(international_players)} ({percentage_non_english:.2f}%)")


# Count frequency of each nationality (excluding England)
top_nationalities = international_players["Nationality"].value_counts().head(10)

# Plot
plt.figure(figsize=(10, 5))
top_nationalities.plot(kind="bar", color="blue")
plt.xlabel("Nationality")
plt.ylabel("Number of Players")
plt.title("Top 10 Most Common Nationalities in EPL (2018-19)")
plt.show()

# Count International players players per club
international_count_per_club = international_players["Club"].value_counts()

# Plot top 10 clubs with most International players
international_count_per_club.head(10).plot(kind="barh", color="green", figsize=(10, 5))
plt.xlabel("Number of International Players")
plt.ylabel("Club")
plt.title("Top 10 EPL Clubs with Most International Players (2018-19)")
plt.gca().invert_yaxis()
plt.show()

international_players_by_position = international_players["Position"].value_counts()

# Print the counts
print(international_players_by_position)

# Plot the data
plt.figure(figsize=(8, 5))
international_players_by_position.plot(kind="bar", color=["red", "blue", "green", "purple"])
plt.xlabel("Position")
plt.ylabel("Number of International Players")
plt.title("Number of International Players per Position in EPL (2018-19)")
plt.xticks(rotation=0)  
plt.show()










