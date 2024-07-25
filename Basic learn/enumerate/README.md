# تابع `enumerate` در پایتون

تابع `enumerate` در پایتون یکی از توابع داخلی مفید است که به شما این امکان را می‌دهد تا به راحتی در مجموعه‌های قابل تکرار مانند لیست‌ها، تاپل‌ها و رشته‌ها پیمایش کنید و به هر عنصر شماره شاخص اختصاص دهید.

## استفاده از `enumerate`

تابع `enumerate` یک شیء شمارشی (enumerator) برمی‌گرداند که شامل جفت‌های `(index, value)` است، جایی که `index` شماره شاخص عنصر و `value` خود عنصر است. این ویژگی برای زمانی که نیاز دارید بدانید هر عنصر در چه موقعیتی در مجموعه قرار دارد، بسیار مفید است.

### مثال

```python
fruits = ['apple', 'banana', 'cherry']

for index, fruit in enumerate(fruits):
    print(index, fruit)

خروجی:


0 apple
1 banana
2 cherry

گزینه‌های اضافی
تابع enumerate یک پارامتر اختیاری به نام start دارد که می‌توانید با استفاده از آن شماره شاخص اولیه را تنظیم کنید. به طور پیش‌فرض، این مقدار 0 است، اما می‌توانید آن را به هر عدد صحیح دلخواه تغییر دهید.

مثال با پارامتر start
```python
fruits = ['apple', 'banana', 'cherry']

for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)
```
خروجی:

1 apple
2 banana
3 cherry
