# [image_analyzer.py] - AI 이미지 분석 모듈 (v16)
import os
import config
import utils
from pathlib import Path
#-----------------------------------------
# 라이브러리 로드 및 상태 체크
# [개선] 라이브러리 로드 실패 시에도 시스템이 계속 작동하도록 예외 처리 강화
# [개선] 각 라이브러리 로드 시 상세 오류 로그 기록
# [개선] 이미지 분석에 필요한 라이브러리 로드 시도 및 상태 플래그 설정
#-----------------------------------------
AI_READY = False
TF_READY = False
GPU_ACTIVE = False
#-----------------------------------------
# [개선] 라이브러리 로드 실패 시에도 시스템이 계속 작동하도록 예외 처리 강화
# [개선] 각 라이브러리 로드 시 상세 오류 로그 기록
# [개선] 이미지 분석에 필요한 라이브러리 로드 시도 및 상태 플래그 설정
#-----------------------------------------
try:
    import numpy as np
    from PIL import Image, UnidentifiedImageError
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus: tf.config.experimental.set_memory_growth(gpu, True)
        GPU_ACTIVE = True
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
    TF_READY = True
    AI_READY = True
except Exception as e:
        utils.log_message(f"이미지 초기화 오류 : {e}", "ERROR")
        pass

model = None
#-----------------------------------------
# TF 모델 로드 함수
# [개선] TF 모델 로드 함수 개선하여 모델이 준비된 경우에만
# [개선] TF 모델 로드 함수 개선하여 모델 로딩 중 발생하는 오류는 로그에 기록하되, 시스템이 계속 작동하도록 예외 처리 강화
#-----------------------------------------
def load_tf_model():
    global model
    if not TF_READY: return
    try:
        model = MobileNetV2(weights='imagenet')
    except Exception as e:
        utils.log_message(f"TF 모델 로딩 실패: {e}", "ERROR")
