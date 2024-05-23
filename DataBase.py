import sqlite3
import random


def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('Vetor.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS Vetor
                 (id INTEGER PRIMARY KEY,
                 descricao TEXT,
                 random_numbers TEXT)''')  # Storing numbers as comma-separated text

    # Commit changes and close connection
    conn.commit()
    conn.close()


def insert_database(descricao, numbers):
    # Connect to SQLite database
    conn = sqlite3.connect('Vetor.db')
    c = conn.cursor()

    # Insert data into the table
    c.execute("INSERT INTO Vetor (descricao, random_numbers) VALUES (?, ?)", (descricao, ', '.join(map(str, numbers))))

    # Commit changes and close connection
    conn.commit()
    conn.close()


def fetch_numbers_from_database():
    # Connect to SQLite database
    conn = sqlite3.connect('Vetor.db')
    c = conn.cursor()

    # Fetch the data from the table
    c.execute("SELECT random_numbers FROM Vetor")
    rows = c.fetchall()

    # Close connection
    conn.close()

    # Parse the comma-separated string of numbers into a list of integers
    numbers = []
    for row in rows:
        numbers.extend(map(int, row[0].split(', ')))

    # Split the list of numbers into three equal parts
    chunk_size = len(numbers) // 3
    chunks = [numbers[i:i+chunk_size] for i in range(0, len(numbers), chunk_size)]

    return chunks


def fisher_yates(n):
    # Generate n random numbers using Fisher-Yates algorithm
    numbers = list(range(1, n + 1))  # Create a list of numbers from 1 to n
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        numbers[i], numbers[j] = numbers[j], numbers[i]  # Swap the elements
    return numbers


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    merge_sort(left_half)
    merge_sort(right_half)

    i = j = k = 0

    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

    return arr
