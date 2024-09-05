from .models import Meeting

def create_meeting(
    category, date, time, max_people, location, notice, equipment, leader_info, end_time
):
    new_meeting = Meeting(
        category=category,
        date=date,
        time=time,
        end_time=end_time,
        max_people=max_people,
        location=location,
        notice=notice,
        equipment=equipment,
        leader_info=leader_info
    )
    new_meeting.save()
    return new_meeting


def get_meeting_list():
    return Meeting.get_all_meetings()


def get_meeting_details(meeting_id):
    return Meeting.get_meeting_by_id(meeting_id)


def update_meeting(meeting_id, data):
    meeting = Meeting.get_meeting_by_id(meeting_id)
    if meeting:
        meeting.update(data)
        return meeting
    return None


def delete_meeting(meeting_id):
    return Meeting.delete(meeting_id)

def clean_leader_info(leader_info):
    """MongoDB ObjectId를 문자열로 변환하여 JSON 변환 가능하게 함"""
    if leader_info and '_id' in leader_info:
        leader_info['_id'] = str(leader_info['_id'])
    return leader_info
  

# def search_address_by_kakao(address):
#     # 카카오 REST API 키 (여기에 본인의 키를 넣으세요)
#     KAKAO_API_KEY = '94b797812acad4bfe4727e6d3ef89e75'
#     url = 'https://dapi.kakao.com/v2/local/search/address.json'
#     headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
#     params = {"query": address}

#     response = requests.get(url, headers=headers, params=params)

#     if response.status_code == 200:
#         result = response.json()
#         if result['documents']:
#             address_info = result['documents'][0]  # 첫 번째 검색 결과
#             print(f"주소: {address_info['address_name']}")
#             print(f"위도: {address_info['y']}, 경도: {address_info['x']}")
#             return address_info
#         else:
#             print("검색 결과가 없습니다.")
#             return None
#     else:
#         print(f"Error: {response.status_code}")
#         return None

# # 주소 검색 예시
# search_address_by_kakao('서울특별시 강남구 삼성동 100')
# 91cc5e295563f8e78c0e7a0d50f72c5f
# 94b797812acad4bfe4727e6d3ef89e75
