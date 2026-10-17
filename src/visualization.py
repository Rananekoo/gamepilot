import matplotlib.pyplot as plt


def show_character_chart(players):
    character_counts = {}

    for row in players:
        character = row['character']

        if character in character_counts:
            character_counts[character] += 1
        else:
            character_counts[character] = 1

    characters = list(character_counts.keys())
    counts = list(character_counts.values())

    plt.figure(figsize=(8, 5))
    plt.bar(characters, counts)

    plt.title("Character Popularity")
    plt.xlabel("Character")
    plt.ylabel("Number of Players")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_activity_chart(players):
    activity_counts = {
        "Low Activity": 0,
        "Medium Activity": 0,
        "High Activity": 0
    }

    for row in players:
        days = int(row['days_played'])

        if days < 7:
            activity_counts["Low Activity"] += 1
        elif days < 20:
            activity_counts["Medium Activity"] += 1
        else:
            activity_counts["High Activity"] += 1

    levels = list(activity_counts.keys())
    counts = list(activity_counts.values())

    plt.figure(figsize=(7, 5))
    plt.bar(levels, counts)

    plt.title("Player Activity")
    plt.xlabel("Activity Level")
    plt.ylabel("Number of Players")

    plt.tight_layout()
    plt.show()


def show_payment_chart(players):
    paying_players = 0
    non_paying_players = 0

    for row in players:
        if int(row['paid']) == 1:
            paying_players += 1
        else:
            non_paying_players += 1

    labels = ["Paying Players", "Non-paying Players"]
    counts = [paying_players, non_paying_players]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, counts)

    plt.title("Player Payment Status")
    plt.xlabel("Payment Status")
    plt.ylabel("Number of Players")

    plt.tight_layout()
    plt.show()