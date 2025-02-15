import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


# Завантаження даних
df = pd.read_csv('4_DataAnalyst.csv')
print(df.info())
# Видалення рядків з невідомим сектором
df = df[df["Sector"].str.strip() != "-1"]
location_works=df["Location"].value_counts()
# Перевірка пропущених значень
print("Кількість пустих значень стовпця Rating:", df["Rating"].isnull().sum())
print("Кількість пустих значень стовпця Salary Estimate:", df["Salary Estimate"].isnull().sum())
print("Кількість пустих значень стовпця Revenue:", df["Revenue"].isnull().sum())

# Перевірка гіпотез
# 1. Залежність зарплати від рейтингу компанії
def parse_salary(salary):
    match = re.search(r'\$(\d{2,3})K-\$(\d{2,3})K', str(salary))
    if match:
        min_salary = int(match.group(1)) * 1000
        max_salary = int(match.group(2)) * 1000
        return min_salary, max_salary
    return np.nan, np.nan

df[['Min Salary', 'Max Salary']] = df['Salary Estimate'].apply(lambda x: pd.Series(parse_salary(x)))
df["Mean Salary"] = (df["Min Salary"] + df["Max Salary"]) / 2


df.plot(x='Rating', y='Max Salary', kind='scatter', title='Залежність зарплати від рейтингу компанії', color="red")
#plt.show()

# 2. В яких секторах найбільше працюють Data Analysts
sector_counts = df["Sector"].value_counts()

# Відфільтруємо малі категорії
threshold = 50
filtered_counts = sector_counts[sector_counts >= threshold]
filtered_counts["Other"] = sector_counts[sector_counts < threshold].sum()
# Побудова кругової діаграми
filtered_counts.plot(kind='pie', figsize=(10, 6), autopct="%1.1f%%", title="Сектори, де працюють Data Analysts")
#plt.show()
# 3. Чи залежить зарплата аналітиків від доходу компанії
def parse_revenue(revenue):
    match = re.search(r'(\d+)(?:\+| to )?(\d+)? (million|billion)', str(revenue), re.IGNORECASE)
    if match:
        min_rev = int(match.group(1)) * (1_000_000 if match.group(3).lower() == "million" else 1_000_000_000)
        max_rev = int(match.group(2)) * (1_000_000 if match.group(3).lower() == "million" else 1_000_000_000) \
            if match.group(2) else min_rev
        return min_rev, max_rev
    return np.nan, np.nan

df[['Min Revenue', 'Max Revenue']] = df['Revenue'].apply(lambda x: pd.Series(parse_revenue(x)))
df["Mean Revenue"] = df["Min Revenue"]+df["Max Revenue"]/2
df.plot(x='Mean Revenue', y='Mean Salary', kind='scatter', title='Залежність зарплати аналітика від доходу компанії',
        color="red")
#plt.show()


#Гіпотеза №4 "Більше доходу отримує компанія з меншою кількістю вакансій"
#print(df["Size"].value_counts())
def parse_size(size):
    match = re.search(r'(\d+)(?:\+| to )?(\d+)? employees', size, re.IGNORECASE)
    if match:
        return[match.group(1), match.group(2)] # Возвращаем кортеж чисел
    return np.nan, np.nan  # Если нет совпадения

df[['Min Employees', 'Max Employees']] = df['Size'].apply(lambda x: pd.Series(parse_size(x)))
df['Min Employees'] = pd.to_numeric(df['Min Employees'], errors='coerce')
df['Max Employees'] = pd.to_numeric(df['Max Employees'], errors='coerce')
df.plot(x='Min Employees', y='Max Revenue', kind='hist', title="Більше доходу отримує компанія \nз меншою кількістю вакансій", color="red")
plt.show()




