import cv2
import pytesseract
import re
from pytesseract import Output
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import ImageGrab
import keyboard
from datetime import datetime
import pyautogui
import shutil
import time
import sys
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

def create_folders():
    # پیدا کردن مسیر پوشه‌ای که فایل اجرایی در آن قرار دارد
    exe_dir = os.path.dirname(sys.executable)

    # ساخت مسیرهای پوشه‌های مورد نظر
    source_folder = os.path.join(exe_dir, 'source_folder')
    destination_base_folder = os.path.join(exe_dir, 'destination_base_folder')

    # ایجاد پوشه‌ها اگر وجود ندارند
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(destination_base_folder, exist_ok=True)

    return source_folder, destination_base_folder


def move_files(destination_f):
    # دایرکتوری جاری (همان‌جایی که فایل اجرایی اجرا می‌شود)
    current_dir = os.getcwd()
    # پوشه منبع و مقصد
    source_folder = current_dir
    today = datetime.now().strftime("%Y-%m-%d")
    destination_base_folder = os.path.join(current_dir, today, destination_f)


    if not os.path.exists(destination_base_folder):
        os.makedirs(destination_base_folder)

    files_moved = False

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.txt')):
            source_file = os.path.join(source_folder, filename)
            destination_file = os.path.join(destination_base_folder, filename)
            attempt = 0
            max_attempts = 5
            while attempt < max_attempts:
                try:
                    shutil.move(source_file, destination_file)
                    print(f'Moved {source_file} to {destination_file}')
                    files_moved = True
                    break
                except PermissionError as e:
                    print(f'Error moving {source_file}: {e}')
                    time.sleep(1)  # تأخیر 1 ثانیه
                    attempt += 1
            else:
                print(f'Failed to move {source_file} after {max_attempts} attempts.')

    if not files_moved:
        print("No files were moved. Please check the source folder and file permissions.")


def process_image(image, threshold_value):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(gray, 1)
    _, img_thresh = cv2.threshold(img_blur, threshold_value, 255, cv2.THRESH_BINARY)
    return img_thresh

def get_ocr_text(image, lang='fas'):
    return pytesseract.image_to_string(image, lang=lang).strip()

def get_ocr_text1(image, lang='eng'):
    return pytesseract.image_to_string(image, lang=lang).strip()

def resize_image(image, scale):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

def check_threshold(image, threshold):
    processed_image = process_image(image, threshold)
    ocr_text = get_ocr_text(processed_image)
    return ocr_text

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot1.jpg")
    print("تصویر ذخیره شد")

def seryal_govahi(image_path):
    # سریال گواهی
    original_image = cv2.imread(image_path)
    height, width, _ = original_image.shape
    cropped_range2 = original_image[209:(height - 848), 810:(width - 750)]
    scales2 = [1.5]
    for scale in scales2:
        resized_image2 = resize_image(cropped_range2, scale)
        threshold2 = 225
        processed_image2 = process_image(resized_image2, threshold2)
        ocr_text200 = get_ocr_text(processed_image2).replace("سرپال","سریال").replace("گواهی:","گواهی")
        list_govahi= ocr_text200.split()
#        return list_govahi[0], list_govahi[1]
        if len(list_govahi) >= 2:
            if list_govahi[0] == "سریال" or list_govahi[1] == "گواهی":
                return 1

    return 0


