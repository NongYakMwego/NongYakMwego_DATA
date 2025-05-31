import pandas as pd
import requests
import time
import xml.etree.ElementTree as ET
import html

# 엑셀 파일 불러오기 (wordNo까지 포함된 파일)
df = pd.read_excel('/Users/kimdoyeon/Desktop/nym-data/crop_list_with_wordno.xlsx', engine='openpyxl')

# 컬럼 추가
df['작물코드'] = None
df['작물설명'] = None

# API 설정
detail_url = "http://api.nongsaro.go.kr/service/farmDic/detailWord"
api_key = "202505277Z6NQU9NKO84B90IZ24FG"

for i, row in df.iterrows():
    word_no = row.get('wordNo')

    if pd.isna(word_no):
        print(f"⚠️ {row['작물명']}: wordNo 없음 - 건너뜀")
        continue

    params = {
        'apiKey': api_key,
        'wordNo': str(int(word_no))  # wordNo는 정수형처럼 보이지만 문자열로 요청
    }

    try:
        response = requests.get(detail_url, params=params)
        if response.status_code == 200:
            root = ET.fromstring(response.content)

            item = root.find('.//item')
            if item is not None:
                crop_code_elem = item.find('farmngWordNo')
                desc_elem = item.find('wordDc')

                crop_code = crop_code_elem.text.strip() if crop_code_elem is not None else ""
                description_raw = desc_elem.text if desc_elem is not None else ""

                # 특수문자(HTML entity) 디코딩
                description_clean = html.unescape(description_raw.strip())

                df.at[i, '작물코드'] = crop_code
                df.at[i, '작물설명'] = description_clean

                print(f"✅ {row['작물명']}: 코드 {crop_code}, 설명 저장 완료")
            else:
                print(f"⚠️ {row['작물명']}: 상세 item 없음")

        else:
            print(f"❌ {row['작물명']}: 응답 코드 {response.status_code}")

    except Exception as e:
        print(f"❌ {row['작물명']} 처리 중 오류 발생: {e}")

    time.sleep(0.5)

# 결과 저장
output_path = '/Users/kimdoyeon/Desktop/nym-data/crop_list_final.xlsx'
df.to_excel(output_path, index=False)
print(f"\n✅ 엑셀 저장 완료: {output_path}")
