import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 수집할 카테고리 리스트 및 한국어 매핑
find_list = [
    'FoodImageListR',       # 식량작물
    'FruitImageListR',      # 과수
    'VegitablesImageListR',# 채소
    'FlowerImageListR',     # 화훼
    'SpecialImageListR',    # 특용작물
    'WeedsImgSearchR'       # 잡초
]

category_names = {
    'FoodImageListR': '식량작물',
    'FruitImageListR': '과수',
    'VegitablesImageListR': '채소',
    'FlowerImageListR': '화훼',
    'SpecialImageListR': '특용작물',
    'WeedsImgSearchR': '잡초'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

all_crops = {}

def clean_crop_name(name):
    # 괄호 및 괄호 안 내용 제거: "작물명(내용)" -> "작물명"
    cleaned = re.sub(r'\([^)]*\)', '', name)
    # 양쪽 공백 제거
    return cleaned.strip()

for category in find_list:
    url = f'https://ncpms.rda.go.kr/npms/{category}.np'
    print(f'🟦 현재 카테고리: {category} ({url})')

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        crop_items = soup.select('ul > li')
        crop_names = []

        for item in crop_items:
            strong_tag = item.find('strong')
            if strong_tag:
                raw_name = strong_tag.get_text(strip=True)
                cleaned_name = clean_crop_name(raw_name)
                crop_names.append(cleaned_name)

        all_crops[category] = crop_names

        for name in crop_names:
            print(f'  - {name}')

    except Exception as e:
        print(f'❌ 오류 발생 ({category}): {e}')

print("\n✅ 모든 카테고리 수집 완료.")

# 엑셀 저장을 위해 DataFrame 생성
df_list = []
for category, crops in all_crops.items():
    # 카테고리명 한글 매핑
    cat_name = category_names.get(category, category)
    for crop in crops:
        df_list.append({'카테고리': cat_name, '작물명': crop})

df = pd.DataFrame(df_list)

# 엑셀 파일로 저장
output_file = '/Users/kimdoyeon/Desktop/nym-data/crop_list.xlsx'
df.to_excel(output_file, index=False)

print(f"✅ 엑셀 파일로 저장 완료: {output_file}")