def process_and_save_data(image_path, file):
    global today, subfolder_name, only_numbers10
    original_image = cv2.imread(image_path)
    height, width, _ = original_image.shape

    file.write(f"Processing {image_path}\n" + ":")
    file.write("\n")
    file.write("\n")


    def find_most_frequent_char(chars):
        from collections import Counter
        counter = Counter(chars)
        most_common_char, _ = counter.most_common(1)[0]
        return most_common_char

    # گواهی
    cropped_range1 = original_image[170:(height - 880), 805:(width - 750)]
    scales1 = [1.5]
    for scale in scales1:
        resized_image1 = resize_image(cropped_range1, scale)
        threshold1 = 225
        processed_image1 = process_image(resized_image1, threshold1)
        ocr_text1 = get_ocr_text(processed_image1)
        # p("=======================================")
        file.write('گواهی :')
        file.write("\n")
        file.write(ocr_text1.replace('فتی', 'فنی').replace('بنزیتی', 'بنزینی').replace('\n', ''))
        file.write("\n")
        file.write("\n")


    # سریال گواهی
    cropped_range6 = original_image[209:(height - 848), 810:(width - 750)]
    scales6 = [1.5]
    thresholds = [235, 236, 237, 240, 241]
    ocr_texts = []
    for scale in scales6:
        resized_image2 = resize_image(cropped_range6, scale)
        for threshold2 in thresholds:
            processed_image2 = process_image(resized_image2, threshold2)
            ocr_text2 = get_ocr_text(processed_image2)
            ocr_text2 = re.sub(r'\D', '', ocr_text2)

            ocr_texts.append(ocr_text2)

    # پیدا کردن طولانی‌ترین متن OCR
    max_len = max(len(text) for text in ocr_texts)

    # مقایسه و انتخاب کاراکترهای پر تکرار در هر موقعیت
    final_text = []
    for i in range(max_len):
        chars_at_position = [text[i] for text in ocr_texts if i < len(text)]
        most_frequent_char = find_most_frequent_char(chars_at_position)
        final_text.append(most_frequent_char)
    # نتیجه نهایی
    final_result = ''.join(final_text)
    file.write('سریال گواهی:')
    file.write("\n")
    file.write(final_result)
    file.write("\n")
    file.write("\n")

    # گرفتن تاریخ امروز به فرمت YYYY-MM-DD
    today = datetime.today().strftime('%Y-%m-%d')
    folder_name = today

    # بررسی وجود پوشه و در صورت عدم وجود، ساخت آن
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # گرفتن نام پوشه از تابع و ساخت آن داخل پوشه ایجاد شده
    subfolder_name = ocr_text2
    subfolder_path = os.path.join(folder_name, subfolder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    source_folder, destination_base_folder = create_folders()
    destination_folder = os.path.join(destination_base_folder, today, subfolder_name)  # پوشه‌ی جدید که تصاویر به آنجا منتقل می‌شوند

    # مشخصات مرکز
    cropped_range8 = original_image[235:(height - 816), 826:(width - 665)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 225
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text(processed_image8)
        # file.write("=======================================")
        file.write('مشخصات مرکز:')
        file.write("\n")
        file.write(ocr_text8.replace("تهرانن","تهران").replace('ابراقیمی', 'ابراهیمی').replace(': 8 - حامد تجاری اصل','بیهقی -کد: 1718- حامد نجاری اصل').replace('حسیتی','حسینی') )
        file.write("\n")
        file.write("\n")

    # شناسه پذیرش
    cropped_range8 = original_image[270:(height - 782), 1100:(width - 670)]
    scales8 = [1.5]
    plt.imsave("شناسه پذیرش.jpg", cropped_range8)
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('شناسه پذیرش:')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # زمان ثبت نام
    cropped_range1 = original_image[306:(height - 750), 1120:(width - 670)]
    scales1 = [1.5]

    for scale in scales1:
        resized_image1 = resize_image(cropped_range1, scale)
        threshold1 = 215
        processed_image1 = process_image(resized_image1, threshold1)
        ocr_text1 = get_ocr_text1(processed_image1)
        # file.write("=======================================")
        file.write('زمان ثبت نام:')
        file.write("\n")
        file.write(ocr_text1)
        file.write("\n")
        file.write("\n")

    # تاریخ
    cropped_range1 = original_image[270:(height - 782), 830:(width - 988)]
    scales1 = [1.5]

    for scale in scales1:
        resized_image1 = resize_image(cropped_range1, scale)
        threshold1 = 215
        processed_image1 = process_image(resized_image1, threshold1)
        ocr_text1 = get_ocr_text1(processed_image1)
        # file.write("=======================================")
        file.write('تاریخ:')
        file.write("\n")
        file.write(ocr_text1)
        file.write("\n")
        file.write("\n")

    # تاریخ اعتبار
    cropped_range1 = original_image[306:(height - 750), 830:(width - 988)]
    scales1 = [1.5]

    for scale in scales1:
        resized_image1 = resize_image(cropped_range1, scale)
        threshold1 = 215
        processed_image1 = process_image(resized_image1, threshold1)
        ocr_text1 = get_ocr_text1(processed_image1)
        # file.write("=======================================")
        file.write('تاریخ اعتبار:')
        file.write("\n")
        file.write(ocr_text1)
        file.write("\n")
        file.write("\n")

    #
    # مدل
    cropped_range7 = original_image[340:(height - 715), 830:(width - 988)]
    scales7 = [1.5]

    for scale in scales7:
        resized_image7 = resize_image(cropped_range7, scale)
        threshold7 = 197
        processed_image7 = process_image(resized_image7, threshold7)
        ocr_text7 = get_ocr_text1(processed_image7)
        # file.write("=======================================")
        file.write('مدل:')
        file.write("\n")
        file.write(ocr_text7)
        file.write("\n")
        file.write("\n")

    #
    # دفعات مراجعه
    cropped_range1 = original_image[380:(height - 677), 1030:(width - 530)]
    scales1 = [3]
    thresholds = [198, 200, 210, 237, 244]
    ocr_texts = []

    for scale in scales1:
        resized_image2 = resize_image(cropped_range1, scale)
        for threshold2 in thresholds:
            processed_image2 = process_image(resized_image2, threshold2)
            ocr_text2 = get_ocr_text1(processed_image2)
            ocr_text2 = re.sub(r'V[/\\]', 'W', ocr_text2)
            ocr_text2 = ocr_text2.replace(" ", "").replace("]", "J")
            ocr_texts.append(ocr_text2[0:1])

    # تابعی برای پیدا کردن بیشترین تکرار در هر موقعیت

    # پیدا کردن طولانی‌ترین متن OCR
    max_len = max(len(text) for text in ocr_texts)

    # مقایسه و انتخاب کاراکترهای پر تکرار در هر موقعیت
    final_text = []
    for i in range(max_len):
        chars_at_position = [text[i] for text in ocr_texts if i < len(text)]
        most_frequent_char = find_most_frequent_char(chars_at_position)
        final_text.append(most_frequent_char)

    # نتیجه نهایی
    final_result = ''.join(final_text)
    file.write('دفعات مراجعه:')
    file.write("\n")
    file.write(final_result)
    file.write("\n")
    file.write("\n")

    # نوع سوخت
    cropped_range4 = original_image[410:(height - 648), 1050:(width - 675)]
    cropped_range14 = original_image[405:(height - 644), 1050:(width - 530)]
    scales4 = 1.5
    scales14 = 3
    threshold4 = 248
    threshold14 = 195

    resized_image4 = resize_image(cropped_range4, scales4)
    resized_image14 = resize_image(cropped_range14, scales14)
    processed_image4 = process_image(resized_image4, threshold4)
    processed_image14 = process_image(resized_image14, threshold14)
    ocr_text4 = get_ocr_text(processed_image4)
    ocr_text14 = get_ocr_text(processed_image14)

    if len(ocr_text4) > 2 :
        # file.write("=======================================")
        file.write('نوع سوخت:')
        file.write(ocr_text4.replace('بتزینی', 'بنزینی').replace('بنزیتی', 'بنزینی'))
        file.write("\n")
        file.write("\n")
    else:
        # file.write("=======================================")
        file.write(ocr_text14.replace('بتزینی', 'بنزینی').replace('بنزیتی', 'بنزینی'))
        file.write("\n")
        file.write("\n")


    # شماره پلاک
    cropped_range1 = original_image[428:(height - 615), 1040:(width - 675)]
    scales1 = [1.5]
    plt.imsave("شماره پلاک.jpg", cropped_range1)
    for scale in scales1:
        resized_image1 = resize_image(cropped_range1, scale)
        threshold1 = 216
        processed_image1 = process_image(resized_image1, threshold1)
        ocr_text1 = get_ocr_text1(processed_image1)
        ocr_text2 = get_ocr_text(processed_image1)
        ocr_text1 = ocr_text1.strip().replace(' ', '')
        ocr_text2 = ocr_text2.strip().replace(' ', '')
        only_letters = re.sub(r'\d', '', ocr_text2)
        # file.write("=======================================")
        file.write('حرف پلاک:')
        file.write("\n")
        # file.write(ocr_text1[0:2].replace('€', '6'))
        if len(ocr_text1) > 2 and ocr_text1[2] == '3':
            file.write("د")
            file.write("\n")
            file.write("\n")
        elif len(ocr_text1) > 2 and ocr_text1[2] == "1":
            file.write("ط")
            file.write("\n")
            file.write("\n")
        elif len(ocr_text1) > 2 and ocr_text1[2] == "b":
            file.write("ط")
            file.write("\n")
            file.write("\n")
        else:
            file.write(ocr_text2[-3:-2].replace('0', 'ن'))
        # file.write(ocr_text1[3:6].replace('B', '8').replace('S', '8'))
        # file.write('ایران ' + ocr_text1[7:9])
        file.write("\n")
        file.write('شماره پلاک بصورت یکجا:')
        ocr_text2 = ocr_text2.replace("ایرات", "ایران").replace("ايرآن", "ایران") # ابتدا اصلاح خطای تایپی
        file.write("\n")
        file.write("\n")
        if ocr_text2[5] == '0':
            ocr_text2 = ocr_text2[:5] + ocr_text2[6:]  # حذف کردن کاراکتر '0' در اندیس 5
        file.write(ocr_text2)
        file.write("\n")
        file.write("\n")

    #
    # سیستم
    cropped_range1 = original_image[456:(height - 592), 1040:(width - 675)]
    scales1 = [1.5]
    for scale in scales1:
        resized_image1 = resize_image(cropped_range1, scale)
        threshold1 = 215
        processed_image1 = process_image(resized_image1, threshold1)
        ocr_text1 = get_ocr_text(processed_image1)
        # file.write("=======================================")
        file.write('سیستم:')
        file.write("\n")
        file.write(ocr_text1.replace("یژو", "پژو").replace("بژو", "پژو").replace('ساییا','سایپا').replace('سولري','سواری').replace("تویهتا", "تویوتا").replace("رتو", "رنو").replace("اسبورتیج", "اسپورتیج").replace("لیشانه","لیفان").replace("لکسسی", "لکسوس").replace("تیسانه", "نیسان") )
        file.write("\n")
        file.write("\n")

    # شماره شاسی
    cropped_range2 = original_image[478:(height - 564), 1040:(width - 675)]
    scales2 = [1.5]
    plt.imsave("شماره شاسی.jpg", cropped_range2)
    thresholds = [185, 186, 190, 207, 211]
    ocr_texts = []

    for scale in scales2:
        resized_image2 = resize_image(cropped_range2, scale)
        for threshold2 in thresholds:
            processed_image2 = process_image(resized_image2, threshold2)
            ocr_text2 = get_ocr_text1(processed_image2)
            ocr_text2 = re.sub(r'V[/\\]', 'W', ocr_text2)
            ocr_text2 = ocr_text2.replace(" ", "").replace("]", "J")
            ocr_texts.append(ocr_text2)

    # تابعی برای پیدا کردن بیشترین تکرار در هر موقعیت

    # پیدا کردن طولانی‌ترین متن OCR
    max_len = max(len(text) for text in ocr_texts)

    # مقایسه و انتخاب کاراکترهای پر تکرار در هر موقعیت
    final_text = []
    for i in range(max_len):
        chars_at_position = [text[i] for text in ocr_texts if i < len(text)]
        most_frequent_char = find_most_frequent_char(chars_at_position)
        final_text.append(most_frequent_char)

    # نتیجه نهایی
    final_result = ''.join(final_text)
    file.write('شماره شاسی:')
    file.write("\n")
    file.write(final_result)
    file.write("\n")
    file.write("\n")


    # # رنگ2
    # cropped_range311 = original_image[378:(height - 670), 550:(width - 930)]
    # scales3 = [1.5, 1]
    # threshold20 = [215, 216]
    # plt.imsave("رنگ.jpg", cropped_range311)
    #
    # # پردازش تصویر با اولین مقیاس و آستانه
    # resized_image31 = resize_image(cropped_range311, scales3[0])
    # processed_image31 = process_image(resized_image31, threshold20[0])
    # ocr_text3_234 = get_ocr_text(processed_image31)
    #
    # # پردازش تصویر با دومین مقیاس و آستانه
    # resized_image311 = resize_image(cropped_range311, scales3[1])
    # processed_image311 = process_image(resized_image311, threshold20[1])
    # ocr_text3_216 = get_ocr_text(processed_image311)
    #
    # # file.write("=======================================")
    # file.write(f"خروجی پردازش اول: {ocr_text3_234}")
    # file.write("\n")
    # file.write(f"خروجی پردازش دوم: {ocr_text3_216} ")
    # file.write("\n")
    #
    # if ocr_text3_234:
    #     file.write('رنگ1:')
    #     file.write("\n")
    #     file.write(ocr_text3_234.replace('توار شطرتجي معشکي', 'نوار شطرنجی مشکی').replace('توار شطرتجي معشکي', 'نوار شطرنجی مشکی').replace('زود', 'زرد').replace("نقره اکه", "نقره ای").replace("فرمر", "قرمز").replace("سقید صقي", "سفید صدفی"))
    #     file.write("\n")
    #     file.write("\n")
    # else:
    #     if ocr_text3_216:
    #         file.write('رنگ2:')
    #         file.write("\n")
    #         file.write(ocr_text3_216.replace('سید', 'سفید').replace('زود', 'زرد').replace("نقره اکه", "نقره ای").replace("فرمر", "قرمز").replace("سقید صقي", "سفید صدفی"))
    #         file.write("\n")
    #         file.write("\n")
    #     else:
    #         file.write('رنگ3:')
    #         file.write("\n")
    #         file.write("سفید")
    #         file.write("\n")
    #         file.write("\n")
    #
    #

    # سیستم سوخت
    cropped_range8 = original_image[407:(height - 648), 550:(width - 1150)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 210
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text(processed_image8)
        # file.write("=======================================")
        file.write('سیستم سوخت:')
        file.write("\n")
        file.write(ocr_text8[0:7].replace('اتزکتور', 'انژکتور').replace('اتژکتور', 'انژکتور'))
        file.write("\n")
        file.write("\n")

    # VIN
    cropped_range2 = original_image[428:(height - 615), 550:(width - 1150)]
    scales2 = [1.5]
    thresholds = [185, 186, 190, 207, 211]
    plt.imsave("VIN.jpg", cropped_range2)
    ocr_texts = []
    for scale in scales2:
        resized_image2 = resize_image(cropped_range2, scale)
        for threshold2 in thresholds:
            processed_image2 = process_image(resized_image2, threshold2)
            ocr_text2 = get_ocr_text1(processed_image2)
            ocr_text2 = re.sub(r'V[/\\]', 'W', ocr_text2)
            ocr_text2 = ocr_text2.replace(" ", "").replace("]", "J")
            ocr_texts.append(ocr_text2)
            # نمایش نتیجه OCR برای هر آستانه
            # print(f'Threshold {threshold2}:')
            # print(ocr_text2)
            # print('---')

    # تابعی برای پیدا کردن بیشترین تکرار در هر موقعیت

    # پیدا کردن طولانی‌ترین متن OCR
    max_len = max(len(text) for text in ocr_texts)

    # مقایسه و انتخاب کاراکترهای پر تکرار در هر موقعیت
    final_text = []
    for i in range(max_len):
        chars_at_position = [text[i] for text in ocr_texts if i < len(text)]
        most_frequent_char = find_most_frequent_char(chars_at_position)
        final_text.append(most_frequent_char)
    # نتیجه نهایی
    final_result = ''.join(final_text)
    file.write('VIN:')
    file.write("\n")
    file.write(final_result)
    file.write("\n")
    file.write("\n")

    # تیپ
    cropped_range10 = original_image[456:(height - 592), 550:(width - 1150)]
    scales10 = [1.5]
    plt.imsave("تیپ خودرو.jpg", cropped_range10)

    for scale in scales10:
        resized_image10 = resize_image(cropped_range10, scale)
        threshold5 = 198
        processed_image10 = process_image(resized_image10, threshold5)
        ocr_text10_eng = get_ocr_text(processed_image10, lang='eng')
        ocr_text10_fas = get_ocr_text(processed_image10, lang='fas')
        ocr_text10_eng = ocr_text10_eng.replace('TUS', 'TU5')
        # file.write("=======================================")
        file.write('تیپ:')
        file.write("\n")
        file.write(f"خروجی OCR انگلیسی: {ocr_text10_eng.replace('1328X', '132SX').replace("€s250", "ES250").replace(" ", "").replace("15HFC", "J5HFC").replace("1115E", "111SE")} ")
        file.write("\n")
        file.write("\n")
        file.write(f"خروجی OCR فارسی: {ocr_text10_fas.replace('تباة', 'تیبا').replace("ننا","دنا").replace("اسیورتیج","اسپورتیج")} ")
        file.write("\n")
        file.write("\n")

    # شماره موتور
    cropped_range6 = original_image[478:(height - 564), 550:(width - 1150)]
    scales6 = [1.5]
    thresholds = [185, 186, 190, 207, 211]
    plt.imsave("شماره موتور.jpg", cropped_range6)
    ocr_texts = []
    for scale in scales6:
        resized_image2 = resize_image(cropped_range6, scale)
        for threshold2 in thresholds:
            processed_image2 = process_image(resized_image2, threshold2)
            ocr_text2 = get_ocr_text1(processed_image2)
            ocr_text2 = re.sub(r'V[/\\]', 'W', ocr_text2)
            ocr_text2 = ocr_text2.replace(" ", "").replace("]", "J")
            ocr_texts.append(ocr_text2)
            # نمایش نتیجه OCR برای هر آستانه
            # print(f'Threshold {threshold2}:')
            # print(ocr_text2)
            # print('---')

    # تابعی برای پیدا کردن بیشترین تکرار در هر موقعیت

    # پیدا کردن طولانی‌ترین متن OCR
    max_len = max(len(text) for text in ocr_texts)

    # مقایسه و انتخاب کاراکترهای پر تکرار در هر موقعیت
    final_text = []
    for i in range(max_len):
        chars_at_position = [text[i] for text in ocr_texts if i < len(text)]
        most_frequent_char = find_most_frequent_char(chars_at_position)
        final_text.append(most_frequent_char)
    # نتیجه نهایی
    final_result = ''.join(final_text)
    file.write('شماره موتور:')
    file.write("\n")
    file.write(final_result)
    file.write("\n")
    file.write("\n")

    # شتاب ترمز - ترمز اصلی
    cropped_range8 = original_image[576:(height - 480), 1160:(width - 700)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('شتاب ترمز - ترمز اصلی:')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # شتاب ترمز - ترمز دستی
    cropped_range8 = original_image[603:(height - 455), 1160:(width - 700)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('شتاب ترمز - ترمز دستی:')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # آلایندگی - CO
    cropped_range8 = original_image[630:(height - 428), 1160:(width - 700)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('آلایندگی - CO :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # آلایندگی - HC
    cropped_range8 = original_image[657:(height - 401), 1160:(width - 700)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('آلایندگی - HC :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # آلایندگی - Y
    cropped_range8 = original_image[684:(height - 374), 1160:(width - 700)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('آلایندگی - Y :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # آلایندگی - CO(fast)
    cropped_range8 = original_image[709:(height - 347), 1160:(width - 700)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('آلایندگی - CO(fast) :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # آلایندگی - O2
    cropped_range8 = original_image[734:(height - 320), 1160:(width - 700)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('آلایندگی - O2 :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # آلایندگی - دور موتور
    cropped_range8 = original_image[759:(height - 293), 1160:(width - 700)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('آلایندگی - دور موتور :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # نیروی ترمز - جلو - راست
    cropped_range8 = original_image[576:(height - 480), 825:(width - 1042)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('ترمز - جلو - راست :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # نیروی ترمز - جلو - چپ
    cropped_range8 = original_image[576:(height - 480), 763:(width - 1100)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('نیروی ترمز - جلو - چپ :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # نیروی ترمز - جلو - عدم توازن
    cropped_range8 = original_image[576:(height - 480), 680:(width - 1158)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('نیروی ترمز - جلو - عدم توازن :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # نیروی ترمز - عقب - راست
    cropped_range8 = original_image[603:(height - 455), 825:(width - 1042)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('نیروی ترمز - عقب - راست :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # نیروی ترمز - عقب - چپ
    cropped_range8 = original_image[603:(height - 455), 763:(width - 1100)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('نیروی ترمز - عقب - چپ :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")


    # نیروی ترمز - عقب - عدم توازن
    cropped_range8 = original_image[603:(height - 455), 680:(width - 1158)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('نیروی ترمز - عقب - عدم توازن :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")


    # نیروی ترمز - دستی - راست
    cropped_range8 = original_image[630:(height - 428), 825:(width - 1042)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('نیروی ترمز - دستی - راست :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # نیروی ترمز - دستی - چپ
    cropped_range8 = original_image[630:(height - 428), 763:(width - 1100)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('نیروی ترمز - دستی - چپ :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # نیروی ترمز - دستی - عدم توازن
    cropped_range8 = original_image[630:(height - 428), 680:(width - 1158)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('نیروی ترمز - دستی - عدم توازن :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # کمک فنر - جلو - راست
    cropped_range8 = original_image[657:(height - 401), 825:(width - 1042)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('کمک فنر - جلو - راست :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # کمک فنر - جلو - چپ
    cropped_range8 = original_image[657:(height - 401), 763:(width - 1100)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('کمک فنر - جلو - چپ :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # کمک فنر - جلو - عدم توازن
    cropped_range8 = original_image[657:(height - 401), 680:(width - 1158)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('کمک فنر - جلو - عدم توازن :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # کمک فنر - عقب - راست
    cropped_range8 = original_image[684:(height - 374), 825:(width - 1042)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('کمک فنر - عقب - راست :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # کمک فنر - عقب - چپ
    cropped_range8 = original_image[684:(height - 374), 763:(width - 1100)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('کمک فنر - عقب - چپ :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # کمک فنر - عقب - عدم توازن
    cropped_range8 = original_image[684:(height - 374), 680:(width - 1158)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('کمک فنر - عقب - عدم توازن :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # لغزش جانبی جلو
    cropped_range8 = original_image[709:(height - 347), 763:(width - 1042)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('لغزش جانبی جلو :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # وزن - جلو - راست
    cropped_range8 = original_image[734:(height - 320), 825:(width - 1042)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('وزن - جلو - راست :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # وزن - جلو - چپ
    cropped_range8 = original_image[734:(height - 293), 763:(width - 1100)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('وزن - جلو - چپ :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # وزن - عقب - راست
    cropped_range8 = original_image[759:(height - 293), 825:(width - 1042)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('وزن - عقب - راست :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("\n")

    # وزن - عقب - چپ
    cropped_range8 = original_image[734:(height - 293), 763:(width - 1100)]
    scales8 = [1.5]
    for scale in scales8:
        resized_image8 = resize_image(cropped_range8, scale)
        threshold8 = 198
        processed_image8 = process_image(resized_image8, threshold8)
        ocr_text8 = get_ocr_text1(processed_image8)
        # file.write("=======================================")
        file.write('وزن - عقب - چپ :')
        file.write("\n")
        file.write(ocr_text8)
        file.write("\n")
        file.write("=======================================")
        file.write("\n")
        file.write("\n")
    file.close()
    move_files(subfolder_name)

# تابع برای بررسی کلیدهای فشرده شده
def check_hotkey_pressed(target_date):
    # چک کردن آیا کلید Ctrl و P همزمان فشرده شده است
    if keyboard.is_pressed('ctrl') and keyboard.is_pressed('p'):
        current_date = datetime.now()
        print(current_date)
        if current_date < target_date:
            take_screenshot()
            time.sleep(1)
            # باز کردن فایل برای نوشتن نتایج
            with open("ocr_results.txt", "w", encoding="utf-8") as file:
                # حلقه برای پردازش تصاویر از screenshot1 تا screenshot50
                for i in range(12, 13):
                    image_path_png = f"screenshot{i}.png"
                    image_path_jpg = f"screenshot{i}.jpg"

                    if os.path.exists(image_path_png):
                        print(f"screenshot{i}.png")
                        A = seryal_govahi(image_path_png)
                        if A == 1:
                            process_and_save_data(image_path_png, file)
                            print(" تصویر پردازش شد و نتایج ذخیره شدند.")
                        else:
                            print("تصویر نامناسب")

                    elif os.path.exists(image_path_jpg):
                        print(f"screenshot{i}.jpg")
                        A = seryal_govahi(image_path_jpg)
                        if A == 1:
                            process_and_save_data(image_path_jpg, file)
                            print(" تصویر پردازش شد و نتایج ذخیره شدند.")
                        else:
                            # دایرکتوری جاری
                            current_dir = os.getcwd()

                            # لیست فرمت‌های قابل قبول
                            valid_extensions = ('.png', '.jpg', '.jpeg', '.txt')
                            file.close()
                            # حذف فایل‌های با فرمت‌های مشخص
                            for filename in os.listdir(current_dir):
                                if filename.lower().endswith(valid_extensions):
                                    file_path = os.path.join(current_dir, filename)
                                    try:
                                        os.remove(file_path)
                                        print(f'حذف {file_path}')
                                    except Exception as e:
                                        print(f'خطا در حذف {file_path}: {e}')

                            print("تصویر نامناسب")

                    else:
                        file.write(f"Image {i} not found.")
                        file.write(f"Image screenshot{i} not found.\n")

        else:
            print(f"کد در تاریخ {target_date.strftime('%Y-%m-%d')} اجرا نخواهد شد.")



target_date = datetime(2024, 8, 30)
# حلقه اصلی برنامه برای چک کردن کلیدهای فشرده شده
while True:
    check_hotkey_pressed(target_date)
