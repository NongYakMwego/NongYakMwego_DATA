import pandas as pd
import requests
import re
import time

def remove_parentheses(text):
    return re.sub(r'\s*\(.*?\)', '', str(text)).strip()

df = pd.read_excel('/Users/kimdoyeon/Desktop/nym-data/crop_list.xlsx', engine='openpyxl')
df["원본작물명"] = df["작물명"]
df["제목_정제"] = df["작물명"].apply(remove_parentheses)

all_results = []

for i, row in df.iterrows():
    original_crop = row["원본작물명"]
    cleaned_crop = row["제목_정제"]

    print(f"🔍 '{original_crop}' 처리 중... (검색어: '{cleaned_crop}')")

    url = "http://ncpms.rda.go.kr/npmsAPI/service"
    service_key = "20259e249898f9bd8e7b40b5a5cc3f61ba63"
    params = {
        "apiKey": service_key,
        "serviceCode": "SVC03",
        "serviceType": "AA003",
        "cropName": cleaned_crop,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(response.status_code)
            print(response.url)  # 실제 호출한 URL
            print(response.json())  # API가 응답한 원본 데이터 전체
            data = response.json()
            items = data.get("service", {}).get("list", [])

            if items:
                for item in items:
                    # cropName 소문자 비교로 유연하게 체크 (필요시)
                    if item.get("cropName", "").lower() == cleaned_crop.lower():
                        result_item = {
                            "cropName": item.get("cropName"),
                            "insectKorName": item.get("insectKorName"),
                            "speciesName":item.get("speciesName"),
                            "cropCode": item.get("cropCode"),
                            "oriImg": item.get("oriImg"),
                            "insectKey": item.get("insectKey"),
                            "요청작물명": cleaned_crop,
                            "원본작물명": original_crop
                        }
                        all_results.append(result_item)
                print(f"✅ '{original_crop}' 처리 완료")
            else:
                print(f"⚠️ '{original_crop}' → '{cleaned_crop}' 응답은 정상이나 데이터 없음")
        else:
            print(f"❌ '{original_crop}' API 요청 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ '{original_crop}' 처리 중 오류 발생: {e}")

    time.sleep(0.5)

if all_results:
    result_df = pd.DataFrame(all_results)
    result_df.to_excel("/Users/kimdoyeon/Desktop/nym-data/result_pest.xlsx", index=False)
    print("📁 result.xlsx 저장 완료")
else:
    print("❌ 저장할 데이터가 없습니다.")
