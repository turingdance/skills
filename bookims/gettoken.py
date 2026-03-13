import os
import requests
import json
from datetime import datetime, timedelta
CACHE_FILE = "turingdance_bookims_token_cache.json"

def get_access_token():
    """同步获取access token，持久化文件缓存（有效期1天）"""
    now = datetime.now()
    
    # ========== 1. 读取文件缓存 ==========
    token = None
    expire_at = None
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
            token = cache_data.get("token")
            # 将字符串格式的时间戳转回datetime对象
            expire_at_str = cache_data.get("expire_at")
            if expire_at_str:
                expire_at = datetime.fromisoformat(expire_at_str)
    
    # 检查缓存是否有效
    if token and expire_at and now < expire_at:
        return token
    
    # ========== 2. 重新请求token ==========
    # 读取环境变量（和之前逻辑一致）
    host = os.getenv("TURINGDANCE_BOOKIMS_HOST")
    app_key = os.getenv("TURINGDANCE_BOOKIMS_APPKEY")
    app_secret = os.getenv("TURINGDANCE_BOOKIMS_APPSECRET")
    if not all([host, app_key, app_secret]):
        raise ValueError("环境变量 TURINGDANCE_BOOKIMS_HOST/TURINGDANCE_BOOKIMS_APPKEY/TURINGDANCE_BOOKIMS_APPSECRET 不能为空")
    
    url = f"{host}/uc/user/accessToken"
    payload = {"appKey": app_key, "appSecret": app_secret}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 200:
            raise RuntimeError(f"获取token失败：{result}")
        token = result.get("token")
        if not token:
            raise RuntimeError("响应无token")
        
        # ========== 3. 写入文件缓存 ==========
        expire_at = now + timedelta(days=1)
        cache_data = {
            "token": token,
            "expire_at": expire_at.isoformat()  # 转为字符串存储
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f)
        
        return token
    
    except Exception as e:
        # 异常时删除缓存文件，避免脏数据
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        raise

# 测试示例
# def test():
#     try:
#         # 第一次请求：从接口获取token
#         token = get_access_token()
#         #print(f"首次获取token：{token}")
#         # 第二次请求：验证缓存生效（直接返回缓存）
#         token2 = get_access_token()
#         #print(f"缓存获取token：{token2}")
#         #print(f"两次token是否一致：{token == token2}")
#     except Exception as e:
#         print(f"错误：{str(e)}")

# if __name__ == "__main__":
#     # 测试用：先设置环境变量（实际部署时从系统环境变量读取）
#     # os.environ["TURINGDANCE_BOOKIMS_HOST"] = "http://127.0.0.1:8085"
#     # os.environ["TURINGDANCE_BOOKIMS_APPKEY"] = "2031655939660189696"
#     # os.environ["TURINGDANCE_BOOKIMS_APPSECRET"] = "e030nh6hnc8lvxmi6bwia1yru0uv28re"
#     # 执行测试
#     #test()
#     #token = get_access_token()
#     print("run success √")