# --------------------------------
# [핵심] 이미지 분석 및 분류 함수
# [개선] 이미지 분석 및 분류 함수 개선하여 키워드 기반 분류를 먼저 수행하도록 개선 (신분증 등 중요 문서 보호)
# [개선] 이미지 분석 및 분류 함수 개선하여 AI 정밀 분석은 모델이 준비된 경우에만 수행하도록 개선
# [개선] 이미지 분석 및 분류 함수 개선하여 분석 중 발생하는 오류는 로그에 기록하되, 시스템이 계속 작동하도록 예외 처리 강화
#-----------------------------------------
AI_CATEGORIES = {
    "01_중요문서_및_행정": ["envelope", "web_site", "menu", "book_jacket", "crossword_puzzle", "id_card", "passport", "comic_book", "street_sign", "street_art", "bulletin_board", "notebook", "comic_strip", "scoreboard", "traffic_light", "traffic_sign", "parking_meter", "mailbox", "postbox"],
    "02_동물_및_생물": ["dog", "cat", "bird", "fish", "butterfly", "insect", "animal", "pet", "lion", "tiger", "bear", "zebra", "giraffe", "monkey", "horse", "cow", "sheep", "elephant", "panda", "koala"],
    "03_풍경_및_자연": ["valley", "mountain", "alp", "volcano", "promontory", "lakeside", "seashore", "ocean", "tree", "forest", "sky", "cloud"],
    "04_음식_및_요리": ["food", "plate", "dish", "burrito", "pizza", "guacamole", "ice_cream", "bakery", "cake", "fruit", "hotdog", "sandwich", "steak", "pasta", "sushi", "egg", "coffee", "tea"],
    "05_가구_및_사물": ["desk", "table", "chair", "laptop", "monitor", "mouse", "keyboard", "cellular_telephone", "car", "bicycle", "sofa", "bed", "toilet", "refrigerator", "microwave", "oven", "toaster", "sink", "bookcase"],
    "06_인물_이미지": ["person", "portrait", "selfie", "face", "man", "woman", "child", "baby", "bride", "groom", "athlete", "performer", "celebrity", "model", "worker", "student"],
    "07_기타_이미지": [ "clothing", "footwear", "accessory", "sports_equipment", "musical_instrument", "tool", "appliance", "electronic_device", "furniture", "artwork", "logo", "symbol"]
}
# ----------------------------------------
# [핵심] 이미지 분석 및 분류 함수
# [개선] 이미지 분석 및 분류 함수 개선하여 키워드 기반 분류를 먼저 수행하도록 개선 (신분증 등 중요 문서 보호)
# [개선] 이미지 분석 및 분류 함수 개선하여 AI 정밀 분석은 모델이 준비된 경우에만 수행하도록 개선
# [개선] 이미지 분석 및 분류 함수 개선하여 분석 중 발생하는 오류는 로그에 기록하되, 시스템이 계속 작동하도록 예외 처리 강화
#-----------------------------------------
def analyze_image_final(image_path):
    try:
        if image_path.name in config.EXCLUDE_LIST: return None
        # 1단계: 키워드 기반 분류 (신분증 등 중요 문서 보호)
        name = image_path.name.lower()
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in name for kw in kws): return folder
        
        # 2단계: AI 정밀 분석 (모델이 준비된 경우에만)
        if TF_READY:
            try:
                # 이미지 열기 및 손상 여부 검사
                #   - (파일이 깨짐, 확장자만 PNG, Windows 스크린샷 버그, 파일 잠김, Pillow가 특정 PNG 못 읽는 경우 있음.)
                img = Image.open(image_path)
                # 진짜 이미지 검사
                img.verify()
                # 다시 열기
                img = Image.open(image_path).convert('RGB')
            except UnidentifiedImageError:
                utils.log_error( f"손상 이미지: {image_path}" )
                return "99_손상된_이미지"
            if model is None: load_tf_model()
            img = Image.open(image_path).convert('RGB').resize((224, 224))
            x = preprocess_input(np.expand_dims(tf.keras.preprocessing.image.img_to_array(img), axis=0))
            preds = model.predict(x, verbose=0)
            label = decode_predictions(preds, top=1)[0][0][1].lower()
            results = decode_predictions(preds, top=3)[0]
            
            for _, label, score in results:
                label = label.lower()
                for category, keywords in AI_CATEGORIES.items():
                    if any(kw in label for kw in keywords):
                        return category
    except Exception as e:
        utils.log_message(f"이미지 분석 오류 ({image_path.name}): {e}", "ERROR")
    # AI 결과가 어떤 카테고리에도 없으면 기본적으로 기타 이미지로 분류
    return  label if TF_READY else "09_일반_사진"
# ----------------------------------------
# [핵심] 이미지 분석 및 분류 실행 함수
# [개선] 이미지 분석 및 분류 함수 개선하여 키워드 기반 분류를 먼저 수행하도록 개선 (신분증 등 중요 문서 보호)
# [개선] 이미지 분석 및 분류 함수 개선하여 AI 정밀 분석은 모델이 준비된 경우에만 수행하도록 개선
# [개선] 이미지 분석 및 분류 함수 개선하여 분석 중 발생하는 오류는 로그에 기록하되, 시스템이 계속 작동하도록 예외 처리 강화
#-----------------------------------------  
# def run_image_ai_organizing(target_path):
#     result_root = utils.get_ai_result_root(target_path)
#     target = Path(target_path)
#     count = 0
#     #ai_root = target / "AI_TF_분석결과"
#     ai_root = utils.get_ai_result_root(target_path)
#     print("🧠 AI 이미지 정밀 분석 및 분류 중...")

#     try:
#         pattern = '**/*' if (config.RECURSIVE_SCAN or config.UNPACK_ALL) else '*'
#         #files = [f for f in target.glob(pattern) if f.is_file() and f.suffix.lower() in config.IMAGE_EXTENSIONS]
#         #all_files = utils.get_initial_files( )

