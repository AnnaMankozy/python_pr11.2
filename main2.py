import pandas as pd
import matplotlib.pyplot as plt
import os

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

file_path = r'C:\Users\Admin\Downloads\comptagevelo20152.csv'

if not os.path.exists(file_path):
    print(f"Файл не знайдено за шляхом: {file_path}")
    print("Файли в поточній папці:")
    print(os.listdir('.'))
    exit()

try:
    df = pd.read_csv(
        file_path,
        sep=',',
        quotechar='"',
        parse_dates=['Date'],
        dayfirst=True,
        index_col='Date'
    )
except Exception as e:
    print("Ошибка при чтении файла:", e)
    exit()

print("Перші 5 рядків:\n")
print(df.head())
print("\nІнформація про DataFrame:\n")
df.info()
print("\nОписова статистика:\n")
print(df.describe())

total_bikes = df.select_dtypes(include='number').sum().sum()
print("\nЗагальна кількість велосипедистів за рік на усіх велодоріжках:", total_bikes)

total_per_track = df.select_dtypes(include='number').sum()
print("\nЗагальна кількість велосипедистів за рік по кожній велодоріжці:\n", total_per_track)

bike_tracks = df.select_dtypes(include='number').columns
tracks = bike_tracks[:3]

df_monthly = df.resample('ME').sum()

for track in tracks:
    popular_month = df_monthly[track].idxmax().strftime('%B')
    print(f"Найбільш популярний місяць для {track}: {popular_month}")

plt.figure(figsize=(15, 10))
df.plot(ax=plt.gca())
plt.title('Використання велодоріжок за 2015 рік')
plt.xlabel('Дата')
plt.ylabel('Кількість велосипедистів')
plt.show()

print("Доступні велодоріжки:")
for i, track in enumerate(bike_tracks):
    print(f"{i+1}. {track}")

while True:
    choice = input("\nВведіть номер велодоріжки для графіка: ")

    if not choice.isdigit():
        print(" Невірна доріжка! Можна вводити лише НОМЕР зі списку.")
        continue

    choice_index = int(choice) - 1

    if 0 <= choice_index < len(bike_tracks):
        track_to_plot = bike_tracks[choice_index]
        break
    else:
        print("Невірна доріжка! Можна вводити лише номер зі списку.")

monthly_sum = df_monthly[track_to_plot]
monthly_sum.index = monthly_sum.index.strftime('%Y-%m')

plt.figure(figsize=(15, 7))
monthly_sum.plot(kind='bar', color='skyblue')
plt.title(f'Завантаженість велодоріжки "{track_to_plot}" по місяцях')
plt.xlabel('Місяць')
plt.ylabel('Кількість велосипедистів')
plt.xticks(rotation=45)

for i, val in enumerate(monthly_sum):
    plt.text(i, val + 5, int(val), ha='center', va='bottom', fontsize=9)

plt.show()