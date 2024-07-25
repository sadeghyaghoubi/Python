## توضیح روش `.copy()` در Python

در زبان برنامه‌نویسی Python، روش `.copy()` برای ایجاد یک نسخه جدید از یک شیء (object) که از نوع قابل کپی (copyable) باشد، استفاده می‌شود. این روش معمولاً برای ایجاد یک کپی از لیست، دیکشنری یا سایر ساختارهای داده‌ای به کار می‌رود تا تغییرات اعمال‌شده به یک نسخه، تأثیری بر روی دیگر نسخه‌ها نداشته باشد.

### مثال استفاده از `.copy()`:

#### برای لیست‌ها
```python
original_list = [1, 2, 3, 4, 5]
copied_list = original_list.copy()

# تغییر مقدار یکی از عناصر لیست اصلی
copied_list[0] = 10

print("Original List:", original_list)  # Output: [1, 2, 3, 4, 5]
print("Copied List:", copied_list)      # Output: [10, 2, 3, 4, 5]

```

در این مثال، original_list.copy() از لیست original_list یک کپی جدید به نام copied_list ایجاد می‌کند. هرگونه تغییری که به original_list اعمال شود، تأثیری بر روی copied_list ندارد، زیرا آن‌ها دو شیء مستقل هستند.


## برای دیکشنری‌ها

```python
original_dict = {'a': 1, 'b': 2, 'c': 3}
copied_dict = original_dict.copy()

# تغییر مقدار یک کلید در دیکشنری اصلی
copied_dict['a'] = 10

print("Original Dictionary:", original_dict)  # Output: {'a': 1, 'b': 2, 'c': 3}
print("Copied Dictionary:", copied_dict)      # Output: {'a': 10, 'b': 2, 'c': 3}
```

در این مثال نیز، original_dict.copy() از دیکشنری original_dict یک کپی به نام copied_dict ایجاد می‌کند. تغییری که در original_dict ایجاد شده، تأثیری بر روی copied_dict ندارد.

استفاده از .copy() مفید است زمانی که نیاز به ایجاد یک نسخه مستقل از یک ساختار داده دارید تا تغییرات دیگر نسخه‌ها را تحت تأثیر قرار ندهد.


