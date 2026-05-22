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
import tensorflow as tf

print("TF 버전:", tf.__version__)
print("CUDA 지원:", tf.test.is_built_with_cuda())
print("GPU 목록:", tf.config.list_physical_devices('GPU'))