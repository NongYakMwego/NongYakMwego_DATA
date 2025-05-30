import pandas as pd

# 엑셀 파일 불러오기
df = pd.read_excel('/Users/kimdoyeon/Desktop/nym-data/combined_result.xlsx')

# 문자열 공백을 제거한 후 빈 문자열은 NaN 처리
df['pest-diseaseNameEng'] = df['pest-diseaseNameEng'].astype(str).str.strip().replace('', pd.NA)

# pest-diseaseNameKor별로 비어 있지 않은 첫 번째 pest-diseaseNameEng 값을 찾음
first_valid_eng = (
    df.dropna(subset=['pest-diseaseNameEng'])
      .drop_duplicates(subset=['pest-diseaseNameKor'])[['pest-diseaseNameKor', 'pest-diseaseNameEng']]
)

# 딕셔너리로 매핑
kor_to_eng = dict(zip(first_valid_eng['pest-diseaseNameKor'], first_valid_eng['pest-diseaseNameEng']))

# 기존 df의 pest-diseaseNameEng 열을 위에서 만든 매핑으로 통일
df['pest-diseaseNameEng'] = df['pest-diseaseNameKor'].map(kor_to_eng)

# 결과 저장
df.to_excel('/Users/kimdoyeon/Desktop/nym-data/combined_result_fixed.xlsx', index=False)
