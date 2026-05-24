# import tensorflow

# #print(tf.config.list_physical_devices('GPU'))
# import pytesseract

# patients = [
#     {"name": "김환자", "age": 65, "systolic": 145},
#     {"name": "이환자", "age": 45, "systolic": 125},
#     {"name": "박환자", "age": 32, "systolic": 115},
#     {"name": "최환자", "age": 28, "systolic": 135},
#     {"name": "정환자", "age": 70, "systolic": 190}
# ]

# # 여기에 코드를 작성하세요

# Norma_Systolic = 120
# Prehyper_Systolic = 140
# Stage1_Systolic = 160

# systolics = [patient["systolic"] for patient in patients]#patients.get('systolic')

# print(systolics)

# systolics =[ i+10 for i in range(10)] #[patient["systolic"] for patient in patients]#patients.get('systolic')

# print(systolics)

# result = [(f"{x}x{y}={x*y}" for x in range(2, 9) for y in range(1, 9)) if y % 9 == 0 else f"{'\\n'}"]

# print(result)
# import tensorflow as tf

# print("TF 버전:", tf.__version__)
# print("CUDA 지원:", tf.test.is_built_with_cuda())
# print("GPU 목록:", tf.config.list_physical_devices('GPU'))

AI_CATEGORIES = {
    "01_중요문서_및_행정": ["envelope", "web_site", "menu", "book_jacket", "crossword_puzzle", "id_card", "passport", "comic_book", "street_sign", "street_art", "bulletin_board", "notebook", "comic_strip", "scoreboard", "traffic_light", "traffic_sign", "parking_meter", "mailbox", "postbox"],
    "02_동물_및_생물": ["dog", "cat", "bird", "fish", "butterfly", "insect", "animal", "pet", "lion", "tiger", "bear", "zebra", "giraffe", "monkey", "horse", "cow", "sheep", "elephant", "panda", "koala"],
    "03_풍경_및_자연": ["valley", "mountain", "alp", "volcano", "promontory", "lakeside", "seashore", "ocean", "tree", "forest", "sky", "cloud"],
    "04_음식_및_요리": ["food", "plate", "dish", "burrito", "pizza", "guacamole", "ice_cream", "bakery", "cake", "fruit", "hotdog", "sandwich", "steak", "pasta", "sushi", "egg", "coffee", "tea"],
    "05_가구_및_사물": ["desk", "table", "chair", "laptop", "monitor", "mouse", "keyboard", "cellular_telephone", "car", "bicycle", "sofa", "bed", "toilet", "refrigerator", "microwave", "oven", "toaster", "sink", "bookcase"],
    "06_인물_이미지": ["person", "portrait", "selfie", "face", "man", "woman", "child", "baby", "bride", "groom", "athlete", "performer", "celebrity", "model", "worker", "student"],
    "07_기타_이미지": [ "clothing", "footwear", "accessory", "sports_equipment", "musical_instrument", "tool", "appliance", "electronic_device", "furniture", "artwork", "logo", "symbol"]
}

person_keywords = (
    AI_CATEGORIES["06_인물_이미지"]
)

PERSON_KEYWORDS = AI_CATEGORIES.get(
    "06_인물_이미지",
    []
) 
print(PERSON_KEYWORDS)
print("인물 이미지 키워드:", PERSON_KEYWORDS)