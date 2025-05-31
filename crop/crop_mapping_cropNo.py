import pandas as pd
import requests
import time
import xml.etree.ElementTree as ET

# 원본 엑셀 파일 읽기
df = pd.read_excel('/Users/kimdoyeon/Desktop/nym-data/crop_list.xlsx', engine='openpyxl')

# wordNo 컬럼 추가
df['wordNo'] = None

# API 기본 설정
base_url = "http://api.nongsaro.go.kr/service/farmDic/searchEqualWord"
api_key = "202505277Z6NQU9NKO84B90IZ24FG"

for i, row in df.iterrows():
    crop_name = row['작물명']

    params = {
        'apiKey': api_key,
        'word': crop_name
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            root = ET.fromstring(response.content)

            word_no_elem = root.find('.//wordNo')
            if word_no_elem is not None and word_no_elem.text:
                df.at[i, 'wordNo'] = word_no_elem.text.strip()
                print(f"✅ {crop_name}: wordNo {word_no_elem.text.strip()} 추가 완료")
            else:
                print(f"⚠️ {crop_name}: wordNo 없음")

        else:
            print(f"❌ {crop_name}: 응답 코드 {response.status_code}")

    except Exception as e:
        print(f"❌ '{crop_name}' 처리 중 오류 발생: {e}")

    time.sleep(0.5)  # 요청 간 시간 간격 유지

# 결과 엑셀 파일로 저장
df.to_excel('/Users/kimdoyeon/Desktop/nym-data/crop_list_with_wordno.xlsx', index=False)
print("\n✅ 엑셀 저장 완료: crop_list_with_wordno.xlsx")
