import pandas as pd
import re

# 파일 경로
input_path = '/Users/kimdoyeon/Desktop/nym-data/cleaned_crop.xlsx'
output_path = '/Users/kimdoyeon/Desktop/nym-data/cleaned_crop_final.xlsx'

# 1. 파일 불러오기
df = pd.read_excel(input_path, engine='openpyxl')

# 2. 괄호 및 괄호 안 내용 제거 함수
def remove_parentheses(text):
    return re.sub(r'\s*\(.*?\)', '', str(text)).strip()

# 3. '제목' 컬럼 정제
df['제목'] = df['제목'].apply(remove_parentheses)

# 4. '제목' 중복된 행 모두 제거
df = df.drop_duplicates(subset='제목', keep='first')


# 5. 결과 저장
df.to_excel(output_path, index=False)
print(f"✅ 괄호 제거 및 중복 작물 제거 완료 → {output_path}")
