# مثال‌های استفاده از `.join()` و `.split()` در پایتون

در اینجا، دو متد `.join()` و `.split()` در پایتون را با استفاده از عبارت `"Hello my name is Sadegh"` بررسی می‌کنیم.

## استفاده از `.split()`

با استفاده از متد `.split()`، رشته را به کلمات جداگانه تقسیم می‌کنیم:

```python
test_string = "Hello my name is Sadegh"
list_of_words = test_string.split(" ")
print(list_of_words)


نتیجه‌ی اجرای این کد به این صورت خواهد بود:

['Hello', 'my', 'name', 'is', 'Sadegh']

در اینجا، متد 
split(" ")
 رشته را بر اساس فضای خالی (فاصله) جدا کرده و یک لیست از کلمات ایجاد می‌کند.

استفاده از
 .join()

اکنون می‌توانیم لیست کلمات به دست آمده را با استفاده از متد 
.join()
 دوباره به یک رشته تبدیل کنیم. این بار، از یک جداکننده‌ی خاص استفاده می‌کنیم؛ برای مثال، یک خط تیره (-):

separator = "-"
joined_string = separator.join(list_of_words)
print(joined_string)

نتیجه‌ی این کد به این صورت خواهد بود:

Hello-my-name-is-Sadegh

در اینجا، متد join("-") تمام عناصر لیست list_of_words را با استفاده از خط تیره به هم متصل کرده است.