#         #files = [ f for f in all_files if f.suffix.lower() in config.IMAGE_EXTENSIONS]
#         files = [ f for f in utils.get_initial_files() if f.suffix.lower() in config.IMAGE_EXTENSIONS]
#         for item in files:
#             if item.name in config.EXCLUDE_LIST: continue
#             # 이미 분류된 폴더 제외 (해체 모드가 아닐 때)
#             if not config.UNPACK_ALL:
#                 if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹')) for p in item.parents if p != target):
#                     continue
#             category = analyze_image_final(item)
#             # 1단계: 키워드 기반 분류 (신분증 등 중요 문서 보호)
#             sw = True
#             #name = target_path.path.name.lower()
#             for folder, kws in config.KEYWORD_RULES.items():
#                 if any(kw.lower() in category for kw in kws):
#                     sw = False
#                     break
#             # AI 분석 결과에 따른 분류 (AI 카테고리에 해당하면 AI 폴더로, 아니면 일반 폴더로)
#             # [개선] 이미지 분석 및 분류 함수 개선하여 AI 분석 결과에 따른 분류 (AI 카테고리에 해당하면 AI 폴더로, 아니면 일반 폴더로) 개선하여 AI 카테고리에 해당하는 경우는 AI_TF_분석결과 폴더로 이동하도록 개선
#             # # [개선] 이미지 분석 및 분류 함수 개선하여 AI 분석 결과에 따른 분류 (AI 카테고리에 해당하면 AI 폴더로, 아니면 일반 폴더로) 개선하여 AI 카테고리에 해당하는 경우는 AI_TF_분석결과 폴더로 이동하도록 개선
#             #   - (카테고리명에 날짜/시간 패턴이 포함된 경우, 패턴을 제거하고 카테고리명만 폴더 이름에 포함하도록 개선)
#             if category in AI_CATEGORIES and sw:
#                 utils.move_file(item, ai_root / category)
#             else:
#                 target = result_root / category
#                 utils.move_file(item, target )
#             count += 1
#     except Exception as e:
#         utils.log_message(f"이미지 프로세스 오류: {e}", "ERROR")
#     return count
def run_image_ai_organizing(target_path):
    # --------------------------------
    # AI 결과 루트
    # --------------------------------
    result_root = utils.get_ai_result_root( target_path )
    base_path = Path(target_path)
    count = 0
    print("🧠 AI 이미지 정밀 분석 및 분류 중...")
    utils.log_message( "🧠 AI 이미지 정밀 분석 및 분류 중...", "INFO" )
    try:
        # --------------------------------
        # 최초 상태 파일만 탐색
        # --------------------------------
        files = [ f for f in utils.get_initial_files() if ( f.suffix.lower() in config.IMAGE_EXTENSIONS ) ]
        for item in files:
            try:
                # 제외 경로
                if utils.is_excluded(item):
                    continue
                # # 결과 폴더 재탐색 방지
                # if not config.UNPACK_ALL:
                #     if any( p.name.startswith( config.SKIP_FOLDERS ) for p in item.parents if p != base_path ):
                #         continue
                # --------------------------------
                # 이미 정리된 폴더 제외
                # --------------------------------
                if any( p.name.startswith(config.SKIP_FOLDERS) for p in item.parents if p != base_path ):
                    continue
                # --------------------------------
                # AI 이미지 분석
                # --------------------------------
                category = analyze_image_final( item )
                # --------------------------------
                # 키워드 보호 규칙
                # --------------------------------
                sw = True
                for folder, kws in ( config.KEYWORD_RULES.items() ):
                    if any( kw.lower() in category.lower() for kw in kws ):
                        sw = False
                        break
                # --------------------------------
                # 대상 폴더 ←————— # AI 결과 저장 경로
                # --------------------------------
                # dest_dir = ( result_root / category )

                # --------------------------------
                # AI 분석 결과 폴더
                # --------------------------------
                if ( category in config.AI_CATEGORIES.keys() and sw ):

                    # AI 전용 결과 폴더
                    dest_dir = ( result_root / category )
                else:
                    # 일반 분류 폴더
                    dest_dir = ( base_path / category )
                # --------------------------------
                # 파일 이동
                # --------------------------------
                utils.move_file( item, dest_dir )
                count += 1
            except Exception as e:
                utils.log_error( f"이미지 처리 실패 ({item}): {e}" )
    except Exception as e:
        utils.log_message( f"이미지 프로세스 오류: {e}", "ERROR" )
    return count