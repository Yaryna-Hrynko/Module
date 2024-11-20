"""Взаємодія з CSV-файлом:
Завантаження даних про книги із CSV-файлу. Дані повинні містити такі колонки:
Назва книги.
Автор.
Рік видання.
Жанр.
yaer примірників.
Збереження оновлених даних у CSV-файл.
Основні операції з книгами:
Додавання нової книги.
Редагування інформації про книгу.
Видалення книги за назвою.
Виведення списку книг у вигляді таблиці.
Обчислення загальної кількості книг у бібліотеці.
Виведення списку найпопулярніших жанрів.
Пошук книг певного автора або книг, виданих у конкретному році.
Візуалізація:
Побудова кругової діаграми розподілу книг за жанрами.
Побудова гістограми кількості книг за роками видання."""
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file):
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        print("Файл не знайдено. Створюємо новий.")
        return pd.DataFrame(columns=["Назва книги", "Автор", "Рік видання", "Жанр", "Кількість примірників"])


def save_data(data, file):
    data.to_csv(file, index=False)
    print("Дані збережено.")


def add_book(data):
    name = input("Введіть назву книги: ")
    author = input("Введіть автора: ")
    year = int(input("Введіть рік видання: "))
    genre = input("Введіть жанр: ")
    count = int(input("Введіть кількість примірників: "))
    new_row = {"Назва книги": name, "Автор": author, "Рік видання": year, "Жанр": genre, "Кількість примірників": count}
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    print("Книгу додано.")
    return data

def edit_book(data):
    name = input("Введіть назву книги для редагування: ")
    if name in data["Назва книги"].values:
        index = data[data["Назва книги"] == name].index[0]
        print(f"Поточні дані:\n{data.loc[index]}")
        data.at[index, "Автор"] = input("Новий автор (Enter - залишити без змін): ") or data.at[index, "Автор"]
        data.at[index, "Рік видання"] = input("Новий рік (Enter - залишити без змін): ") or data.at[index, "Рік видання"]
        data.at[index, "Жанр"] = input("Новий жанр (Enter - залишити без змін): ") or data.at[index, "Жанр"]
        data.at[index, "Кількість примірників"] = input("Нова кількість (Enter - залишити без змін): ") or data.at[index, "Кількість примірників"]
        print("Дані оновлено.")
    else:
        print("Книгу не знайдено.")
    return data

def delete_book(data):
    name = input("Введіть назву книги для видалення: ")
    if name in data["Назва книги"].values:
        data = data[data["Назва книги"] != name]
        print("Книгу видалено.")
    else:
        print("Книгу не знайдено.")
    return data


def display_books(data):
    if data.empty:
        print("Список книг порожній.")
    else:
        print(data.to_string(index=False))


def total_books(data):
    total = data["Кількість примірників"].astype(int).sum()
    print(f"Загальна кількість книг: {total}")

#Виведення списку найпопулярніших жанрів.
def popular_genres(data):
    genre_counts = data["Жанр"].value_counts()
    print("Найпопулярніші жанри:")
    print(genre_counts)
#Пошук книг певного автора або книг, виданих у конкретному році.
def search_books(data):
    author = input("Введіть автора (Enter - пропустити): ")
    year = input("Введіть рік видання (Enter - пропустити): ")
    results = data
    if author:
        results = results[results["Автор"].str.contains(author, case=False)]
    if year:
        results = results[results["Рік видання"] == int(year)]
    if results.empty:
        print("Книг не знайдено.")
    else:
        print("Результати пошуку:")
        print(results.to_string(index=False))

#Побудова кругової діаграми розподілу книг за жанрами.
def plot_genre_distribution(data):
    genre_counts = data["Жанр"].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Розподіл книг за жанрами")
    plt.axis("equal")
    plt.show()

#Побудова гістограми кількості книг за роками видання.
def plot_year_histogram(data):
    plt.figure(figsize=(8, 6))
    plt.hist(data["Рік видання"], bins=10, color='green', alpha=0.7, edgecolor='black')
    plt.title("Гістограма за роками видання")
    plt.xlabel("Рік видання")
    plt.ylabel("Кількість книг")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()



def main():
    file = "data.csv"
    data = load_data(file)

    while True:
        print("1. Додати книгу ")
        print("2. Редагувати книгу")
        print("3. Видалити книгу")
        print("4. Показати всі книги")
        print("5. Вивести загальну кількість книг")
        print("6. Вивести список нйпопулярніших жанрів")
        print("7. Пошук книги за автором або роком")
        print("8. Побудова кругової діаграми розподілу книг за жанрами")
        print("9.Побудова гістограми кількості книг за роками видання.")
        print("11. Зберегти та вийти")
        choice = input("Оберіть дію: ")

        if choice == "1":
            data = add_book(data)
        elif choice == "2":
            data = edit_book(data)
        elif choice == "3":
            data = delete_book(data)
        elif choice == "4":
            display_books(data)
        elif choice == "5":
            total_books(data)
        elif choice == "6":
            popular_genres(data)
        elif choice == "7":
            search_books(data)
        elif choice == "8":
            plot_genre_distribution(data)
        elif choice == "9":
            plot_year_histogram(data)
        elif choice == "0":
            save_data(data, file)
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()