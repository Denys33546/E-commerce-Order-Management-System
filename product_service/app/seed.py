import time
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Product


# Огромный массив из 50 полноценных товаров интернет-магазина
BIG_CATALOG = [
    # --- КАТЕГОРИЯ: НОУТБУКИ (15 шт) ---
    {
        "title": "Apple MacBook Pro 14 M3",
        "category": "Ноутбуки",
        "price": 1999.0,
        "inventory": 15,
        "description": "Профессиональный ноутбук для разработчиков и дизайнеров.",
        "specifications": {
            "Процессор": "Apple M3 Pro",
            "ОЗУ": "18 ГБ",
            "Накопитель": "512 ГБ SSD",
            "Экран": "14.2 Liquid Retina XDR",
            "ОС": "macOS"
        }
    },
    {
        "title": "ASUS ROG Strix G16",
        "category": "Ноутбуки",
        "price": 1499.0,
        "inventory": 10,
        "description": "Мощный игровой ноутбук с продвинутым охлаждением.",
        "specifications": {
            "Процессор": "Intel Core i7-13650HX",
            "Видеокарта": "RTX 4060 8GB",
            "ОЗУ": "16 ГБ",
            "Экран": "16 FHD+ 165Hz",
            "Накопитель": "1 ТБ SSD"
        }
    },
    {
        "title": "HP Pavilion 15",
        "category": "Ноутбуки",
        "price": 650.0,
        "inventory": 25,
        "description": "Надежный рабочий инструмент для офиса и учебы.",
        "specifications": {
            "Процессор": "AMD Ryzen 5 5500U",
            "ОЗУ": "8 ГБ",
            "Накопитель": "512 ГБ SSD",
            "Экран": "15.6 IPS FHD",
            "ОС": "Windows 11"
        }
    },
    {
        "title": "Lenovo ThinkPad X1 Carbon Gen 11",
        "category": "Ноутбуки",
        "price": 1850.0,
        "inventory": 8,
        "description": "Премиальный ультрабук в прочном углепластиковом корпусе.",
        "specifications": {
            "Процессор": "Intel Core i7-1355U",
            "ОЗУ": "32 ГБ",
            "Накопитель": "1 ТБ SSD",
            "Экран": "14 WUXGA IPS",
            "Вес": "1.12 кг"
        }
    },
    {
        "title": "Acer Aspire 3",
        "category": "Ноутбуки",
        "price": 450.0,
        "inventory": 40,
        "description": "Бюджетный ноутбук для повседневных задач.",
        "specifications": {
            "Процессор": "Intel Core i3-1215U",
            "ОЗУ": "8 ГБ",
            "Накопитель": "256 ГБ SSD",
            "Экран": "15.6 TN FHD",
            "ОС": "Без ОС"
        }
    },
    {
        "title": "MSI Katana 17 B12V",
        "category": "Ноутбуки",
        "price": 1290.0,
        "inventory": 12,
        "description": "Большой игровой ноутбук с экраном 17 дюймов.",
        "specifications": {
            "Процессор": "Intel Core i7-12650H",
            "Видеокарта": "RTX 4060 8GB",
            "ОЗУ": "16 ГБ",
            "Экран": "17.3 144Hz FHD",
            "Накопитель": "1 ТБ SSD"
        }
    },
    {
        "title": "Dell XPS 13 Plus",
        "category": "Ноутбуки",
        "price": 1699.0,
        "inventory": 7,
        "description": "Ультрасовременный безрамочный дизайн и сенсорная панель.",
        "specifications": {
            "Процессор": "Intel Core i7-1360P",
            "ОЗУ": "16 ГБ",
            "Накопитель": "512 ГБ SSD",
            "Экран": "13.4 OLED 3.5K Touch",
            "ОС": "Windows 11 Pro"
        }
    },
    {
        "title": "Gigabyte G5 KF",
        "category": "Ноутбуки",
        "price": 999.0,
        "inventory": 14,
        "description": "Доступный гейминг на архитектуре Ada Lovelace.",
        "specifications": {
            "Процессор": "Intel Core i5-12500H",
            "Видеокарта": "RTX 4060 8GB",
            "ОЗУ": "16 ГБ",
            "Накопитель": "512 ГБ SSD",
            "Экран": "15.6 144Hz"
        }
    },
    {
        "title": "Xiaomi RedmiBook Pro 15",
        "category": "Ноутбуки",
        "price": 899.0,
        "inventory": 18,
        "description": "Металлический корпус и потрясающий экран 3.2K.",
        "specifications": {
            "Процессор": "AMD Ryzen 7 7840HS",
            "ОЗУ": "16 ГБ",
            "Накопитель": "512 ГБ SSD",
            "Экран": "15.6 3.2K 120Hz",
            "Корпус": "Алюминий"
        }
    },
    {
        "title": "Huawei MateBook D 16",
        "category": "Ноутбуки",
        "price": 799.0,
        "inventory": 20,
        "description": "Большой экран в компактном и легком корпусе.",
        "specifications": {
            "Процессор": "Intel Core i5-12450H",
            "ОЗУ": "16 ГБ",
            "Накопитель": "512 ГБ SSD",
            "Экран": "16 IPS FHD",
            "Батарея": "56 Втч"
        }
    },
    {
        "title": "Razer Blade 16",
        "category": "Ноутбуки",
        "price": 2999.0,
        "inventory": 5,
        "description": "Ультимативный игровой флагман премиум-уровня.",
        "specifications": {
            "Процессор": "Intel Core i9-13950HX",
            "Видеокарта": "RTX 4080 12GB",
            "ОЗУ": "32 ГБ",
            "Экран": "16 Dual QHD+ 240Hz",
            "Накопитель": "1 ТБ SSD"
        }
    },
    {
        "title": "ASUS Zenbook S 13 OLED",
        "category": "Ноутбуки",
        "price": 1399.0,
        "inventory": 10,
        "description": "Самый тонкий OLED-ноутбук в мире — всего 1 см.",
        "specifications": {
            "Процессор": "Intel Core i7-1355U",
            "ОЗУ": "16 ГБ",
            "Накопитель": "1 ТБ SSD",
            "Экран": "13.3 OLED 2.8K",
            "Вес": "1.0 кг"
        }
    },
    {
        "title": "Lenovo IdeaPad Slim 3",
        "category": "Ноутбуки",
        "price": 520.0,
        "inventory": 30,
        "description": "Сбалансированный ноутбук для дома.",
        "specifications": {
            "Процессор": "AMD Ryzen 3 7320U",
            "ОЗУ": "8 ГБ",
            "Накопитель": "512 ГБ SSD",
            "Экран": "15.6 IPS FHD",
            "ОС": "Windows 11 S"
        }
    },
    {
        "title": "Apple MacBook Air 13 M2",
        "category": "Ноутбуки",
        "price": 1099.0,
        "inventory": 22,
        "description": "Тонкий, легкий и абсолютно бесшумный ноутбук.",
        "specifications": {
            "Процессор": "Apple M2 (8 ядер)",
            "ОЗУ": "8 ГБ",
            "Накопитель": "256 ГБ SSD",
            "Экран": "13.6 Liquid Retina",
            "Охлаждение": "Пассивное"
        }
    },
    {
        "title": "HP Omen 16",
        "category": "Ноутбуки",
        "price": 1550.0,
        "inventory": 9,
        "description": "Серьезная игровая станция строгой эстетики.",
        "specifications": {
            "Процессор": "AMD Ryzen 7 7840HS",
            "Видеокарта": "RTX 4070 8GB",
            "ОЗУ": "16 ГБ",
            "Накопитель": "1 ТБ SSD",
            "Экран": "16.1 QHD 165Hz"
        }
    },

    # --- КАТЕГОРИЯ: СМАРТФОНЫ (15 шт) ---
    {
        "title": "Apple iPhone 15 Pro Max",
        "category": "Смартфоны",
        "price": 1199.0,
        "inventory": 30,
        "description": "Титановый флагман от Apple с 5x оптическим зумом.",
        "specifications": {
            "Процессор": "Apple A17 Pro",
            "Экран": "6.7 OLED 120Hz",
            "Камера": "48+12+12 Мп",
            "Память": "256 ГБ",
            "Корпус": "Титан"
        }
    },
    {
        "title": "Samsung Galaxy S24 Ultra",
        "category": "Смартфоны",
        "price": 1299.0,
        "inventory": 25,
        "description": "Флагман со встроенным стилусом S-Pen и функциями AI.",
        "specifications": {
            "Процессор": "Snapdragon 8 Gen 3",
            "Экран": "6.8 Dynamic AMOLED 2X",
            "Камера": "200+50+12+10 Мп",
            "Память": "512 ГБ",
            "Стилус": "Есть"
        }
    },
    {
        "title": "Google Pixel 8 Pro",
        "category": "Смартфоны",
        "price": 999.0,
        "inventory": 15,
        "description": "Смартфон с лучшими алгоритмами мобильной фотографии.",
        "specifications": {
            "Процессор": "Google Tensor G3",
            "Экран": "6.7 OLED 120Hz",
            "Камера": "50+48+48 Мп",
            "Память": "128 ГБ",
            "ОС": "Android 14 Чистый"
        }
    },
    {
        "title": "Xiaomi 14 Ultra",
        "category": "Смартфоны",
        "price": 1099.0,
        "inventory": 12,
        "description": "Камерофон, разработанный совместно с брендом Leica.",
        "specifications": {
            "Процессор": "Snapdragon 8 Gen 3",
            "Матрица": "1 дюйм Sony LYT-900",
            "Камера": "50+50+50+50 Мп",
            "ОЗУ": "16 ГБ",
            "Зарядка": "90 Вт"
        }
    },
    {
        "title": "POCO X6 Pro 5G",
        "category": "Смартфоны",
        "price": 350.0,
        "inventory": 50,
        "description": "Король производительности в среднем сегменте.",
        "specifications": {
            "Процессор": "MediaTek Dimensity 8300-Ultra",
            "Экран": "6.67 AMOLED 1.5K 120Hz",
            "Память": "256 ГБ",
            "Антуту": "~1.4 млн баллов"
        }
    },
    {
        "title": "Samsung Galaxy A55 5G",
        "category": "Смартфоны",
        "price": 420.0,
        "inventory": 45,
        "description": "Сбалансированный среднебюджетник с влагозащитой IP67.",
        "specifications": {
            "Процессор": "Exynos 1480",
            "Экран": "6.6 Super AMOLED 120Hz",
            "Камера": "50+12+5px",
            "Влагозащита": "IP67",
            "Материал": "Стекло и металл"
        }
    },
    {
        "title": "OnePlus 12",
        "category": "Смартфоны",
        "price": 799.0,
        "inventory": 14,
        "description": "Флагман-убийца с ярчайшим экраном и быстрой зарядкой 100W.",
        "specifications": {
            "Процессор": "Snapdragon 8 Gen 3",
            "Зарядка": "100W SuperVOOC",
            "Батарея": "5400 мАч",
            "Экран": "6.82 BOE X1 2K"
        }
    },
    {
        "title": "Realme GT 6",
        "category": "Смартфоны",
        "price": 590.0,
        "inventory": 20,
        "description": "Смартфон с AI-функциями экрана и рекордной яркостью 6000 нит.",
        "specifications": {
            "Процессор": "Snapdragon 7+ Gen 3",
            "Яркость пиковая": "6000 нит",
            "Зарядка": "120 Вт",
            "Камера": "50 Мп Sony LYT-600"
        }
    },
    {
        "title": "Nothing Phone (2)",
        "category": "Смартфоны",
        "price": 649.0,
        "inventory": 11,
        "description": "Уникальный прозрачный дизайн и интерфейс подсветки Glyph.",
        "specifications": {
            "Процессор": "Snapdragon 8+ Gen 1",
            "Экран": "6.7 LTPO OLED",
            "Интерфейс": "Glyph 2.0",
            "Память": "256 ГБ",
            "ОС": "Nothing OS"
        }
    },
    {
        "title": "Apple iPhone 13 (128GB)",
        "category": "Смартфоны",
        "price": 599.0,
        "inventory": 35,
        "description": "Народный хит, не теряющий актуальности.",
        "specifications": {
            "Процессор": "Apple A15 Bionic",
            "Экран": "6.1 Super Retina XDR",
            "Камера": "12+12 Мп",
            "Память": "128 ГБ"
        }
    },
    {
        "title": "Infinix NOTE 40 Pro",
        "category": "Смартфоны",
        "price": 260.0,
        "inventory": 60,
        "description": "Смартфон со скругленным 3D-экраном и беспроводной магнитной зарядкой.",
        "specifications": {
            "Процессор": "MediaTek Helio G99 Ultimate",
            "Экран": "6.78 AMOLED 120Hz Curved",
            "Зарядка беспроводная": "20 Вт MagCharge",
            "Камера": "108 Мп"
        }
    },
    {
        "title": "Sony Xperia 1 V",
        "category": "Смартфоны",
        "price": 949.0,
        "inventory": 6,
        "description": "Премиум смартфон для энтузиастов кино и аудио 4K.",
        "specifications": {
            "Процессор": "Snapdragon 8 Gen 2",
            "Экран": "6.5 4K OLED 21:9",
            "Разъем Jack 3.5mm": "Есть",
            "Слот MicroSD": "До 1 ТБ"
        }
    },
    {
        "title": "ASUS ROG Phone 8",
        "category": "Смартфоны",
        "price": 999.0,
        "inventory": 8,
        "description": "Экстремальный геймерский смартфон с триггерами.",
        "specifications": {
            "Процессор": "Snapdragon 8 Gen 3",
            "ОЗУ": "16 ГБ",
            "Экран": "6.78 AMOLED 165Hz",
            "Кулер AirTrigger": "Сенсорные зоны"
        }
    },
    {
        "title": "Motorola Edge 50 Pro",
        "category": "Смартфоны",
        "price": 699.0,
        "inventory": 13,
        "description": "Невероятная задняя панель из экокожи с ароматом парфюма из коробки.",
        "specifications": {
            "Процессор": "Snapdragon 7 Gen 3",
            "Экран": "6.7 pOLED 144Hz",
            "Зарядка": "125 Вт TurboPower",
            "Защита корпуса": "IP68"
        }
    },
    {
        "title": "Redmi Note 13 Pro 4G",
        "category": "Смартфоны",
        "price": 240.0,
        "inventory": 70,
        "description": "Популярнейший аппарат с крутой камерой 200 Мп.",
        "specifications": {
            "Процессор": "MediaTek Helio G99 Ultra",
            "Камера": "200 Мп с OIS",
            "Экран": "6.67 AMOLED",
            "Батарея": "5000 мАч"
        }
    },

    # --- КАТЕГОРИЯ: КОМПЛЕКТУЮЩИЕ И МОНИТОРЫ (20 шт) ---
    {
        "title": "Монитор ASUS TUF Gaming VG27AQ",
        "category": "Мониторы",
        "price": 320.0,
        "inventory": 15,
        "description": "Игровой IPS монитор высокого разрешения.",
        "specifications": {
            "Диагональ": "27 дюймов",
            "Матрица": "IPS",
            "Разрешение": "2K QHD 2560x1440",
            "Частота": "165 Гц",
            "Время отклика": "1 мс"
        }
    },
    {
        "title": "Видеокарта NVIDIA RTX 4070 Ti Super",
        "category": "Комплектующие",
        "price": 849.0,
        "inventory": 10,
        "description": "Отличная видеокарта для гейминга в 2K и 4K.",
        "specifications": {
            "Объем видеопамяти": "16 ГБ",
            "Тип памяти": "GDDR6X",
            "Шина данных": "256 бит",
            "Интерфейс": "PCI-E 4.0"
        }
    },
    {
        "title": "Процессор AMD Ryzen 7 7800X3D",
        "category": "Комплектующие",
        "price": 399.0,
        "inventory": 20,
        "description": "Лучший в мире игровой процессор с технологией 3D V-Cache.",
        "specifications": {
            "Сокет": "AM5",
            "Количество ядер": "8",
            "Потоков": "16",
            "Кэш L3": "96 МБ",
            "Техпроцесс": "5 нм"
        }
    },
    {
        "title": "Накопитель SSD Samsung 990 PRO 2TB",
        "category": "Комплектующие",
        "price": 180.0,
        "inventory": 35,
        "description": "Высокоскоростной твердотельный накопитель NVMe M.2.",
        "specifications": {
            "Объем": "2 ТБ",
            "Форм-фактор": "M.2 2280",
            "Скорость чтения": "До 7450 МБ/с",
            "Скорость записи": "До 6900 МБ/с"
        }
    },
    {
        "title": "Оперативная память G.Skill Trident Z5 RGB 32GB",
        "category": "Комплектующие",
        "price": 140.0,
        "inventory": 25,
        "description": "Комплект скоростной премиальной памяти DDR5.",
        "specifications": {
            "Объем": "32 ГБ (2x16GB)",
            "Тип памяти": "DDR5",
            "Частота": "6000 МГц",
            "Тайминги": "CL30-40-40-96"
        }
    },
    {
        "title": "Блок питания Corsair RM850x Shift",
        "category": "Комплектующие",
        "price": 160.0,
        "inventory": 15,
        "description": "Модульный блок питания со специфическим боковым расположением разъемов.",
        "specifications": {
            "Мощность": "850 Вт",
            "Сертификат": "80 PLUS Gold",
            "Кабели": "Полностью модульные",
            "Стандарт": "ATX 3.0 (PCIe 5.0)"
        }
    },
    {
        "title": "Материнская плата MSI MAG B650 TOMAHAWK WIFI",
        "category": "Комплектующие",
        "price": 220.0,
        "inventory": 18,
        "description": "Топовая плата среднего класса для процессоров Ryzen.",
        "specifications": {
            "Чипсет": "AMD B650",
            "Форм-фактор": "ATX",
            "Поддержка ОЗУ": "DDR5",
            "Беспроводная связь": "Wi-Fi 6E + Bluetooth 5.3"
        }
    },
    {
        "title": "Кулер для процессора Deepcool AK620 Digital",
        "category": "Комплектующие",
        "price": 80.0,
        "inventory": 30,
        "description": "Двухбашенный суперкулер со встроенным ЖК-дисплеем мониторинга.",
        "specifications": {
            "Тип": "Воздушный (Башня)",
            "Рассеиваемая мощность": "260 Вт TPD",
            "Вентиляторы": "2x120мм",
            "Дисплей температуры": "Есть"
        }
    },
    {
        "title": "Корпус LIAN LI PC-O11 Dynamic EVO",
        "category": "Комплектующие",
        "price": 190.0,
        "inventory": 12,
        "description": "Премиальный корпус-аквариум из закаленного стекла.",
        "specifications": {
            "Форм-фактор": "Mid-Tower",
            "Материалы": "Сталь + Закаленное стекло",
            "Расположение БП": "Двухкамерный дизайн"
        }
    },
    {
        "title": "Процессор Intel Core i5-14600K",
        "category": "Комплектующие",
        "price": 340.0,
        "inventory": 22,
        "description": "Сбалансированный процессор 14-го поколения.",
        "specifications": {
            "Сокет": "LGA1700",
            "Ядер всего": "14 (6P + 8E)",
            "Потоков": "20",
            "Частота макс": "5.3 ГГц"
        }
    },
    {
        "title": "Монитор LG UltraGear 34GN850-B",
        "category": "Мониторы",
        "price": 690.0,
        "inventory": 5,
        "description": "Широкоформатный изогнутый UltraWide гейминг монитор.",
        "specifications": {
            "Диагональ": "34 дюйма",
            "Разрешение": "UWQHD 3440x1440",
            "Соотношение сторон": "21:9",
            "Радиус изгиба": "1900R"
        }
    },
    {
        "title": "Система водяного охлаждения NZXT Kraken Elite 360",
        "category": "Комплектующие",
        "price": 280.0,
        "inventory": 8,
        "description": "СЖО замкнутого цикла с большим круглым экраном на помпе.",
        "specifications": {
            "Размер радиатора": "360 мм",
            "Вентиляторы": "3x120мм Static Pressure",
            "Дисплей на помпе": "2.36 дюйма LCD custom GIF"
        }
    },
    {
        "title": "Материнская плата ASUS ROG STRIX Z790-F GAMING",
        "category": "Комплектующие",
        "price": 410.0,
        "inventory": 10,
        "description": "Флагманская плата для разгона процессоров Intel Intel.",
        "specifications": {
            "Чипсет": "Intel Z790",
            "Питание VRM": "16+1 фаза",
            "Слоты M.2 NVMe": "4 слота",
            "Звук": "ROG SupremeFX"
        }
    },
    {
        "title": "Термопаста Arctic MX-6 (4g)",
        "category": "Комплектующие",
        "price": 12.0,
        "inventory": 200,
        "description": "Эффективный термоинтерфейс для CPU и GPU.",
        "specifications": {
            "Вес": "4 грамма",
            "Вязкость": "45000 Па*с",
            "Электропроводность": "Нет (Безопасная)"
        }
    },
    {
        "title": "Жесткий диск WD Purple 4TB",
        "category": "Комплектующие",
        "price": 110.0,
        "inventory": 25,
        "description": "Специализированный HDD для систем видеонаблюдения и NAS.",
        "specifications": {
            "Объем": "4 ТБ",
            "Скорость вращения": "5400 об/мин",
            "Кэш память": "256 МБ",
            "Интерфейс": "SATA III"
        }
    },
    {
        "title": "Звуковая карта Creative Sound BlasterX G6",
        "category": "Комплектующие",
        "price": 150.0,
        "inventory": 14,
        "description": "Внешний игровой ЦАП и дискретный усилитель наушников.",
        "specifications": {
            "Тип": "Внешняя (USB)",
            "ЦАП": "32-бит / 384 кГц",
            "Усилитель Xamp": "Дискретный для каждого канала",
            "Доп выходы": "Оптический Toslink"
        }
    },
    {
        "title": "Сетевая карта ASUS PCE-AX58BT",
        "category": "Комплектующие",
        "price": 65.0,
        "inventory": 30,
        "description": "Плата расширения PCI-E со скоростным Wi-Fi 6.",
        "specifications": {
            "Стандарт": "Wi-Fi 6 (802.11ax)",
            "Частотные диапазоны": "2.4 ГГц + 5 ГГц",
            "Bluetooth": "Версия 5.0",
            "Антенны": "Внешняя база"
        }
    },
    {
        "title": "Монитор Samsung Odyssey G7",
        "category": "Мониторы",
        "price": 550.0,
        "inventory": 7,
        "description": "Суперизогнутый игровой QLED монитор.",
        "specifications": {
            "Диагональ": "27 дюймов",
            "Радиус изгиба": "1000R Экстремальный",
            "Разрешение": "2K QHD",
            "Частота": "240 Гц",
            "Матрица": "VA QLED"
        }
    },
    {
        "title": "Вентилятор для корпуса Noctua NF-A12x25 PWM",
        "category": "Комплектующие",
        "price": 35.0,
        "inventory": 80,
        "description": "Легендарный эталон тишины и воздушного давления.",
        "specifications": {
            "Размер": "120x120x25 мм",
            "Тип подшипника": "SSO2 гидродинамический",
            "Обороты": "450 - 2000 RPM",
            "Шум": "Макс 22.6 дБ"
        }
    },
    {
        "title": "Коврик для мыши SteelSeries QcK L",
        "category": "Комплектующие",
        "price": 25.0,
        "inventory": 100,
        "description": "Тканевый игровой коврик большой площади.",
        "specifications": {
            "Размер": "450 x 400 мм",
            "Толщина": "2 мм",
            "Материал поверхности": "Микрофибра",
            "Основание": "Резина"
        }
    }
]


def seed_products():
    """Заполняет базу данных товарами, если она пустая."""
    db: Session = SessionLocal()

    try:
        # Проверяем, есть ли уже товары в базе данных
        if db.query(Product).count() == 0:
            print(
                "📦 Инициализация базы данных: "
                "Наполнение каталога товарами..."
            )

            for item in BIG_CATALOG:
                product = Product(**item)
                db.add(product)

            db.commit()

            print(
                f" [✓] Каталог успешно заполнен "
                f"({len(BIG_CATALOG)} товаров добавлено)!"
            )

        else:
            print(
                " [i] База данных товаров уже содержит записи. "
                "Пропуск автозаполнения."
            )

    except Exception as e:
        print(f" [!] Ошибка при автозаполнении каталога: {e}")

    finally:
        db.close()