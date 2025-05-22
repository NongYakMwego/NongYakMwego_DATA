import pandas as pd

# 작물 파일 불러오기
df = pd.read_excel('/Users/kimdoyeon/Downloads/crop.xlsx', engine='openpyxl')

# 카테고리, 서브제목1,서브내용2,서브제목3,서브제목4,서브내용4,서브내용5,등록일 제거
delete = ['카테고리', '요약글', '서브제목1', '서브제목2', '서브내용3', '서브내용4', '서브내용2', '서브제목3', '서브제목4', '서브제목5', '서브내용5', '등록일']

for i in delete:
    df = df.drop(columns=[i])

for value in ['제목', '서브내용1']:
    df[value] = df[value].str.replace('<br>', '')

# 제목 중복 시 행 제거
df = df.drop_duplicates(subset='제목')
# 결과 저장
output_path = '/Users/kimdoyeon/Desktop/nym-data/cleaned_crop.xlsx'
df.to_excel(output_path, index=False)

print("파일 정제 완료")
