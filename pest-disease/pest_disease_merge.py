import pandas as pd

# 1. 엑셀 파일 불러오기
df_disease = pd.read_excel('/Users/kimdoyeon/Desktop/nym-data/result_disease.xlsx')
df_pest = pd.read_excel('/Users/kimdoyeon/Desktop/nym-data/result_pest.xlsx')

# 2. 각 데이터프레임의 열 이름 매핑
disease_renamed = df_disease.rename(columns={
    'cropName': 'cropName',
    'sickNameKor': 'pest-diseaseNameKor',
    'sickNameEng': 'pest-diseaseNameEng',
    'oriImg': 'img'
})[['cropName', 'pest-diseaseNameKor', 'pest-diseaseNameEng', 'img']]

pest_renamed = df_pest.rename(columns={
    'cropName': 'cropName',
    'insectKorName': 'pest-diseaseNameKor',
    'speciesName': 'pest-diseaseNameEng',
    'oriImg': 'img'
})[['cropName', 'pest-diseaseNameKor', 'pest-diseaseNameEng', 'img']]

# 3. 두 데이터프레임 세로로 합치기
combined_df = pd.concat([disease_renamed, pest_renamed], ignore_index=True)

# 4. 결과를 엑셀 파일로 저장
combined_df.to_excel('/Users/kimdoyeon/Desktop/nym-data/combined_result.xlsx', index=False)

print("✅ 엑셀 파일이 성공적으로 병합 및 저장되었습니다: combined_result.xlsx")

