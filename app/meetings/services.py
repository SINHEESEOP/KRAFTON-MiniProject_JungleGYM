import requests

def search_address_by_kakao(address):
    # 카카오 REST API 키 (여기에 본인의 키를 넣으세요)
    KAKAO_API_KEY = '94b797812acad4bfe4727e6d3ef89e75'
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        if result['documents']:
            address_info = result['documents'][0]  # 첫 번째 검색 결과
            print(f"주소: {address_info['address_name']}")
            print(f"위도: {address_info['y']}, 경도: {address_info['x']}")
            return address_info
        else:
            print("검색 결과가 없습니다.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# 주소 검색 예시
search_address_by_kakao('서울특별시 강남구 삼성동 100')
# 91cc5e295563f8e78c0e7a0d50f72c5f
# 94b797812acad4bfe4727e6d3ef89e75